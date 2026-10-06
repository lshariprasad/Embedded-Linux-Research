#!/usr/bin/env python3
"""Summarize every results/raw/uart_*.csv into results/processed/summary.csv.

throughput_kbit_s = bits moved both ways / median round-trip time
                  = (payload_bytes * 2 * 8) / median_rtt_us * 1000
"""
import csv
import glob
import os
import statistics
from collections import defaultdict

RAW = "results/raw"
OUT = "results/processed/summary.csv"


def percentile(sorted_vals, p):
    k = min(len(sorted_vals) - 1, int(round(p / 100.0 * (len(sorted_vals) - 1))))
    return sorted_vals[k]


def main():
    files = sorted(glob.glob(os.path.join(RAW, "uart_*.csv")))
    if not files:
        print("no raw files found")
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    out_rows = []
    for path in files:
        groups = defaultdict(list)
        errors = defaultdict(int)
        with open(path, newline="") as f:
            for r in csv.DictReader(f):
                size = int(r["payload_bytes"])
                if r["ok"] == "1":
                    groups[size].append(float(r["rtt_us"]))
                else:
                    errors[size] += 1
        sizes = sorted(set(groups) | set(errors))
        for size in sizes:
            vals = sorted(groups.get(size, []))
            n = len(vals) + errors.get(size, 0)
            if vals:
                med = statistics.median(vals)
                thr = (size * 2 * 8) / med * 1000.0
                row = [os.path.basename(path), size, n, errors.get(size, 0),
                       round(med, 1), round(percentile(vals, 99), 1), round(vals[-1], 1), round(thr, 1)]
            else:
                row = [os.path.basename(path), size, n, errors.get(size, 0), "", "", "", ""]
            out_rows.append(row)

    header = ["file", "payload_bytes", "iterations", "errors", "median_us", "p99_us", "max_us", "throughput_kbit_s"]
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(out_rows)
    print(f"summary saved: {OUT} ({len(out_rows)} rows)")


if __name__ == "__main__":
    main()