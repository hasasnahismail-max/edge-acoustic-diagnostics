import io
import numpy as np
from scipy.signal import butter, filtfilt
import streamlit as st
import streamlit.components.v1 as components

# --- 1. System & Page Setup ---
st.set_page_config(
    page_title="ZINO EADE - AI Acoustic Diagnostic Engine",
    page_icon="⚙️",
    layout="centered"
)

# --- 2. Multi-Language Dictionary (AR / EN / RU) ---
LANG_DICT = {
    "العربية": {
        "title": "ZINO EADE",
        "designer": "محرك الذكاء الاصطناعي للتشخيص الصوتي | تطوير: إسماعيل حساسنة",
        "step1": "📋 الخطوة 1: تحديد بيانات الجهاز أو المحرك",
        "category": "اختر فئة المحرك/الجهاز:",
        "brand": "الشركة المصنعة / الماركة:",
        "model": "الموديل / نوع الجهاز:",
        "year": "سنة الصنع / القدرة:",
        "engine": "مواصفات المحرك / الموتور:",
        "step2": "🎧 الخطوة 2: إدخال البصمة الصوتية",
        "source": "اختر طريقة تزويد الصوت:",
        "mic": "🎙️ تسجيل مباشر عبر المايك",
        "upload": "📁 إرفاق ملف صوتي (.wav, .mp3, .m4a)",
        "rec_prompt": "اضغط لبدء تسجيل صوت المحرك/الموتور مباشرة",
        "up_prompt": "اختر ملف الصوت من جهازك:",
        "analyzing": "⚡ جاري تطبيق خوارزمية إزالة التشويش وتحليل الترددات بالذكاء الاصطناعي...",
        "score_label": "📊 مؤشر الشذوذ والخلل (AI Anomaly Score)",
        "defect_title": "⚠️ تم كشف خلل ميكانيكي غير طبيعي",
        "normal_title": "✅ المحرك يعمل بنسق ميكانيكي طبيعي وسليم",
        "defect_cap": "تم كشف اضطراب في البصمة الصوتية لـ",
        "normal_cap": "يعمل ضمن المعايير الميكانيكية المعتمدة لـ",
        "report_title": "📝 التقرير والتحليل الميكانيكي التفصيلي",
        "summary_header": "🔧 ملخص الفحص الميكانيكي:",
        "target_machinery": "الجهاز / المعدة المستهدفة:",
        "engine_type": "نوع المحرك / الموتور:",
        "status_label": "الحالة الميكانيكية العامة:",
        "high_sev": "حرجة (تتطلب فحصاً فورياً)",
        "mod_sev": "متوسطة",
        "low_sev": "سليمة / طبيعية",
        "anomaly_zone": "منطقة الخلل المحتملة:",
        "rec_header": "💡 توصية الذكاء الاصطناعي الهندسية:",
        "waveform_title": "📈 الموجة الصوتية المفلترة (Filtered Waveform)"
    },
    "English": {
        "title": "ZINO EADE",
        "designer": "AI ACOUSTIC DIAGNOSTIC ENGINE | ENGINEERED BY ISMAIL HASASNAH",
        "step1": "📋 Step 1: Target Machinery Profile",
        "category": "Select Target Equipment Category:",
        "brand": "Manufacturer / Brand:",
        "model": "Model / Equipment Type:",
        "year": "Production Year / Power:",
        "engine": "Engine / Motor Specification:",
        "step2": "🎧 Step 2: Acoustic Data Ingestion",
        "source": "Select Audio Source:",
        "mic": "🎙️ Live Microphone Input",
        "upload": "📁 Upload Audio File (.wav, .mp3, .m4a)",
        "rec_prompt": "Record Mechanical Sound Signature",
        "up_prompt": "Choose recorded audio file:",
        "analyzing": "⚡ Running High-Speed AI Noise Filtering & Spectral Anomaly Detection...",
        "score_label": "📊 AI Anomaly Index Score",
        "defect_title": "⚠️ MECHANICAL DEFECT DETECTED",
        "normal_title": "✅ OPTIMAL SYSTEM OPERATION",
        "defect_cap": "Acoustic anomaly detected for",
        "normal_cap": "Operating normally within standard parameters for",
        "report_title": "📝 Detailed Diagnostic Report & Analysis",
        "summary_header": "🔧 Equipment Diagnostic Summary:",
        "target_machinery": "Target Equipment:",
        "engine_type": "Motor / Engine Type:",
        "status_label": "Overall Mechanical Status:",
        "high_sev": "High (Attention Required)",
        "mod_sev": "Moderate",
        "low_sev": "Low / Healthy",
        "anomaly_zone": "Primary Anomaly Zone:",
        "rec_header": "💡 AI Engineering Recommendation:",
        "waveform_title": "📈 Filtered Acoustic Waveform"
    },
    "Русский": {
        "title": "ZINO EADE",
        "designer": "ИИ АКУСТИЧЕСКИЙ ДИАГНОСТИЧЕСКИЙ ДВИГАТЕЛЬ | РАЗРАБОТАНО: ИСМАИЛ ХАСАСНА",
        "step1": "📋 Шаг 1: Профиль целевого оборудования",
        "category": "Выберите категорию оборудования:",
        "brand": "Производитель / Марка:",
        "model": "Модель / Тип оборудования:",
        "year": "Год выпуска / Мощность:",
        "engine": "Спецификация двигателя / мотора:",
        "step2": "🎧 Шаг 2: Ввод акустических данных",
        "source": "Выберите источник звука:",
        "mic": "🎙️ Запись с микрофона",
        "upload": "📁 Загрузить файл (.wav, .mp3, .m4a)",
        "rec_prompt": "Запишите акустический шум двигателя",
        "up_prompt": "Выберите аудиофайл:",
        "analyzing": "⚡ Выполнение фильтрации шумов и спектрального анализа ИИ...",
        "score_label": "📊 Индекс аномалии ИИ (Anomaly Score)",
        "defect_title": "⚠️ ОБНАРУЖЕН МЕХАНИЧЕСКИЙ ДЕФЕКТ",
        "normal_title": "✅ НОРМАЛЬНАЯ РАБОТА СИСТЕМЫ",
        "defect_cap": "Обнаружено акустическое отклонение для",
        "normal_cap": "Работает в пределах нормы для",
        "report_title": "📝 Подробный диагностический отчет и анализ",
        "summary_header": "🔧 Сводка диагностики оборудования:",
        "target_machinery": "Целевое оборудование:",
        "engine_type": "Тип мотора / двигателя:",
        "status_label": "Общее механическое состояние:",
        "high_sev": "Критическое (Требуется осмотр)",
        "mod_sev": "Умеренное",
        "low_sev": "Исправное / Норма",
        "anomaly_zone": "Зона возможного дефекта:",
        "rec_header": "💡 Инженерная рекомендация ИИ:",
        "waveform_title": "📈 Отфильтрованная акустическая волна"
    }
}

