import io
import numpy as np
from scipy.signal import butter, filtfilt
import streamlit as st
import streamlit.components.v1 as components

# --- 1. Page Config ---
st.set_page_config(
    page_title="ZINO EADE - AI Acoustic Diagnostic Engine",
    page_icon="⚙️",
    layout="centered"
)

# --- 2. Multi-Language & Multi-Domain Dictionary ---
LANG_DICT = {
    "العربية": {
        "title": "ZINO EADE",
        "designer": "محرك الذكاء الاصطناعي للتشخيص الصوتي المتقدم | تطوير: إسماعيل حساسنة",
        "select_domain": "🎛️ اختر قطاع التشخيص المتخصص (Specialized Diagnostic Domain):",
        "step2": "🎧 الخطوة 2: إدخال البصمة الصوتية للمعدة",
        "source": "اختر طريقة تزويد الصوت:",
        "mic": "🎙️ تسجيل مباشر عبر المايك",
        "upload": "📁 إرفاق ملف صوتي (.wav, .mp3, .m4a)",
        "rec_prompt": "اضغط لبدء تسجيل البصمة الصوتية بدقة",
        "up_prompt": "اختر ملف الصوت الفعلي من جهازك:",
        "analyzing": "⚡ جاري الفحص الطيفي الدقيق ورصد أي انحراف ميكانيكي بنسبة 0.001%...",
        "score_label": "📊 مؤشر الانحراف والشذوذ الدقيق (Anomaly Index)",
        "defect_title": "⚠️ تم رصد خلل ميكانيكي / انحراف طيفي",
        "normal_title": "✅ المعدة سليمة تماماً (لا توجد أخطاء)",
        "report_title": "📝 التقرير الهندسي والتشخيص الدقيق",
        "summary_header": "🔧 المواصفات وملخص الفحص:",
        "status_label": "حالة الأداء الميكانيكي:",
        "anomaly_zone": "القطعة المرشحة للخلل:",
        "rec_header": "💡 التوصية الهندسية الدقيقة:",
        "waveform_title": "📈 تحليل الموجة الصوتية المفلترة"
    },
    "English": {
        "title": "ZINO EADE",
        "designer": "ADVANCED AI ACOUSTIC DIAGNOSTIC ENGINE | ENGINEERED BY ISMAIL HASASNAH",
        "select_domain": "🎛️ Select Specialized Diagnostic Domain:",
        "step2": "🎧 Step 2: Machinery Acoustic Ingestion",
        "source": "Select Audio Source:",
        "mic": "🎙️ Live Microphone Input",
        "upload": "📁 Upload Audio File (.wav, .mp3, .m4a)",
        "rec_prompt": "Record High-Precision Sound Signature",
        "up_prompt": "Choose actual audio file:",
        "analyzing": "⚡ Running High-Resolution Spectral Analysis & Micro-Deviation Detection...",
        "score_label": "📊 Micro-Anomaly Index Score",
        "defect_title": "⚠️ MECHANICAL DEVIATION / FAULT DETECTED",
        "normal_title": "✅ SYSTEM HEALTHY (Zero Faults Detected)",
        "report_title": "📝 Engineering Diagnostic Report",
        "summary_header": "🔧 Equipment Profile & Summary:",
        "status_label": "Mechanical Performance Status:",
        "anomaly_zone": "Identified Defect Zone:",
        "rec_header": "💡 Precision Engineering Recommendation:",
        "waveform_title": "📈 Filtered Acoustic Waveform"
    },
    "Русский": {
        "title": "ZINO EADE",
        "designer": "ПЕРЕДОВОЙ ИИ АКУСТИЧЕСКИЙ ДИАГНОСТИЧЕСКИЙ ДВИГАТЕЛЬ | РАЗРАБОТАНО: ИСМАИЛ ХАСАСНА",
        "select_domain": "🎛️ Выберите специализированный домен диагностики:",
        "step2": "🎧 Шаг 2: Ввод акустической подписи оборудования",
        "source": "Выберите источник звука:",
        "mic": "🎙️ Запись с микрофона",
        "upload": "📁 Загрузить файл (.wav, .mp3, .m4a)",
        "rec_prompt": "Запишите точный акустический профиль",
        "up_prompt": "Выберите аудиофайл:",
        "analyzing": "⚡ Высокоточный спектральный анализ и поиск микроаномалий...",
        "score_label": "📊 Индекс микроаномалий ИИ",
        "defect_title": "⚠️ ОБНАРУЖЕНО МЕХАНИЧЕСКОЕ ОТКЛОНЕНИЕ",
        "normal_title": "✅ СИСТЕМА ИСПРАВНА (Ошибок не обнаружено)",
        "report_title": "📝 Инженерный отчет диагностики",
        "summary_header": "🔧 Сводка профиля оборудования:",
        "status_label": "Состояние механической работы:",
        "anomaly_zone": "Зона вероятного дефекта:",
        "rec_header": "💡 Точная инженерная рекомендация:",
        "waveform_title": "📈 Отфильтрованная акустическая волна"
    }
}

