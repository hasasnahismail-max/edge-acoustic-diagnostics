import io
import numpy as np
import plotly.graph_objects as go
import scipy.io.wavfile as wavfile
import scipy.signal as signal
import streamlit as st

# استدعاء آمن لمكتبات الصوت لدعم كافة الصيغ
HAS_LIBROSA, HAS_SOUNDFILE, HAS_PYDUB = False, False, False
try:
    import librosa
    HAS_LIBROSA = True
except ImportError:
    pass
try:
    import soundfile as sf
    HAS_SOUNDFILE = True
except ImportError:
    pass
try:
    from pydub import AudioSegment
    HAS_PYDUB = True
except ImportError:
    pass

st.set_page_config(page_title="ZINO EADE - Acoustic Workstation", page_icon="⚡", layout="wide")

# ==========================================
# 1. الثيمات والألوان الديناميكية للأقسام
# ==========================================
THEMES = {
    "السيارات والمركبات": {"color": "#ff7b00", "glow": "rgba(255, 123, 0, 0.25)", "icon": "🚗", "desc": "فحص محركات البنزين والديزل والتيربو"},
    "الثلاجات والتبريد": {"color": "#0099ff", "glow": "rgba(0, 153, 255, 0.25)", "icon": "🧊", "desc": "تشخيص ضواغط الإنفرتر وغرف التبريد"},
    "الأجهزة الكهربائية": {"color": "#a855f7", "glow": "rgba(168, 85, 247, 0.25)", "icon": "🔌", "desc": "محركات الغسالات، المضخات والمحركات العامة"},
    "الماكينات والمعدات": {"color": "#94a3b8", "glow": "rgba(148, 163, 184, 0.25)", "icon": "⚙️", "desc": "محركات JCB، الجرارات والمولدات الصناعية"}
}

if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = "السيارات والمركبات"

current_cat = st.session_state["selected_category"]
theme = THEMES[current_cat]

