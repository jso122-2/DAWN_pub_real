import importlib

def reload_module(module_name: str):
    try:
        module = importlib.import_module(module_name)
        importlib.reload(module)
        print(f"🔁 Reloaded {module_name}")
        return module
    except Exception as e:
        print(f"❌ Failed to reload {module_name}: {e}")
        return None 