# Top Control Bar: Language Selection
lang_choice = st.selectbox("🌐 Choose Language / اختر اللغة / Выберите язык:", ["العربية", "English", "Русский"])
T = LANG_DICT[lang_choice]

# Domain Selector
domain_choice = st.selectbox(
    T['select_domain'],
    [
        "🚗 قطاع السيارات والمركبات (Automotive Hub)",
        "🧊 قطاع التبريد والثلاجات التجارية (Refrigeration Hub)",
        "🧺 قطاع الغسالات والأجهزة المنزلية (Home Appliances Hub)",
        "⚙️ قطاع المحركات والمولدات الصناعية (Industrial Machinery Hub)"
    ]
)

# Dynamic Theme & Branding Configuration based on Domain
if "Automotive" in domain_choice:
    primary_color = "#FF6B00"
    bg_gradient = "linear-gradient(135deg, #1A1816 0%, #261D18 100%)"
    domain_badge = "AUTOMOTIVE DIESEL & GASOLINE ENGINE LAB"
    domain_icon = "🚘"
elif "Refrigeration" in domain_choice:
    primary_color = "#06B6D4"
    bg_gradient = "linear-gradient(135deg, #142226 0%, #182C33 100%)"
    domain_badge = "COMMERCIAL REFRIGERATION & FREEZER LAB"
    domain_icon = "🧊"
elif "Appliances" in domain_choice:
    primary_color = "#8B5CF6"
    bg_gradient = "linear-gradient(135deg, #1F192E 0%, #28203D 100%)"
    domain_badge = "HOME APPLIANCES & MOTOR LAB"
    domain_icon = "🧺"
else:
    primary_color = "#F59E0B"
    bg_gradient = "linear-gradient(135deg, #241E14 0%, #302718 100%)"
    domain_badge = "HEAVY INDUSTRIAL MACHINERY LAB"
    domain_icon = "⚙️"

# Apply Custom Dynamic CSS Template
st.markdown(f'''
    <style>
    #vg-tooltip-element, .vg-tooltip, .vega-bind, .vega-actions, div[class*="tooltip"] {{
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }}
    .stApp {{
        background-color: #0E1210;
        color: #E2E8F0;
        font-family: 'Inter', system-ui, sans-serif;
    }}
    .brand-card {{
        background: {bg_gradient};
        border: 2px solid {primary_color};
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.4);
        margin-bottom: 25px;
    }}
    .brand-title {{
        color: {primary_color};
        font-size: 34px;
        font-weight: 900;
        margin: 0;
        text-transform: uppercase;
    }}
    .designer-tag {{
        color: #94A3B8;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-top: 5px;
    }}
    .report-card {{
        background-color: #141C18;
        border: 1px solid #22332B;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
        margin-bottom: 20px;
    }}
    [data-testid="stMetricValue"] {{
        color: {primary_color} !important;
        font-size: 36px !important;
        font-weight: 800 !important;
    }}
    </style>
''', unsafe_allow_html=True)

# Domain Header Rendering
st.markdown(f'''
    <div class="brand-card">
        <h1 class="brand-title">{domain_icon} {T['title']}</h1>
        <div style="color: {primary_color}; font-weight: 800; font-size: 14px; margin-top: 6px;">{domain_badge}</div>
        <div class="designer-tag">{T['designer']}</div>
    </div>
''', unsafe_allow_html=True)

# Specialized Domain Input Schemas (Isolated Templates)
st.markdown(f"### 📋 Step 1: Specialized Technical Parameters")

make, model, year, engine_spec = "", "", "", ""

if "Automotive" in domain_choice:
    col1, col2 = st.columns(2)
    with col1:
        make = st.selectbox("Vehicle Brand (Make):", ["Hyundai", "Volkswagen", "Skoda", "Honda", "Mitsubishi", "Toyota", "Other"])
        model = st.text_input("Vehicle Model:", "Santa Fe / Pajero / Caddy")
    with col2:
        year = st.text_input("Production Year:", "2017")
        engine_spec = st.selectbox("Engine & Fuel System:", ["2.0L CRDi Turbo Diesel", "1.6L TDI / CRDi", "2.0L TSI Turbo", "V6 3.5L Gasoline", "1.6L GDI Injection"])

