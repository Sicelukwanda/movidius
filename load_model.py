try:
    from openvino.inference_engine import IECore
    import os

    def main():
        import usb.core
        import time
        import os
        
        # Enable detailed logging
        os.environ["OPENVINO_LOG_LEVEL"] = "3"
        os.environ["MVNC_LOG_LEVEL"] = "3"
        
        # 1. Manual Reset to ensure clean state
        print("Searching for NCS1 (03e7:2150)...")
        dev = usb.core.find(idVendor=0x03e7, idProduct=0x2150)
        if dev:
            print("Found NCS1 bootloader. Resetting...")
            try:
                dev.reset()
                time.sleep(3)
            except:
                pass

        ie = IECore()
        
        # # Use both variants of the reset config
        # ie.set_config({"MYRIAD_ENABLE_FORCE_RESET": "YES"}, "MYRIAD")
        # ie.set_config({"VPU_MYRIAD_FORCE_RESET": "YES"}, "MYRIAD")
        
        blob_path = "model.blob"

        if not os.path.exists(blob_path):
            print(f"Error: {blob_path} not found. Run export_to_blob.py on host first.")
            return

        print(f"Loading model to MYRIAD device from {blob_path}...")
        try:
            # In older OpenVINO, to load a blob directly you use import_network
            exec_net = ie.import_network(model_file=blob_path, device_name="MYRIAD")
            print("Success: Model loaded to Movidius NCS1!")
            
            # Print inputs/outputs
            print(f"Inputs: {list(exec_net.input_info.keys())}")
            print(f"Outputs: {list(exec_net.outputs.keys())}")
            
        except Exception as e:
            print(f"Failed to load model to MYRIAD: {e}")

    if __name__ == "__main__":
        main()
except ImportError:
    print("OpenVINO IE not found. Ensure you are running this inside the container.")
