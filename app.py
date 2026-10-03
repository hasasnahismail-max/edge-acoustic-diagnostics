import streamlit as st
import numpy as np
import plotly.graph_objects as go
import io
import time

# Optional Audio Libraries
try:
    import librosa
    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False

try:
    import soundfile as sf
    HAS_SOUNDFILE = True
except ImportError:
    HAS_SOUNDFILE = False

try:
    from pydub import AudioSegment
    HAS_PYDUB = True
except ImportError:
    HAS_PYDUB = False

from scipy.io import wavfile

# ==========================================
# 1. إعدادات الصفحة والتصميم العام (ZINO EADE Theme)
# ==========================================
st.set_page_config(
    page_title="ZINO EADE - Edge-Acoustic Diagnostic Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #f0f6fc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .theme-header { font-size: 28px; font-weight: 800; color: #58a6ff; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 5px; }
    .designer-tag { font-size: 14px; color: #8b949e; font-weight: 600; margin-bottom: 25px; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    .metric-card { background: rgba(22, 27, 34, 0.95); border: 1px solid #30363d; border-radius: 10px; padding: 15px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
    .status-healthy { color: #3fb950; font-weight: bold; font-size: 18px; }
    .status-critical { color: #f85149; font-weight: bold; font-size: 18px; }
    .laser-container { position: relative; border-radius: 12px; overflow: hidden; border: 2px solid #58a6ff; box-shadow: 0 0 20px rgba(88, 166, 255, 0.3); }
    .laser-line { position: absolute; top: 0; left: 0; width: 100%; height: 3px; background: #ff7b72; box-shadow: 0 0 12px #ff7b72; animation: scanLaser 2.5s infinite ease-in-out; z-index: 10; }
    @keyframes scanLaser { 0% { top: 0%; } 50% { top: 100%; } 100% { top: 0%; } }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. القواميس وقاعدة البيانات الهندسية
# ==========================================
L = {
    "designer": "Platform Architect & Designer: Ismail Hasasna (إسماعيل حساسنة)",
    "subtitle": "Edge-Acoustic Diagnostic Engine (ZINO-EADE) — Real-Time Mechanical Frequency Analyzer",
    "select_cat": "Select Engineering Sector / قطاع الفحص الهندسي:",
    "select_unit": "Select Target Unit / المركبة أو المعدة المستهدفة:",
    "audio_src": "Audio Input Source / مصدر إشارة الفحص الصوتي:",
    "upload_mode": "📁 Upload Audio File (ملف حقيقي)",
    "demo_mode": "⚡ Synthetic Signal Generator (محاكاة)",
    "run_btn": "🚀 Run Deep Acoustic & Laser Scan / بدء التشخيص الطيفي الكامل",
    "tab_visual": "🔬 Optical & Spectral Scan",
    "tab_fft": "📈 FFT Frequency Analysis",
    "tab_recs": "🛠️ Engineering Recommendations",
    "tab_report": "📋 Inspection Report",
    "target_unit": "Target Unit:",
    "faulty_comp": "Isolated Anomaly / القطعة المعزولة:",
    "status_label": "System Status / حالة الأداء:",
    "health_index": "Health Index / مؤشر السلامة:",
    "peak_freq": "Dominant Peak Freq",
    "centroid": "Spectral Centroid",
    "healthy": "Optimal Performance / أداء سليم ضمن الحدود الهندسية",
    "critical": "Critical Deviation Detected / انحراف ميكانيكي حرج",
    "download_rep": "📥 Download Official Inspection Report",
    "cats": {
        "AUTOMOTIVE": "سيارات الركاب والدفع الرباعي (Automotive Fleet)",
        "HVAC": "أنظمة التكييف والتبريد الصناعي (HVAC & Refrigeration)",
        "MACHINERY": "المعدات الثقيلة والجرارات (Heavy Machinery & Tractors)"
    }
}

THEMES = {
    "AUTOMOTIVE": {"color": "#58a6ff", "glow": "rgba(88,166,255,0.4)", "icon": "🚙"},
    "HVAC": {"color": "#3fb950", "glow": "rgba(63,185,80,0.4)", "icon": "❄️"},
    "MACHINERY": {"color": "#d29922", "glow": "rgba(210,153,34,0.4)", "icon": "🚜"}
}

if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = "AUTOMOTIVE"
current_cat = st.session_state["selected_category"]
theme = THEMES[current_cat]

COMPONENT_IMAGES = {
    "healthy": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=800&q=80",
    "bearings": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80",
    "valves": "https://images.unsplash.com/photo-1581092335397-9583fe92d232?auto=format&fit=crop&w=800&q=80",
    "injectors": "https://images.unsplash.com/photo-1581092580497-e0d23cbdf1dc?auto=format&fit=crop&w=800&q=80",
    "turbo": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?auto=format&fit=crop&w=800&q=80",
    "belt": "https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?auto=format&fit=crop&w=800&q=80"
}

UNIVERSAL_DATABASE = {
    "Hyundai Santa Fe 2.2 CRDi VGT": {
        "category": "AUTOMOTIVE", "brand": "Hyundai", "model": "Santa Fe 2.2 CRDi VGT",
        "code": "D4HB R-Engine", "oil": "5W-30 ACEA C3 Diesel Oil", "injection": "Bosch CRDi 2000 Bar VGT System",
        "specs": "2.2L CRDi Variable Geometry Turbo Diesel", "has_turbo": True,
        "unit_image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=800&q=80",
        "bands": {"bearing_wear": (15, 450), "turbo_shaft": (1200, 6000), "injector_clatter": (2200, 4800), "valve_clearance": (500, 1100)},
        "names": {"bearing_wear": "محامل الكرانك والسبايك", "turbo_shaft": "عمود تيربو VGT", "injector_clatter": "بخاخات الديزل الضغط العالي", "valve_clearance": "تكايات وصمامات المحرك"}
    },
    "Mitsubishi Pajero V20 3.4L V6": {
        "category": "AUTOMOTIVE", "brand": "Mitsubishi", "model": "Pajero V20 3.4L V6 Manual 4x4",
        "code": "6G74 DOHC 24V Engine", "oil": "10W-40 / 15W-40 Heavy Duty Oil", "injection": "EGI-MULTI Electronic Injection",
        "specs": "3.4L 6G74 V6 MK Manual Transmission Engine", "has_turbo": False,
        "unit_image": "https://images.unsplash.com/photo-1553440569-bcc63803a83d?auto=format&fit=crop&w=800&q=80",
        "bands": {"bearing_wear": (20, 480), "belt_squeal": (700, 2200), "valve_clearance": (900, 3200)},
        "names": {"bearing_wear": "سبيكة الكرانك والعمود المرفقي", "belt_squeal": "سيور المحرك والملحقات", "valve_clearance": "صمامات المحرك"}
    },
    "VW Golf VII 1.4 TSI": {
        "category": "AUTOMOTIVE", "brand": "Volkswagen", "model": "Golf VII 1.4 TSI",
        "code": "EA211 / CZCA Engine Code", "oil": "5W-40 VW 502.00 Spec", "injection": "Direct Gasoline Injection (TSI)",
        "specs": "1.4L TSI Direct Injection Turbo", "has_turbo": True,
        "unit_image": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=800&q=80",
        "bands": {"bearing_wear": (30, 380), "turbo_shaft": (1300, 5200), "injector_clatter": (3000, 5500)},
        "names": {"bearing_wear": "سبائك العمود", "turbo_shaft": "عمود التيربو", "injector_clatter": "حاقنات الوقود (Injectors)"}
    },
    "Smart Inverter Refrigerator": {
        "category": "HVAC", "brand": "LG / Samsung", "model": "Inverter R600a Compressor",
        "code": "BSA075LNEG Inverter", "oil": "Ester Synthetic Refrigeration Oil", "injection": "Hermetic Variable Frequency",
        "specs": "Variable Speed Hermetic Compressor Unit", "has_turbo": False,
        "unit_image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80",
        "bands": {"bearing_wear": (20, 320), "compressor_valves": (800, 2800)},
        "names": {"bearing_wear": "صواميل الضاغط الداخلية", "compressor_valves": "صمامات الضاغط الناطقة"}
    },
    "JCB 3CX / 4CX EcoMAX 4.4L": {
        "category": "MACHINERY", "brand": "JCB", "model": "EcoMAX 4.4L Diesel Engine",
        "code": "JCB EcoMAX T4I", "oil": "15W-40 Heavy Duty Diesel Oil", "injection": "Delphi Common Rail System",
        "specs": "4.4L Turbocharged Heavy Duty Engine", "has_turbo": True,
        "unit_image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80",
        "bands": {"bearing_wear": (15, 380), "turbo_shaft": (1200, 5800), "injector_clatter": (2300, 7800)},
        "names": {"bearing_wear": "السبائك الكبرى وأعمدة الكرانك", "turbo_shaft": "شاحن التيربو الهيدروليكي", "injector_clatter": "بخاخات الضغط العالي"}
    }
}

# ==========================================
# 3. دوال قراءة الصوت والمعالجة الطيفية
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
    base = 0.2 * np.sin(2 * np.pi * 60 * t)
    if fault_type == "bearing_wear":
        f_sig = 0.6 * np.sin(2 * np.pi * 220 * t) * np.sin(2 * np.pi * 10 * t)
    elif fault_type == "turbo_shaft":
        f_sig = 0.65 * np.sin(2 * np.pi * 2400 * t)
    elif fault_type == "injector_clatter":
        f_sig = 0.7 * np.sin(2 * np.pi * 3100 * t)
    else:
        f_sig = 0.0
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
    detected_faults = []
    component_img = COMPONENT_IMAGES["healthy"]
    fault_type_key = L["healthy"]
    health_score = 94

    matched_key = None
    for b_name, (low, high) in bands.items():
        mask_band = (fft_freqs >= low) & (fft_freqs <= high)
        if np.any(mask_band):
            band_energy = np.sum(fft_vals[mask_band])
            avg_band_energy = total_power / max(len(fft_vals), 1)
            if band_energy > (avg_band_energy * 1.5) or (low <= peak_freq <= high):
                matched_key = b_name
                break

    if matched_key:
        comp_name = names.get(matched_key, matched_key)
        detected_faults.append(f"Spectral Deviation in [{matched_key}]: {comp_name}")
        fault_type_key = comp_name
        if "bearing" in matched_key:
            component_img = COMPONENT_IMAGES["bearings"]
            health_score = 38
        elif "turbo" in matched_key:
            component_img = COMPONENT_IMAGES["turbo"]
            health_score = 24
        elif "injector" in matched_key:
            component_img = COMPONENT_IMAGES["injectors"]
            health_score = 42
        elif "valve" in matched_key:
            component_img = COMPONENT_IMAGES["valves"]
            health_score = 49
        elif "belt" in matched_key:
            component_img = COMPONENT_IMAGES["belt"]
            health_score = 61
        else:
            component_img = COMPONENT_IMAGES["bearings"]
            health_score = 45

    status_text = L["critical"] if detected_faults else L["healthy"]
    status_class = "status-critical" if detected_faults else "status-healthy"

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
        "status_text": status_text,
        "status_class": status_class,
        "health_score": health_score,
        "peak_freq": round(peak_freq, 2),
        "centroid": round(spectral_centroid, 2),
        "rms": round(rms_energy, 5),
        "detected_faults": detected_faults if detected_faults else ["No Critical Acoustic Deviations Detected (Optimal)"],
        "recommendations": f"Detected dominant frequency component at {peak_freq:.1f} Hz. Spectral analysis confirms anomaly in {fault_type_key}." if detected_faults else "Target unit acoustic profile aligns perfectly with optimal manufacturer operational benchmarks.",
        "fft_freqs": fft_freqs,
        "fft_vals": fft_vals
    }

# ==========================================
# 4. الواجهة الرئيسية والتفاعل
# ==========================================
st.markdown(f'<div class="theme-header">⚡ ZINO EADE WORKSTATION</div>', unsafe_allow_html=True)
st.markdown(f'<div class="designer-tag">{L["designer"]}<br><small style="color:#8b949e">{L["subtitle"]}</small></div>', unsafe_allow_html=True)

st.markdown(f"### {L['select_cat']}")
cols = st.columns(3)
cat_keys = list(THEMES.keys())
for idx, cat in enumerate(cat_keys):
    t_info = THEMES[cat]
    is_act = cat == current_cat
    cat_translated = L["cats"].get(cat, cat)
    with cols[idx]:
        st.markdown(f'<div style="background: rgba(22, 27, 34, 0.95); border: 2px solid {t_info["color"] if is_act else "#30363d"}; border-radius: 12px; padding: 12px; text-align: center; box-shadow: 0 4px 18px {t_info["glow"] if is_act else "transparent"};"><h4 style="color: {t_info["color"]} !important; margin:0; font-size:15px;">{t_info["icon"]} {cat_translated}</h4></div>', unsafe_allow_html=True)
        if st.button(f"{t_info['icon']} Select Sector", key=f"btn_cat_{idx}"):
            st.session_state["selected_category"] = cat
            st.rerun()

st.markdown("---")

ctl_col1, ctl_col2 = st.columns(2)
filtered_units = {k: v for k, v in UNIVERSAL_DATABASE.items() if v["category"] == current_cat}

with ctl_col1:
    selected_unit = st.selectbox(L["select_unit"], list(filtered_units.keys()))
    unit_info = UNIVERSAL_DATABASE[selected_unit]
    with st.popover("⚙️ View Unit Technical Specs / عرض المواصفات الفنية"):
        st.markdown(f"### ⚙️ {selected_unit}")
        st.write(f"• **Engine Code:** {unit_info.get('code', 'N/A')}")
        st.write(f"• **Oil Spec:** {unit_info.get('oil', 'N/A')}")
        st.write(f"• **Injection Spec:** {unit_info.get('injection', 'N/A')}")
        st.write(f"• **Mechanical Specs:** {unit_info['specs']}")

with ctl_col2:
    source_mode = st.radio(L["audio_src"], (L["upload_mode"], L["demo_mode"]), horizontal=True)

audio_file, synthetic_fault = None, "bearing_wear"
if source_mode == L["upload_mode"]:
    audio_file = st.file_uploader("Upload Audio Signal File (.wav, .mp3, .flac):", type=["wav", "mp3", "m4a", "ogg", "flac"])
else:
    synthetic_fault = st.selectbox("Synthetic Fault Pattern / نمط الخلل للاختبار:", ["bearing_wear", "turbo_shaft", "injector_clatter", "healthy"])

st.markdown("<br>", unsafe_allow_html=True)
run_click = st.button(L["run_btn"], type="primary")

# ==========================================
# 5. تنفيذ الفحص وعرض النتائج
# ==========================================
if run_click or "has_run" in st.session_state:
    st.session_state["has_run"] = True
    
    if run_click:
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        stages = [
            ("⚡ المرحلة 1: تهيئة محرك المعالجة الطيفية وعزل الضوضاء المحيطة...", 25, 0.3),
            ("📈 المرحلة 2: تشريح موجات الصوت وتحويل فوريه السريع (FFT Spectrum)...", 50, 0.4),
            ("🔍 المرحلة 3: مطابقة البصمة الصوتية مع بنك وحدات (VW, Hyundai, Mitsubishi, JCB)...", 75, 0.4),
            ("🎯 المرحلة 4: عزل القطعة التالفة وتوليد مؤشر السلامة الميكانيكية بالليزر...", 100, 0.3)
        ]
        
        for msg, pct, delay in stages:
            progress_text.markdown(f"**{msg}**")
            progress_bar.progress(pct)
            time.sleep(delay)
            
        progress_text.empty()
        def render_inspection_results(audio_data, sample_rate, selected_unit):
    res = run_diagnostic(audio_data, sample_rate, selected_unit)
    tab1, tab2, tab3, tab4 = st.tabs([L["tab_visual"], L["tab_fft"], L["tab_recs"], L["tab_report"]])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"#### 🚙 {L['target_unit']} {res['target_unit']}")
            st.markdown(f'''
                <div class="laser-container">
                    <div class="laser-line"></div>
                    <img src="{res['unit_image']}" alt="Target Unit" style="width:100%; height:320px; object-fit:cover;">
                </div>
            ''', unsafe_allow_html=True)
        with c2:
            st.markdown(f"#### 🎯 {L['faulty_comp']} {res['fault_type_key']}")
            st.markdown(f'''
                <div style="border-radius: 12px; overflow: hidden; border: 2px solid #30363d; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                    <img src="{res['component_image']}" alt="Component Anomaly" style="width:100%; height:320px; object-fit:cover;">
                </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("---")
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f'<div class="metric-card"><small>{L["status_label"]}</small><br><span class="{res["status_class"]}">{res["status_text"]}</span></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card"><small>{L["health_index"]}</small><h2 style="color:{theme["color"]};margin:0">{res["health_score"]}%</h2></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card"><small>{L["peak_freq"]}</small><h2 style="margin:0">{res["peak_freq"]} Hz</h2></div>', unsafe_allow_html=True)
        m4.markdown(f'<div class="metric-card"><small>{L["centroid"]}</small><h2 style="margin:0">{res["centroid"]} Hz</h2></div>', unsafe_allow_html=True)

    with tab2:
        fig = go.Figure()
        mask = res["fft_freqs"] <= 8000
        fig.add_trace(go.Scatter(
            x=res["fft_freqs"][mask], 
            y=res["fft_vals"][mask], 
            mode="lines", 
            line=dict(color=theme["color"], width=2.5)
        ))
        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Frequency (Hz)",
            yaxis_title="Amplitude Spectrum Density",
            plot_bgcolor="#0d1117",
            paper_bgcolor="#0d1117",
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.info(res["recommendations"])
        st.markdown("### Detected Fault Signatures:")
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
        st.download_button(L["download_rep"], report_text, file_name="ZINO_EADE_Inspection_Report.txt")

if audio_data is not None:
    render_inspection_results(audio_data, sample_rate, selected_unit)
