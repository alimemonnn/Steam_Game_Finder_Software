<div align="center">

# 🎮 Steam Game Finder

### A real-time Steam storefront clone built with Python & Flask

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Vercel](https://img.shields.io/badge/Deployed_on-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br>

**Search the real Steam catalog. See live prices, ratings, and discounts.
Build your shortlist. Export to Excel in one click.**

<br>

🔗 **[Try the Live Demo →](https://steam-game-finder-software.vercel.app)**

</div>

---

## 🤔 What is this?

Ever wanted to quickly search Steam, compare games side by side, and save a list of what you want to buy — without opening Steam itself?

That's exactly what this does. Type any game name, genre, or keyword (like *"RPG"*, *"Free"*, or *"Cyberpunk"*) and get instant results pulled straight from Steam's live catalog — with real prices, review ratings, and active discounts. Add the ones you like to your shortlist and export the whole thing to a CSV spreadsheet.

It's a full Steam storefront experience, rebuilt from scratch in Python.

---

## ✨ What can it do?

🔍 &nbsp;**Search anything** — game titles, genres, keywords, even "free to play"

⭐ &nbsp;**Real ratings** — live review scores pulled directly from Steam (e.g. *"92% positive"*)

💸 &nbsp;**Live prices & deals** — see the current price and any active discount badge

🛒 &nbsp;**Personal shortlist** — add games you're interested in, remove ones you change your mind about

💰 &nbsp;**Running total** — see exactly how much your shortlist would cost

📥 &nbsp;**Export to CSV** — download your shortlist as a spreadsheet you can open in Excel or Google Sheets

🎨 &nbsp;**Steam-style UI** — dark theme, game cards with cover art, feels familiar if you've used Steam

---

## 🖥️ How it looks

```
┌─────────────────────────────────────────────────────────┐
│  🎮 Steam Clone          [ Search games...  ] [Search]  │
├──────────────────────────────────────┬──────────────────┤
│                                      │  🛒 My Shortlist │
│  ┌──────────┐  ┌──────────┐          │                  │
│  │ Game Art │  │ Game Art │          │  Cyberpunk 2077  │
│  │          │  │          │          │  $29.99          │
│  │ Title    │  │ Title    │          │                  │
│  │ ⭐ 92%   │  │ ⭐ 88%   │          │  Elden Ring      │
│  │ $29.99   │  │ Free     │          │  $59.99          │
│  │ [+ Keep] │  │ [+ Keep] │          │                  │
│  └──────────┘  └──────────┘          │  Total: $89.98   │
│                                      │  [📥 Export CSV] │
└──────────────────────────────────────┴──────────────────┘
```

---

## 🚀 Run it yourself

You only need Python installed. No database, no API keys, no setup headaches.

**Step 1 — Clone the project**
```bash
git clone https://github.com/alimemonnn/Steam_Game_Finder_Software.git
cd Steam_Game_Finder_Software
```

**Step 2 — Install the one dependency**
```bash
pip install -r requirements.txt
```

**Step 3 — Start it up**
```bash
python app.py
```

**Step 4 — Open your browser and go to:**
```
http://127.0.0.1:5000
```

That's it. Search for anything.

---

## 🗂️ Project structure

It's intentionally simple — just two files:

```
📁 Steam_Game_Finder/
│
├── 📄 app.py              ← Everything: Flask server, Steam API calls, and the UI
└── 📄 requirements.txt    ← Just one line: flask
```

All the HTML, CSS, and JavaScript live inside `app.py` as a template. No build tools, no node_modules, no complexity.

---

## ⚙️ How it works under the hood

```
User types a search query
        │
        ▼
Flask receives GET /api/search?q=...
        │
        ▼
Calls Steam Store Search API
(store.steampowered.com/api/storesearch)
        │
        ▼
For each result, fetches review data
(store.steampowered.com/appreviews/{id})
        │
        ▼
Returns JSON with title, price, discount, rating
        │
        ▼
Browser renders game cards with cover art
```

No data is stored anywhere. Every search hits Steam's live API fresh.

---

## 🌐 API reference

If you want to use the search endpoint directly:

```
GET /api/search?q={your query}
```

**Example:**
```bash
curl https://steam-game-finder-software.vercel.app/api/search?q=elden+ring
```

**Returns:**
```json
[
  {
    "id": "1245620",
    "title": "ELDEN RING",
    "price": "$59.99",
    "discount": "0%",
    "rating": "95%",
    "reviews": "1,024,381"
  }
]
```

---

## 🛠️ Built with

| What | Why |
|------|-----|
| **Python** | Backend logic and Steam API integration |
| **Flask** | Lightweight web framework to serve the app |
| **Vanilla JS** | Frontend interactivity — no heavy frameworks needed |
| **Steam Public API** | Live game data, prices, and review scores |
| **Vercel** | Free serverless deployment, zero config |

---

## ⚠️ A few things to know

- This uses Steam's **unofficial public API** — it's not affiliated with or endorsed by Valve
- Searches are capped at **12 results** to keep response times fast on serverless
- Occasionally Steam's API may be slow or rate-limited — just search again if results don't load
- This is a **portfolio & learning project**, not for commercial use

---

## 👤 Made by

**Muhammad Ali** · Full Stack Developer

[![GitHub](https://img.shields.io/badge/GitHub-alimemonnn-181717?style=flat-square&logo=github)](https://github.com/alimemonnn)

> Built to learn Python web development and practice real-world API integration.
> If you found this useful or interesting, a ⭐ on the repo would mean a lot!

---

<div align="center">
  <sub>MIT License · Free to use and modify with credit</sub>
</div>
