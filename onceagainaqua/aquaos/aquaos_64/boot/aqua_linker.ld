ENTRY(kernel_main)

SECTIONS {
    /* Higher-half kernel base address */
    . = 0xFFFFFFFF80000000;

    /* Text (code) section */
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
}