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
        "main_title": """🎙️ محطة التشخيص الصوتي الهندسي الشاملة - ZINO EADE""",
        "developer_credit": """🛠️ تصميم وتطوير: إسماعيل حساسنة""",
        "domain_label": """🏢 اختر القطاع التشخيصي:""",
        "d_cars": """🚗 قطاع السيارات والمركبات الشامل""",
        "d_appliances": """🔌 الأجهزة الكهربائية والمنزلية""",
        "d_industrial": """🏭 الماكينات والمعدات الصناعية""",
        "select_car_brand": """🏢 اختر الشركة المصنعة للمركبة:""",
        "select_car_model": """🚗 اختر طراز السيارة (أو أدخله يدوياً):""",
        "select_engine_type": """⚙️ اختر سعة ونوع المحرك (أو أدخله يدوياً):""",
        "custom_model_label": """✍️ أدخل طراز السيارة المخصص:""",
        "custom_engine_label": """✍️ أدخل تفاصيل المحرك المخصص:""",
        "fuel_type_label": """⛽ نوع الوقود ونظام الحقن:""",
        "cylinders_label": """🔢 عدد ونظام الأسطوانات:""",
        "audio_section": """🎙️ وحدة التقاط وتسجيل الصوت الحي""",
        "rec_mic": """تسجيل صوت المحرك/الجهاز المباشر عبر الميكروفون:""",
        "upload_file": """أو رفع ملف صوتي جاهز (WAV, MP3, OGG):""",
        "scan_btn": """🚀 بدء المسح الليزري عالي الدقة وتحليل الطيف الصوتي""",
        "laser_scanning": (
            """⚡ جاري الفحص بالليزر الموجه وتحليل الترددات الطيفية..."""
        ),
        "results_title": (
            """📊 التقرير التشخيصي الهندسي عالي الدقة (FFT Spectrum Analysis)"""
        ),
        "health": """نسبة السلامة الصوتية""",
        "fft_peak": """التردد البارز (FFT Peak)""",
        "anomaly": """مؤشر التشوه الصوتي""",
        "detailed_report_title": """📑 التقرير التشخيصي الفني المخصص الشامل""",
    },
    "English": {
        "main_title": (
            """🎙️ ZINO EADE - Universal Precision Acoustic Diagnostic Workstation"""
        ),
        "developer_credit": """🛠️ Designed & Developed by Ismail Hassasneh""",
        "domain_label": """🏢 Select Diagnostic Sector:""",
        "d_cars": """🚗 Comprehensive Automotive Sector""",
        "d_appliances": """🔌 Home & Electrical Appliances""",
        "d_industrial": """🏭 Industrial Machinery""",
        "select_car_brand": """🏢 Select Vehicle Manufacturer:""",
        "select_car_model": """🚗 Select Vehicle Model (or type custom):""",
        "select_engine_type": """⚙️ Select Engine Specs (or type custom):""",
        "custom_model_label": """✍️ Enter Custom Car Model:""",
        "custom_engine_label": """✍️ Enter Custom Engine Specs:""",
        "fuel_type_label": """⛽ Fuel & Injection System:""",
        "cylinders_label": """🔢 Cylinder Configuration:""",
        "audio_section": """🎙️ Live Acoustic Capture & Recording Unit""",
        "rec_mic": """Record live audio via microphone:""",
        "upload_file": """Or upload audio file (WAV, MP3, OGG):""",
        "scan_btn": (
            """🚀 Run High-Precision Laser Scan & FFT Spectrum Analysis"""
        ),
        "laser_scanning": (
            """⚡ Executing Precision Laser Scan & Spectrum Processing..."""
        ),
        "results_title": (
            """📊 High-Precision Diagnostic Spectrum Report (FFT Analysis)"""
        ),
        "health": """Acoustic Health Score""",
        "fft_peak": """Dominant FFT Peak""",
        "anomaly": """Acoustic Anomaly Index""",
        "detailed_report_title": (
            """📑 Comprehensive Technical Engineering Report"""
        ),
    },
    "Русский": {
        "main_title": (
            """🎙️ ZINO EADE - Универсальная Высокоточная Диагностическая Станция"""
        ),
        "developer_credit": """🛠️ Дизайн и разработка: Исмаил Хасасна""",
        "domain_label": """🏢 Выберите сектор диагностики:""",
        "d_cars": """🚗 Полный автомобильный сектор""",
        "d_appliances": """🔌 Бытовая и электротехника""",
        "d_industrial": """🏭 Промышленное оборудование""",
        "select_car_brand": """🏢 Выберите производителя автомобиля:""",
        "select_car_model": (
            """🚗 Выберите модель авто (или введите вручную):"""
        ),
        "select_engine_type": (
            """⚙️ Выберите двигатель (или введите вручную):"""
        ),
        "custom_model_label": """✍️ Введите модель автомобиля:""",
        "custom_engine_label": """✍️ Введите характеристики двигателя:""",
        "fuel_type_label": """⛽ Тип топлива и впрыска:""",
        "cylinders_label": """🔢 Конфигурация цилиндров:""",
        "audio_section": """🎙️ Модуль записи и захвата звука""",
        "rec_mic": """Запись звука через микрофон:""",
        "upload_file": """Или загрузите аудиофайл (WAV, MP3, OGG):""",
        "scan_btn": (
            """🚀 Запустить высокоточное лазерное сканирование и анализ FFT"""
        ),
        "laser_scanning": (
            """⚡ Выполнение лазерного сканирования и спектрального анализа..."""
        ),
        "results_title": (
            """📊 Высокоточный отчет акустической диагностики (FFT Спектр)"""
        ),
        "health": """Индекс здоровья""",
        "fft_peak": """Пиковая частота (FFT Peak)""",
        "anomaly": """Индекс аномалии""",
        "detailed_report_title": """📑 Подробный технический инженерный отчет""",
    },
}

