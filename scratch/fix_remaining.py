import os
import re

RESOURCE_DIR = "warera/resources"

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Fix get_all / helper loops
    content = re.sub(
        r'async for page in await self\.(\w+)\((.*?)auto_paginate=True(.*?)\):\n\s*items\.extend\(page\.items\)',
        r'async for item in self.\1(\2auto_items=True\3):\n            items.append(item)',
        content
    )

    # 2. Fix duplicated `import warnings` in collect_all
    content = re.sub(
        r'import warnings\n\s*warnings\.warn\(\n\s*"`collect_all\(\)` is deprecated\. Use `get_all\(\)` directly\.",\n\s*DeprecationWarning,\n\s*stacklevel=2,\n\s*\)\n\s*import warnings\n\s*warnings\.warn\(\n\s*"`collect_all\(\)` is deprecated\. Use `get_all\(\)` directly\.",\n\s*DeprecationWarning,\n\s*stacklevel=2,\n\s*\)',
        r'import warnings\n\n        warnings.warn(\n            "`collect_all()` is deprecated. Use `get_all()` directly.",\n            DeprecationWarning,\n            stacklevel=2,\n        )',
        content
    )
    
    # 3. Swap the overloads manually
    # Overload 1 ends with -> CursorPage[...]: ...
    # Overload 2 ends with -> AsyncIterator[...]: ...
    # We can match both consecutive overloads using a massive regex.
    # Pattern:
    # (@typing\.overload\n\s*async def \w+\(.*?\)\s*->\s*CursorPage[^:]*:\s*\.\.\.\n+)
    # (@typing\.overload\n\s*async def \w+\(.*?\)\s*->\s*AsyncIterator[^:]*:\s*\.\.\.\n+)
    # Replacement: \2\1
    
    pattern = re.compile(
        r'([ \t]*@typing\.overload\n[ \t]*async def \w+\(.*?\)\s*->\s*CursorPage[^:]*:\s*\.\.\.\n+)'
        r'([ \t]*@typing\.overload\n[ \t]*async def \w+\(.*?\)\s*->\s*AsyncIterator[^:]*:\s*\.\.\.\n+)',
        re.DOTALL
    )
    
    content = pattern.sub(r'\2\1', content)

    with open(filepath, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    for filename in os.listdir(RESOURCE_DIR):
        if filename.endswith(".py") and filename != "__init__.py":
            fix_file(os.path.join(RESOURCE_DIR, filename))
    print("Done running fix script")
