# rpi5-stm32-link-benchmark

Latency and throughput of UART (SPI and I2C to follow) between a **Raspberry Pi 5 (Linux)** and an **STM32F446RE (Nucleo-64)**.

Part of [Embedded-Linux-Research](https://github.com/lshariprasad/Embedded-Linux-Research).

## Research question (PICO)

| Element | This study |
|---|---|
| **P** (Population) | Raspberry Pi 5 running Linux (OS image and kernel recorded per run) connected to an STM32F446RE Nucleo-64 |
| **I** (Intervention) | Each interface: UART, SPI, I2C |
| **C** (Comparison) | Interfaces against each other; baud rates; payload sizes; idle vs CPU-loaded Linux |
| **O** (Outcome) | Round-trip latency (µs), throughput (kbit/s), error or timeout rate |

**Hypothesis:** to be written before the main runs.

## Status

- [ ] Phase 0: UART loopback on the Pi alone (no STM32)
- [ ] Phase 1: UART with STM32 echo firmware
- [ ] Phase 2: UART under CPU load
- [ ] Phase 3: SPI
- [ ] Phase 4: I2C
- [ ] Phase 5: Analysis and paper draft

## What you need

- Raspberry Pi 5 with Raspberry Pi OS (keyboard and screen, or SSH)
- STM32 NUCLEO-F446RE and a USB-A to Mini-B cable
- 3 female-to-female jumper wires
- A computer to flash the STM32 with PlatformIO (`pip install platformio`)

## Step 0: Set up the Pi (one time)

Enable the hardware serial port:

```bash
sudo raspi-config
# Interface Options -> Serial Port
# "Login shell over serial?"  -> No
# "Serial port hardware?"     -> Yes
sudo reboot
```

Check the serial device (confirm the exact name on your Pi 5):

```bash
ls -l /dev/serial0 /dev/ttyAMA*
```

Get the code and set up Python:

```bash
sudo apt install -y git stress-ng
sudo usermod -aG dialout $USER      # log out and back in after this
git clone https://github.com/lshariprasad/Embedded-Linux-Research.git
cd Embedded-Linux-Research/rpi5-stm32-link-benchmark
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Phase 0: UART loopback (Pi only)

This gives the Linux-side baseline, with no STM32 involved.

1. Power off the Pi. Connect one jumper wire from **GPIO14 (TXD, pin 8)** to **GPIO15 (RXD, pin 10)**.
2. Power on, activate the venv, and run:

```bash
./scripts/run_uart.sh 115200 loopback
```

3. A table of median, p99 and max round-trip time is printed. Raw data goes to `results/raw/` and the summary to `results/processed/summary.csv`.
4. Commit the results:

```bash
git add -A && git commit -m "Phase 0 loopback results" && git push
```

## Phase 1: UART with the STM32

### Wiring

Both boards use 3.3 V logic. Connect GND first, and never connect 5 V to these pins.

| Raspberry Pi 5 | STM32 Nucleo-F446RE |
|---|---|
| GPIO14 TXD (pin 8) | D2 (PA10, USART1 RX) |
| GPIO15 RXD (pin 10) | D8 (PA9, USART1 TX) |
| GND (pin 6) | GND |

Remove the loopback wire before wiring the STM32.

### Flash the echo firmware

On the computer the Nucleo is plugged into:

```bash
cd firmware/stm32
pio run -e baud115200 -t upload
```

### Run the benchmark (on the Pi)

```bash
./scripts/run_uart.sh 115200 stm32_echo
```

Repeat for the other baud rates. The firmware and the script baud must match:

```bash
pio run -e baud460800 -t upload      # then on the Pi: ./scripts/run_uart.sh 460800 stm32_echo
pio run -e baud1000000 -t upload     # then on the Pi: ./scripts/run_uart.sh 1000000 stm32_echo
```

## Phase 2: Under CPU load

Start the load in one terminal and the benchmark in another:

```bash
stress-ng --cpu 4 --timeout 600s
./scripts/run_uart.sh 115200 cpu_load
```

## Results

Fill this table from `results/processed/summary.csv` as runs complete.

| Interface | Baud / clock | Payload (bytes) | Load | Median RTT (µs) | p99 RTT (µs) | Max RTT (µs) | Throughput (kbit/s) | Errors |
|---|---|---|---|---|---|---|---|---|
| UART loopback | 115200 | 1 | idle | | | | | |
| UART + STM32 | 115200 | 1 | idle | | | | | |

## Rules for every run

1. `run_uart.sh` saves the environment snapshot (kernel, OS, CPU governor, temperature) with each run. Keep it with the data.
2. Use at least 1000 iterations per setting.
3. Never edit raw CSV files by hand.
4. Log what you did in `docs/lab-notebook.md`.
5. Report timeouts and errors; do not hide them.

## Folder layout

```
rpi5-stm32-link-benchmark/
├── README.md
├── requirements.txt
├── docs/                 experiment plan, wiring, lab notebook
├── firmware/stm32/       PlatformIO project (UART echo)
├── host/                 uart_rtt.py (benchmark), summarize.py (statistics)
├── scripts/              run_uart.sh, env_snapshot.sh
├── results/raw/          raw CSV data and environment snapshots
├── results/processed/    summary tables
└── paper/                draft
```

## Troubleshooting

| Problem | Likely cause and fix |
|---|---|
| Permission denied on the serial port | You are not in the `dialout` group. Run the `usermod` command and log in again. |
| All iterations time out in loopback | GPIO14 and GPIO15 are not joined, or the serial port is not enabled. |
| All iterations time out with the STM32 | Check TX/RX are crossed (Pi TX to STM32 RX), GND is common, and the firmware baud matches the script baud. |
| Errors only at high baud | Lower the baud rate. Wire length and baud-rate error both matter. |
| `/dev/serial0` not found | Re-run `raspi-config`, reboot, and check `ls /dev/ttyAMA*`. |

## Author

Hari Prasad L S, B.E. EEE, SIMATS Saveetha School of Engineering, Chennai
