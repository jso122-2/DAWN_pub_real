# fractal_key_generator.py
# Generates a complex seed value from words and depths for Julia fractals.

import hashlib
from typing import List

def generate_complex_seed(words: List[str], depths: List[int]) -> complex:
    """
    Combines words and depths into a hash to derive a complex constant c.
    """
    combined = ''.join(words) + ''.join(map(str, depths))
    h = hashlib.sha256(combined.encode()).hexdigest()
    # Map portions of hash to real and imaginary parts in [-1.75, 1.75]
    real = (int(h[:16], 16) / 2**64) * 3.5 - 1.75
    imag = (int(h[16:32], 16) / 2**64) * 3.5 - 1.75
    return complex(real, imag)
