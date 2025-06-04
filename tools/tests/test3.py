with open("codex/sigil_symbols.py", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if "—" in line:
            print(f"Line {i}: contains em dash — {line.strip()}")
