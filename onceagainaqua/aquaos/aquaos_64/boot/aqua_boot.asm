org 0x7C00
bits 16

start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00

    call print_bootmsg

    mov ah, 0x02         ; Read sectors
    mov al, 4            ; Number of sectors
    mov ch, 0            ; Cylinder
    mov cl, 2            ; Sector (starts at 1)
    mov dh, 0            ; Head
    mov dl, 0x80         ; First HDD
    mov bx, 0x8000       ; Load address
    int 0x13
    jc disk_fail

    jmp 0x0000:0x8000    ; Jump to GDT setup

print_char:
    mov ah, 0x0E
    int 0x10
    ret

print_bootmsg:
    mov si, boot_msg
.next:
    lodsb
    or al, al
    jz .done
    call print_char
    jmp .next
.done:
    ret

disk_fail:
    mov si, fail_msg
    call print_bootmsg
    hlt

boot_msg db "yay", 0
fail_msg db "aww", 0

times 510 - ($ - $$) db 0
dw 0xAA55