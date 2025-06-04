
# Core process definitions and input triggers mapped to sigil logic

SIGIL_PROCESSES = {
    "juliet_bloom": {
        "triggers": ["mood", "entropy_score", "bloom_factor"],
        "outputs": ["json", "png", "seed", "mood"],
        "linked_sigils": [":", "◇"]
    },
    "ash_yield": {
        "triggers": ["SCUP >= 0.9", "stabilized bloom"],
        "outputs": ["Ash packet", "nutrient_signal"],
        "linked_sigils": ["^", "A"]
    },
    "soot_detection": {
        "triggers": ["coherence drop", "conflict"],
        "outputs": ["Soot residue", "pressure shift"],
        "linked_sigils": ["⟁", "~"]
    },
    "sigil_overflow": {
        "triggers": ["temp > 50", "sigil_queue > capacity"],
        "outputs": ["Overflow queue", "sigil decay"],
        "linked_sigils": ["~", "θ"]
    },
    "pressure_reflex": {
        "triggers": ["TP-RAR spike", "climate shift"],
        "outputs": ["pulse_rate", "tick interval shift"],
        "linked_sigils": [">~", "="]
    },
    "recursive_synthesis": {
        "triggers": ["synthesis file", "calm zone"],
        "outputs": ["synthesis_summary", "reflected_moods"],
        "linked_sigils": ["/|-/", ":"]
    },
    "schema_pivot": {
        "triggers": ["SCUP < 0.3", "soft edge failure"],
        "outputs": ["transition_state", "schema_lock"],
        "linked_sigils": ["⨀", "/X-"]
    }
}

def describe_process(name):
    p = SIGIL_PROCESSES.get(name)
    if not p:
        return f"[SigilProcess] ❌ Unknown process: {name}"
    lines = [f"[SigilProcess] {name}"]
    lines.append(f"↪ Triggers: {', '.join(p['triggers'])}")
    lines.append(f"→ Outputs: {', '.join(p['outputs'])}")
    lines.append(f"🔣 Linked Sigils: {', '.join(p['linked_sigils'])}")
    return "\n".join(lines)
