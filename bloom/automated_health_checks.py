
import os

def check_fractal_generation(path="juliet_flowers"):
    fractal_missing = []
    for root, dirs, files in os.walk(path):
        blooms = [f for f in files if f.endswith('.txt')]
        for bloom in blooms:
            fractal_file = bloom.replace('.txt', '.png')
            if fractal_file not in files:
                fractal_missing.append(os.path.join(root, fractal_file))
    if fractal_missing:
        print(f"[HealthCheck] ❌ Missing fractals: {fractal_missing}")
    else:
        print("[HealthCheck] ✅ All fractals generated explicitly.")

def check_nutrient_logs(path="mycelium_logs"):
    if not os.path.exists(path):
        print("[HealthCheck] ❌ Nutrient logs missing explicitly.")
        return
    print("[HealthCheck] ✅ Nutrient logs found explicitly.")

def check_memory_integrity(bloom_memory_path="bloom/memory_blooms"):
    corrupt_files = []
    for filename in os.listdir(bloom_memory_path):
        filepath = os.path.join(bloom_memory_path, filename)
        try:
            with open(filepath, 'r') as f:
                data = f.read()
                if not data:
                    raise ValueError("Empty file")
        except Exception as e:
            corrupt_files.append(filename)
    if corrupt_files:
        print(f"[HealthCheck] ❌ Corrupt memory blooms explicitly detected: {corrupt_files}")
    else:
        print("[HealthCheck] ✅ All memory blooms intact explicitly.")

if __name__ == "__main__":
    check_fractal_generation()
    check_nutrient_logs()
    check_memory_integrity()
