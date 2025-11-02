import argparse
import os
from ascon.aead import Ascon128
from ascon.hash import ascon_hash
from ascon.mac import AsconMAC
from ascon.reference_adapters import (
    aes_gcm_encrypt,
    sha256_hash,
    hmac_sha256_mac
)
from bench.measure import measure_function, save_results_csv, plot_metric


def deterministic_input(size: int) -> bytes:
    return bytes((i % 256) for i in range(size))


def run_aead_bench(algorithm, key, nonce, sizes, runs, warmup, out_csv):
    rows = []
    for s in sizes:
        pt = deterministic_input(s)
        if algorithm == "ascon":
            a = Ascon128(key)
            fn = lambda: a.encrypt(nonce, pt, b"")
        elif algorithm == "aes-gcm":
            fn = lambda: aes_gcm_encrypt(key, nonce, pt, b"")
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        m = measure_function(fn, runs=runs, warmup=warmup)
        m["input_size"] = s
        m["algorithm"] = algorithm
        m["mode"] = "aead"
        rows.append(m)

    headers = ["algorithm", "mode", "input_size", "wall_time_mean", "cpu_time_mean", "mem_peak_mean"]
    save_results_csv(out_csv, rows, headers)
    plot_metric(rows, "wall_time_mean", out_csv + ".png")


def run_hash_bench(algorithm, sizes, runs, warmup, out_csv):
    rows = []
    for s in sizes:
        data = deterministic_input(s)
        if algorithm == "ascon":
            fn = lambda: ascon_hash(data)
        elif algorithm == "sha256":
            fn = lambda: sha256_hash(data)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        m = measure_function(fn, runs=runs, warmup=warmup)
        m["input_size"] = s
        m["algorithm"] = algorithm
        m["mode"] = "hash"
        rows.append(m)

    save_results_csv(out_csv, rows, ["algorithm", "mode", "input_size", "wall_time_mean", "cpu_time_mean", "mem_peak_mean"])
    plot_metric(rows, "wall_time_mean", out_csv + ".png")


def run_mac_bench(algorithm, key, sizes, runs, warmup, out_csv):
    rows = []
    for s in sizes:
        data = deterministic_input(s)
        if algorithm == "ascon":
            mac = AsconMAC(key)
            fn = lambda: mac.mac(data)
        elif algorithm == "hmac-sha256":
            fn = lambda: hmac_sha256_mac(key, data)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        m = measure_function(fn, runs=runs, warmup=warmup)
        m["input_size"] = s
        m["algorithm"] = algorithm
        m["mode"] = "mac"
        rows.append(m)

    save_results_csv(out_csv, rows, ["algorithm", "mode", "input_size", "wall_time_mean", "cpu_time_mean", "mem_peak_mean"])
    plot_metric(rows, "wall_time_mean", out_csv + ".png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["aead", "hash", "mac"], required=True)
    parser.add_argument("--algorithm", default="ascon")
    parser.add_argument("--runs", type=int, default=200)
    parser.add_argument("--warmup", type=int, default=10)
    parser.add_argument("--out", default="results/out.csv")
    parser.add_argument("--sizes", nargs="+", type=int, default=[16, 256, 4096, 65536])
    args = parser.parse_args()

    os.makedirs("results", exist_ok=True)
    key = b"\x00" * 16
    nonce = b"\x00" * 16

    if args.mode == "aead":
        run_aead_bench(args.algorithm, key, nonce, args.sizes, args.runs, args.warmup, args.out)
    elif args.mode == "hash":
        run_hash_bench(args.algorithm, args.sizes, args.runs, args.warmup, args.out)
    else:
        run_mac_bench(args.algorithm, key, args.sizes, args.runs, args.warmup, args.out)


if __name__ == "__main__":
    main()
