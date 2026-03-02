import torch
import torch.nn as nn
import onnx
import openvino as ov
import os

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
    print(f"PyTorch version: {torch.__version__}")
    model = SimpleNet()
    model.eval()

    # 1. Export to ONNX using modern PyTorch
    dummy_input = torch.randn(1, 3, 224, 224)
    onnx_path = "model.onnx"
    
    print("Exporting to ONNX...")
    torch.onnx.export(
        model, 
        dummy_input, 
        onnx_path, 
        input_names=['input'], 
        output_names=['output'],
        opset_version=11,
        do_constant_folding=True
    )
    
    if os.path.exists(onnx_path):
        print(f"Success: {onnx_path} created.")

    # 2. Convert to OpenVINO IR (Host side)
    print("Converting to OpenVINO IR...")
    core = ov.Core()
    ov_model = ov.convert_model(onnx_path)
    ov.save_model(ov_model, "model.xml")
    print("Success: model.xml and model.bin created.")

if __name__ == "__main__":
    main()
