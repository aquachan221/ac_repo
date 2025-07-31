; aqua_pmode.asm — AquaOS Protected Mode Setup
bits 16
org 0x9000

start:
    cli
    mov eax, cr0
    or eax, 0x1           ; Set PE bit to enable protected mode
    mov cr0, eax

    jmp CODE_SEG:init_pm  ; Far jump to flush pipeline

; -------------------------------
; Protected Mode Init
bits 32
init_pm:
    mov ax, DATA_SEG
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov esp, 0xA000       ; Stack for PM

    mov si, pm_msg
    call print_string

    jmp 0x0000:0xA000     ; Jump to paging setup

; -------------------------------
; Text Output (BIOS-compatible)
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

pm_msg db "🔧 AquaOS: Protected mode activated!", 0

CODE_SEG equ 0x08
DATA_SEG equ 0x10