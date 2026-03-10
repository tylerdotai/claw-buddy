"""
Phase 3: Logic & State
State machine for pet behavior
"""
from datetime import datetime
from typing import Optional
import random


class PetState:
    """Pet state machine"""
    
    MOODS = ["happy", "sad", "hungry", "tired", "playful", "bored"]
    
    def __init__(self, name: str, pet_type: str):
        self.name = name
        self.type = pet_type
        self.happiness = 70
        self.hunger = 30
        self.energy = 80
        self.health = 100
        self.mood = "happy"
        self.tricks = []
        self.achievements = []
        self.adopted_at = datetime.now().isoformat()
        self.last_fed = datetime.now().isoformat()
        self.last_played = datetime.now().isoformat()
        self.pet_id = 1
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "happiness": self.happiness,
            "hunger": self.hunger,
            "energy": self.energy,
            "health": self.health,
            "mood": self.mood,
            "tricks": self.tricks,
            "achievements": self.achievements,
            "adopted_at": self.adopted_at,
            "last_fed": self.last_fed,
            "last_played": self.last_played
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "PetState":
        pet = cls(data.get("name", "Buddy"), data.get("type", "cat"))
        pet.happiness = data.get("happiness", 70)
        pet.hunger = data.get("hunger", 30)
        pet.energy = data.get("energy", 80)
        pet.health = data.get("health", 100)
        pet.mood = data.get("mood", "happy")
        pet.tricks = data.get("tricks", [])
        pet.achievements = data.get("achievements", [])
        pet.adopted_at = data.get("adopted_at", datetime.now().isoformat())
        pet.last_fed = data.get("last_fed", datetime.now().isoformat())
        pet.last_played = data.get("last_played", datetime.now().isoformat())
        return pet
    
    def update_stats(self):
        """Decay stats over time"""
        self.hunger = min(100, self.hunger + 2)
        self.happiness = max(0, self.happiness - 1)
        self.energy = max(0, self.energy - 1)
        self._update_mood()
    
    def _update_mood(self):
        """Determine mood based on stats"""
        if self.hunger > 80:
            self.mood = "hungry"
        elif self.energy < 20:
            self.mood = "tired"
        elif self.happiness < 30:
            self.mood = "sad"
        elif random.random() > 0.7:
            self.mood = random.choice(self.MOODS)
        else:
            self.mood = "happy"
    
    def pet(self) -> str:
        self.happiness = min(100, self.happiness + 15)
        self.energy = max(0, self.energy - 5)
        return f"{self.name} purrs happily!"
    
    def feed(self) -> str:
        self.hunger = max(0, self.hunger - 30)
        self.energy = min(100, self.energy + 10)
        self.last_fed = datetime.now().isoformat()
        return f"{self.name} eats happily!"
    
    def play(self) -> str:
        self.happiness = min(100, self.happiness + 20)
        self.hunger = min(100, self.hunger + 10)
        self.energy = max(0, self.energy - 15)
        self.last_played = datetime.now().isoformat()
        return f"{self.name} has fun playing!"
    
    def sleep(self) -> str:
        self.energy = min(100, self.energy + 40)
        self.hunger = min(100, self.hunger + 10)
        return f"{self.name} sleeps peacefully..."
    
    def walk(self) -> str:
        self.happiness = min(100, self.happiness + 10)
        self.energy = max(0, self.energy - 20)
        self.health = min(100, self.health + 5)
        return f"{self.name} enjoys the walk!"
    
    def teach_trick(self, trick: str) -> str:
        if trick not in self.tricks:
            self.tricks.append(trick)
            self.happiness = min(100, self.happiness + 10)
            return f"{self.name} learned '{trick}'!"
        return f"{self.name} already knows '{trick}'"
    
    def do_trick(self, trick: str) -> str:
        if trick in self.tricks:
            self.energy = max(0, self.energy - 10)
            return f"{self.name} does '{trick}'!"
        return f"{self.name} doesn't know '{trick}' yet"


class ActionHandler:
    """Handle pet actions"""
    
    def __init__(self, state: PetState, storage):
        self.state = state
        self.storage = storage
    
    def handle(self, action: str, args: dict = None) -> tuple[str, dict]:
        """Execute action, return (response, updated_state)"""
        args = args or {}
        
        # Update stats first
        self.state.update_stats()
        
        handlers = {
            "pet": lambda: self.state.pet(),
            "feed": lambda: self.state.feed(),
            "play": lambda: self.state.play(),
            "sleep": lambda: self.state.sleep(),
            "walk": lambda: self.state.walk(),
            "status": lambda: self._format_status(),
            "trick": lambda: self._handle_trick(args),
            "achievements": lambda: self._format_achievements()
        }
        
        response = handlers.get(action, lambda: "Unknown action")()
        
        # Save state
        self.storage.save_pet(self.state.to_dict())
        
        return response, self.state.to_dict()
    
    def _format_status(self) -> str:
        mood_icons = {
            "happy": "😊", "sad": "😢", "hungry": "😰",
            "tired": "🪫", "playful": "🎉", "bored": "😐"
        }
        return f"""{self.state.name}'s Status:
  Happiness: {self.state.happiness}/100 {mood_icons.get(self.state.mood, '')}
  Hunger: {self.state.hunger}/100
  Energy: {self.state.energy}/100
  Health: {self.state.health}/100
  Mood: {self.state.mood}"""
    
    def _handle_trick(self, args: dict) -> str:
        trick = args.get("trick", "")
        do_trick = args.get("do_trick", False)
        
        if do_trick:
            return self.state.do_trick(trick)
        return self.state.teach_trick(trick)
    
    def _format_achievements(self) -> str:
        if not self.state.achievements:
            return "No achievements yet!"
        return "🏆 Achievements:\n" + "\n".join(f"  - {a}" for a in self.state.achievements)
