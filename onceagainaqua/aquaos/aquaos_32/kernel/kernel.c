// kernel.c — AquaOS C Kernel Entry
void print(const char* str) {
    while (*str) {
        asm volatile (
            "movb $0x0E, %%ah\n"
            "int $0x10"
            : : "a"(*str++)
        );
    }
}

void kernel_main() {
    print("ok\n");
    while (1) asm volatile ("hlt");
}