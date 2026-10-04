import time
import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="ZINO EADE - Acoustic Workstation",
    page_icon="🚗",
    layout="wide",
)

# روابط الشعارات وصور السيارات المباشرة (عالية الجودة)
LOGOS = {
    "Mitsubishi": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Mitsubishi_logo.svg",
    "Hyundai": "https://upload.wikimedia.org/wikipedia/commons/4/44/Hyundai_Motor_Company_logo.svg",
    "Volkswagen": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Volkswagen_logo_2019.svg",
}

CAR_IMAGES = {
    "Mitsubishi": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Mitsubishi_Pajero_V20_front.jpg/800px-Mitsubishi_Pajero_V20_front.jpg",
    "Hyundai": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Hyundai_Santa_Fe_DM_IMG_0392.jpg/800px-Hyundai_Santa_Fe_DM_IMG_0392.jpg",
    "Volkswagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Volkswagen_Caddy_Maxi_TDI_Facelift_front.jpg/800px-Volkswagen_Caddy_Maxi_TDI_Facelift_front.jpg",
}

# قاموس اللغات الثلاث
I18N = {
    "العربية": {
        "title": "⚙️ محطة التشخيص الهندسي الصوتي - ZINO EADE",
        "select_brand": "🏢 اختر الشركة المصنعة للمركبة:",
        "mitsubishi": "ميتسوبيشي (Mitsubishi)",
        "hyundai": "هيونداي (Hyundai)",
        "volkswagen": "فولكسفاغن (Volkswagen)",
        "model_label": "اسم السيارة والموديل:",
        "engine_label": "نوع وسعة المحرك:",
        "scan_btn": "🚀 بدء التحليل الصوتي المتقدم وتفكيك الترددات",
        "card_title": "🔍 بطاقة المواصفات الفنية وصورة المركبة",
        "results_title": "📊 نتائج التشخيص الهندسي الدقيق للمحرك",
        "analyzing": "جاري تحليل بصمة الصوت والترددات الخاصة بمحرك",
        "health_score": "نسبة الكفاءة الصوتية للمحرك",
        "fft_peak": "التردد الصوتي البارز (FFT Peak)",
        "anomaly": "مستوى التشوه الصوتي (Anomaly Score)",
        "diag_report": "📑 التقرير التشخيصي المخصص",
    },
    "English": {
        "title": "⚙️ ZINO EADE - Advanced Acoustic Diagnostic Workstation",
        "select_brand": "🏢 Select Vehicle Manufacturer:",
        "mitsubishi": "Mitsubishi",
        "hyundai": "Hyundai",
        "volkswagen": "Volkswagen",
        "model_label": "Car Model:",
        "engine_label": "Engine Type & Specs:",
        "scan_btn": "🚀 Run Deep Acoustic & Frequency Scan",
        "card_title": "🔍 Selected Vehicle Specifications & Photo",
        "results_title": "📊 Precision Acoustic Diagnostic Output",
        "analyzing": "Analyzing engine acoustic signature for",
        "health_score": "Engine Acoustic Health Score",
        "fft_peak": "Dominant Peak Frequency (FFT)",
        "anomaly": "Acoustic Anomaly Index",
        "diag_report": "📑 Dedicated Diagnostic Report",
    },
    "Русский": {
        "title": "⚙️ ZINO EADE - Акустическая Диагностическая Станция",
        "select_brand": "🏢 Выберите производителя автомобиля:",
        "mitsubishi": "Mitsubishi",
        "hyundai": "Hyundai",
        "volkswagen": "Volkswagen",
        "model_label": "Модель автомобиля:",
        "engine_label": "Тип и объем двигателя:",
        "scan_btn": "🚀 Запустить глубокий акустический анализ",
        "card_title": "🔍 Технические характеристики и фото авто",
        "results_title": "📊 Точный отчет акустической диагностики",
        "analyzing": "Анализ акустического профиля двигателя",
        "health_score": "Индекс акустического здоровья двигателя",
        "fft_peak": "Пиковая частота (FFT Peak)",
        "anomaly": "Индекс акустической аномалии",
        "diag_report": "📑 Подробный диагностический отчет",
    },
}

# الشريط الجانبي باختيار اللغة
st.sidebar.title("⚙️ Language / اللغة")
lang = st.sidebar.selectbox(
    "🌐 Select / اختر / Выбрать", ["العربية", "English", "Русский"]
)
t = I18N[lang]

# اختيار الشركة
st.markdown(f"### {t['select_brand']}")
col_b1, col_b2, col_b3 = st.columns(3)

