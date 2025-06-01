# /owl/memory_index.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


MEMORY_NOTE_DIR = "owl/commentary"


def has_logged_note(seed_id):
    """
    Checks if a memory note exists for a given seed.
    """
    if not os.path.exists(MEMORY_NOTE_DIR):
        return False

    for fname in os.listdir(MEMORY_NOTE_DIR):
        if seed_id in fname:
            return True

    return False
