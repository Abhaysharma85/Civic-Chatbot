# Civic Chatbot

A chatbot project built with **Flask**, designed for deployment on **Vercel’s Python serverless environment**.

## 🚀 Features

- **Flask-based** Python API and chatbot logic.
- **Serverless deployment ready** — ideal for quick prototyping and cloud hosting.
- **FAQ-style interaction** (note: modifications persist only via external DBs/services in Vercel due to its ephemeral filesystem).
- **One-command deploy** to Vercel.

---

## 📦 Getting Started

### Prerequisites

- Python **3.x** and pip installed locally.
- A **Vercel** account and **Vercel CLI** installed.
- *(Optional)* Local Flask development setup.

---

### 🔧 Installation

1. **Clone the Repository**
```bash
git clone https://github.com/Abhaysharma85/Civic-Chatbot.git
cd Civic-Chatbot
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run Locally (Optional)**
```bash
python app.py
```
Your Flask app should be running at:
```
http://localhost:5000/
```

---

## ☁ Deployment to Vercel

1. **Login to Vercel**
```bash
vercel login
```

2. **Deploy**
```bash
vercel
```
The `vercel.json` file ensures all web requests are routed to `app.py` for your Flask endpoints.

---

## ⚠ Important Notes

- **Flask sessions & secret keys:** Store securely via **environment variables** in production.
- **Persistence:** File writes (e.g., updating `faqs.json`) won’t persist across serverless calls — use a **database** for production.
- **Vercel Limitations:**  
  - No long-lived processes  
  - Limited support for some Flask features (e.g., file uploads)  
  - For complex needs, consider a traditional server deployment.
- **Dependencies:** Ensure all Python packages are listed in `requirements.txt`.

---

## 📂 Project Structure
```
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
└── vercel.json         # Vercel configuration
```

---

## 🛠 Troubleshooting

- Missing module errors → Check `requirements.txt`.
- Persistent storage issues → Use external DB (e.g., MongoDB, Firebase, PostgreSQL).
- Vercel-specific issues → Check [Vercel Python Documentation](https://vercel.com/docs).

---

## 📜 License

MIT License — feel free to use, modify, and distribute.

---

> 💡 Tip: As your project evolves, keep updating this README with technical details, API docs, and usage examples.
