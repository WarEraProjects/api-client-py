import os
import re

RESOURCE_DIR = "warera/resources"

def fix_overloads(filepath):
    with open(filepath) as f:
        content = f.read()

    # 1. Replace auto_items: bool = False, with typing.Literal[False] = False, if it's inside an overload returning CursorPage
    # Regex: match `@typing.overload` up to `-> CursorPage`
    # We can do this by splitting the file on `@typing.overload`
    parts = content.split("@typing.overload")
    for i in range(1, len(parts)):
        part = parts[i]
        # find where the overload ends (the next `def ` or `async def ` that does NOT have `@typing.overload` before it? No, just find `...`)
        # Actually, let's just find the first `-> ` and see what it returns
        return_match = re.search(r'->\s+([^:]+):\s*\.\.\.', part)
        if return_match:
            ret_type = return_match.group(1).strip()
            if ret_type.startswith("CursorPage"):
                # It's the False overload
                parts[i] = re.sub(r'auto_items:\s*bool\s*=\s*False,', 'auto_items: typing.Literal[False] = False,', part, count=1)
            elif ret_type.startswith("AsyncIterator"):
                # It's the True overload
                parts[i] = re.sub(r'auto_items:\s*bool\s*=\s*False,', 'auto_items: typing.Literal[True],', part, count=1)
                
    content = "@typing.overload".join(parts)
    
    # 2. Fix the paginate_items missing import issue in `warera/resources/*.py`
    # The script removed `from .._pagination import auto_paginate_pages` but left `paginate_items` references in the `paginate()` method.
    # Oh wait, `paginate` method was removed? No, I only removed `auto_paginate` arg. 
    # But wait! I removed `paginate_items` from `warera/_pagination.py` entirely!
    # Let's remove the `paginate` method from all resource files!
    # A `paginate` method looks like:
    #     async def paginate(self, **kwargs: typing.Any) -> typing.AsyncIterator[...]:
    #         ...
    #         async for item in paginate_items(fetch_fn, **kwargs):
    #             yield item
    # Since `auto_items=True` works on all endpoints now, `paginate` method is redundant and broken. We can just delete it.
    
    # Regex to delete the paginate method:
    content = re.sub(r'[ \t]*async def paginate\(self, \*\*kwargs: typing\.Any\).*?(?:async for item in paginate_items[^\n]*\n\s*yield item\n)', '', content, flags=re.DOTALL)
    
    with open(filepath, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    for filename in os.listdir(RESOURCE_DIR):
        if filename.endswith(".py") and filename != "__init__.py":
            fix_overloads(os.path.join(RESOURCE_DIR, filename))
    print("Done fixing overloads")
