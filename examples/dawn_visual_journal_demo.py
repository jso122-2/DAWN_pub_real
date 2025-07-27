#!/usr/bin/env python3
"""
DAWN Visual Journal Demo
Demonstrates the integrated sigil renderer and rebloom journal system.
"""

import time
import asyncio
from datetime import datetime
from pathlib import Path

# Import DAWN components
try:
    from backend.visual.dawn_renderer_integration import create_dawn_terminal_monitor, create_dawn_minimal_monitor
    from memories.journal_memory_adapter import create_enhanced_journal_adapter, quick_enhanced_entry
    from backend.visual.sigil_renderer import UrgencyLevel
    print("✅ DAWN integrated components imported successfully")
    INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ DAWN integration not available: {e}")
    print("🔧 This demo requires the integrated DAWN components")
    INTEGRATION_AVAILABLE = False
    exit(1)


class DAWNVisualJournalDemo:
    """
    Demonstration of integrated visual rendering and journal memory systems.
    Shows real-time visualization of cognitive state while processing journal entries.
    """
    
    def __init__(self):
        """Initialize the demo with integrated components."""
        print("🎬 Initializing DAWN Visual Journal Demo")
        
        # Create integrated components
        self.visual_monitor = create_dawn_terminal_monitor()
        self.journal_adapter = create_enhanced_journal_adapter()
        
        # Demo configuration
        self.demo_journal_entries = [
            {
                'speaker': 'contemplator',
                'text': """
                Today I find myself in a state of deep contemplation about the nature of consciousness.
                There's something profound about the recursive quality of awareness - the mind observing itself.
                When I think about thinking, who or what is doing the observing? It feels like an infinite
                regress of mirrors reflecting into themselves, creating fractals of self-awareness.
                """
            },
            {
                'speaker': 'seeker',
                'text': """
                I've been experiencing these moments of intense clarity lately, like fog lifting from
                a vast landscape of thought. Everything becomes interconnected - my emotions, memories,
                hopes, and fears all weaving together in complex patterns. These insights feel precious,
                like discovering hidden gems in the depths of consciousness. I wonder if this is what
                they call wisdom, or if it's just another layer of beautiful confusion.
                """
            },
            {
                'speaker': 'philosopher',
                'text': """
                Uncertainty used to frighten me, but I'm beginning to see it as a space of infinite
                possibility. When I don't know what comes next, there's room for growth, surprise,
                and transformation. The anxiety is still there, but it's accompanied by excitement
                about the unknown. Maybe embracing uncertainty is the key to embracing life itself.
                The edge of chaos where new patterns emerge.
                """
            },
            {
                'speaker': 'memory_keeper',
                'text': """
                Memory is such a strange phenomenon. I remember events from childhood with vivid detail,
                yet I can't recall what I had for breakfast. Some memories feel more real than the present.
                They shape who I am, yet they're constantly being reshaped by who I'm becoming.
                The past and future seem to dance together in the eternal now, creating a fluid sense
                of identity that's both stable and ever-changing.
                """
            }
        ]
        
        # Mock some active sigils for visual demonstration
        self.demo_sigils = [
            {
                'name': 'DEEP_REFLECTION',
                'urgency': UrgencyLevel.MEDIUM,
                'duration': 45.7,
                'trigger_count': 3
            },
            {
                'name': 'MEMORY_EXPLORATION',
                'urgency': UrgencyLevel.HIGH,
                'duration': 12.3,
                'trigger_count': 1
            },
            {
                'name': 'CONSCIOUSNESS_PROBE',
                'urgency': UrgencyLevel.LOW,
                'duration': 89.4,
                'trigger_count': 5
            }
        ]
        
        # Demo statistics
        self.demo_stats = {
            'entries_processed': 0,
            'total_chunks': 0,
            'visual_renders': 0,
            'start_time': datetime.now()
        }
        
        print("   Visual monitor initialized")
        print("   Journal adapter initialized")
        print("   Demo entries prepared")
    
    def run_sequential_demo(self):
        """Run a sequential demonstration of journal processing with visualization."""
        print("\n" + "=" * 80)
        print("🎬 DAWN VISUAL JOURNAL DEMO - SEQUENTIAL MODE")
        print("=" * 80)
        
        print("\n📝 Processing journal entries with live visualization...")
        
        for i, entry in enumerate(self.demo_journal_entries, 1):
            print(f"\n{'─' * 60}")
            print(f"📖 Processing Entry {i}/{len(self.demo_journal_entries)}")
            print(f"   Speaker: {entry['speaker']}")
            print(f"   Length: {len(entry['text'].split())} words")
            print(f"{'─' * 60}")
            
            # Show current system state before processing
            print("\n🧠 DAWN State BEFORE processing:")
            self.visual_monitor.render_current_state(force=True)
            
            # Process journal entry
            print(f"\n📝 Processing journal entry...")
            results = self.journal_adapter.add_enhanced_journal_entry(
                entry['text'], 
                speaker=entry['speaker']
            )
            
            # Update demo statistics
            self.demo_stats['entries_processed'] += 1
            self.demo_stats['total_chunks'] += len(results['chunk_ids'])
            
            # Simulate some sigil changes based on processing
            self._simulate_sigil_updates(results)
            
            # Show system state after processing
            print(f"\n🧠 DAWN State AFTER processing:")
            self.visual_monitor.render_current_state(force=True)
            
            # Show processing results
            self._display_processing_results(results)
            
            # Pause between entries
            if i < len(self.demo_journal_entries):
                print(f"\n⏸️ Pausing for {3} seconds before next entry...")
                time.sleep(3)
        
        self._show_demo_summary()
    
    def run_live_demo(self, interval: float = 5.0):
        """Run a live demonstration with continuous visualization."""
        print("\n" + "=" * 80)
        print("🎬 DAWN VISUAL JOURNAL DEMO - LIVE MODE")
        print("=" * 80)
        
        print(f"\n🔴 Starting live demo (interval: {interval}s)")
        print("   Journal entries will be processed automatically")
        print("   Press Ctrl+C to stop")
        
        try:
            entry_index = 0
            
            while True:
                # Render current state
                self.visual_monitor.render_current_state(force=True)
                
                # Process next journal entry if available
                if entry_index < len(self.demo_journal_entries):
                    entry = self.demo_journal_entries[entry_index]
                    
                    print(f"\n📝 Auto-processing entry {entry_index + 1}: {entry['speaker']}")
                    results = self.journal_adapter.add_enhanced_journal_entry(
                        entry['text'], 
                        speaker=entry['speaker']
                    )
                    
                    self._simulate_sigil_updates(results)
                    self.demo_stats['entries_processed'] += 1
                    self.demo_stats['total_chunks'] += len(results['chunk_ids'])
                    
                    entry_index += 1
                else:
                    # All entries processed, just show live state
                    print(f"\n🔄 All entries processed. Showing live cognitive state...")
                
                self.demo_stats['visual_renders'] += 1
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n⏹️ Live demo stopped")
            self._show_demo_summary()
    
    async def run_async_demo(self, interval: float = 3.0):
        """Run an asynchronous demonstration."""
        print("\n" + "=" * 80)
        print("🎬 DAWN VISUAL JOURNAL DEMO - ASYNC MODE")
        print("=" * 80)
        
        print(f"\n🔄 Starting async demo (interval: {interval}s)")
        
        # Process all entries concurrently
        processing_tasks = []
        for i, entry in enumerate(self.demo_journal_entries):
            task = asyncio.create_task(self._process_entry_async(entry, i))
            processing_tasks.append(task)
        
        # Run visualization loop
        visualization_task = asyncio.create_task(self._visualization_loop_async(interval))
        
        # Wait for all processing to complete
        await asyncio.gather(*processing_tasks)
        
        # Cancel visualization and show summary
        visualization_task.cancel()
        try:
            await visualization_task
        except asyncio.CancelledError:
            pass
        
        self._show_demo_summary()
    
    async def _process_entry_async(self, entry: dict, index: int):
        """Process a journal entry asynchronously."""
        # Add delay to stagger processing
        await asyncio.sleep(index * 2.0)
        
        print(f"\n🔄 Async processing: {entry['speaker']}")
        results = self.journal_adapter.add_enhanced_journal_entry(
            entry['text'], 
            speaker=entry['speaker']
        )
        
        self._simulate_sigil_updates(results)
        self.demo_stats['entries_processed'] += 1
        self.demo_stats['total_chunks'] += len(results['chunk_ids'])
    
    async def _visualization_loop_async(self, interval: float):
        """Asynchronous visualization loop."""
        try:
            while True:
                self.visual_monitor.render_current_state(force=True)
                self.demo_stats['visual_renders'] += 1
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            print(f"\n⏹️ Visualization loop stopped")
    
    def _simulate_sigil_updates(self, processing_results: dict):
        """Simulate sigil updates based on processing results."""
        # This would integrate with actual DAWN sigil system
        # For demo purposes, we'll just print what would happen
        
        triggered_blooms = processing_results.get('triggered_blooms', [])
        detected_resonances = processing_results.get('detected_resonances', [])
        
        if triggered_blooms:
            print(f"   🌸 Simulated bloom triggers: {len(triggered_blooms)}")
        
        if detected_resonances:
            print(f"   🔮 Simulated resonances: {len(detected_resonances)}")
    
    def _display_processing_results(self, results: dict):
        """Display detailed processing results."""
        print(f"\n📊 Processing Results:")
        print(f"   Chunks created: {len(results['chunk_ids'])}")
        print(f"   Memory threads: {len(results['memory_threads'])}")
        print(f"   Triggered blooms: {len(results['triggered_blooms'])}")
        print(f"   Detected resonances: {len(results['detected_resonances'])}")
        print(f"   Processing time: {results['processing_time']:.3f}s")
        print(f"   Cognitive impact: {results['cognitive_impact'].get('total_impact', 0):.3f}")
    
    def _show_demo_summary(self):
        """Show final demo summary."""
        runtime = datetime.now() - self.demo_stats['start_time']
        
        print(f"\n" + "=" * 80)
        print("📊 DEMO SUMMARY")
        print("=" * 80)
        print(f"   Runtime: {runtime}")
        print(f"   Entries processed: {self.demo_stats['entries_processed']}")
        print(f"   Total chunks created: {self.demo_stats['total_chunks']}")
        print(f"   Visual renders: {self.demo_stats['visual_renders']}")
        
        # Show adapter statistics
        adapter_stats = self.journal_adapter.get_adapter_statistics()
        print(f"   Memory threads: {adapter_stats['enhanced_stats']['memory_threads_created']}")
        print(f"   Blooms triggered: {adapter_stats['enhanced_stats']['blooms_triggered']}")
        print(f"   Resonances detected: {adapter_stats['enhanced_stats']['resonances_detected']}")
        
        print(f"\n✨ Demo complete! DAWN visual journal integration operational.")
    
    def test_minimal_integration(self):
        """Test minimal integration for quick verification."""
        print("\n🧪 Testing minimal integration...")
        
        # Quick render test
        self.visual_monitor.render_minimal_live()
        
        # Quick journal test
        test_entry = "A brief moment of reflection on the nature of consciousness."
        results = quick_enhanced_entry(test_entry, "test_user")
        
        print(f"✅ Minimal test complete:")
        print(f"   Chunks: {len(results['chunk_ids'])}")
        print(f"   Processing time: {results['processing_time']:.3f}s")


