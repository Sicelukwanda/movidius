# Modern-to-Legacy NCS1 Bridge

This project provides a functional bridge between **modern AI software (PyTorch 2.10+)** and the **legacy Intel Movidius Neural Compute Stick 1 (NCS1)** from 2017. 

## The Challenge
Bridging a 9-year gap in AI software is difficult because:
1. **Driver Deprecation:** Modern OpenVINO (2024+) has completely removed the `MYRIAD` plugin required for the NCS1.
2. **USB Handshake:** The NCS1 uses a unique two-stage boot. It starts as ID `03e7:2150` (Bootloader), receives firmware, resets itself, and re-appears as ID `03e7:215a` (VPU).
3. **Kernel/Controller Conflicts:** Modern Linux kernels and high-speed xHCI (USB 3.x) controllers often "lock" the device or cause timing timeouts during this reset.

## Architecture
- **Host Side:** A modern `uv`-managed Python environment (Python 3.12) used for model design and exporting to the specialized `.blob` format via the Luxonis/DepthAI Cloud API.
- **Docker Side:** A legacy OpenVINO environment (version 2021.4) acting as the hardware bridge to talk to the physical stick.

## Prerequisites
- Linux Host (Ubuntu/Debian recommended)
- `uv` (Python package manager)
- Docker & Docker Compose
- Intel Movidius NCS1 (Original)

## Setup

### 1. Install Udev Rules (CRITICAL)
The host must allow the container to access the USB device in both its unbooted and booted states.
```bash
chmod +x install_udev_rules.sh
./install_udev_rules.sh
```

### 2. Prepare the Host Environment
```bash
uv sync
```

## Usage

### Step 1: Export the Model (Host)
Design your model in modern PyTorch and convert it to a `.blob` file compatible with OpenVINO 2021.4.
```bash
uv run export_to_blob.py
```
This generates `model.blob`.

### Step 2: Run Inference (Docker)
Build and run the container to load the blob onto the NCS1 hardware.
```bash
docker compose up --build
```

## Known Issues & Troubleshooting

### `NC_ERROR` / Handshake Timeout
If you see `Failed to load model to MYRIAD: Can not init Myriad device: NC_ERROR`, the software "sees" the stick but the hardware handshake failed.

**Root Cause:** Modern xHCI (USB 3.x/3.1) controllers on high-end motherboards (like TRX40) have aggressive power management and timing that disrupt the legacy 2017 firmware upload.

**Solutions:**
1. **USB 2.0 Hub (Recommended):** Plug the NCS1 into a cheap, non-powered USB 2.0 hub. This forces the handshake to use legacy timing which is significantly more stable.
2. **BIOS Port:** Use the designated "BIOS" or "Flash" USB port on your rear I/O, which often has a different controller configuration.
3. **Udev Tagging:** Ensure the `ID_MM_DEVICE_IGNORE="1"` environment variable is set in your udev rules (included in our script) to prevent ModemManager from "probing" the stick during boot.

## Core Files
- `export_to_blob.py`: Modern PyTorch -> ONNX -> Simplified -> Myriad Blob.
- `load_model.py`: Legacy OpenVINO script to import the blob and initialize the VPU.
- `Dockerfile`: Legacy OpenVINO 2021.4.2 environment.
- `install_udev_rules.sh`: Permission setup for Myriad 1/2/X devices.
