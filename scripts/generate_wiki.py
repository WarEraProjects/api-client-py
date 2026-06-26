import inspect
import os
import re
import shutil
import typing
from typing import Any, get_args, get_origin

from pydantic import BaseModel

import warera

WIKI_DIR = os.path.join(os.path.dirname(__file__), "api-client-py.wiki")
REPO_URL = "https://github.com/WarEra-India/api-client-py.wiki.git"

def get_pydantic_models_from_type(t: Any, seen: set[Any] | None = None) -> set[type[BaseModel]]:
    if seen is None:
        seen = set()
    models: set[type[BaseModel]] = set()
    
    # Handle string forward refs implicitly by just ignoring or trying to resolve if we had a namespace
    if type(t) is typing.ForwardRef:
        return models
        
    origin = get_origin(t)
    args = get_args(t)
    
    if isinstance(t, type) and issubclass(t, BaseModel):
        if t in seen:
            return models
        seen.add(t)
        models.add(t)
        # Recurse into fields
        for _field_name, field_info in t.model_fields.items():
            if field_info.annotation is not None:
                models.update(get_pydantic_models_from_type(field_info.annotation, seen))
    elif origin:
        if isinstance(origin, type) and issubclass(origin, BaseModel) and origin not in seen:
            seen.add(origin)
            models.add(origin)
            for _field_name, field_info in origin.model_fields.items():
                if field_info.annotation is not None:
                    models.update(get_pydantic_models_from_type(field_info.annotation, seen))
        for arg in args:
            models.update(get_pydantic_models_from_type(arg, seen))
    
    return models

def clean_type_str(t: Any) -> str:
    # simplify type hints for display
    s = str(t)
    s = s.replace("typing.", "").replace("warera.resources.", "").replace("warera.models.", "").replace("warera._enums.", "")
    s = re.sub(r"<class '([^']+)'>", r"\1", s)
    s = s.replace(" | None", "").replace("None | ", "")
    s = s.replace("|", "&#124;")
    return s

def format_type_with_link(t: str) -> str:
    def repl(m: re.Match[str]) -> str:
        word = m.group(0)
        if len(word) > 1 and word[0].isupper() and any(c.islower() for c in word[1:]) and word not in ["Any", "None", "Optional"]:
            return f'<a href="#{word.lower()}">{word}</a>'
        return word
    
    formatted = re.sub(r'[a-zA-Z]+', repl, t)
    return f"<code>{formatted}</code>"

def generate_schema_markdown(model: type[BaseModel]) -> str:
    schema = model.model_json_schema()
    lines = []
    lines.append(f"#### `{model.__name__}`")
    if "description" in schema:
        lines.append(schema["description"])
        lines.append("")
    
    lines.append("| Field | Type | Required |")
    lines.append("|---|---|---|")
    
    props = schema.get("properties", {})
    required = schema.get("required", [])
    
    for field_name, field_info in props.items():
        type_str = field_info.get("type", "any")
        
        # Handle $ref
        if "$ref" in field_info:
            type_str = field_info["$ref"].split("/")[-1]
            
        # Handle array items
        if type_str == "array" and "items" in field_info:
            item_type = field_info["items"].get("type", "any")
            if "$ref" in field_info["items"]:
                item_type = field_info["items"]["$ref"].split("/")[-1]
            type_str = f"array[{item_type}]"
            
        # Handle anyOf / allOf
        if "anyOf" in field_info:
            types = []
            for sub in field_info["anyOf"]:
                if "type" in sub:
                    t = sub["type"]
                    if t == "null":
                        continue
                    if t == "array" and "items" in sub:
                        item_type = sub["items"].get("type", "any")
                        if "$ref" in sub["items"]:
                            item_type = sub["items"]["$ref"].split("/")[-1]
                        t = f"array[{item_type}]"
                    types.append(t)
                elif "$ref" in sub:
                    types.append(sub["$ref"].split("/")[-1])
            type_str = " &#124; ".join(types)
            if not type_str:
                type_str = "any"
            
        req_mark = "Required" if field_name in required else "Optional"
        type_str = type_str.replace("|", "&#124;")
        type_formatted = format_type_with_link(type_str)
        
        lines.append(f"| `{field_name}` | {type_formatted} | {req_mark} |")
        
    return "\n".join(lines)


