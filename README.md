# Embedded-Linux-Research

Embedded Linux, BSP and driver development research by **Hari Prasad L S**. Every topic is a reproducible experiment with its own folder, scripts, raw data and paper draft, so the work can be checked and repeated.

## Why this repo exists

Embedded Linux products run into the same practical problems again and again: unpredictable latency, slow boot, vendor kernels that are hard to update, driver bugs and unsafe updates. Each topic below takes one of these problems, defines a measurable question and answers it with data from real hardware.

## Research tracker

| S.No | Title | Date I'm going to work | Status |
|---|---|---|---|
| 1 | Real-time latency: PREEMPT_RT vs standard kernel | TBD | Updating |
| 2 | Linux + Cortex-M co-processing: Raspberry Pi 5 and STM32 link benchmark | TBD | Updating |
| 3 | Boot time optimization | TBD | Planned |
| 4 | Vendor BSP fragmentation: vendor kernel to mainline | TBD | Planned |
| 5 | Driver bugs and safety: fuzzing and static analysis | TBD | Planned |
| 6 | OTA updates and supply-chain security | TBD | Planned |
| 7 | Rust for Linux drivers | TBD | Planned |

**Status legend:** Planned = not started · Updating = work in progress · Completed = results published in the folder

## Topics explained

### 1. Real-time latency: PREEMPT_RT vs standard kernel
- **Problem:** Standard Linux is not deterministic. The time between an event and the task that handles it can spike, and PREEMPT_RT behavior varies by board and workload.
- **Study:** Measure worst-case scheduling latency with `cyclictest` on BeagleBone and Raspberry Pi, with and without PREEMPT_RT, under CPU, I/O and network load.
- **Outcome measured:** Maximum and average latency in microseconds.
- **Folder:** `linux-rt-latency-study`

### 2. Linux + Cortex-M co-processing: Raspberry Pi 5 and STM32 link benchmark
- **Problem:** Many products pair a Linux board with a microcontroller, but the communication latency and design choices are poorly documented.
- **Study:** Compare UART, SPI and I2C links between a Raspberry Pi 5 and an STM32F446RE (Nucleo-64). RPMsg/OpenAMP applies only between cores on the same chip, so it is out of scope unless an STM32MP1-class board is added later.
- **Outcome measured:** Round-trip latency, throughput and error rate.
- **Folder:** `rpi5-stm32-link-benchmark`

### 3. Boot time optimization
- **Problem:** Slow boots are a real product problem in automotive and industrial devices.
- **Study:** Optimize boot time step by step (U-Boot, kernel configuration, init system) and report the gain from each change.
- **Outcome measured:** Time from power-on to a usable system, per optimization step.
- **Folder:** `boot-time-optimization`

### 4. Vendor BSP fragmentation: vendor kernel to mainline
- **Problem:** Vendor kernels are often old forks that are hard to update or upstream.
- **Study:** Document the effort of moving a board from a vendor kernel to mainline Linux, including device tree and driver differences.
- **Outcome measured:** What worked, what broke, what was missing, and the effort involved.
- **Folder:** `bsp-mainline-porting`

### 5. Driver bugs and safety: fuzzing and static analysis
- **Problem:** Drivers account for a large share of kernel bugs, and testing them without the hardware is hard.
- **Study:** Fuzz or statically analyze a small driver. This is an advanced topic.
- **Outcome measured:** Bugs found, methods used and false-positive rate.
- **Folder:** `driver-fuzzing-static-analysis`

### 6. OTA updates and supply-chain security
- **Problem:** Updates must not brick devices, and regulations such as the EU Cyber Resilience Act are pushing SBOM requirements. The current status should be verified before writing.
- **Study:** Compare OTA frameworks (RAUC, Mender, SWUpdate) on reliability and rollback behavior.
- **Outcome measured:** Update success rate, rollback behavior after a failed update, and setup effort.
- **Folder:** `ota-update-comparison`

### 7. Rust for Linux drivers
- **Problem:** Rust support in the kernel is an emerging area and its status changes quickly.
- **Study:** Compare a simple C driver and a Rust driver. Attempt this later, and verify the current state of Rust in the kernel first.
- **Outcome measured:** Code size, safety issues caught at compile time, and effort.
- **Folder:** `rust-for-linux-drivers`

## Folder layout of each topic

- `docs/` : PICO table, experiment plan, lab notebook
- `firmware/` : microcontroller code
- `host/` : Linux-side scripts
- `scripts/` : environment snapshot and helpers
- `results/raw/` : raw CSV data, never edited by hand
- `results/processed/` : tables and plots
- `paper/` : draft

## Rules for every experiment

1. State the question in PICO form (Population, Intervention, Comparison, Outcome) before running anything.
2. Record the kernel version, OS image, hardware model and wiring with every run.
3. Keep raw data; never delete or hand-edit it.
4. Report failures and outliers as well as good results.
5. Publish the scripts so anyone can repeat the experiment.

## How to update this table

1. Fill in the date when you start a topic.
2. Change the status from Planned to Updating when work starts, and to Completed when the results and paper draft are in the folder.
3. Commit the change with a message such as `Update tracker: topic 2 completed`.

## Author

Hari Prasad L S, B.E. EEE, SIMATS Saveetha School of Engineering, Chennai
GitHub: github.com/lshariprasad
