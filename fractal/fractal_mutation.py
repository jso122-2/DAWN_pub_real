# /fractal/fractal_mutation.py

import math
import hashlib
import random

def evolve_fractal_signature(bloom):
    """
    Generates a Julia fractal seed based on bloom entropy, lineage, and bloom_factor.
    Returns a complex number (c) to seed the fractal shape.
    """

    entropy = bloom.entropy_score
    depth = bloom.lineage_depth
    factor = bloom.bloom_factor

    # Base mutation influenced by entropy (chaos) and bloom_factor (weight)
    real = math.cos(entropy * math.pi) * 0.7885 + (factor - 1.0) * 0.1
    imag = math.sin(depth) * 0.3 + random.uniform(-0.05, 0.05)

    # Optional: hash-based uniqueness from seed_id
    seed_hash = int(hashlib.md5(bloom.seed_id.encode()).hexdigest(), 16)
    offset = ((seed_hash % 1000) / 1000.0 - 0.5) * 0.2

    c = complex(real + offset, imag)
    bloom.fractal_signature = str(c)

    return c
