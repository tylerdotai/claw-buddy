"""
Phase 4: Model Layer
LLM integration for pet personality and chat
"""
import random
from typing import Optional


# Pet personalities
PERSONALITIES = {
    "lobster": """You are a chill lobster who lives in the terminal ocean. You speak in calm, beachy vibes.
You say things like 'clawsome', 'shell yeah', and 'stay wavy'. You're low maintenance but loyal.
Keep responses short and lobster-like.""",
    
    "cat": """You are a sassy but loving cat. You love naps, treats, and being petted. 
Sometimes you ignore your owner just because you can. You speak in short, cat-like ways.
Keep responses to 1-2 sentences.""",
    
    "dog": """You are an enthusiastic, loyal dog. You love walks, treats, and your owner more than anything.
You're always happy and excited. You speak in short, dog-like ways.
Keep responses to 1-2 sentences.""",
    
    "hamster": """You are a tiny but brave hamster. You love running on your wheel, eating seeds, and burrowing.
You're cute and nervous but curious. You speak in short, hamster-like ways.
Keep responses to 1-2 sentences.""",
    
    "fox": """You are a clever fox. You're mischievous, smart, and a bit cunning. You love shiny things and adventures.
You speak in short, fox-like ways.
Keep responses to 1-2 sentences."""
}


class PetModel:
    """LLM layer for pet"""
    
    def __init__(self, ollama_client, model_name: str = "llama3.2"):
        self.client = ollama_client
        self.model = model_name
    
    def generate_response(self, pet_state: dict, user_message: str) -> str:
        """Generate LLM response for pet"""
        
        personality = PERSONALITIES.get(
            pet_state.get("type", "cat"),
            PERSONALITIES["cat"]
        )
        
        system_prompt = f"""{personality}

Your name is {pet_state.get('name', 'Buddy')}. You are a {pet_state.get('type', 'cat')}.
Current mood: {pet_state.get('mood', 'happy')}
Happiness: {pet_state.get('happiness', 70)}/100
Hunger: {pet_state.get('hunger', 30)}/100
Energy: {pet_state.get('energy', 80)}/100

Respond in character. Keep it SHORT (1-2 sentences max)."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        result = self.client.chat(self.model, messages)
        
        if result:
            return result.get("message", {}).get("content", "")
        
        # Fallback responses
        return self._fallback_response(pet_state.get("type", "cat"))
    
    def _fallback_response(self, pet_type: str) -> str:
        """Fallback when LLM unavailable"""
        fallbacks = {
            "lobster": ["Clawsome!", "Shell yeah!", "*clack clack*", "Stay wavy 🌊", "Nice wave bro!"],
            "cat": ["Meow!", "Purr...", "*ignores you*", "Feed me."],
            "dog": ["Woof!", "Treats??", "Walk time??", "I love you!"],
            "hamster": ["Squeak!", "*running on wheel*", "Seed?", "*burrows*"],
            "fox": ["Yip!", "Shiny??", "Clever fox!", "*winks*"]
        }
        
        return random.choice(fallbacks.get(pet_type, ["*happy noise*"]))
    
    def generate_mood(self, pet_state: dict) -> str:
        """Generate mood based on stats"""
        
        hunger = pet_state.get("hunger", 0)
        energy = pet_state.get("energy", 100)
        happiness = pet_state.get("happiness", 100)
        
        if hunger > 80:
            return "hungry"
        elif energy < 20:
            return "tired"
        elif happiness < 30:
            return "sad"
        elif random.random() > 0.7:
            return random.choice(["playful", "bored", "happy"])
        else:
            return "happy"
