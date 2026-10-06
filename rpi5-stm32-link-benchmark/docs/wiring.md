# Wiring

| Raspberry Pi 5 | STM32 Nucleo-F446RE |
|---|---|
| GPIO14 TXD (pin 8) | D2 = PA10 (USART1 RX) |
| GPIO15 RXD (pin 10) | D8 = PA9 (USART1 TX) |
| GND (pin 6) | GND |

Loopback (Phase 0): GPIO14 to GPIO15 only.
Both sides are 3.3 V logic. Never connect 5 V to these pins.