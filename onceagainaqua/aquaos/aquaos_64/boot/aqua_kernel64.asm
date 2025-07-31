; aqua_kernel64.asm — AquaOS 64-bit Kernel Entry
bits 64
org 0xC000

start:
    cli
    mov ax, DATA_SEG
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov rsp, 0xD000         ; Stack pointer

    mov rsi, kernel_msg
    call print_string

.halt:
    hlt
    jmp .halt

; -------------------------------
; Text Output (VGA direct write)
print_char:
    mov rbx, 0xB8000
    mov ah, 0x0F
    mov [rbx], ax
    add rbx, 2
    ret

print_string:
.next:
    lodsb
    or al, al
    jz .done
    mov ah, 0x0F
    call print_char
    jmp .next
.done:
    ret

kernel_msg db "🧬 AquaOS Kernel64: Ready to vibe.", 0

CODE_SEG equ 0x08
DATA_SEG equ 0x10