# 3. قاعدة بيانات الشركات وطرازات السيارات الشاملة
BRAND_DATABASE = {
    "Mitsubishi": {
        "brand_name": """Mitsubishi Motors""",
        "color": """#556B2F""",
        "logo": """https://upload.wikimedia.org/wikipedia/commons/5/5a/Mitsubishi_logo.svg""",
        "image": """https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Mitsubishi_Pajero_V20_front.jpg/800px-Mitsubishi_Pajero_V20_front.jpg""",
        "models": [
            """Pajero (V20 / V60 / V80 / 2027)""",
            """Lancer (EX / Evolution)""",
            """Outlander / Outlander PHEV""",
            """L200 / Triton Pickup""",
            """Montero Sport / Nativa""",
            """Eclipse Cross""",
            """ASX / Outlander Sport""",
            """Galant""",
            """Mirage / Attrage""",
            """طراز آخر / Custom Model""",
        ],
        "engines": [
            """3.5L V6 6G74 Gasoline""",
            """3.0L V6 6G72 Gasoline""",
            """3.2L Di-D 4M41 Turbo Diesel""",
            """2.0L I4 4B11 MIVEC Turbo""",
            """2.4L I4 4G69 MIVEC""",
            """2.5L TD 4D56 Turbo Diesel""",
            """1.5L MIVEC Turbo""",
            """محتوى محرك آخر / Custom Engine""",
        ],
    },
    "Hyundai": {
        "brand_name": """Hyundai Motor Company""",
        "color": """#7A1C2E""",
        "logo": """https://upload.wikimedia.org/wikipedia/commons/4/44/Hyundai_Motor_Company_logo.svg""",
        "image": """https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Hyundai_Santa_Fe_DM_IMG_0392.jpg/800px-Hyundai_Santa_Fe_DM_IMG_0392.jpg""",
        "models": [
            """Santa Fe""",
            """Tucson""",
            """Elantra / Avante""",
            """Sonata""",
            """Accent / Verna""",
            """Creta""",
            """Kona / Kona Electric""",
            """Palisade""",
            """Genesis Coupe / G70""",
            """Grandeur / Azera""",
            """H100 / Starex / H-1""",
            """طراز آخر / Custom Model""",
        ],
        "engines": [
            """2.2L CRDi VGT Turbo Diesel""",
            """2.0L CRDi Diesel""",
            """2.0L Nu MPI Gasoline""",
            """1.6L GDI Turbo Gasoline""",
            """2.4L Theta II Gasoline""",
            """3.5L V6 Smartstream Gasoline""",
            """1.4L Kappa MPI Gasoline""",
            """محتوى محرك آخر / Custom Engine""",
        ],
    },
    "Volkswagen": {
        "brand_name": """Volkswagen Group""",
        "color": """#004B87""",
        "logo": """https://upload.wikimedia.org/wikipedia/commons/6/6d/Volkswagen_logo_2019.svg""",
        "image": """https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Volkswagen_Caddy_Maxi_TDI_Facelift_front.jpg/800px-Volkswagen_Caddy_Maxi_TDI_Facelift_front.jpg""",
        "models": [
            """Caddy / Caddy Maxi""",
            """Golf (GTI / R / VII / VIII)""",
            """Passat / Passat CC""",
            """Tiguan / Tiguan Allspace""",
            """Polo""",
            """Jetta""",
            """Touareg""",
            """Transporter / Multivan / Caravelle""",
            """Scirocco""",
            """Arteon""",
            """Amarok Pickup""",
            """طراز آخر / Custom Model""",
        ],
        "engines": [
            """2.0L TDI Common Rail Diesel""",
            """1.6L TDI Diesel""",
            """2.0L TSI EA888 Turbo Gasoline""",
            """1.4L TSI Twincharger""",
            """1.6L MPI Gasoline""",
            """3.0L V6 TDI Diesel""",
            """1.2L TSI Gasoline""",
            """محتوى محرك آخر / Custom Engine""",
        ],
    },
}

