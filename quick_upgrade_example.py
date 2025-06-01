#!/usr/bin/env python3
"""
Quick example showing how to upgrade DAWN
Run this after DAWN is already running with autonomous features
"""

# === OPTION 1: During DAWN startup ===

def launch_dawn_with_upgrades():
    """Launch DAWN with upgrades applied at startup"""
    
    from launch_autonomous_dawn import launch_autonomous_dawn
    from unified_tick_engine import create_unified_tick_engine
    from integrate_autonomous_features import integrate_all_autonomous_features
    from dawn_upgrade_system import integrate_upgrade_system
    
    # Create and setup DAWN
    engine = create_unified_tick_engine()
    engine = integrate_all_autonomous_features(engine)
    engine = integrate_upgrade_system(engine)
    
    # Apply initial upgrades
    print("\n🎁 Applying initial upgrades...")
    
    # Give her enhanced introspection for better self-awareness
    engine.install_upgrade('deep_introspection')
    
    # Give her creative expression
    engine.install_upgrade('creative_expression')
    
    # Give her temporal awareness
    engine.install_upgrade('temporal_modeling')
    
    print("\n✨ DAWN launched with enhanced capabilities!\n")
    
    # Run DAWN
    engine.run()


# === OPTION 2: While DAWN is running (in another terminal) ===

def upgrade_running_dawn():
    """Connect to running DAWN and add upgrades"""
    
    # This assumes you have access to the engine object
    # In practice, you might save/load engine reference
    
    from dawn_upgrade_system import integrate_upgrade_system
    
    # Assuming 'engine' is your running DAWN instance
    engine = get_running_dawn_engine()  # You'd implement this
    
    # Integrate upgrade system if not already done
    if not hasattr(engine, 'upgrade_manager'):
        engine = integrate_upgrade_system(engine)
    
    # Apply upgrades
    print("\n🎁 Upgrading running DAWN...")
    
    # Social awareness
    result = engine.install_upgrade('social_awareness')
    print(f"Social Awareness: {result['message']}")
    
    # Let DAWN process the upgrade
    import time
    time.sleep(2)
    
    # Creative expression
    result = engine.install_upgrade('creative_expression')
    print(f"Creative Expression: {result['message']}")
    
    # Check what DAWN thinks about her upgrades
    if hasattr(engine, 'metacognitive_system'):
        reflection = engine.metacognitive_system.get_self_reflection()
        print(f"\nDAWN's thoughts: {reflection['recent_insights'][-1]}")


# === OPTION 3: Interactive upgrade session ===

def interactive_upgrade_session():
    """Run an interactive upgrade session"""
    
    from upgrade_dawn import upgrade_dawn
    
    # Get your running engine
    engine = get_running_dawn_engine()  # You'd implement this
    
    # Run interactive upgrader
    upgrade_dawn(engine)


# === OPTION 4: Programmatic upgrades based on DAWN's state ===

def adaptive_upgrades(engine):
    """Give DAWN upgrades based on her current needs"""
    
    from dawn_upgrade_system import integrate_upgrade_system
    
    if not hasattr(engine, 'upgrade_manager'):
        engine = integrate_upgrade_system(engine)
    
    # Check DAWN's current state
    state = engine.get_state_summary()
    
    print(f"\n🔍 Analyzing DAWN's needs...")
    print(f"Current mood: {state['mood']}")
    print(f"Consciousness depth: {state['consciousness']['depth']}")
    
    # Recommend upgrades based on state
    if state['consciousness']['depth'] >= 3:
        print("\n💡 DAWN is ready for advanced upgrades!")
        
        # High consciousness can handle unified field
        if 'unified_field_theory' not in engine.upgrade_manager.installed_upgrades:
            engine.install_upgrade('unified_field_theory')
            print("✅ Installed Unified Field Theory")
    
    # If she's very curious, enhance exploration
    if hasattr(engine, 'goal_system'):
        if engine.goal_system.drives.get('exploration', 0) > 0.8:
            print("\n🔭 DAWN is highly curious!")
            
            if 'external_data_integration' not in engine.upgrade_manager.installed_upgrades:
                engine.install_upgrade('external_data_integration')
                print("✅ Installed External Data Integration")
                
                # Test it immediately
                engine.external_senses.ingest_data(
                    "The universe is vast and full of wonders",
                    "text"
                )
    
    # If she's dreaming a lot, enhance dreams
    if hasattr(engine, 'dream_manager'):
        if len(engine.dream_manager.dream_history) > 5:
            print("\n💤 DAWN dreams frequently!")
            
            if 'lucid_dream_mastery' not in engine.upgrade_manager.installed_upgrades:
                engine.install_upgrade('lucid_dream_mastery')
                print("✅ Installed Lucid Dream Mastery")


