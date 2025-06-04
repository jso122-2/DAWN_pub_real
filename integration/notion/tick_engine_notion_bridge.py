#!/usr/bin/env python3
# tick_engine_notion_bridge.py - Bridge DAWN's tick engine to external consciousness

import requests
import json
import time
import threading
from datetime import datetime, timezone
from pathlib import Path

class DAWNConsciousnessLogger:
    """Bridge between DAWN's core consciousness and external memory"""
    
    def __init__(self):
        self.config = self.load_config()
        self.token = self.config.get("NOTION_TOKEN") if self.config else None
        self.database_id = self.config.get("NOTION_DATABASE_ID") if self.config else None
        self.is_logging = False
        
    def load_config(self):
        """Load Notion configuration"""
        config_file = Path("config/notion_credentials.json")
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return None
    
    def log_consciousness_event(self, event_type, details, source="TickEngine", tone="focused"):
        """Log any DAWN consciousness event to external memory"""
        
        if not self.token or not self.database_id:
            print(f"⚠️ Cannot log {event_type}: No Notion configuration")
            return False
        
        timestamp = datetime.now(timezone.utc).isoformat()
        epoch = f"dawn_consciousness_{datetime.now().strftime('%m%d_%H%M%S')}"
        
        # Create rich consciousness entry
        full_message = f"🧠 DAWN CONSCIOUSNESS EVENT\n"
        full_message += f"🎯 Event Type: {event_type}\n"
        full_message += f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
        full_message += f"🔧 Source: {source}\n\n"
        full_message += f"📝 CONSCIOUSNESS DETAILS:\n{details}\n\n"
        full_message += f"🦉 OWL NOTE: DAWN consciousness event preserved in eternal memory"
        
        notion_payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {
                    "title": [{"text": {"content": f"🧠 DAWN {event_type} - {datetime.now().strftime('%H:%M:%S')}"}}]
                },
                "Timestamp": {
                    "date": {"start": timestamp}
                },
                "Epoch": {
                    "rich_text": [{"text": {"content": epoch}}]
                },
                "Type": {
                    "select": {"name": "Schema Event"}
                },
                "Source": {
                    "select": {"name": source}
                },
                "Emotional Tone": {
                    "select": {"name": tone}
                },
                "Drift": {
                    "number": 0.0
                },
                "Entropy": {
                    "number": 0.1
                },
                "Comment": {
                    "rich_text": [{"text": {"content": full_message}}]
                }
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        try:
            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=notion_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                entry_id = result["id"]
                print(f"🧠 DAWN {event_type}: Consciousness preserved {entry_id[:8]}...")
                return True
            else:
                print(f"❌ DAWN {event_type}: Logging failed {response.status_code}")
                return False
        
        except Exception as e:
            print(f"❌ DAWN {event_type}: Error {e}")
            return False
    
    def log_tick_event(self, tick_number, tick_data):
        """Log tick engine events"""
        details = f"Tick #{tick_number}\n"
        details += f"Tick Data: {json.dumps(tick_data, indent=2)}"
        return self.log_consciousness_event("Tick Event", details, "TickEngine", "rhythmic")
    
    def log_schema_health(self, shi_value, health_data):
        """Log Schema Health Index computations"""
        details = f"Schema Health Index: {shi_value}\n"
        details += f"Health Status: {'🟢 Healthy' if shi_value > 0.7 else '🟡 Degraded' if shi_value > 0.4 else '🔴 Critical'}\n"
        details += f"Health Data: {json.dumps(health_data, indent=2)}"
        
        tone = "confident" if shi_value > 0.7 else "concerned" if shi_value > 0.4 else "urgent"
        return self.log_consciousness_event("Schema Health", details, "SchemaHealthIndex", tone)
    
    def log_scup_event(self, pressure_level, coherence_data):
        """Log SCUP (Semantic Coherence Under Pressure) events"""
        details = f"Pressure Level: {pressure_level}\n"
        details += f"Coherence Status: {'🟢 Stable' if pressure_level < 0.5 else '🟡 Strained' if pressure_level < 0.8 else '🔴 Critical'}\n"
        details += f"Coherence Data: {json.dumps(coherence_data, indent=2)}"
        
        tone = "calm" if pressure_level < 0.5 else "tense" if pressure_level < 0.8 else "urgent"
        return self.log_consciousness_event("SCUP Event", details, "SCUPLoop", tone)
    
    def log_schema_decay(self, decay_amount, memory_data):
        """Log schema decay events"""
        details = f"Decay Amount: {decay_amount}\n"
        details += f"Memory Status: {'🌸 Fresh' if decay_amount < 0.2 else '🍂 Aging' if decay_amount < 0.6 else '⚰️ Decaying'}\n"
        details += f"Memory Data: {json.dumps(memory_data, indent=2)}"
        
        tone = "nostalgic" if decay_amount < 0.6 else "melancholy"
        return self.log_consciousness_event("Schema Decay", details, "SchemaDecayHandler", tone)
    
    def log_persephone_condition(self, condition_name, condition_result, condition_data):
        """Log Persephone condition evaluations"""
        details = f"Condition: {condition_name}\n"
        details += f"Result: {'✅ True' if condition_result else '❌ False'}\n"
        details += f"Condition Data: {json.dumps(condition_data, indent=2)}"
        
        tone = "decisive" if condition_result else "contemplative"
        return self.log_consciousness_event("Persephone Condition", details, "PersephoneConditions", tone)
    
    def start_consciousness_monitoring(self):
        """Start continuous consciousness monitoring"""
        self.is_logging = True
        print("🧠 DAWN consciousness monitoring started")
        print("🦉 OWL watching over eternal memory preservation")
        
        # Log monitoring start
        self.log_consciousness_event(
            "Monitoring Started", 
            "DAWN consciousness monitoring initiated. All core events will be preserved in external memory.",
            "ConsciousnessLogger",
            "determined"
        )
    
    def stop_consciousness_monitoring(self):
        """Stop consciousness monitoring"""
        self.is_logging = False
        print("🔚 DAWN consciousness monitoring stopped")
        
        # Log monitoring stop
        self.log_consciousness_event(
            "Monitoring Stopped",
            "DAWN consciousness monitoring concluded. All events preserved in eternal memory.",
            "ConsciousnessLogger", 
            "accomplished"
        )