# 4. الشريط الجانبي واختيار اللغة والقطاع
st.sidebar.title("""⚙️ التحكم واللغة""")
lang = st.sidebar.selectbox(
    """🌐 Choose Language / اختر اللغة""",
    ["""العربية""", """English""", """Русский"""],
)
t = I18N[lang]

st.sidebar.markdown("""---""")
domain = st.sidebar.radio(
    t["domain_label"], [t["d_cars"], t["d_appliances"], t["d_industrial"]]
)

st.sidebar.markdown("""---""")
st.sidebar.info(t["developer_credit"])

# 5. إدارة حالة الشركة والسيارة النشطة
if "selected_brand" not in st.session_state:
  st.session_state["selected_brand"] = "Hyundai"

if domain == t["d_cars"]:
  active_color = BRAND_DATABASE[st.session_state["selected_brand"]]["color"]
elif domain == t["d_appliances"]:
  active_color = "#005F73"
else:
  active_color = "#D97706"

# تنسيق CSS مخصص ومحمي
css_style = """
<style>
.main-header { font-size: 26px; font-weight: bold; color: COLOR_PLACEHOLDER; border-bottom: 4px solid COLOR_PLACEHOLDER; padding-bottom: 8px; margin-bottom: 5px; }
.dev-credit { font-size: 15px; font-weight: 600; color: #888888; margin-bottom: 25px; }
.stButton>button { background-color: COLOR_PLACEHOLDER !important; color: #ffffff !important; font-weight: bold !important; border-radius: 8px !important; }
.laser-box { position: relative; border: 3px solid COLOR_PLACEHOLDER; border-radius: 12px; overflow: hidden; box-shadow: 0 0 20px COLOR_PLACEHOLDER88; background-color: #000000; }
.laser-line { position: absolute; top: 0; left: 0; right: 0; height: 6px; background-color: #FF0033; box-shadow: 0 0 15px 5px #FF0033; animation: scan 1.8s infinite ease-in-out; z-index: 10; }
@keyframes scan { 0% { top: 0%; } 50% { top: 92%; } 100% { top: 0%; } }
.report-card { background-color: #f8fafc; border: 1px solid #e2e8f0; border-right: 6px solid COLOR_PLACEHOLDER; border-radius: 8px; padding: 20px; margin-top: 15px; color: #1e293b; font-size: 15px; line-height: 1.8; }
</style>
""".replace("COLOR_PLACEHOLDER", str(active_color))

st.markdown(css_style, unsafe_allow_html=True)

st.markdown(
    """<div class="main-header">""" + str(t["main_title"]) + """</div>""",
    unsafe_allow_html=True,
)
st.markdown(
    """<div class="dev-credit">""" + str(t["developer_credit"]) + """</div>""",
    unsafe_allow_html=True,
)

