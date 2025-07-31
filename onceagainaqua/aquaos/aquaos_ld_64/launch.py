import subprocess
import os

def launch_qemu(iso_path, disk_image="vm.img", memory="512M", cpu_cores=1,
                qemu_path="D:\\path\\to\\qemu-system-x86_64.exe",
                qemu_img_path="D:\\path\\to\\qemu-img.exe"):
    
    # Ensure paths exist
    if not os.path.isfile(iso_path):
        raise FileNotFoundError(f"ISO not found at: {iso_path}")
    
    if not os.path.isfile(qemu_path):
        raise FileNotFoundError(f"QEMU binary not found at: {qemu_path}")

    if not os.path.isfile(qemu_img_path):
        raise FileNotFoundError(f"qemu-img not found at: {qemu_img_path}")

    # Create disk image if missing
    if not os.path.exists(disk_image):
        subprocess.run([qemu_img_path, "create", "-f", "qcow2", disk_image, "512M"])

    # Construct QEMU command
    cmd = [
        qemu_path,
        "-m", memory,
        "-smp", str(cpu_cores),
        "-cdrom", iso_path,
        "-hda", disk_image,
        "-boot", "d",
        "-net", "nic",
        "-net", "user",
        "-display", "default"
    ]

    print(f"Launching QEMU with ISO: {iso_path}")
    subprocess.run(cmd)

# Example usage
launch_qemu(
    iso_path="D:\\aqua\\code\\aqua.os\\aquaos_ld_64\\ld\\tinycore-current.iso",
    qemu_path="D:\\aqua\\code\\aqua.os\\qemu-portable-20241220\\qemu-portable-20241220\\qemu-system-x86_64.exe",
    qemu_img_path="D:\\aqua\\code\\aqua.os\\qemu-portable-20241220\\qemu-portable-20241220\\qemu-img.exe"
)