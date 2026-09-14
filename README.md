# Edge-Acoustic Diagnostic Engine (EADE) 🎙️⚙️

An ultra-lightweight, real-time acoustic anomaly detection framework designed for embedded edge devices (ESP32-S3 / Raspberry Pi / Jetson Nano).

## 📌 Overview
EADE processes real-time mechanical sound signatures, converts raw audio buffers into normalized Log-Mel Spectrograms, and uses a Deep Autoencoder neural network to detect mechanical wear and tear before system failure.

## 🛠️ Key Features
- **Zero-Cloud Dependency:** Operates fully on edge nodes with sub-20ms inference latency.
- **Unsupervised Anomaly Detection:** Learns normal operating sounds and flags deviations without needing labeled fault data.
- **Optimized Pipeline:** Custom STFT signal conversion paired with ONNX/TFLite model quantization.

## 🚀 Quick Start

### Installation
```bash
git clone [https://github.com/YOUR_USERNAME/edge-acoustic-diagnostics.git](https://github.com/YOUR_USERNAME/edge-acoustic-diagnostics.git)
cd edge-acoustic-diagnostics
pip install -r requirements.txt
```

### Basic Usage
```python
from audio_processor import AcousticFeatureExtractor
from anomaly_model import AcousticAutoencoder

# 1. Initialize Extractor and Autoencoder
extractor = AcousticFeatureExtractor()
model = AcousticAutoencoder()

# 2. Extract Spectrogram Features
# spec = extractor.extract_mel_spectrogram(audio_buffer)
```

## 🏗️ System Architecture
`Audio Input (Mic/Sensor) -> STFT / Mel-Transformation -> Autoencoder Reconstruction -> Anomaly Score`
