import zipfile
import os
import json
import shutil
import argparse
from datetime import datetime

DAWN_ROOT = os.path.abspath(".")
OWL_LOG = os.path.join(DAWN_ROOT, "owl_logs", "install_commentary.txt")

def log_owl(msg):
    os.makedirs(os.path.dirname(OWL_LOG), exist_ok=True)
    with open(OWL_LOG, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")
    print(f"🦉 {msg}")

def extract_and_install(zip_path, target_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        if "manifest.json" not in zip_ref.namelist():
            raise ValueError("Missing manifest.json in zip package.")

        manifest_data = json.loads(zip_ref.read("manifest.json"))
        module_name = manifest_data.get("module", "unnamed")
        version = manifest_data.get("version", "0.0")
        priority = manifest_data.get("priority", "low")

        install_path = os.path.join(target_dir, module_name)
        if os.path.exists(install_path):
            shutil.rmtree(install_path)
            log_owl(f"Removed old module: {module_name}")

        zip_ref.extractall(target_dir)
        log_owl(f"Installed {module_name} v{version} [{priority}] into {target_dir}")

        return manifest_data

def run_if_flagged(manifest):
    if manifest.get("run_on_install"):
        script = manifest.get("script", "wake_dawn.sh")
        os.system(f"bash {script}")
        log_owl(f"Auto-ran script: {script}")

def main():
    parser = argparse.ArgumentParser(description="DAWN CLI Install Agent")
    parser.add_argument("--zip", help="Path to .zip file to unpack")
    parser.add_argument("--to", default=DAWN_ROOT, help="Target install directory")

    args = parser.parse_args()

    if args.zip:
        manifest = extract_and_install(args.zip, args.to)
        run_if_flagged(manifest)

if __name__ == "__main__":
    main()
