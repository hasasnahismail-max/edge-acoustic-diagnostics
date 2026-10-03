import io
import numpy as np
import scipy.io.wavfile as wavfile
import scipy.signal as signal
import streamlit as st

# محاولة تحميل مكتبة soundfile للقراءة الصوتية المتقدمة
try:
    import soundfile as sf

    HAS_SOUNDFILE = True
except ImportError:
    HAS_SOUNDFILE = False

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="ZINO EADE - Visual Acoustic Diagnostic Workstation",
    page_icon="🚘",
    layout="wide",
)

# ==========================================
# 1. مكتبة الصور الميكانيكية والقطع
# ==========================================
COMPONENT_IMAGES = {
    "injectors": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=600&auto=format&fit=crop&q=80",
    "turbo": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=600&auto=format&fit=crop&q=80",
    "bearings": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=600&auto=format&fit=crop&q=80",
    "valves": "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=600&auto=format&fit=crop&q=80",
    "belt": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&auto=format&fit=crop&q=80",
    "healthy": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=600&auto=format&fit=crop&q=80",
}

# ==========================================
# 2. قاعدة بيانات المحركات والسيارات الشاملة
# ==========================================
ENGINE_DATABASE = {
    "VW Caddy 1.6 TDI (تنفس طبيعي / بدون تيربو)": {
        "brand": "Volkswagen",
        "model": "Caddy 1.6 TDI NA",
        "specs": "1.6L TDI / Non-Turbo (Common Rail)",
        "has_turbo": False,
        "car_image": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=800&auto=format&fit=crop&q=80",
        "bands": {
            "bearing_wear": (20, 350),
            "belt_squeal": (700, 2000),
            "valve_clearance": (1000, 2800),
            "injector_clatter": (3000, 8000),
        },
    },
    "VW Caddy 1.6 TDI (شاحن تيربو)": {
        "brand": "Volkswagen",
        "model": "Caddy 1.6 TDI Turbo",
        "specs": "1.6L TDI / Turbocharged",
        "has_turbo": True,
        "car_image": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=800&auto=format&fit=crop&q=80",
        "bands": {
            "bearing_wear": (20, 350),
            "turbo_shaft": (1500, 5500),
            "valve_clearance": (1000, 2800),
            "injector_clatter": (3000, 8000),
        },
    },
    "Hyundai Santa Fe 2.2 CRDi (تيربو)": {
        "brand": "Hyundai",
        "model": "Santa Fe 2.2 CRDi",
        "specs": "2.2L CRDi / Turbo Diesel",
        "has_turbo": True,
        "car_image": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=800&auto=format&fit=crop&q=80",
        "bands": {
            "bearing_wear": (20, 300),
            "turbo_shaft": (1500, 5000),
            "injector_clatter": (2500, 8000),
        },
    },
    "Honda Civic 1.5 Turbo": {
        "brand": "Honda",
        "model": "Civic 1.5 VTEC Turbo",
        "specs": "1.5L Direct Injection Turbo",
        "has_turbo": True,
        "car_image": "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=800&auto=format&fit=crop&q=80",
        "bands": {
            "bearing_wear": (30, 320),
            "turbo_shaft": (1600, 5200),
            "injector_clatter": (3200, 8500),
        },
    },
    "Toyota Corolla 1.6L (بنزين)": {
        "brand": "Toyota",
        "model": "Corolla 1.6 VVT-i",
        "specs": "1.6L VVT-i / Gasoline NA",
        "has_turbo": False,
        "car_image": "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800&auto=format&fit=crop&q=80",
        "bands": {
            "bearing_wear": (30, 350),
            "belt_squeal": (800, 2000),
            "valve_clearance": (1000, 3200),
        },
    },
}


# ==========================================
# 3. دالة استخراج ومعالجة الصوت الحقيقي
# ==========================================
def read_uploaded_audio(uploaded_file):
    bytes_data = uploaded_file.read()
    buffer = io.BytesIO(bytes_data)

    if HAS_SOUNDFILE:
        try:
            data, samplerate = sf.read(buffer)
            if data.ndim > 1:
                data = np.mean(data, axis=1)
            return data.astype(np.float32), samplerate
        except Exception:
            pass

    try:
        buffer.seek(0)
        samplerate, data = wavfile.read(buffer)
        if data.ndim > 1:
            data = np.mean(data, axis=1)
        if data.dtype == np.int16:
            data = data / 32768.0
        elif data.dtype == np.int32:
            data = data / 2147483648.0
        return data.astype(np.float32), samplerate
    except Exception as e:
        st.error(f"خطأ في قراءة ملف الصوت: {e}")
        return None, None