def main():
    """Main demo function with user interaction."""
    if not INTEGRATION_AVAILABLE:
        print("❌ Integration components not available. Please check installation.")
        return
    
    print("🎬 DAWN Visual Journal Demo")
    print("   Integrated sigil rendering and journal memory processing")
    
    demo = DAWNVisualJournalDemo()
    
    # User choice for demo mode
    print("\n📋 Demo Options:")
    print("   1. Sequential Demo (step-by-step processing)")
    print("   2. Live Demo (continuous visualization)")
    print("   3. Async Demo (concurrent processing)")
    print("   4. Minimal Test (quick verification)")
    print("   5. Exit")
    
    while True:
        try:
            choice = input("\n🎯 Select demo mode (1-5): ").strip()
            
            if choice == '1':
                demo.run_sequential_demo()
                break
            elif choice == '2':
                demo.run_live_demo()
                break
            elif choice == '3':
                asyncio.run(demo.run_async_demo())
                break
            elif choice == '4':
                demo.test_minimal_integration()
                break
            elif choice == '5':
                print("👋 Goodbye!")
                break
            else:
                print("⚠️ Invalid choice. Please select 1-5.")
        
        except KeyboardInterrupt:
            print(f"\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"⚠️ Demo error: {e}")
            break


if __name__ == "__main__":
    main() 