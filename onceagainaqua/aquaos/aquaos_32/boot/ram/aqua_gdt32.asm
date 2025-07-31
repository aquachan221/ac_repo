; aqua_gdt32.asm — AquaOS 32-bit Global Descriptor Table Setup
[bits 16]

gdt32_init:
    cli
    lgdt [gdt_descriptor]      ; Load the GDT
    mov eax, cr0
    or eax, 0x1                ; Enable Protected Mode
    mov cr0, eax
    jmp 0x08:pmode_entry       ; Far jump to flush pipeline

; -----------------------------------------
gdt_start:
    dq 0x0000000000000000      ; Null descriptor
    dq 0x00CF9A000000FFFF      ; Code segment
    dq 0x00CF92000000FFFF      ; Data segment
gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

; -----------------------------------------
[bits 32]
pmode_entry:
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov esp, 0x9FC00

    mov si, banner
    call print_string

    call paging32_init         ; Inlined below

.halt:
    hlt
    jmp .halt

; -----------------------------------------
paging32_init:
    mov si, paging_msg
    call print_string
    ret

banner db "🔧 AquaOS: GDT loaded, entering protected mode!", 0
paging_msg db "🧠 Paging init stub: Ready for expansion", 0

; -----------------------------------------
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