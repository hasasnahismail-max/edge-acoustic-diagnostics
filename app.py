import streamlit as st

st.set_page_config(
    page_title="ZINO EADE Workstation", page_icon="🚗", layout="wide"
)

st.markdown("### 🚘 اختيار المركبة ونظام الفحص الهندسي")

car_option = st.selectbox(
    "اختر طراز المركبة الأساسي:",
    [
        "Mitsubishi Pajero V20 3.4L V6",
        "Hyundai Santa Fe 2.2 CRDI VGT",
        "Volkswagen Golf / Caddy 1.4 TSI",
        "أخرى (إدخال يدوي مخصص / Custom Input)",
    ],
)

if "أخرى" in car_option:
    custom_car_input = st.text_input(
        "اكتب اسم ورقم طراز المركبة يدوياً:",
        value="",
        placeholder="مثال: Mercedes W124 2.3L",
    )
    selected_car = (
        custom_car_input
        if custom_car_input
        else "مركبة مخصصة (Custom Vehicle)"
    )
else:
    selected_car = car_option

# تحديد الثيم اللوني حصرياً بناءً على العلامة التجارية (خمري، بيج، زيتي)
if "Mitsubishi" in car_option:
    theme_color = "#556B2F"  # زيتي (Olive Green)
    color_name = "الزيتي (Olive Green)"
elif "Hyundai" in car_option:
    theme_color = "#7A1C2E"  # خمري (Burgundy)
    color_name = "الخمري (Burgundy)"
elif "Volkswagen" in car_option:
    theme_color = "#A39171"  # بيج (Beige)
    color_name = "البيج (Beige)"
else:
    theme_color = "#7A1C2E"
    color_name = "الخمري"

st.markdown(
    f"""
    <style>
    .main-header {{
        font-size: 28px;
        font-weight: bold;
        color: {theme_color};
        border-bottom: 4px solid {theme_color};
        padding-bottom: 10px;
        margin-bottom: 20px;
    }}
    .engine-card {{
        background-color: #1e1e1e;
        border-left: 8px solid {theme_color};
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }}
    .engine-title {{
        font-size: 22px;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 8px;
    }}
    .engine-text {{
        font-size: 16px;
        color: #dddddd;
        line-height: 1.5;
    }}
    .stButton>button {{
        background-color: {theme_color};
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-header">⚙️ ZINO EADE - محطة التشخيص الهندسي المتقدم</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="engine-card">
    <div class="engine-title">🔍 بطاقة معلومات المحرك والتشخيص</div>
    <div class="engine-text">
        <b>المركبة الحالية:</b> {selected_car}<br>
        <b>الثيم اللوني النشط:</b> <span style="color: {theme_color}; font-weight: bold;">{color_name}</span><br>
        <b>نظام التحليل:</b> مطابقة ترددات الصوت العكسية وفحص أداء المحرك والاحتراق الداخلي.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("### 🎛️ خيارات الفحص والتحليل المتقدم")
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 بدء فحص الصوت والترددات"):
        st.success(f"جاري تحليل ترددات المحرك لـ ({selected_car})...")

with col2:
    if st.button("📊 تقرير سلامة قطع المحرك"):
        st.info(f"جاري مطابقة مصفوفات الفحص لـ ({selected_car})...")
