# 🔊 EADE: Edge-Acoustic Diagnostic Engine

![C++](https://img.shields.io/badge/Language-C%2B%2B17-blue.svg)
![Python](https://img.shields.io/badge/Language-Python%203.10-green.svg)
![Signal Processing](https://img.shields.io/badge/Domain-Signal%20Processing-orange.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

> An edge-compatible acoustic and vibration signal processing framework designed for automated mechanical anomaly detection using Short-Time Fourier Transform (STFT) and spectral analysis.

---

## 📸 Quick Visual Demo

![EADE Spectrogram Processing Demo](./assets/demo_preview.gif)

🎬 **[Watch High-Resolution Demo Video](https://github.com/IsmailHasasna)** | 📄 **[Read Technical Overview](./docs/TECHNICAL_REPORT.pdf)**

---

## 🔑 Core Features & Engineering Highlights

- **Time-Frequency Spectral Decomposition:** Utilizes Short-Time Fourier Transform (STFT) with custom windowing (Hann/Hamming) to isolate acoustic frequency variations.
- **Edge Hardware Optimization:** Low-memory array processing designed to execute efficiently on embedded ARM/Linux architecture.
- **Automated Anomaly Detection:** Extracts spectral centroid and energy distribution to detect mechanical irregularities in real time.
- **Noise Suppression Pipeline:** Integrates digital FIR/Butterworth filtering to remove ambient background noise prior to signal evaluation.

---

## 🛠️ Tech Stack & Requirements

- **Languages:** C++17, Python 3.10
- **Signal Processing & Math:** STFT Algorithms, NumPy, SciPy
- **Target Hardware:** Embedded Nodes / Linux Workstations

---

## 🚀 Quick Execution Guide

```bash
# Clone repository
git clone [https://github.com/IsmailHasasna/EADE.git](https://github.com/IsmailHasasna/EADE.git)
cd EADE

# Run signal analysis pipeline
python src/main_analysis.py --input data/sample_vibration.wav
