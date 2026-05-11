from tools_impl import save_note, list_notes

TOOL_REGISTRY = {
    "save_note": save_note,
    "list_notes": list_notes,
}

def run_tool(name: str, args: dict) -> dict:
    fn = TOOL_REGISTRY.get(name)
    if fn is None:
        return {"ok": False, "error": f"Unknown tool: {name}"}
    try:
        return fn(**args)
    except TypeError as e:
        return {"ok": False, "error": f"Bad args for {name}: {e}"}
    except Exception as e:
        return {"ok": False, "error": f"{name} failed: {e}"}