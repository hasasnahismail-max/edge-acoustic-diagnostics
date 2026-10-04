import streamlit as st

# إعداد الصفحة
st.set_page_config(
    page_title="ZINO EADE Workstation", page_icon="🚗", layout="wide"
)

# اختيار المركبة مع إمكانية التحديد والإدخال اليدوي
st.markdown("### 🚘 اختيار المركبة ونظام الفحص")
car_option = st.selectbox(
    "اختر طراز المركبة الأساسي:",
    [
        "Mitsubishi Pajero V20 3.4L V6",
        "Hyundai Santa Fe 2.2 CRDI VGT",
        "Volkswagen Golf / Caddy 1.4 TSI",
        "أخرى (إدخال يدوي مخصص / Custom Input)",
    ],
)

# خانة إضافية للكتابة اليدوية إذا اخترت الإدخال المخصص
if "أخرى" in car_option:
    custom_car_input = st.text_input(
        "اكتب اسم ورقم طراز المركبة يدوياً:",
        value="",
        placeholder="مثال: Mercedes W124 2.3L",
    )
    selected_brand_name = (
        custom_car_input
        if custom_car_input
        else "مركبة مخصصة (Custom Vehicle)"
    )
else:
    selected_brand_name = car_option

# تحديد الثيم اللوني حصرياً بناءً على العلامة التجارية (خمري، بيج، زيتي)
if "Mitsubishi" in car_option:
    theme_color = "#556B2F"  # زيتي (Olive Green)
    color_name = "زيتي"
elif "Hyundai" in car_option:
    theme_color = "#7A1C2E"  # خمري (Burgundy)
    color_name = "خمري"
elif "Volkswagen" in car_option:
    theme_color = "#A39171"  # بيج (Beige / Khaki)
    color_name = "بيج"
else:
    theme_color = "#7A1C2E"  # افتراضي خمري للطرازات المخصصة
    color_name = "خمري مخصص"

# حقن أكواد CSS لتصميم الواجهة وتطبيق الألوان الكبيرة والديناميكية
st.markdown(
    f"""
    <style>
    .main-title {{
        font-size: 28px;
        font-weight: bold;
        color: {theme_color};
        border-bottom: 4px solid {theme_color};
        padding-bottom: 12px;
        margin-bottom: 20px;
    }}
    .engine-box {{
        background-color: #1a1a1a;
        border-left: 8px solid {theme_color};
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }}
    .engine-title {{
        font-size: 22px;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 10px;
    }}
    .engine-details {{
        font-size: 16px;
        color: #cccccc;
        line-height: 1.6;
    }}
    .badge {{
        background-color: {theme_color};
        color: white;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# عنوان النظام الرئيسي
st.markdown(
    '<div class="main-title">⚙️ ZINO EADE - محطة التشخيص الهندسي المتقدمة</div>',
    unsafe_allow_html=True,
)

# قسم معلومات المحرك المخصص والبارز بأيقونة كبيرة
st.markdown(
    f"""
<div class="engine-box">
    <div class="engine-title">🔍 بطاقة معلومات المحرك والتشخيص المتقدم</div>
    <div class="engine-details">
        <b>المركبة المحددة:</b> {selected_brand_name}<br>
        <b>نظام التحليل:</b> مطابقة ترددات الأكستيك الصوتي (STFT) وفحص الاحتراق الداخلي.<br>
        <b>الثيم اللوني النشط:</b> <span style="color: {theme_color}; font-weight: bold;">{color_name}</span>
    </div>
    <div class="badge">النظام جاهز للفحص الهندسي</div>
</div>
""",
    unsafe_allow_html=True,
)

# أزرار التشخيص المتقدمة بأسلوب واضح وكبير
st.markdown("### 🎛️ لوحة التحكم التنفيذية للتشخيص")
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 تشخيص الصوت العميق والترددات"):
        st.success(
            f"جاري فحص الاهتزازات الصوتية لطراز ({selected_brand_name})..."
        )

with col2:
    if st.button("📊 تقرير سلامة قطع المحرك"):
        st.info(
            f"جاري مطابقة المصفوفات الحسابية لأجزاء المحرك الخاصة بـ ({selected_brand_name})..."
        )
