import io
import json
import numpy as np
import plotly.graph_objects as go
import scipy.io.wavfile as wavfile
import scipy.signal as signal
import streamlit as st

# ضبط إعدادات الصفحة الاحترافية
st.set_page_config(
    page_title="ZINO EADE - Universal Acoustic Diagnostic Workstation",
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
        },
        "component_names": {
            "bearing_wear": "محامل المحرك الكهربائي (Motor Bearings)",
            "pump_impeller": "عنفة / فراشة المضخة (Pump Impeller)",
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
        },
        "component_names": {
            "bearing_wear": "محامل الدوران الأمامية والخلفية (Drive Bearings)",
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
            "injector_clatter": (3000, 8000),
        },
        "component_names": {
            "bearing_wear": "سبيكة الكرنك (Crank Bearings)",
            "turbo_shaft": "مروحة وعمود التيربو (Turbocharger Shaft)",
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
}


# ==========================================
# 4. معالج الصوت السريع
# ==========================================
def read_wav_safe(uploaded_file):
    try:
        bytes_data = uploaded_file.read()
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
        st.error("⚠️ يرجى استخدام ملف بصيغة WAV معيارية.")
        return None, None


def generate_synthetic_audio(fault_type="bearing_wear", sr=22050, duration=3.0):
    t = np.linspace(0, duration, int(sr * duration))
    base = 0.2 * np.sin(2 * np.pi * 50 * t)
    if fault_type == "bearing_wear":
        f_sig = 0.45 * np.sin(2 * np.pi * 180 * t)
    elif fault_type == "turbo_shaft":
        f_sig = 0.5 * np.sin(2 * np.pi * 3200 * t)
    elif fault_type == "injector_clatter":
        f_sig = 0.4 * np.sin(2 * np.pi * 4800 * t)
    else:
        f_sig = 0.0
    noise = np.random.normal(0, 0.02, len(t))
    return (base + f_sig + noise).astype(np.float32), sr


# ==========================================
# 5. محرك التشخيص والتقرير
# ==========================================
def run_full_diagnostic(audio_data, sample_rate, selected_unit_key):
    unit = UNIVERSAL_DATABASE[selected_unit_key]
    rms_energy = float(np.sqrt(np.mean(audio_data**2)))
    fft_vals = np.abs(np.fft.rfft(audio_data))
    fft_freqs = np.fft.rfftfreq(len(audio_data), 1.0 / sample_rate)

    total_power = np.sum(fft_vals)
    spectral_centroid = (
        float(np.sum(fft_freqs * fft_vals) / total_power)
        if total_power > 0
        else 0.0
    )
    peak_freq = float(fft_freqs[np.argmax(fft_vals)])

    bands = unit["bands"]
    component_names = unit.get("component_names", {})

    detected_faults = []
    fault_type_key = "سليم (Healthy)"
    component_img = COMPONENT_IMAGES["healthy"]
    health_score = 100

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

    elif (
        "belt_squeal" in bands
        and bands["belt_squeal"][0] <= peak_freq <= bands["belt_squeal"][1]
    ):
        name_str = component_names.get(
            "belt_squeal", "سير المجموعات (Drive Belt)"
        )
        detected_faults.append(f"انزلاق/ارتخاء في {name_str}")
        component_img = COMPONENT_IMAGES["belt"]
        fault_type_key = "Drive Belt / سير الحركة"
        health_score = 65

    elif (
        "valve_clearance" in bands
        and bands["valve_clearance"][0]
        <= peak_freq
        <= bands["valve_clearance"][1]
    ):
        name_str = component_names.get(
            "valve_clearance", "صمامات المحرك (Valvetrain)"
        )
        detected_faults.append(f"اتساع خلوص {name_str}")
        component_img = COMPONENT_IMAGES["valves"]
        fault_type_key = "Valvetrain / صمامات المحرك"
        health_score = 50

    elif (
        "injector_clatter" in bands
        and bands["injector_clatter"][0]
        <= peak_freq
        <= bands["injector_clatter"][1]
    ):
        name_str = component_names.get(
            "injector_clatter", "بخاخات الوقود (Injectors)"
        )
        detected_faults.append(f"تفاوت ضغط في {name_str}")
        component_img = COMPONENT_IMAGES["injectors"]
        fault_type_key = "Fuel Injectors / البخاخات"
        health_score = 45

    elif (
        unit["has_turbo"]
        and "turbo_shaft" in bands
        and bands["turbo_shaft"][0] <= peak_freq <= bands["turbo_shaft"][1]
    ):
        name_str = component_names.get(
            "turbo_shaft", "عمود التيربو (Turbo Shaft)"
        )
        detected_faults.append(f"احتراق/احتكاك في {name_str}")
        component_img = COMPONENT_IMAGES["turbo"]
        fault_type_key = "Turbocharger Shaft / عمود التيربو"
        health_score = 25

    if not detected_faults:
        status_text = "Healthy / أداء منتظم وسليم"
        status_class = "status-badge-healthy"
        recommendations = f"وحدة {unit['brand']} {unit['model']} تعمل بكفاءة عالية وضمن النطاق الطيفي الطبيعي."
    else:
        status_text = "Critical / يلزم الصيانة"
        status_class = "status-badge-critical"
        faults_str = " | ".join(detected_faults)
        recommendations = f"تم رصد انحراف طيفي محدد عند تردد ({peak_freq:.1f} Hz). يُنصح بالفحص الميداني المباشر للقطع التالية: ({faults_str})."

    return {
        "target_unit": f"{unit['brand']} {unit['model']}",
        "category": unit["category"],
        "specs": unit["specs"],
        "unit_image": unit["unit_image"],
        "component_image": component_img,
        "fault_type_key": fault_type_key,
        "status_text": status_text,
        "status_class": status_class,
        "health_score": health_score,
        "peak_freq": round(peak_freq, 2),
        "centroid": round(spectral_centroid, 2),
        "rms": round(rms_energy, 5),
        "detected_faults": (
            detected_faults
            if detected_faults
            else ["لا يوجد انحرافات طيفية"]
        ),
        "recommendations": recommendations,
        "fft_freqs": fft_freqs,
        "fft_vals": fft_vals,
        "audio_data": audio_data,
        "sample_rate": sample_rate,
    }


