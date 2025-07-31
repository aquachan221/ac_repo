import os
import subprocess
import time

# === User-Defined Build Folder ===
BUILD_DIR = r"F:\aqua\aqua.os\aquaos32\build32"

# === Folder Setup ===
OBJ_DIR     = os.path.join(BUILD_DIR, "obj")
IMG_PATH    = os.path.join(BUILD_DIR, "aquaos32.img")

# === Source Paths ===
BOOTLOADER = r"F:\aqua\aqua.os\aquaos32\boot"
RAMSEG_DIR = os.path.join(BOOTLOADER, "ram")
KERNEL_C   = r"F:\aqua\aqua.os\aquaos32\kernel\kernel.c"

# === Toolchain ===
NASM     = r"F:\aqua\aqua.os\nasm\nasm.exe"
GCC      = r"F:\aqua\aqua.os\gcc-prebuilt-elf-toolchains-master\aarch64-milouk-elf\bin\aarch64-milouk-elf-gcc.exe"
OBJCOPY  = os.path.join(os.path.dirname(GCC), "i386-elf-objcopy.exe")

# === Input Files ===
ASM_FILES = [
    os.path.join(BOOTLOADER, "modes", "aqua_pmode32.asm"),
    os.path.join(RAMSEG_DIR, "aqua_gdt32.asm"),
    os.path.join(BOOTLOADER, "ram", "aqua_paging32.asm"),
    os.path.join(BOOTLOADER, "aqua_kernel32.asm")
]

def run(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print("❌ Command failed:\n" + " ".join(cmd))
        print(result.stderr.decode())
        raise subprocess.CalledProcessError(result.returncode, cmd)

def ensure_dirs():
    os.makedirs(OBJ_DIR, exist_ok=True)

def build_asm():
    print("🔧 Assembling ASM files to flat binaries...")
    bin_paths = []
    for path in ASM_FILES:
        name = os.path.basename(path).replace(".asm", ".bin")
        out = os.path.join(OBJ_DIR, name)
        run([NASM, "-f", "bin", path, "-o", out])
        bin_paths.append(out)
    return bin_paths

def build_c_kernel():
    print("🧬 Compiling C kernel to binary...")
    kernel_obj  = os.path.join(OBJ_DIR, "kernel_main.o")
    kernel_bin  = os.path.join(OBJ_DIR, "kernel_main.bin")
    run([GCC, "-m32", "-ffreestanding", "-c", KERNEL_C, "-o", kernel_obj])
    run([OBJCOPY, "-O", "binary", kernel_obj, kernel_bin])
    return kernel_bin

def make_img(all_bins):
    print("📦 Combining all binaries into disk image...")
    with open(IMG_PATH, "wb") as out_img:
        for path in all_bins:
            with open(path, "rb") as part:
                out_img.write(part.read())
    print(f"✅ Disk image created: {IMG_PATH}")

def launch_qemu():
    print("🚀 Launching AquaOS in QEMU...")
    run(["qemu-system-i386", "-drive", f"file={IMG_PATH},format=raw", "-m", "64M"])

def clear():
    time.sleep(3)
    os.system("cls" if os.name == "nt" else "clear")

def build_all():
    ensure_dirs()
    bins = build_asm()
    kernel_bin = build_c_kernel()
    bins.append(kernel_bin)
    make_img(bins)
    launch_qemu()
    clear()

if __name__ == "__main__":
    build_all()