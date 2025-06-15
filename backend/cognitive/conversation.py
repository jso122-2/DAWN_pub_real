from typing import Dict, Any, Optional, List
from datetime import datetime
import numpy as np

class ConversationModule:
    def __init__(self):
        self.conversation_state = {
            "context": {},
            "history": [],
            "active_topics": [],
            "sentiment": 0.0,
            "engagement": 0.0
        }
        self.last_update = datetime.now()
        self._active = True
    
    def is_active(self) -> bool:
        return self._active
    
    def get_metrics(self) -> Dict[str, Any]:
        return {
            "conversation_state": self.conversation_state,
            "last_update": self.last_update.isoformat(),
            "active": self._active
        }
    
    def configure(self, config: Dict[str, Any]) -> None:
        if "active" in config:
            self._active = config["active"]
        if "conversation_state" in config:
            self.conversation_state.update(config["conversation_state"])
        self.last_update = datetime.now()
    
    def update(self, new_state: Dict[str, Any]) -> None:
        self.conversation_state.update(new_state)
        self.last_update = datetime.now()
    
    def add_message(self, message: Dict[str, Any]) -> None:
        self.conversation_state["history"].append({
            **message,
            "timestamp": datetime.now().isoformat()
        })
        if len(self.conversation_state["history"]) > 1000:  # Keep last 1000 messages
            self.conversation_state["history"].pop(0)
    
    def get_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self.conversation_state["history"][-limit:]
    
    def get_context(self) -> Dict[str, Any]:
        return self.conversation_state["context"]
    
    def update_context(self, new_context: Dict[str, Any]) -> None:
        self.conversation_state["context"].update(new_context)
    
    def get_active_topics(self) -> List[str]:
        return self.conversation_state["active_topics"]
    
    def add_topic(self, topic: str) -> None:
        if topic not in self.conversation_state["active_topics"]:
            self.conversation_state["active_topics"].append(topic)
    
    def remove_topic(self, topic: str) -> None:
        if topic in self.conversation_state["active_topics"]:
            self.conversation_state["active_topics"].remove(topic)
    
    def get_sentiment(self) -> float:
        return self.conversation_state["sentiment"]
    
    def get_engagement(self) -> float:
        return self.conversation_state["engagement"]
    
    def clear_history(self) -> None:
        self.conversation_state["history"] = []
    
    def clear_context(self) -> None:
        self.conversation_state["context"] = {}
    
    def clear_topics(self) -> None:
        self.conversation_state["active_topics"] = [] 