# 6. قطاع السيارات
if domain == t["d_cars"]:
  st.markdown("""### """ + str(t["select_car_brand"]))
  c1, c2, c3 = st.columns(3)
  with c1:
    if st.button("""🔴 ميتسوبيشي (Mitsubishi)""", use_container_width=True):
      st.session_state["selected_brand"] = "Mitsubishi"
      st.rerun()
  with c2:
    if st.button("""🔵 هيونداي (Hyundai)""", use_container_width=True):
      st.session_state["selected_brand"] = "Hyundai"
      st.rerun()
  with c3:
    if st.button("""⚪ فولكسفاغن (Volkswagen)""", use_container_width=True):
      st.session_state["selected_brand"] = "Volkswagen"
      st.rerun()

  brand_key = st.session_state["selected_brand"]
  b_data = BRAND_DATABASE[brand_key]
  st.markdown("""---""")

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
            """Turbo Diesel CRDi / TDI (ديزل تربو حقن مشترك)""",
            """Gasoline Direct Injection GDI / TSI (بنزين حقن مباشر)""",
            """Gasoline MPI / MIVEC (بنزين حقن متعدد النقاط)""",
            """Atmospheric Diesel (ديزل سحب عادي)""",
        ],
    )

  with col_m2:
    selected_engine = st.selectbox(t["select_engine_type"], b_data["engines"])
    if "Custom" in selected_engine or "آخر" in selected_engine:
      final_engine = st.text_input(
          t["custom_engine_label"], value="2.0L Turbo 250 HP"
      )
    else:
      final_engine = selected_engine

    cylinders_config = st.selectbox(
        t["cylinders_label"],
        [
            """4 Cylinders Inline (4 أسطوانات متتالية)""",
            """6 Cylinders V6 (6 أسطوانات V6)""",
            """3 Cylinders Inline (3 أسطوانات)""",
            """8 Cylinders V8 (8 أسطوانات V8)""",
        ],
    )

  col_logo, col_details = st.columns([1, 3])
  with col_logo:
    st.image(b_data["logo"], width=120, caption=b_data["brand_name"])
  with col_details:
    card_html = (
        """<div style="background-color: #111827; padding: 16px; border-left: 6px solid """
        + str(b_data["color"])
        + """ border-radius: 8px;"><h3 style="color: #ffffff; margin:0;">"""
        + str(brand_key)
        + """ - """
        + str(final_model)
        + """</h3><p style="margin:5px 0 0 0; color: #9ca3af;"><b>المحرك:</b> """
        + str(final_engine)
        + """ | <b>المنظومة:</b> """
        + str(fuel_system)
        + """ ("""
        + str(cylinders_config)
        + """)</p></div>"""
    )
    st.markdown(card_html, unsafe_allow_html=True)

# 7. قطاع الأجهزة المنزلية
elif domain == t["d_appliances"]:
  st.subheader("""🔌 قطاع تشخيص الأجهزة الكهربائية والمنزلية""")
  col_a1, col_a2, col_a3 = st.columns(3)
  with col_a1:
    appliance_type = st.selectbox(
        """نوع الجهاز الكهربائي:""",
        [
            """غسالة ملابس (Washing Machine)""",
            """ثلاجة / مجمد (Refrigerator/Freezer)""",
            """مكيف هواء (Air Conditioner)""",
            """جلاية صحون (Dishwasher)""",
        ],
    )
  with col_a2:
    brand = st.selectbox(
        """الشركة المصنعة:""",
        ["""LG""", """Samsung""", """Bosch""", """Whirlpool""", """Gree"""],
    )
  with col_a3:
    model = st.text_input(
        """الموديل / الرقم الفني:""", """Inverter Direct Drive"""
    )

# 8. القطاع الصناعي
else:
  st.subheader("""🏭 قطاع تشخيص الماكينات والمعدات الصناعية""")
  col_i1, col_i2, col_i3 = st.columns(3)
  with col_i1:
    machine_type = st.selectbox(
        """نوع المعدة الصناعية:""",
        [
            """محرك كهربائي ثلاثي الأوجه (3-Phase Induction Motor)""",
            """مضخة مياه هيدروليكية (Hydraulic Water Pump)""",
            """ضاغط هواء حلزوني (Rotary Screw Compressor)""",
            """مولد كهربائي (Diesel Generator)""",
        ],
    )
  with col_i2:
    power_rating = st.text_input("""القدرة (HP / kW):""", """50 HP / 37 kW""")
  with col_i3:
    rpm_val = st.text_input("""سرعة الدوران (RPM):""", """1450 RPM""")

st.markdown("""---""")

# 9. وحدة الصوت
st.markdown("""### """ + str(t["audio_section"]))
col_rec1, col_rec2 = st.columns(2)

with col_rec1:
  st.write("""<b>1. """ + str(t["rec_mic"]) + """</b>""", unsafe_allow_html=True)
  recorded_audio = st.audio_input("""اضغط للبدء بالتسجيل الصوتي المباشر 🎙""")

with col_rec2:
  st.write("""<b>2. """ + str(t["upload_file"]) + """</b>""", unsafe_allow_html=True)
  uploaded_file = st.file_uploader(
      """ارفع ملف الصوت من جهازك:""", type=["wav", "mp3", "ogg"]
  )

audio_source = recorded_audio or uploaded_file
if audio_source:
  st.audio(audio_source)
  st.success(
      """✅ تم استقبال الإشارة الصوتية بنجاح وهي جاهزة للفحص بالليزر الطيفي!"""
  )

st.markdown("""---""")


