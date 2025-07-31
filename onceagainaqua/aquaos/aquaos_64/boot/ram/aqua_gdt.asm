; aqua_gdt.asm — AquaOS GDT Setup
bits 16
org 0x8000

start:
    cli
    lgdt [gdt_descriptor]     ; Load GDT

    jmp 0x0000:0x9000

gdt_start:
    dq 0x0000000000000000      ; Null descriptor
    dq 0x00CF9A000000FFFF      ; Code segment
    dq 0x00CF92000000FFFF      ; Data segment
gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start