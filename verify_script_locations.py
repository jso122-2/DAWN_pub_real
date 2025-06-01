import os

base_dir = os.getcwd()

# List all .py files explicitly and their current locations
with open('explicit_py_files_locations.txt', 'w') as log:
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                log.write(full_path + '\n')
                print(f"📂 Found explicitly: {full_path}")

print("✅ Explicitly logged Python file locations to explicit_py_files_locations.txt")
