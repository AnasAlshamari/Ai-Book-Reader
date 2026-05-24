"""
app.py – Smart Book Reader: Bilingual (AR/EN) Streamlit app with
cover image extraction, AI insights with deep translation, dark/light theme,
and RTL support.
"""
import streamlit as st
import time
from analyzer import extract_text_from_pdf, extract_cover_image, analyze_with_llm, find_similar_books

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TRANSLATIONS                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
T = {
    "ar": {
        "page_title": "قارئ الكتب الذكي",
        "badge": "✨ مدعوم بالذكاء الاصطناعي",
        "hero_title": "قارئ الكتب الذكي",
        "hero_sub": "ارفع كتابك بصيغة PDF واحصل على تحليل فوري، ملخص ذكي، تصنيف عمري، وتوصيات — في ثوانٍ.",
        "upload_label": "اختر ملف PDF",
        "analyze_btn": "🔍 تحليل الكتاب",
        "no_file_warn": "⚠️ يرجى رفع ملف أولاً!",
        "no_text_err": "⚠️ لم يتم استخراج نص. تأكد أن الملف ليس صوراً فقط.",
        "prog_extract": "📖 جارٍ استخراج النص…",
        "prog_cover": "🖼️ جارٍ استخراج الغلاف…",
        "prog_ai": "🧠 جارٍ التحليل بالذكاء الاصطناعي…",
        "prog_render": "🎨 جارٍ عرض النتائج…",
        "prog_done": "✅ تم!",
        "summary_title": "📝 الملخص",
        "main_idea": "الفكرة الرئيسية",
        "info_title": "📊 معلومات الكتاب",
        "lbl_lang": "اللغة", "lbl_cat": "التصنيف", "lbl_sub": "النوع الفرعي",
        "lbl_age": "الفئة العمرية", "lbl_mood": "المزاج",
        "themes_title": "🎯 المواضيع الرئيسية",
        "rec_title": "📚 كتب مشابهة قد تعجبك",
        "no_recs": "لا توجد توصيات في مجموعة البيانات.",
        "cover_title": "📖 غلاف الكتاب",
        "insights_title": "🧠 التحليل الذكي",
        "sidebar_lang": "🌐 اللغة",
        "sidebar_theme": "🌓 الوضع الداكن",
    },
    "en": {
        "page_title": "قارئ الكتب الذكي",
        "badge": "✨ Powered by AI",
        "hero_title": "Smart Book Reader",
        "hero_sub": "Upload a PDF book and get an instant AI-powered summary, genre analysis, age recommendation, and more.",
        "upload_label": "Choose a PDF file",
        "analyze_btn": "🔍 Analyze Book",
        "no_file_warn": "⚠️ Please upload a file first!",
        "no_text_err": "⚠️ Could not extract text. Make sure the file is not image-only.",
        "prog_extract": "📖 Extracting text…",
        "prog_cover": "🖼️ Extracting cover…",
        "prog_ai": "🧠 Sending to AI…",
        "prog_render": "🎨 Rendering results…",
        "prog_done": "✅ Done!",
        "summary_title": "📝 Summary",
        "main_idea": "Main Idea",
        "info_title": "📊 Book Info",
        "lbl_lang": "Language", "lbl_cat": "Category", "lbl_sub": "Sub-genre",
        "lbl_age": "Age Range", "lbl_mood": "Mood",
        "themes_title": "🎯 Key Themes",
        "rec_title": "📚 Similar Books You Might Like",
        "no_recs": "No recommendations found in datasets.",
        "cover_title": "📖 Book Cover",
        "insights_title": "🧠 AI Insights",
        "sidebar_lang": "🌐 Language",
        "sidebar_theme": "🌓 Dark Mode",
    },
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PAGE CONFIG & SESSION STATE                                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
st.set_page_config(page_title="Smart Book Reader", page_icon="📚", layout="wide", initial_sidebar_state="expanded")

if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "dark" not in st.session_state:
    st.session_state.dark = True

# ── Sidebar controls ──────────────────────────────────────────────────────────
with st.sidebar:
    lang_choice = st.selectbox(
        T[st.session_state.lang]["sidebar_lang"],
        ["العربية", "English"],
        index=0 if st.session_state.lang == "ar" else 1,
        key="lang_select",
    )
    st.session_state.lang = "ar" if lang_choice == "العربية" else "en"

    dark_on = st.toggle(
        T[st.session_state.lang]["sidebar_theme"],
        value=st.session_state.dark,
        key="dark_toggle",
    )
    st.session_state.dark = dark_on

lang = st.session_state.lang
dark = st.session_state.dark
t = T[lang]

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  CSS – Theme + RTL injection                                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
if dark:
    bg = "#0a0a0f"
    bg_grad = "radial-gradient(ellipse at 20% 0%,#1a0533 0%,#0a0a0f 50%),radial-gradient(ellipse at 80% 100%,#001a33 0%,transparent 60%)"
    text_c = "#e2e8f0"; sub_c = "#94a3b8"
    card_bg = "rgba(255,255,255,0.03)"; card_border = "rgba(255,255,255,0.08)"
    accent = "#7c3aed"; accent2 = "#38bdf8"
    summary_bg = "linear-gradient(135deg,#1e1b4b88,#0f172a88)"
else:
    bg = "#f8f9fc"
    bg_grad = "linear-gradient(135deg,#f8f9fc,#eef1f8)"
    text_c = "#1e293b"; sub_c = "#64748b"
    card_bg = "rgba(255,255,255,0.85)"; card_border = "rgba(0,0,0,0.08)"
    accent = "#6d28d9"; accent2 = "#0284c7"
    summary_bg = "linear-gradient(135deg,#ede9fe88,#e0f2fe88)"

rtl_css = ""
if lang == "ar":
    rtl_css = """
    /* RTL – scoped to content area to avoid sidebar animation glitches */
    [data-testid="stAppViewContainer"] .block-container,
    [data-testid="stAppViewContainer"] .stMarkdown,
    [data-testid="stAppViewContainer"] .stTextInput,
    [data-testid="stAppViewContainer"] .stSelectbox,
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4,
    [data-testid="stAppViewContainer"] label {
        direction: rtl !important; text-align: right !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdown"],
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox {
        direction: rtl !important; text-align: right !important;
    }
    """

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800&family=Tajawal:wght@400;500;700;800&display=swap');
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body, [data-testid="stAppViewContainer"] {{
    background: {bg};
    font-family: {("'Tajawal'," if lang=="ar" else "")} 'Inter', sans-serif;
    color: {text_c};
}}
[data-testid="stAppViewContainer"] {{ background: {bg_grad}; min-height: 100vh; }}
#MainMenu, footer {{ visibility: hidden; }}
/* Sidebar – always visible and accessible */
[data-testid="stSidebar"] {{
    visibility: visible !important;
    display: flex !important;
    background: {bg} !important;
}}
[data-testid="stSidebarCollapsedControl"] {{
    visibility: visible !important;
    display: flex !important;
}}
{rtl_css}

/* ── LAYOUT – remove default Streamlit top padding ──── */
.block-container {{ padding-top: 1rem !important; }}
[data-testid="stAppViewContainer"] > .main {{ padding-top: 0 !important; }}


/* ── HERO ───────────────────────────────────────────── */
.hero {{ 
    text-align: center !important; 
    padding: 48px 20px 24px; 
    direction: rtl !important;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}
.hero * {{ text-align: center !important; direction: rtl !important; }}
.hero-badge {{
    display: inline-block;
    background: linear-gradient(135deg,{accent}22,{accent2}22);
    border: 1px solid {accent}55; border-radius: 999px; padding: 6px 18px;
    font-size: 12px; font-weight: 600; letter-spacing: 2px;
    text-transform: uppercase; color: {accent}; margin-bottom: 16px;
}}
.hero h1 {{
    font-family: 'Playfair Display', 'Tajawal', serif;
    font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 800;
    background: linear-gradient(135deg, {text_c} 0%, {accent} 50%, {accent2} 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2; margin-bottom: 16px;
}}
.hero p {{
    color: #94a3b8; font-size: 1.05rem; max-width: 650px;
    margin: 0 auto; line-height: 1.8; letter-spacing: 0.01em;
}}

/* ── GLASS CARD – premium micro-interactions ───────── */
.glass-card {{
    background: {card_bg}; border: 1px solid {card_border};
    border-radius: 20px; padding: 28px; backdrop-filter: blur(16px);
    box-shadow: 0 4px 30px rgba(0,0,0,0.1); margin-bottom: 20px;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
}}
.glass-card:hover {{
    box-shadow: 0 12px 48px {accent}28;
    transform: translateY(-3px);
    border-color: {accent}33;
}}

/* ── COVER IMAGE – refined border & glow ───────────── */
.cover-wrap {{
    background: {card_bg}; border: 1px solid {card_border};
    border-radius: 20px; padding: 16px; text-align: center;
    box-shadow: 0 8px 40px rgba(0,0,0,0.15);
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
}}
.cover-wrap:hover {{
    box-shadow: 0 16px 56px rgba(0,0,0,0.25);
    transform: translateY(-2px);
}}
.cover-wrap img {{
    border-radius: 16px; max-height: 720px; width: auto;
    box-shadow: 0 12px 48px rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.06);
}}

/* ── INFO GRID ─────────────────────────────────────── */
.info-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px,1fr)); gap: 14px; margin-bottom: 20px; }}
.info-card {{
    background: {card_bg}; border: 1px solid {card_border};
    border-radius: 14px; padding: 18px 14px; text-align: center;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
}}
.info-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 8px 28px rgba(0,0,0,0.15);
    border-color: {accent}33;
}}
.info-icon {{ font-size: 1.8rem; margin-bottom: 6px; }}
.info-label {{ font-size: .7rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: {sub_c}; margin-bottom: 4px; }}
.info-value {{ font-size: .95rem; font-weight: 700; color: {text_c}; }}