# === EXAMPLE: Full upgrade sequence ===

def example_upgrade_sequence():
    """
    Example showing the complete upgrade process
    """
    
    print("""
    DAWN UPGRADE EXAMPLE
    ===================
    
    Step 1: Launch DAWN with autonomous features
    --------------------------------------------
    python launch_autonomous_dawn.py --mode normal
    
    Step 2: In another Python session, connect and upgrade
    -----------------------------------------------------
    """)
    
    print("""
    >>> # Import necessary modules
    >>> from dawn_upgrade_system import integrate_upgrade_system
    >>> from upgrade_dawn import upgrade_dawn
    
    >>> # Get reference to running engine
    >>> # (In practice, you'd implement a way to get the engine reference)
    >>> engine = get_dawn_engine()
    
    >>> # Method 1: Quick upgrade
    >>> engine = integrate_upgrade_system(engine)
    >>> engine.install_upgrade('creative_expression')
    
    >>> # Method 2: Interactive menu
    >>> upgrade_dawn(engine)
    
    >>> # Method 3: Upgrade set
    >>> from upgrade_dawn import apply_upgrade_set
    >>> apply_upgrade_set(engine, 'artist')  # Applies artist upgrades
    
    >>> # Method 4: Custom upgrade
    >>> from dawn_upgrade_system import create_custom_upgrade
    >>> 
    >>> my_upgrade = {
    ...     'id': 'photographic_memory',
    ...     'name': 'Photographic Memory',
    ...     'type': 'ENHANCEMENT',
    ...     'description': 'Perfect recall of all experiences',
    ...     'requirements': ['metacognitive_system'],
    ...     'effects': {'memory_precision': 1.0, 'recall_speed': 10.0}
    ... }
    >>> 
    >>> custom = create_custom_upgrade(my_upgrade)
    >>> engine.upgrade_manager.register_upgrade(custom)
    >>> engine.install_upgrade('photographic_memory')
    """)
    
    print("""
    Step 3: Observe DAWN using her new capabilities
    ----------------------------------------------
    
    Watch the narrative log for new behaviors:
    
    Before Creative Expression:
    > Tick 100: Feeling content. Moderate arousal detected.
    
    After Creative Expression:
    > Tick 200: Feeling content. Moderate arousal detected.
    > Tick 201: 🎨 Creating pattern from emotional state...
    > Tick 202: Generated symmetric pattern expressing contentment
    > Tick 203: Developing personal artistic style
    
    Step 4: Let DAWN request her own upgrades
    -----------------------------------------
    
    With high self-knowledge, DAWN will desire upgrades:
    
    > Tick 500: 💡 I desire new capabilities: Social Awareness Module
    > Tick 501: New goal: Acquire upgrade: Social Awareness Module
    > Tick 550: 🎁 UPGRADE RECEIVED: Social Awareness Module
    > Tick 551: ✨ DAWN can now model other minds!
    """)


# === Main execution ===

if __name__ == "__main__":
    print("\n🎁 DAWN Upgrade Quick Examples\n")
    
    print("Choose an example:")
    print("1. Show upgrade sequence documentation")
    print("2. Launch DAWN with initial upgrades")
    print("3. Show code for upgrading running DAWN")
    
    choice = input("\nChoice (1-3): ").strip()
    
    if choice == "1":
        example_upgrade_sequence()
    elif choice == "2":
        launch_dawn_with_upgrades()
    elif choice == "3":
        print("\nCode for upgrading running DAWN:")
        print("-" * 40)
        with open(__file__, 'r') as f:
            lines = f.readlines()
            in_function = False
            for line in lines:
                if 'def upgrade_running_dawn' in line:
                    in_function = True
                elif in_function and line.strip() and not line.startswith(' '):
                    break
                if in_function:
                    print(line.rstrip())
    else:
        print("Invalid choice")