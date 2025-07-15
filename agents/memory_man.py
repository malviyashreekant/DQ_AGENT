import json
import os
from datetime import datetime
from typing import Dict, List, Any
import logging

class DQMemory:
    def __init__(self, path="dq_memory.json", max_entries=1000):
        self.path = path
        self.max_entries = max_entries
        self.logger = logging.getLogger(__name__)
        self.memory = self._load_memory()

    def _load_memory(self) -> List[Dict[str, Any]]:
        """Load memory from file with error handling"""
        try:
            if os.path.exists(self.path):
                with open(self.path, "r") as f:
                    memory = json.load(f)
                    if not isinstance(memory, list):
                        self.logger.warning("Memory file corrupted, starting fresh")
                        return []
                    return memory
        except Exception as e:
            self.logger.error(f"Failed to load memory: {str(e)}")
        
        return []

    def log(self, event: Dict[str, Any]):
        """Log an event with timestamp and rotation"""
        try:
            # Add metadata
            enhanced_event = {
                'timestamp': datetime.now().isoformat(),
                'session_id': os.getpid(),  # Simple session tracking
                **event
            }
            
            self.memory.append(enhanced_event)
            
            # Rotate if needed
            if len(self.memory) > self.max_entries:
                self.memory = self.memory[-self.max_entries:]
                self.logger.info(f"Memory rotated, keeping last {self.max_entries} entries")
            
            self._save_memory()
            
        except Exception as e:
            self.logger.error(f"Failed to log event: {str(e)}")

    def _save_memory(self):
        """Save memory to file"""
        try:
            with open(self.path, "w") as f:
                json.dump(self.memory, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save memory: {str(e)}")

    def get_memory(self) -> List[Dict[str, Any]]:
        """Get all memory entries"""
        return self.memory.copy()

    def get_recent_entries(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent memory entries"""
        return self.memory[-count:]

    def clear_memory(self):
        """Clear all memory entries"""
        self.memory = []
        self._save_memory()
        self.logger.info("Memory cleared")