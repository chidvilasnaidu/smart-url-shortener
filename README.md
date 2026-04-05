# ✂️ Snip — URL Shortener

> A clean, full-stack URL shortener built with **Flask**, **SQLAlchemy**, and **SQLite** — turn long, ugly links into short, shareable ones in under a second.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=flat-square&logo=flask)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?style=flat-square)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue?style=flat-square&logo=sqlite)
![Bootstrap Icons](https://img.shields.io/badge/Icons-Bootstrap-purple?style=flat-square&logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📌 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [How It Works](#how-it-works)
- [Screenshots](#screenshots)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## About

**Snip** is a lightweight URL shortener web application. Instead of copying and pasting long, cumbersome URLs, Snip lets users paste any link and instantly get a short, clean URL they can share with a single click.

All shortened URLs are saved in a local SQLite database, so users can revisit their history, copy old links, and track how many times each link was clicked.

---

## Features

- 🔗 **Shorten any URL** — paste a long link, get a 6-character short code instantly
- 📋 **One-click copy** — copy the shortened URL to clipboard without fuss
- 📜 **History page** — view all previously shortened URLs with their short codes, click counts, and creation dates
- ✅ **URL validation** — checks for valid scheme (`http`/`https`) and domain before saving
- 🔁 **Deduplication** — re-submitting the same URL returns the existing short code instead of creating a new one
- 🗑️ **Delete links** — remove any entry from history
- 📊 **Live stats** — total links shortened and total clicks tracked on the home page
- 🔍 **Search & filter** — search through history in real time

---

## Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python, Flask                     |
| ORM        | SQLAlchemy                        |
| Database   | SQLite                            |
| Frontend   | HTML, CSS, JavaScript             |
| UI Icons   | Bootstrap Icons                   |
| Fonts      | Google Fonts (Syne, DM Mono, DM Sans) |

---

## Project Structure

```
url_shortener/
│
├── app.py                  # Flask application, routes, ORM model
├── requirements.txt        # Python dependencies
│
└── templates/
    ├── base.html           # Shared layout, navigation, toast notifications
    ├── index.html          # Home page — shorten a URL
    └── history.html        # History page — all saved URLs
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/snip-url-shortener.git
cd snip-url-shortener
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run the app**

```bash
python app.py
```

**4. Open in browser**

```
http://127.0.0.1:5000
```

The SQLite database (`urls.db`) is created automatically on first run inside the project directory.

---

## How It Works

### URL Shortening Flow

```
User enters URL
      │
      ▼
Validate URL (scheme + domain check via urlparse)
      │
      ├── Invalid → Return error message to user
      │
      └── Valid
            │
            ▼
      Check if URL already exists in DB
            │
            ├── Exists → Return existing short code
            │
            └── New → Generate unique 6-char alphanumeric code
                        │
                        ▼
                  Save to SQLite via SQLAlchemy
                        │
                        ▼
                  Return short URL to user
```

### Redirect Flow

```
User visits  /<short_code>
      │
      ▼
Look up code in database
      │
      ├── Not found → 404
      │
      └── Found → Increment click counter → Redirect to original URL
```

---

## API Endpoints

| Method   | Endpoint            | Description                          |
|----------|---------------------|--------------------------------------|
| `GET`    | `/`                 | Home page                            |
| `GET`    | `/history`          | History page                         |
| `POST`   | `/shorten`          | Shorten a URL (JSON body: `{url}`)   |
| `GET`    | `/<code>`           | Redirect to original URL             |
| `DELETE` | `/delete/<id>`      | Delete a URL record                  |
| `GET`    | `/api/stats`        | Returns total links and total clicks |

### Example Request

```bash
curl -X POST http://127.0.0.1:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/some/very/long/path"}'
```

### Example Response

```json
{
  "short_url": "http://127.0.0.1:5000/aB3xYz",
  "code": "aB3xYz"
}
```

---

## Database Model

```python
class URL(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    original   = db.Column(db.String(2048), nullable=False)
    shortened  = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    clicks     = db.Column(db.Integer, default=0)
```

---

## Future Improvements

- [ ] User authentication — personal link dashboards
- [ ] Custom aliases — let users pick their own short code
- [ ] QR code generation for each shortened URL
- [ ] Link expiration dates
- [ ] Analytics dashboard with click-over-time graphs
- [ ] Rate limiting to prevent abuse
- [ ] Deploy to cloud (Render, Railway, or Heroku)

---

## License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">Built with ❤️ using Flask & Python</p>
