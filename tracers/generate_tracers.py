# /tracers/generate_tracers.py

import os
from datetime import datetime

TRACER_DIR = "tracers"
os.makedirs(TRACER_DIR, exist_ok=True)

tracer_specs = {
    "whale.py": {
        "emoji": "🐋",
        "name": "Whale",
        "role": "Pigment tone stability monitor",
        "watch": ["⨀", "/X-"],
        "message": "[🐋 Whale] Diving into deep tone logs for pigment audit."
    },
    "bee.py": {
        "emoji": "🐝",
        "name": "Bee",
        "role": "Ash nutrient carrier",
        "watch": ["^", "~"],
        "message": "[🐝 Bee] Routing Ash nutrient to schema nodes."
    },
    "owl.py": {
        "emoji": "🦉",
        "name": "Owl",
        "role": "Silent entropy observer",
        "watch": ["⌂", "⧉"],
        "message": "[🦉 Owl] Ghost echo log sweep initiated."
    },
    "beetle.py": {
        "emoji": "🐞",
        "name": "Beetle",
        "role": "Edge glow monitor",
        "watch": ["~", "="],
        "message": "[🐞 Beetle] Scanning soft edge pressure glow."
    },
    "ant.py": {
        "emoji": "🐜",
        "name": "Ant",
        "role": "Rhizome path validator",
        "watch": [">~", "/–\\"],  # ✅ fixed invalid string
        "message": "[🐜 Ant] Validating semantic trails in rhizome."
    },
    "spider.py": {
        "emoji": "🕷",
        "name": "Spider",
        "role": "Bloom reactivator",
        "watch": [":"],
        "message": "[🕷 Spider] Reanimating dormant blooms..."
    }
}

def write_tracer(filename, spec):
    path = os.path.join(TRACER_DIR, filename)
    if os.path.exists(path):
        print(f"[TracerGen] ⏩ Skipping {filename} (already exists)")
        return

    docstring = f'"""\n{spec["emoji"]} {spec["name"]} – {spec["role"]}\nWatches: {", ".join(spec["watch"])}\nGenerated on {datetime.now().isoformat()}\n"""'

    content = f"""# AUTO-GENERATED TRACER

{docstring}

from tracers.base import Tracer

def action():
    print("{spec['message']}")

{spec['name']} = Tracer(
    name="{spec['name']}",
    role="{spec['role']}",
    watch={spec['watch']},
    act=action
)
"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"[TracerGen] ✅ Created {filename}")


if __name__ == "__main__":
    for filename, spec in tracer_specs.items():
        try:
            write_tracer(filename, spec)
        except Exception as e:
            print(f"[TracerGen] ❌ Failed to create {filename}: {e}")
