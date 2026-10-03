import io
import time
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
# 1. نظام اللغات والتوثيق (إسماعيل حساسنة)
# ==========================================
I18N = {
    "العربية": {
        "designer": "تصميم وتطوير: إسماعيل حساسنة (Ismail Hasasna)",
        "subtitle": "منظومة التشخيص الصوتي والطيفي الشاملة لأعطال المحركات والأنظمة الميكانيكية",
        "select_cat": "🎯 اختر الشركة أو القطاع الهندسي المطلوب:",
        "select_unit": "اختر موديل السيارة والطراز الهندسي للمحرك:",
        "audio_src": "مصدر الإشارة الصوتية:",
        "upload_mode": "رفع تسجيل صوتي (MP3, WAV, M4A, OGG, FLAC)",
        "demo_mode": "محاكي الإشارات والموجات (Demo Engine)",
        "run_btn": "🚀 بدء المسح والتشخيص الطيفي المباشر",
        "tab_visual": "📷 المسح البصري بالليزر ومواصفات المحرك",
        "tab_fft": "📈 التحليل الطيفي الترددي (FFT Spectrum)",
        "tab_recs": "🔧 تقرير العزل والقطع التالفة",
        "tab_report": "📑 التقرير الهندسي الشامل",
        "status_label": "حالة الأداء",
        "health_index": "مؤشر السلامة الميكانيكية",
        "peak_freq": "التردد السائد (Peak Freq)",
        "centroid": "المركز الطيفي (Centroid)",
        "target_unit": "وحدة الفحص المستهدفة:",
        "faulty_comp": "القطعة المعزولة بالمسح:",
        "healthy": "أداء سليم ضمن الحدود الهندسية",
        "critical": "انحراف طيفي - يلزم الصيانة المباشرة",
        "download_rep": "📥 تحميل التقرير الهندسي (TXT)",
        "info_btn": "ℹ️ بطاقة المواصفات الفنية للسيارة والمحرك",
        "cats": {
            "فولكسفاجن (Volkswagen)": "فولكسفاجن (Volkswagen)",
            "هيونداي (Hyundai)": "هيونداي (Hyundai)",
            "ميتسوبيشي (Mitsubishi)": "ميتسوبيشي (Mitsubishi)",
            "الثلاجات والآلات والمعدات": "الثلاجات والآلات والمعدات"
        }
    },
    "English": {
        "designer": "Designed & Developed by: Ismail Hasasna",
        "subtitle": "Universal AI-Powered Acoustic & Spectral Diagnostic Workstation",
        "select_cat": "🎯 Select Target Brand or Sector:",
        "select_unit": "Select Vehicle Model & Engine Spec:",
        "audio_src": "Audio Signal Source:",
        "upload_mode": "Upload Audio File (MP3, WAV, M4A, OGG, FLAC)",
        "demo_mode": "Synthetic Wave Simulator (Demo)",
        "run_btn": "🚀 Run Spectral Scan & Diagnostics",
        "tab_visual": "📷 Laser Visual Scan & Engine Specs",
        "tab_fft": "📈 FFT Spectral Analysis",
        "tab_recs": "🔧 Fault Component Isolation",
        "tab_report": "📑 Comprehensive Inspection Report",
        "status_label": "Operational Status",
        "health_index": "Mechanical Safety Index",
        "peak_freq": "Peak Frequency",
        "centroid": "Spectral Centroid",
        "target_unit": "Scanned Unit:",
        "faulty_comp": "Isolated Fault Component:",
        "healthy": "Optimal Mechanical Operation",
        "critical": "Spectral Anomaly - Inspection Required",
        "download_rep": "📥 Download Engineering Report (TXT)",
        "info_btn": "ℹ️️ Engine & Vehicle Technical Specs",
        "cats": {
            "فولكسفاجن (Volkswagen)": "Volkswagen Fleet",
            "هيونداي (Hyundai)": "Hyundai Fleet",
            "ميتسوبيشي (Mitsubishi)": "Mitsubishi Fleet",
            "الثلاجات والآلات والمعدات": "HVAC & Heavy Machinery"
        }
    },
    "Русский": {
        "designer": "Разработано: Исмаил Хасасна (Ismail Hasasna)",
        "subtitle": "Универсальная акустическая диагностическая платформа",
        "select_cat": "🎯 Выберите марку или инженерный сектор:",
        "select_unit": "Выберите модель и спецификацию двигателя:",
        "audio_src": "Источник аудиосигнала:",
        "upload_mode": "Загрузить аудиозапись (MP3, WAV, M4A, OGG, FLAC)",
        "demo_mode": "Симулятор сигналов (Демо)",
        "run_btn": "🚀 Запустить спектральный анализ",
        "tab_visual": "📷 Лазерный сканер и ТТХ",
        "tab_fft": "📈 Спектральный анализ (FFT)",
        "tab_recs": "🔧 Изоляция дефектных узлов",
        "tab_report": "📑 Полный инженерный отчет",
        "status_label": "Статус",
        "health_index": "Индекс надежности",
        "peak_freq": "Пиковая частота",
        "centroid": "Спектральный центр",
        "target_unit": "Объект проверки:",
        "faulty_comp": "Изолированный дефектный узел:",
        "healthy": "Нормальный режим",
        "critical": "Критическое отклонение - Требуется ремонт",
        "download_rep": "📥 Скачать инженерный отчет (TXT)",
        "info_btn": "ℹ️ Технические характеристики двигателя",
        "cats": {
            "فولكسفاجن (Volkswagen)": "Volkswagen Автопарк",
            "هيونداي (Hyundai)": "Hyundai Автопарк",
            "ميتسوبيشي (Mitsubishi)": "Mitsubishi Автопарк",
            "الثلاجات والآلات والمعدات": "Холодильное и пром. оборудование"
        }
    }
}

