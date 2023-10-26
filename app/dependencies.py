from models.model_manager import ModelsPool


pool = ModelsPool()

def get_pool() -> ModelsPool:
    return pool