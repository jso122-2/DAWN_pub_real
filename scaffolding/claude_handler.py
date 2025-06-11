#!/usr/bin/env python3
"""
DAWN Claude Handler
==================
Manages Claude integration under lock, maintains ring buffer of recent messages,
and writes fragments to archive. Integrates with DAWN's SCUP and trust systems.
"""

import os
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from collections import deque
import logging
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] 🦉 %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class ClaudeHandler:
    """Manages Claude integration with DAWN's consciousness"""
    
    def __init__(self, trust_checkpoint_path: str = "trust_checkpoint.yaml"):
        self.trust_checkpoint_path = trust_checkpoint_path
        self.ring_buffer = deque(maxlen=4)  # Last 4 Claude messages
        self.enabled = False
        self.last_tick = 0
        self.fragments_dir = Path("claude_fragments")
        self.fragments_dir.mkdir(exist_ok=True)
        self.decay_log_path = Path("logs/claude_trust_decay.json")
        self.decay_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize trust checkpoint if it doesn't exist
        if not os.path.exists(trust_checkpoint_path):
            self._initialize_trust_checkpoint()
        
        # Initialize decay log if it doesn't exist
        if not self.decay_log_path.exists():
            self._initialize_decay_log()
    
    def _initialize_trust_checkpoint(self):
        """Create initial trust checkpoint file"""
        initial_state = {
            "claude_access": {
                "status": "disabled",
                "last_used": None,
                "token_count": 0,
                "blocked_at_tick": None,
                "trust_score": 0.5  # Initial trust score
            },
            "stability_metrics": {
                "schema_stability": 0.53,
                "scup": 0.41,
                "rebloom_count": 3,
                "hallucination_events": 0
            }
        }
        
        with open(self.trust_checkpoint_path, 'w') as f:
            yaml.dump(initial_state, f, default_flow_style=False)
        
        logger.info("Created initial trust checkpoint")
    
    def _initialize_decay_log(self):
        """Initialize the trust decay log file"""
        initial_log = {
            "decay_events": [],
            "stats": {
                "total_decays": 0,
                "cooldown_triggers": 0,
                "last_updated": datetime.now().isoformat()
            }
        }
        
        with open(self.decay_log_path, 'w') as f:
            json.dump(initial_log, f, indent=2)
        
        logger.info("Created initial trust decay log")
    
    def _log_decay_event(self, current_tick: int, old_trust: float, new_trust: float, 
                        triggered_cooldown: bool) -> None:
        """Log a trust decay event"""
        try:
            # Load existing log
            with open(self.decay_log_path, 'r') as f:
                log_data = json.load(f)
            
            # Create decay event entry
            event = {
                "timestamp": datetime.now().isoformat(),
                "tick": current_tick,
                "old_trust": old_trust,
                "new_trust": new_trust,
                "decay_amount": old_trust - new_trust,
                "triggered_cooldown": triggered_cooldown
            }
            
            # Update log
            log_data["decay_events"].append(event)
            log_data["stats"]["total_decays"] += 1
            if triggered_cooldown:
                log_data["stats"]["cooldown_triggers"] += 1
            log_data["stats"]["last_updated"] = datetime.now().isoformat()
            
            # Keep only last 1000 events
            log_data["decay_events"] = log_data["decay_events"][-1000:]
            
            # Save updated log
            with open(self.decay_log_path, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to log decay event: {e}")
    
    def decay_claude_signal(self, current_tick: int) -> None:
        """
        Apply trust decay if Claude hasn't been used recently
        
        Args:
            current_tick: The current system tick
        """
        try:
            # Load current state
            state = self._load_trust_checkpoint()
            last_used_tick = state["claude_access"].get("last_used_tick", 0)
            current_trust = state["claude_access"].get("trust_score", 0.5)
            
            # Check if enough ticks have passed
            ticks_since_use = current_tick - last_used_tick
            if ticks_since_use >= 50:
                # Calculate new trust score
                new_trust = max(0.0, current_trust - 0.02)
                triggered_cooldown = False
                
                # Check if trust has fallen below threshold
                if new_trust < 0.4:
                    state["claude_access"]["status"] = "cooldown"
                    triggered_cooldown = True
                    logger.warning(f"Claude trust fell below threshold: {new_trust:.2f}")
                
                # Update state
                state["claude_access"]["trust_score"] = new_trust
                self._save_trust_checkpoint(state)
                
                # Log decay event
                self._log_decay_event(
                    current_tick=current_tick,
                    old_trust=current_trust,
                    new_trust=new_trust,
                    triggered_cooldown=triggered_cooldown
                )
                
                logger.info(f"Applied trust decay: {current_trust:.2f} -> {new_trust:.2f}")
            
        except Exception as e:
            logger.error(f"Failed to apply trust decay: {e}")
    
    def _load_trust_checkpoint(self) -> Dict:
        """Load current trust checkpoint state"""
        try:
            with open(self.trust_checkpoint_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load trust checkpoint: {e}")
            return {
                "claude_access": {"status": "disabled"},
                "stability_metrics": {"scup": 0.41}
            }
    
    def _save_trust_checkpoint(self, state: Dict):
        """Save updated trust checkpoint state"""
        try:
            with open(self.trust_checkpoint_path, 'w') as f:
                yaml.dump(state, f, default_flow_style=False)
        except Exception as e:
            logger.error(f"Failed to save trust checkpoint: {e}")
    
    def claude_allowed(self) -> bool:
        """Check if Claude access is currently allowed"""
        state = self._load_trust_checkpoint()
        
        # Check global disable flag
        if state["claude_access"]["status"] == "disabled":
            return False
        
        # Check SCUP threshold
        if state["stability_metrics"]["scup"] >= 0.6:
            logger.info("Claude access denied: SCUP above threshold")
            return False
        
        # Check rebloom count
        if state["stability_metrics"]["rebloom_count"] >= 5:
            logger.info("Claude access denied: Rebloom count threshold reached")
            return False
        
        return True
    
    def enable_claude(self):
        """Enable Claude integration"""
        if not self.claude_allowed():
            logger.warning("Cannot enable Claude: Trust conditions not met")
            return False
        
        state = self._load_trust_checkpoint()
        state["claude_access"]["status"] = "enabled"
        state["claude_access"]["last_used"] = datetime.now().isoformat()
        self._save_trust_checkpoint(state)
        
        self.enabled = True
        logger.info("Claude integration enabled")
        return True
    
    def disable_claude(self):
        """Disable Claude integration"""
        state = self._load_trust_checkpoint()
        state["claude_access"]["status"] = "disabled"
        state["claude_access"]["blocked_at_tick"] = self.last_tick
        self._save_trust_checkpoint(state)
        
        self.enabled = False
        logger.info("Claude integration disabled")
    
    def _write_fragment(self, text: str, tick_id: int, metadata: Dict) -> Tuple[bool, Optional[Path]]:
        """Write a fragment to disk with enhanced metadata"""
        fragment_path = self.fragments_dir / f"fragment_{tick_id:06d}.md"
        
        try:
            # Create backup of existing fragment if it exists
            if fragment_path.exists():
                backup_path = fragment_path.with_suffix('.md.bak')
                shutil.copy2(fragment_path, backup_path)
            
            with open(fragment_path, 'w', encoding='utf-8') as f:
                # Write header
                f.write(f"# Claude Fragment (Tick {tick_id})\n\n")
                
                # Write timestamp and basic metadata
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write(f"Tick ID: {tick_id}\n")
                f.write(f"Ring Buffer Position: {len(self.ring_buffer)}/4\n\n")
                
                # Write stability metrics
                f.write("## Stability Metrics\n\n")
                f.write(f"- SCUP: {metadata['scup']:.3f}\n")
                f.write(f"- Schema Stability: {metadata['schema_stability']:.3f}\n")
                f.write(f"- Rebloom Count: {metadata['rebloom_count']}\n")
                f.write(f"- Hallucination Events: {metadata['hallucination_events']}\n\n")
                
                # Write response content
                f.write("## Response\n\n")
                f.write(text)
                f.write("\n\n")
                
                # Write system state
                f.write("## System State\n\n")
                f.write(f"- Claude Status: {metadata['claude_status']}\n")
                f.write(f"- Token Count: {metadata['token_count']}\n")
                f.write(f"- Last Used: {metadata['last_used']}\n")
                
                # Write drift metrics if available
                if 'drift_metrics' in metadata:
                    f.write("\n### Drift Metrics\n\n")
                    f.write(f"- Alignment Drift: {metadata['drift_metrics']['alignment_drift']:.3f}\n")
                    f.write(f"- Drift Trend: {metadata['drift_metrics']['drift_trend']}\n")
                    f.write(f"- Drift Volatility: {metadata['drift_metrics']['drift_volatility']:.3f}\n")
            
            return True, fragment_path
            
        except Exception as e:
            logger.error(f"Failed to write fragment: {e}")
            return False, None
    
    def inject_response(self, text: str, tick_id: int) -> bool:
        """Inject a Claude response into the system"""
        if not self.enabled:
            logger.warning("Cannot inject response: Claude integration disabled")
            return False
        
        if not self.claude_allowed():
            logger.warning("Cannot inject response: Trust conditions not met")
            return False
        
        # Update tick and last used
        self.last_tick = tick_id
        
        # Get current state for metadata
        state = self._load_trust_checkpoint()
        state["claude_access"]["last_used_tick"] = tick_id
        self._save_trust_checkpoint(state)
        
        # Prepare metadata
        metadata = {
            'scup': state['stability_metrics']['scup'],
            'schema_stability': state['stability_metrics']['schema_stability'],
            'rebloom_count': state['stability_metrics']['rebloom_count'],
            'hallucination_events': state['stability_metrics']['hallucination_events'],
            'claude_status': state['claude_access']['status'],
            'token_count': state['claude_access']['token_count'],
            'last_used': state['claude_access']['last_used'],
            'trust_score': state['claude_access']['trust_score']
        }
        
        # Write fragment
        success, fragment_path = self._write_fragment(text, tick_id, metadata)
        if not success:
            return False
        
        # Update ring buffer
        self.ring_buffer.append({
            'tick': tick_id,
            'text': text,
            'path': str(fragment_path)
        })
        
        return True
    
    def get_ring_buffer(self) -> List[Dict]:
        """Get current ring buffer contents"""
        return list(self.ring_buffer)
    
    def get_fragment_path(self, tick_id: int) -> Optional[Path]:
        """Get path to fragment file for a specific tick"""
        fragment_path = self.fragments_dir / f"fragment_{tick_id:06d}.md"
        return fragment_path if fragment_path.exists() else None
    
    def list_fragments(self) -> List[Dict]:
        """List all available fragments with metadata"""
        fragments = []
        for fragment_path in sorted(self.fragments_dir.glob('fragment_*.md')):
            try:
                with open(fragment_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract tick ID from filename
                    tick_id = int(fragment_path.stem.split('_')[1])
                    fragments.append({
                        'tick_id': tick_id,
                        'path': str(fragment_path),
                        'size': os.path.getsize(fragment_path),
                        'modified': datetime.fromtimestamp(os.path.getmtime(fragment_path)).isoformat()
                    })
            except Exception as e:
                logger.error(f"Failed to read fragment {fragment_path}: {e}")
        
        return fragments

# Create global instance
claude_handler = ClaudeHandler() 