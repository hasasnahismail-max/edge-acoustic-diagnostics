import io
import numpy as np
import plotly.graph_objects as go
import scipy.io.wavfile as wavfile
import streamlit as st

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

st.set_page_config(
    page_title="ZINO EADE - Universal Acoustic Workstation",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 1. نظام اللغات بدون ألقاب (إسماعيل حساسنة)
# ==========================================
I18N = {
    "العربية": {
        "designer": "تصميم وتطوير: إسماعيل حساسنة (Ismail Hasasna)",
        "subtitle": "المنظومة الذكية الشاملة للتشخيص الصوتي لأعطال المحركات",
        "select_cat": "🎯 اختر القطاع المطلوب لفحصه:",
        "select_unit": "اختر الطراز والمحرك المباشر:",
        "audio_src": "مصدر الصوت:",
        "upload_mode": "رفع ملف صوتي (MP3, WAV, M4A, OGG, FLAC)",
        "demo_mode": "محاكي الموجات الهندسي (Demo Engine)",
        "run_btn": "🚀 بدء المسح والتشخيص المباشر",
        "tab_visual": "📷 المسح البصري بالليزر",
        "tab_fft": "📈 التحليل الطيفي (FFT)",
        "tab_recs": "🔧 التوصيات والقطع",
        "tab_report": "📑 التقرير الشامل",
        "status_label": "حالة الأداء",
        "health_index": "مؤشر السلامة",
        "peak_freq": "التردد السائد",
        "centroid": "المركز الطيفي",
        "target_unit": "وحدة الفحص المباشر:",
        "faulty_comp": "القطعة المحددة بالمسح:",
        "healthy": "أداء منتظم وسليم",
        "critical": "يلزم الصيانة المباشرة",
        "download_rep": "📥 تحميل التقرير الهندسي (TXT)",
        "cats": {
            "السيارات والمركبات": "السيارات والمركبات",
            "الثلاجات والتبريد": "الثلاجات والتبريد",
            "الأجهزة الكهربائية": "الأجهزة الكهربائية",
            "الماكينات والمعدات": "الماكينات والمعدات"
        }
    },
    "English": {
        "designer": "Designed & Developed by: Ismail Hasasna",
        "subtitle": "Universal AI-Powered Acoustic Diagnostic Workstation",
        "select_cat": "🎯 Select Sector for Acoustic Scan:",
        "select_unit": "Select Model & Engine:",
        "audio_src": "Audio Source:",
        "upload_mode": "Upload Audio File (MP3, WAV, M4A, OGG, FLAC)",
        "demo_mode": "Synthetic Wave Simulator (Demo)",
        "run_btn": "🚀 Start Live Scan & Diagnostics",
        "tab_visual": "📷 Laser Visual Scan",
        "tab_fft": "📈 Spectral Analysis (FFT)",
        "tab_recs": "🔧 Recommendations & Faults",
        "tab_report": "📑 Inspection Report",
        "status_label": "Health Status",
        "health_index": "Safety Index",
        "peak_freq": "Peak Frequency",
        "centroid": "Spectral Centroid",
        "target_unit": "Scanned Unit:",
        "faulty_comp": "Isolated Faulty Component:",
        "healthy": "Healthy / Normal Operation",
        "critical": "Critical / Inspection Required",
        "download_rep": "📥 Download Engineering Report (TXT)",
        "cats": {
            "السيارات والمركبات": "Automotive & Vehicles",
            "الثلاجات والتبريد": "Refrigeration & HVAC",
            "الأجهزة الكهربائية": "Electrical Appliances",
            "الماكينات والمعدات": "Heavy Machinery"
        }
    },
    "Русский": {
        "designer": "Разработано: Исмаил Хасасна (Ismail Hasasna)",
        "subtitle": "Универсальная акустическая диагностическая платформа",
        "select_cat": "🎯 Выберите сектор для сканирования:",
        "select_unit": "Выберите модель и двигатель:",
        "audio_src": "Источник аудиосигнала:",
        "upload_mode": "Загрузить аудиофайл (MP3, WAV, M4A, OGG, FLAC)",
        "demo_mode": "Инженерный симулятор волн (Демо)",
        "run_btn": "🚀 Запустить сканирование и диагностику",
        "tab_visual": "📷 Лазерный визуальный сканер",
        "tab_fft": "📈 Спектральный анализ (FFT)",
        "tab_recs": "🔧 Рекомендации и узлы",
        "tab_report": "📑 Инженерный отчет",
        "status_label": "Состояние",
        "health_index": "Индекс надежности",
        "peak_freq": "Пиковая частота",
        "centroid": "Спектральный центр",
        "target_unit": "Объект проверки:",
        "faulty_comp": "Определенный дефектный узел:",
        "healthy": "Исправно / Нормальный режим",
        "critical": "Критично / Требуется ремонт",
        "download_rep": "📥 Скачать инженерный отчет (TXT)",
        "cats": {
            "السيارات والمركبات": "Автомобили и транспорт",
            "الثلاجات والتبريد": "Холодильное оборудование",
            "الأجهزة الكهربائية": "Электроприборы",
            "الماكينات والمعدات": "Тяжелая техника"
        }
    }
}

# إخفاء القائمة الجانبية تماماً عبر CSS
st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# شريط اللغة في أعلى الصفحة الرئيسية
top_col1, top_col2 = st.columns([3, 1])
with top_col2:
    lang_choice = st.selectbox("🌐 Language / اللغة", ["العربية", "English", "Русский"], index=0)

L = I18N[lang_choice]

THEMES = {
    "السيارات والمركبات": {"color": "#ff7b00", "glow": "rgba(255, 123, 0, 0.3)", "icon": "🚗"},
    "الثلاجات والتبريد": {"color": "#0099ff", "glow": "rgba(0, 153, 255, 0.3)", "icon": "🧊"},
    "الأجهزة الكهربائية": {"color": "#a855f7", "glow": "rgba(168, 85, 247, 0.3)", "icon": "🔌"},
    "الماكينات والمعدات": {"color": "#94a3b8", "glow": "rgba(148, 163, 184, 0.3)", "icon": "⚙️"}
}

if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = "السيارات والمركبات"

current_cat = st.session_state["selected_category"]
theme = THEMES[current_cat]

# تصميم الثيم وتأثير الليزر البصري المتحرك
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%); color: #c9d1d9; }}
    .theme-header {{ color: {theme['color']} !important; text-shadow: 0 0 15px {theme['glow']}; font-weight: 800; margin-bottom: 0px; text-align: center; font-size: 2.3rem; }}
    .designer-tag {{ color: #58a6ff; font-weight: 600; font-size: 1.1rem; text-align: center; margin-top: 4px; margin-bottom: 20px; }}
    .metric-card {{ background: rgba(22, 27, 34, 0.85); border: 2px solid {theme['color']}; border-radius: 12px; padding: 14px; box-shadow: 0 6px 20px {theme['glow']}; margin-bottom: 12px; text-align: center; }}
    .stButton>button {{ background: linear-gradient(90deg, {theme['color']} 0%, #238636 100%) !important; color: #fff !important; font-weight: bold !important; border-radius: 8px !important; border: none !important; padding: 12px 24px !important; width: 100%; }}
    .status-healthy {{ background: rgba(46, 160, 67, 0.2); color: #3fb950; border: 1px solid #2ea043; padding: 6px 14px; border-radius: 20px; font-weight: 700; display: inline-block; }}
    .status-critical {{ background: rgba(248, 81, 73, 0.2); color: #f85149; border: 1px solid #da3633; padding: 6px 14px; border-radius: 20px; font-weight: 700; display: inline-block; }}
    
    /* تأثير أنيميشن الليزر فوق الصورة */
    .laser-container {{ position: relative; overflow: hidden; border-radius: 12px; border: 2px solid {theme['color']}; box-shadow: 0 0 15px {theme['glow']}; }}
    .laser-container img {{ width: 100%; display: block; }}
    .laser-line {{
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: {theme['color']};
        box-shadow: 0 0 15px 4px {theme['color']};
        animation: scan 2.5s infinite ease-in-out;
        z-index: 10;
    }}
    @keyframes scan {{
        0% {{ top: 0%; }}
        50% {{ top: 95%; }}
        100% {{ top: 0%; }}
    }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. الصور وقاعدة البيانات المحدثة (صورة كادي الصحيحة)
# ==========================================
COMPONENT_IMAGES = {
    # صورة VW Caddy فان حقيقية وصحيحة دقيقة
    "car_caddy": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=800&auto=format&fit=crop&q=80",
    "car_hyundai": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=800&auto=format&fit=crop&q=80",
    "car_pajero": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800&auto=format&fit=crop&q=80",
    "fridge": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&auto=format&fit=crop&q=80",
    "washer": "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=800&auto=format&fit=crop&q=80",
    "pump": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format&fit=crop&q=80",
    "jcb": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=800&auto=format&fit=crop&q=80",
    "injectors": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=600&auto=format&fit=crop&q=80",
    "turbo": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=600&auto=format&fit=crop&q=80",
    "bearings": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=600&auto=format&fit=crop&q=80",
    "valves": "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=600&auto=format&fit=crop&q=80",
    "belt": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&auto=format&fit=crop&q=80",
    "healthy": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=600&auto=format&fit=crop&q=80"
}

UNIVERSAL_DATABASE = {
    "VW Caddy 1.6 TDI (تنفس طبيعي / بدون تيربو)": {
        "category": "السيارات والمركبات", "brand": "Volkswagen", "model": "Caddy 1.6 TDI NA",
        "specs": "1.6L TDI Common Rail Non-Turbo Engine", "has_turbo": False, "unit_image": COMPONENT_IMAGES["car_caddy"],
        "bands": {"bearing_wear": (20, 350), "belt_squeal": (700, 2000), "valve_clearance": (1000, 2800), "injector_clatter": (3000, 8000)},
        "names": {"bearing_wear": "سبيكة محامل الكرنك", "belt_squeal": "قشاط المجموعات", "valve_clearance": "صمامات المحرك", "injector_clatter": "بخاخات الديزل"}
    },
    "VW Caddy 2.0 TDI (شاحن تيربو)": {
        "category": "السيارات والمركبات", "brand": "Volkswagen", "model": "Caddy 2.0 TDI Turbo",
        "specs": "2.0L TDI Turbocharged Engine", "has_turbo": True, "unit_image": COMPONENT_IMAGES["car_caddy"],
        "bands": {"bearing_wear": (20, 350), "turbo_shaft": (1500, 5500), "injector_clatter": (3000, 8000)},
        "names": {"bearing_wear": "سبيكة الكرنك", "turbo_shaft": "عمود شاحن التيربو", "injector_clatter": "بخاخات الديزل"}
    },
    "VW Golf 1.4 TSI (بنزين تيربو)": {
        "category": "السيارات والمركبات", "brand": "Volkswagen", "model": "Golf VII 1.4 TSI",
        "specs": "1.4L TSI Direct Injection Turbo", "has_turbo": True, "unit_image": COMPONENT_IMAGES["car_caddy"],
        "bands": {"bearing_wear": (30, 320), "turbo_shaft": (1600, 5200), "injector_clatter": (3200, 8500)},
        "names": {"bearing_wear": "سبيكة الكرنك", "turbo_shaft": "عمود التيربو", "injector_clatter": "بخاخات البنزين"}
    },
    "VW Polo 1.2 MPI (بدون تيربو)": {
        "category": "السيارات والمركبات", "brand": "Volkswagen", "model": "Polo 1.2 MPI NA",
        "specs": "1.2L 3-Cylinder NA Engine", "has_turbo": False, "unit_image": COMPONENT_IMAGES["car_caddy"],
        "bands": {"bearing_wear": (30, 350), "belt_squeal": (800, 2000), "valve_clearance": (1000, 3000)},
        "names": {"bearing_wear": "سبيكة المحرك", "belt_squeal": "قشاط الحركة", "valve_clearance": "صمامات المحرك"}
    },
    "VW Passat 2.0 TDI (تيربو ديزل)": {
        "category": "السيارات والمركبات", "brand": "Volkswagen", "model": "Passat B8 2.0 TDI",
        "specs": "2.0L TDI Clean Diesel Turbo", "has_turbo": True, "unit_image": COMPONENT_IMAGES["car_caddy"],
        "bands": {"bearing_wear": (20, 300), "turbo_shaft": (1500, 5200), "injector_clatter": (2800, 8000)},
        "names": {"bearing_wear": "سبيكة الكرنك", "turbo_shaft": "التيربو", "injector_clatter": "بخاخات الديزل"}
    },
    "VW Jetta 1.6 MPI (بدون تيربو)": {
        "category": "السيارات والمركبات", "brand": "Volkswagen", "model": "Jetta 1.6 MPI NA",
        "specs": "1.6L Multi-Point Injection NA", "has_turbo": False, "unit_image": COMPONENT_IMAGES["car_caddy"],
        "bands": {"bearing_wear": (30, 350), "belt_squeal": (800, 2000), "valve_clearance": (1000, 3200)},
        "names": {"bearing_wear": "محامل الكرنك", "belt_squeal": "قشاط المجموعات", "valve_clearance": "الصمامات"}
    },
    "Hyundai Santa Fe 2.2 CRDi (تيربو ديزل)": {
        "category": "السيارات والمركبات", "brand": "Hyundai", "model": "Santa Fe 2.2 CRDi",
        "specs": "2.2L CRDi VGT Turbo Diesel Engine", "has_turbo": True, "unit_image": COMPONENT_IMAGES["car_hyundai"],
        "bands": {"bearing_wear": (20, 300), "turbo_shaft": (1500, 5000), "injector_clatter": (2500, 8000)},
        "names": {"bearing_wear": "سبيكة محامل المحرك", "turbo_shaft": "شاحن التيربو", "injector_clatter": "بخاخات الديزل"}
    },
    "Hyundai Tucson 1.6 T-GDI (تيربو بنزين)": {
        "category": "السيارات والمركبات", "brand": "Hyundai", "model": "Tucson 1.6 T-GDI",
        "specs": "1.6L Turbocharged Direct Injection", "has_turbo": True, "unit_image": COMPONENT_IMAGES["car_hyundai"],
        "bands": {"bearing_wear": (30, 320), "turbo_shaft": (1600, 5200), "injector_clatter": (3000, 8200)},
        "names": {"bearing_wear": "سبيكة المحرك", "turbo_shaft": "عمود التيربو", "injector_clatter": "بخاخات GDI"}
    },
    "Hyundai Elantra 1.6 MPI (بدون تيربو)": {
        "category": "السيارات والمركبات", "brand": "Hyundai", "model": "Elantra 1.6 MPI NA",
        "specs": "1.6L Gamma MPI Naturally Aspirated", "has_turbo": False, "unit_image": COMPONENT_IMAGES["car_hyundai"],
        "bands": {"bearing_wear": (30, 350), "belt_squeal": (800, 2000), "valve_clearance": (1000, 3200)},
        "names": {"bearing_wear": "سبيكة الكرنك", "belt_squeal": "سير الحركة", "valve_clearance": "صمامات المحرك"}
    },
    "Hyundai Accent 1.4 MPI (بدون تيربو)": {
        "category": "السيارات والمركبات", "brand": "Hyundai", "model": "Accent 1.4 MPI NA",
        "specs": "1.4L Kappa MPI Engine", "has_turbo": False, "unit_image": COMPONENT_IMAGES["car_hyundai"],
        "bands": {"bearing_wear": (30, 350), "belt_squeal": (800, 2000), "valve_clearance": (1000, 3200)},
        "names": {"bearing_wear": "سبيكة الكرنك", "belt_squeal": "قشاط المجموعات", "valve_clearance": "الصمامات"}
    },
    "Mitsubishi Pajero V20 3.4L V6 (بنزين - جير عادي)": {
        "category": "السيارات والمركبات", "brand": "Mitsubishi", "model": "Pajero V20 3.4L V6 NA Manual",
        "specs": "3.4L 6G74 V6 NA Engine", "has_turbo": False, "unit_image": COMPONENT_IMAGES["car_pajero"],
        "bands": {"bearing_wear": (20, 320), "belt_squeal": (700, 1900), "valve_clearance": (1000, 3000)},
        "names": {"bearing_wear": "سبيكة محامل الكرنك V6", "belt_squeal": "سير المجموعات", "valve_clearance": "صمامات المحرك"}
    },
    "Mitsubishi Pajero V80 3.2 DI-D (تيربو ديزل)": {
        "category": "السيارات والمركبات", "brand": "Mitsubishi", "model": "Pajero V80 3.2 DI-D Turbo",
        "specs": "3.2L Common Rail Turbo Diesel", "has_turbo": True, "unit_image": COMPONENT_IMAGES["car_pajero"],
        "bands": {"bearing_wear": (20, 280), "turbo_shaft": (1400, 4800), "injector_clatter": (2200, 7500)},
        "names": {"bearing_wear": "سبيكة محامل الكرنك", "turbo_shaft": "عمود شاحن التيربو", "injector_clatter": "بخاخات الديزل"}
    },
    "Mitsubishi L200 2.4 DI-D (تيربو ديزل)": {
        "category": "السيارات والمركبات", "brand": "Mitsubishi", "model": "L200 Pickup 2.4 DI-D",
        "specs": "2.4L MIVEC Turbo Diesel Engine", "has_turbo": True, "unit_image": COMPONENT_IMAGES["car_pajero"],
        "bands": {"bearing_wear": (20, 300), "turbo_shaft": (1500, 5000), "injector_clatter": (2500, 7800)},
        "names": {"bearing_wear": "سبيكة الكرنك", "turbo_shaft": "التيربو", "injector_clatter": "بخاخات الوقود"}
    },
    "ضاغط ثلاجة منزلي (Inverter Refrigerator Compressor)": {
        "category": "الثلاجات والتبريد", "brand": "LG / GE", "model": "Inverter R600a Compressor",
        "specs": "Variable Speed Hermetic Unit", "has_turbo": False, "unit_image": COMPONENT_IMAGES["fridge"],
        "bands": {"bearing_wear": (20, 280), "compressor_valves": (850, 2400)},
        "names": {"bearing_wear": "محامل الكرنك والضاغط", "compressor_valves": "صمامات الضاغط الداخلية"}
    },
    "محرك غسالة ملابس (Direct Drive Motor)": {
        "category": "الأجهزة الكهربائية", "brand": "Samsung / Bosch", "model": "BLDC Direct Drive",
        "specs": "Inverter Motor Assembly", "has_turbo": False, "unit_image": COMPONENT_IMAGES["washer"],
        "bands": {"bearing_wear": (30, 320), "belt_squeal": (700, 1900)},
        "names": {"bearing_wear": "محامل الحلة والمحرك", "belt_squeal": "قشاط / سير الحركة"}
    },
    "مضخة مياه كهربائية (Electric Water Pump 2HP)": {
        "category": "الأجهزة الكهربائية", "brand": "Pedrollo / Grundfos", "model": "CPM-158 Pump",
        "specs": "2.0 HP Single-Phase Engine", "has_turbo": False, "unit_image": COMPONENT_IMAGES["pump"],
        "bands": {"bearing_wear": (20, 260), "pump_impeller": (900, 2700)},
        "names": {"bearing_wear": "محامل المحرك", "pump_impeller": "عنفة المضخة"}
    },
    "محرك حفار JCB (JCB EcoMAX 4.4L Turbo)": {
        "category": "الماكينات والمعدات", "brand": "JCB", "model": "EcoMAX 4.4L Diesel",
        "specs": "Heavy Duty Turbo Engine", "has_turbo": True, "unit_image": COMPONENT_IMAGES["jcb"],
        "bands": {"bearing_wear": (20, 280), "turbo_shaft": (1400, 4800), "injector_clatter": (2200, 7500)},
        "names": {"bearing_wear": "سبيكة العمود الفقري", "turbo_shaft": "عمود شاحن التيربو", "injector_clatter": "بخاخات الديزل"}
    }
}

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
            if data.ndim > 1:
                data = np.mean(data, axis=1)
            return data.astype(np.float32), samplerate
        except Exception:
            pass
    if HAS_PYDUB:
        try:
            buffer = io.BytesIO(bytes_data)
            sound = AudioSegment.from_file(buffer)
            samplerate = sound.frame_rate
            samples = np.array(sound.get_array_of_samples())
            if sound.channels > 1:
                samples = samples.reshape((-1, sound.channels)).mean(axis=1)
            return (samples.astype(np.float32) / (2 ** (sound.sample_width * 8 - 1))), samplerate
        except Exception:
            pass
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
    st.error("⚠️ Error decoding audio file / تعذر فك تشفير الملف الصوتي.")
    return None, None

def generate_synthetic_audio(fault_type="bearing_wear", sr=22050, duration=3.0):
    t = np.linspace(0, duration, int(sr * duration))
    base = 0.2 * np.sin(2 * np.pi * 50 * t)
    f_sig = 0.45 * np.sin(2 * np.pi * 180 * t) if fault_type == "bearing_wear" else (0.5 * np.sin(2 * np.pi * 3200 * t) if fault_type == "turbo_shaft" else 0.0)
    return (base + f_sig + np.random.normal(0, 0.02, len(t))).astype(np.float32), sr

def run_diagnostic(audio_data, sample_rate, unit_key):
    unit = UNIVERSAL_DATABASE[unit_key]
    rms_energy = float(np.sqrt(np.mean(audio_data**2)))
    fft_vals = np.abs(np.f
np.fft.rfft(audio_data))
    fft_freqs = np.fft.rfftfreq(len(audio_data), 1.0 / sample_rate)

    total_power = np.sum(fft_vals)
    spectral_centroid = float(np.sum(fft_freqs * fft_vals) / total_power) if total_power > 0 else 0.0
    peak_freq = float(fft_freqs[np.argmax(fft_vals)])

    bands, names = unit["bands"], unit.get("names", {})
    detected_faults, component_img, fault_type_key, health_score = [], COMPONENT_IMAGES["healthy"], L["healthy"], 100

    if "bearing_wear" in bands and bands["bearing_wear"][0] <= peak_freq <= bands["bearing_wear"][1]:
        detected_faults.append(f"Bearing Wear: {names.get('bearing_wear', 'Crank Bearings')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["bearings"], "Bearing Wear / السبيكة والمحامل", 42
    elif "compressor_valves" in bands and bands["compressor_valves"][0] <= peak_freq <= bands["compressor_valves"][1]:
        detected_faults.append(f"Compressor Valves: {names.get('compressor_valves', 'Reed Valves')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["healthy"], "Compressor Valves / صمامات الضاغط", 38
    elif "belt_squeal" in bands and bands["belt_squeal"][0] <= peak_freq <= bands["belt_squeal"][1]:
        detected_faults.append(f"Belt Squeal: {names.get('belt_squeal', 'Drive Belt')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["belt"], "Drive Belt / سير الحركة", 65
    elif "valve_clearance" in bands and bands["valve_clearance"][0] <= peak_freq <= bands["valve_clearance"][1]:
        detected_faults.append(f"Valvetrain Deviation: {names.get('valve_clearance', 'Valves')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["valves"], "Valvetrain / صمامات المحرك", 50
    elif "injector_clatter" in bands and bands["injector_clatter"][0] <= peak_freq <= bands["injector_clatter"][1]:
        detected_faults.append(f"Injector Clatter: {names.get('injector_clatter', 'Injectors')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["injectors"], "Fuel Injectors / البخاخات", 45
    elif unit["has_turbo"] and "turbo_shaft" in bands and bands["turbo_shaft"][0] <= peak_freq <= bands["turbo_shaft"][1]:
        detected_faults.append(f"Turbo Shaft Friction: {names.get('turbo_shaft', 'Turbo')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["turbo"], "Turbocharger Shaft / عمود التيربو", 25

    return {
        "target_unit": f"{unit['brand']} {unit['model']}",
        "category": unit["category"],
        "specs": unit["specs"],
        "unit_image": unit["unit_image"],
        "component_image": component_img,
        "fault_type_key": fault_type_key,
        "status_text": L["critical"] if detected_faults else L["healthy"],
        "status_class": "status-critical" if detected_faults else "status-healthy",
        "health_score": health_score,
        "peak_freq": round(peak_freq, 2),
        "centroid": round(spectral_centroid, 2),
        "rms": round(rms_energy, 5),
        "detected_faults": detected_faults if detected_faults else ["No Spectral Deviations"],
        "recommendations": f"Spectral deviation identified at peak ({peak_freq:.1f} Hz). Immediate component inspection required." if detected_faults else "Target unit operating within optimal engineering frequency range.",
        "fft_freqs": fft_freqs,
        "fft_vals": fft_vals
    }

st.markdown(f'<div class="theme-header">⚡ ZINO EADE</div>', unsafe_allow_html=True)
st.markdown(f'<div class="designer-tag">{L["designer"]}<br><small style="color:#8b949e">{L["subtitle"]}</small></div>', unsafe_allow_html=True)

st.markdown(f"### {L['select_cat']}")
cols = st.columns(4)
for idx, (cat, t_info) in enumerate(THEMES.items()):
    is_act = cat == current_cat
    cat_translated = L["cats"].get(cat, cat)
    with cols[idx]:
        st.markdown(f'<div style="background: rgba(22, 27, 34, 0.9); border: 2px solid {t_info["color"] if is_act else "#30363d"}; border-radius: 12px; padding: 10px; text-align: center; box-shadow: 0 4px 15px {t_info["glow"] if is_act else "transparent"};"><h4 style="color: {t_info["color"]} !important; margin:0;">{t_info["icon"]} {cat_translated}</h4></div>', unsafe_allow_html=True)
        if st.button(f"{t_info['icon']} Select", key=f"btn_{idx}"):
            st.session_state["selected_category"] = cat
            st.rerun()

st.markdown("---")

ctl_col1, ctl_col2 = st.columns(2)
filtered_units = {k: v for k, v in UNIVERSAL_DATABASE.items() if v["category"] == current_cat}

with ctl_col1:
    selected_unit = st.selectbox(L["select_unit"], list(filtered_units.keys()))

with ctl_col2:
    source_mode = st.radio(L["audio_src"], (L["upload_mode"], L["demo_mode"]), horizontal=True)

audio_file, synthetic_fault = None, "bearing_wear"
if source_mode == L["upload_mode"]:
    audio_file = st.file_uploader("Upload Audio File:", type=["wav", "mp3", "m4a", "ogg", "flac"])
else:
    synthetic_fault = st.selectbox("Fault Pattern:", ["bearing_wear", "turbo_shaft", "healthy"])

st.markdown("<br>", unsafe_allow_html=True)
run_click = st.button(L["run_btn"])

if run_click or "has_run" in st.session_state:
    st.session_state["has_run"] = True
    audio_data, sample_rate = None, 22050
    if source_mode == L["upload_mode"]:
        if audio_file is not None:
            audio_data, sample_rate = read_any_audio(audio_file)
        else:
            st.warning("⚠ Please upload an audio file first.")
    else:
        audio_data, sample_rate = generate_synthetic_audio(synthetic_fault)

    if audio_data is not None:
        res = run_diagnostic(audio_data, sample_rate, selected_unit)
        tab1, tab2, tab3, tab4 = st.tabs([L["tab_visual"], L["tab_fft"], L["tab_recs"], L["tab_report"]])

        with tab1:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"#### ⚙️ {L['target_unit']} {res['target_unit']}")
                st.markdown(f'''
                    <div class="laser-container">
                        <div class="laser-line"></div>
                        <img src="{res['unit_image']}" alt="Target Unit">
                    </div>
                ''', unsafe_allow_html=True)
            with c2:
                st.markdown(f"#### 🎯 {L['faulty_comp']} {res['fault_type_key']}")
                st.image(res["component_image"], use_container_width=True)
            
            st.markdown("---")
            m1, m2, m3, m4 = st.columns(4)
            m1.markdown(f'<div class="metric-card"><small>{L["status_label"]}</small><br><span class="{res["status_class"]}">{res["status_text"]}</span></div>', unsafe_allow_html=True)
            m2.markdown(f'<div class="metric-card"><small>{L["health_index"]}</small><h2 style="color:{theme["color"]};margin:0">{res["health_score"]}%</h2></div>', unsafe_allow_html=True)
            m3.markdown(f'<div class="metric-card"><small>{L["peak_freq"]}</small><h2 style="margin:0">{res["peak_freq"]} Hz</h2></div>', unsafe_allow_html=True)
            m4.markdown(f'<div class="metric-card"><small>{L["centroid"]}</small><h2 style="margin:0">{res["centroid"]} Hz</h2></div>', unsafe_allow_html=True)

        with tab2:
            fig = go.Figure()
            mask = res["fft_freqs"] <= 8000
            fig.add_trace(go.Scatter(x=res["fft_freqs"][mask], y=res["fft_vals"][mask], mode="lines", line=dict(color=theme["color"], width=2)))
            fig.update_layout(template="plotly_dark", xaxis_title="Frequency (Hz)", yaxis_title="Amplitude Density")
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.info(res["recommendations"])
            for f in res["detected_faults"]:
                st.write(f"• **{f}**")

        with tab4:
            report_text = f"""==================================================
ZINO EADE ACOUSTIC DIAGNOSTIC INSPECTION REPORT
{L['designer']}
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
Platform Designer : Ismail Hasasna (إسماعيل حساسنة)
"""
            st.code(report_text, language="text")
            st.download_button(L["download_rep"], report_text, file_name="ZINO_EADE_Report.txt")