st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

top_col1, top_col2 = st.columns([3, 1])
with top_col2:
    lang_choice = st.selectbox("🌐 Language / اللغة / Язык", ["العربية", "English", "Русский"], index=0)

L = I18N[lang_choice]

THEMES = {
    "فولكسفاجن (Volkswagen)": {"color": "#ff7b00", "glow": "rgba(255, 123, 0, 0.35)", "icon": "🚘"},
    "هيونداي (Hyundai)": {"color": "#0099ff", "glow": "rgba(0, 153, 255, 0.35)", "icon": "🚙"},
    "ميتسوبيشي (Mitsubishi)": {"color": "#ff2a2a", "glow": "rgba(255, 42, 42, 0.35)", "icon": "🏎️"},
    "الثلاجات والآلات والمعدات": {"color": "#00ff88", "glow": "rgba(0, 255, 136, 0.35)", "icon": "⚙️"}
}

if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = "فولكسفاجن (Volkswagen)"

current_cat = st.session_state["selected_category"]
theme = THEMES[current_cat]

st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(135deg, #0a0d12 0%, #121721 50%, #0a0d12 100%); color: #c9d1d9; }}
    .theme-header {{ color: {theme['color']} !important; text-shadow: 0 0 18px {theme['glow']}; font-weight: 900; text-align: center; font-size: 2.5rem; }}
    .designer-tag {{ color: #58a6ff; font-weight: 600; font-size: 1.15rem; text-align: center; margin-bottom: 20px; }}
    .metric-card {{ background: rgba(22, 27, 34, 0.9); border: 2px solid {theme['color']}; border-radius: 12px; padding: 14px; box-shadow: 0 6px 20px {theme['glow']}; margin-bottom: 12px; text-align: center; }}
    .stButton>button {{ background: linear-gradient(90deg, {theme['color']} 0%, #1f6feb 100%) !important; color: #fff !important; font-weight: bold !important; border-radius: 8px !important; border: none !important; padding: 14px !important; width: 100%; box-shadow: 0 4px 15px {theme['glow']}; }}
    .status-healthy {{ background: rgba(46, 160, 67, 0.25); color: #3fb950; border: 1.5px solid #2ea043; padding: 6px 16px; border-radius: 20px; font-weight: 800; display: inline-block; }}
    .status-critical {{ background: rgba(248, 81, 73, 0.25); color: #f85149; border: 1.5px solid #da3633; padding: 6px 16px; border-radius: 20px; font-weight: 800; display: inline-block; }}
    
    .laser-container {{ position: relative; overflow: hidden; border-radius: 14px; border: 2px solid {theme['color']}; box-shadow: 0 0 20px {theme['glow']}; background: #000; }}
    .laser-container img {{ width: 100%; display: block; height: auto; max-height: 380px; object-fit: cover; }}
    .laser-line {{
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: {theme['color']};
        box-shadow: 0 0 18px 6px {theme['color']};
        animation: scan 2.2s infinite ease-in-out;
        z-index: 10;
    }}
    @keyframes scan {{
        0% {{ top: 0%; }}
        50% {{ top: 96%; }}
        100% {{ top: 0%; }}
    }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. مكتبة الصور المحققة للشركات والقطع
# ==========================================
COMPONENT_IMAGES = {
    # فولكسفاجن (VW)
    "vw_caddy": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=800&auto=format&fit=crop&q=80",
    "vw_golf": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&auto=format&fit=crop&q=80",
    "vw_passat": "https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?w=800&auto=format&fit=crop&q=80",
    "vw_crafter": "https://images.unsplash.com/photo-1559416523-140ddc3d238c?w=800&auto=format&fit=crop&q=80",
    
    # هيونداي (Hyundai)
    "hyundai_santafe": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=800&auto=format&fit=crop&q=80",
    "hyundai_tucson": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=800&auto=format&fit=crop&q=80",
    "hyundai_elantra": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=800&auto=format&fit=crop&q=80",
    
    # ميتسوبيشي (Mitsubishi)
    "pajero_v20": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800&auto=format&fit=crop&q=80",
    "pajero_v80": "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=800&auto=format&fit=crop&q=80",
    "mitsubishi_l200": "https://images.unsplash.com/photo-1559416523-140ddc3d238c?w=800&auto=format&fit=crop&q=80",
    
    # ثلاجات وآلات
    "fridge": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&auto=format&fit=crop&q=80",
    "washer": "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=800&auto=format&fit=crop&q=80",
    "pump": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format&fit=crop&q=80",
    "jcb": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=800&auto=format&fit=crop&q=80",
    
    # القطع التالفة
    "injectors": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=600&auto=format&fit=crop&q=80",
    "turbo": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=600&auto=format&fit=crop&q=80",
    "bearings": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=600&auto=format&fit=crop&q=80",
    "valves": "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=600&auto=format&fit=crop&q=80",
    "belt": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&auto=format&fit=crop&q=80",
    "healthy": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=600&auto=format&fit=crop&q=80"
}

# ==========================================
# 3. قاعدة البيانات الشاملة مع تفاصيل المحركات
# ==========================================
UNIVERSAL_DATABASE = {
    # ----- VOLKSWAGEN FLEET -----
    "VW Caddy 1.6 TDI (سحب طبيعي / بدون تيربو)": {
        "category": "فولكسفاجن (Volkswagen)", "brand": "Volkswagen", "model": "Caddy 1.6 TDI NA",
        "code": "CAYD / CAYA Engine Code", "oil": "5W-30 VW 507.00 Spec", "injection": "Bosch Common Rail 1600 Bar",
        "specs": "1.6L TDI Common Rail Non-Turbo Engine", "has_turbo": False, "unit_image": COMPONENT_IMAGES["vw_caddy"],
        "bands": {"bearing_wear": (20, 380), "belt_squeal": (700, 2000), "valve_clearance": (1000, 2800), "injector_clatter": (2800, 8000)},
        "names": {"bearing_wear": "سبيكة محامل الكرنك (Crank Bearing)", "belt_squeal": "قشاط المجموعات (Timing Belt)", "valve_clearance": "صمامات المحرك (Valves)", "injector_clatter": "بخاخات الديزل (Injectors)"}
    },
    "VW Caddy 2.0 TDI (شاحن تيربو)": {
        "category": "فولكسفاجن (Volkswagen)", "brand": "Volkswagen", "model": "Caddy 2.0 TDI Turbo",
        "code": "CFHC / DFSD Engine Code", "oil": "5W-30 Synthetic Clean Diesel", "injection": "Bosch Piezo Common Rail 1800 Bar",
        "specs": "2.0L TDI Turbocharged Engine", "has_turbo": True, "unit_image": COMPONENT_IMAGES["vw_caddy"],
        "bands": {"bearing_wear": (20, 350), "turbo_shaft": (1200, 5800), "injector_clatter": (2600, 8000)},
        "names": {"bearing_wear": "سبيكة الكرنك الرئيسية", "turbo_shaft": "عمود شاحن التيربو (Turbo Shaft)", "injector_clatter": "بخاخات الديزل High Pressure"}
    },
    "VW Golf VII 1.4 TSI (بنزين تيربو)": {
        "category": "فولكسفاجن (Volkswagen)", "brand": "Volkswagen", "model": "Golf VII 1.4 TSI",
        "code": "EA211 / CZCA Engine Code", "oil": "5W-40 VW 502.00 Spec", "injection": "Direct Gasoline Injection (TSI)",
        "specs": "1.4L TSI Direct Injection Turbo", "has_turbo": True, "unit_image": COMPONENT_IMAGES["vw_golf"],
        "bands": {"bearing_wear": (30, 350), "turbo_shaft": (1400, 5500), "injector_clatter": (3000, 8500)},
        "names": {"bearing_wear": "سبيكة المحرك", "turbo_shaft": "عمود التيربو", "injector_clatter": "بخاخات TSI البنزين"}
    },
    "VW Passat B8 2.0 TDI (تيربو ديزل)": {
        "category": "فولكسفاجن (Volkswagen)", "brand": "Volkswagen", "model": "Passat B8 2.0 TDI",
        "code": "CRLB / DBGA Engine Code", "oil": "0W-30 VW LongLife III", "injection": "Common Rail Direct Injection",
        "specs": "2.0L TDI Clean Diesel Turbo", "has_turbo": True, "unit_image": COMPONENT_IMAGES["vw_passat"],
        "bands": {"bearing_wear": (20, 320), "turbo_shaft": (1300, 5400), "injector_clatter": (2800, 8000)},
        "names": {"bearing_wear": "سبيكة الكرنك", "turbo_shaft": "التيربو", "injector_clatter": "بخاخات الديزل"}
    },
    "VW Crafter 2.0 BiTDI Commercial (تيربو مزدوج)": {
        "category": "فولكسفاجن (Volkswagen)", "brand": "Volkswagen", "model": "Crafter Van 2.0 BiTDI",
        "code": "CKUB / CSHA BiTurbo", "oil": "5W-30 Heavy Commercial Spec", "injection": "Bosch Common Rail Twin Turbo System",
        "specs": "2.0L BiTDI Commercial Engine", "has_turbo": True, "unit_image": COMPONENT_IMAGES["vw_crafter"],
        "bands": {"bearing_wear": (15, 340), "turbo_shaft": (1200, 5800), "injector_clatter": (2400, 8200)},
        "names": {"bearing_wear": "سبيكة الكرنك والعمود الفقري", "turbo_shaft": "التيربو المزدوج المرتفع", "injector_clatter": "بخاخات الديزل التجاري"}
    },

    # ----- HYUNDAI FLEET -----
    "Hyundai Santa Fe 2.2 CRDi VGT (تيربو ديزل)": {
        "category": "هيونداي (Hyundai)", "brand": "Hyundai", "model": "Santa Fe 2.2 CRDi VGT",
        "code": "D4HB R-Engine", "oil": "5W-30 ACEA C3 Diesel Oil", "injection": "Bosch CRDi 2000 Bar VGT System",
        "specs": "2.2L CRDi Variable Geometry Turbo Diesel", "has_turbo": True, "unit_image": COMPONENT_IMAGES["hyundai_santafe"],
        "bands": {"bearing_wear": (15, 420), "turbo_shaft": (1200, 6000), "injector_clatter": (2400, 8500), "valve_clearance": (800, 2600)},
        "names": {"bearing_wear": "سبيكة الكرنك ومحامل المحرك (Bearings)", "turbo_shaft": "شاحن التيربو VGT", "injector_clatter": "بخاخات الديزل CRDi", "valve_clearance": "التكايات الهيدروليكية والصمامات"}
    },
    "Hyundai Tucson 1.6 T-GDI (تيربو بنزين)": {
        "category": "هيونداي (Hyundai)", "brand": "Hyundai", "model": "Tucson 1.6 T-GDI",
        "code": "G4FJ Smartstream Gamma", "oil": "5W-30 Full Synthetic API SP", "injection": "GDI Direct Gasoline Turbo",
        "specs": "1.6L Turbocharged Direct Injection", "has_turbo": True, "unit_image": COMPONENT_IMAGES["hyundai_tucson"],
        "bands": {"bearing_wear": (30, 360), "turbo_shaft": (1500, 5600), "injector_clatter": (3000, 8200)},
        "names": {"bearing_wear": "سبيكة المحرك", "turbo_shaft": "عمود التيربو", "injector_clatter": "بخاخات GDI High Pressure"}
    },
    "Hyundai Elantra 1.6 MPI (تنفس طبيعي)": {
        "category": "هيونداي (Hyundai)", "brand": "Hyundai", "model": "Elantra 1.6 MPI NA",
        "code": "G4FG Gamma II Engine", "oil": "5W-20 / 5W-30 Engine Oil", "injection": "Multi-Point Injection (MPI)",
        "specs": "1.6L Gamma MPI Naturally Aspirated", "has_turbo": False, "unit_image": COMPONENT_IMAGES["hyundai_elantra"],
        "bands": {"bearing_wear": (30, 380), "belt_squeal": (800, 2200), "valve_clearance": (1000, 3200)},
        "names": {"bearing_wear": "سبيكة الكرنك", "belt_squeal": "سير وقشاط المجموعات", "valve_clearance": "صمامات المحرك"}
    },

    # ----- MITSUBISHI FLEET -----
    "Mitsubishi Pajero V20 3.4L V6 (6G74 بنزين - جير عادي 4x4)": {
        "category": "ميتسوبيشي (Mitsubishi)", "brand": "Mitsubishi", "model": "Pajero V20 3.4L V6 Manual 4x4",
        "code": "6G74 DOHC 24V Engine", "oil": "10W-40 / 15W-40 Heavy Duty Oil", "injection": "ECI-MULTI Electronic Injection",
        "specs": "3.4L 6G74 V6 NA Manual Transmission Engine", "has_turbo": False, "unit_image": COMPONENT_IMAGES["pajero_v20"],
        "bands": {"bearing_wear": (15, 400), "belt_squeal": (700, 2100), "valve_clearance": (900, 3100)},
        "names": {"bearing_wear": "سبيكة الكرنك ومحامل V6 6G74", "belt_squeal": "سير الدينامو والمجموعات", "valve_clearance": "تكايات وصمامات رأس المحرك"}
    },
    "Mitsubishi Pajero V80 3.2 DI-D (تيربو ديزل)": {
        "category": "ميتسوبيشي (Mitsubishi)", "brand": "Mitsubishi", "model": "Pajero V80 3.2 DI-D Common Rail",
        "code": "4M41 Common Rail Engine", "oil": "5W-40 / 10W-40 Diesel Spec", "injection": "Denso Common Rail System",
        "specs": "3.2L Common Rail Turbo Diesel", "has_turbo": True, "unit_image": COMPONENT_IMAGES["pajero_v80"],
        "bands": {"bearing_wear": (20, 350), "turbo_shaft": (1300, 5200), "injector_clatter": (2300, 7800)},
        "names": {"bearing_wear": "سبيكة الكرنك والعمود الفقري", "turbo_shaft": "عمود شاحن التيربو", "injector_clatter": "بخاخات الديزل Denso"}
    },
    "Mitsubishi L200 Pickup 2.4 DI-D (تيربو ديزل)": {
        "category": "ميتسوبيشي (Mitsubishi)", "brand": "Mitsubishi", "model": "L200 Pickup 2.4 DI-D MIVEC",
        "code": "4N15 MIVEC Clean Diesel", "oil": "5W-30 ACEA C2/C3", "injection": "Common Rail Direct Injection",
        "specs": "2.4L MIVEC Turbo Diesel Engine", "has_turbo": True, "unit_image": COMPONENT_IMAGES["mitsubishi_l200"],
        "bands": {"bearing_wear": (20, 360), "turbo_shaft": (1400, 5400), "injector_clatter": (2500, 8000)},
        "names": {"bearing_wear": "سبيكة الكرنك الرئيسية", "turbo_shaft": "شاحن التيربو", "injector_clatter": "بخاخات الوقود"}
    },

    # ----- HVAC & MACHINERY -----
    "ثلاجة منزلية انفرتر (Smart Inverter Refrigerator)": {
        "category": "الثلاجات والآلات والمعدات", "brand": "LG / Samsung", "model": "Inverter R600a Compressor",
        "code": "BSA075LNEG Inverter", "oil": "Ester Synthetic Refrigeration Oil", "injection": "Hermetic Variable Frequency",
        "specs": "Variable Speed Hermetic Compressor Unit", "has_turbo": False, "unit_image": COMPONENT_IMAGES["fridge"],
        "bands": {"bearing_wear": (20, 320), "compressor_valves": (800, 2600)},
        "names": {"bearing_wear": "محامل الضاغط الداخلية", "compressor_valves": "صمامات الضاغط الداخلية"}
    },
    "حفار JCB 3CX / 4CX (JCB EcoMAX 4.4L Turbo)": {
        "category": "الثلاجات والآلات والمعدات", "brand": "JCB", "model": "EcoMAX 4.4L Diesel Engine",
        "code": "JCB EcoMAX T4i", "oil": "15W-40 Heavy Duty Diesel Oil", "injection": "Delphi Common Rail System",
        "specs": "4.4L Turbocharged Heavy Duty Engine", "has_turbo": True, "unit_image": COMPONENT_IMAGES["jcb"],
        "bands": {"bearing_wear": (15, 380), "turbo_shaft": (1200, 5200), "injector_clatter": (2200, 7800)},
        "names": {"bearing_wear": "سبيكة الكرنك والعمود الفقري", "turbo_shaft": "عمود شاحن التيربو", "injector_clatter": "بخاخات الديزل الهيدروليكية"}
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
    fft_vals = np.abs(np.fft.rfft(audio_data))
    fft_freqs = np.fft.rfftfreq(len(audio_data), 1.0 / sample_rate)

    total_power = np.sum(fft_vals)
    spectral_centroid = float(np.sum(fft_freqs * fft_vals) / total_power) if total_power > 0 else 0.0
    peak_freq = float(fft_freqs[np.argmax(fft_vals)])

    bands, names = unit["bands"], unit.get("names", {})
    detected_faults, component_img, fault_type_key, health_score = [], COMPONENT_IMAGES["healthy"], L["healthy"], 100

    if "bearing_wear" in bands and (bands["bearing_wear"][0] <= peak_freq <= bands["bearing_wear"][1] or peak_freq < 450):
        detected_faults.append(f"Bearing Wear: {names.get('bearing_wear', 'Crank Bearings')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["bearings"], names.get("bearing_wear", "السبيكة والمحامل"), 38
    elif "compressor_valves" in bands and bands["compressor_valves"][0] <= peak_freq <= bands["compressor_valves"][1]:
        detected_faults.append(f"Compressor Valve Deviation: {names.get('compressor_valves', 'Reed Valves')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["healthy"], names.get("compressor_valves", "صمامات الضاغط"), 35
    elif "belt_squeal" in bands and bands["belt_squeal"][0] <= peak_freq <= bands["belt_squeal"][1]:
        detected_faults.append(f"Belt Squeal / Friction: {names.get('belt_squeal', 'Drive Belt')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["belt"], names.get("belt_squeal", "سير الحركة"), 62
    elif "valve_clearance" in bands and bands["valve_clearance"][0] <= peak_freq <= bands["valve_clearance"][1]:
        detected_faults.append(f"Valvetrain Deviation: {names.get('valve_clearance', 'Valves')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["valves"], names.get("valve_clearance", "صمامات المحرك والتكايات"), 48
    elif "injector_clatter" in bands and bands["injector_clatter"][0] <= peak_freq <= bands["injector_clatter"][1]:
        detected_faults.append(f"Injector Clatter: {names.get('injector_clatter', 'Injectors')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["injectors"], names.get("injector_clatter", "البخاخات"), 42
    elif unit["has_turbo"] and "turbo_shaft" in bands and bands["turbo_shaft"][0] <= peak_freq <= bands["turbo_shaft"][1]:
        detected_faults.append(f"Turbo Shaft Friction: {names.get('turbo_shaft', 'Turbo')}")
        component_img, fault_type_key, health_score = COMPONENT_IMAGES["turbo"], names.get("turbo_shaft", "عمود شاحن التيربو"), 22

    return {
        "target_unit": f"{unit['brand']} {unit['model']}",
        "category": unit["category"],
        "specs": unit["specs"],
        "code": unit.get("code", "N/A"),
        "oil": unit.get("oil", "N/A"),
        "injection": unit.get("injection", "N/A"),
        "unit_image": unit["unit_image"],
        "component_image": component_img,
        "fault_type_key": fault_type_key,
        "status_text": L["critical"] if detected_faults else L["healthy"],
        "status_class": "status-critical" if detected_faults else "status-healthy",
        "health_score": health_score,
        "peak_freq": round(peak_freq, 2),
        "centroid": round(spectral_centroid, 2),
        "rms": round(rms_energy, 5),
        "detected_faults": detected_faults if detected_faults else ["No Critical Deviations Detected"],
        "recommendations": f"Spectral anomaly detected at peak ({peak_freq:.1f} Hz). Targeted inspection required for isolated component." if detected_faults else "Target unit operating within optimal engineering frequency range.",
        "fft_freqs": fft_freqs,
        "fft_vals": fft_vals
    }

# ==========================================
# 4. الواجهة الرئيسية والتفاعل
# ==========================================
st.markdown(f'<div class="theme-header">⚡ ZINO EADE WORKSTATION</div>', unsafe_allow_html=True)
st.markdown(f'<div class="designer-tag">{L["designer"]}<br><small style="color:#8b949e">{L["subtitle"]}</small></div>', unsafe_allow_html=True)

st.markdown(f"### {L['select_cat']}")
cols = st.columns(4)
for idx, (cat, t_info) in enumerate(THEMES.items()):
    is_act = cat == current_cat
    cat_translated = L["cats"].get(cat, cat)
    with cols[idx]:
        st.markdown(f'<div style="background: rgba(22, 27, 34, 0.95); border: 2px solid {t_info["color"] if is_act else "#30363d"}; border-radius: 12px; padding: 12px; text-align: center; box-shadow: 0 4px 18px {t_info["glow"] if is_act else "transparent"};"><h4 style="color: {t_info["color"]} !important; margin:0;">{t_info["icon"]} {cat_translated}</h4></div>', unsafe_allow_html=True)
        if st.button(f"{t_info['icon']} Select", key=f"btn_{idx}"):
            st.session_state["selected_category"] = cat
            st.rerun()

st.markdown("---")

ctl_col1, ctl_col2 = st.columns(2)
filtered_units = {k: v for k, v in UNIVERSAL_DATABASE.items() if v["category"] == current_cat}

with ctl_col1:
    selected_unit = st.selectbox(L["select_unit"], list(filtered_units.keys()))
    unit_info = UNIVERSAL_DATABASE[selected_unit]
    with st.popover(L["info_btn"]):
        st.markdown(f"### ⚙️ {selected_unit}")
        st.write(f"• **Engine Code:** {unit_info.get('code', 'N/A')}")
        st.write(f"• **Oil Spec:** {unit_info.get('oil', 'N/A')}")
        st.write(f"• **Injection Spec:** {unit_info.get('injection', 'N/A')}")
        st.write(f"• **Mechanical Specs:** {unit_info['specs']}")

with ctl_col2:
    source_mode = st.radio(L["audio_src"], (L["upload_mode"], L["demo_mode"]), horizontal=True)

audio_file, synthetic_fault = None, "bearing_wear"
if source_mode == L["upload_mode"]:
    audio_file = st.file_uploader("Upload Audio Signal File:", type=["wav", "mp3", "m4a", "ogg", "flac"])
else:
    synthetic_fault = st.selectbox("Synthetic Fault Pattern:", ["bearing_wear", "turbo_shaft", "healthy"])

st.markdown("<br>", unsafe_allow_html=True)
run_click = st.button(L["run_btn"])

# ==========================================
# 5. شريط محاكاة المسح والتشخيص
# ==========================================
if run_click or "has_run" in st.session_state:
    st.session_state["has_run"] = True
    
    if run_click:
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        stages = [
            ("⚡ المرحلة 1: شحن محرك المعالجة الطيفية وعزل الضوضاء المباشرة...", 25, 0.4),
            ("📈 المرحلة 2: تشريح موجات الصوت باستعمال تحويل فوريه السريع (FFT)...", 50, 0.5),
            ("🔍 المرحلة 3: مطابقة بصمة الصوت مع قاعدة بيانات محركات (VW, Hyundai, Mitsubishi)...", 75, 0.5),
            ("🎯 المرحلة 4: تحديد الانحرافات الترددية وعزل القطعة التالفة بالليزر...", 100, 0.4)
        ]
        
        for msg, pct, delay in stages:
            progress_text.markdown(f"**{msg}**")
            progress_bar.progress(pct)
            time.sleep(delay)
            
        progress_text.empty()
        progress_bar.empty()

    audio_data, sample_rate = None, 22050
    if source_mode == L["upload_mode"]:
        if audio_file is not None:
            audio_data, sample_rate = read_any_audio(audio_file)
        else:
            st.warning("⚠️ Please upload an audio file first.")
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
            fig.add_trace(go.Scatter(x=res["fft_freqs"][mask], y=res["fft_vals"][mask], mode="lines", line=dict(color=theme["color"], width=2.5)))
            fig.update_layout(template="plotly_dark", xaxis_title="Frequency (Hz)", yaxis_title="Amplitude Spectrum Density")
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
Engine Code       : {res['code']}
Oil Spec          : {res['oil']}
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
