import asyncio
from bleak import BleakClient

address = "BC:10:2F:34:C8:69"

def notification_handler(sender, data):
    print(f"🔔 Notification from {sender}: {data}")

async def main():
    async with BleakClient(address) as client:
        print("✅ Connected:", client.is_connected)

        for service in client.services:
            for char in service.characteristics:
                # Readable
                if "read" in char.properties:
                    try:
                        value = await client.read_gatt_char(char.uuid)
                        print(f"📖 {char.uuid} READ:", value)
                    except Exception as e:
                        print(f"⚠️ Could not read {char.uuid}: {e}")

                # Notifiable
                if "notify" in char.properties:
                    try:
                        await client.start_notify(char.uuid, notification_handler)
                        print(f"🔔 Subscribed to {char.uuid}")
                    except Exception as e:
                        print(f"⚠️ Could not subscribe to {char.uuid}: {e}")

        # Stay connected for notifications
        await asyncio.sleep(10)

asyncio.run(main())