# ==========================================
# 4. محرك التشخيص الطيفي والصوري المتقدم
# ==========================================
def run_visual_acoustic_analysis(audio_data, sample_rate, vehicle_key):
    vehicle = ENGINE_DATABASE[vehicle_key]

    rms_energy = float(np.sqrt(np.mean(audio_data**2)))
    fft_vals = np.abs(np.fft.rfft(audio_data))
    fft_freqs = np.fft.rfftfreq(len(audio_data), 1.0 / sample_rate)

    total_power = np.sum(fft_vals)
    spectral_centroid = (
        float(np.sum(fft_freqs * fft_vals) / total_power)
        if total_power > 0
        else 0.0
    )

    peak_index = np.argmax(fft_vals)
    peak_freq = float(fft_freqs[peak_index])

    detected_faults = []
    component_img = COMPONENT_IMAGES["healthy"]
    fault_type_key = "none"

    bands = vehicle["bands"]

    # مطابقة الخلل وإسناد صورة القطعة الميكانيكية المحددة
    if "bearing_wear" in bands and bands["bearing_wear"][0] <= peak_freq <= bands["bearing_wear"][1]:
        detected_faults.append(
            "تآكل في سبيكة الكرنك ومحامل المحرك (Bearing Wear)"
        )
        component_img = COMPONENT_IMAGES["bearings"]
        fault_type_key = "Crankshaft Bearings"

    elif "belt_squeal" in bands and bands["belt_squeal"][0] <= peak_freq <= bands["belt_squeal"][1]:
        detected_faults.append(
            "انزلاق/احتكاك في سير المجموعات والبكرات (Belt Squeal)"
        )
        component_img = COMPONENT_IMAGES["belt"]
        fault_type_key = "Timing/Drive Belt"

    elif "valve_clearance" in bands and bands["valve_clearance"][0] <= peak_freq <= bands["valve_clearance"][1]:
        detected_faults.append(
            "اتساع خلوص الصمامات واحتكاك التاكيهات (Valve Clearance)"
        )
        component_img = COMPONENT_IMAGES["valves"]
        fault_type_key = "Valvetrain System"

    elif "injector_clatter" in bands and bands["injector_clatter"][0] <= peak_freq <= bands["injector_clatter"][1]:
        detected_faults.append(
            "تفاوت وضغط عالي في بخاخات الوقود (Injector Clatter)"
        )
        component_img = COMPONENT_IMAGES["injectors"]
        fault_type_key = "Fuel Injectors"

    elif (
        vehicle["has_turbo"]
        and "turbo_shaft" in bands
        and bands["turbo_shaft"][0] <= peak_freq <= bands["turbo_shaft"][1]
    ):
        detected_faults.append(
            "احتكاك / خلل في اتزان عمود التيربو (Turbocharger Shaft)"
        )
        component_img = COMPONENT_IMAGES["turbo"]
        fault_type_key = "Turbocharger"

    if not detected_faults:
        status = "Healthy / أداء ميكانيكي منتظم"
        fault_summary = (
            "لم يتم رصد أي انحراف طيفي خارج الحدود المسموحة للمحرك."
        )
        recommendations = "المحرك يعمل بحالة ممتازة ضمن المدى الهندسي الطبيعي."
    else:
        status = "Critical / Inspection Required"
        fault_summary = " | ".join(detected_faults)
        recommendations = f"تم تشخيص خلل بصري وطيفي لسيارة {vehicle['brand']} {vehicle['model']}. القطعة التالفة المحددة بالمسح: ({fault_type_key})."

    return {
        "target_unit": f"{vehicle['brand']} {vehicle['model']}",
        "specs": vehicle["specs"],
        "car_image": vehicle["car_image"],
        "component_image": component_img,
        "fault_type_key": fault_type_key,
        "status": status,
        "fault_summary": fault_summary,
        "centroid": round(spectral_centroid, 2),
        "rms": round(rms_energy, 5),
        "peak_freq": round(peak_freq, 2),
        "recommendations": recommendations,
    }


# ==========================================
# 5. واجهة المستخدم البصرية (Streamlit UI)
# ==========================================
st.title("🚘 ZINO EADE - Visual Acoustic Diagnostic Workstation")
st.caption(
    "المنظومة الذكية المتقدمة للتشخيص الطيفي والبصري المباشر لأعطال السيارات"
)

st.sidebar.header("🎯 تحديد وحدة الفحص")
selected_vehicle = st.sidebar.selectbox(
    "اختر نوع السيارة والمحرك المباشر:", list(ENGINE_DATABASE.keys())
)

uploaded_file = st.sidebar.file_uploader(
    "ارفع تسجيل صوت المحرك (WAV / MP3):", type=["wav", "mp3"]
)

if st.sidebar.button("بدء المسح البصري والتشخيص الطيفي"):
    if uploaded_file is None:
        st.warning("يرجى رفع ملف صوت المحرك أولاً للبدء.")
    else:
        with st.spinner(
            "جاري معالجة موجات الصوت وإسقاط المسح البصري على المكونات..."
        ):
            audio_data, sample_rate = read_uploaded_audio(uploaded_file)

            if audio_data is not None:
                res = run_visual_acoustic_analysis(
                    audio_data, sample_rate, selected_vehicle
                )

                st.markdown("---")

                # عرض الصورة المركبة (صورة السيارة + صورة القطعة المحددة)
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"### 🚗 وحدة الفحص: {res['target_unit']}")
                    st.image(
                        res["car_image"],
                        caption=f"Target: {res['target_unit']} ({res['specs']})",
                        use_container_width=True,
                    )

                with col2:
                    st.markdown(
                        f"### 🔍 القطعة المحددة بالمسح: {res['fault_type_key']}"
                    )
                    st.image(
                        res["component_image"],
                        caption=f"Component Diagnostic Focus: {res['fault_type_key']}",
                        use_container_width=True,
                    )

                st.markdown("---")
                st.markdown("### 📊 التقرير الطيفي والهندسي:")

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("حالة الأداء", res["status"])
                m2.metric("Peak Frequency", f"{res['peak_freq']} Hz")
                m3.metric("Spectral Centroid", f"{res['centroid']} Hz")
                m4.metric("Signal RMS Energy", f"{res['rms']}")

                st.write(f"• **المواصفات:** {res['specs']}")
                st.write(f"• **القطعة المرشحة للخلل:** {res['fault_summary']}")

                st.markdown("---")
                st.markdown("### 💡 التوصية الهندسية المباشرة:")
                st.info(res["recommendations"])