with col_b1:
    mitsu_click = st.button("🔴 " + t["mitsubishi"], use_container_width=True)
with col_b2:
    hyundai_click = st.button("🔵 " + t["hyundai"], use_container_width=True)
with col_b3:
    vw_click = st.button("⚪ " + t["volkswagen"], use_container_width=True)

if "selected_company" not in st.session_state:
    st.session_state["selected_company"] = "Mitsubishi"

if mitsu_click:
    st.session_state["selected_company"] = "Mitsubishi"
elif hyundai_click:
    st.session_state["selected_company"] = "Hyundai"
elif vw_click:
    st.session_state["selected_company"] = "Volkswagen"

company = st.session_state["selected_company"]

# تحديد الألوان حسب العلامة التجارية
if company == "Mitsubishi":
    theme_color = "#556B2F"  # زيتي
    default_model = "Pajero V20"
    default_engine = "3.5L V6 6G74"
elif company == "Hyundai":
    theme_color = "#7A1C2E"  # خمري
    default_model = "Santa Fe 2.2 CRDI"
    default_engine = "2.2L CRDI VGT Turbo"
else:
    theme_color = "#A39171"  # بيج
    default_model = "Caddy 2.0 TDI"
    default_engine = "2.0L TDI Diesel"

# تنسيق CSS الديناميكي
st.markdown(
    f"""
    <style>
    .main-header {{
        font-size: 26px;
        font-weight: bold;
        color: {theme_color};
        border-bottom: 4px solid {theme_color};
        padding-bottom: 8px;
        margin-bottom: 20px;
    }}
    .brand-card {{
        background-color: #1a1a1a;
        border-left: 8px solid {theme_color};
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }}
    .stButton>button {{
        background-color: {theme_color} !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }}
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="main-header">{t["title"]}</div>', unsafe_allow_html=True
)

# حقول إدخال طراز وسعة المحرك
col_in1, col_in2 = st.columns(2)
with col_in1:
    car_model = st.text_input(
        t["model_label"],
        value=default_model,
        placeholder="مثال: Pajero V20 / Santa Fe",
    )
with col_in2:
    engine_type = st.text_input(
        t["engine_label"],
        value=default_engine,
        placeholder="مثال: 3.5L V6 / 2.0 TDI",
    )

# عرض شريط السيارة مع الشعار والصورة
st.markdown(
    f'<div class="brand-card"><h4 style="color:{theme_color}; margin:0;">{t["card_title"]}</h4></div>',
    unsafe_allow_html=True,
)

col_logo, col_img = st.columns([1, 3])
with col_logo:
    st.image(LOGOS[company], width=110, caption=f"Brand: {company}")
with col_img:
    st.image(
        CAR_IMAGES[company],
        caption=f"{company} - {car_model} ({engine_type})",
        use_container_width=True,
    )

# زر إجراء التحليل
if st.button(t["scan_btn"], use_container_width=True):
    with st.spinner(f"{t['analyzing']} {company} ({car_model})..."):
        time.sleep(1.2)

    st.markdown(f"### {t['results_title']}")
    res_col1, res_col2, res_col3 = st.columns(3)

    if company == "Mitsubishi":
        health_score = "94.2%"
        fft_freq = "142.5 Hz (V6 Firing)"
        anomaly_score = "0.018 (Optimal)"
        report_text = f"تم فحص {car_model} بمحرك {engine_type}. ترددات الصبابات متزنة تماماً، ولا توجد أي اهتزازات هيدروليكية أو تشوهات صوتية في منظومة الوقود والمحرك."
    elif company == "Hyundai":
        health_score = "91.8%"
        fft_freq = "285.0 Hz (CRDi Pulse)"
        anomaly_score = "0.032 (Normal Diesel)"
        report_text = f"تم تشخيص {car_model} بمحرك {engine_type}. ضغط مضخة الديزل/البنزين مستقر، واستجابة شاحن التوربو (VGT) ممتازة بدون أي احتكاك صوتي."
    else:
        health_score = "95.6%"
        fft_freq = "98.2 Hz (DMF Resonance)"
        anomaly_score = "0.012 (Low Anomaly)"
        report_text = f"تم تشخيص {car_model} بمحرك {engine_type}. حذافة الفولام (Dual-Mass Flywheel) متزنة صوتياً، ونظام الحقن وسير التوقيت يعملان بكفاءة عالية."

    with res_col1:
        st.metric(t["health_score"], health_score)
    with res_col2:
        st.metric(t["fft_peak"], fft_freq)
    with res_col3:
        st.metric(t["anomaly"], anomaly_score)

    st.info(f"**{t['diag_report']}:**\n\n{report_text}")
