import logging
import os
from time import time, sleep
import threading
from functools import wraps
from environment import detect_environment
from metrics.performance_metrics import calculate_power_consumption

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Store the detected environment and the corresponding translation function
_environment = None
_translation_function = None

def initialize_translation_environment(llm_model: str):
    """
    Detects the translation environment and sets the corresponding translation function.

    Raises:
        EnvironmentError: If no suitable environment is detected.
    """
    global _environment, _translation_function, _devices
    _devices = []
    env_info = detect_environment()
    _environment = env_info["environment"]
    _devices = env_info["devices"]
    
    if _environment == "gpu":
        from translate.gpu import translate_with_gpu
        _translation_function = monitor_power(lambda text, src, tgt: translate_with_gpu(text, src, tgt, llm_model=llm_model))
        logging.info("Translation environment detected: GPU. Using GPU for translations.")
    elif _environment == "furiosa":
        from translate.furiosa import translate_with_furiosa
        _translation_function = monitor_power(translate_with_furiosa)
        logging.info("Translation environment detected: Furiosa NPU. Using NPU for translations.")
    else:
        error_message = (
            "No suitable environment detected. "
            "Ensure that either a CUDA-enabled GPU or Furiosa NPU is properly configured."
        )
        logging.error(error_message)
        raise EnvironmentError(error_message)



def monitor_power(func):
    """
    Decorator to monitor power consumption during the execution of the translation function.

    Args:
        func (function): The translation function to wrap.

    Returns:
        function: The wrapped function with monitoring.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        _monitoring_enabled = os.getenv("ENABLE_MONITORING", "false").lower() == "true"
        if not _monitoring_enabled:
            return func(*args, **kwargs)

        # Detect environment and initialize monitoring
        devices = _devices  # Use the detected devices from environment detection
        power_data = {device: [] for device in devices}
        timing_data = {device: [] for device in devices}
        stop_event = threading.Event()

        def monitor():
            start_time = time()
            while not stop_event.is_set():
                for device in devices:
                    power = calculate_power_consumption(device)
                    power_data[device].append(power)
                    timing_data[device].append(round(time() - start_time, 2))
                sleep(0.1)  # Sampling interval

        # Start monitoring in a separate thread
        monitor_thread = threading.Thread(target=monitor)
        monitor_thread.start()

        try:
            # Execute the original translation function
            result = func(*args, **kwargs)
        finally:
            # Stop monitoring
            stop_event.set()
            monitor_thread.join()

        # Calculate total power consumption
        total_power_absolute = sum(
            sum(data) for data in power_data.values()
        )
        total_power_relative = {
            device: sum(data) / total_power_absolute if total_power_absolute > 0 else 0.0
            for device, data in power_data.items()
        }

        # # Log power consumption data
        # logging.info(f"Total Power Consumption (Absolute): {total_power_absolute} W")
        # logging.info(f"Power Data (Relative by Device): {total_power_relative}")
        # for device, data in power_data.items():
        #     logging.info(f"Power Data for {device}: {data}")
        #     logging.info(f"Timing Data for {device}: {timing_data[device]}")

        # Attach monitoring results to the function's return value
        if isinstance(result, dict):
            result["total_power"] = {
                "absolute": total_power_absolute,
                "relative": total_power_relative,
            }
            result["power_data"] = power_data
            result["timing_data"] = timing_data

        return result

    return wrapper


def translate_text(input_text, source_language="Korean", target_language="English"):
    """
    Translates text using the pre-determined environment and translation function.

    Args:
        input_text (str): Text to be translated.
        source_language (str): Source language (default: "Korean").
        target_language (str): Target language (default: "English").

    Returns:
        str: Translated text.

    Raises:
        RuntimeError: If the translation environment is not initialized.
    """
    if _translation_function is None:
        raise RuntimeError("Translation environment not initialized. Call initialize_translation_environment first.")
    
    return _translation_function(input_text, source_language, target_language)

@monitor_power
def batch_translate_text(input_texts, source_language="Korean", target_language="English"):
    """
    Batch translate multiple texts using the pre-determined environment.

    Args:
        input_texts (list): List of texts to translate.
        source_language (str): Source language (default: "Korean").
        target_language (str): Target language (default: "English").

    Returns:
        dict: Translated texts and monitoring data.
    """
    translations = []
    for text in input_texts:
        start_time = time()
        result = translate_text(text, source_language=source_language, target_language=target_language)
        elapsed_time = time() - start_time

        # Add elapsed time to the result
        result_with_time = {
            "translation": result,
            "elapsed_time": elapsed_time
        }
        translations.append(result_with_time)

    # Wrap results and monitoring data into a single dict
    return {
        "translations": translations,
        # Monitoring data will be attached by the `monitor_power` decorator
    }