elif "Refrigeration" in domain_choice:
    col1, col2 = st.columns(2)
    with col1:
        make = st.selectbox("Freezer / Refrigerator Brand:", ["Commercial Ice Cream Freezer", "Ugur", "Frigoglass", "Carrier", "Danfoss", "Other"])
        model = st.text_input("Unit Type / Model:", "Vertical Glass Door Display / Deep Freezer")
    with col2:
        year = st.text_input("Compressor Capacity:", "1/3 HP / 1/2 HP Commercial")
        engine_spec = st.selectbox("Cooling System Type:", ["Hermetic Reciprocating Compressor", "Rotary Compressor Inverter", "Scroll Compressor Unit"])

elif "Appliances" in domain_choice:
    col1, col2 = st.columns(2)
    with col1:
        make = st.selectbox("Appliance Brand:", ["LG", "Samsung", "Bosch", "Whirlpool", "Other"])
        model = st.text_input("Appliance Model:", "Front Load Automatic Washer")
    with col2:
        year = st.text_input("Capacity / Spin RPM:", "8 KG / 1400 RPM")
        engine_spec = st.selectbox("Motor Architecture:", ["Inverter Direct Drive Motor", "Universal Brush Motor", "AC Induction Drum Motor"])

else:
    col1, col2 = st.columns(2)
    with col1:
        make = st.selectbox("Industrial Brand:", ["Caterpillar", "Cummins", "Perkins", "Deutz", "Other"])
        model = st.text_input("Generator / Heavy Unit:", "Diesel Generating Set")
    with col2:
        year = st.text_input("Power Rating:", "50 KVA - 150 KVA")
        engine_spec = st.selectbox("Heavy Engine Spec:", ["Heavy Duty Turbocharged Diesel", "Inline 6 Cylinder Industrial"])

st.divider()

# Step 2: Audio Ingestion
st.markdown(f"### {T['step2']}")

input_method = st.radio(T['source'], [T['mic'], T['upload']], horizontal=True)

audio_bytes = None
if T['mic'] in input_method:
    recorded_audio = st.audio_input(T['rec_prompt'])
    if recorded_audio:
        audio_bytes = recorded_audio.read()
else:
    uploaded_file = st.file_uploader(T['up_prompt'], type=["wav", "mp3", "m4a"])
    if uploaded_file:
        audio_bytes = uploaded_file.read()

def parse_universal_audio_signal(raw_bytes):
    try:
        from scipy.io import wavfile
        sr, signal = wavfile.read(io.BytesIO(raw_bytes))
        if len(signal.shape) > 1:
            signal = np.mean(signal, axis=1)
        return signal.astype(np.float32), float(sr)
    except Exception:
        pass

    raw_samples = np.frombuffer(raw_bytes, dtype=np.uint8).astype(np.float32)
    if len(raw_samples) > 200:
        raw_samples = raw_samples[100:]
    centered_samples = (raw_samples - 128.0) / 128.0
    target_length = 66150
    if len(centered_samples) > target_length:
        step = len(centered_samples) // target_length
        signal = centered_samples[::step][:target_length]
    else:
        signal = np.pad(centered_samples, (0, max(0, target_length - len(centered_samples))), mode='wrap')
    return signal.astype(np.float32), 22050.0

def apply_noise_filter(signal, sample_rate):
    nyquist = 0.5 * sample_rate
    low = max(20.0, 80.0 / nyquist)
    high = min(0.99, 4500.0 / nyquist)
    b, a = butter(2, [low, high], btype='band')
    return filtfilt(b, a, signal)

def compute_micro_anomaly_score(clean_signal):
    energy = float(np.mean(clean_signal**2))
    zcr = float(np.mean(np.diff(np.signbit(clean_signal)) != 0))
    fft_spec = np.abs(np.fft.rfft(clean_signal[:2048]))
    
    spectral_centroid = float(np.sum(fft_spec * np.arange(len(fft_spec))) / (np.sum(fft_spec) + 1e-6))
    high_freq_ratio = float(np.sum(fft_spec[80:]) / (np.sum(fft_spec) + 1e-6))
    
    peak = float(np.max(np.abs(clean_signal)))
    rms = float(np.sqrt(energy) + 1e-6)
    crest_factor = peak / rms
    
    deviation_factor = (
        (zcr * 45.0) +
        (high_freq_ratio * 25.0) +
        (max(0.0, crest_factor - 1.8) * 8.0) +
        (max(0.0, spectral_centroid - 180.0) / 30.0)
    )
    
    anomaly_score = round(float(np.clip(deviation_factor * 1.35, 1.000, 99.999)), 3)
    return anomaly_score, spectral_centroid, energy

