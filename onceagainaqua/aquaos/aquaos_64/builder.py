import os
import sys
import shutil
import subprocess
import struct
import time

# Paths
AQUA_BOOT = r"F:\aqua\aqua.os\aquaosfr\boot\aqua_boot.asm"
AQUA_GDT = r"F:\aqua\aqua.os\aquaosfr\boot\ram\aqua_gdt.asm"
AQUA_PMODE = r"F:\aqua\aqua.os\aquaosfr\boot\modes\aqua_pmode.asm"
AQUA_PAGING = r"F:\aqua\aqua.os\aquaosfr\boot\ram\aqua_paging.asm"
AQUA_LONGMODE = r"F:\aqua\aqua.os\aquaosfr\boot\modes\aqua_long_mode.asm"

KERNEL_ASM = r"F:\aqua\aqua.os\aquaosfr\boot\aqua_kernel64.asm"
KERNEL_C = r"F:\aqua\aqua.os\aquaosfr\kernel\aqua_kernel.c"
LINKER_LD = r"F:\aqua\aqua.os\aquaosfr\boot\aqua_linker.ld"

IMAGE_PATH = r"F:\aqua\aqua.os\build\aquaos.img"
KERNEL_ELF = r"F:\aqua\aqua.os\build\kernel.elf"
OBJ_DIR = r"F:\aqua\aqua.os\build\obj"
BIN_DIR = r"F:\aqua\aqua.os\build\bin"

NASM = r"F:\aqua\aqua.os\nasm\nasm.exe"
GCC = r"F:\aqua\aqua.os\x86_64_elf_tools_windows\x86_64_elf_tools_windows\bin\x86_64-elf-gcc.exe"
LD = r"F:\aqua\aqua.os\x86_64_elf_tools_windows\x86_64_elf_tools_windows\bin\x86_64-elf-ld.exe"

def run(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stderr.decode())
        raise subprocess.CalledProcessError(result.returncode, cmd)

def clean():
    if os.path.exists(OBJ_DIR): shutil.rmtree(OBJ_DIR)
    if os.path.exists(BIN_DIR): shutil.rmtree(BIN_DIR)
    if os.path.exists(IMAGE_PATH): os.remove(IMAGE_PATH)
    if os.path.exists(KERNEL_ELF): os.remove(KERNEL_ELF)
    os.makedirs(OBJ_DIR)
    os.makedirs(BIN_DIR)

def build_boot():
    files = [AQUA_BOOT, AQUA_GDT, AQUA_PMODE, AQUA_PAGING, AQUA_LONGMODE]
    addr = 0x7C00
    out = os.path.join(BIN_DIR, "boot.bin")
    with open(out, "wb") as out_file:
        for f in files:
            obj = os.path.join(OBJ_DIR, os.path.basename(f) + ".bin")
            run([NASM, f, "-f", "bin", "-o", obj])
            out_file.write(open(obj, "rb").read())
            addr += os.path.getsize(obj)

def build_kernel():
    obj_c = os.path.join(OBJ_DIR, "kernel.o")
    run([GCC, "-c", KERNEL_C, "-ffreestanding", "-m64", "-o", obj_c])
    run([LD, "-T", LINKER_LD, obj_c, "-o", KERNEL_ELF])

def make_image():
    with open(IMAGE_PATH, "wb") as img:
        boot_bin = os.path.join(BIN_DIR, "boot.bin")
        img.write(open(boot_bin, "rb").read())
        img.write(open(KERNEL_ELF, "rb").read())

def read_bytes(f, offset, count):
    f.seek(offset)
    return f.read(count)

def hex_dump(data, width=16):
    for i in range(0, len(data), width):
        chunk = data[i:i+width]
        hex_str = ' '.join(f"{b:02X}" for b in chunk)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print(f"{i:08X}  {hex_str:<48}  {ascii_str}")

def print_layout():
    with open(IMAGE_PATH, "rb") as img:
        data = img.read()
        boot_size = data.find(b'\x7FELF')
        kernel_offset = boot_size if boot_size != -1 else len(data) // 2
        print(f"[BOOTLOADER]  Offset: 0x0000  Size: {kernel_offset} bytes")
        print(f"[KERNEL.ELF]  Offset: {kernel_offset:#06X}  Size: {len(data) - kernel_offset} bytes\n")
        print("ELF HEADER:")
        hex_dump(read_bytes(img, kernel_offset, 64))

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    clean()
    build_boot()
    build_kernel()
    make_image()
    print_layout()
    time.sleep(20)
    clear()