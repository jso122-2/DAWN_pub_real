# /scripts/tracer_dashboard.py

from tracers import TRACER_REGISTRY

def print_tracer_dashboard():
    print("=== 🧭 DAWN Tracer Dashboard ===\n")
    if not TRACER_REGISTRY:
        print("⚠️ No tracers registered.")
        return

    for name, tracer in TRACER_REGISTRY.items():
        print(f"[{tracer.name}] ({tracer.role})")
        print(f"  ▶️  Status: {tracer.get_status()}")
        print("")

if __name__ == "__main__":
    print_tracer_dashboard()
