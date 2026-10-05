# 🎙️ ZINO EADE - Edge Acoustic Diagnostic Engine

![Python](https://img.shields.io/badge/Language-Python%203.10-blue.svg)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red.svg)
![Signal Processing](https://img.shields.io/badge/Domain-FFT%20%26%20Audio%20Diagnostics-orange.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

> An edge-compatible acoustic diagnostic platform leveraging Fast Fourier Transform (FFT) signal processing for real-time mechanical anomaly detection and predictive maintenance across automotive, industrial, and home appliance domains.

---

## 🔑 Key Features & Technical Highlights

- **Live & File Audio Ingestion:** Direct microphone input streaming (`st.audio_input`) or pre-recorded audio file analysis (`WAV`, `MP3`, `OGG`).
- **FFT Spectrum Analysis:** Decomposes acoustic signatures to calculate **Acoustic Health Score**, **Dominant FFT Peak Frequency**, and **Anomaly Index**.
- **Multi-Domain Diagnostic Engine:**
  - 🚗 **Automotive Platform:** Specialized acoustic profiling for **Mitsubishi Pajero V20**, **Hyundai Santa Fe**, and **Volkswagen Caddy TDI**.
  - 🔌 **Home Appliances:** Diagnostic modules for washing machines, refrigerators, air conditioners, and dishwashers.
  - 🏭 **Industrial Machinery:** Vibration and acoustic fault analysis for 3-phase induction motors, hydraulic pumps, and screw compressors.
- **Interactive Visuals & Multilingual Support:** Features dynamic color laser scan simulations and full trilingual UI support (**Arabic, English, Russian**).

---

## 🛠️ Tech Stack & Dependencies

- **Core Language:** Python 3.10+
- **Frontend / UI Framework:** Streamlit, HTML5, Custom CSS3 Styling
- **Signal Processing:** Audio Spectrum Breakdown, FFT Peak Detection, NumPy, SciPy

---

## 📁 Repository Structure

- `app.py` - Main Streamlit execution & UI pipeline
- `requirements.txt` - Python dependencies
- `README.md` - Project technical documentation

---

## 🚀 Quick Execution Guide

```bash
# Clone repository
git clone https://github.com/hasasnahismail-max/edge-acoustic-diagnostics.git
cd edge-acoustic-diagnostics

# Install dependencies
pip install -r requirements.txt

# Launch application
streamlit run app.py