# ==========================================
# 6. الواجهة والتفاعل
# ==========================================
st.markdown(
    """
<div style="text-align: center; padding: 10px 0 25px 0;">
    <h1 style="font-size: 2.8rem; margin-bottom: 0px;">⚡ ZINO EADE</h1>
    <p style="font-size: 1.1rem; color: #8b949e; margin-top: 5px;">
        Universal Edge Acoustic Diagnostic Engine | المنظومة الذكية الشاملة للتشخيص الصوتي الهندسي
    </p>
</div>
""",
    unsafe_allow_html=True,
)

st.sidebar.header("🎯 إعدادات وحدة الفحص")
category_list = sorted(
    list(set(v["category"] for v in UNIVERSAL_DATABASE.values()))
)
selected_category = st.sidebar.selectbox("اختر فئة المعدة:", category_list)

filtered_units = {
    k: v
    for k, v in UNIVERSAL_DATABASE.items()
    if v["category"] == selected_category
}
selected_unit = st.sidebar.selectbox(
    "اختر الطراز والمحرك المباشر:", list(filtered_units.keys())
)

st.sidebar.markdown("---")
st.sidebar.header("🔊 مصدر الصوت")
source_mode = st.sidebar.radio(
    "اختر طريقة وضع الصوت:",
    ("رفع ملف صوتي (WAV)", "محاكي الموجات الهندسي (Demo Engine)"),
)

audio_file = None
synthetic_fault = "bearing_wear"

if source_mode == "رفع ملف صوتي (WAV)":
    audio_file = st.sidebar.file_uploader(
        "ارفع ملف الصوت المطلوب إخضاعه للفحص:", type=["wav"]
    )
else:
    synthetic_fault = st.sidebar.selectbox(
        "اختر نمط الخلل المراد محاكاته:",
        ["bearing_wear", "turbo_shaft", "injector_clatter", "healthy"],
    )

run_button = st.sidebar.button("🚀 بدء المسح والتشخيص المباشر")

if run_button:
    audio_data = None
    sample_rate = 22050

    if source_mode == "رفع ملف صوتي (WAV)":
        if audio_file is None:
            st.warning("⚠️ يرجى رفع ملف صوت أولاً للبدء.")
        else:
            audio_data, sample_rate = read_wav_safe(audio_file)
    else:
        audio_data, sample_rate = generate_synthetic_audio(synthetic_fault)

    if audio_data is not None:
        res = run_full_diagnostic(audio_data, sample_rate, selected_unit)

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "📷 المسح البصري المباشر",
                "📈 التحليل الطيفي والموجي (FFT)",
                "🔧 التوصيات والقطع التالفة",
                "📑 التقرير الهندسي الشامل",
            ]
        )

        with tab1:
            st.markdown("### 🔍 نتيجة المسح البصري الثنائي")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"#### ⚙️ وحدة الفحص: {res['target_unit']}")
                st.image(res["unit_image"], use_container_width=True)

            with c2:
                st.markdown(
                    f"#### 🎯 القطعة المحددة بالمسح: {res['fault_type_key']}"
                )
                st.image(res["component_image"], use_container_width=True)

            st.markdown("---")
            m1, m2, m3, m4 = st.columns(4)
            m1.markdown(
                f'<div class="metric-card"><small>حالة الأداء</small><br><span class="{res["status_class"]}">{res["status_text"]}</span></div>',
                unsafe_allow_html=True,
            )
            m2.markdown(
                f'<div class="metric-card"><small>مؤشر السلامة</small><h2 style="color:#58a6ff;margin:0">{res["health_score"]}%</h2></div>',
                unsafe_allow_html=True,
            )
            m3.markdown(
                f'<div class="metric-card"><small>Peak Frequency</small><h2 style="color:#f0f6fc;margin:0">{res["peak_freq"]} Hz</h2></div>',
                unsafe_allow_html=True,
            )
            m4.markdown(
                f'<div cla
