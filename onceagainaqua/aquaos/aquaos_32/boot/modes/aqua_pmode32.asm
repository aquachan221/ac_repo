[bits 32]

pmode32_init:
    cli

    ; Setup data segments
    mov ax, 0x10       ; Data segment selector from GDT
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax

    ; Setup safe stack
    mov esp, 0x9FC00

    ; Boot banner
    mov si, msg
    call print_string

    ; Call kernel stub
    call kernel32_entry

.halt:
    hlt
    jmp .halt

; -------------------------------
kernel32_entry:
    mov si, kernel_msg
    call print_string
    ret

; -------------------------------
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

msg        db "🚀 AquaOS: Protected mode initialized. Launching kernel...", 0
kernel_msg db "🌊 AquaOS: Kernel32 stub reached successfully.", 0