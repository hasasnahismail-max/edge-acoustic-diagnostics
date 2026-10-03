import io, numpy as np, plotly.graph_objects as go, scipy.io.wavfile as wavfile, streamlit as st

HAS_LIB, HAS_SF, HAS_PD = False, False, False
try: import librosa; HAS_LIB = True
except: pass
try: import soundfile as sf; HAS_SF = True
except: pass
try: from pydub import AudioSegment; HAS_PD = True
except: pass

st.set_page_config(page_title="ZINO EADE", page_icon="⚡", layout="wide")

I18N = {
    "العربية": {
        "designer": "تصميم وتطوير المهندس: إسماعيل حساسنة (Ismail Hasasna)",
        "sub": "المنظومة الذكية الشاملة للتشخيص الصوتي لأعطال المحركات",
        "cat_title": "🎯 اختر القطاع المطلوب لفحصه:", "select_unit": "اختر الطراز والمحرك المباشر:",
        "audio_src": "مصدر الصوت:", "up_mode": "رفع ملف صوتي (MP3, WAV, M4A, OGG, FLAC)", "demo_mode": "محاكي الموجات الهندسي (Demo)",
        "btn_run": "🚀 بدء المسح والتشخيص المباشر", "v_tab": "📷 المسح البصري", "f_tab": "📈 التحليل الطيفي",
        "r_tab": "🔧 التوصيات والقطع", "rep_tab": "📑 التقرير الشامل", "healthy": "أداء منتظم وسليم", "critical": "يلزم الصيانة المباشرة",
        "cats": {"السيارات والمركبات": "السيارات والمركبات", "الثلاجات والتبريد": "الثلاجات والتبريد", "الأجهزة الكهربائية": "الأجهزة الكهربائية", "الماكينات والمعدات": "الماكينات والمعدات"}
    },
    "English": {
        "designer": "Designed & Developed by Engineer: Ismail Hasasna",
        "sub": "Universal AI-Powered Acoustic Diagnostic Workstation",
        "cat_title": "🎯 Select Sector for Acoustic Scan:", "select_unit": "Select Model & Engine:",
        "audio_src": "Audio Source:", "up_mode": "Upload Audio File (MP3, WAV, M4A, OGG, FLAC)", "demo_mode": "Synthetic Wave Simulator (Demo)",
        "btn_run": "🚀 Start Live Scan & Diagnostics", "v_tab": "📷 Visual Scan", "f_tab": "📈 Spectral Analysis",
        "r_tab": "🔧 Recommendations", "rep_tab": "📑 Inspection Report", "healthy": "Healthy / Normal Operation", "critical": "Critical / Inspection Required",
        "cats": {"السيارات والمركبات": "Automotive & Vehicles", "الثلاجات والتبريد": "Refrigeration & HVAC", "الأجهزة الكهربائية": "Electrical Appliances", "الماكينات والمعدات": "Heavy Machinery"}
    },
    "Русский": {
        "designer": "Разработано инженером: Исмаил Хасасна (Ismail Hasasna)",
        "sub": "Универсальная акустическая диагностическая платформа для двигателей",
        "cat_title": "🎯 Выберите сектор для сканирования:", "select_unit": "Выберите модель и двигатель:",
        "audio_src": "Источник аудиосигнала:", "up_mode": "Загрузить аудиофайл (MP3, WAV, M4A, OGG, FLAC)", "demo_mode": "Инженерный симулятор волн (Демо)",
        "btn_run": "🚀 Запустить сканирование и диагностику", "v_tab": "📷 Визуальный сканер", "f_tab": "📈 Спектральный анализ",
        "r_tab": "🔧 Рекомендации", "rep_tab": "📑 Инженерный отчет", "healthy": "Исправно / Нормальный режим", "critical": "Критично / Требуется ремонт",
        "cats": {"السيارات والمركبات": "Автомобили и транспорт", "الثلاجات والتبريد": "Холодильное оборудование", "الأجهزة الكهربائية": "Электроприборы", "الماكينات والمعدات": "Тяжелая техника"}
    }
}

