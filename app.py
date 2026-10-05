import time
import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="ZINO EADE - Precision Workstation",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. القاموس متعدد اللغات
I18N = {
    "العربية": {
        "main_title": "🎙️ محطة التشخيص الصوتي الهندسي الشاملة - ZINO EADE",
        "developer_credit": "🛠️ تصميم وتطوير: إسماعيل حساسنة",
        "domain_label": "🏢 اختر القطاع التشخيصي:",
        "d_cars": "🚗 قطاع السيارات والمركبات",
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
        "results_title": "📊 التقرير التشخيصي الهندسي عالي الدقة (FFT Analysis)",
        "health": "نسبة السلامة الصوتية",
        "fft_peak": "التردد البارز (FFT Peak)",
        "anomaly": "مؤشر التشوه الصوتي",
        "detailed_report_title": "📑 التقرير التشخيصي الفني المخصص الشامل",
        "appliance_type": "نوع الجهاز الكهربائي:",
        "appliance_brand": "الشركة المصنعة للجهاز:",
        "appliance_model": "الموديل / الرقم الفني للجهاز:",
        "machine_type": "نوع المعدة الصناعية:",
        "machine_power": "القدرة التشغيلية (HP / kW):",
        "machine_rpm": "سرعة الدوران (RPM):",
    },
    "English": {
        "main_title": "🎙️ ZINO EADE - Precision Acoustic Diagnostic Workstation",
        "developer_credit": "🛠️ Designed & Developed by Ismail Hassasneh",
        "domain_label": "🏢 Select Diagnostic Sector:",
        "d_cars": "🚗 Automotive Sector",
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
        "laser_scanning": "⚡ Executing Precision Laser Scan & Processing...",
        "results_title": "📊 High-Precision Spectrum Report (FFT Analysis)",
        "health": "Acoustic Health Score",
        "fft_peak": "Dominant FFT Peak",
        "anomaly": "Acoustic Anomaly Index",
        "detailed_report_title": "📑 Comprehensive Technical Engineering Report",
        "appliance_type": "Appliance Category:",
        "appliance_brand": "Manufacturer Brand:",
        "appliance_model": "Model / Technical Specs:",
        "machine_type": "Industrial Machinery Type:",
        "machine_power": "Power Rating (HP / kW):",
        "machine_rpm": "Rotation Speed (RPM):",
    },
    "Русский": {
        "main_title": "🎙️ ZINO EADE - Высокоточная Диагностическая Станция",
        "developer_credit": "🛠️ Дизайн и разработка: Исмаил Хасасна",
        "domain_label": "🏢 Выберите сектор диагностики:",
        "d_cars": "🚗 Автомобильный сектор",
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
        "scan_btn": "🚀 Запустить лазерное сканирование и анализ FFT",
        "laser_scanning": "⚡ Выполнение лазерного сканирования...",
        "results_title": "📊 Отчет акустической диагностики (FFT Спектр)",
        "health": "Индекс здоровья",
        "fft_peak": "Пиковая частота (FFT Peak)",
        "anomaly": "Индекс аномалии",
        "detailed_report_title": "📑 Подробный технический инженерный отчет",
        "appliance_type": "Категория прибора:",
        "appliance_brand": "Производитель:",
        "appliance_model": "Модель / Спецификация:",
        "machine_type": "Тип промышленного оборудования:",
        "machine_power": "Мощность (Л.С. / кВт):",
        "machine_rpm": "Скорость вращения (ОБ/МИН):",
    },
}

