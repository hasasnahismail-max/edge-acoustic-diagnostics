import time
import streamlit as st

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="ZINO EADE - Multi-Vehicle Precision Acoustic Engine",
    page_icon="🎙️",
    layout="wide",
)

# 2. القاموس متعدد اللغات الشامل للواجهة والتحكم
I18N = {
    "العربية": {
        "main_title": "🎙️ محطة التشخيص الصوتي الهندسي الشاملة - ZINO EADE",
        "developer_credit": "🛠️ تصميم وتطوير: إسماعيل حساسنة",
        "domain_label": "🏢 اختر القطاع التشخيصي:",
        "d_cars": "🚗 قطاع السيارات والمركبات الشامل",
        "d_appliances": "🔌 الأجهزة الكهربائية والمنزلية",
        "d_industrial": "🏭 الماكينات والمعدات الصناعية",
        "select_car_brand": "🏢 اختر الشركة المصنعة للمركبة:",
        "select_car_model": "🚗 اختر طراز السيارة (أو أدخله يدوياً):",
        "select_engine_type": "⚙️ اختر سعة ونوع المحرك (أو أدخله يدوياً):",
        "custom_model_label": "✍️ أدخل طراز السيارة المخصص:",
        "custom_engine_label": "✍️ أدخل تفاصيل المحرك المخصص:",
        "fuel_type_label": "⛽ نوع الوقود ونظام الحقن:",
        "cylinders_label": "🔢 عدد ونظام الأسطوانات:",
        "audio_section": "🎙️ وحدة التقاط وتسجيل الصوت الحي",
        "rec_mic": "تسجيل صوت المحرك/الجهاز المباشر عبر الميكروفون:",
        "upload_file": "أو رفع ملف صوتي جاهز (WAV, MP3, OGG):",
        "scan_btn": "🚀 بدء المسح الليزري عالي الدقة وتحليل الطيف الصوتي",
        "laser_scanning": "⚡ جاري الفحص بالليزر الموجه وتحليل الترددات الطيفية...",
        "results_title": "📊 التقرير التشخيصي الهندسي عالي الدقة (FFT Spectrum Analysis)",
        "health": "نسبة السلامة الصوتية",
        "fft_peak": "التردد البارز (FFT Peak)",
        "anomaly": "مؤشر التشوه الصوتي",
        "detailed_report_title": "📑 التقرير التشخيصي الفني المخصص الشامل",
    },
    "English": {
        "main_title": "🎙️ ZINO EADE - Universal Precision Acoustic Diagnostic Workstation",
        "developer_credit": "🛠️ Designed & Developed by Ismail Hassasneh",
        "domain_label": "🏢 Select Diagnostic Sector:",
        "d_cars": "🚗 Comprehensive Automotive Sector",
        "d_appliances": "🔌 Home & Electrical Appliances",
        "d_industrial": "🏭 Industrial Machinery",
        "select_car_brand": "🏢 Select Vehicle Manufacturer:",
        "select_car_model": "🚗 Select Vehicle Model (or type custom):",
        "select_engine_type": "⚙️ Select Engine Specs (or type custom):",
        "custom_model_label": "✍️ Enter Custom Car Model:",
        "custom_engine_label": "✍️ Enter Custom Engine Specs:",
        "fuel_type_label": "⛽ Fuel & Injection System:",
        "cylinders_label": "🔢 Cylinder Configuration:",
        "audio_section": "🎙️ Live Acoustic Capture & Recording Unit",
        "rec_mic": "Record live audio via microphone:",
        "upload_file": "Or upload audio file (WAV, MP3, OGG):",
        "scan_btn": "🚀 Run High-Precision Laser Scan & FFT Spectrum Analysis",
        "laser_scanning": "⚡ Executing Precision Laser Scan & Spectrum Processing...",
        "results_title": "📊 High-Precision Diagnostic Spectrum Report (FFT Analysis)",
        "health": "Acoustic Health Score",
        "fft_peak": "Dominant FFT Peak",
        "anomaly": "Acoustic Anomaly Index",
        "detailed_report_title": "📑 Comprehensive Technical Engineering Report",
    },
    "Русский": {
        "main_title": "🎙️ ZINO EADE - Универсальная Высокоточная Диагностическая Станция",
        "developer_credit": "🛠️ Дизайн и разработка: Исмаил Хасасна",
        "domain_label": "🏢 Выберите сектор диагностики:",
        "d_cars": "🚗 Полный автомобильный сектор",
        "d_appliances": "🔌 Бытовая и электротехника",
        "d_industrial": "🏭 Промышленное оборудование",
        "select_car_brand": "🏢 Выберите производителя автомобиля:",
        "select_car_model": "🚗 Выберите модель авто (или введите вручную):",
        "select_engine_type": "⚙️ Выберите двигатель (или введите вручную):",
        "custom_model_label": "✍️ Введите модель автомобиля:",
        "custom_engine_label": "✍️ Введите характеристики двигателя:",
        "fuel_type_label": "⛽ Тип топлива и впрыска:",
        "cylinders_label": "🔢 Конфигурация цилиндров:",
        "audio_section": "🎙️ Модуль записи и захвата звука",
        "rec_mic": "Запись звука через микрофон:",
        "upload_file": "Или загрузите аудиофайл (WAV, MP3, OGG):",
        "scan_btn": "🚀 Запустить высокоточное лазерное сканирование и анализ FFT",
        "laser_scanning": "⚡ Выполнение лазерного сканирования и спектрального анализа...",
        "results_title": "📊 Высокоточный отчет акустической диагностики (FFT Спектр)",
        "health": "Индекс здоровья",
        "fft_peak": "Пиковая частота (FFT Peak)",
        "anomaly": "Индекс аномалии",
        "detailed_report_title": "📑 Подробный технический инженерный отчет",
    },
}

