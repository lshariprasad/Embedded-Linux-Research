#!/usr/bin/env bash
# Usage: ./scripts/run_uart.sh <baud> <label> [port] [iterations]
# Example: ./scripts/run_uart.sh 115200 stm32_echo
set -e
BAUD=${1:?usage: run_uart.sh <baud> <label> [port] [iterations]}
LABEL=${2:?usage: run_uart.sh <baud> <label> [port] [iterations]}
PORT=${3:-/dev/serial0}
ITER=${4:-1000}
cd "$(dirname "$0")/.."
mkdir -p results/raw
STAMP=$(date +%Y%m%d_%H%M%S)
bash scripts/env_snapshot.sh > "results/raw/env_${LABEL}_${BAUD}_${STAMP}.txt"
python3 host/uart_rtt.py --port "$PORT" --baud "$BAUD" --label "$LABEL" --iterations "$ITER"
python3 host/summarize.py