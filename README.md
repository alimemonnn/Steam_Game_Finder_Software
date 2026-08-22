
# 🎮 Steam Game Finder & Evaluator

An interactive web application built with **Python (Flask)** and **Vanilla JavaScript** that interfaces directly with Steam's public APIs. It allows users to search live Steam titles, view rating analytics in real time, build custom game shortlists with dynamic budget estimation, and export selected games directly to CSV.

---

## ✨ Features

* 🔍 **Live Steam API Integration:** Performs real-time game searches directly against Steam storefront data.
* ⚡ **Fast Concurrent Processing:** Utilizes Python's `ThreadPoolExecutor` to perform asynchronous parallel review scoring lookups.
* 🛒 **Interactive Shortlist:** Add or remove games on the fly with live total budget estimation.
* 📥 **CSV Export:** Download your custom shortlist with game titles, prices, ratings, and direct store URLs in one click.
* 📱 **Responsive UI:** Dark-mode Steam storefront UI built with standard CSS grid and flexbox.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend Framework** | Python 3, Flask |
| **Concurrency** | `concurrent.futures` (`ThreadPoolExecutor`) |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) |
| **Deployment Platform** | Vercel Serverless Functions |

---

## 🚀 Getting Started Locally

### Prerequisites

* Python 3.9+ installed on your system.
* Git installed.

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/alimemonnn/Steam_Game_Finder_Software.git](https://github.com/alimemonnn/Steam_Game_Finder_Software.git)
   cd Steam_Game_Finder_Software
