#!/usr/bin/env python3
"""UART round-trip latency benchmark.

Sends a payload, waits for the same number of bytes to come back (STM32 echo, or a
TX-RX loopback wire for Phase 0) and records the round-trip time per iteration.
"""
import argparse
import csv
import os
import statistics
import time
from datetime import datetime

import serial


def run_size(ser, size, iterations):
    payload = bytes((i * 7 + 3) % 256 for i in range(size))
    rows = []
    for i in range(iterations):
        ser.reset_input_buffer()
        t0 = time.perf_counter_ns()
        ser.write(payload)
        ser.flush()
        data = ser.read(size)
        t1 = time.perf_counter_ns()
        rows.append((i, size, (t1 - t0) / 1000.0, int(data == payload)))
    return rows


def percentile(sorted_vals, p):
    if not sorted_vals:
        return float("nan")
    k = min(len(sorted_vals) - 1, int(round(p / 100.0 * (len(sorted_vals) - 1))))
    return sorted_vals[k]


def main():
    ap = argparse.ArgumentParser(description="UART round-trip latency benchmark")
    ap.add_argument("--port", default="/dev/serial0")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--sizes", type=int, nargs="+", default=[1, 8, 64, 256])
    ap.add_argument("--iterations", type=int, default=1000)
    ap.add_argument("--timeout", type=float, default=1.0, help="read timeout in seconds")
    ap.add_argument("--label", default="loopback", help="loopback, stm32_echo, cpu_load, ...")
    ap.add_argument("--outdir", default="results/raw")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = os.path.join(args.outdir, f"uart_{args.label}_{args.baud}_{stamp}.csv")

    ser = serial.Serial(args.port, args.baud, timeout=args.timeout)
    time.sleep(0.2)

    all_rows = []
    print(f"port={args.port} baud={args.baud} label={args.label} iterations={args.iterations}")
    print(f"{'size':>6} {'median_us':>11} {'p99_us':>11} {'max_us':>11} {'errors':>7}")
    for size in args.sizes:
        rows = run_size(ser, size, args.iterations)
        all_rows.extend(rows)
        good = sorted(r[2] for r in rows if r[3] == 1)
        errors = sum(1 for r in rows if r[3] == 0)
        med = statistics.median(good) if good else float("nan")
        mx = good[-1] if good else float("nan")
        print(f"{size:>6} {med:>11.1f} {percentile(good, 99):>11.1f} {mx:>11.1f} {errors:>7}")
    ser.close()

    with open(outfile, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["iteration", "payload_bytes", "rtt_us", "ok"])
        w.writerows(all_rows)
    print(f"saved: {outfile}")


if __name__ == "__main__":
    main()