lang = st.sidebar.selectbox("🌐 Language / اللغة / Язык", ["العربية", "English", "Русский"])
L = I18N[lang]

THEMES = {
    "السيارات والمركبات": {"color": "#ff7b00", "glow": "rgba(255,123,0,0.25)", "icon": "🚗"},
    "الثلاجات والتبريد": {"color": "#0099ff", "glow": "rgba(0,153,255,0.25)", "icon": "🧊"},
    "الأجهزة الكهربائية": {"color": "#a855f7", "glow": "rgba(168,85,247,0.25)", "icon": "🔌"},
    "الماكينات والمعدات": {"color": "#94a3b8", "glow": "rgba(148,163,184,0.25)", "icon": "⚙️"}
}

if "selected_cat" not in st.session_state: st.session_state["selected_cat"] = "السيارات والمركبات"
cur_cat = st.session_state["selected_cat"]
th = THEMES[cur_cat]

st.markdown(f"""<style>
.stApp {{ background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%); color: #c9d1d9; }}
.th-head {{ color: {th['color']} !important; text-shadow: 0 0 12px {th['glow']}; font-weight: 800; text-align: center; font-size: 2.2rem; }}
.des-tag {{ color: #58a6ff; font-weight: 600; text-align: center; margin-bottom: 15px; }}
.m-card {{ background: rgba(22,27,34,0.85); border: 2px solid {th['color']}; border-radius: 12px; padding: 14px; box-shadow: 0 4px 15px {th['glow']}; margin-bottom: 10px; }}
.stButton>button {{ background: linear-gradient(90deg, {th['color']} 0%, #238636 100%) !important; color: #fff !important; font-weight: bold; border-radius: 8px; border: none; padding: 10px; width: 100%; }}
</style>""", unsafe_allow_html=True)

IMGS = {
    "car": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=800&q=80",
    "hyundai": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=800&q=80",
    "pajero": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800&q=80",
    "fridge": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&q=80",
    "washer": "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=800&q=80",
    "pump": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80",
    "jcb": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=800&q=80",
    "inj": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=600&q=80",
    "turbo": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=600&q=80",
    "bear": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=600&q=80",
    "valve": "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=600&q=80",
    "belt": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&q=80",
    "ok": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=600&q=80"
}

DB = {}
auto_models = [
    ("VW Caddy 1.6 TDI (تنفس طبيعي / بدون تيربو)", "Volkswagen", "Caddy 1.6 TDI NA", "1.6L TDI Non-Turbo", False, IMGS["car"]),
    ("VW Caddy 2.0 TDI (شاحن تيربو)", "Volkswagen", "Caddy 2.0 TDI Turbo", "2.0L TDI Turbocharged", True, IMGS["car"]),
    ("VW Golf 1.4 TSI (بنزين تيربو)", "Volkswagen", "Golf VII 1.4 TSI", "1.4L TSI Turbo", True, IMGS["car"]),
    ("VW Polo 1.2 MPI (بدون تيربو)", "Volkswagen", "Polo 1.2 MPI", "1.2L MPI NA Engine", False, IMGS["car"]),
    ("VW Passat 2.0 TDI (تيربو ديزل)", "Volkswagen", "Passat B8 2.0 TDI", "2.0L TDI Clean Diesel", True, IMGS["car"]),
    ("VW Jetta 1.6 MPI (بدون تيربو)", "Volkswagen", "Jetta 1.6 MPI", "1.6L Multi-Point NA", False, IMGS["car"]),
    ("VW Crafter 2.0 TDI (تجاري تيربو)", "Volkswagen", "Crafter Van 2.0 TDI", "2.0L BiTDI Turbo Van", True, IMGS["car"]),
    ("Hyundai Santa Fe 2.2 CRDi (تيربو ديزل)", "Hyundai", "Santa Fe 2.2 CRDi", "2.2L CRDi VGT Turbo", True, IMGS["hyundai"]),
    ("Hyundai Tucson 1.6 T-GDI (تيربو بنزين)", "Hyundai", "Tucson 1.6 T-GDI", "1.6L Turbo GDI", True, IMGS["hyundai"]),
    ("Hyundai Elantra 1.6 MPI (بدون تيربو)", "Hyundai", "Elantra 1.6 MPI", "1.6L Gamma MPI NA", False, IMGS["hyundai"]),
    ("Hyundai Accent 1.4 MPI (بدون تيربو)", "Hyundai", "Accent 1.4 MPI", "1.4L Kappa MPI NA", False, IMGS["hyundai"]),
    ("Hyundai H-1 Starex 2.5 CRDi (تيربو)", "Hyundai", "H-1 Starex 2.5 CRDi", "2.5L Commercial Turbo", True, IMGS["hyundai"]),
    ("Mitsubishi Pajero V20 3.4L V6 (بنزين - جير عادي)", "Mitsubishi", "Pajero V20 3.4L V6 NA Manual", "3.4L 6G74 V6 NA Engine", False, IMGS["pajero"]),
    ("Mitsubishi Pajero V80 3.2 DI-D (تيربو ديزل)", "Mitsubishi", "Pajero V80 3.2 DI-D Turbo", "3.2L Common Rail Turbo", True, IMGS["pajero"]),
    ("Mitsubishi L200 2.4 DI-D (تيربو ديزل)", "Mitsubishi", "L200 Pickup 2.4 DI-D", "2.4L MIVEC Turbo Diesel", True, IMGS["pajero"]),
    ("Mitsubishi Lancer EX 1.8 MIVEC (بدون تيربو)", "Mitsubishi", "Lancer EX 1.8 MIVEC", "1.8L 4B10 MIVEC NA Engine", False, IMGS["pajero"])
]

