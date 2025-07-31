; aqua_paging32.asm — AquaOS 32-bit Paging Setup
[bits 32]

paging32_init:
    cli

    ; Load page directory address into CR3
    mov eax, page_directory
    mov cr3, eax

    ; Enable paging (set PG bit in CR0)
    mov eax, cr0
    or eax, 0x80000000
    mov cr0, eax

    ; Display paging message
    mov si, msg
    call print_string

    ret

; -------------------------------
align 4096
page_directory:
    dd page_table + 0x3           ; First entry: present + rw
    times 1023 dd 0               ; Unused entries

align 4096
page_table:
    %assign i 0
    %rep 1024
        dd i + 0x3                ; Identity map + present + rw
        %assign i i + 0x1000
    %endrep

; -------------------------------
msg db "🧠 AquaOS: Paging enabled (32-bit)", 0

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