def generate_method_markdown(method_name: str, method: Any, resource_name: str) -> str:
    lines = []
    lines.append(f"## `.{method_name}()`")
    
    doc = inspect.getdoc(method)
    if doc:
        lines.append(doc)
        lines.append("")
        
    sig = inspect.signature(method)
    lines.append("### Signature")
    lines.append("```python")
    lines.append(f"await client.{resource_name}.{method_name}{sig}")
    lines.append("```")
    lines.append("")
    
    if sig.parameters:
        lines.append("### Parameters")
        lines.append("| Name | Type | Default |")
        lines.append("|---|---|---|")
        for name, param in sig.parameters.items():
            if name == "self":
                continue
            ptype = clean_type_str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any"
            pdef = param.default if param.default != inspect.Parameter.empty else "*Required*"
            pdef_str = f"`{pdef}`" if pdef != "*Required*" else pdef
            ptype_formatted = format_type_with_link(ptype)
            lines.append(f"| `{name}` | {ptype_formatted} | {pdef_str} |")
        lines.append("")
        
    try:
        type_hints = typing.get_type_hints(method)
        ret_type = type_hints.get('return', inspect.Signature.empty)
    except Exception:
        ret_type = sig.return_annotation

    if ret_type != inspect.Signature.empty:
        models = get_pydantic_models_from_type(ret_type)
        if models:
            lines.append("### Return Models")
            lines.append("")
            # Sort models by name for consistent output
            for model in sorted(models, key=lambda m: m.__name__):
                lines.append(generate_schema_markdown(model))
                lines.append("")
                
    return "\n".join(lines)


def generate_resource_page(name: str, res: Any) -> str:
    lines = []
    class_name = res.__class__.__name__
    lines.append(f"# {class_name} (`client.{name}`)")
    
    doc = inspect.getdoc(res.__class__)
    if doc:
        lines.append(doc)
        lines.append("")
        
    for method_name in dir(res):
        if method_name.startswith("_"):
            continue
        method = getattr(res, method_name)
        if not callable(method):
            continue
        
        lines.append(generate_method_markdown(method_name, method, name))
        lines.append("---")
        
    return "\n".join(lines)

def run() -> None:
    os.makedirs(WIKI_DIR, exist_ok=True)
    
    client = warera.WareraClient()
    resources = []
    for prop in dir(client):
        if prop.startswith("_") or prop in ["batch", "rate_limit_remaining", "rate_limit_reset", "rate_limit_total"]:
            continue
        
        attr = getattr(client, prop)
        if hasattr(attr, "__module__") and "warera.resources" in attr.__module__:
            resources.append((prop, attr))
            
    # Generate Resource Pages
    sidebar_lines = ["# Warera API Client", ""]
    sidebar_lines.append("## Getting Started")
    sidebar_lines.append("- [Home](Home)")
    sidebar_lines.append("- [Introduction](Introduction)")
    sidebar_lines.append("- [Your First Script](Getting-Started)")
    sidebar_lines.append("")
    sidebar_lines.append("## Guides")
    sidebar_lines.append("- [Advanced Usage](Advanced-Usage)")
    sidebar_lines.append("- [Code Snippets](Code-Snippets)")
    sidebar_lines.append("- [FAQ](FAQ)")
    sidebar_lines.append("")
    sidebar_lines.append("## Reference")
    sidebar_lines.append("- [API Reference](API-Reference)")
    sidebar_lines.append("- [Migration Guide](Migration-Guide)")
    sidebar_lines.append("")
    sidebar_lines.append("## Resources")
    
    api_ref_lines = ["# API Reference", "", "Below is a list of all available resource namespaces on the `WareraClient`:"]
    
    for name, res in sorted(resources, key=lambda x: x[0]):
        page_name = f"Resource-{res.__class__.__name__}"
        file_path = os.path.join(WIKI_DIR, f"{page_name}.md")
        
        print(f"Generating {page_name}.md...")
        md = generate_resource_page(name, res)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md)
            
        sidebar_lines.append(f"- [{name}]({page_name})")
        api_ref_lines.append(f"- [`client.{name}`]({page_name}) - {res.__class__.__name__}")

    print("Generating _Sidebar.md...")
    with open(os.path.join(WIKI_DIR, "_Sidebar.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(sidebar_lines))
        
    print("Generating API-Reference.md...")
    with open(os.path.join(WIKI_DIR, "API-Reference.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(api_ref_lines))

    for doc_name in [
        "Home.md", "Introduction.md", "Getting-Started.md", 
        "Advanced-Usage.md", "Code-Snippets.md", "FAQ.md", 
        "Migration-Guide.md"
    ]:
        main_doc = os.path.join(os.path.dirname(__file__), "..", "wiki", doc_name)
        if os.path.exists(main_doc):
            print(f"Copying {doc_name}...")
            shutil.copy(main_doc, os.path.join(WIKI_DIR, doc_name))

    print("\nGeneration complete!")
    print(f"Check the {WIKI_DIR} directory. You can now cd into it, and manually `git commit` and `git push`.")

if __name__ == "__main__":
    run()
