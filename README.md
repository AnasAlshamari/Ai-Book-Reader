

<h1 align="center">📚 Smart Book Reader | قارئ الكتب الذكي</h1>

<p align="center">
  <strong>AI-Powered Book Analysis — Upload a PDF and get instant insights</strong><br>
  <strong>تحليل ذكي للكتب — ارفع كتابك بصيغة PDF واحصل على تحليل فوري</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/AI-GPT--4-412991?style=for-the-badge&logo=openai&logoColor=white" alt="AI" />
  <img src="https://img.shields.io/badge/Bilingual-AR%20%7C%20EN-2ea44f?style=for-the-badge" alt="Bilingual" />
</p>

<p align="center">
  <b>🌐 <a href="https://ai-book-reader.streamlit.app/">Live Demo | تجربة حية</a></b>
</p>

<p align="center">
  <a href="#-features">Features | الميزات</a> •
  <a href="#-demo">Demo | العرض</a> •
  <a href="#-quick-start">Quick Start | البدء السريع</a> •
  <a href="#-project-structure">Structure | الهيكل</a> •
  <a href="#-tech-stack">Tech Stack | التقنيات</a>
</p>

---

## ✨ Features | الميزات

| Feature | Description | الوصف |
|---------|-------------|-------|
| 📄 **PDF Upload** | Extract text from the first 30 pages of any PDF book | استخراج النص من أول 30 صفحة من أي كتاب بصيغة PDF |
| 🖼️ **Cover Extraction** | Automatically renders the first page as a high-quality cover | استخراج صفحة الغلاف تلقائياً كصورة عالية الجودة |
| 🧠 **AI Analysis** | Get summary, main idea, genre, mood, themes, and age range | احصل على ملخص، الفكرة الرئيسية، التصنيف، المزاج، والمواضيع |
| 🌍 **Bilingual Support** | Full Arabic (RTL) & English UI — AI adapts accordingly | واجهة عربية وإنجليزية كاملة، والذكاء الاصطناعي يتكيف معها |
| 📚 **Recommendations** | Matches AI genre with datasets to suggest similar reads | يطابق تصنيف الكتاب مع بيانات محلية لاقتراح كتب مشابهة |
| 🌓 **Themes** | Toggle between premium dark and light modes | التبديل بين الوضعين الداكن والفاتح بتصميم عصري |

---

## 🎬 Demo | العرض السريع

<p align="center">
  <em>Upload any PDF → get AI insights in seconds</em><br>
  <em>ارفع أي كتاب → احصل على رؤى ذكية في ثوانٍ</em>
</p>

```
1. Choose a PDF file | اختر ملف الكتاب
2. Click "🔍 Analyze Book" | اضغط "تحليل الكتاب"
3. View insights & recommendations | تصفح التحليل والتوصيات
```

**Try it yourself:** [https://ai-book-reader.streamlit.app/](https://ai-book-reader.streamlit.app/)

---

## 🚀 Quick Start | البدء السريع

### Prerequisites | المتطلبات

- **Python 3.10+**

### Installation | التثبيت

```bash
# 1. Clone the repository | استنساخ المستودع
git clone https://github.com/<your-username>/Smart-Book-Reader.git
cd Smart-Book-Reader

# 2. Create a virtual environment | إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies | تثبيت الحزم
pip install -r requirements.txt

# 4. Run the app | تشغيل التطبيق
streamlit run app.py
```

The app will open at **http://localhost:8501** 🎉

---

## 📁 Project Structure | هيكل المشروع

```
Smart-Book-Reader/
├── app.py                # Main Streamlit application (UI, themes, layout)
├── analyzer.py           # PDF extraction, AI analysis, dataset recommendations
├── requirements.txt      # Python dependencies
├── assets/
│   └── banner.png        # README banner image
├── Datasets/             # Local CSV datasets for recommendations
│   ├── jamalon dataset.csv
│   ├── books.csv
│   └── books_datasets.csv
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack | التقنيات المستخدمة

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit + Custom CSS (glassmorphism, RTL) |
| **PDF Engine** | PyMuPDF (fitz) |
| **AI Backend** | g4f (GPT-4 / GPT-3.5 fallback, free API) |
| **Data** | Pandas + local CSV datasets |
| **Fonts** | Google Fonts (Inter, Playfair Display, Tajawal) |

---

<p align="center">
  Made by <a href="https://www.linkedin.com/in/anas-alshammari-795013369">Anas Alshammari</a>
</p>