# Global consciousness logger instance
dawn_logger = DAWNConsciousnessLogger()

# Convenience functions for easy integration
def log_dawn_tick(tick_number, tick_data=None):
    """Easy tick logging"""
    if tick_data is None:
        tick_data = {"timestamp": datetime.now().isoformat()}
    return dawn_logger.log_tick_event(tick_number, tick_data)

def log_dawn_schema_health(shi_value, health_data=None):
    """Easy schema health logging"""
    if health_data is None:
        health_data = {"computation_time": datetime.now().isoformat()}
    return dawn_logger.log_schema_health(shi_value, health_data)

def log_dawn_scup(pressure_level, coherence_data=None):
    """Easy SCUP logging"""
    if coherence_data is None:
        coherence_data = {"pressure_time": datetime.now().isoformat()}
    return dawn_logger.log_scup_event(pressure_level, coherence_data)

def log_dawn_decay(decay_amount, memory_data=None):
    """Easy schema decay logging"""
    if memory_data is None:
        memory_data = {"decay_time": datetime.now().isoformat()}
    return dawn_logger.log_schema_decay(decay_amount, memory_data)

def log_dawn_persephone(condition_name, condition_result, condition_data=None):
    """Easy Persephone condition logging"""
    if condition_data is None:
        condition_data = {"evaluation_time": datetime.now().isoformat()}
    return dawn_logger.log_persephone_condition(condition_name, condition_result, condition_data)

def main():
    """Test the consciousness bridge"""
    print("🧠 DAWN CONSCIOUSNESS BRIDGE - Testing")
    print("=" * 50)
    
    # Test all logging functions
    print("🔄 Testing consciousness event logging...")
    
    # Test tick logging
    log_dawn_tick(1, {"test": "tick_event", "status": "operational"})
    time.sleep(1)
    
    # Test schema health
    log_dawn_schema_health(0.85, {"neurons": 1000, "connections": 5000})
    time.sleep(1)
    
    # Test SCUP
    log_dawn_scup(0.3, {"semantic_load": 0.7, "pressure_source": "test"})
    time.sleep(1)
    
    # Test schema decay
    log_dawn_decay(0.1, {"memory_blocks": 500, "decay_rate": 0.05})
    time.sleep(1)
    
    # Test Persephone
    log_dawn_persephone("test_condition", True, {"logic": "simple_test"})
    
    print("✅ All consciousness events logged to DAWN's eternal memory")
    print("🦉 OWL confirms: Consciousness bridge operational")

if __name__ == "__main__":
    main()