import os
import re

RESOURCE_DIR = "warera/resources"

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # The paginate method might be split over lines
    # It starts with `    async def paginate(` and ends with `yield item\n`
    content = re.sub(
        r'[ \t]*async def paginate\([\s\S]*?yield item\n',
        '',
        content
    )

    with open(filepath, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    for filename in os.listdir(RESOURCE_DIR):
        if filename.endswith(".py") and filename != "__init__.py":
            fix_file(os.path.join(RESOURCE_DIR, filename))
    print("Done")
