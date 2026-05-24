"""
analyzer.py – PDF text extraction, cover-image extraction, AI analysis
               with deep translation support, and dataset recommendations.
"""
import fitz  # PyMuPDF
import pandas as pd
import os, json, re, io

# ── Dataset paths ──────────────────────────────────────────────────────────────
BASE = os.path.dirname(__file__)
JAMALON_PATH = os.path.join(BASE, "Datasets", "jamalon dataset.csv")
BOOKS_PATH   = os.path.join(BASE, "Datasets", "books.csv")
BOOKS_DS     = os.path.join(BASE, "Datasets", "books_datasets.csv")


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PDF EXTRACTION                                                            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF bytes, limited to first 30 pages."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages = []
    for i, page in enumerate(doc):
        if i >= 30:
            break
        pages.append(page.get_text())
    doc.close()
    return "\n".join(pages)


def extract_cover_image(file_bytes: bytes) -> bytes:
    """
    Render the first page of the PDF as a high-quality PNG image.
    Returns raw PNG bytes suitable for st.image().
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    page = doc[0]
    # Render at 2x resolution for a crisp cover image
    pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
    png_bytes = pix.tobytes("png")
    doc.close()
    return png_bytes


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  AI ANALYSIS  (with deep translation)                                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def analyze_with_llm(text: str, filename: str, ui_lang: str = "ar") -> dict:
    """
    Call an LLM to analyze book text.
    ──────────────────────────────────────────────────────────────
    ui_lang: "ar" or "en" – controls the OUTPUT language.
             When "ar", the LLM is explicitly told to write every
             value in Arabic regardless of the source text language.
    ──────────────────────────────────────────────────────────────
    PLACEHOLDER: Replace the g4f calls below with your preferred
    API (OpenAI, Gemini, Claude, etc.).
    ──────────────────────────────────────────────────────────────
    """
    snippet = text[:4000].strip()

    # ── Dynamic language instruction ───────────────────────────────────────────
    if ui_lang == "ar":
        lang_instruction = (
            "CRITICAL: You MUST write ALL values in Arabic. "
            "Even if the book text is in English or any other language, "
            "translate the summary, main_idea, category, subcategory, "
            "age_range, themes, and mood into Arabic. "
            "Only the JSON keys must remain in English."
        )
        example_cat = "مثال: رواية، تاريخ، تطوير ذات، علوم، دين، فلسفة"
        example_age = "مثال: أطفال (٦-١٢)، يافعين (١٣-١٧)، بالغين (١٨+)، جميع الأعمار"
        example_mood = "مثال: ملهم، مظلم، فكاهي، رومانسي، تعليمي"
    else:
        lang_instruction = (
            "Write ALL values in English."
        )
        example_cat = "e.g. Fiction, History, Self-Help, Science, Religion, Philosophy"
        example_age = "e.g. Children (6-12), Young Adult (13-17), Adult (18+), All Ages"
        example_mood = "e.g. Inspiring, Dark, Humorous, Romantic, Educational"

    prompt = f"""You are an expert librarian and literary analyst.
Analyze the following book excerpt and respond in valid JSON only — no extra text.

{lang_instruction}

Book filename: {filename}
Excerpt:
\"\"\"
{snippet}
\"\"\"

Return exactly this JSON structure:
{{
  "language": "Arabic or English (the language of the original text)",
  "summary": "2-3 sentence summary of the book",
  "main_idea": "one sentence main idea",
  "category": "{example_cat}",
  "subcategory": "more specific genre",
  "age_range": "{example_age}",
  "themes": ["theme1", "theme2", "theme3"],
  "mood": "{example_mood}"
}}"""

    # ── g4f call (free, no API key) ────────────────────────────────────────────
    try:
        import g4f
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": prompt}],
        )
        match = re.search(r'\{.*\}', str(response), re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass

    # ── Fallback model ─────────────────────────────────────────────────────────
    try:
        import g4f
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=[{"role": "user", "content": prompt}],
        )
        match = re.search(r'\{.*\}', str(response), re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass

    # ── Hard fallback ──────────────────────────────────────────────────────────
    if ui_lang == "ar":
        return {
            "language": "غير معروف",
            "summary": "تعذّر إنشاء الملخص — يرجى المحاولة مرة أخرى.",
            "main_idea": "", "category": "غير معروف", "subcategory": "",
            "age_range": "غير معروف", "themes": [], "mood": ""
        }
    return {
        "language": "Unknown",
        "summary": "Could not generate summary – please try again.",
        "main_idea": "", "category": "Unknown", "subcategory": "",
        "age_range": "Unknown", "themes": [], "mood": ""
    }


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  DATASET RECOMMENDATIONS                                                   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def _load_csv(path, encoding="utf-8"):
    try:
        return pd.read_csv(path, encoding=encoding, on_bad_lines="skip")
    except Exception:
        return pd.DataFrame()


def find_similar_books(category: str, lang: str = "ar", n: int = 5) -> list[dict]:
    """Cross-reference AI-generated category with local datasets."""
    results = []
    if lang == "ar":
        df = _load_csv(JAMALON_PATH)
        if df.empty:
            df = _load_csv(BOOKS_DS)
        if df.empty:
            return []
        cat_col = "Category" if "Category" in df.columns else "Subcategory"
        if cat_col not in df.columns:
            # books_datasets.csv uses Arabic column names
            title_col = next((c for c in df.columns if "اسم الكتاب" in c), None)
            author_col = next((c for c in df.columns if "اسم المؤلف" in c), None)
            if title_col:
                sample = df.sample(min(n, len(df)), random_state=42)
                for _, row in sample.iterrows():
                    results.append({
                        "title": str(row.get(title_col, "")),
                        "author": str(row.get(author_col, "")),
                        "category": "",
                    })
                return results
        mask = df[cat_col].astype(str).str.contains(category, na=False, case=False)
        subset = df[mask] if mask.sum() > 0 else df
        sample = subset.sample(min(n, len(subset)), random_state=42)
        for _, row in sample.iterrows():
            results.append({
                "title": str(row.get("Title", "")),
                "author": str(row.get("Author", "")),
                "category": str(row.get("Category", "")),
            })
    else:
        df = _load_csv(BOOKS_PATH)
        if df.empty:
            return []
        sample = df.sample(min(n, len(df)), random_state=42)
        for _, row in sample.iterrows():
            results.append({
                "title": str(row.get("title", "")),
                "author": str(row.get("authors", "")),
                "rating": str(row.get("average_rating", "")),
            })
    return results
