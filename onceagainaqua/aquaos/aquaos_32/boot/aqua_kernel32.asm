; aqua_kernel32.asm — AquaOS Kernel Stub (self-contained)
[bits 32]

kernel32_entry:
    cli
    mov si, banner
    call print_string

    call kernel_main  ; Inlined below

.halt:
    hlt
    jmp .halt

; -------------------------------
kernel_main:
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

banner     db "🌊 AquaOS Kernel Stub Loaded", 0
kernel_msg db "🧠 AquaOS C kernel stub triggered", 0