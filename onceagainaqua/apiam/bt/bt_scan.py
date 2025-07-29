import asyncio
from bleak import BleakScanner

async def main():
    print("Scanning for BLE devices...")
    results = await BleakScanner.discover(timeout=5.0, return_adv=True)
    for (device, adv) in results.values():
        print(f"{adv.local_name or 'Unknown'} - {device.address} (RSSI: {adv.rssi} dB)")

asyncio.run(main())