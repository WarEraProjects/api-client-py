import os
import re

RESOURCE_DIR = "warera/resources"


def process_file(filepath):
    with open(filepath) as f:
        lines = f.readlines()

    out_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("from .._pagination import auto_paginate_pages"):
            i += 1
            continue

        # Remove auto_paginate: bool = False, from main implementation
        if "auto_paginate: bool = False," in line:
            i += 1
            continue

        # Handle the True overload
        if "auto_paginate: typing.Literal[True]," in line:
            out_lines.append(
                line.replace(
                    "auto_paginate: typing.Literal[True],", "auto_items: typing.Literal[True],"
                )
            )
            i += 1
            if i < len(lines) and "auto_items: bool = False," in lines[i]:
                i += 1
            continue

        # Handle the False overload
        if "auto_paginate: typing.Literal[False] = False," in line:
            out_lines.append(
                line.replace(
                    "auto_paginate: typing.Literal[False] = False,",
                    "auto_items: typing.Literal[False] = False,",
                )
            )
            i += 1
            if i < len(lines) and "auto_items: bool = False," in lines[i]:
                i += 1
            continue

        # Modify return type of True overload
        if ") -> AsyncIterator[CursorPage[" in line:
            out_lines.append(
                line.replace(") -> AsyncIterator[CursorPage[", ") -> AsyncIterator[").replace(
                    "]]: ...", "]: ..."
                )
            )
            i += 1
            continue

        # Remove the union of the return type in the main method
        if " | AsyncIterator[CursorPage[" in line:
            new_line = re.sub(r" \| AsyncIterator\[CursorPage\[[^\]]+\]\]", "", line)
            out_lines.append(new_line)
            i += 1
            continue

        # Remove the if auto_paginate: block
        if line.strip() == "if auto_paginate:":
            base_indent = len(line) - len(line.lstrip())
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if next_line.strip() == "":
                    i += 1
                    continue
                next_indent = len(next_line) - len(next_line.lstrip())
                if next_indent <= base_indent:
                    break
                i += 1
            continue

        out_lines.append(line)
        i += 1

    with open(filepath, "w") as f:
        f.writelines(out_lines)


if __name__ == "__main__":
    for filename in os.listdir(RESOURCE_DIR):
        if filename.endswith(".py") and filename != "__init__.py":
            process_file(os.path.join(RESOURCE_DIR, filename))
    print("Done")
