"""
ReflexExecutor - Executes schema reflexes for DAWN system coordination
Integrates with pulse control, sigil memory management, and bloom suppression
"""

import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class ReflexExecutor:
    """
    Executes schema reflexes like slow tick, suppress bloom, or prune sigils.
    Coordinates with system components for stability and performance control.
    """
    
    def __init__(self, pulse_controller, sigil_memory_ring, tick_loop):
        """Accepts system components for coordination."""
        self.pulse = pulse_controller
        self.sigil_ring = sigil_memory_ring
        self.tick_loop = tick_loop
        self._suppression_active = False
        self._original_tick_rate = None
        
        logger.info("ReflexExecutor initialized with system components")

    def execute(self, commands: List[str]) -> Dict[str, Any]:
        """
        Execute schema reflexes like slow tick, suppress bloom, or prune sigils.
        
        Args:
            commands: List of reflex commands to execute
            
        Returns:
            Dictionary with execution results for each command
        """
        results = {}
        
        for cmd in commands:
            try:
                if cmd == "slow_tick":
                    results[cmd] = self.slow_tick()
                elif cmd == "suppress_rebloom":
                    results[cmd] = self.block_rebloom()
                elif cmd == "prune_sigils":
                    results[cmd] = self.clear_sigil_ring()
                else:
                    results[cmd] = {"status": "unknown_command", "error": f"Unknown command: {cmd}"}
                    logger.warning(f"Unknown reflex command: {cmd}")
                    
            except Exception as e:
                results[cmd] = {"status": "error", "error": str(e)}
                logger.error(f"Error executing reflex command {cmd}: {e}")
                
        return results

    def slow_tick(self) -> Dict[str, Any]:
        """
        Adjust tick controller to slow down processing speed.
        Reduces system heat and provides stability during high entropy periods.
        """
        try:
            # Store original tick rate if not already stored
            if self._original_tick_rate is None and hasattr(self.tick_loop, 'tick_rate'):
                self._original_tick_rate = self.tick_loop.tick_rate
            elif self._original_tick_rate is None and hasattr(self.tick_loop, 'minimum_bloom_interval'):
                self._original_tick_rate = self.tick_loop.minimum_bloom_interval
                
            # Apply tick slowdown based on system design
            if hasattr(self.tick_loop, 'tick_rate'):
                # Reduce tick rate by 50% for stability
                self.tick_loop.tick_rate = self.tick_loop.tick_rate * 0.5
                logger.info(f"Tick rate slowed to {self.tick_loop.tick_rate}")
                
            elif hasattr(self.tick_loop, 'minimum_bloom_interval'):
                # Increase bloom interval for spacing
                self.tick_loop.minimum_bloom_interval = self.tick_loop.minimum_bloom_interval * 2.0
                logger.info(f"Bloom interval extended to {self.tick_loop.minimum_bloom_interval}")
                
            # Adjust pulse thermal properties if available
            if hasattr(self.pulse, 'system_temperature'):
                # Cool down system temperature
                self.pulse.system_temperature = max(0.1, self.pulse.system_temperature * 0.8)
                logger.info(f"System temperature cooled to {self.pulse.system_temperature}")
                
            # Update pulse heat if available
            if hasattr(self.pulse, 'heat') and hasattr(self.pulse, 'modulate_heat'):
                self.pulse.modulate_heat(0.7)  # Reduce heat by 30%
                logger.info("Pulse heat modulated for stability")
                
            return {
                "status": "success",
                "action": "tick_slowed",
                "message": "Tick processing rate reduced for system stability"
            }
            
        except Exception as e:
            logger.error(f"Failed to slow tick: {e}")
            return {
                "status": "error", 
                "action": "tick_slow_failed",
                "error": str(e)
            }

    def block_rebloom(self) -> Dict[str, Any]:
        """
        Prevent bloom_manager from reblooming.
        Activates bloom suppression to maintain system stability.
        """
        try:
            suppressed_count = 0
            
            # Method 1: Direct bloom suppression via bloom_suppression flag
            if hasattr(self.pulse, 'bloom_suppression'):
                self.pulse.bloom_suppression = True
                logger.info("Bloom suppression activated via pulse controller")
                suppressed_count += 1
                
            # Method 2: Suppress via bloom engine if available
            if hasattr(self.pulse, 'suppress_all_blooms'):
                self.pulse.suppress_all_blooms()
                logger.info("All blooms suppressed via bloom engine")
                suppressed_count += 1
                
            # Method 3: Set activation state to suppressed
            if hasattr(self.pulse, 'activation_state'):
                # Assuming BloomActivationState.SUPPRESSED exists
                self.pulse.activation_state = "SUPPRESSED"
                logger.info("Bloom activation state set to suppressed")
                suppressed_count += 1
                
            # Method 4: Block via bloom manager if accessible
            if hasattr(self.pulse, 'bloom_manager') and hasattr(self.pulse.bloom_manager, 'suppress_all_blooms'):
                self.pulse.bloom_manager.suppress_all_blooms()
                suppressed_count += 1
                
            # Set internal suppression flag
            self._suppression_active = True
            
            if suppressed_count > 0:
                return {
                    "status": "success",
                    "action": "rebloom_blocked",
                    "suppressed_systems": suppressed_count,
                    "message": "Bloom/rebloom functionality suppressed for system protection"
                }
            else:
                return {
                    "status": "partial",
                    "action": "rebloom_block_attempted",
                    "message": "Bloom suppression attempted but no compatible interfaces found"
                }
                
        except Exception as e:
            logger.error(f"Failed to block rebloom: {e}")
            return {
                "status": "error",
                "action": "rebloom_block_failed", 
                "error": str(e)
            }

    def clear_sigil_ring(self) -> Dict[str, Any]:
        """
        Empty the sigil memory ring completely.
        Clears all sigil memory to reduce system entropy and reset state.
        """
        try:
            cleared_count = 0
            original_count = 0
            
            # Method 1: Clear ring-based sigil memory (priority rings)
            if hasattr(self.sigil_ring, 'rings'):
                for ring_level in self.sigil_ring.rings:
                    original_count += len(self.sigil_ring.rings[ring_level])
                    self.sigil_ring.rings[ring_level].clear()
                    
                cleared_count = original_count
                logger.info(f"Cleared {cleared_count} sigils from priority rings")
                
            # Method 2: Clear deque-based sigil memory
            elif hasattr(self.sigil_ring, 'ring') and hasattr(self.sigil_ring.ring, 'clear'):
                original_count = len(self.sigil_ring.ring)
                self.sigil_ring.ring.clear()
                cleared_count = original_count
                logger.info(f"Cleared {cleared_count} sigils from memory ring")
                
            # Method 3: Clear dictionary-based sigil memory
            elif hasattr(self.sigil_ring, 'sigil_memory_ring'):
                if isinstance(self.sigil_ring.sigil_memory_ring, dict):
                    original_count = len(self.sigil_ring.sigil_memory_ring)
                    self.sigil_ring.sigil_memory_ring.clear()
                    cleared_count = original_count
                    logger.info(f"Cleared {cleared_count} sigils from global memory ring")
                    
            # Method 4: Clear active sigils if available
            if hasattr(self.sigil_ring, 'active_sigils'):
                if isinstance(self.sigil_ring.active_sigils, list):
                    original_count += len(self.sigil_ring.active_sigils)
                    self.sigil_ring.active_sigils.clear()
                    cleared_count += len(self.sigil_ring.active_sigils)
                    
            # Method 5: Use purge methods if available
            if hasattr(self.sigil_ring, 'purge_expired_sigils'):
                self.sigil_ring.purge_expired_sigils()
                logger.info("Purged expired sigils")
                
            if hasattr(self.sigil_ring, 'purge_dead_sigils'):
                self.sigil_ring.purge_dead_sigils(threshold=0.0)  # Purge all
                logger.info("Purged all dead sigils")
                
            # Reset system temperature if sigil ring controls it
            if hasattr(self.sigil_ring, 'system_temperature'):
                self.sigil_ring.system_temperature = 0.3  # Reset to baseline
                
            # Reset entropy if controlled by sigil ring
            if hasattr(self.sigil_ring, 'current_tick'):
                self.sigil_ring.current_tick = 0
                
            return {
                "status": "success",
                "action": "sigils_cleared",
                "original_count": original_count,
                "cleared_count": cleared_count,
                "message": f"Sigil memory ring cleared - removed {cleared_count} sigils"
            }
            
        except Exception as e:
            logger.error(f"Failed to clear sigil ring: {e}")
            return {
                "status": "error",
                "action": "sigil_clear_failed",
                "error": str(e)
            }
            
    def restore_normal_operation(self) -> Dict[str, Any]:
        """
        Restore normal system operation after reflex interventions.
        """
        try:
            restored_systems = []
            
            # Restore original tick rate
            if self._original_tick_rate is not None:
                if hasattr(self.tick_loop, 'tick_rate'):
                    self.tick_loop.tick_rate = self._original_tick_rate
                    restored_systems.append("tick_rate")
                elif hasattr(self.tick_loop, 'minimum_bloom_interval'):
                    self.tick_loop.minimum_bloom_interval = self._original_tick_rate
                    restored_systems.append("bloom_interval")
                    
            # Restore bloom functionality
            if self._suppression_active:
                if hasattr(self.pulse, 'bloom_suppression'):
                    self.pulse.bloom_suppression = False
                    restored_systems.append("bloom_suppression")
                    
                if hasattr(self.pulse, 'activation_state'):
                    self.pulse.activation_state = "ACTIVE"
                    restored_systems.append("activation_state")
                    
                self._suppression_active = False
                
            return {
                "status": "success",
                "action": "normal_operation_restored",
                "restored_systems": restored_systems,
                "message": "System restored to normal operation"
            }
            
        except Exception as e:
            logger.error(f"Failed to restore normal operation: {e}")
            return {
                "status": "error",
                "action": "restore_failed",
                "error": str(e)
            }
            
    def get_status(self) -> Dict[str, Any]:
        """Get current reflex executor status"""
        return {
            "suppression_active": self._suppression_active,
            "original_tick_rate": self._original_tick_rate,
            "pulse_available": self.pulse is not None,
            "sigil_ring_available": self.sigil_ring is not None,
            "tick_loop_available": self.tick_loop is not None
        } 