for name, b, m, s, turbo, img in auto_models:
    bands = {"bearing_wear": (20, 350), "belt_squeal": (700, 2000), "valve_clearance": (1000, 3000), "injector_clatter": (3000, 8000)}
    if turbo: bands["turbo_shaft"] = (1400, 5200)
    DB[name] = {"cat": "السيارات والمركبات", "brand": b, "model": m, "specs": s, "turbo": turbo, "img": img, "bands": bands}

DB["ضاغط ثلاجة منزلي (Inverter Refrigerator)"] = {"cat": "الثلاجات والتبريد", "brand": "LG / GE", "model": "Smart Inverter R600a", "specs": "Variable Speed Unit", "turbo": False, "img": IMGS["fridge"], "bands": {"bearing_wear": (20, 280), "compressor_valves": (850, 2400)}}
DB["محرك غسالة ملابس (Direct Drive Motor)"] = {"cat": "الأجهزة الكهربائية", "brand": "Samsung / Bosch", "model": "BLDC Direct Drive", "specs": "Inverter Motor Assembly", "turbo": False, "img": IMGS["washer"], "bands": {"bearing_wear": (30, 320), "belt_squeal": (700, 1900)}}
DB["مضخة مياه كهربائية (Electric Water Pump 2HP)"] = {"cat": "الأجهزة الكهربائية", "brand": "Pedrollo / Grundfos", "model": "CPM-158 Pump", "specs": "2.0 HP Single-Phase", "turbo": False, "img": IMGS["pump"], "bands": {"bearing_wear": (20, 260), "pump_impeller": (900, 2700)}}
DB["محرك حفار JCB (JCB EcoMAX 4.4L Turbo)"] = {"cat": "الماكينات والمعدات", "brand": "JCB", "model": "EcoMAX 4.4L Diesel", "specs": "Heavy Duty Turbo Engine", "turbo": True, "img": IMGS["jcb"], "bands": {"bearing_wear": (20, 280), "turbo_shaft": (1400, 4800), "injector_clatter": (2200, 7500)}}

def read_audio(uf):
    bd = uf.read()
    if HAS_LIB:
        try: return librosa.load(io.BytesIO(bd), sr=None, mono=True)[0].astype(np.float32), 22050
        except: pass
    if HAS_SF:
        try: d, sr = sf.read(io.BytesIO(bd)); return (np.mean(d, axis=1) if d.ndim > 1 else d).astype(np.float32), sr
        except: pass
    try:
        sr, d = wavfile.read(io.BytesIO(bd))
        if d.ndim > 1: d = np.mean(d, axis=1)
        return (d / (32768.0 if d.dtype == np.int16 else 2147483648.0)).astype(np.float32), sr
    except: return None, None

