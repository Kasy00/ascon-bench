# uruchamianie eksperymentów, warm-up, powtórzenia

import csv
import time
import tracemalloc
import psutil
import statistics
from typing import Callable, Dict, Any

def measure(func: Callable, *args, runs: int = 100, warmup: int = 10, **kwargs) -> Dict[str, Any]:
    """
    Execute function multiple times and gather timing and memory metrics.
    Returns dict with average metrics.
    """
    # Warm-up phase
    for _ in range(warmup):
        func(*args, **kwargs)

    times = []
    cpu_times = []
    mem_peaks = []

    process = psutil.Process()
    for _ in range(runs):
        tracemalloc.start()
        start_wall = time.perf_counter()
        start_cpu = process.cpu_times()
        func(*args, **kwargs)
        end_cpu = process.cpu_times()
        end_wall = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        times.append(end_wall - start_wall)
        cpu_times.append((end_cpu.user - start_cpu.user) + (end_cpu.system - start_cpu.system))
        mem_peaks.append(peak / 1024)  # kB

    return {
        "elapsed_time_avg": statistics.mean(times),
        "cpu_time_avg": statistics.mean(cpu_times),
        "memory_peak_avg_kb": statistics.mean(mem_peaks),
        "runs": runs,
        "warmup": warmup
    }


def export_csv(filename: str, results: Dict[str, Any]):
    """Write benchmark results to CSV file."""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        for key, value in results.items():
            writer.writerow([key, value])
