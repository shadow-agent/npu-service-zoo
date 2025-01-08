# common/monitoring.py
import os
import threading
from time import time, sleep
from functools import wraps
from metrics.performance_metrics import calculate_power_consumption

def monitor_power(func):
    """
    Decorator to monitor power consumption during the execution of a function.

    Args:
        func (function): The function to wrap.

    Returns:
        function: The wrapped function with monitoring.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        _monitoring_enabled = os.getenv("ENABLE_MONITORING", "false").lower() == "true"
        if not _monitoring_enabled:
            return func(*args, **kwargs)

        # Detect devices for monitoring
        devices = kwargs.get("_devices", [])
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
            # Execute the original function
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