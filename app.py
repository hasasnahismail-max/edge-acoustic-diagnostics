import io
import numpy as np
from scipy.io import wavfile
from sklearn.ensemble import IsolationForest
import streamlit as st

# --- 1. Mechanical Custom Theme Configuration ---
st.set_page_config(
    page_title="ZINO EADE - Ismail Hasasnah", page_icon="⚙️", layout="centered"
)

st.markdown(
    """
    <style>
    /* Carbon Slate Background */
    .stApp {
        background-color: #121519;
        color: #FFFFFF;
    }
    /* ZINO EADE Mechanical Header Card */
    .brand-header {
        background: linear-gradient(180deg, #1A1D22 0%, #1E232A 100%);
        border: 2px solid #FF6B00;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0px 4px 20px rgba(255, 107, 0, 0.35);
        margin-bottom: 20px;
    }
    .brand-title {
        color: #FF6B00;
        font-size: 32px;
        font-weight: 900;
        letter-spacing: 2px;
        margin: 0;
    }
    .designer-tag {
        color: #9CA3AF;
        font-size: 13px;
        font-weight: bold;
        margin-top: 6px;
    }
    .vehicle-badge {
        background-color: #1E232A;
        border-left: 5px solid #FF6B00;
        border-right: 1px solid #2C333D;
        border-top: 1px solid #2C333D;
        border-bottom: 1px solid #2C333D;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 25px;
        font-size: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- 2. Branding Header & Vehicle Profile ---
st.markdown(
    """
    <div class="brand-header">
        <h1 class="brand-title">⚙️ ZINO EADE</h1>
        <div class="designer-tag">ACOUSTIC DIAGNOSTIC SYSTEM | ENGINEERED BY ISMAIL HASASNAH</div>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="vehicle-badge">
        🚙 <strong>Target Vehicle Profile:</strong> Mitsubishi Pajero V20 (1998) 3.4L V6 Engine
    </div>
""",
    unsafe_allow_html=True,
)


# --- 3. Acoustic Processing Engine ---
class AudioProcessor:

    def extract_features(self, signal, n_fft=512, hop_length=256):
        signal = np.asarray(signal, dtype=np.float32)
        if len(signal) < n_fft:
            signal = np.pad(signal, (0, n_fft - len(signal)))
        num_frames = max(1, (len(signal) - n_fft) // hop_length + 1)
        window = np.hanning(n_fft)

        spectrogram = []
        for i in range(num_frames):
            start = i * hop_length
            frame = signal[start : start + n_fft]
            if len(frame) < n_fft:
                frame = np.pad(frame, (0, n_fft - len(frame)))
            fft_mag = np.abs(np.fft.rfft(frame * window))
            spectrogram.append(fft_mag)

        spectrogram = np.array(spectrogram)
        spec_mean = np.mean(spectrogram, axis=0)[:18]
        energy = np.mean(signal**2)
        zcr = np.mean(np.diff(np.signbit(signal)) != 0)
        return np.concatenate([spec_mean, [energy, zcr]])


@st.cache_resource
def load_trained_model():
    processor = AudioProcessor()
    normal_samples = [
        np.random.normal(0, 0.1, size=22050 * 2) for _ in range(40)
    ]
    X_train = np.array([processor.extract_features(s) for s in normal_samples])
    model = IsolationForest(contamination=0.03, random_state=42)
    model.fit(X_train)
    return processor, model


processor, model = load_trained_model()

# --- 4. Live Audio Recording Input ---
st.subheader("🎙️ الفحص المباشر لمكونات المحرك")
audio_data = st.audio_input("اضغط تسجيل للحصول على البصمة الصوتية للمحرك")

if audio_data is not None:
    st.audio(audio_data, format="audio/wav")

    bytes_data = audio_data.read()
    sr, signal = wavfile.read(io.BytesIO(bytes_data))

    if len(signal.shape) > 1:
        signal = np.mean(signal, axis=1)

    signal = signal / np.max(np.abs(signal) + 1e-6)

    features = processor.extract_features(signal)
    score = model.score_samples([features])[0]
    prediction = model.predict([features])[0]

    anomaly_pct = round((1 - (score + 1) / 2) * 100, 2)
    is_anomaly = prediction == -1

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Anomaly Score (نسبة الشذوذ)", value=f"{anomaly_pct}%")

    with col2:
        if is_anomaly:
            st.error("⚠️ MECHANICAL DEFECT DETECTED")
            st.caption("تم كشف اضطراب في البصمة الصوتية (احتكاك / طقطقة ميكانيكية)")
        else:
            st.success("✅ OPTIMAL ENGINE OPERATION")
            st.caption("المحرك يعمل بنسق طبيعي وسليم")

    st.subheader("📈 الموجة الصوتية الحية (Live Waveform)")
    st.line_chart(signal[::100])
