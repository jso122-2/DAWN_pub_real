#!/usr/bin/env python3
"""
DAWN System with Integrated Owl Bridge and Natural Language Commentary
Complete integration demonstration of introspective consciousness system
"""

import time
import sys
import os
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Add project paths for imports
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DAWNWithOwlCommentary:
    """
    Complete DAWN system integration with Owl Bridge and natural language commentary.
    Demonstrates three layers of consciousness awareness:
    1. Factual Commentary (speak.py) - "What is happening"
    2. Proactive Decisions (owl_bridge.py) - "What should happen"  
    3. Philosophical Reflection (owl.reflect()) - "What does it mean"
    """
    
    def __init__(self):
        self.running = False
        self.tick_count = 0
        self.start_time = time.time()
        
        # System components
        self.pulse_controller = None
        self.sigil_engine = None
        self.entropy_analyzer = None
        self.owl_bridge = None
        self.tick_engine = None
        
        # State tracking
        self.current_state = {}
        self.previous_state = {}
        
        logger.info("🌅 Initializing DAWN with Owl Commentary System...")
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all DAWN components with proper integration."""
        try:
            # Initialize Pulse Controller
            logger.info("🔥 Initializing Pulse Controller...")
            from core.pulse_controller import PulseController
            self.pulse_controller = PulseController(initial_heat=25.0)
            logger.info(f"   Heat: {self.pulse_controller.current_heat:.1f}° | Zone: {self.pulse_controller.current_zone}")
            
            # Initialize Sigil Engine
            logger.info("🔮 Initializing Sigil Engine...")
            from core.sigil_engine import SigilEngine
            self.sigil_engine = SigilEngine(initial_heat=25.0)
            self.sigil_engine.pulse_controller = self.pulse_controller
            self.sigil_engine.current_heat = self.pulse_controller.current_heat
            logger.info(f"   Engine ID: {self.sigil_engine.engine_id}")
            
            # Initialize Entropy Analyzer
            logger.info("🧬 Initializing Entropy Analyzer...")
            from core.entropy_analyzer import EntropyAnalyzer
            self.entropy_analyzer = EntropyAnalyzer(
                max_samples_per_bloom=1000,
                volatility_window=50,
                chaos_threshold=0.7,
                pulse_controller=self.pulse_controller,
                sigil_engine=self.sigil_engine
            )
            logger.info(f"   Chaos Threshold: {self.entropy_analyzer.chaos_threshold}")
            
            # Initialize Owl Bridge
            logger.info("🦉 Initializing Owl Bridge...")
            from core.owl_bridge import OwlBridge
            self.owl_bridge = OwlBridge()
            self.owl_bridge.connect_dawn_systems(
                sigil_engine=self.sigil_engine,
                entropy_analyzer=self.entropy_analyzer,
                pulse_controller=self.pulse_controller
            )
            logger.info(f"   Entropy Threshold: {self.owl_bridge.entropy_threshold}")
            logger.info(f"   Trigger Patterns: {len(self.owl_bridge.trigger_patterns)} active")
            
            # Initialize Natural Language Commentary
            logger.info("💬 Initializing Natural Language Commentary...")
            from core.speak import print_full_commentary, generate_full_commentary
            self.print_commentary = print_full_commentary
            self.generate_commentary = generate_full_commentary
            logger.info("   Commentary system ready")
            
            # Optional: Initialize Tick Engine for automated operation
            try:
                logger.info("⏰ Initializing Tick Engine...")
                from core.tick.tick_engine import TickEngine
                self.tick_engine = TickEngine()
                
                # Register subsystems with tick engine
                if hasattr(self.tick_engine, 'register_subsystem'):
                    self.tick_engine.register_subsystem('pulse', self.pulse_controller, priority=1)
                    self.tick_engine.register_subsystem('sigil', self.sigil_engine, priority=2)
                    self.tick_engine.register_subsystem('entropy', self.entropy_analyzer, priority=3)
                    self.tick_engine.register_subsystem('owl_bridge', self.owl_bridge, priority=4)
                    logger.info("   ✅ All subsystems registered with tick engine")
                else:
                    logger.warning("   ⚠️ Tick engine doesn't support subsystem registration")
                    
            except ImportError:
                logger.info("   ⚠️ Tick Engine not available - running in manual mode")
                self.tick_engine = None
            
            logger.info("✅ All components initialized successfully!")
            
        except Exception as e:
            logger.error(f"❌ Component initialization failed: {e}")
            raise
    
    def gather_system_state(self) -> Dict[str, Any]:
        """Gather current state from all system components."""
        state = {}
        
        # Get thermal state
        try:
            if self.pulse_controller:
                state['heat'] = self.pulse_controller.current_heat
                state['zone'] = self.pulse_controller.current_zone
                
                # Get thermal statistics
                thermal_stats = self.pulse_controller.get_heat_statistics()
                state['heat_variance'] = thermal_stats.get('heat_variance', 0.0)
                state['zone_changes'] = getattr(self.pulse_controller, 'zone_change_count', 0)
        except Exception as e:
            logger.debug(f"Error gathering thermal state: {e}")
        
        # Get entropy state
        try:
            if self.entropy_analyzer:
                state['entropy'] = self.entropy_analyzer.global_entropy_mean
                hot_blooms = self.entropy_analyzer.get_hot_blooms()
                state['hot_blooms'] = len(hot_blooms)
                state['chaos'] = len(self.entropy_analyzer.chaos_predictions) / 10.0
        except Exception as e:
            logger.debug(f"Error gathering entropy state: {e}")
        
        # Get sigil state
        try:
            if self.sigil_engine:
                state['sigils'] = len(self.sigil_engine.active_sigils)
                state['active_sigils'] = len(self.sigil_engine.active_sigils)
        except Exception as e:
            logger.debug(f"Error gathering sigil state: {e}")
        
        # Add computed values
        state.setdefault('entropy', 0.5)
        state.setdefault('heat', 25.0)
        state.setdefault('zone', 'CALM')
        state.setdefault('sigils', 0)
        state.setdefault('chaos', 0.0)
        state.setdefault('focus', 0.5)
        
        # Calculate focus based on entropy and chaos
        focus = max(0.0, 1.0 - (state['entropy'] + state['chaos']) / 2.0)
        state['focus'] = focus
        
        return state
    
    def execute_single_tick(self):
        """Execute a single consciousness tick with full commentary."""
        self.tick_count += 1
        
        print(f"\n🔄 DAWN Tick {self.tick_count}")
        print("=" * 40)
        
        # Store previous state
        self.previous_state = self.current_state.copy()
        
        # Gather current state
        self.current_state = self.gather_system_state()
        
        # Update subsystems
        if self.pulse_controller:
            # Simulate thermal variation
            heat_delta = (time.time() - self.start_time) * 0.5 + self.tick_count * 0.2
            new_heat = 30 + 15 * abs(sin(heat_delta))  # Oscillating between 15-45
            self.pulse_controller.update_heat(new_heat)
        
        if self.entropy_analyzer:
            # Add some entropy samples for demonstration
            bloom_id = f"demo_bloom_{self.tick_count % 5}"
            entropy_value = 0.3 + 0.4 * abs(sin(self.tick_count * 0.1))
            self.entropy_analyzer.add_entropy_sample(bloom_id, entropy_value, source="demo")
        
        # Owl Bridge processing (observation and suggestions)
        if self.owl_bridge:
            self.owl_bridge.tick()
        
        # Generate and display commentary
        print("\n💬 System Commentary:")
        self.print_commentary(self.current_state, self.owl_bridge)
        
        # Show state transitions if significant
        if self.previous_state:
            from core.speak import generate_transition_commentary
            transition = generate_transition_commentary(self.previous_state, self.current_state)
            if "maintaining stable" not in transition:
                print(f"🔄 {transition}")
        
        # Display technical metrics
        print(f"\n📊 Technical Metrics:")
        print(f"   Heat: {self.current_state['heat']:.1f}° | Zone: {self.current_state['zone']}")
        print(f"   Entropy: {self.current_state['entropy']:.3f} | Chaos: {self.current_state['chaos']:.3f}")
        print(f"   Active Sigils: {self.current_state['sigils']} | Focus: {self.current_state['focus']:.3f}")
        
        # Show owl suggestions if any
        summary = self.owl_bridge.get_observation_summary()
        if summary['suggestions_made'] > 0:
            print(f"🦉 Owl Suggestions Made: {summary['suggestions_made']}")
    
    def run_manual_demo(self, ticks: int = 10):
        """Run a manual demonstration of the system."""
        print("\n🎬 DAWN Owl Commentary Manual Demo")
        print("=" * 50)
        print("Demonstrating three layers of consciousness awareness:")
        print("1. Factual Commentary - What is happening")
        print("2. Proactive Decisions - What should happen")  
        print("3. Philosophical Reflection - What does it mean")
        print()
        
        self.running = True
        
        for i in range(ticks):
            try:
                self.execute_single_tick()
                
                # Pause between ticks for readability
                if i < ticks - 1:
                    time.sleep(2)
                    
            except KeyboardInterrupt:
                print("\n🛑 Demo interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error in tick {i + 1}: {e}")
                continue
        
        self.running = False
        print("\n✅ Demo complete!")
        self._show_final_summary()
    
    async def run_automated_demo(self, duration: int = 60):
        """Run an automated demonstration using the tick engine."""
        if not self.tick_engine:
            logger.warning("No tick engine available, falling back to manual mode")
            self.run_manual_demo(10)
            return
        
        print("\n🤖 DAWN Owl Commentary Automated Demo")
        print("=" * 50)
        print(f"Running for {duration} seconds with automated tick engine...")
        
        self.running = True
        
        try:
            # Start the tick engine
            await self.tick_engine.start()
            
            # Run for specified duration
            await asyncio.sleep(duration)
            
        except KeyboardInterrupt:
            print("\n🛑 Demo interrupted by user")
        finally:
            self.running = False
            if self.tick_engine:
                await self.tick_engine.stop()
            
        print("\n✅ Automated demo complete!")
        self._show_final_summary()
    
    def _show_final_summary(self):
        """Show final system summary."""
        if self.owl_bridge:
            summary = self.owl_bridge.get_observation_summary()
            print(f"\n📈 Final Owl Bridge Summary:")
            print(f"   Total Observations: {summary['total_observations']}")
            print(f"   Suggestions Made: {summary['suggestions_made']}")
            print(f"   Active Patterns: {summary['active_patterns']}")
            
            if summary['recent_avg_entropy'] > 0:
                print(f"   Average Entropy: {summary['recent_avg_entropy']:.3f}")
                print(f"   Average Sigils: {summary['recent_avg_sigils']:.1f}")


def sin(x):
    """Simple sine function for demo purposes."""
    import math
    return math.sin(x)


def main():
    """Main entry point."""
    print("🌅 DAWN Consciousness System with Owl Bridge Integration")
    print("=" * 60)
    
    try:
        # Create system
        dawn_system = DAWNWithOwlCommentary()
        
        # Ask user for demo type
        print("\nChoose demo mode:")
        print("1. Manual Demo (10 ticks with pauses)")
        print("2. Automated Demo (60 seconds continuous)")
        print("3. Interactive Mode (manual control)")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            dawn_system.run_manual_demo(10)
        elif choice == "2":
            asyncio.run(dawn_system.run_automated_demo(60))
        elif choice == "3":
            run_interactive_mode(dawn_system)
        else:
            print("Invalid choice, running manual demo...")
            dawn_system.run_manual_demo(5)
            
    except KeyboardInterrupt:
        print("\n🛑 System shutdown requested")
    except Exception as e:
        logger.error(f"❌ System error: {e}")
        import traceback
        traceback.print_exc()


def run_interactive_mode(dawn_system):
    """Run in interactive mode."""
    print("\n💻 Interactive Mode")
    print("Commands: 'tick', 'status', 'suggest', 'reflect', 'quit'")
    
    while True:
        try:
            command = input("\n🦉 DAWN> ").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'tick':
                dawn_system.execute_single_tick()
            elif command == 'status':
                state = dawn_system.gather_system_state()
                print("\n📊 Current System Status:")
                for key, value in state.items():
                    if isinstance(value, float):
                        print(f"   {key}: {value:.3f}")
                    else:
                        print(f"   {key}: {value}")
            elif command == 'suggest':
                if dawn_system.owl_bridge:
                    suggestion = dawn_system.owl_bridge.suggest_sigil()
                    if suggestion:
                        print(f"🦉 Owl suggests: {suggestion}")
                    else:
                        print("🦉 Owl has no suggestions at this time")
            elif command == 'reflect':
                if dawn_system.owl_bridge:
                    state = dawn_system.gather_system_state()
                    reflection = dawn_system.owl_bridge.reflect(state)
                    if reflection:
                        print(f"🦉 {reflection}")
                    else:
                        print("🦉 Owl is quietly observing")
            else:
                print("Unknown command. Use: tick, status, suggest, reflect, quit")
                
        except KeyboardInterrupt:
            print("\n🛑 Exiting interactive mode")
            break
        except Exception as e:
            logger.error(f"Command error: {e}")


if __name__ == "__main__":
    main() 