def run_diag(audio, sr, unit_key):
    u = DB[unit_key]
    fft_vals = np.abs(np.fft.rfft(audio))
    fft_freqs = np.fft.rfftfreq(len(audio), 1.0 / sr)
    peak_f = float(fft_freqs[np.argmax(fft_vals)])
    p_tot = np.sum(fft_vals)
    centroid = float(np.sum(fft_freqs * fft_vals) / p_tot) if p_tot > 0 else 0.0

    faults, comp_img, fault_name, score = [], IMGS["ok"], L["healthy"], 100
    b = u["bands"]

    if "bearing_wear" in b and b["bearing_wear"][0] <= peak_f <= b["bearing_wear"][1]:
        faults.append("Bearing Wear / تآكل محامل الكرنك"); comp_img, fault_name, score = IMGS["bear"], "Crank Bearings / المحامل", 42
    elif "compressor_valves" in b and b["compressor_valves"][0] <= peak_f <= b["compressor_valves"][1]:
        faults.append("Compressor Reed Valves / صمامات الضاغط"); comp_img, fault_name, score = IMGS["ok"], "Reed Valves / صمامات الضاغط", 38
    elif "belt_squeal" in b and b["belt_squeal"][0] <= peak_f <= b["belt_squeal"][1]:
        faults.append("Belt Squeal / انزلاق سير الحركة"); comp_img, fault_name, score = IMGS["belt"], "Drive Belt / سير الحركة", 65
    elif "valve_clearance" in b and b["valve_clearance"][0] <= peak_f <= b["valve_clearance"][1]:
        faults.append("Valvetrain Deviation / اتساع صمامات المحرك"); comp_img, fault_name, score = IMGS["valve"], "Valvetrain / الصمامات", 50
    elif "injector_clatter" in b and b["injector_clatter"][0] <= peak_f <= b["injector_clatter"][1]:
        faults.append("Injector Clatter / خلل بخاخات الوقود"); comp_img, fault_name, score = IMGS["inj"], "Injectors / البخاخات", 45
    elif u["turbo"] and "turbo_shaft" in b and b["turbo_shaft"][0] <= peak_f <= b["turbo_shaft"][1]:
        faults.append("Turbo Shaft Friction / احتكاك عمود التيربو"); comp_img, fault_name, score = IMGS["turbo"], "Turbo Shaft / التيربو", 25

    return {"unit": f"{u['brand']} {u['model']}", "cat": u["cat"], "specs": u["specs"], "unit_img": u["img"], "comp_img": comp_img,
            "fault_name": fault_name, "status": L["critical"] if faults else L["healthy"], "score": score,
            "peak_f": round(peak_f, 1), "centroid": round(centroid, 1), "faults": faults, "freqs": fft_freqs, "vals": fft_vals}

st.markdown(f'<div class="th-head">⚡ ZINO EADE</div>', unsafe_allow_html=True)
st.markdown(f'<div class="des-tag">{L["designer"]}<br><small style="color:#8b949e">{L["sub"]}</small></div>', unsafe_allow_html=True)

st.markdown(f"### {L['cat_title']}")
cols = st.columns(4)
for idx, (cat, t_info) in enumerate(THEMES.items()):
    is_act = (cat == cur_cat)
    with cols[idx]:
        st.markdown(f'<div style="background:rgba(22,27,34,0.9); border:2px solid {t_info["color"] if is_act else "#30363d"}; border-radius:10px; padding:10px; text-align:center;"><h4 style="color:{t_info["color"]} !important; margin:0;">{t_info["icon"]} {L["cats"].get(cat, cat)}</h4></div>', unsafe_allow_html=True)
        if st.button(f"{t_info['icon']} Select", key=f"cat_{idx}"):
            st.session_state["selected_cat"] = cat; st.rerun()

st.markdown("---")
filtered_units = {k: v for k, v in DB.items() if v["cat"] == cur_cat}

