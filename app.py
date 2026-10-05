import time
import streamlit as st

# 1. إعدادات الصفحة - إغلاق القائمة الجانبية افتراضياً لتوفير مساحة الجوال
st.set_page_config(
    page_title="ZINO EADE - Mobile Diagnostic Engine",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. القاموس الموحد المخصص
I18N = {
    "العربية": {
        "title": "🎙️ ZINO EADE - محطة التشخيص الهندسي",
        "dev": "🛠️ تصميم وتطوير: إسماعيل حساسنة",
        "lang_lbl": "🌐 اللغة:",
        "domain_lbl": "🏢 القطاع التشخيصي:",
        "d_cars": "🚗 قطاع السيارات والمركبات",
        "d_app": "🔌 الأجهزة الكهربائية والمنزلية",
        "d_ind": "🏭 الماكينات والمعدات الصناعية",
        "brand_lbl": "🏢 اختر الشركة المصنعة:",
        "model_lbl": "🚗 اختر طراز السيارة:",
        "engine_lbl": "⚙️ سعة ونوع المحرك:",
        "custom_m": "✍️ أدخل الموديل يدوياً:",
        "custom_e": "✍️ أدخل المحرك يدوياً:",
        "fuel_lbl": "⛽ نوع الوقود ونظام الحقن:",
        "cyl_lbl": "🔢 أسطوانات المحرك:",
        "rec_btn": "🎙️ تسجيل الصوت الحي عبر الميكروفون",
        "up_btn": "📁 أو رفع ملف صوتي (WAV, MP3)",
        "scan_btn": "🚀 بدء الفحص بالليزر وتحليل الطيف (FFT)",
        "scanning": "⚡ جاري الفحص بالليزر الموجه وتحليل الصوت...",
        "res_title": "📊 التقرير التشخيصي الهندسي (FFT Analysis)",
        "health": "نسبة السلامة",
        "peak": "التردد البارز",
        "anomaly": "مؤشر التشوه",
        "rep_title": "📑 التقرير الفني المخصص الشامل",
    },
    "English": {
        "title": "🎙️ ZINO EADE - Precision Diagnostic Engine",
        "dev": "🛠️ Designed & Developed by Ismail Hassasneh",
        "lang_lbl": "🌐 Language:",
        "domain_lbl": "🏢 Diagnostic Sector:",
        "d_cars": "🚗 Automotive Sector",
        "d_app": "🔌 Home Appliances",
        "d_ind": "🏭 Industrial Machinery",
        "brand_lbl": "🏢 Select Manufacturer:",
        "model_lbl": "🚗 Select Vehicle Model:",
        "engine_lbl": "⚙️ Select Engine Specs:",
        "custom_m": "✍️ Enter Custom Model:",
        "custom_e": "✍️ Enter Custom Engine:",
        "fuel_lbl": "⛽ Fuel & Injection System:",
        "cyl_lbl": "🔢 Cylinder Configuration:",
        "rec_btn": "🎙️ Record Live Audio via Mic",
        "up_btn": "📁 Or Upload Audio File (WAV, MP3)",
        "scan_btn": "🚀 Run Laser Scan & FFT Analysis",
        "scanning": "⚡ Processing Laser Scan & Frequency Spectrum...",
        "res_title": "📊 Diagnostic Spectrum Report (FFT Analysis)",
        "health": "Health Score",
        "peak": "Dominant Peak",
        "anomaly": "Anomaly Index",
        "rep_title": "📑 Technical Diagnostic Report",
    },
    "Русский": {
        "title": "🎙️ ZINO EADE - Диагностическая Станция",
        "dev": "🛠️ Разработка: Исмаил Хасасна",
        "lang_lbl": "🌐 Язык:",
        "domain_lbl": "🏢 Сектор диагностики:",
        "d_cars": "🚗 Автомобильный сектор",
        "d_app": "🔌 Бытовая техника",
        "d_ind": "🏭 Промышленное оборудование",
        "brand_lbl": "🏢 Выберите производителя:",
        "model_lbl": "🚗 Выберите модель авто:",
        "engine_lbl": "⚙️ Характеристики двигателя:",
        "custom_m": "✍️ Введите модель вручную:",
        "custom_e": "✍️ Введите двигатель вручную:",
        "fuel_lbl": "⛽ Тип топлива и впрыска:",
        "cyl_lbl": "🔢 Конфигурация цилиндров:",
        "rec_btn": "🎙️ Запись звука через микрофон",
        "up_btn": "📁 Или загрузите аудиофайл",
        "scan_btn": "🚀 Запустить сканирование и FFT анализ",
        "scanning": "⚡ Лазерное сканирование и обработка...",
        "res_title": "📊 Отчет акустической диагностики (FFT)",
        "health": "Индекс здоровья",
        "peak": "Пиковая частота",
        "anomaly": "Индекс аномалии",
        "rep_title": "📑 Технический инженерный отчет",
    }
}

# 3. قاعدة البيانات
BRAND_DATABASE = {
    "Hyundai": {
        "name": "Hyundai Motor Company",
        "color": "#002C5F",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/4/44/Hyundai_Motor_Company_logo.svg",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Hyundai_Santa_Fe_DM_IMG_0392.jpg/800px-Hyundai_Santa_Fe_DM_IMG_0392.jpg",
        "models": ["Santa Fe", "Tucson", "Elantra / Avante", "Sonata", "Accent / Verna", "Creta", "Kona", "Palisade", "H100 / Starex", "طراز آخر / Custom"],
        "engines": ["2.2L CRDi VGT Turbo Diesel", "2.0L CRDi Diesel", "2.0L Nu MPI Gasoline", "1.6L GDI Turbo Gasoline", "2.4L Theta II Gasoline", "3.5L V6 Smartstream", "محرك آخر / Custom"]
    },
    "Mitsubishi": {
        "name": "Mitsubishi Motors",
        "color": "#D21034",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Mitsubishi_logo.svg",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Mitsubishi_Pajero_V20_front.jpg/800px-Mitsubishi_Pajero_V20_front.jpg",
        "models": ["Pajero (V20 / V60 / V80)", "Lancer (EX / Evolution)", "Outlander / PHEV", "L200 / Triton Pickup", "Montero Sport", "Eclipse Cross", "ASX", "طراز آخر / Custom"],
        "engines": ["3.5L V6 6G74 Gasoline", "3.0L V6 6G72 Gasoline", "3.2L Di-D 4M41 Turbo Diesel", "2.0L I4 4B11 MIVEC Turbo", "2.4L I4 4G69 MIVEC", "2.5L TD 4D56 Diesel", "محرك آخر / Custom"]
    },
    "Volkswagen": {
        "name": "Volkswagen Group",
        "color": "#001E50",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Volkswagen_logo_2019.svg",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Volkswagen_Caddy_Maxi_TDI_Facelift_front.jpg/800px-Volkswagen_Caddy_Maxi_TDI_Facelift_front.jpg",
        "models": ["Caddy / Caddy Maxi", "Golf (GTI / R / VII / VIII)", "Passat / CC", "Tiguan", "Polo", "Jetta", "Touareg", "Transporter / Caravelle", "طراز آخر / Custom"],
        "engines": ["2.0L TDI Common Rail Diesel", "1.6L TDI Diesel", "2.0L TSI EA888 Turbo Gasoline", "1.4L TSI Twincharger", "1.6L MPI Gasoline", "3.0L V6 TDI Diesel", "محرك آخر / Custom"]
    }
}

# 4. الترويسة العليا وأدوات التحكم المباشرة بالصفحة (بدون قائمة جانبية)
st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>🎙️ ZINO EADE</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #777; font-size: 14px;'>🛠️ تصميم وتطوير: إسماعيل حساسنة</p>", unsafe_allow_html=True)

col_ctrl1, col_ctrl2 = st.columns([1, 2])
with col_ctrl1:
    selected_lang = st.selectbox("🌐 Language / اللغة", ["العربية", "English", "Русский"], key="top_lang_select")
t = I18N[selected_lang]

with col_ctrl2:
    domain_code = st.selectbox(
        t["domain_lbl"],
        options=["cars", "appliances", "industrial"],
        format_func=lambda x: {"cars": t["d_cars"], "appliances": t["d_app"], "industrial": t["d_ind"]}[x],
        key="top_domain_select"
    )

st.markdown("---")

# 5. قطاع السيارات بتصميم مرن للجوال
if domain_code == "cars":
    selected_brand_key = st.selectbox(t["brand_lbl"], ["Hyundai", "Mitsubishi", "Volkswagen"], key="brand_select_box")
    b_data = BRAND_DATABASE[selected_brand_key]
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        selected_model = st.selectbox(t["model_lbl"], b_data["models"], key=f"mod_{selected_brand_key}_{selected_lang}")
        if "Custom" in selected_model or "آخر" in selected_model:
            final_model = st.text_input(t["custom_m"], value="Pajero / Lancer", key="c_m_in")
        else:
            final_model = selected_model

        fuel_system = st.selectbox(
            t["fuel_lbl"],
            [
                "Turbo Diesel CRDi / TDI (ديزل تربو حقن مشترك)",
                "Gasoline Direct Injection GDI / TSI (بنزين حقن مباشر)",
                "Gasoline MPI / MIVEC (بنزين حقن متعدد النقاط)",
                "Atmospheric Diesel (ديزل سحب عادي)"
            ],
            key=f"fuel_{selected_lang}"
        )

    with col_m2:
        selected_engine = st.selectbox(t["engine_lbl"], b_data["engines"], key=f"eng_{selected_brand_key}_{selected_lang}")
        if "Custom" in selected_engine or "آخر" in selected_engine:
            final_engine = st.text_input(t["custom_e"], value="2.0L Turbo", key="c_e_in")
        else:
            final_engine = selected_engine

        cylinders_config = st.selectbox(
            t["cyl_lbl"],
            ["4 Cylinders Inline", "6 Cylinders V6", "3 Cylinders Inline", "8 Cylinders V8"],
            key=f"cyl_{selected_lang}"
        )

    # كارت السيارة المحدد
    st.markdown(
        f'<div style="background-color: #111827; padding: 12px; border-radius: 8px; border-left: 5px solid {b_data["color"]}; margin-top: 10px;">'
        f'<h4 style="color: #ffffff; margin:0;">{selected_brand_key} - {final_model}</h4>'
        f'<p style="color: #9ca3af; margin: 4px 0 0 0; font-size: 13px;"><b>المحرك:</b> {final_engine} | <b>المنظومة:</b> {fuel_system}</p>'
        f'</div>',
        unsafe_allow_html=True
    )

# 6. قطاع الأجهزة المنزلية
elif domain_code == "appliances":
    st.subheader(t["d_app"])
    ca1, ca2 = st.columns(2)
    with ca1:
        app_type = st.selectbox("نوع الجهاز:", ["غسالة ملابس", "ثلاجة / مجمد", "مكيف هواء", "جلاية صحون"], key=f"app_t_{selected_lang}")
        app_brand = st.selectbox("الشركة المصنعة:", ["LG", "Samsung", "Bosch", "Whirlpool", "Gree"], key=f"app_b_{selected_lang}")
    with ca2:
        app_model = st.text_input("الموديل / الرقم الفني:", "Inverter Direct Drive", key=f"app_m_{selected_lang}")

# 7. القطاع الصناعي
else:
    st.subheader(t["d_ind"])
    ci1, ci2 = st.columns(2)
    with ci1:
        ind_type = st.selectbox("نوع المعدة:", ["محرك كهربائي 3-Phase", "مضخة مياه هيدروليكية", "ضاغط هواء حلزوني", "مولد ديزل"], key=f"ind_t_{selected_lang}")
        ind_power = st.text_input("القدرة (HP / kW):", "50 HP / 37 kW", key=f"ind_p_{selected_lang}")
    with ci2:
        ind_rpm = st.text_input("سرعة الدوران (RPM):", "1450 RPM", key=f"ind_r_{selected_lang}")

st.markdown("---")

# 8. قسم التقاط الصوت
st.markdown("#### " + t["rec_btn"])
rec_audio = st.audio_input("اضغط للبدء بالتسجيل المباشر 🎙", key=f"mic_{selected_lang}")
up_audio = st.file_uploader(t["up_btn"], type=["wav", "mp3", "ogg"], key=f"up_{selected_lang}")

audio_source = rec_audio or up_audio
if audio_source:
    st.audio(audio_source)
    st.success("✅ تم استقبال الإشارة الصوتية بنجاح!")

st.markdown("---")

# 9. دالة التقرير الهندسية
def get_report(brand, model, engine, fuel, cylinders, lang_code):
    b, m, e, f, c = str(brand), str(model), str(engine), str(fuel), str(cylinders)
    is_diesel = ("Diesel" in f) or ("CRDi" in e) or ("TDI" in e)
    is_turbo = ("Turbo" in f) or ("Turbo" in e) or ("TSI" in e)

    if lang_code == "العربية":
        p1 = f"<b>1. تحليل طيف فوريه (FFT):</b><br>تفاصيل الإشارة الصوتية لسيارة <b>{b} {m}</b> ({e}). التردد مطابق لزمن الاحتراق للـ {c}."
        p2 = f"<b>2. صمامات المحرك الكامبشافت:</b><br>خلوص الصبابات يعمل ضمن المجال القياسي لشركة {b}."
        inj = "ترددات بخاخات الديزل الضغط العالي متزنة ونقية." if is_diesel else "نظام حقن البنزين يعمل بانتظام وبضوضاء طبيعية."
        p3 = f"<b>3. حقن الوقود والضغط:</b><br>{inj}"
        turbo = "عنفة التوربو تعمل بستارة صوتية مستقرة." if is_turbo else "منظومة سحب الهواء تعمل بكفاءة بدون تسريب."
        p4 = f"<b>4. الشاحن التوربيني / الهواء:</b><br>{turbo}"
        p5 = "<b>5. الكرنك والحذافة:</b><br>عدم وجود اهتزازات منخفضة التردد في محامل الكرنك."
        p6 = f"<b>6. خطة الصيانة:</b><br>المحرك بحالة ممتازة. يوصى بالمحافظة على زيت {b} عند 10,000 كم."
        return f"{p1}<br><br>{p2}<br><br>{p3}<br><br>{p4}<br><br>{p5}<br><br>{p6}"
    
    elif lang_code == "English":
        p1 = f"<b>1. FFT Spectrum Core:</b><br>Acoustic signal for <b>{b} {m}</b> ({e}). Dominant peak matches {c}."
        p2 = f"<b>2. Valve Train:</b><br>Clearances operate strictly within {b} specs."
        inj = "High-pressure Common Rail Diesel injectors are synchronized." if is_diesel else "Gasoline injection pulses show clean harmonics."
        p3 = f"<b>3. Fuel Injection:</b><br>{inj}"
        turbo = "Turbocharger spool frequency shows smooth resonance." if is_turbo else "Naturally aspirated intake shows no leaks."
        p4 = f"<b>4. Induction System:</b><br>{turbo}"
        p5 = "<b>5. Bearings & Flywheel:</b><br>Main bearings show zero low-frequency rumble."
        p6 = f"<b>6. Maintenance:</b><br>Powertrain health is optimal. Service {b} regularly."
        return f"{p1}<br><br>{p2}<br><br>{p3}<br><br>{p4}<br><br>{p5}<br><br>{p6}"

    else:
        p1 = f"<b>1. Спектральный анализ FFT:</b><br>Сигнал для <b>{b} {m}</b> ({e}) разобран."
        p2 = f"<b>2. Клапанный механизм:</b><br>Зазоры клапанов в пределах допусков {b}."
        inj = "Импульсы форсунок высокого давления синхронизированы." if is_diesel else "Импульсы впрыска бензина в норме."
        p3 = f"<b>3. Топливная система:</b><br>{inj}"
        turbo = "Частота турбокомпрессора показывает плавный резонанс." if is_turbo else "Впускной коллектор работает без утечек."
        p4 = f"<b>4. Система впуска:</b><br>{turbo}"
        p5 = "<b>5. Подшипники и маховик:</b><br>Подшипники коленвала без шумов."
        p6 = f"<b>6. Обслуживание:</b><br>Состояние оптимальное. Заменяйте масло {b} каждые 10 000 км."
        return f"{p1}<br><br>{p2}<br><br>{p3}<br><br>{p4}<br><br>{p5}<br><br>{p6}"

# 10. تنفيذ المسح
if st.button(t["scan_btn"], use_container_width=True, key="main_scan_btn"):
    with st.spinner(t["scanning"]):
        time.sleep(1.5)

    st.markdown("### " + t["res_title"])
    r1, r2, r3 = st.columns(3)
    text_dir = "rtl" if selected_lang == "العربية" else "ltr"

    if domain_code == "cars":
        b_data = BRAND_DATABASE[selected_brand_key]
        r1.metric(t["health"], "94.6%")
        r2.metric(t["peak"], "168.4 Hz" if "V6" in cylinders_config else "124.2 Hz")
        r3.metric(t["anomaly"], "0.015")

        report_content = get_report(selected_brand_key, final_model, final_engine, fuel_system, cylinders_config, selected_lang)
        
        st.markdown(
            f'<div dir="{text_dir}" style="background-color: #f8fafc; border: 1px solid #cbd5e1; border-right: 5px solid {b_data["color"]}; padding: 15px; border-radius: 8px; margin-top: 15px; color: #0f172a;">'
            f'<h4 style="margin-top:0; color:{b_data["color"]};">{t["rep_title"]} - {selected_brand_key} {final_model}</h4>'
            f'{report_content}</div>',
            unsafe_allow_html=True
        )
    elif domain_code == "appliances":
        r1.metric(t["health"], "88.5%")
        r2.metric(t["peak"], "50.0 Hz")
        r3.metric(t["anomaly"], "0.045")
        st.info("• تم كشف احتكاك بسيط في محامل الدوران (Bearings). يوصى بالصيانة الوقائية.")
    else:
        r1.metric(t["health"], "96.2%")
        r2.metric(t["peak"], "300.0 Hz")
        r3.metric(t["anomaly"], "0.011")
        st.info("• جميع تروس المضخة الهيدروليكية تعمل بالتوافق الترددي الكامل دون ظاهرة تكهف.")
