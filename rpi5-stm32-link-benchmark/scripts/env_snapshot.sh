#!/usr/bin/env bash
# Prints the test environment. run_uart.sh saves it next to each run.
echo "date: $(date -Is)"
echo "kernel: $(uname -a)"
echo "os: $(grep PRETTY_NAME /etc/os-release | cut -d= -f2)"
echo "model: $(tr -d '\0' < /proc/device-tree/model 2>/dev/null)"
echo "cpu governor: $(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null)"
echo "cpu freq (kHz): $(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq 2>/dev/null)"
echo "temperature: $(vcgencmd measure_temp 2>/dev/null)"
echo "serial devices:"; ls -l /dev/serial* /dev/ttyAMA* 2>/dev/null