st.sidebar.markdown(f"<h3 style='color:{th['color']}'>{th['icon']} {L['cats'].get(cur_cat, cur_cat)}</h3>", unsafe_allow_html=True)
selected_unit = st.sidebar.selectbox(L["select_unit"], list(filtered_units.keys()))
source_mode = st.sidebar.radio(L["audio_src"], (L["up_mode"], L["demo_mode"]))

audio_file, synthetic_fault = None, "bearing_wear"
if source_mode == L["up_mode"]: audio_file = st.sidebar.file_uploader("Upload:", type=["wav", "mp3", "m4a", "ogg", "flac"])
else: synthetic_fault = st.sidebar.selectbox("Fault Mode:", ["bearing_wear", "turbo_shaft", "healthy"])

if st.sidebar.button(L["btn_run"]):
    a_data, sr = None, 22050
    if source_mode == L["up_mode"]:
        if audio_file: a_data, sr = read_audio(audio_file)
        else: st.warning("⚠️ Please upload an audio file first.")
    else:
        t = np.linspace(0, 3.0, int(22050 * 3.0))
        sig = 0.45 * np.sin(2 * np.pi * 180 * t) if synthetic_fault == "bearing_wear" else (0.5 * np.sin(2 * np.pi * 3200 * t) if synthetic_fault == "turbo_shaft" else 0.0)
        a_data, sr = (0.2 * np.sin(2 * np.pi * 50 * t) + sig + np.random.normal(0, 0.02, len(t))).astype(np.float32), 22050

    if a_data is not None:
        res = run_diag(a_data, sr, selected_unit)
        t1, t2, t3, t4 = st.tabs([L["v_tab"], L["f_tab"], L["r_tab"], L["rep_tab"]])

        with t1:
            c1, c2 = st.columns(2)
            c1.markdown(f"#### ⚙️ {res['unit']}"); c1.image(res["unit_img"], use_container_width=True)
            c2.markdown(f"#### 🎯 {res['fault_name']}"); c2.image(res["comp_img"], use_container_width=True)
            st.markdown("---")
            m1, m2, m3, m4 = st.columns(4)
            m1.markdown(f'<div class="m-card"><small>Status</small><br><b>{res["status"]}</b></div>', unsafe_allow_html=True)
            m2.markdown(f'<div class="m-card"><small>Health Index</small><h3 style="color:{th["color"]};margin:0">{res["score"]}%</h3></div>', unsafe_allow_html=True)
            m3.markdown(f'<div class="m-card"><small>Peak Freq</small><h3 style="margin:0">{res["peak_f"]} Hz</h3></div>', unsafe_allow_html=True)
            m4.markdown(f'<div class="m-card"><small>Centroid</small><h3 style="margin:0">{res["centroid"]} Hz</h3></div>', unsafe_allow_html=True)

        with t2:
            fig = go.Figure()
            mask = res["freqs"] <= 8000
            fig.add_trace(go.Scatter(x=res["freqs"][mask], y=res["vals"][mask], mode="lines", line=dict(color=th["color"], width=2)))
            fig.update_layout(template="plotly_dark", xaxis_title="Frequency (Hz)", yaxis_title="Amplitude")
            st.plotly_chart(fig, use_container_width=True)

        with t3:
            st.info(f"Spectral Peak: {res['peak_f']} Hz. Recommended component inspection.")
            for f in res["faults"]: st.write(f"• **{f}**")

        with t4:
            rep = f"""==================================================
ZINO EADE ACOUSTIC DIAGNOSTIC INSPECTION REPORT
{L['designer']}
==================================================
Target Unit       : {res['unit']}
Engineering Class : {res['cat']}
Specification     : {res['specs']}
Health Status     : {res['status']}
Health Index      : {res['score']}%
--------------------------------------------------
ACOUSTIC METRICS: Peak Freq: {res['peak_f']} Hz | Centroid: {res['centroid']} Hz
DETECTED FAULTS : {', '.join(res['faults'])}
==================================================
Platform Designer : Ismail Hasasna (إسماعيل حساسنة)
"""
            st.code(rep, language="text")
            st.download_button("📥 Download Report (TXT)", rep, file_name="ZINO_EADE_Report.txt")