# 3. قاعدة البيانات
BRAND_DATABASE = {
    "Mitsubishi": {
        "brand_name": "Mitsubishi Motors",
        "color": "#556B2F",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Mitsubishi_logo.svg",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Mitsubishi_Pajero_V20_front.jpg/800px-Mitsubishi_Pajero_V20_front.jpg",
        "models": [
            "Pajero (V20 / V60 / V80)",
            "Lancer (EX / Evolution)",
            "Outlander / Outlander PHEV",
            "L200 / Triton Pickup",
            "Montero Sport / Nativa",
            "Eclipse Cross",
            "ASX / Outlander Sport",
            "Galant",
            "Mirage / Attrage",
            "Custom Model / طراز آخر",
        ],
        "engines": [
            "3.5L V6 6G74 Gasoline",
            "3.0L V6 6G72 Gasoline",
            "3.2L Di-D 4M41 Turbo Diesel",
            "2.0L I4 4B11 MIVEC Turbo",
            "2.4L I4 4G69 MIVEC",
            "2.5L TD 4D56 Turbo Diesel",
            "1.5L MIVEC Turbo",
            "Custom Engine / محرك آخر",
        ],
    },
    "Hyundai": {
        "brand_name": "Hyundai Motor Company",
        "color": "#002C5F",
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
            "Custom Model / طراز آخر",
        ],
        "engines": [
            "2.2L CRDi VGT Turbo Diesel",
            "2.0L CRDi Diesel",
            "2.0L Nu MPI Gasoline",
            "1.6L GDI Turbo Gasoline",
            "2.4L Theta II Gasoline",
            "3.5L V6 Smartstream Gasoline",
            "1.4L Kappa MPI Gasoline",
            "Custom Engine / محرك آخر",
        ],
    },
    "Volkswagen": {
        "brand_name": "Volkswagen Group",
        "color": "#001E50",
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
            "Custom Model / طراز آخر",
        ],
        "engines": [
            "2.0L TDI Common Rail Diesel",
            "1.6L TDI Diesel",
            "2.0L TSI EA888 Turbo Gasoline",
            "1.4L TSI Twincharger",
            "1.6L MPI Gasoline",
            "3.0L V6 TDI Diesel",
            "1.2L TSI Gasoline",
            "Custom Engine / محرك آخر",
        ],
    },
}

# 4. الشريط الجانبي
st.sidebar.title("⚙️ التحكم واللغة")

lang = st.sidebar.selectbox(
    "🌐 Choose Language / اختر اللغة",
    ["العربية", "English", "Русский"],
    key="app_lang_select"
)
t = I18N[lang]

st.sidebar.markdown("---")

domain_code = st.sidebar.radio(
    t["domain_label"],
    options=["cars", "appliances", "industrial"],
    format_func=lambda x: {
        "cars": t["d_cars"],
        "appliances": t["d_appliances"],
        "industrial": t["d_industrial"],
    }[x],
    key="app_domain_radio"
)

st.sidebar.markdown("---")
st.sidebar.info(t["developer_credit"])

# 5. إدارة الحالة
if "selected_brand" not in st.session_state:
    st.session_state["selected_brand"] = "Hyundai"

brand_key = st.session_state["selected_brand"]

if domain_code == "cars":
    active_color = BRAND_DATABASE[brand_key]["color"]
elif domain_code == "appliances":
    active_color = "#005F73"
else:
    active_color = "#D97706"

c_val = str(active_color)