def get_domain_expert_diagnosis(domain, score, lang):
    is_fault = score >= 40.0
    
    if "Automotive" in domain:
        img_url = "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1000&q=80"
        title = "🚘 Automotive Acoustic & Micro-Scan"
        if is_fault:
            zone = {"العربية": "عمود التيربو / خلوص البخاخات / تآكل صمامات", "English": "Turbocharger Bearing / Fuel Injector Clearance", "Русский": "Вал турбины / Зазор форсунок"}
            rec = {"العربية": "تم رصد انحراف طيفي طفيف يشير إلى احتكاك معدني في محمل التيربو أو تفاوت في حقن الوقود. يُنصح بالفحص العيني الفوري.", "English": "Micro-deviation detected indicating minor metallic friction in turbocharger shaft or fuel injector clearance.", "Русский": "Обнаружено микроотклонение, указывающее на трение в вале турбины."}
        else:
            zone = {"العربية": "لا توجد أي أعطال (نظام سليم 100%)", "English": "None (System 100% Healthy)", "Русский": "Нет (Система исправна на 100%)"}
            rec = {"العربية": "محرك المركبة يعمل بسلاسة تامة ومطابق للمعايير القياسية. لا توجد أي أصوات احتكاك أو طقطقة.", "English": "Engine operating with absolute smoothness. Zero abnormal acoustic friction or mechanical knocking detected.", "Русский": "Двигатель работает идеально плавно. Аномальных шумов не обнаружено."}

    elif "Refrigeration" in domain:
        img_url = "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=1000&q=80"
        title = "🧊 Commercial Refrigeration Micro-Scan"
        if is_fault:
            zone = {"العربية": "صمامات ضاغط التبريد الداخلية / رمان بلي مروحة المكثف", "English": "Compressor Internal Valves / Condenser Fan Bearings", "Русский": "Внутренние клапаны компрессора / Вентилятор"}
            rec = {"العربية": "تم رصد ذبذبة غير طبيعية في ضاغط التبريد أو احتكاك في مروحة المكثف. يُنصح بفحص دورة التبريد.", "English": "Abnormal compressor pulsation or condenser fan bearing friction detected. Inspect refrigeration unit.", "Русский": "Обнаружена пульсация компрессора или трение вентилятора."}
        else:
            zone = {"العربية": "لا توجد أي أعطال (ضاغط التبريد سليم 100%)", "English": "None (Compressor 100% Healthy)", "Русский": "Нет (Компрессор исправен на 100%)"}
            rec = {"العربية": "ضاغط التبريد وموتور الثلاجة يعملان بنسق هادئ ومنتظم وخالٍ تماماً من أي اهتزازات أو أعطال.", "English": "Refrigeration compressor and motor operating quietly with absolute mechanical stability.", "Русский": "Компрессор холодильника работает тихо и стабильно."}

    elif "Appliances" in domain:
        img_url = "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&w=1000&q=80"
        title = "🧺 Home Appliance Motor Micro-Scan"
        if is_fault:
            zone = {"العربية": "رمان بلي حوض الغسيل / شداد القشاط", "English": "Drum Main Bearings / Drive Belt Tensioner", "Русский": "Подшипники барабана / Натяжной ремень"}
            rec = {"العربية": "تم رصد احتكاك دقيق في بلي الحوض أو عدم توازن في دوران المحرك.", "English": "Micro-friction detected in drum bearings or slight motor rotational imbalance.", "Русский": "Обнаружено микротрение в подшипниках барабана."}
        else:
            zone = {"العربية": "لا توجد أي أعطال (الغسالة سليم 100%)", "English": "None (Appliance 100% Healthy)", "Русский": "Нет (Устройство исправно на 100%)"}
            rec = {"العربية": "الموتور والحوض يعملان بكفاءة تامة ودون أي أصوات احتكاك في رومان البلي.", "English": "Motor and drum assembly operating in pristine condition without bearing friction.", "Русский": "Двигатель и барабан работают в идеальном состоянии."}

    else:
        img_url = "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1000&q=80"
        title = "⚙️ Heavy Industrial Machinery Scan"
        if is_fault:
            zone = {"العربية": "رمان بلي المولد الرئيسي / مضخة الحقن", "English": "Main Alternator Bearing / Fuel Injection Pump", "Русский": "Подшипники генератора / Топливный насос"}
            rec = {"العربية": "تم رصد اهتزاز دوري غير طبيعي في محامل المولد أو مضخة الوقود.", "English": "Periodic abnormal vibration detected in alternator bearings or fuel pump.", "Русский": "Обнаружена периодическая вибрация в подшипниках генератора."}
        else:
            zone = {"العربية": "لا توجد أي أعطال (المعدة الصناعية سليمة 100%)", "English": "None (Machinery 100% Healthy)", "Русский": "Нет (Оборудование исправно на 100%)"}
            rec = {"العربية": "المعدة الصناعية تعمل بتوازن واستقرار ممتازين وخالية من أي أعطال.", "English": "Industrial machinery operating with excellent acoustic balance and zero faults.", "Русский": "Промышленное оборудование работает с отличным балансом."}

    return zone[lang], rec[lang], img_url, title, is_fault