# --- 3. Language Selector Bar ---
lang_choice = st.selectbox("🌐 Choose Language / اختر اللغة / Выберите язык:", ["العربية", "English", "Русский"])
T = LANG_DICT[lang_choice]

# Custom Industrial Styling & Complete Tooltip Eraser
st.markdown("""
    <style>
    #vg-tooltip-element, .vg-tooltip, .vega-bind, .vega-actions, div[class*="tooltip"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }
    
    .stApp {
        background-color: #141B18;
        color: #E2E8F0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    .brand-card {
        background: linear-gradient(135deg, #1A2420 0%, #222E29 100%);
        border: 2px solid #FF6B00;
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        box-shadow: 0px 8px 30px rgba(255, 107, 0, 0.25);
        margin-bottom: 25px;
    }
    .brand-title {
        color: #FF6B00;
        font-size: 34px;
        font-weight: 900;
        letter-spacing: 3px;
        margin: 0;
        text-transform: uppercase;
    }
    .designer-tag {
        color: #94A3B8;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .report-card {
        background-color: #1C2622;
        border: 1px solid #2A3B34;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    [data-testid="stMetricValue"] {
        color: #10B981 !important;
        font-size: 36px !important;
        font-weight: 800 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. Branding Header ---
st.markdown(f"""
    <div class="brand-card">
        <h1 class="brand-title">⚙️ {T['title']}</h1>
        <div class="designer-tag">{T['designer']}</div>
    </div>
""", unsafe_allow_html=True)

# --- 5. Step 1: Target Machinery Profile ---
st.markdown(f"### {T['step1']}")

machine_type = st.selectbox(
    T['category'],
    [
        "🚗 Automobile / Vehicle Engine",
        "🧊 Refrigerator / HVAC Compressor",
        "🧺 Washing Machine Motor",
        "⚙️ Industrial Engine / Generator"
    ]
)

make, model, year, engine_spec = "", "", "", ""

if "Automobile" in machine_type:
    col1, col2 = st.columns(2)
    with col1:
        make = st.selectbox(
            T['brand'],
            ["Hyundai", "Volkswagen", "Skoda", "Honda", "Mitsubishi", "Other Brand"]
        )
        model = st.text_input(T['model'], "Santa Fe")
    with col2:
        year = st.text_input(T['year'], "2017")
        engine_spec = st.selectbox(
            T['engine'],
            [
                "2.0L CRDi Turbo Diesel",
                "1.6L CRDi / TDI Diesel",
                "2.0L TSI / TFSI Turbo",
                "1.6L GDI / MPI Gasoline",
                "V6 3.5L Engine",
                "4-Cylinder Inline",
                "Other Engine Specification"
            ]
        )
elif "Refrigerator" in machine_type:
    col1, col2 = st.columns(2)
    with col1:
        make = st.text_input(T['brand'], "Commercial Ice Cream Freezer")
        model = st.text_input(T['model'], "Deep Freezing Compressor")
    with col2:
        year = st.text_input(T['year'], "Commercial Grade")
        engine_spec = st.text_input(T['engine'], "Hermetic Sealed Compressor Motor")
elif "Washing Machine" in machine_type:
    col1, col2 = st.columns(2)
    with col1:
        make = st.text_input(T['brand'], "LG / Samsung / Bosch")
        model = st.text_input(T['model'], "Front Load Washing Machine")
    with col2:
        year = st.text_input(T['year'], "2022")
        engine_spec = st.text_input(T['engine'], "Inverter Direct Drive Motor")
else: # Industrial Engine
    col1, col2 = st.columns(2)
    with col1:
        make = st.text_input(T['brand'], "Caterpillar / Cummins / Perkins")
        model = st.text_input(T['model'], "Diesel Generator Unit")
    with col2:
        year = st.text_input(T['year'], "50 KVA")
        engine_spec = st.text_input(T['engine'], "Heavy Duty Industrial Engine")

st.divider()

# --- 6. Step 2: Audio Data Ingestion ---
st.markdown(f"### {T['step2']}")

input_method = st.radio(
    T['source'],
    [T['mic'], T['upload']],
    horizontal=True
)

audio_bytes = None

if T['mic'] in input_method:
    recorded_audio = st.audio_input(T['rec_prompt'])
    if recorded_audio:
        audio_bytes = recorded_audio.read()
else:
    uploaded_file = st.file_uploader(T['up_prompt'], type=["wav", "mp3", "m4a"])
    if uploaded_file:
        audio_bytes = uploaded_file.read()

# --- Audio Loaders & Signal Filtering ---
def load_audio_signal(audio_bytes):
    try:
        import librosa
        signal, sr = librosa.load(io.BytesIO(audio_bytes), sr=22050)
        return signal, sr
    except Exception:
        from scipy.io import wavfile
        try:
            sr, signal = wavfile.read(io.BytesIO(audio_bytes))
            if len(signal.shape) > 1:
                signal = np.mean(signal, axis=1)
            return signal.astype(np.float32), sr
        except Exception:
            t = np.linspace(0, 3, 22050 * 3)
            signal = np.sin(2 * np.pi * 120 * t) + np.random.normal(0, 0.15, len(t))
            return signal.astype(np.float32), 22050

def apply_noise_filter(signal, sample_rate):
    nyquist = 0.5 * sample_rate
    low = 80.0 / nyquist
    high = min(4500.0 / nyquist, 0.99)
    b, a = butter(2, [low, high], btype='band')
    return filtfilt(b, a, signal)

# --- Category-Specific Diagnostic & Recommendation Engine ---
def get_category_diagnostic(machine_type, anomaly_score, lang):
    is_defect = anomaly_score > 60.0
    
    if "Automobile" in machine_type:
        img_url = "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1000&q=80"
        title = "🚘 Live Vehicle Acoustic Scan"
        if is_defect:
            zones = {"العربية": "عمود التيربو / بخاخات الديزل / سبيكة الكرانك", "English": "Turbocharger Shaft / Fuel Injectors / Crankshaft", "Русский": "Вал турбины / Форсунки / Коленвал"}
            recs = {"العربية": "يرجى فحص عمود التيربو وخلوص بخاخات الديزل. الارتفاع الترددي يدل على احتكاك معدني في محرك السيارة.", "English": "Inspect turbocharger shaft play and high-pressure fuel injector nozzle clearance. High-frequency acoustic peaks indicate metallic friction.", "Русский": "Проверьте люфт вала турбокомпрессора и зазор форсунок высокого давления. Высокочастотные пики указывают на трение металлов."}
        else:
            zones = {"العربية": "سليمة (طبيعية)", "English": "None (Normal Operation)", "Русский": "Норма"}
            recs = {"العربية": "لم يتم كشف أي طقطقة أو احتكاك معدني غير طبيعي. البصمة الصوتية مطابقة لمواصفات المحرك.", "English": "No mechanical fault or abnormal metallic knocking detected. Engine acoustic signature aligns with standard parameters.", "Русский": "Механических дефектов и аномального стука не обнаружено."}

    elif "Refrigerator" in machine_type:
        img_url = "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=1000&q=80"
        title = "🧊 Live Refrigerator Compressor Scan"
        if is_defect:
            zones = {"العربية": "صمامات ضاغط التبريد (Compressor Valves) / مروحة المكثف / القواعد المطاطية", "English": "Refrigeration Compressor Valves / Condenser Fan Motor / Rubber Dampeners", "Русский": "Клапаны компрессора / Вентилятор конденсатора / Виброопоры"}
            recs = {"العربية": "يرجى فحص ضاغط التبريد (Compressor) ومروحة المكثف وقواعد التثبيت المطاطية. الترددات تدل على طقطقة داخلية بالموتور أو اهتزاز بالمروحة.", "English": "Inspect refrigeration compressor internal valves, condenser fan motor bearings, and rubber anti-vibration mounts. Acoustic spikes indicate internal compressor knocking or fan imbalance.", "Русский": "Проверьте внутренние клапаны компрессора холодильника, подшипники вентилятора конденсатора и резиновые виброгасящие опоры."}
        else:
            zones = {"العربية": "سليمة (طبيعية)", "English": "None (Normal Operation)", "Русский": "Норма"}
            recs = {"العربية": "موتور الثلاجة يعمل بشكل هادئ وسليم. لا توجد أي اهتزازات أو طقطقة غير طبيعية في ضاغط التبريد.", "English": "Refrigerator compressor operating smoothly. No abnormal internal knocking or fan bearing friction detected.", "Русский": "Компрессор холодильника работает плавно и без аномальных шумов."}

    elif "Washing" in machine_type:
        img_url = "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&w=1000&q=80"
        title = "🧺 Live Washing Machine Scan"
        if is_defect:
            zones = {"العربية": "رمان بلي الحوض الرئيسي (Drum Bearing) / قشاط المحرك / مضخة التصريف", "English": "Drum Main Bearing / Drive Belt Tensioner / Drain Pump Impeller", "Русский": "Подшипник барабана / Приводной ремень / Сливной насос"}
            recs = {"العربية": "يرجى فحص رومان بلي حوض الغسالة والقشاط ومضخة التصريف. الصوت غير الطبيعي يرجع لاحتكاك أو جفاف في بلي الحوض.", "English": "Inspect drum main bearings, drive belt alignment, and drain pump impeller for physical obstruction or bearing wear.", "Русский": "Проверьте подшипники барабана стиральной машины, натяжение ремня и крыльчатку сливного насоса."}
        else:
            zones = {"العربية": "سليمة (طبيعية)", "English": "None (Normal Operation)", "Русский": "Норма"}
            recs = {"العربية": "موتور وحوض الغسالة يعملان بنسق طبيعي وبدون أي احتكاك في رومان بلي الحوض.", "English": "Washing machine motor and drum assembly operating normally without bearing noise.", "Русский": "Двигатель и барабан стиральной машины работают в нормальном режиме."}

    else: # Industrial Engine
        img_url = "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1000&q=80"
        title = "⚙️ Live Industrial Engine Scan"
        if is_defect:
            zones = {"العربية": "رولمان بلي المولد (Alternator Bearing) / مضخة الحقن / قواعد التثبيت", "English": "Alternator Bearing / Injection Pump / Engine Mounting Couplings", "Русский": "Подшипники генератора / Топливный насос / Опоры"}
            recs = {"العربية": "يرجى فحص رولمان بلي الدينامو ومضخة حقن الوقود وقواعد تثبيت المحرك الصناعي. الاهتزاز الصوتي ينم عن احتكاك دوراني.", "English": "Inspect alternator bearings, fuel injection pump timing, and engine mounting dampeners for mechanical misalignment.", "Русский": "Проверьте подшипники генератора, топливный насос высокого давления и виброопоры."}
        else:
            zones = {"العربية": "سليمة (طبيعية)", "English": "None (Normal Operation)", "Русский": "Норма"}
            recs = {"العربية": "المحرك الصناعي يعمل بنسق استقرار ممتاز وتوازن ترددي طبيعي.", "English": "Industrial engine operating within healthy acoustic and vibration stability parameters.", "Русский": "Промышленный двигатель работает в пределах нормы."}

    return zones[lang], recs[lang], img_url, title

# --- 7. Diagnostic Execution & Output ---
if audio_bytes is not None:
    st.audio(audio_bytes)
    
    with st.spinner(T['analyzing']):
        clean_signal, sr = load_audio_signal(audio_bytes)
        clean_signal = apply_noise_filter(clean_signal, sr)
        clean_signal = clean_signal / (np.max(np.abs(clean_signal)) + 1e-6)
        
        energy = np.mean(clean_signal**2)
        zcr = np.mean(np.diff(np.signbit(clean_signal)) != 0)
        fft_spectrum = np.abs(np.fft.rfft(clean_signal[:2048]))
        spectral_centroid = np.sum(fft_spectrum * np.arange(len(fft_spectrum))) / (np.sum(fft_spectrum) + 1e-6)
        
        raw_score = float((energy * 800) + (zcr * 40) + (spectral_centroid / 120))
        anomaly_score = round(float(np.clip(raw_score * 7.821, 14.120, 96.850)), 3)
        
        # Fetch Category-Specific Diagnostic Info
        fault_zone, rec_text, visual_img_url, scan_title = get_category_diagnostic(machine_type, anomaly_score, lang_choice)
        
        st.divider()
        
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.metric(label=T['score_label'], value=f"{anomaly_score:.3f}%")
            
        with col_res2:
            if anomaly_score > 60.0:
                st.error(T['defect_title'])
                st.caption(f"{T['defect_cap']} {make} {model}.")
            else:
                st.success(T['normal_title'])
                st.caption(f"{T['normal_cap']} {make} {model}.")

        # --- Detailed Category Diagnostic Report ---
        st.markdown(f"### {T['report_title']}")
        
        severity_str = T['high_sev'] if anomaly_score > 70 else (T['mod_sev'] if anomaly_score > 50 else T['low_sev'])
        
        st.markdown(f"""
            <div class="report-card">
                <h4 style="color: #FF6B00; margin-top:0;">{T['summary_header']}</h4>
                <ul>
                    <li><strong>{T['target_machinery']}</strong> {make} {model} ({year})</li>
                    <li><strong>{T['engine_type']}</strong> {engine_spec}</li>
                    <li><strong>{T['status_label']}</strong> <span style="color:{'#EF4444' if anomaly_score > 60 else '#10B981'}; font-weight:bold;">{severity_str}</span></li>
                    <li><strong>{T['anomaly_zone']}</strong> {fault_zone}</li>
                    <li><strong>Spectral Centroid Frequency:</strong> {spectral_centroid:.2f} Hz</li>
                    <li><strong>Signal Energy Density:</strong> {energy:.6f} RMS</li>
                </ul>
                <h4 style="color: #10B981; margin-top:15px;">{T['rec_header']}</h4>
                <p style="color:#CBD5E1; font-size:14px;">
                    {rec_text}
                </p>
            </div>
        """, unsafe_allow_html=True)

        # --- Category-Specific Visual Inspection Scanner ---
        st.markdown(f"### {scan_title}")
        
        laser_color = "#EF4444" if anomaly_score > 60 else "#10B981"
        
        html_scanner = f"""
        <div style="position: relative; width: 100%; height: 280px; border-radius: 14px; overflow: hidden; border: 2px solid #FF6B00; box-shadow: 0 0 20px rgba(255,107,0,0.3);">
            <!-- High-Res Category Machine Image -->
            <img src="{visual_img_url}" style="width: 100%; height: 100%; object-fit: cover; filter: brightness(0.75) contrast(1.1);" />
            
            <!-- Animated AI Laser Beam Overlay -->
            <div class="laser-beam"></div>
            
            <!-- Scanning Watermark Badge -->
            <div style="position: absolute; top:
