import logging
import os
from time import time
from common.environment import detect_environment
from common.monitoring import monitor_power

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Global instances for environment and summarization function
_environment = None
_summarization_function = None
_devices = []

def initialize_summarization_environment(llm_model: str = "default_model"):
    """
    Detects the summarization environment and initializes the corresponding summarization function.

    Args:
        llm_model (str): The LLM model to use. Default: "default_model".

    Raises:
        EnvironmentError: If no suitable environment is detected.
    """
    global _environment, _summarization_function, _devices

    env_info = detect_environment()
    _environment = env_info["environment"]
    _devices = env_info.get("devices", [])

    if _environment == "gpu":
        from summarization.gpu import summarize_with_gpu
        _summarization_function = monitor_power(
            lambda text: summarize_with_gpu(text, llm_model=llm_model),
            devices=_devices
        )
        logging.info("Summarization environment detected: GPU. Using GPU for summarization.")
    elif _environment == "furiosa":
        from summarization.furiosa import summarize_with_furiosa
        _summarization_function = monitor_power(summarize_with_furiosa, devices=_devices)
        logging.info("Summarization environment detected: Furiosa NPU. Using NPU for summarization.")
    else:
        error_message = (
            "No suitable environment detected. "
            "Ensure that either a CUDA-enabled GPU or Furiosa NPU is properly configured."
        )
        logging.error(error_message)
        raise EnvironmentError(error_message)


def summarize_text(input_text: str) -> str:
    """
    Summarizes text using the pre-determined environment and summarization function.

    Args:
        input_text (str): Text to be summarized.

    Returns:
        str: Summarized text.

    Raises:
        RuntimeError: If the summarization environment is not initialized.
    """
    if _summarization_function is None:
        raise RuntimeError("Summarization environment not initialized. Call initialize_summarization_environment first.")

    return _summarization_function(input_text)


def batch_summarize_text(input_texts: list) -> dict:
    """
    Batch summarize multiple texts using the pre-determined environment.

    Args:
        input_texts (list): List of texts to summarize.

    Returns:
        dict: Summarized texts and monitoring data.
    """
    summaries = []
    for text in input_texts:
        start_time = time()
        result = summarize_text(text)
        elapsed_time = time() - start_time

        summaries.append({
            "summary": result,
            "elapsed_time": elapsed_time
        })

    return {
        "summaries": summaries
    }