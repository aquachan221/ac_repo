import usb.core
import usb.backend.libusb1

backend = usb.backend.libusb1.get_backend(
    find_library=lambda x: r"D:\aqua\code\dependencies\python\Lib\site-packages\libusb\_platform\_windows\x64\libusb-1.0.dll"
)

devices = usb.core.find(find_all=True, backend=backend)

if devices:
    for dev in devices:
        print(f"Vendor ID: {hex(dev.idVendor)}, Product ID: {hex(dev.idProduct)}")
else:
    print("No USB devices found or accessible.")