# 6. قواعد CSS
css_code = f"""
<style>
    .main-header {{
        font-size: 26px;
        font-weight: 800;
        color: {c_val};
        border-bottom: 3px solid {c_val};
        padding-bottom: 8px;
        margin-bottom: 4px;
    }}
    .dev-credit {{
        font-size: 14px;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 20px;
    }}
    .stButton>button {{
        background-color: {c_val} !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 16px !important;
        transition: all 0.3s ease !important;
    }}
    .stButton>button:hover {{
        opacity: 0.9 !important;
        transform: translateY(-1px);
    }}
    .laser-box {{
        position: relative;
        border: 3px solid {c_val};
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 0 20px {c_val}66;
        background-color: #000000;
        margin-top: 15px;
    }}
    .laser-line {{
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 5px;
        background-color: #FF0033;
        box-shadow: 0 0 15px 4px #FF0033;
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
        border-right: 6px solid {c_val};
        border-radius: 10px;
        padding: 20px;
        margin-top: 15px;
        color: #0f172a;
        font-size: 15px;
        line-height: 1.8;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }}
    @media (max-width: 768px) {{
        .main-header {{ font-size: 20px !important; }}
        .dev-credit {{ font-size: 12px !important; margin-bottom: 15px !important; }}
        .report-card {{ padding: 12px !important; font-size: 13.5px !important; }}
        .stButton>button {{ padding: 8px 12px !important; font-size: 13px !important; }}
    }}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

st.markdown(f'<div class="main-header">{t["main_title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="dev-credit">{t["developer_credit"]}</div>', unsafe_allow_html=True)

# 7. قطاع السيارات
if domain_code == "cars":
    st.markdown(f"### {t['select_car_brand']}")
    
    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        if st.button("🔴 ميتسوبيشي (Mitsubishi)", use_container_width=True, key="btn_mitsu"):
            st.session_state["selected_brand"] = "Mitsubishi"
            st.rerun()
    with b_col2:
        if st.button("🔵 هيونداي (Hyundai)", use_container_width=True, key="btn_hyundai"):
            st.session_state["selected_brand"] = "Hyundai"
            st.rerun()
    with b_col3:
        if st.button("⚪ فولكسفاغن (Volkswagen)", use_container_width=True, key="btn_vw"):
            st.session_state["selected_brand"] = "Volkswagen"
            st.rerun()

    brand_key = st.session_state["selected_brand"]
    b_data = BRAND_DATABASE[brand_key]
    st.markdown("---")

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        selected_model = st.selectbox(
            t["select_car_model"], 
            b_data["models"],
            key=f"model_select_{brand_key}_{lang}"
        )
        if "Custom" in selected_model or "آخر" in selected_model:
            final_model = st.text_input(t["custom_model_label"], value="Pajero / Lancer / Golf", key=f"cust_m_{brand_key}")
        else:
            final_model = selected_model

        fuel_system = st.selectbox(
            t["fuel_type_label"],
            [
                "Turbo Diesel CRDi / TDI (ديزل تربو حقن مشترك)",
                "Gasoline Direct Injection GDI / TSI (بنزين حقن مباشر)",
                "Gasoline MPI / MIVEC (بنزين حقن متعدد النقاط)",
                "Atmospheric Diesel (ديزل سحب عادي)"
            ],
            key=f"fuel_select_{lang}"
        )

    with col_m2:
        selected_engine = st.selectbox(
            t["select_engine_type"], 
            b_data["engines"],
            key=f"engine_select_{brand_key}_{lang}"
        )
        if "Custom" in selected_engine or "آخر" in selected_engine:
            final_engine = st.text_input(t["custom_engine_label"], value="2.0L Turbo 250 HP", key=f"cust_e_{brand_key}")
        else:
            final_engine = selected_engine

        cylinders_config = st.selectbox(
            t["cylinders_label"],
            [
                "4 Cylinders Inline (4 أسطوانات متتالية)",
                "6 Cylinders V6 (6 أسطوانات V6)",
                "3 Cylinders Inline (3 أسطوانات)",
                "8 Cylinders V8 (8 أسطوانات V8)"
            ],
            key=f"cyl_select_{lang}"
        )

    col_logo, col_details = st.columns([1, 3])
    with col_logo:
        st.image(b_data["logo"], width=110, caption=b_data["brand_name"])
    with col_details:
        card_html = f"""
        <div style="background-color: #0f172a; padding: 14px; border-left: 5px solid {b_data['color']}; border-radius: 8px;">
            <h3 style="color: #ffffff; margin:0; font-size: 18px;">{brand_key} - {final_model}</h3>
            <p style="margin:4px 0 0 0; color: #94a3b8; font-size: 13px;">
                <b>المحرك:</b> {final_engine} | <b>المنظومة:</b> {fuel_system} ({cylinders_config})
            </p>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

# 8. قطاع الأجهزة المنزلية
elif domain_code == "appliances":
    st.subheader(t["d_appliances"])
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        appliance_type = st.selectbox(
            t["appliance_type"],
            ["غسالة ملابس (Washing Machine)", "ثلاجة / مجمد (Refrigerator/Freezer)", "مكيف هواء (Air Conditioner)", "جلاية صحون (Dishwasher)"],
            key=f"app_type_{lang}"
        )
    with col_a2:
        brand = st.selectbox(t["appliance_brand"], ["LG", "Samsung", "Bosch", "Whirlpool", "Gree"], key=f"app_brand_{lang}")
    with col_a3:
        model = st.text_input(t["appliance_model"], "Inverter Direct Drive", key=f"app_model_{lang}")

# 9. القطاع الصناعي
else:
    st.subheader(t["d_industrial"])
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1:
        machine_type = st.selectbox(
            t["machine_type"],
            ["محرك كهربائي ثلاثي الأوجه (3-Phase Motor)", "مضخة مياه هيدروليكية (Water Pump)", "ضاغط هواء حلزوني (Screw Compressor)", "مولد ديزل (Diesel Generator)"],
            key=f"ind_type_{lang}"
        )
    with col_i2:
        power_rating = st.text_input(t["machine_power"], "50 HP / 37 kW", key=f"ind_power_{lang}")
    with col_i3:
        rpm_val = st.text_input(t["machine_rpm"], "1450 RPM", key=f"ind_rpm_{lang}")

