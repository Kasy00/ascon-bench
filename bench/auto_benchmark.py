import os
import sys
import subprocess
from datetime import datetime

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def run_benchmark(description, args):
    print(f"\n🚀 Running: {description}")
    env = os.environ.copy()
    env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")
    cmd = ["python", "bench/bench_cli.py"] + args
    subprocess.run(cmd, check=True, env=env)

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("results", exist_ok=True)

    benchmarks = [
        # AEAD benchmarks
        ("ASCON-128 vs AES-GCM", ["--mode", "aead", "--algorithm", "aes-gcm", "--runs", "100", "--warmup", "10", "--out", f"results/aead_{timestamp}.csv"]),
        ("ASCON-128 (self test)", ["--mode", "aead", "--runs", "100", "--warmup", "10", "--out", f"results/ascon_aead_{timestamp}.csv"]),

        # Hash benchmarks
        ("ASCON-Hash vs SHA-256", ["--mode", "hash", "--algorithm", "sha256", "--runs", "200", "--warmup", "10", "--out", f"results/hash_{timestamp}.csv"]),
        ("ASCON-Hash (self test)", ["--mode", "hash", "--runs", "200", "--warmup", "10", "--out", f"results/ascon_hash_{timestamp}.csv"]),

        # MAC benchmarks
        ("ASCON-MAC vs HMAC-SHA-256", ["--mode", "mac", "--algorithm", "hmac-sha256", "--runs", "100", "--warmup", "10", "--out", f"results/mac_{timestamp}.csv"]),
        ("ASCON-MAC (self test)", ["--mode", "mac", "--runs", "100", "--warmup", "10", "--out", f"results/ascon_mac_{timestamp}.csv"]),
    ]

    for desc, args in benchmarks:
        try:
            run_benchmark(desc, args)
        except subprocess.CalledProcessError:
            print(f"❌ Failed: {desc}")

    print("\n✅ All benchmarks completed successfully!")
    print("📊 Results saved in ./results/*.csv")

if __name__ == "__main__":
    main()
