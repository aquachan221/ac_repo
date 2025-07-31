; aqua_long_mode.asm — AquaOS Long Mode Setup
bits 32
org 0xB000

start:
    cli

    ; Enable PAE
    mov eax, cr4
    or eax, 1 << 5
    mov cr4, eax

    ; Load PML4
    mov eax, pml4_table
    mov cr3, eax

    ; Enable long mode via EFER MSR
    mov ecx, 0xC0000080
    rdmsr
    or eax, 1 << 8
    wrmsr

    ; Enable paging + protected mode
    mov eax, cr0
    or eax, 0x80000001
    mov cr0, eax

    ; Load 64-bit GDT
    lgdt [gdt64_descriptor]

    ; Far jump to 64-bit kernel
    jmp 0x08:kernel64_entry

; -------------------------------
; 64-bit GDT
align 8
gdt64_start:
    dq 0x0000000000000000
    dq 0x00AF9A000000FFFF
    dq 0x00AF92000000FFFF
gdt64_end:

gdt64_descriptor:
    dw gdt64_end - gdt64_start - 1
    dd gdt64_start

; -------------------------------
; Dummy PML4 (identity map for demo)
align 4096
pml4_table:
    dd pdpt_table + 0x03
    times 511 dd 0

align 4096
pdpt_table:
    dd pd_table + 0x03
    times 511 dd 0

align 4096
pd_table:
    dd 0x00000000 + 0x83
    times 511 dd 0

; -------------------------------
bits 64
kernel64_entry:
    mov rsi, msg64
    mov rdi, 0xB8000

.loop:
    lodsb
    test al, al
    jz .done
    mov ah, 0x0F
    mov [rdi], ax
    add rdi, 2
    jmp .loop

.done:
.halt:
    hlt
    jmp .halt

msg64 db "🚀 AquaOS: Long mode engaged!", 0