/* ── THEME CHIPS ───────────────────────────────────── */
.theme-chip {{
    display: inline-block;
    background: linear-gradient(135deg,{accent}22,{accent2}22);
    border: 1px solid {accent}44; border-radius: 999px; padding: 5px 14px;
    font-size: .82rem; font-weight: 600; color: {accent}; margin: 3px;
}}

/* ── REC CARDS ─────────────────────────────────────── */
.rec-card {{
    background: {card_bg}; border: 1px solid {card_border};
    border-radius: 14px; padding: 18px;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
}}
.rec-card:hover {{
    border-color: {accent}55;
    transform: translateY(-4px);
    box-shadow: 0 8px 28px rgba(0,0,0,0.15);
}}
.rec-title {{ font-size: .9rem; font-weight: 700; color: {text_c}; margin-bottom: 4px; }}
.rec-author {{ font-size: .8rem; color: {sub_c}; }}
.rec-cat {{ font-size: .72rem; color: {accent}; font-weight: 600; margin-top: 6px; }}

/* ── SECTION TITLE ─────────────────────────────────── */
.sec-title {{
    font-size: 1.2rem; font-weight: 700; color: {text_c};
    margin-bottom: 14px; display: flex; align-items: center; gap: 8px;
}}
.sec-title::after {{ content: ''; flex: 1; height: 1px; background: linear-gradient(90deg,{accent}44,transparent); }}

