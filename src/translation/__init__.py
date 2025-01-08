try:
    from .gpu import translate_with_gpu
except ImportError:
    translate_with_gpu = None  # Fallback if GPU is not available

try:
    from .furiosa import translate_with_furiosa
except ImportError:
    translate_with_furiosa = None  # Fallback if Furiosa LLM is not available

from .one_trans import translate_text

__all__ = [
    "translate_with_gpu",
    "translate_with_furiosa",
    "translate_text",
]