st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%); color: #c9d1d9; }}
    .theme-header {{ color: {theme['color']} !important; text-shadow: 0 0 15px {theme['glow']}; font-weight: 800; }}
    .metric-card {{ background: rgba(22, 27, 34, 0.85); border: 2px solid {theme['color']}; border-radius: 12px; padding: 18px; box-shadow: 0 6px 20px {theme['glow']}; margin-bottom: 15px; }}
    .stButton>button {{ background: linear-gradient(90deg, {theme['color']} 0%, #238636 100%) !important; color: #fff !important; font-weight: bold !important; border-radius: 8px !important; border: none !important; padding: 12px 24px !important; width: 100%; }}
    .status-healthy {{ background: rgba(46, 160, 67, 0.2); color: #3fb950; border: 1px solid #2ea043; padding: 6px 14px; border-radius: 20px; font-weight: 700; display: inline-block; }}
    .status-critical {{ background: rgba(248, 81, 73, 0.2); color: #f85149; border: 1px solid #da3633; padding: 6px 14px; border-radius: 20px; font-weight: 700; display: inline-block; }}
    h1, h2, h3, h4 {{ color: #f0f6fc !important; }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. صور القطع الميكانيكية
# ==========================================
COMPONENT_IMAGES = {
    "injectors": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=600&auto=format&fit=crop&q=80",
    "turbo": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=600&auto=format&fit=crop&q=80",
    "bearings": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=600&auto=format&fit=crop&q=80",
    "valves": "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=600&auto=format&fit=crop&q=80",
    "belt": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&auto=format&fit=crop&q=80",
    "compressor_valves": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=600&auto=format&fit=crop&q=80",
    "motor_bearings": "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=600&auto=format&fit=crop&q=80",
    "pump_impeller": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&auto=format&fit=crop&q=80",
    "healthy": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=600&auto=format&fit=crop&q=80"
}

# ==========================================
# 3. قاعدة البيانات العالمية الشاملة
# ==========================================
UNIVERSAL_DATABASE = {
    # --- السيارات ---
    "VW Caddy 1.6 TDI (تنفس طبيعي / بدون تيربو)": {
        "category": "السيارات والمركبات", "brand": "Volkswagen", "model": "Caddy 1.6 TDI NA", "specs": "1.6L TDI Non-Turbo", "has_turbo": False,
        "unit_image": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=800&auto=format&fit=crop&q=80",
        "bands": {"bearing_wear": (20, 350), "belt_squeal": (700, 2000), "valve_clearance": (1000, 2800), "injector_clatter": (3000, 8000)},
        "names": {"bearing_wear": "سبيكة محامل الكرنك", "belt_squeal": "قشاط المجموعات", "valve_clearance": "صمامات المحرك", "injector_clatter": "بخاخات الديزل"}
    },
    "VW Caddy 1.6 TDI (شاحن تيربو)": {
        "category": "السيارات والمركبات", "brand": "Volkswagen", "model": "Caddy 1.6 TDI Turbo", "specs": "1.6L TDI Turbocharged", "has_turbo": True,
        "unit_image": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=800&auto=format&fit=crop&q=80",
        "bands": {"bearing_wear": (20, 350), "turbo_shaft": (1500, 5500), "injector_clatter": (3000, 8000)},
        "names": {"bearing_wear": "سبيكة الكرنك", "turbo_shaft": "عمود ومروحة التيربو", "injector_clatter": "بخاخات الديزل"}
    },
    "Hyundai Santa Fe 2.2 CRDi (تيربو)": {
        "category": "السيارات والمركبات", "brand": "Hyundai", "model": "Santa Fe 2.2 CRDi", "specs": "2.2L CRDi Turbo Diesel", "has_turbo": True,
        "unit_image": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=800&auto=format&fit=crop&q=80",
        "bands": {"bearing_wear": (20, 300), "turbo_shaft": (1500, 5000), "injector_clatter": (2500, 8000)},
        "names": {"bearing_wear": "سبيكة محامل المحرك", "turbo_shaft": "شاحن التيربو", "injector_clatter": "بخاخات الديزل"}
    },
    "Toyota Corolla 1.6L (بنزين)": {
        "category": "السيارات والمركبات", "brand": "Toyota", "model": "Corolla 1.6 VVT-i", "specs": "1.6L VVT-i NA Engine", "has_turbo": False,
        "unit_image": "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800&auto=format&fit=crop&q=80",
        "bands": {"bearing_wear": (30, 350), "belt_squeal": (800, 2000), "valve_clearance": (1000, 3200)},
        "names": {"bearing_wear": "سبيكة الكرنك", "belt_squeal": "سير الحركة", "valve_clearance": "صمامات VVT-i"}
    },

    # --- الثلاجات والتبريد ---
    "ضاغط ثلاجة منزلي (Inverter Compressor)": {
        "category": "الثلاجات والتبريد", "brand": "LG / GE", "model": "Inverter R600a Compressor", "specs": "Variable Speed Hermetic Unit", "has_turbo": False,
        "unit_image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&auto=format&fit=crop&q=80",
        "bands": {"bearing_wear": (20, 280), "compressor_valves": (850, 2400)},
        "names": {"bearing_wear": "محامل الكرنك والضاغط", "compressor_valves": "صمامات الضاغط الداخلية"}
    },

    # --- الأجهزة الكهربائية ---
    "محرك غسالة ملابس (Direct Drive Motor)": {
        "category": "الأجهزة الكهربائية", "brand": "Samsung / Bosch", "model": "BLDC Direct Drive", "specs": "Inverter Motor Assembly", "has_turbo": False,
        "unit_image": "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=800&auto=format&fit=crop&q=80",
        "bands": {"bearing_wear": (30, 320), "belt_squeal": (700, 1900)},
        "names": {"bearing_wear": "محامل الحلة والمحرك", "belt_squeal": "قشاط / سير الحركة"}
    },
    "مضخة مياه كهربائية (Electric Water Pump 2HP)": {
        "category": "الأجهزة الكهربائية", "brand": "Pedrollo / Grundfos", "model": "CPM-158 Pump", "specs": "2.0 HP Single-Phase", "has_turbo": False,
        "unit_image": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format&fit=crop&q=80",
        "bands": {"bearing_wear": (20, 260), "pump_impeller": (900, 2700)},
        "names": {"bearing_wear": "محامل المحرك", "pump_impeller": "عنفة المضخة"}
    },

    # --- الماكينات والمعدات ---
    "محرك حفار JCB (JCB EcoMAX 4.4L Turbo)": {
        "category": "الماكينات والمعدات", "brand": "JCB", "model": "EcoMAX 4.4L Diesel", "specs": "Heavy Duty Turbo Engine", "has_turbo": True,
        "unit_image": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=800&auto=format&fit=crop&q=80",
        "bands": {"bearing_wear": (20, 280), "turbo_shaft": (1400, 4800), "injector_clatter": (2200, 7500)},
        "names": {"bearing_wear": "سبيكة العمود الفقري", "turbo_shaft": "عمود شاحن التيربو", "injector_clatter": "بخاخات الديزل"}
    }
}

# ==========================================
# 4. المعالج الصوتي الشامل لجميع الصيغ
# ==========================================
def read_any_audio(uploaded_file):
    bytes_data = uploaded_file.read()
    if HAS_LIBROSA:
        try:
            buffer = io.BytesIO(bytes_data)
            data, samplerate = librosa.load(buffer, sr=None, mono=True)
            return data.astype(np.float32), samplerate
        except Exception:
            pass
    if HAS_SOUNDFILE:
        try:
            buffer = io.BytesIO(bytes_data)
            data, samplerate = sf.read(buffer)
            if data.ndim > 1: data = np.mean(data, axis=1)
            return data.astype(np.float32), samplerate
        except Exception:
            pass
    if HAS_PYDUB:
        try:
            buffer = io.BytesIO(bytes_data)
            sound = AudioSegment.from_file(buffer)
            samplerate = sound.frame_rate
            samples = np.array(sound.get_array_of_samples())
            if sound.channels > 1: samples = samples.reshape((-1, sound.channels)).mean(axis=1)
            return (samples.astype(np.float32) / (2 ** (sound.sample_width * 8 - 1))), samplerate
        except Exception:
            pass
    try:
        buffer = io.BytesIO(bytes_data)
        samplerate, data = wavfile.read(buffer)
        if data.ndim > 1: data = np.mean(data, axis=1)
        if data.dtype == np.int16: data = data / 32768.0
        elif data.dtype == np.int32: data = data / 2147483648.0
        return data.astype(np.float32), samplerate
    except Exception:
        pass
    st.error("⚠️ تعذر فك تشفير الصوت. يرجى استخدام ملف صالحة (MP3, WAV, M4A, OGG).")
    return None, None

def generate_synthetic_audio(fault_type="bearing_wear", sr=22050, duration=3.0):
    t = np.linspace(0, duration, int(sr * duration))
    base = 0.2 * np.sin(2 * np.pi * 50 * t)
    f_sig = 0.45 * np.sin(2 * np.pi * 180 * t) if fault_type == "bearing_wear" else (0.5 * np.sin(2 * np.pi * 3200 * t) if fault_type == "turbo_shaft" else 0.0)
    return (base + f_sig + np.random.normal(0, 0.02, len(t))).astype(np.float32), sr

# ==========================================
# 5. محرك التشخيص
# ==========================================
def run_diagnostic(audio_data, sample_rate, unit_key):
    unit = UNIVERSAL_DATABASE[unit_key]
    rms_energy = float(np.sqrt(np.mean(audio_data**2)))
    fft_vals = np.abs(np.fft.rfft(audio_data))
    fft_freqs = np.fft.rfftfreq(len(audio_data), 1.0 / sample_rate)

    total_power = np.sum(fft_vals)
    spectral_centroid = float(np.sum(fft_freqs * fft_vals) / total_power) if total_power > 0 else 0.0
    peak_freq = float(fft_freqs[np.argmax(fft_vals)])

    bands, names = unit["bands"], unit.get("names", {})
    detected_faults, component_img, fault_type_key, health_score = [], COMPONENT_IMAGES["healthy"], "سليم (Healthy)", 100

    if "bearing_wear" in bands and bands["bearing_wear"][0] <= peak_freq <= bands["bearing_wear"][1]:
        detected_faults.append(f"تآكل في {names.get('bearing_wear', 'محامل الكرنك')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES.get("motor_bearings", COMPONENT_IMAGES["bearings"]), "Bearing Wear / السبيكة والمحامل", 42
    elif "compressor_valves" in bands and bands["compressor_valves"][0] <= peak_freq <= bands["compressor_valves"][1]:
        detected_faults.append(f"انحراف في {names.get('compressor_valves', 'صمامات الضاغط')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["compressor_valves"], "Compressor Valves / صمامات الضاغط", 38
    elif "belt_squeal" in bands and bands["belt_squeal"][0] <= peak_freq <= bands["belt_squeal"][1]:
        detected_faults.append(f"انزلاق في {names.get('belt_squeal', 'سير الحركة')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["belt"], "Drive Belt / سير الحركة", 65
    elif "valve_clearance" in bands and bands["valve_clearance"][0] <= peak_freq <= bands["valve_clearance"][1]:
        detected_faults.append(f"اتساع خلوص {names.get('valve_clearance', 'صمامات المحرك')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["valves"], "Valvetrain / صمامات المحرك", 50
    elif "injector_clatter" in bands and bands["injector_clatter"][0] <= peak_freq <= bands["injector_clatter"][1]:
        detected_faults.append(f"تفاوت ضغط {names.get('injector_clatter', 'بخاخات الوقود')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["injectors"], "Fuel Injectors / البخاخات", 45
    elif unit["has_turbo"] and "turbo_shaft" in bands and bands["turbo_shaft"][0] <= peak_freq <= bands["turbo_shaft"][1]:
        detected_faults.append(f"احتراق/احتكاك {names.get('turbo_shaft', 'عمود التيربو')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["turbo"], "Turbocharger Shaft / عمود التيربو", 25

    return {
        "target_unit": f"{unit['brand']} {unit['model']}", "category": unit["category"], "specs": unit["specs"],
        "unit_image": unit["unit_image"], "component_image": component_img, "fault_type_key": fault_type_key,
        "status_text": "Critical / يلزم الصيانة" if detected_faults else "Healthy / أداء منتظم",
        "status_class": "status-critical" if detected_faults else "status-healthy",
        "health_score": health_score, "peak_freq": round(peak_freq, 2), "centroid": round(spectral_centroid, 2),
        "rms": round(rms_energy, 5), "detected_faults": detected_faults if detected_faults else ["لا يوجد انحرافات طيفية"],
        "recommendations": f"تم رصد خلل طيفي عند تردد ({peak_freq:.1f} Hz) يقتضي الفحص المباشر." if detected_faults else "الوحدة تعمل بكفاءة طبيعية.",
        "fft_freqs": fft_freqs, "fft_vals": fft_vals
    }

# ==========================================
# 6. الواجهة الرئيسية
# ==========================================
st.markdown(f'<div style="text-align: center;"><h1 class="theme-header">⚡ ZINO EADE</h1><p style="color: #8b949e;">Universal Edge Acoustic Diagnostic Workstation</p></div>', unsafe_allow_html=True)

st.markdown("### 🎯 اختر القطاع المطلوب فدحصه:")
cols = st.columns(4)
for idx, (cat, t_info) in enumerate(THEMES.items()):
    is_act = (cat == current_cat)
    with cols[idx]:
        st.markdown(f'<div style="background: rgba(22, 27, 34, 0.9); border: 2px solid {t_info["color"] if is_act else "#30363d"}; border-radius: 12px; padding: 12px; text-align: center; box-shadow: 0 4px 15px {t_info["glow"] if is_act else "transparent"};"><h3 style="color: {t_info["color"]} !important; margin:0;">{t_info["icon"]} {cat}</h3></div>', unsafe_allow_html=True)
        if st.button(f"اختيار {t_info['icon']}", key=f"btn_{idx}"):
            st.session_state["selected_category"] = cat
            st.rerun()

st.markdown("---")
filtered_units = {k: v for k, v in UNIVERSAL_DATABASE.items() if v["category"] == current_cat}

st.sidebar.markdown(f"<h3 style='color: {theme['color']}'>{theme['icon']} {current_cat}</h3>", unsafe_allow_html=True)
selected_unit = st.sidebar.selectbox("اختر الطراز والمحرك:", list(filtered_units.keys()))
source_mode = st.sidebar.radio("مصدر الصوت:", ("رفع ملف صوتي (MP3, WAV, M4A)", "محاكي الموجات الهندسي"))

audio_file, synthetic_fault = None, "bearing_wear"
if source_mode == "رفع ملف صوتي (MP3, WAV, M4A)":
    audio_file = st.sidebar.file_uploader("ارفع الصوت:", type=["wav", "mp3", "m4a", "ogg", "flac"])
else:
    synthetic_fault = st.sidebar.selectbox("نمط الخلل المحاكى:", ["bearing_wear", "turbo_shaft", "healthy"])

if st.sidebar.button("🚀 بدء المسح والتشخيص المباشر"):
    audio_data, sample_rate = None, 22050
    if source_mode == "رفع ملف صوتي (MP3, WAV, M4A)":
        if audio_file is not None:
            audio_data, sample_rate = read_any_audio(audio_file)
        else:
            st.warning("⚠️ يرجى رفع ملف صوتي أولاً.")
    else:
        audio_data, sample_rate = generate_synthetic_audio(synthetic_fault)

    if audio_data is not None:
        res = run_diagnostic(audio_data, sample_rate, selected_unit)
        tab1, tab2, tab3, tab4 = st.tabs(["📷 المسح البصري", "📈 التحليل الطيفي (FFT)", "🔧 التوصيات والقطع", "📑 التقرير الشامل"])

        with tab1:
            c1, c2 = st.columns(2)
            c1.markdown(f"#### ⚙️ وحدة الفحص: {res['target_unit']}")
            c1.image(res["unit_image"], use_container_width=True)
            c2.markdown(f"#### 🎯 القطعة المحددة: {res['fault_type_key']}")
            c2.image(res["component_image"], use_container_width=True)
            st.markdown("---")
            m1, m2, m3, m4 = st.columns(4)
            m1.markdown(f'<div class="metric-card"><small>حالة الأداء</small><br><span class="{res["status_class"]}">{res["status_text"]}</span></div>', unsafe_allow_html=True)
            m2.markdown(f'<div class="metric-card"><small>مؤشر السلامة</small><h2 style="color:{theme["color"]};margin:0">{res["health_score"]}%</h2></div>', unsafe_allow_html=True)
            m3.markdown(f'<div class="metric-card"><small>Peak Freq</small><h2 style="margin:0">{res["peak_freq"]} Hz</h2></div>', unsafe_allow_html=True)
            m4.markdown(f'<div class="metric-card"><small>Centroid</small><h2 style="margin:0">{res["centroid"]} Hz</h2></div>', unsafe_allow_html=True)

        with tab2:
            fig = go.Figure()
            mask = res["fft_freqs"] <= 8000
            fig.add_trace(go.Scatter(x=res["fft_freqs"][mask], y=res["fft_vals"][mask], mode="lines", line=dict(color=theme["color"], width=2)))
            fig.update_layout(template="plotly_dark", xaxis_title="Frequency (Hz)", yaxis_title="Amplitude Density")
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.info(res["recommendations"])
            for f in res["detected_faults"]: st.write(f"• **{f}**")

        with tab4:
            report_text = f"""==================================================
ZINO EADE ACOUSTIC DIAGNOSTIC INSPECTION REPORT
==================================================
Target Unit       : {res['target_unit']}
Engineering Class : {res['category']}
Specification     : {res['specs']}
Health Status     : {res['status_text']}
Health Index      : {res['health_score']}%
--------------------------------------------------
ACOUSTIC SPECTRAL METRICS:
Dominant Peak Freq: {res['peak_freq']} Hz
Spectral Centroid : {res['centroid']} Hz
Signal RMS Energy : {res['rms']} RMS Density
--------------------------------------------------
DETECTED COMPONENT FAULTS:
{chr(10).join(['- ' + f for f in res['detected_faults']])}
==================================================
"""
            st.code(report_text, language="text")
            st.download_button("📥 تحميل التقرير (TXT)", report_text, file_name="ZINO_EADE_Report.txt")
