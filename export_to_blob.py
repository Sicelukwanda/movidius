import torch
import torch.nn as nn
import blobconverter
import os
import onnx
from onnxsim import simplify

class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.conv = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2)
        self.fc = nn.Linear(16 * 112 * 112, 10)

    def forward(self, x):
        x = self.pool(self.relu(self.conv(x)))
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x

def main():
    model = SimpleNet()
    model.eval()

    dummy_input = torch.randn(1, 3, 224, 224)
    onnx_path = "model.onnx"
    
    print("Exporting to ONNX...")
    torch.onnx.export(
        model, 
        dummy_input, 
        onnx_path, 
        input_names=['input'], 
        output_names=['output'],
        opset_version=12
    )

    print("Simplifying ONNX...")
    onnx_model = onnx.load(onnx_path)
    model_simp, check = simplify(onnx_model)
    assert check, "Simplified ONNX model could not be validated"
    onnx.save(model_simp, "model_sim.onnx")

    print("Converting Simplified ONNX to Myriad Blob via Luxonis API...")
    try:
        # 2021.4 is stable and often compatible with 2020.1 blobs
        blob_path = blobconverter.from_onnx(
            model="model_sim.onnx",
            data_type="FP16",
            shaves=4,
            version="2021.4",
            use_cache=False
        )
        
        if os.path.exists(blob_path):
            os.rename(blob_path, "model.blob")
            print(f"Success: model.blob created.")
    except Exception as e:
        print(f"Conversion failed: {e}")

if __name__ == "__main__":
    main()
