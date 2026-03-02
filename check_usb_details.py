import usb.core
import usb.util
import sys

# NCS1 IDs
VENDOR_ID = 0x03e7
PRODUCT_ID = 0x2150 # Unbooted

def check_usb():
    print(f"Searching for device {VENDOR_ID:04x}:{PRODUCT_ID:04x}...")
    dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    
    if dev is None:
        print("Device not found.")
        # Check if it's already booted
        dev = usb.core.find(idVendor=0x03e7, idProduct=0x215a)
        if dev:
            print("Device found in BOOTED state (03e7:215a)!")
        return

    print("Device found!")
    print(f"Manufacturer: {usb.util.get_string(dev, dev.iManufacturer)}")
    print(f"Product: {usb.util.get_string(dev, dev.iProduct)}")
    print(f"Serial: {usb.util.get_string(dev, dev.iSerialNumber)}")

    for cfg in dev:
        print(f"Config {cfg.bConfigurationValue}:")
        for intf in cfg:
            print(f"  Interface {intf.bInterfaceNumber}, Alt {intf.bAlternateSetting}:")
            for ep in intf:
                print(f"    Endpoint {ep.bEndpointAddress:02x}, Type: {ep.bmAttributes}, MaxPacket: {ep.wMaxPacketSize}")

if __name__ == "__main__":
    check_usb()
