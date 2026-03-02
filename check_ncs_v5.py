import usb.core
import usb.util
import time
import os
from openvino.inference_engine import IECore

def main():
    print("--- NCS1 Final Stand Detection ---")
    # Increase OpenVINO logging
    os.environ["OPENVINO_LOG_LEVEL"] = "3"
    os.environ["MVNC_LOG_LEVEL"] = "3"
    
    ie = IECore()
    print("Watching for 03e7:2150...")

    while True:
        dev = usb.core.find(idVendor=0x03e7, idProduct=0x2150)
        if dev:
            print(f">>> Found NCS1 Bootloader (03e7:2150).")
            try:
                print("Performing hard reset via libusb...")
                dev.reset()
                time.sleep(2) # Wait for device to settle
            except Exception as e:
                print(f"Reset info: {e}")
            
            print("Requesting OpenVINO to claim Myriad...")
            try:
                # This specific call forces the plugin to look for and boot the device
                devices = ie.available_devices
                print(f"Current devices: {devices}")
                if "MYRIAD" in devices:
                    print("!!! SUCCESS: NCS1 CLAIMED BY OPENVINO !!!")
                    break
            except Exception as e:
                print(f"IE Error: {e}")
        
        # Check if it already booted (215a)
        dev_booted = usb.core.find(idVendor=0x03e7, idProduct=0x215a)
        if dev_booted:
            print(">>> Found NCS1 in BOOTED state (03e7:215a).")
            if "MYRIAD" in ie.available_devices:
                print("!!! SUCCESS: NCS1 IS READY !!!")
                break
        
        time.sleep(1)

if __name__ == "__main__":
    main()