st.markdown("---")

# 10. التقاط الصوت
st.markdown(f"### {t['audio_section']}")
col_rec1, col_rec2 = st.columns(2)

with col_rec1:
    st.write(f"<b>1. {t['rec_mic']}</b>", unsafe_allow_html=True)
    recorded_audio = st.audio_input("اضغط للبدء بالتسجيل المباشر 🎙", key=f"mic_in_{lang}")

with col_rec2:
    st.write(f"<b>2. {t['upload_file']}</b>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("ارفع ملف الصوت من جهازك:", type=["wav", "mp3", "ogg"], key=f"file_in_{lang}")

audio_source = recorded_audio or uploaded_file
if audio_source:
    st.audio(audio_source)
    st.success("✅ تم استقبال الإشارة الصوتية بنجاح وهي جاهزة للفحص الطيفي!")

st.markdown("---")

# 11. دالة التقرير الآمنة البرمجياً
def generate_expanded_car_report(brand, model, engine, fuel, cylinders, lang_code):
    b, m, e, f, c = str(brand), str(model), str(engine), str(fuel), str(cylinders)
    is_diesel = ("Diesel" in f) or ("CRDi" in e) or ("TDI" in e)
    is_turbo = ("Turbo" in f) or ("Turbo" in e) or ("TSI" in e)

    if lang_code == "العربية":
        inj_str = "ترددات بخاخات الديزل ذات الضغط العالي متزنة ونقية." if is_diesel else "نظام حقن البنزين يعمل بانتظام وبضوضاء ضمن الحدود الطبيعية."
        turbo_str = "عنفة التوربو تعمل بستارة صوتية مستقرة دون صفير." if is_turbo else "منظومة سحب الهواء وتطابق الضغط تعمل بكفاءة عالية."
        
        paragraphs = [
            f"<b>1. تحليل طيف فوريه الترددي (FFT):</b><br>تم تفكيك الإشارة الصوتية لسيارة <b>{b} {m}</b> (محرك <b>{e}</b>). التردد يطابق زمن الاحتراق للـ {c}.",
            f"<b>2. معاينة صمامات ومحاور الكامبشافت:</b><br>خلوص الصبابات والصمامات يعمل ضمن المجال القياسي لشركة {b}.",
            f"<b>3. نظام حقن الوقود والضغط العالي:</b><br>{inj_str}",
            f"<b>4. الشاحن التوربيني وسحب الهواء:</b><br>{turbo_str}",
            "<b>5. محامل الدوران وعمود الكرنك والحذافة:</b><br>لا توجد اهتزازات منخفضة التردد، والحذافة امتصت الصدمات بكفاءة.",
            f"<b>6. التوصيات الهندسية وخطة الصيانة:</b><br>المحرك بحالة ممتازة. يوصى بصيانة زيت {b} الأصلي عند 10,000 كم."
        ]
        return "<br><br>".join(paragraphs)

    elif lang_code == "English":
        inj_str = "High-pressure Common Rail Diesel injectors are synchronized." if is_diesel else "Gasoline injection pulses show clean harmonics."
        turbo_str = "Turbocharger spool frequency exhibits smooth resonance." if is_turbo else "Naturally aspirated air intake shows no pressure leaks."
        
        paragraphs = [
            f"<b>1. FFT Acoustic Spectrum Core Analysis:</b><br>Acoustic signal breakdown for <b>{b} {m}</b> ({e}). Dominant peak matches {c}.",
            f"<b>2. Valve Train & Camshaft Inspection:</b><br>Valve clearances operate strictly within {b} specs.",
            f"<b>3. Fuel Injection System:</b><br>{inj_str}",
            f"<b>4. Turbocharger & Induction Harmonics:</b><br>{turbo_str}",
            "<b>5. Bearings & Flywheel Dynamics:</b><br>Crankshaft bearings show zero low-frequency rumble.",
            f"<b>6. Maintenance & Engineering Plan:</b><br>Overall powertrain acoustic health is optimal. Service {b} regularly."
        ]
        return "<br><br>".join(paragraphs)

    else:
        inj_str = "Импульсы форсунок высокого давления синхронизированы." if is_diesel else "Импульсы впрыска бензина демонстрируют чистые гармоники."
        turbo_str = "Частота турбоком
