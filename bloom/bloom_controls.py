# File Path: /src/bloom/bloom_controls.py

from bloom.juliet_flower import JulietFlower  # Example import, adjust based on your actual project structure

def suppress_all_blooms():
    """
    Function to suppress all blooms.
    This function can be used to suppress all blooms by, for example, marking them inactive,
    reducing their rate to zero, or any other logic that "suppresses" the bloom.
    """
    # Example logic: loop through all blooms and set their rate to zero or disable them
    # Assuming you have a global list or registry of blooms to iterate through
    all_blooms = JulietFlower.get_all_blooms()  # Assuming you have a method to get all blooms
    
    for bloom in all_blooms:
        bloom.rate = 0  # Suppress the bloom by setting rate to zero
        bloom.status = "suppressed"  # Set a status or flag to show it's suppressed
        print(f"[BloomControls] Suppressed bloom {bloom.seed_id}.")

def modulate_bloom_rate(bloom, rate_modifier):
    """
    Modulate the bloom's rate based on the given modifier.
    This can adjust the bloom's properties (like growth rate, color, or any other behavior).
    """
    # Example: Adjust bloom rate based on the modifier (increasing/decreasing its rate)
    if isinstance(bloom, JulietFlower):  # Ensure the object is an instance of JulietFlower
        original_rate = bloom.rate
        bloom.rate *= rate_modifier  # Apply the rate modifier (e.g., 1.2 for 20% increase)
        print(f"[BloomControls] Bloom {bloom.seed_id} rate modulated from {original_rate} to {bloom.rate}.")
    else:
        print("[BloomControls] Invalid bloom object. Could not modulate rate.")

