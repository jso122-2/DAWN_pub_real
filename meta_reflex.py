"""
MetaReflex module for DAWN consciousness system.
Evaluates system state and outputs schema-wide reflex actions.
"""

from datetime import datetime
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class MetaReflex:
    """Meta-reflexive system for monitoring and responding to DAWN system pressures."""
    
    def __init__(self):
        """Initialize MetaReflex with empty log."""
        self.log = []
        self.tick_count = 0
        logger.info("MetaReflex initialized")

    def evaluate_system_state(self, scup: float, entropy: float, zone: str) -> List[str]:
        """
        Evaluate system state and determine what reflexive triggers are needed.
        
        Args:
            scup: Semantic Coherence Under Pressure (float 0-1)
            entropy: Bloom volatility (float)
            zone: Current pulse state string ("CALM", "ACTIVE", "SURGE")
            
        Returns:
            List of trigger strings
        """
        triggers = []

        # Check SCUP threshold
        if scup < 0.5:
            triggers.append("LOW_SCUP")
            
        # Check entropy threshold
        if entropy > 0.75:
            triggers.append("HIGH_ENTROPY")
            
        # Check pulse zone
        if zone.upper() == "SURGE":
            triggers.append("ZONE_SURGE")

        logger.debug(f"Evaluated state: SCUP={scup:.3f}, Entropy={entropy:.3f}, Zone={zone} -> Triggers: {triggers}")
        return triggers

    def generate_reflex_commands(self, triggers: List[str]) -> List[str]:
        """
        Generate reflex commands based on triggers.
        
        Args:
            triggers: List of trigger strings from evaluate_system_state
            
        Returns:
            List of command strings to execute
        """
        reflex_map = {
            "LOW_SCUP": "slow_tick",
            "HIGH_ENTROPY": "suppress_rebloom", 
            "ZONE_SURGE": "prune_sigils"
        }

        commands = [reflex_map[t] for t in triggers if t in reflex_map]
        
        if commands:
            logger.info(f"Generated reflex commands: {commands}")
            
        return commands

    def log_intervention(self, reason: str) -> None:
        """
        Log a reflex intervention with timestamp.
        
        Args:
            reason: String describing why the intervention was triggered
        """
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] Reflex activated due to: {reason}"
        self.log.append(log_entry)
        logger.warning(f"MetaReflex intervention: {reason}")

    def get_log(self) -> List[str]:
        """
        Get the full intervention log.
        
        Returns:
            List of log entries
        """
        return self.log.copy()

    def execute_reflex_commands(self, commands: List[str], system_context: Dict[str, Any] = None) -> None:
        """
        Execute reflex commands with optional system context.
        
        Args:
            commands: List of commands to execute
            system_context: Optional context dictionary for command execution
        """
        for command in commands:
            try:
                if command == "slow_tick":
                    self._slow_tick_rate(system_context)
                elif command == "suppress_rebloom":
                    self._suppress_rebloom(system_context)
                elif command == "prune_sigils":
                    self._prune_sigils(system_context)
                else:
                    logger.warning(f"Unknown reflex command: {command}")
                    
                print(f"🔧 MetaReflex executed: {command}")
                    
            except Exception as e:
                logger.error(f"Error executing reflex command '{command}': {e}")

    def _slow_tick_rate(self, context: Dict[str, Any] = None) -> None:
        """Slow down the tick rate to reduce system pressure."""
        logger.info("Executing slow_tick reflex - reducing system tick rate")
        # Implementation would modify tick rate in the context
        
    def _suppress_rebloom(self, context: Dict[str, Any] = None) -> None:
        """Suppress rebloom operations to reduce entropy."""
        logger.info("Executing suppress_rebloom reflex - temporarily halting bloom operations")
        # Implementation would set rebloom suppression flag
        
    def _prune_sigils(self, context: Dict[str, Any] = None) -> None:
        """Prune sigil memory ring to clear surge conditions."""
        logger.info("Executing prune_sigils reflex - clearing low-priority sigils")
        # Implementation would interface with sigil memory ring
        
    def tick_update(self) -> None:
        """Update tick counter for periodic log dumping."""
        self.tick_count += 1
        
        # Dump recent log entries every 50 ticks
        if self.tick_count % 50 == 0 and self.log:
            recent_logs = self.log[-5:] if len(self.log) >= 5 else self.log
            print(f"\n📊 MetaReflex Log (Last {len(recent_logs)} entries, Tick {self.tick_count}):")
            for entry in recent_logs:
                print(f"  {entry}")
            print()

    def get_system_health_metrics(self) -> Dict[str, Any]:
        """
        Get system health metrics for monitoring.
        
        Returns:
            Dictionary of health metrics
        """
        return {
            "total_interventions": len(self.log),
            "tick_count": self.tick_count,
            "recent_interventions": len([log for log in self.log if "recent" in log]) if self.log else 0,
            "last_intervention": self.log[-1] if self.log else None
        } 