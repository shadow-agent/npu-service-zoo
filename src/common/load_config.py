import yaml

def load_config(config_path: str):
    """
    Load the full configuration from the config file.

    Parameters:
        config_path (str): Path to the config YAML file.

    Returns:
        dict: Parsed configuration dictionary or an empty dictionary if the file is missing.
    """
    try:
        with open(config_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Config file not found at: {config_path}. Using default settings.")
        return {}

def load_active_metrics(config_path: str):
    """
    Load active metrics (set to True) from the config file.

    Parameters:
        config_path (str): Path to the config YAML file.

    Returns:
        list: A list of active metrics or default metrics if not specified.
    """
    config = load_config(config_path)
    metrics_config = config.get("evaluation", {}).get("metrics", {})
    active_metrics = [metric for metric, is_active in metrics_config.items() if is_active]
    return active_metrics if active_metrics else ["multimodal_bleu", "tps"]  # Default metrics

def load_device_config(config_path: str):
    """
    Load device-related configuration from the config file.

    Parameters:
        config_path (str): Path to the config YAML file.

    Returns:
        dict: Device configuration or default values.
    """
    config = load_config(config_path)
    return config.get("device", {"type": "npu:*:*", "model": "RNGD", "count": 1})  # Default values

def load_model_config(config_path: str):
    """
    Load model-related configuration from the config file.

    Parameters:
        config_path (str): Path to the config YAML file.

    Returns:
        dict: Model configuration or default values.
    """
    config = load_config(config_path)
    return config.get("model", {"name": "llama3.1-8B-Instruct", "quantization": "W8A8"})  # Default values

def load_evaluation_settings(config_path: str):
    """
    Load evaluation settings from the config file.

    Parameters:
        config_path (str): Path to the config YAML file.

    Returns:
        dict: Evaluation settings or default values.
    """
    config = load_config(config_path)
    evaluation = config.get("evaluation", {})
    return {
        "task": evaluation.get("task", "multimodal"),  # Default task
        "output_dir": evaluation.get("output_dir", "./results")  # Default output directory
    }

def load_all_configurations(config_path: str):
    """
    Load all configurations from the config file, with defaults for missing values.

    Parameters:
        config_path (str): Path to the config YAML file.

    Returns:
        dict: Dictionary containing all configuration sections.
    """
    return {
        "active_metrics": load_active_metrics(config_path),
        "device_config": load_device_config(config_path),
        "model_config": load_model_config(config_path),
        "evaluation_settings": load_evaluation_settings(config_path),
    }

if __name__ == "__main__":
    # Define the path to the configuration file
    config_path = "/home/elicer/Jun/llm-rag-chatbot/main/config_npu_translation.yaml"

    # Load all configurations
    all_configs = load_all_configurations(config_path)

    # Print the loaded configurations
    print("Configurations Loaded Successfully:")
    print("Active Metrics:", all_configs["active_metrics"])
    print("Device Config:", all_configs["device_config"])
    print("Model Config:", all_configs["model_config"])
    print("Evaluation Settings:", all_configs["evaluation_settings"])