FROM openvino/ubuntu18_dev:2021.4.2

USER root

# Install dependencies for USB device management
RUN apt-get update && apt-get install -y --no-install-recommends \
    libusb-1.0-0-dev \
    libusb-0.1-4 \
    usbutils \
    python3-pip \
    python3-setuptools \
    && rm -rf /var/lib/apt/lists/*

# Install python libraries
RUN pip3 install --upgrade pip && \
    pip3 install depthai pyusb numpy opencv-python

USER root

WORKDIR /app

# Simple script to check for NCS devices
COPY load_model.py .

# Use python3 explicitly in the entrypoint
ENTRYPOINT ["/bin/bash", "-c", "source /opt/intel/openvino/bin/setupvars.sh && python3 -u load_model.py"]
