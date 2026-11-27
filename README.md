# Embedded-Linux-Research

An evolving research roadmap for Embedded Linux, board-support packages (BSPs) and driver development by **Hari Prasad L S**. The repository currently contains an in-progress Raspberry Pi 5–STM32 communication benchmark. The other topics are planned; no measurements or completed research results are claimed for them.

## Why this repo exists

Embedded Linux products face practical challenges such as scheduling latency, slow boot, vendor-kernel maintenance, driver defects and safe updates. The topics below identify questions that could be investigated. A topic should only be described as completed after its methods, environment and measured results have been committed.

## Research tracker

| S.No | Title | Date I'm going to work | Status |
|---|---|---|---|
| 1 | Real-time latency: PREEMPT_RT vs standard kernel | TBD | Planned |
| 2 | Linux + Cortex-M co-processing: Raspberry Pi 5 and STM32 link benchmark | TBD | In progress (no benchmark results committed yet) |
| 3 | Boot time optimization | TBD | Planned |
| 4 | Vendor BSP fragmentation: vendor kernel to mainline | TBD | Planned |
| 5 | Driver bugs and safety: fuzzing and static analysis | TBD | Planned |
| 6 | OTA updates and supply-chain security | TBD | Planned |
| 7 | Rust for Linux drivers | TBD | Planned |

**Status legend:** Planned = not started · In progress = project files or experiment planning are being developed · Completed = methods and measured results are documented in the repository

## Topics explained

### 1. Real-time latency: PREEMPT_RT vs standard kernel
- **Problem:** Standard Linux is not deterministic. The time between an event and the task that handles it can spike, and PREEMPT_RT behavior varies by board and workload.
- **Study:** Measure worst-case scheduling latency with `cyclictest` on BeagleBone and Raspberry Pi, with and without PREEMPT_RT, under CPU, I/O and network load.
- **Outcome measured:** Maximum and average latency in microseconds.
- **Status:** Planned; the experiment folder and measurement data have not yet been committed.

### 2. Linux + Cortex-M co-processing: Raspberry Pi 5 and STM32 link benchmark
- **Problem:** Many products pair a Linux board with a microcontroller, but the communication latency and design choices are poorly documented.
- **Study:** Compare UART, SPI and I2C links between a Raspberry Pi 5 and an STM32F446RE (Nucleo-64). RPMsg/OpenAMP applies only between cores on the same chip, so it is out of scope unless an STM32MP1-class board is added later.
- **Outcome measured:** Round-trip latency, throughput and error rate.
- **Folder:** `rpi5-stm32-link-benchmark` (the current in-progress project; results folders are placeholders until measurements are added).

### 3. Boot time optimization
- **Problem:** Slow boots are a real product problem in automotive and industrial devices.
- **Study:** Optimize boot time step by step (U-Boot, kernel configuration, init system) and report the gain from each change.
- **Outcome measured:** Time from power-on to a usable system, per optimization step.
- **Status:** Planned; the experiment folder has not yet been committed.

### 4. Vendor BSP fragmentation: vendor kernel to mainline
- **Problem:** Vendor kernels are often old forks that are hard to update or upstream.
- **Study:** Document the effort of moving a board from a vendor kernel to mainline Linux, including device tree and driver differences.
- **Outcome measured:** What worked, what broke, what was missing, and the effort involved.
- **Status:** Planned; the experiment folder has not yet been committed.

### 5. Driver bugs and safety: fuzzing and static analysis
- **Problem:** Drivers account for a large share of kernel bugs, and testing them without the hardware is hard.
- **Study:** Fuzz or statically analyze a small driver. This is an advanced topic.
- **Outcome measured:** Bugs found, methods used and false-positive rate.
- **Status:** Planned; the experiment folder has not yet been committed.

### 6. OTA updates and supply-chain security
- **Problem:** Updates must not brick devices, and regulations such as the EU Cyber Resilience Act are pushing SBOM requirements. The current status should be verified before writing.
- **Study:** Compare OTA frameworks (RAUC, Mender, SWUpdate) on reliability and rollback behavior.
- **Outcome measured:** Update success rate, rollback behavior after a failed update, and setup effort.
- **Status:** Planned; the experiment folder has not yet been committed.

### 7. Rust for Linux drivers
- **Problem:** Rust support in the kernel is an emerging area and its status changes quickly.
- **Study:** Compare a simple C driver and a Rust driver. Attempt this later, and verify the current state of Rust in the kernel first.
- **Outcome measured:** Code size, safety issues caught at compile time, and effort.
- **Status:** Planned; the experiment folder has not yet been committed.

## Current project layout: Raspberry Pi 5–STM32 link benchmark

The committed `rpi5-stm32-link-benchmark/` folder currently contains:

- `docs/` – experiment plan, lab notebook and wiring notes
- `firmware/stm32/` – PlatformIO project and STM32 firmware source
- `host/` – UART and result-summary scripts
- `scripts/` – environment snapshot and run helpers
- `results/raw/` and `results/processed/` – placeholders; no benchmark dataset is currently committed
- `paper/` – placeholder for a future report

Other research topics will receive their own folders when work begins.

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
