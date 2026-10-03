import io
import json
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.io.wavfile as wavfile
import scipy.signal as signal
import streamlit as st

# ==========================================
# 0. استدعاء آمن لمكتبات قراءة الصوت والرسوم
# ==========================================
HAS_LIBROSA = False
try:
    import librosa

    HAS_LIBROSA = True
except ImportError:
    pass

HAS_SOUNDFILE = False
try:
    import soundfile as sf

    HAS_SOUNDFILE = True
except ImportError:
    pass

HAS_PYDUB = False
try:
    from pydub import AudioSegment

    HAS_PYDUB = True
except ImportError:
    pass

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="ZINO EADE - Universal Acoustic Diagnostic Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 1. تصميم CSS هندسي عالي الجودة (Cyberpunk UI)
# ==========================================
st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
        color: #c9d1d9;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .metric-card {
        background: rgba(22, 27, 34, 0.85);
        border: 1px solid rgba(48, 54, 61, 0.9);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        margin-bottom: 15px;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: #58a6ff;
    }

    .status-badge-healthy {
        background: rgba(46, 160, 67, 0.2);
        color: #3fb950;
        border: 1px solid #2ea043;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1rem;
        display: inline-block;
        box-shadow: 0 0 15px rgba(63, 185, 80, 0.3);
    }
    .status-badge-critical {
        background: rgba(248, 81, 73, 0.2);
        color: #f85149;
        border: 1px solid #da3633;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1rem;
        display: inline-block;
        box-shadow: 0 0 15px rgba(248, 81, 73, 0.3);
    }
    .status-badge-warning {
        background: rgba(210, 153, 34, 0.2);
        color: #d29922;
        border: 1px solid #bb8009;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1rem;
        display: inline-block;
        box-shadow: 0 0 15px rgba(210, 153, 34, 0.3);
    }

    .stButton>button {
        background: linear-gradient(90deg, #1f6beb 0%, #238636 100%);
        color: #ffffff;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 12px 28px;
        font-size: 1.05rem;
        box-shadow: 0 0 20px rgba(31, 107, 235, 0.5);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px rgba(35, 134, 54, 0.8);
        transform: scale(1.02);
    }
    
    h1, h2, h3, h4 {
        color: #f0f6fc !important;
        font-weight: 700;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(22, 27, 34, 0.6);
        border-radius: 8px 8px 0px 0px;
        color: #8b949e;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f6beb !important;
        color: #ffffff !important;
        font-weight: bold;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. صور المكونات والأجزاء الميكانيكية
# ==========================================
COMPONENT_IMAGES = {
    "injectors": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=600&auto=format&fit=crop&q=80",
    "turbo": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=600&auto=format&fit=crop&q=80",
    "bearings": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=600&auto=format&fit=crop&q=80",
    "valves": "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=600&auto=format&fit=crop&q=80",
    "belt": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&auto=format&fit=crop&q=80",
    "compressor_valves": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=600&auto=format&fit=crop&q=80",
    "motor_bearings": "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=600&auto=format&fit=crop&q=80",
    "motor_brushes": "https://images.unsplash.com/photo-1581092335397-9583fe92d232?w=600&auto=format&fit=crop&q=80",
    "pump_impeller": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&auto=format&fit=crop&q=80",
    "healthy": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=600&auto=format&fit=crop&q=80",
}

# ==========================================
# 3. قاعدة البيانات العالمية الشاملة (Universal Database)
# ==========================================
UNIVERSAL_DATABASE = {
    # ------------------ أجهزة منزلية وصناعية ------------------
    "ضاغط ثلاجة (Inverter Refrigerator Compressor)": {
        "category": "Household & HVAC",
        "brand": "LG / General Electric",
        "model": "Smart Inverter R600a Compressor",
        "specs": "Variable Speed Hermetic Reciprocating Unit",
        "has_turbo": False,
        "unit_image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&auto=format&fit=crop&q=80",
        "bands": {
            "bearing_wear": (20, 280),
            "compressor_valves": (850, 2400),
            "motor_vibration": (40, 150),
        },
        "component_names": {
            "bearing_wear": "محامل الكرنك والضاغط (Crank Bearings)",
            "compressor_valves": "صمامات الضاغط الداخلية (Reed Valves)",
            "motor_vibration": "اختلال اتزان ملفات المحرك (Stator Coil)",
        },
    },
    "محرك غسالة ملابس (Washing Machine Direct Drive)": {
        "category": "Household & HVAC",
        "brand": "Samsung / Bosch",
        "model": "Inverter Direct Drive BLDC Motor",
        "specs": "Brushless DC Motor / Belt Drive Assembly",
        "has_turbo": False,
        "unit_image": "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=800&auto=format&fit=crop&q=80",
        "bands": {
            "bearing_wear": (30, 320),
            "motor_brushes": (1200, 3600),
            "belt_squeal": (700, 1900),
        },
        "component_names": {
            "bearing_wear": "محامل الحلة والمحرك (Drum Bearings)",
            "motor_brushes": "فحمات التلامس الكهربائي (Carbon Brushes)",
            "belt_squeal": "قشاط / سير الحركة (Drive Belt)",
        },
    },
    "مضخة مياه كهربائية (Electric Water Pump 2HP)": {
        "category": "Household & HVAC",
        "brand": "Pedrollo / Grundfos",
        "model": "CPM-158 Centrifugal Water Pump",
        "specs": "2.0 HP Single-Phase Induction Motor",
        "has_turbo": False,
        "unit_image": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format&fit=crop&q=80",
        "bands": {
            "bearing_wear": (20, 260),
            "pump_impeller": (900, 2700),
            "cavitation": (3200, 7500),
        },
        "component_names": {
            "bearing_wear": "محامل المحرك الكهربائي (Motor Bearings)",
            "pump_impeller": "عنفة / فراشة المضخة (Pump Impeller)",
            "cavitation": "تكفف الماء والاحتكاك الطيفي (Cavitation Noise)",
        },
    },
    "محرك حثي صناعي (Industrial 3-Phase AC Motor 15kW)": {
        "category": "Industrial Automation",
        "brand": "Siemens / ABB",
        "model": "1LE1 Severe Duty Industrial Motor",
        "specs": "15 kW / 400V 3-Phase 50Hz Heavy Unit",
        "has_turbo": False,
        "unit_image": "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=800&auto=format&fit=crop&q=80",
        "bands": {
            "bearing_wear": (20, 300),
            "rotor_unbalance": (40, 120),
            "stator_fault": (1000, 3200),
        },
        "component_names": {
            "bearing_wear": "محامل الدوران الأمامية والخلفية (Drive Bearings)",
            "rotor_unbalance": "اختلال اتزان الدوار (Rotor Unbalance)",
            "stator_fault": "ترددات الملفات الثابتة (Stator Winding Fault)",
        },
    },
    # ------------------ معدات ثقيلة وزراعية ------------------
    "محرك حفار JCB (JCB EcoMAX 4.4L Turbo)": {
        "category": "Heavy Machinery",
        "brand": "JCB Construction Equipment",
        "model": "EcoMAX 444 Heavy Diesel Engine",
        "specs": "4.4L Turbocharged Direct Injection Unit",
        "has_turbo": True,
        "unit_image": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=800&auto=format&fit=crop&q=80",
        "bands": {
            "bearing_wear": (20, 280),
            "turbo_shaft": (1400, 4800),
            "injector_clatter": (2200, 7500),
        },
        "component_names": {
            "bearing_wear": "سبيكة العمود الفقري والكرنك (Main Bearings)",
            "turbo_shaft": "عمود شاحن التيربو (Turbocharger Shaft)",
            "injector_clatter": "بخاخات الديزل الضغط العالي (Common Rail Injectors)",
        },
    },
    "جرار زراعي (John Deere 6M Heavy Tractor)": {
        "category": "Heavy Machinery",
        "brand": "John Deere Agriculture",
        "model": "6M PowerTech Diesel Engine",
        "specs": "6.8L 6-Cylinder Heavy Duty Diesel",
        "has_turbo": True,
        "unit_image": "https://images.unsplash.com/photo-1592838064575-70ed626d3a0e?w=800&auto=format&fit=crop&q=80",
        "bands": {
            "bearing_wear": (20, 250),
            "valve_clearance": (900, 2500),
            "injector_clatter": (2500, 7200),
        },
        "component_names": {
            "bearing_wear": "سبيكة محامل الكرنك (Crank Bearings)",
            "valve_clearance": "خلوص صمامات الديزل (Valvetrain Clearance)",
            "injector_clatter": "بخاخات الوقود المباشرة (Direct Fuel Injectors)",
        },
    },
    # ------------------ سيارات ومركبات ------------------
    "VW Caddy 1.6 TDI (تنفس طبيعي / بدون تيربو)": {
        "category": "Automotive Passenger",
        "brand": "Volkswagen",
        "model": "Caddy (1.6L TDI NA)",
        "specs": "1.6L TDI Naturally Aspirated (Common Rail)",
        "has_turbo": False,
        "unit_image": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=800&auto=format&fit=crop&q=80",
        "bands": {
            "bearing_wear": (20, 350),
            "belt_squeal": (700, 2000),
            "valve_clearance": (1000, 2800),
            "injector_clatter": (3000, 8000),
        },
        "component_names": {
            "bearing_wear": "سبيكة محامل الكرنك (Engine Crank Bearings)",
            "belt_squeal": "قشاط المجموعات والمكواة (Serpentine Belt)",
            "valve_clearance": "تاكيهات وصمامات المحرك (Engine Valves)",
            "injector_clatter": "بخاخات الديزل (CRDi Fuel Injectors)",
        },
    },
    "VW Caddy 1.6 TDI (شاحن تيربو)": {
        "category": "Automotive Passenger",
        "brand": "Volkswagen",
        "model": "Caddy (1.6L TDI Turbo)",
        "specs": "1.6L TDI Turbocharged Engine",
        "has_turbo": True,
        "unit_image": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=800&auto=format&fit=crop&q=80",
        "bands": {
            "bearing_wear": (20, 350),
            "turbo_shaft": (1500, 5500),
            "valve_clearance": (1000, 2800),
            "injector_clatter": (3000, 8000),
        },
        "component_names": {
            "bearing_wear": "سبيكة الكرنك (Crank Bearings)",
            "turbo_shaft": "مروحة وعمود التيربو (Turbocharger Shaft)",
            "valve_clearance": "صمامات المحرك (Valvetrain)",
            "injector_clatter": "بخاخات الوقود (Injectors)",
        },
    },
    "Hyundai Santa Fe 2.2 CRDi (تيربو ديزل)": {
        "category": "Automotive Passenger",
        "brand": "Hyundai",
        "model": "Santa Fe 2.2L CRDi",
        "specs": "2.2L CRDi VGT Turbo Diesel Engine",
        "has_turbo": True,
        "unit_image": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=800&auto=format&fit=crop&q=80",
        "bands": {
            "bearing_wear": (20, 300),
            "turbo_shaft": (1500, 5000),
            "injector_clatter": (2500, 8000),
        },
        "component_names": {
            "bearing_wear": "سبيكة الكرنك والسلندر (Engine Bearings)",
            "turbo_shaft": "عمود شاحن التيربو (Turbocharger Assembly)",
            "injector_clatter": "بخاخات الديزل الضغط العالي (CRDi Injectors)",
        },
    },
    "Honda Civic 1.5 Turbo (بنزين)": {
        "category": "Automotive Passenger",
        "brand": "Honda",
        "model": "Civic 1.5 VTEC Turbo",
        "specs": "1.5L Earth Dreams Direct Injection Turbo",
        "has_turbo": True,
        "unit_image": "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=800&auto=format&fit=crop&q=80",
        "bands": {
            "bearing_wear": (30, 320),
            "turbo_shaft": (1600, 5200),
            "injector_clatter": (3200, 8500),
        },
        "component_names": {
            "bearing_wear": "سبيكة محامل الكرنك (Crankshaft Bearings)",
            "turbo_shaft": "عمود التيربو (VTEC Turbo Shaft)",
            "injector_clatter": "بخاخات الحقن المباشر (GDI Injectors)",
        },
    },
    "Toyota Corolla 1.6L (بنزين - بدون تيربو)": {
        "category": "Automotive Passenger",
        "brand": "Toyota",
        "model": "Corolla 1.6 VVT-i",
        "specs": "1.6L Dual VVT-i Naturally Aspirated",
        "has_turbo": False,
        "unit_image": "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800&auto=format&fit=crop&q=80",
        "bands": {
            "bearing_wear": (30, 350),
            "belt_squeal": (800, 2000),
            "valve_clearance": (1000, 3200),
        },
        "component_names": {
            "bearing_wear": "سبيكة الكرنك (Crankshaft Bearings)",
            "belt_squeal": "قشاط الدينامو والمجموعات (Drive Belt)",
            "valve_clearance": "نظام صمامات VVT-i (Valvetrain Clearance)",
        },
    },
}


# ==========================================
# 4. دالة معالجة الصوت وقراءته بآمان
# ==========================================
def read_audio_safely(uploaded_file):
    """تقرأ كافة أشكال ملفات الصوت بطرق آمنة متدرجة تمنع الأخطاء تماماً"""
    bytes_data = uploaded_file.read()

    # 1. Librosa
    if HAS_LIBROSA:
        try:
            buffer = io.BytesIO(bytes_data)
            data, samplerate = librosa.load(buffer, sr=None, mono=True)
            return data.astype(np.float32), samplerate
        except Exception:
            pass

    # 2. Soundfile
    if HAS_SOUNDFILE:
        try:
            buffer = io.BytesIO(bytes_data)
            data, samplerate = sf.read(buffer)
            if data.ndim > 1:
                data = np.mean(data, axis=1)
            return data.astype(np.float32), samplerate
        except Exception:
            pass

    # 3. Pydub
    if HAS_PYDUB:
        try:
            buffer = io.BytesIO(bytes_data)
            sound = AudioSegment.from_file(buffer)
            samplerate = sound.frame_rate
            samples = np.array(sound.get_array_of_samples())
            if sound.channels > 1:
                samples = samples.reshape((-1, sound.channels)).mean(axis=1)
            data = samples.astype(np.float32) / (
                2 ** (sound.sample_width * 8 - 1)
            )
            return data, samplerate
        except Exception:
            pass

    # 4. Fallback SciPy WAV
    try:
        buffer = io.BytesIO(bytes_data)
        samplerate, data = wavfile.read(buffer)
        if data.ndim > 1:
            data = np.mean(data, axis=1)
        if data.dtype == np.int16:
            data = data / 32768.0
        elif data.dtype == np.int32:
            data = data / 2147483648.0
        return data.astype(np.float32), samplerate
    except Exception:
        pass

    st.error(
        "⚠️ تعذر فك تشفير ترميز الملف الصوتي. يرجى رفع ملف WAV أو MP3 معيارياً."
    )
    return None, None


def generate_synthetic_audio(fault_type="bearing_wear", sr=22050, duration=3.0):
    """توليد موجات صوتية هندسية لاختبار المنظومة"""
    t = np.linspace(0, duration, int(sr * duration))
    base_engine_hum = 0.2 * np.sin(2 * np.pi * 50 * t) + 0.1 * np.sin(
        2 * np.pi * 100 * t
    )

    if fault_type == "bearing_wear":
        fault_signal = 0.45 * np.sin(2 * np.pi * 180 * t)
    elif fault_type == "turbo_shaft":
        fault_signal = 0.5 * np.sin(2 * np.pi * 3200 * t)
    elif fault_type == "injector_clatter":
        fault_signal = 0.4 * np.sin(2 * np.pi * 4800 * t)
    elif fault_type == "valve_clearance":
        fault_signal = 0.35 * np.sin(2 * np.pi * 1800 * t)
    else:
        fault_signal = 0.0

    noise = np.random.normal(0, 0.02, len(t))
    synthetic_signal = base_engine_hum + fault_signal + noise
    return synthetic_signal.astype(np.float32), sr


# ==========================================
# 5. محرك التشخيص الطيفي والهندسي الأساسي
# ==========================================
def run_full_diagnostic(audio_data, sample_rate, selected_unit_key):
    unit = UNIVERSAL_DATABASE[selected_unit_key]

    # 1. حساب RMS
    rms_energy = float(np.sqrt(np.mean(audio_data**2)))

    # 2. حساب FFT
    fft_vals = np.abs(np.fft.rfft(audio_data))
    fft_freqs = np.fft.rfftfreq(len(audio_data), 1.0 / sample_rate)

    total_power = np.sum(fft_vals)
    spectral_centroid = (
        float(np.sum(fft_freqs * fft_vals) / total_power)
        if total_power > 0
        else 0.0
    )

    peak_idx = np.argmax(fft_vals)
    peak_freq = float(fft_freqs[peak_idx])

    # 3. المطابقة مع النطاقات المسموحة
    bands = unit["bands"]
    component_names = unit.get("component_names", {})

    detected_faults = []
    fault_type_key = "سليم (Healthy)"
    component_img = COMPONENT_IMAGES["healthy"]
    health_score = 100

    # فحص السبيكة والمحامل
    if (
        "bearing_wear" in bands
        and bands["bearing_wear"][0] <= peak_freq <= bands["bearing_wear"][1]
    ):
        name_str = component_names.get(
            "bearing_wear", "محامل الكرنك (Bearings Wear)"
        )
        detected_faults.append(f"تآكل في {name_str}")
        component_img = COMPONENT_IMAGES.get(
            "motor_bearings", COMPONENT_IMAGES["bearings"]
        )
        fault_type_key = "Bearing Wear / السبيكة والمحامل"
        health_score = 42

    # فحص صمامات الضواغط
    elif (
        "compressor_valves" in bands
        and bands["compressor_valves"][0]
        <= peak_freq
        <= bands["compressor_valves"][1]
    ):
        name_str = component_names.get(
            "compressor_valves", "صمامات الضاغط (Reed Valves)"
        )
        detected_faults.append(f"انحراف في {name_str}")
        component_img = COMPONENT_IMAGES["compressor_valves"]
        fault_type_key = "Compressor Reed Valves / صمامات الضاغط"
        health_score = 38

    # فحص فحمات المحركات
    elif (
        "motor_brushes" in bands
        and bands["motor_brushes"][0]
        <= peak_freq
        <= bands["motor_brushes"][1]
    ):
        name_str = component_names.get(
            "motor_brushes", "فحمات التلامس (Carbon Brushes)"
        )
        detected_faults.append(f"تآكل في {name_str}")
        component_img = COMPONENT_IMAGES["motor_brushes"]
        fault_type_key = "Carbon Brushes / فحمات المحرك"
        health_score = 55

    # فحص عنفة المضخات
    elif (
        "pump_impeller" in bands
        and bands["pump_impeller"][0]
        <= peak_freq
        <= bands["pump_impeller"][1]
    ):
        name_str = component_names.get(
            "pump_impeller", "عنفة المضخة (Impeller)"
        )
        detected_faults.append(f"احتكاك في {name_str}")
        component_img = COM
