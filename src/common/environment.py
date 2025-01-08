import subprocess
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def detect_all_gpus() -> list:
    """
    Detects all available GPU devices on the node.

    Returns:
        list: List of GPU IDs (e.g., ["cuda:0", "cuda:1", ...]).
    """
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=index", "--format=csv,noheader"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        gpu_ids = result.stdout.strip().split("\n")
        return [f"cuda:{gpu_id.strip()}" for gpu_id in gpu_ids if gpu_id.strip()]
    except Exception as e:
        logging.error(f"Failed to detect GPUs: {e}")
        return []


def detect_all_npus() -> list:
    """
    Detects all available NPU devices on the node.

    Returns:
        list: List of NPU IDs (e.g., ["npu0", "npu1", ...]).
    """
    try:
        result = subprocess.run(
            ["furiosa-smi", "info"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stdout

        # Remove ANSI escape codes from the output
        clean_output = re.sub(r'\x1b\[.*?m', '', output)

        # Extract all NPU device IDs (e.g., npu0, npu1)
        npu_ids = []
        for line in clean_output.split("\n"):
            match = re.search(r"npu\d+", line)
            if match:
                npu_ids.append(match.group())
        return npu_ids
    except Exception as e:
        logging.error(f"Failed to detect NPUs: {e}")
        return []


def detect_environment() -> dict:
    """
    Checks the current system environment to determine if it's GPU-based or Furiosa RNGD.

    Returns:
        dict: A dictionary with detected environment and available device lists.
              Example: {"environment": "gpu", "devices": ["cuda:0", "cuda:1"]}
    """
    gpus = detect_all_gpus()
    npus = detect_all_npus()

    if gpus:
        return {"environment": "gpu", "devices": gpus}
    elif npus:
        return {"environment": "furiosa", "devices": npus}
    else:
        return {"environment": "unknown", "devices": []}


if __name__ == "__main__":
    env_info = detect_environment()
    logging.info(f"Detected Environment: {env_info['environment']}")
    logging.info(f"Detected Devices: {env_info['devices']}")