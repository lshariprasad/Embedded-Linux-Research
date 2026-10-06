/*
 * UART echo for the Raspberry Pi 5 <-> STM32F446RE link benchmark.
 * USART1: PA9 = TX (Nucleo D8), PA10 = RX (Nucleo D2), alternate function 7.
 * Runs from the default 16 MHz HSI clock (no PLL), so BRR values below are for 16 MHz,
 * oversampling by 16:  baud = 16 MHz / (16 * USARTDIV).
 */
#include "stm32f4xx.h"
#include <stdint.h>

#ifndef BAUD_RATE
#define BAUD_RATE 115200
#endif

#if BAUD_RATE == 115200
#define BRR_VALUE 0x8B   /* USARTDIV 8.6875 -> 115107 baud (-0.08%) */
#elif BAUD_RATE == 460800
#define BRR_VALUE 0x23   /* USARTDIV 2.1875 -> 457143 baud (-0.79%) */
#elif BAUD_RATE == 1000000
#define BRR_VALUE 0x10   /* USARTDIV 1.0    -> 1000000 baud (exact) */
#else
#error "Unsupported BAUD_RATE (use 115200, 460800 or 1000000)"
#endif

int main(void)
{
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    RCC->APB2ENR |= RCC_APB2ENR_USART1EN;

    /* PA9, PA10: alternate function mode, very high speed, PA10 pull-up */
    GPIOA->MODER   &= ~((3U << (9 * 2)) | (3U << (10 * 2)));
    GPIOA->MODER   |=  ((2U << (9 * 2)) | (2U << (10 * 2)));
    GPIOA->OSPEEDR |=  ((3U << (9 * 2)) | (3U << (10 * 2)));
    GPIOA->PUPDR   &= ~(3U << (10 * 2));
    GPIOA->PUPDR   |=  (1U << (10 * 2));
    GPIOA->AFR[1]  &= ~((0xFU << ((9 - 8) * 4)) | (0xFU << ((10 - 8) * 4)));
    GPIOA->AFR[1]  |=  ((7U << ((9 - 8) * 4)) | (7U << ((10 - 8) * 4)));

    USART1->BRR = BRR_VALUE;
    USART1->CR1 = USART_CR1_TE | USART_CR1_RE | USART_CR1_UE;

    for (;;) {
        uint32_t sr = USART1->SR;
        if (sr & USART_SR_ORE) {          /* overrun: clear by reading SR then DR */
            (void)USART1->DR;
            continue;
        }
        if (sr & USART_SR_RXNE) {
            uint8_t b = (uint8_t)USART1->DR;
            while (!(USART1->SR & USART_SR_TXE)) { }
            USART1->DR = b;
        }
    }
}