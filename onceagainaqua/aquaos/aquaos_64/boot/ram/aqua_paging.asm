; aqua_paging.asm — AquaOS 64-bit Paging Setup
bits 32
org 0xA000

start:
    cli

    ; Enable PAE
    mov eax, cr4
    or eax, 1 << 5         ; PAE bit
    mov cr4, eax

    ; Load PML4 base into CR3
    mov eax, pml4_table
    mov cr3, eax

    ; Enable long mode via EFER MSR
    mov ecx, 0xC0000080    ; IA32_EFER
    rdmsr
    or eax, 1 << 8         ; LME bit
    wrmsr

    ; Enable paging + protected mode
    mov eax, cr0
    or eax, 0x80000001     ; PG + PE
    mov cr0, eax

    mov si, paging_msg
    call print_string

    jmp 0x0000:0xB000      ; Jump to long mode setup

; -------------------------------
; Recursive Paging Tables
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
    ; Map 0x00000000 → 0x00200000 (2MB page)
    dd 0x00000000 + 0x83
    ; Map 0x100000 → 0x10200000 (kernel physical)
    dd 0x00100000 + 0x83
    times 510 dd 0

; -------------------------------
; Text Output
print_char:
    mov ah, 0x0E
    int 0x10
    ret

print_string:
.next:
    lodsb
    or al, al
    jz .done
    call print_char
    jmp .next
.done:
    ret

paging_msg db "paging", 0