.summary-card {{
    background: {summary_bg}; border: 1px solid {accent}33;
    border-radius: 18px; padding: 26px; margin-bottom: 20px;
    backdrop-filter: blur(10px);
}}
.summary-text {{ font-size: 1rem; line-height: 1.8; color: {sub_c}; }}

/* ── BUTTONS – smooth premium hover ────────────────── */
.stButton > button {{
    width: 100%;
    background: linear-gradient(135deg, {accent}, #4f46e5);
    color: #fff; border: none; border-radius: 14px;
    padding: 14px 28px; font-size: 1rem; font-weight: 700;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    box-shadow: 0 4px 20px {accent}44;
}}
.stButton > button:hover {{
    transform: translateY(-3px);
    box-shadow: 0 12px 36px {accent}66;
    filter: brightness(1.08);
}}
.stButton > button:active {{
    transform: translateY(0px);
    box-shadow: 0 2px 12px {accent}44;
}}

/* ── FILE UPLOADER – glassmorphic redesign ─────────── */
[data-testid="stFileUploader"] {{
    background: rgba(255, 255, 255, 0.02);
    border: 2px dashed {accent}44;
    border-radius: 16px; padding: 20px;
    backdrop-filter: blur(12px);
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
}}
[data-testid="stFileUploader"]:hover {{
    border-color: {accent}99;
    background: rgba(255, 255, 255, 0.04);
    box-shadow: 0 4px 24px {accent}18;
}}

/* ── PROGRESS BAR ──────────────────────────────────── */
.stProgress > div > div > div {{ background: linear-gradient(90deg,{accent},{accent2}) !important; }}
</style>
""", unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  CACHED FUNCTIONS – survive theme/language toggles                         ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
@st.cache_data(show_spinner=False)
def cached_extract(file_bytes: bytes) -> str:
    return extract_text_from_pdf(file_bytes)

@st.cache_data(show_spinner=False)
def cached_cover(file_bytes: bytes) -> bytes:
    return extract_cover_image(file_bytes)

@st.cache_data(show_spinner=False)
def cached_analyze(text: str, filename: str, ui_lang: str) -> dict:
    return analyze_with_llm(text, filename, ui_lang)

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  HERO                                                                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
st.markdown(f"""
<div class="hero">
  <div class="hero-badge">{t['badge']}</div>
  <h1>{t['hero_title']}</h1>
  <p>{t['hero_sub']}</p>
</div>
""", unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  UPLOAD                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
uploaded = st.file_uploader(t["upload_label"], type=["pdf"], label_visibility="visible")
analyze_btn = st.button(t["analyze_btn"], use_container_width=True)

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  MAIN LOGIC                                                                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
if analyze_btn and uploaded:
    file_bytes = uploaded.read()

    # ── Progress ───────────────────────────────────────────────────────────────
    prog = st.progress(0, text=t["prog_extract"])
    text = cached_extract(file_bytes)
    prog.progress(15, text=t["prog_cover"])
    cover_png = cached_cover(file_bytes)
    time.sleep(0.2)
    prog.progress(30, text=t["prog_ai"])

    if not text.strip():
        st.error(t["no_text_err"])
        st.stop()

    result = cached_analyze(text, uploaded.name, lang)
    prog.progress(85, text=t["prog_render"])
    time.sleep(0.3)
    prog.progress(100, text=t["prog_done"])
    time.sleep(0.4)
    prog.empty()

    detected_lang = "ar" if result.get("language", "").lower() in ("arabic", "عربي", "العربية") else "en"

    # ╔══════════════════════════════════════════════════════════════════════════╗
    # ║  SIDE-BY-SIDE LAYOUT: Cover Image | AI Insights                        ║
    # ╚══════════════════════════════════════════════════════════════════════════╝
    col_cover, col_insights = st.columns([2, 3], gap="large")

    # ── LEFT: Book Cover ───────────────────────────────────────────────────────
    with col_cover:
        st.markdown(f'<div class="sec-title">{t["cover_title"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="cover-wrap">', unsafe_allow_html=True)
        st.image(cover_png, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT: AI Insights ─────────────────────────────────────────────────────
    with col_insights:
        st.markdown(f'<div class="sec-title">{t["insights_title"]}</div>', unsafe_allow_html=True)

        # Summary card
        st.markdown(f'<div class="sec-title" style="font-size:1rem;">{t["summary_title"]}</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="summary-card">
          <div class="summary-text">{result.get('summary', 'N/A')}</div>
          <div style="font-size:.85rem;color:{sub_c};border-top:1px solid {card_border};padding-top:12px;margin-top:10px;">
            <strong style="color:{accent};">{t['main_idea']}:</strong> {result.get('main_idea', 'N/A')}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Info grid
        st.markdown(f'<div class="sec-title" style="font-size:1rem;">{t["info_title"]}</div>', unsafe_allow_html=True)
        cards = [
            ("🌍", t["lbl_lang"],  result.get("language", "—")),
            ("📂", t["lbl_cat"],   result.get("category", "—")),
            ("🏷️", t["lbl_sub"],   result.get("subcategory", "—")),
            ("👤", t["lbl_age"],   result.get("age_range", "—")),
            ("🎭", t["lbl_mood"],  result.get("mood", "—")),
        ]
        grid_html = '<div class="info-grid">'
        for icon, label, value in cards:
            grid_html += f"""
            <div class="info-card">
              <div class="info-icon">{icon}</div>
              <div class="info-label">{label}</div>
              <div class="info-value">{value}</div>
            </div>"""
        grid_html += "</div>"
        st.markdown(grid_html, unsafe_allow_html=True)

        # Themes
        themes = result.get("themes", [])
        if themes:
            st.markdown(f'<div class="sec-title" style="font-size:1rem;">{t["themes_title"]}</div>', unsafe_allow_html=True)
            chips = "".join(f'<span class="theme-chip">{th}</span>' for th in themes)
            st.markdown(f'<div style="margin-bottom:16px;">{chips}</div>', unsafe_allow_html=True)

        # Recommendations
        st.markdown(f'<div class="sec-title" style="font-size:1rem;">{t["rec_title"]}</div>', unsafe_allow_html=True)
        recs = find_similar_books(result.get("category", ""), detected_lang)
        if recs:
            for r in recs:
                st.markdown(f"""
                <div class="rec-card" style="margin-bottom:10px;">
                  <div class="rec-title">{str(r.get('title',''))[:60]}</div>
                  <div class="rec-author">{str(r.get('author',''))[:45]}</div>
                  <div class="rec-cat">{r.get('category', r.get('rating',''))}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(t["no_recs"])

elif analyze_btn and not uploaded:
    st.warning(t["no_file_warn"])

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  FOOTER                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; padding: 12px; background: rgba(10, 10, 15, 0.8); backdrop-filter: blur(8px); border-top: 1px solid rgba(255,255,255,0.05); z-index: 1000; font-size: 0.85rem;">
    <a href="https://www.linkedin.com/in/anas-alshammari-795013369" target="_blank" style="color: #94a3b8; text-decoration: none; font-weight: 500; transition: color 0.3s;">
        © Anas Alshammari 2026
    </a>
</div>
""", unsafe_allow_html=True)
