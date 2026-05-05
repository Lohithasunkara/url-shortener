# 🔗 Scalable URL Shortener 

A powerful URL Shortener built with Python & Flask.

---

## ✨ Features

- ✅ Shorten any long URL
- ✅ Custom short codes (e.g. `/my-link`)
- ✅ Click tracking & analytics
- ✅ Full click history with timestamps
- ✅ SQLite database (no setup needed)

---

## 📁 Project Structure

```
url-shortener/
├── app.py           # Main Flask application
├── database.py      # Database handler (SQLite)
├── shortener.py     # Short code generator
├── requirements.txt # Dependencies
└── README.md        # This file
```

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
python app.py
```

### 3. Open in browser
```
http://localhost:5000
```

---

## 📡 API Endpoints

### ➡️ Shorten a URL
```
POST /shorten
```
**Body (JSON):**
```json
{
  "url": "https://www.google.com"
}
```
**Response:**
```json
{
  "short_url": "http://localhost:5000/aB3xYz",
  "short_code": "aB3xYz",
  "original_url": "https://www.google.com"
}
```

---

### ➡️ Shorten with Custom Code
```
POST /shorten
```
**Body (JSON):**
```json
{
  "url": "https://www.google.com",
  "custom_code": "google"
}
```
**Short URL:** `http://localhost:5000/google`

---

### ➡️ Redirect
```
GET /<short_code>
```
Automatically redirects to the original URL.

---

### ➡️ Analytics / Stats
```
GET /stats/<short_code>
```
**Response:**
```json
{
  "short_code": "aB3xYz",
  "original_url": "https://www.google.com",
  "total_clicks": 5,
  "created_at": "2026-05-05 10:00:00",
  "click_history": ["2026-05-05 10:05:00", "2026-05-05 10:06:00"]
}
```

---

### ➡️ List All URLs
```
GET /all
```

---

## 🛠️ Tech Stack

| Tech     | Purpose              |
|----------|----------------------|
| Python   | Core language        |
| Flask    | Web framework        |
| SQLite   | Database             |

---

## 👨‍💻 Author
Built using Python & Flask
