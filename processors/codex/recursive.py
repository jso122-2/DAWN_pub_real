
def trigger_recursive_synthesis():
    from codex.registry import log_sigil_invocation
    print("[Sigil] 🔄 Invoked: /|-/ (Recursive synthesis)")
    log_sigil_invocation("/|-/")
    # Add recursive synthesis logic here
