ENTRY(kernel32_entry)

SECTIONS {
    /* Link everything at 1MB */
    . = 0x00100000;

    /* Code section */
    .text : {
        *(.text)
    }

    /* Read-only data */
    .rodata : {
        *(.rodata)
    }

    /* Initialized data */
    .data : {
        *(.data)
    }

    /* Uninitialized data */
    .bss : {
        *(.bss)
        *(COMMON)
    }

    /DISCARD/ : {
        *(.eh_frame)     /* Remove exception handling sections */
        *(.note.*)       /* Strip ELF notes */
    }
}