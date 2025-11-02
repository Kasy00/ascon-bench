import time
import csv
import os
import tracemalloc
from typing import Callable, Dict, Any, Tuple
import statistics
import matplotlib.pyplot as plt

def get_memory_usage_mb():
    current, peak = tracemalloc.get_traced_memory()
    return peak / (1024 * 1024)

 # pomiary czasu/CPU/pamięci, CSV export, plot

def measure_function(fn: Callable, args: tuple=(), kwargs: dict=None, runs: int=100, warmup: int=10) -> Dict[str, Any]:
    if kwargs is None: kwargs = {}
    # warmup
    for _ in range(warmup):
        fn(*args, **kwargs)
    times = []
    cpu_times = []
    mem_peaks = []
    for _ in range(runs):
        tracemalloc.start()
        start_wall = time.perf_counter()
        start_proc = time.process_time()
        fn(*args, **kwargs)
        end_proc = time.process_time()
        end_wall = time.perf_counter()
        current,peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        times.append(end_wall - start_wall)
        cpu_times.append(end_proc - start_proc)
        mem_peaks.append(peak)
    result = {
        "runs": runs,
        "wall_time_mean": statistics.mean(times),
        "wall_time_std": statistics.pstdev(times),
        "cpu_time_mean": statistics.mean(cpu_times),
        "mem_peak_mean": statistics.mean(mem_peaks),
        "throughput_MBps": None
    }
    return result

def save_results_csv(path: str, rows: list, headers: list):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for r in rows:
            writer.writerow([r.get(h,"") for h in headers])

def plot_metric(csv_rows: list, metric: str, out_png: str):
    x = [r['input_size'] for r in csv_rows]
    y = [r[metric] for r in csv_rows]
    plt.figure()
    plt.plot(x,y)
    plt.xlabel('input_size')
    plt.ylabel(metric)
    plt.title(metric + ' vs input size')
    plt.savefig(out_png)
    plt.close()
