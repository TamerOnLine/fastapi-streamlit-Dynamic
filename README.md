# 🧾 fastapi-streamlit-resume

An interactive **Resume Builder** built with **Streamlit** (frontend) and **FastAPI** (backend).  
Generates professional two-column PDF files with profile photo, icons, dynamic sections, and full Arabic (RTL) text support.

---

## ✨ Features

- ⚡ **FastAPI**: High-performance backend API for PDF generation.  
- 🎨 **Streamlit**: Simple, intuitive frontend interface for filling out resume data.  
- 🖼️ **ReportLab**: High-quality PDF rendering with flexible layout.  
- 🌍 **Multilingual support**: Arabic, German, English.  
- 🛠️ Dynamic sections: Projects, Skills, Languages, Education, and extra sections.  
- 📷 Optional profile photo with automatic circular cropping.  

---

## 📦 Requirements

- Python 3.10+  
- Install dependencies from `requirements.txt`:  

```bash
pip install -r requirements.txt
```

---

## 🚀 Run

### 1. Start Backend (FastAPI)
```bash
uvicorn api.main:app --reload
```
- Interactive API docs available at:  
  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Start Frontend (Streamlit)
```bash
streamlit run frontend/app.py
```
- UI available at:  
  [http://localhost:8501](http://localhost:8501)

---

## 📝 Usage

1. Open the Streamlit UI and fill in your details (name, phone, GitHub, LinkedIn, skills, projects …).  
2. Optionally upload a profile photo.  
3. Click **Generate PDF** to instantly create your resume.  

---

## 📂 Project Structure

```
.
├── api/                # FastAPI backend code
│   ├── main.py         # API entry point
│   ├── pdf_utils/      # PDF generation utilities (icons, fonts, layout)
│   └── routes/         # API routes
├── frontend/           # Streamlit UI code
├── outputs/            # Generated PDF files
├── profiles/           # Saved user profiles
├── requirements.txt    # Dependencies
├── LICENSE             # MIT License
└── README.md           # This file
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
