
import os

def ci_test_blooms():
    bloom_path = "juliet_flowers"
    assert os.path.exists(bloom_path), "[CI Test] ❌ Juliet flowers directory missing."
    blooms = [f for f in os.listdir(bloom_path) if os.path.isdir(os.path.join(bloom_path, f))]
    assert blooms, "[CI Test] ❌ No blooms explicitly found."
    print("[CI Test] ✅ Bloom directories explicitly exist.")

def ci_test_fractals():
    fractal_found = False
    for root, dirs, files in os.walk("juliet_flowers"):
        if any(file.endswith('.png') for file in files):
            fractal_found = True
            break
    assert fractal_found, "[CI Test] ❌ No fractals explicitly found."
    print("[CI Test] ✅ Fractal images explicitly exist.")

def ci_test_nutrients():
    nutrient_path = "logs/mycelium_logs"
    assert os.path.exists(nutrient_path), "[CI Test] ❌ Nutrient logs missing explicitly."

    logs_exist = False
    for root, dirs, files in os.walk(nutrient_path):
        if any(file.endswith('.csv') for file in files):
            logs_exist = True
            break

    assert logs_exist, "[CI Test] ❌ No nutrient logs explicitly found."
    print("[CI Test] ✅ Nutrient logs explicitly exist.")


if __name__ == "__main__":
    ci_test_blooms()
    ci_test_fractals()
    ci_test_nutrients()
