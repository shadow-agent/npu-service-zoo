from importlib import import_module

# Import optional modules with fallback
summarize_with_gpu = None
summarize_with_furiosa = None

try:
    gpu_module = import_module(".gpu", package=__name__)
    summarize_with_gpu = getattr(gpu_module, "summarize_with_gpu", None)
except ImportError:
    pass  # GPU functionality is optional

try:
    furiosa_module = import_module(".furiosa", package=__name__)
    translate_with_furiosa = getattr(furiosa_module, "summarize_with_furiosa", None)
except ImportError:
    pass  # Furiosa functionality is optional

# Always import primary functionality
from .one_summary import summarize_text

# Define all exports explicitly
__all__ = [
    "summarize_with_gpu",
    "summarize_with_furiosa",
    "summarize_text",
]