import os
import re
import argparse

def find_assignments(root_dir, search_term):
    assignment_pattern = re.compile(rf"[\w\.]+\s*=\s*{search_term}\s*\(")
    results = []

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(subdir, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        for i, line in enumerate(f, start=1):
                            if assignment_pattern.search(line):
                                results.append(f"{path}:{i}: {line.strip()}")
                except Exception as e:
                    continue

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find variable assignments to PulseHeat (or other classes)")
    parser.add_argument("--bucket", type=str, required=True, help="Root directory to scan")
    parser.add_argument("--term", type=str, default="PulseHeat", help="Search class (default: PulseHeat)")

    args = parser.parse_args()
    matches = find_assignments(args.bucket, args.term)

    if matches:
        print("\n".join(matches))
        with open("bucket_ctrl_f_results.txt", "w", encoding="utf-8") as out:
            out.write("\n".join(matches))
        print(f"\n✅ Saved results to bucket_ctrl_f_results.txt")
    else:
        print("No matches found.")