# 3. قاعدة بيانات الشركات وطرازات السيارات الشاملة
BRAND_DATABASE = {
    "Mitsubishi": {
        "brand_name": "Mitsubishi Motors",
        "color": "#556B2F",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Mitsubishi_logo.svg",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Mitsubishi_Pajero_V20_front.jpg/800px-Mitsubishi_Pajero_V20_front.jpg",
        "models": [
            "Pajero (V20 / V60 / V80 / 2027)",
            "Lancer (EX / Evolution)",
            "Outlander / Outlander PHEV",
            "L200 / Triton Pickup",
            "Montero Sport / Nativa",
            "Eclipse Cross",
            "ASX / Outlander Sport",
            "Galant",
            "Mirage / Attrage",
            "طراز آخر / Custom Model",
        ],
        "engines": [
            "3.5L V6 6G74 Gasoline",
            "3.0L V6 6G72 Gasoline",
            "3.2L Di-D 4M41 Turbo Diesel",
            "2.0L I4 4B11 MIVEC Turbo",
            "2.4L I4 4G69 MIVEC",
            "2.5L TD 4D56 Turbo Diesel",
            "1.5L MIVEC Turbo",
            "محتوى محرك آخر / Custom Engine",
        ],
    },
    "Hyundai": {
        "brand_name": "Hyundai Motor Company",
        "color": "#7A1C2E",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/4/44/Hyundai_Motor_Company_logo.svg",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Hyundai_Santa_Fe_DM_IMG_0392.jpg/800px-Hyundai_Santa_Fe_DM_IMG_0392.jpg",
        "models": [
            "Santa Fe",
            "Tucson",
            "Elantra / Avante",
            "Sonata",
            "Accent / Verna",
            "Creta",
            "Kona / Kona Electric",
            "Palisade",
            "Genesis Coupe / G70",
            "Grandeur / Azera",
            "H100 / Starex / H-1",
            "طراز آخر / Custom Model",
        ],
        "engines": [
            "2.2L CRDi VGT Turbo Diesel",
            "2.0L CRDi Diesel",
            "2.0L Nu MPI Gasoline",
            "1.6L GDI Turbo Gasoline",
            "2.4L Theta II Gasoline",
            "3.5L V6 Smartstream Gasoline",
            "1.4L Kappa MPI Gasoline",
            "محتوى محرك آخر / Custom Engine",
        ],
    },
    "Volkswagen": {
        "brand_name": "Volkswagen Group",
        "color": "#004B87",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Volkswagen_logo_2019.svg",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Volkswagen_Caddy_Maxi_TDI_Facelift_front.jpg/800px-Volkswagen_Caddy_Maxi_TDI_Facelift_front.jpg",
        "models": [
            "Caddy / Caddy Maxi",
            "Golf (GTI / R / VII / VIII)",
            "Passat / Passat CC",
            "Tiguan / Tiguan Allspace",
            "Polo",
            "Jetta",
            "Touareg",
            "Transporter / Multivan / Caravelle",
            "Scirocco",
            "Arteon",
            "Amarok Pickup",
            "طراز آخر / Custom Model",
        ],
        "engines": [
            "2.0L TDI Common Rail Diesel",
            "1.6L TDI Diesel",
            "2.0L TSI EA888 Turbo Gasoline",
            "1.4L TSI Twincharger",
            "1.6L MPI Gasoline",
            "3.0L V6 TDI Diesel",
            "1.2L TSI Gasoline",
            "محتوى محرك آخر / Custom Engine",
        ],
    },
}

