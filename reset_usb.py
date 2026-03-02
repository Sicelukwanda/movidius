import usb.core
import usb.util
import time

def reset_device(vendor_id, product_id):
    dev = usb.core.find(idVendor=vendor_id, idProduct=product_id)
    if dev:
        print(f"Found device {vendor_id:04x}:{product_id:04x}. Resetting...")
        try:
            dev.reset()
            print("Reset successful.")
        except Exception as e:
            print(f"Reset failed: {e}")
    else:
        print("Device not found for reset.")

if __name__ == "__main__":
    # NCS1 initial ID
    reset_device(0x03e7, 0x2150)
