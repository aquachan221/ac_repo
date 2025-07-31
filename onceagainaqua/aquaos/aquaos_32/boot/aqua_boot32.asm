; aqua_boot32.asm — AquaOS Boot Sector (Self-contained)
[bits 16]
[org 0x7C00]

start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00

    mov si, msg
    call print_string

    ; Load GDT and switch to protected mode
    lgdt [gdt_descriptor]
    mov eax, cr0
    or eax, 1
    mov cr0, eax
    jmp 0x08:pmode_entry

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

msg db "🌀 AquaOS: Booting into protected mode", 0

; GDT setup
gdt_start:
    dq 0x0000000000000000
    dq 0x00CF9A000000FFFF
    dq 0x00CF92000000FFFF
gdt_end:
gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

times 510-($-$$) db 0
dw 0xAA55

; ------------------------------------------------------
; Entry point after protected mode transition
[bits 32]
pmode_entry:
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov esp, 0x9FC00

    mov si, pm_msg
    call print_string

    jmp kernel32_entry

pm_msg db "🧠 AquaOS: Welcome to 32-bit mode", 0

; ------------------------------------------------------
kernel32_entry:
    mov si, banner
    call print_string

    ; Hang forever
.halt:
    hlt
    jmp .halt

banner db "🌊 AquaOS Kernel Stub Reached", 0