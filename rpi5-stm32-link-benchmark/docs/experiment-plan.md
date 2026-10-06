# Experiment plan

## Fixed rules
- One variable changes at a time.
- Record kernel, OS image, CPU governor, temperature and wiring for every run.
- At least 1000 iterations per setting; longer runs for worst-case latency.
- Count timeouts as errors; never drop them silently.
- Keep raw CSV files untouched.

## Variables
- Interface: UART (Phases 0-2), SPI (Phase 3), I2C (Phase 4)
- UART baud: 115200, 460800, 1000000. The STM32 runs from its 16 MHz internal oscillator, which gives small baud error at these three speeds. Higher speeds would need the PLL clock and a firmware change.
- Payload size: 1, 8, 64, 256 bytes
- Load: idle vs stress-ng CPU load on the Pi

## Phases
0. UART loopback on the Pi alone (baseline of Linux-side overhead).
1. STM32 echo, real round trip.
2. Same under CPU load.
3. SPI (Pi master, STM32 slave).
4. I2C (Pi master, STM32 slave).
5. Analysis: median, p99, max, error rate, throughput; plots; paper draft.

## Hypothesis (write before the main runs)
TBD