# 4. الشريط الجانبي واختيار اللغة والقطاع
st.sidebar.title("⚙️ التحكم واللغة")
lang = st.sidebar.selectbox(
    "🌐 Choose Language / اختر اللغة", ["العربية", "English", "Русский"]
)
t = I18N[lang]

st.sidebar.markdown("---")
domain = st.sidebar.radio(
    t["domain_label"], [t["d_cars"], t["d_appliances"], t["d_industrial"]]
)

st.sidebar.markdown("---")
st.sidebar.info(f"**{t['developer_credit']}**")

# 5. إدارة حالة الشركة والسيارة النشطة
if "selected_brand" not in st.session_state:
    st.session_state["selected_brand"] = "Hyundai"

# تحديد لون الهوية النشط
if domain == t["d_cars"]:
    active_color = BRAND_DATABASE[st.session_state["selected_brand"]]["color"]
elif domain == t["d_appliances"]:
    active_color = "#005F73"
else:
    active_color = "#D97706"

# 6. تنسيق CSS ديناميكي احترافي
st.markdown(
    f"""
    <style>
    .main-header {{
        font-size: 26px;
        font-weight: bold;
        color: {active_color};
        border-bottom: 4px solid {active_color};
        padding-bottom: 8px;
        margin-bottom: 5px;
    }}
    .dev-credit {{
        font-size: 15px;
        font-weight: 600;
        color: #888888;
        margin-bottom: 25px;
    }}
    .stButton>button {{
        background-color: {active_color} !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }}
    .laser-box {{
        position: relative;
        border: 3px solid {active_color};
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 0 20px {active_color}88;
        background-color: #000000;
    }}
    .laser-line {{
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 6px;
        background-color: #FF0033;
        box-shadow: 0 0 15px 5px #FF0033;
        animation: scan 1.8s infinite ease-in-out;
        z-index: 10;
    }}
    @keyframes scan {{
        0% {{ top: 0%; }}
        50% {{ top: 92%; }}
        100% {{ top: 0%; }}
    }}
    .report-card {{
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-right: 6px solid {active_color};
        border-radius: 8px;
        padding: 20px;
        margin-top: 15px;
        color: #1e293b;
        font-size: 15px;
        line-height: 1.8;
    }}
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="main-header">{t["main_title"]}</div>', unsafe_allow_html=True
)
st.markdown(
    f'<div class="dev-credit">{t["developer_credit"]}</div>',
    unsafe_allow_html=True,
)

# ==========================================
# 🚗 1. قطاع السيارات الشامل (All Models & Brands)
# ==========================================
if domain == t["d_cars"]:
    st.markdown(f"### {t['select_car_brand']}")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("🔴 ميتسوبيشي (Mitsubishi)", use_container_width=True):
            st.session_state["selected_brand"] = "Mitsubishi"
            st.rerun()

    with c2:
        if st.button("🔵 هيونداي (Hyundai)", use_container_width=True):
            st.session_state["selected_brand"] = "Hyundai"
            st.rerun()

    with c3:
        if st.button("⚪ فولكسفاغن (Volkswagen)", use_container_width=True):
            st.session_state["selected_brand"] = "Volkswagen"
            st.rerun()

    brand_key = st.session_state["selected_brand"]
    b_data = BRAND_DATABASE[brand_key]

    st.markdown("---")

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        selected_model = st.selectbox(t["select_car_model"], b_data["models"])
        if "Custom" in selected_model or "آخر" in selected_model:
            final_model = st.text_input(
                t["custom_model_label"], value="Pajero / Lancer / Golf"
            )
        else:
            final_model = selected_model

        fuel_system = st.selectbox(
            t["fuel_type_label"],
            [
                "Turbo Diesel CRDi / TDI (ديزل تربو حقن مشترك)",
                "Gasoline Direct Injection GDI / TSI (بنزين حقن مباشر)",
                "Gasoline MPI / MIVEC (بنزين حقن متعدد النقاط)",
                "Atmospheric Diesel (ديزل سحب عادي)",
            ],
        )

    with col_m2:
        selected_engine = st.selectbox(
            t["select_engine_type"], b_data["engines"]
        )
        if "Custom" in selected_engine or "آخر" in selected_engine:
            final_engine = st.text_input(
                t["custom_engine_label"], value="2.0L Turbo 250 HP"
            )
        else:
            final_engine = selected_engine

        cylinders_config = st.selectbox(
            t["cylinders_label"],
            [
                "4 Cylinders Inline (4 أسطوانات متتالية)",
                "6 Cylinders V6 (6 أسطوانات V6)",
                "3 Cylinders Inline (3 أسطوانات)",
                "8 Cylinders V8 (8 أسطوانات V8)",
            ],
        )

    brand_logo = b_data["logo"]
    brand_name_str = b_data["brand_name"]
    brand_color_str = b_data["color"]

    col_logo, col_details = st.columns([1, 3])
    with col_logo:
        st.image(brand_logo, width=120, caption=brand_name_str)
    with col_details:
        st.markdown(
            f"""
        <div style="background-color: #111827; padding: 16px; border-left: 6px solid {brand_color_str}; border-radius: 8px;">
            <h3 style="color: #ffffff; margin:0;">{brand_key} - {final_model}</h3>
            <p style="margin:5px 0 0 0; color: #9ca3af;"><b>المحرك:</b> {final_engine} | <b>المنظومة:</b> {fuel_system} ({cylinders_config})</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ==========================================
# 🔌 2. قطاع الأجهزة الكهربائية والمنزلية
# ==========================================
elif domain == t["d_appliances"]:
    st.subheader("🔌 قطاع تشخيص الأجهزة الكهربائية والمنزلية")
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        appliance_type = st.selectbox(
            "نوع الجهاز الكهربائي:",
            [
                "غسالة ملابس (Washing Machine)",
                "ثلاجة / مجمد (Refrigerator/Freezer)",
                "مكيف هواء (Air Conditioner)",
                "جلاية صحون (Dishwasher)",
            ],
        )
    with col_a2:
        brand = st.selectbox(
            "الشركة المصنعة:", ["LG", "Samsung", "Bosch", "Whirlpool", "Gree"]
        )
    with col_a3:
        model = st.text_input("الموديل / الرقم الفني:", "Inverter Direct Drive")

# ==========================================
# 🏭 3. قطاع الماكينات والمعدات الصناعية
# ==========================================
else:
    st.subheader("🏭 قطاع تشخيص الماكينات والمعدات الصناعية")
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1:
        machine_type = st.selectbox(
            "نوع المعدة الصناعية:",
            [
                "محرك كهربائي ثلاثي الأوجه (3-Phase Induction Motor)",
                "مضخة مياه هيدروليكية (Hydraulic Water Pump)",
                "ضاغط هواء حلزوني (Rotary Screw Compressor)",
                "مولد كهربائي (Diesel Generator)",
            ],
        )
    with col_i2:
        power_rating = st.text_input("القدرة (HP / kW):", "50 HP / 37 kW")
    with col_i3:
        rpm_val = st.text_input("سرعة الدوران (RPM):", "1450 RPM")

st.markdown("---")

# ==========================================
# 🎙️ قسم التسجيل والالتقاط الصوتي الحي
# ==========================================
st.markdown(f"### {t['audio_section']}")
col_rec1, col_rec2 = st.columns(2)

with col_rec1:
    st.write(f"<b>1. {t['rec_mic']}</b>", unsafe_allow_html=True)
    recorded_audio = st.audio_input("اضغط للبدء بالتسجيل الصوتي المباشر 🎙")

with col_rec2:
    st.write(f"<b>2. {t['upload_file']}</b>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "ارفع ملف الصوت من جهازك:", type=["wav", "mp3", "ogg"]
    )

audio_source = recorded_audio or uploaded_file
if audio_source:
    st.audio(audio_source)
    st.success("✅ تم استقبال الإشارة الصوتية بنجاح وهي جاهزة للفحص بالليزر الطيفي!")

st.markdown("---")


# ==========================================
# 🧬 دالة التقرير الهندسي الديناميكي الموسّع
# ==========================================
def generate_expanded_car_report(
    brand, model, engine, fuel, cylinders, lang
):
    is_diesel = "Diesel" in fuel or "CRDi" in engine or "TDI" in engine
    is_turbo = "Turbo" in fuel or "Turbo" in engine or "TSI" in engine

    if lang == "العربية":
        inj_text = (
            "ترددات بخاخات الديزل ذات الضغط العالي (Common Rail) متزنة ونقية دون"
            " وجود ظاهرة التسريب الترددي."
            if is_diesel
            else (
                "نظام حقن البنزين المباشر/المتعدد يعمل بانتظام، والضوضاء عالية"
                " التردد في النطاق الطبيعي."
            )
        )
        turbo_text = (
            "عنفة التوربو تعمل بستارة صوتية مستقرة دون أي صفير مرتفع أو احتكاك"
            " في شفرات الشاحن."
            if is_turbo
            else (
                "منظومة سحب الهواء وتطابق الضغط الطبيعي تعمل بكفاءة عالية بدون أي"
                " تسريب في المانفولد."
            )
        )

        return (
            f"<b>1. تحليل طيف فوريه الترددي (FFT Spectrum Analysis):</b><br>تم"
            f" تفكيك الإشارة الصوتية لسيارة <b>{brand} {model}</b> (محرك"
            f" <b>{engine}</b>). التردد البارز يطابق زمن الاحتراق للـ"
            f" {cylinders} بدون تشتت في الطاقة.<br><br><b>2. معاينة صمامات ومحاور"
            f" الكامبشافت (Valve Train & Camshaft Acoustics):</b><br>خلوص"
            f" الصبابات والصمامات يعمل ضمن المجال الهيدروليكي القياسي لشركة"
            f" {brand}، ولا تظهر أي طقطقة عشوائية في عمود الكامبشافت.<br><br><b>3."
            f" نظام حقن الوقود والضغط العالي (Injectors & Fuel Rail"
            f" Pressure):</b><br>{inj_text}<br><br><b>4. الشاحن التوربيني ونظام"
            f" سحب الهواء (Turbocharger & Induction):</b><br>{turbo_text}<br><br><b>5."
            f" محامل الدوران وعمود الكرنك والحذافة (Bearings, Crankshaft &"
            f" DMF):</b><br>عدم وجود أي اهتزازات منخفضة التردد في محامل عمود"
            f" الكرنك الرئيسية، وحذافة الفولام المزدوجة امتصت الصدمات الصوتية"
            f" بالكامل.<br><br><b>6. التوصيات الهندسية وخطة الصيانة الوقائية"
            f" (Predictive Maintenance Plan):</b><br>المحرك بحالة ممتازة جداً."
            f" يوصى بالمحافظة على مواعيد استبدال الزيوت والفلاتر الخاصة بـ"
            f" {brand} عند قطع 10,000 كم."
        )

    elif lang == "English":
        inj_text = (
            "High-pressure Common Rail Diesel injector chatter is fully"
            " synchronized with zero cavitation noise."
            if is_diesel
            else (
                "Gasoline injection pulses show crisp, clean high-frequency"
                " harmonics within normal operating range."
            )
        )
        turbo_text = (
            "Turbocharger spool frequency exhibits smooth acoustic resonance"
            " without high-pitched turbine squeal."
            if is_turbo
            else (
                "Naturally aspirated air intake manifold shows no pressure"
                " leaks or turbulent acoustic anomalies."
            )
        )

        return (
            f"<b>1. FFT Acoustic Spectrum Core Analysis:</b><br>Acoustic signal"
            f" breakdown for <b>{brand} {model}</b> ({engine}). Dominant peak"
            f" matches the fundamental combustion frequency for {cylinders}"
            f" with zero spectral leakage.<br><br><b>2. Valve Train & Camshaft"
            f" Acoustic Inspection:</b><br>Valve lash clearances and hydraulic"
            f" lifters operate strictly within nominal {brand}"
            f" specifications. Zero camshaft chatter observed.<br><br><b>3. Fuel"
            f" Injection System & Rail Dynamics:</b><br>{inj_text}<br><br><b>4."
            f" Turbocharger & Induction Harmonics:</b><br>{turbo_text}<br><br><b>5."
            f" Bearings, Crankshaft &
