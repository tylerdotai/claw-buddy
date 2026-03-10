"""
Digital Pet - Main Entry Point
Built using 5-phase agent architecture
"""
import sys
import logging

# Import all phases
from data import CLIParser, OllamaClient
from storage import PetStorage
from logic import PetState, ActionHandler
from model import PetModel
from reliability import ErrorHandler, HealthCheck, logger


def main():
    """Main entry point"""
    logger.info("Digital Pet started")
    
    # Initialize components
    parser = CLIParser()
    storage = PetStorage("pet.db")
    ollama = OllamaClient()
    model = PetModel(ollama)
    error_handler = ErrorHandler()
    
    # Parse input
    try:
        parsed = parser.parse(sys.argv[1:])
    except ValueError as e:
        print(f"❌ {e}")
        print("Usage: python -m src.main adopt <type> <name>")
        print("Types: cat, dog, hamster, fox")
        return
    
    action = parsed.get("action")
    
    # Handle actions
    try:
        if action == "help":
            print("""
🐾 Digital Pet

Usage: python -m src.main <command>

Commands:
  adopt <type> <name>  - Adopt a new pet
  status                - Check pet stats
  pet                  - Pet your animal
  feed                 - Feed your pet
  play                 - Play with your pet
  sleep                - Put pet to sleep
  walk                 - Take pet for a walk
  chat <message>       - Talk to your pet
  trick <name>        - Teach/perform trick
  achievements         - View achievements
  health               - System health check
            """)
            return
        
        if action == "health":
            health = HealthCheck(storage, ollama)
            results = health.check()
            print(f"Health: {'✅' if results['healthy'] else '❌'}")
            for check, status in results['checks'].items():
                print(f"  {check}: {'✅' if status else '❌'}")
            return
        
        # Load existing pet
        pet_data = storage.load_pet()
        
        if action == "adopt":
            # Create new pet
            state = PetState(parsed["name"], parsed["pet_type"])
            storage.save_pet(state.to_dict())
            print(f"🎉 You adopted a {parsed['pet_type']} named {parsed['name']}!")
            return
        
        if not pet_data:
            print("❌ You don't have a pet yet!")
            print("   Adopt one: python -m src.main adopt cat Buddy")
            return
        
        # Create state from storage
        state = PetState.from_dict(pet_data)
        handler = ActionHandler(state, storage)
        
        if action == "chat":
            # Use LLM for chat
            user_message = parsed.get("message", "")
            print(f"You: {user_message}")
            response = model.generate_response(state.to_dict(), user_message)
            print(f"{state.name}: {response}")
            
            # Log conversation
            storage.add_message(state.pet_id, "user", user_message)
            storage.add_message(state.pet_id, "assistant", response)
            return
        
        # Handle other actions
        response, updated_state = handler.handle(action, parsed)
        print(response)
        
    except Exception as e:
        print(error_handler.handle(e))
        logger.error(f"Fatal error: {e}")
        return


if __name__ == "__main__":
    main()
