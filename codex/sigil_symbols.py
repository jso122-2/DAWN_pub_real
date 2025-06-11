"""
Sigil Symbols
Core sigil definitions and utilities
"""

# Core sigil definitions
CORE_SIGILS = {
    'DAWN': '🌅',
    'PULSE': '💫',
    'BLOOM': '🌸',
    'OWL': '🦉',
    'MOOD': '🎭'
}

# Sigil meanings
SIGIL_MEANINGS = {
    'DAWN': 'New beginnings and awakening',
    'PULSE': 'Rhythm and flow',
    'BLOOM': 'Growth and evolution',
    'OWL': 'Wisdom and insight',
    'MOOD': 'Emotional state'
}

# Sigil priorities
SIGIL_PRIORITIES = {
    'DAWN': 1,
    'PULSE': 2,
    'BLOOM': 3,
    'OWL': 4,
    'MOOD': 5
}

def resolve_layering(sigils):
    """Resolve sigil layering order"""
    return sorted(sigils, key=lambda x: SIGIL_PRIORITIES.get(x, 999)) 