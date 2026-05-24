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
        "page_title": "Smart Book Reader",
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
st.set_page_config(page_title="Smart Book Reader", page_icon="📚", layout="wide")

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
    html, body, [data-testid="stAppViewContainer"], .stMarkdown,
    .stTextInput, .stSelectbox, p, h1, h2, h3, h4, span, div, label {
        direction: rtl !important; text-align: right !important;
    }
    [data-testid="stSidebar"] * { direction: rtl !important; text-align: right !important; }
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
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stToolbar"] {{ display: none; }}
{rtl_css}

/* ── HERO ───────────────────────────────────────────── */
.hero {{ text-align: center !important; padding: 40px 20px 20px; direction: ltr !important; }}
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
    line-height: 1.2; margin-bottom: 12px;
}}
.hero p {{ color: {sub_c}; font-size: 1rem; max-width: 560px; margin: 0 auto; line-height: 1.7; }}

/* ── GLASS CARD ─────────────────────────────────────── */
.glass-card {{
    background: {card_bg}; border: 1px solid {card_border};
    border-radius: 20px; padding: 28px; backdrop-filter: blur(16px);
    box-shadow: 0 4px 30px rgba(0,0,0,0.1); margin-bottom: 20px;
    transition: box-shadow .3s, transform .2s;
}}
.glass-card:hover {{ box-shadow: 0 8px 40px {accent}22; transform: translateY(-2px); }}

/* ── COVER IMAGE ────────────────────────────────────── */
.cover-wrap {{
    background: {card_bg}; border: 1px solid {card_border};
    border-radius: 20px; padding: 16px; text-align: center;
    box-shadow: 0 8px 40px rgba(0,0,0,0.15);
}}
.cover-wrap img {{
    border-radius: 12px; max-height: 720px; width: auto;
    box-shadow: 0 12px 48px rgba(0,0,0,0.3);
}}

/* ── INFO GRID ─────────────────────────────────────── */
.info-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px,1fr)); gap: 14px; margin-bottom: 20px; }}
.info-card {{
    background: {card_bg}; border: 1px solid {card_border};
    border-radius: 14px; padding: 18px 14px; text-align: center;
    transition: transform .2s, box-shadow .2s;
}}
.info-card:hover {{ transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.12); }}
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
    border-radius: 14px; padding: 18px; transition: all .2s;
}}
.rec-card:hover {{ border-color: {accent}55; transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.12); }}
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

/* ── BUTTONS & UPLOADER ───────────────────────────── */
.stButton > button {{
    width: 100%;
    background: linear-gradient(135deg, {accent}, #4f46e5);
    color: #fff; border: none; border-radius: 14px;
    padding: 14px 28px; font-size: 1rem; font-weight: 700;
    cursor: pointer; transition: all .3s;
    box-shadow: 0 4px 20px {accent}44;
}}
.stButton > button:hover {{ transform: translateY(-2px); box-shadow: 0 8px 30px {accent}66; }}
[data-testid="stFileUploader"] {{
    background: {card_bg}; border: 2px dashed {accent}55;
    border-radius: 14px; padding: 16px; transition: border-color .3s;
}}
[data-testid="stFileUploader"]:hover {{ border-color: {accent}; }}
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
