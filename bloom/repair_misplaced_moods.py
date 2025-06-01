# repair_misplaced_moods.py

import os
import shutil

BASE = "juliet_flowers/"

def repair_flat_mood_folders():
    repaired = 0
    for entry in os.listdir(BASE):
        path = os.path.join(BASE, entry)
        if os.path.isdir(path):
            files = os.listdir(path)
            if any(f.startswith("flower-") for f in files):
                # Likely a misplaced mood folder, wrap it in dummy agent + tick
                new_path = os.path.join(BASE, "unknown-agent", entry, "0")
                os.makedirs(new_path, exist_ok=True)

                for f in files:
                    shutil.move(os.path.join(path, f), os.path.join(new_path, f))

                os.rmdir(path)
                print(f"[REPAIRED] Moved mood folder '{entry}' → unknown-agent/{entry}/0/")
                repaired += 1

    print(f"\n✅ Repair complete. {repaired} misplaced mood folders corrected.")

if __name__ == "__main__":
    repair_flat_mood_folders()