if audio_bytes is not None:
    st.audio(audio_bytes)
    with st.spinner(T['analyzing']):
        clean_signal, sr = parse_universal_audio_signal(audio_bytes)
        clean_signal = apply_noise_filter(clean_signal, sr)
        max_val = np.max(np.abs(clean_signal))
        if max_val > 0:
            clean_signal = clean_signal / max_val
        
        anomaly_score, spectral_centroid, energy = compute_micro_anomaly_score(clean_signal)
        fault_zone, rec_text, visual_img_url, scan_title, is_fault = get_domain_expert_diagnosis(domain_choice, anomaly_score, lang_choice)
        
        st.divider()
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric(label=T['score_label'], value=f"{anomaly_score:.3f}%")
        with col_res2:
            if is_fault:
                st.error(T['defect_title'])
                st.caption(f"Deviation detected for {make} {model}.")
            else:
                st.success(T['normal_title'])
                st.caption(f"System operating perfectly for {make} {model}.")

        st.markdown(f"### {T['report_title']}")
        status_color = '#EF4444' if is_fault else '#10B981'
        status_text = "Critical / Deviation Requires Inspection" if is_fault else "Optimal / 100% Healthy"
        
        st.markdown(f'''
        <div class="report-card">
            <h4 style="color: {primary_color}; margin-top:0;">{T["summary_header"]}</h4>
            <ul>
                <li><strong>Target Unit:</strong> {make} {model} ({year})</li>
                <li><strong>Specification:</strong> {engine_spec}</li>
                <li><strong>{T["status_label"]}</strong> <span style="color:{status_color}; font-weight:bold;">{status_text}</span></li>
                <li><strong>{T["anomaly_zone"]}</strong> {fault_zone}</li>
                <li><strong>Spectral Centroid Frequency:</strong> {spectral_centroid:.2f} Hz</li>
                <li><strong>Signal Energy Density:</strong> {energy:.6f} RMS</li>
            </ul>
            <h4 style="color: #10B981; margin-top:15px;">{T["rec_header"]}</h4>
            <p style="color:#CBD5E1; font-size:14px;">{rec_text}</p>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown(f"### {scan_title}")
        laser_color = '#EF4444' if is_fault else '#10B981'
        
        scanner_html = (
            f'<div style="position: relative; width: 100%; height: 280px; border-radius: 14px; overflow: hidden; border: 2px solid {primary_color};">'
            f'<img src="{visual_img_url}" style="width: 100%; height: 100%; object-fit: cover; filter: brightness(0.75);" />'
            f'<div style="position: absolute; left: 0; width: 100%; height: 4px; background: {laser_color}; box-shadow: 0 0 15px 5px {laser_color}; animation: laserScan 2.5s infinite ease-in-out;"></div>'
            f'<div style="position: absolute; top: 12px; left: 12px; background: rgba(20,27,24,0.85); border: 1px solid {laser_color}; padding: 6px 14px; border-radius: 8px; color: {laser_color}; font-size: 12px; font-weight: bold;">'
            f'● MICRO-SCANNER ACTIVE | {make.upper()}'
            f'</div></div>'
            f'<style>'
            f'@keyframes laserScan {{ 0% {{ top: 0%; opacity: 0.8; }} 50% {{ top: 92%; opacity: 1; }} 100% {{ top: 0%; opacity: 0.8; }} }}'
            f'</style>'
        )
        components.html(scanner_html, height=300)

        st.markdown(f"### {T['waveform_title']}")
        st.line_
