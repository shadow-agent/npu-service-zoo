import time
import psutil
import torch
import subprocess
import re

def calculate_tps(start_time: float, total_tokens: int) -> float:
    """
    Calculates TPS (Tokens Per Second) based on translation time and token count.

    Parameters:
        start_time (float): The start time of the translation (in seconds since epoch).
        total_tokens (int): Total number of tokens processed.

    Returns:
        float: TPS (tokens/second).

    Raises:
        ValueError: If total_tokens is negative or start_time is in the future.
    """
    if total_tokens < 0:
        raise ValueError("Total tokens cannot be negative.")
    
    elapsed_time = time.time() - start_time
    
    
    return total_tokens / elapsed_time if elapsed_time > 0 else 0



def calculate_memory_usage(device: str = "cuda") -> float:
    """
    Calculates memory usage for CUDA or NPU devices.

    Parameters:
        device (str): Device to check memory usage. Examples:
                      - "cuda" for GPU
                      - "npu:0:*" for NPU (Furiosa runtime format)

    Returns:
        float: Memory usage in MB.
    """
    if "cuda" in device:  # GPU (CUDA)
        if torch.cuda.is_available():
            return torch.cuda.memory_allocated() / (1024 * 1024)
        else:
            print("CUDA device not available.")
            return 0.0
    elif "npu" in device:  # NPU (Furiosa)
        import subprocess
        result = subprocess.run(
            ["furiosa-smi", "info", "--device", device],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        try:
            output = result.stdout.decode()
            # Parse Furiosa memory usage (example parsing logic)
            memory_line = [line for line in output.split("\n") if "Memory Usage" in line][0]
            memory_used = float(memory_line.split(":")[1].strip().split()[0])  # Assuming "Memory Usage: 512 MB"
            return memory_used
        except (IndexError, ValueError):
            print(f"Failed to parse memory usage for device {device}.")
            return 0.0
    else:
        print(f"Unsupported device type: {device}")
        return 0.0



def calculate_power_consumption(device: str) -> float:
    """
    Calculates power consumption for CUDA or NPU devices.

    Parameters:
        device (str): Device to check power usage. Examples:
                      - "cuda:0" for GPU
                      - "npu0" for NPU (Furiosa runtime format)

    Returns:
        float: Power consumption in watts.
    """
    if "cuda" in device:  # GPU (CUDA)
        try:
            # Extract GPU ID from the device string
            gpu_id = device.split(":")[1]

            # Run nvidia-smi command for power usage
            result = subprocess.run(
                ["nvidia-smi", "--id", gpu_id, "--query-gpu=power.draw", "--format=csv,noheader,nounits"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Parse the power consumption value
            power_str = result.stdout.strip()
            if power_str:
                return float(power_str)  # Convert string to float
            else:
                raise ValueError("Power consumption value not found.")
        except Exception as e:
            print(f"Error calculating power consumption for GPU {device}: {e}")
            return 0.0

    elif "npu" in device:  # NPU (Furiosa)
        try:
            # Run furiosa-smi info command
            result = subprocess.run(
                ["furiosa-smi", "info"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output = result.stdout

            # Remove ANSI escape codes from the output
            clean_output = re.sub(r'\x1b\[.*?m', '', output)

            # Use regex to find the target line containing the device
            lines = [line.strip() for line in clean_output.split("\n")]
            target_line = next((line for line in lines if re.search(rf"\| {device}\s+\|", line)), None)
            if not target_line:
                raise ValueError(f"Device {device} not found in furiosa-smi info output.")

            # Extract the Power value from the matched line
            columns = [col.strip() for col in target_line.split("|")]
            power_str = columns[5]  # Power is the 5th column
            if "W" in power_str:
                return float(power_str.split()[0])  # Extract numeric value (e.g., "42.00")
            else:
                raise ValueError(f"Power value not found in the expected column: {power_str}")
        except Exception as e:
            print(f"Error calculating power consumption for NPU {device}: {e}")
            return 0.0

    else:
        print(f"Unsupported device type: {device}")
        return 0.0