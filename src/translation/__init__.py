from importlib import import_module

# Import optional modules with fallback
translate_with_gpu = None
translate_with_furiosa = None

try:
    gpu_module = import_module(".gpu", package=__name__)
    translate_with_gpu = getattr(gpu_module, "translate_with_gpu", None)
except ImportError:
    pass  # GPU functionality is optional

try:
    furiosa_module = import_module(".furiosa", package=__name__)
    translate_with_furiosa = getattr(furiosa_module, "translate_with_furiosa", None)
except ImportError:
    pass  # Furiosa functionality is optional

# Always import primary functionality
from .one_translate import translate_text

# Define all exports explicitly
__all__ = [
    "translate_with_gpu",
    "translate_with_furiosa",
    "translate_text",
]