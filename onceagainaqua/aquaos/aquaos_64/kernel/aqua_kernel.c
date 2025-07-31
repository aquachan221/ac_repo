// aqua_kernel.c — AquaOS 64-bit Kernel Entry
#include <stdint.h>

void start(void) {
    const char* msg = "🧬 AquaOS Kernel: Hello from C!\n";
    volatile uint16_t* vga = (uint16_t*)0xB8000;
    uint16_t color = 0x0F00; // White on black

    for (uint64_t i = 0; msg[i] != '\0'; i++) {
        vga[i] = color | (uint8_t)msg[i];
    }

    while (1) {
        __asm__ __volatile__("hlt");
    }
}