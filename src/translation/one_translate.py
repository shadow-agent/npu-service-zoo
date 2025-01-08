import logging
from time import time
from ..common.environment import detect_environment
from ..common.monitoring import monitor_power

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Global instances for environment and translation function
_environment = None
_translation_function = None

def initialize_translation_environment(llm_model: str = "default_model"):
    """
    Detects the translation environment and initializes the corresponding translation function.

    Args:
        llm_model (str): The LLM model to use. Default: "default_model".

    Raises:
        EnvironmentError: If no suitable environment is detected.
    """
    global _environment, _translation_function, _devices
    _devices = []
    env_info = detect_environment()
    _environment = env_info["environment"]
    _devices = env_info["devices"]

    if _environment == "gpu":
        from .gpu import translate_with_gpu
        _translation_function = monitor_power(lambda text, src, tgt: translate_with_gpu(text, src, tgt, llm_model=llm_model))
        logging.info("Translation environment detected: GPU. Using GPU for translations.")
    elif _environment == "furiosa":
        from .furiosa import translate_with_furiosa
        _translation_function = monitor_power(translate_with_furiosa)
        logging.info("Translation environment detected: Furiosa NPU. Using NPU for translations.")
    else:
        error_message = (
            "No suitable environment detected. "
            "Ensure that either a CUDA-enabled GPU or Furiosa NPU is properly configured."
        )
        logging.error(error_message)
        raise EnvironmentError(error_message)


def translate_text(input_text: str, source_language: str = "Korean", target_language: str = "English") -> str:
    """
    Translates text using the pre-determined environment and translation function.

    Args:
        input_text (str): Text to be translated.
        source_language (str): Source language. Default: "Korean".
        target_language (str): Target language. Default: "English".

    Returns:
        str: Translated text.

    Raises:
        RuntimeError: If the translation environment is not initialized.
    """
    if _translation_function is None:
        raise RuntimeError("Translation environment not initialized. Call initialize_translation_environment first.")

    return _translation_function(input_text, source_language, target_language)


def batch_translate_text(input_texts: list, source_language: str = "Korean", target_language: str = "English") -> dict:
    """
    Batch translate multiple texts using the pre-determined environment.

    Args:
        input_texts (list): List of texts to translate.
        source_language (str): Source language. Default: "Korean".
        target_language (str): Target language. Default: "English".

    Returns:
        dict: Translated texts and monitoring data.
    """
    translations = []
    for text in input_texts:
        start_time = time()
        result = translate_text(text, source_language=source_language, target_language=target_language)
        elapsed_time = time() - start_time

        translations.append({
            "translation": result,
            "elapsed_time": elapsed_time
        })

    return {
        "translations": translations
    }