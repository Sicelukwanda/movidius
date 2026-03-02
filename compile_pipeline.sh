#!/bin/bash
# 1. Export from PyTorch 2.7+ to ONNX (Host)
echo "Step 1: Exporting from PyTorch..."
uv run python export_model.py

# 2. Convert to OpenVINO IR (Host)
echo "Step 2: Converting to OpenVINO IR..."
# Since OpenVINO 2024 is on host, we use its model optimizer or convert_model
uv run python -c "import openvino as ov; model = ov.convert_model('model.onnx'); ov.save_model(model, 'model.xml')"

echo "Step 3: Compiling for MYRIAD (NCS1)..."
# This is the tricky part - compiling to blob without a live device
# We use the 'compile_tool' if available in the openvino package
# Or we rely on the Luxonis online converter if the host can't do it.

# Try local compilation if compile_tool is in path
if [ -f ".venv/bin/compile_tool" ]; then
    .venv/bin/compile_tool -m model.xml -d MYRIAD -ip U8
else
    echo "compile_tool not found in venv. Using Luxonis blobconverter as backup..."
    uv run python export_to_blob.py
fi
