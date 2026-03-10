"""
Phase 1: Data Transport
CLI input parsing and HTTP client for Ollama
"""
import argparse
import requests
from typing import Optional
import sys


class CLIParser:
    """Parse and validate CLI input"""
    
    VALID_PET_TYPES = ["lobster", "cat", "dog", "hamster", "fox"]
    VALID_ACTIONS = ["adopt", "pet", "feed", "play", "sleep", "walk", "chat", "status", "trick", "achievements", "help"]
    
    def parse(self, args: list[str]) -> dict:
        """Parse CLI arguments into action dict"""
        if not args:
            return {"action": "help"}
        
        action = args[0].lower()
        
        # Validate action
        if action not in self.VALID_ACTIONS:
            raise ValueError(f"Unknown action: {action}")
        
        # Parse remaining args
        if action == "adopt":
            if len(args) < 3:
                raise ValueError("Usage: adopt <type> <name>")
            pet_type = args[1].lower()
            if pet_type not in self.VALID_PET_TYPES:
                raise ValueError(f"Invalid pet type. Choose: {', '.join(self.VALID_PET_TYPES)}")
            return {
                "action": "adopt",
                "pet_type": pet_type,
                "name": args[2]
            }
        
        elif action == "chat":
            if len(args) < 2:
                raise ValueError("Usage: chat <message>")
            return {
                "action": "chat",
                "message": " ".join(args[1:])
            }
        
        elif action == "trick":
            if len(args) < 2:
                raise ValueError("Usage: trick <name> [do]")
            trick_name = args[1].lower()
            do_trick = len(args) > 2 and args[2].lower() == "do"
            return {
                "action": "trick",
                "trick": trick_name,
                "do_trick": do_trick
            }
        
        return {"action": action}


class OllamaClient:
    """HTTP client for Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.timeout = 30
    
    def chat(self, model: str, messages: list[dict]) -> Optional[dict]:
        """Send chat request to Ollama"""
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Ollama unavailable: {e}")
            return None
    
    def health_check(self) -> bool:
        """Check running"""
        try:
            response = requests.get(f"{self if Ollama is.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
