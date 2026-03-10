"""
Phase 5: Reliability
Validation, logging, error handling
"""
import logging
import sys
from functools import wraps
from typing import Callable
import traceback


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("digital-pet.log")
    ]
)
logger = logging.getLogger("digital-pet")


def validate_input(schema: dict) -> Callable:
    """Input validation decorator"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Basic validation
            if "action" in kwargs:
                action = kwargs["action"]
                allowed = ["adopt", "pet", "feed", "play", "sleep", "walk", "chat", "status", "trick", "achievements"]
                if action not in allowed:
                    raise ValueError(f"Invalid action: {action}")
            
            logger.info(f"Executing: {func.__name__}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Completed: {func.__name__}")
                return result
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}")
                logger.debug(traceback.format_exc())
                raise
        return wrapper
    return decorator


class PetError(Exception):
    """Base exception for pet errors"""
    pass


class ValidationError(PetError):
    """Invalid input"""
    pass


class StorageError(PetError):
    """Storage operation failed"""
    pass


class ModelError(PetError):
    """LLM operation failed"""
    pass


class ErrorHandler:
    """Central error handling"""
    
    @staticmethod
    def handle(e: Exception) -> str:
        """Return user-friendly error message"""
        
        error_messages = {
            ValidationError: "Invalid input. Check your command.",
            StorageError: "Failed to save pet data.",
            ModelError: "LLM unavailable. Try again later.",
            PetError: "Something went wrong."
        }
        
        for exc_type, message in error_messages.items():
            if isinstance(e, exc_type):
                logger.error(f"{exc_type.__name__}: {e}")
                return f"❌ {message}"
        
        # Unknown error
        logger.critical(f"Unknown error: {e}")
        logger.debug(traceback.format_exc())
        return "❌ An unexpected error occurred."


class HealthCheck:
    """Health check for system"""
    
    def __init__(self, storage, ollama_client):
        self.storage = storage
        self.ollama = ollama_client
    
    def check(self) -> dict:
        """Run health checks"""
        
        results = {
            "storage": False,
            "ollama": False,
            "pet_loaded": False
        }
        
        # Check storage
        try:
            self.storage.load_pet()
            results["storage"] = True
        except Exception as e:
            logger.warning(f"Storage check failed: {e}")
        
        # Check Ollama
        try:
            if self.ollama.health_check():
                results["ollama"] = True
        except Exception as e:
            logger.warning(f"Ollama check failed: {e}")
        
        # Check pet
        try:
            pet = self.storage.load_pet()
            results["pet_loaded"] = pet is not None
        except Exception as e:
            logger.warning(f"Pet check failed: {e}")
        
        all_healthy = all(results.values())
        
        return {
            "healthy": all_healthy,
            "checks": results
        }