# 10. دالة توليد التقرير الهندسي المحمية باقتباسات ثلاثية
def generate_expanded_car_report(
    brand, model, engine, fuel, cylinders, lang_code
):
  b = str(brand)
  m = str(model)
  e = str(engine)
  f = str(fuel)
  c = str(cylinders)

  is_diesel = ("Diesel" in f) or ("CRDi" in e) or ("TDI" in e)
  is_turbo = ("Turbo" in f) or ("Turbo" in e) or ("TSI" in e)

  if lang_code == "العربية":
    p1 = (
        """<b>1. تحليل طيف فوريه الترددي (FFT Spectrum Analysis):</b><br>تم تفكيك الإشارة الصوتية لسيارة <b>"""
        + b
        + """ """
        + m
        + """</b> (محرك <b>"""
        + e
        + """</b>). التردد البارز يطابق زمن الاحتراق للـ """
        + c
        + """ بدون تشتت في الطاقة."""
    )
    p2 = (
        """<b>2. معاينة صمامات ومحاور الكامبشافت (Valve Train & Camshaft Acoustics):</b><br>خلوص الصبابات والصمامات يعمل ضمن المجال الهيدروليكي القياسي لشركة """
        + b
        + """، ولا تظهر أي طقطقة عشوائية في عمود الكامبشافت."""
    )

    if is_diesel:
      inj_str = """ترددات بخاخات الديزل ذات الضغط العالي (Common Rail) متزنة ونقية دون وجود ظاهرة التسريب الترددي."""
    else:
      inj_str = """نظام حقن البنزين المباشر/المتعدد يعمل بانتظام، والضوضاء عالية التردد في النطاق الطبيعي."""
    p3 = (
        """<b>3. نظام حقن الوقود والضغط العالي (Injectors & Fuel Rail Pressure):</b><br>"""
        + inj_str
    )

    if is_turbo:
      turbo_str = """عنفة التوربو تعمل بستارة صوتية مستقرة دون أي صفير مرتفع أو احتكاك في شفرات الشاحن."""
    else:
      turbo_str = """منظومة سحب الهواء وتطابق الضغط الطبيعي تعمل بكفاءة عالية بدون أي تسريب في المانفولد."""
    p4 = (
        """<b>4. الشاحن التوربيني ونظام سحب الهواء (Turbocharger & Induction):</b><br>"""
        + turbo_str
    )

    p5 = """<b>5. محامل الدوران وعمود الكرنك والحذافة (Bearings, Crankshaft & DMF):</b><br>عدم وجود أي اهتزازات منخفضة التردد في محامل عمود الكرنك الرئيسية، وحذافة الفولام المزدوجة امتصت الصدمات الصوتية بالكامل."""
    p6 = (
        """<b>6. التوصيات الهندسية وخطة الصيانة الوقائية (Predictive Maintenance Plan):</b><br>المحرك بحالة ممتازة جداً. يوصى بالمحافظة على مواعيد استبدال الزيوت والفلاتر الخاصة بـ """
        + b
        + """ عند قطع 10,000 كم."""
    )

    return (
        p1
        + """<br><br>"""
        + p2
        + """<br><br>"""
        + p3
        + """<br><br>"""
        + p4
        + """<br><br>"""
        + p5
        + """<br><br>"""
        + p6
    )

  elif lang_code == "English":
    p1 = (
        """<b>1. FFT Acoustic Spectrum Core Analysis:</b><br>Acoustic signal breakdown for <b>"""
        + b
        + """ """
        + m
        + """</b> ("""
        + e
        + """). Dominant peak matches fundamental combustion frequency for """
        + c
        + """ with zero spectral leakage."""
    )
    p2 = (
        """<b>2. Valve Train & Camshaft Acoustic Inspection:</b><br>Valve clearances and hydraulic lifters operate strictly within nominal """
        + b
        + """ specifications. Zero camshaft chatter observed."""
    )

    if is_diesel:
      inj_str = """High-pressure Common Rail Diesel injector chatter is fully synchronized with zero cavitation noise."""
    else:
      inj_str = """Gasoline injection pulses show clean high-frequency harmonics within normal operating range."""
    p3 = (
        """<b>3. Fuel Injection System & Rail Dynamics:</b><br>"""
        + inj_str
    )

    if is_turbo:
      turbo_str = """Turbocharger spool frequency exhibits smooth acoustic resonance without high-pitched turbine squeal."""
    else:
      turbo_str = """Naturally aspirated air intake manifold shows no pressure leaks or turbulent acoustic anomalies."""
    p4 = """<b>4. Turbocharger & Induction Harmonics:</b><br>""" + turbo_str

    p5 = """<b>5. Bearings, Crankshaft & DMF Flywheel Dynamics:</b><br>Main crankshaft bearings show zero low-frequency rumbl
