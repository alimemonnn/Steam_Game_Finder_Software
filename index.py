import json
import urllib.parse
import urllib.request
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Steam Storefront Clone & Evaluator</title>
    <style>
        :root {
            --bg-main: #171a21;
            --bg-card: #1b2838;
            --bg-hover: #2a475e;
            --accent-blue: #66c0f4;
            --accent-green: #a4d007;
            --text-main: #c7d5e0;
        }

        body {
            font-family: 'Motiva Sans', 'Segoe UI', Arial, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            margin: 0;
            padding: 0;
        }

        header {
            background: #171a21;
            border-bottom: 2px solid #000;
            padding: 15px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1.6em;
            font-weight: bold;
            color: #fff;
            letter-spacing: 1px;
        }

        .brand span { color: var(--accent-blue); }

        .search-container {
            display: flex;
            gap: 10px;
            width: 45%;
        }

        .search-container input {
            width: 100%;
            padding: 10px 15px;
            background: #316282;
            border: 1px solid #000;
            border-radius: 3px;
            color: #fff;
            font-size: 1em;
            outline: none;
        }

        .search-container input::placeholder { color: #8f98a0; }

        .search-container button {
            background: linear-gradient(to right, #47bfff, #1a9fff);
            border: none;
            color: #fff;
            padding: 10px 20px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 3px;
        }

        .wrapper {
            display: grid;
            grid-template-columns: 1fr 340px;
            gap: 20px;
            max-width: 1400px;
            margin: 20px auto;
            padding: 0 20px;
        }

        .game-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 15px;
        }

        .game-card {
            background: var(--bg-card);
            border-radius: 4px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s, background 0.2s;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .game-card:hover {
            transform: translateY(-4px);
            background: var(--bg-hover);
        }

        .game-card img {
            width: 100%;
            height: 140px;
            object-fit: cover;
        }

        .game-details {
            padding: 12px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .game-title {
            font-size: 1.1em;
            color: #fff;
            margin-bottom: 8px;
            text-decoration: none;
        }

        .game-title:hover { color: var(--accent-blue); }

        .metrics {
            font-size: 0.85em;
            color: #8f98a0;
            margin-bottom: 10px;
        }

        .price-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #00000040;
            padding: 6px 10px;
            border-radius: 3px;
        }

        .discount-tag {
            background: #4c6b22;
            color: var(--accent-green);
            font-weight: bold;
            padding: 2px 6px;
            border-radius: 2px;
        }

        .price { color: #fff; font-weight: bold; }

        .btn-add {
            width: 100%;
            margin-top: 10px;
            background: #5c7e10;
            color: #fff;
            border: none;
            padding: 8px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 3px;
        }

        .btn-add:hover { background: #8bc53f; color: #000; }

        .sidebar {
            background: var(--bg-card);
            border-radius: 4px;
            padding: 20px;
            height: fit-content;
            position: sticky;
            top: 20px;
        }

        .sidebar h2 { margin-top: 0; color: var(--accent-blue); font-size: 1.3em; }

        .shortlist-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #2a475e;
            font-size: 0.9em;
        }

        .btn-remove {
            background: #a62a2a;
            color: #fff;
            border: none;
            padding: 2px 6px;
            cursor: pointer;
            border-radius: 2px;
        }

        .total-box {
            margin-top: 15px;
            font-size: 1.1em;
            font-weight: bold;
            color: #fff;
        }

        .btn-export {
            width: 100%;
            margin-top: 15px;
            background: var(--accent-blue);
            color: #171a21;
            border: none;
            padding: 12px;
            font-weight: bold;
            font-size: 1em;
            cursor: pointer;
            border-radius: 4px;
        }

        .btn-export:hover { background: var(--accent-green); }

        #loading {
            display: none;
            text-align: center;
            grid-column: 1 / -1;
            padding: 40px;
            font-size: 1.2em;
            color: var(--accent-blue);
        }
    </style>
</head>
<body>

    <header>
        <div class="brand">🎮 STEAM <span>CLONE</span></div>
        <div class="search-container">
            <input type="text" id="query" placeholder="Search Steam full catalog (e.g., Cyberpunk, RPG, Open World, Free)..." onkeypress="handleKeyPress(event)">
            <button onclick="performSearch()">Search</button>
        </div>
    </header>

    <div class="wrapper">
        <div>
            <div id="loading">🔍 Fetching live data from Steam...</div>
            <div class="game-grid" id="game-grid">
                <!-- Search results injected here -->
            </div>
        </div>

        <div class="sidebar">
            <h2>🛒 My Shortlist</h2>
            <div id="shortlist-container">
                <p style="color: #8f98a0;">No games added yet. Search and click "Keep" to add.</p>
            </div>
            <div class="total-box">
                Total Estimated: <span id="total-price" style="color: var(--accent-green);">$0.00</span>
            </div>
            <button class="btn-export" onclick="exportCSV()">📥 Export to Excel (CSV)</button>
        </div>
    </div>

    <script>
        let shortlist = {};

        function handleKeyPress(e) {
            if (e.key === 'Enter') performSearch();
        }

        async function performSearch() {
            const query = document.getElementById('query').value.trim();
            if (!query) return;

            const grid = document.getElementById('game-grid');
            const loading = document.getElementById('loading');
            grid.innerHTML = '';
            loading.style.display = 'block';

            try {
                const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
                const games = await res.json();
                loading.style.display = 'none';

                if (games.length === 0) {
                    grid.innerHTML = '<p>No games found. Try a different query.</p>';
                    return;
                }

                games.forEach(g => {
                    const card = document.createElement('div');
                    card.className = 'game-card';
                    card.innerHTML = `
                        <img src="https://cdn.akamai.steamstatic.com/steam/apps/${g.id}/header.jpg" onerror="this.src='https://via.placeholder.com/280x140?text=Steam+Game'">
                        <div class="game-details">
                            <a href="https://store.steampowered.com/app/${g.id}" target="_blank" class="game-title">${g.title}</a>
                            <div class="metrics">
                                Rating: <strong style="color: var(--accent-blue);">${g.rating}</strong> (${g.reviews} reviews)
                            </div>
                            <div class="price-bar">
                                <span class="discount-tag">${g.discount}</span>
                                <span class="price">${g.price}</span>
                            </div>
                            <button class="btn-add" onclick='addToShortlist(${JSON.stringify(g)})'>+ Keep Game</button>
                        </div>
                    `;
                    grid.appendChild(card);
                });
            } catch (err) {
                loading.style.display = 'none';
                alert('Error fetching game data from Steam.');
            }
        }

        function addToShortlist(game) {
            shortlist[game.id] = game;
            renderShortlist();
        }

        function removeFromShortlist(id) {
            delete shortlist[id];
            renderShortlist();
        }

        function renderShortlist() {
            const container = document.getElementById('shortlist-container');
            container.innerHTML = '';
            let total = 0.0;
            const keys = Object.keys(shortlist);

            if (keys.length === 0) {
                container.innerHTML = '<p style="color: #8f98a0;">No games added yet.</p>';
                document.getElementById('total-price').innerText = '$0.00';
                return;
            }

            keys.forEach(id => {
                const g = shortlist[id];
                total += g.numericPrice;

                const item = document.createElement('div');
                item.className = 'shortlist-item';
                item.innerHTML = `
                    <div>
                        <div style="color: #fff; font-weight: bold;">${g.title}</div>
                        <div style="color: var(--accent-green); font-size: 0.85em;">${g.price}</div>
                    </div>
                    <button class="btn-remove" onclick="removeFromShortlist('${id}')">X</button>
                `;
                container.appendChild(item);
            });

            document.getElementById('total-price').innerText = '$' + total.toFixed(2);
        }

        function exportCSV() {
            const keys = Object.keys(shortlist);
            if (keys.length === 0) {
                alert("Please add at least one game to your shortlist!");
                return;
            }

            let csv = "data:text/csv;charset=utf-8,Game Title,Price,Discount,Rating,App ID,URL\\n";
            keys.forEach(id => {
                const g = shortlist[id];
                csv += `"${g.title}","${g.price}","${g.discount}","${g.rating}","${id}","https://store.steampowered.com/app/${id}"\\n`;
            });

            const encodedUri = encodeURI(csv);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "Steam_Storefront_Shortlist.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        window.onload = () => {
            document.getElementById('query').value = 'Top Rated';
            performSearch();
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/search')
def api_search():
    query = request.args.get('q', 'action')
    encoded_query = urllib.parse.quote(query)

    search_url = f"https://store.steampowered.com/api/storesearch/?term={encoded_query}&l=english&cc=US"
    req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})

    games = []
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            search_data = json.loads(response.read().decode())
            items = search_data.get('items', [])[:12]

            for item in items:
                app_id = str(item['id'])

                rev_url = f"https://store.steampowered.com/appreviews/{app_id}?json=1"
                req_rev = urllib.request.Request(rev_url, headers={'User-Agent': 'Mozilla/5.0'})

                rating_score = "N/A"
                total_reviews = 0
                try:
                    with urllib.request.urlopen(req_rev, timeout=5) as rev_res:
                        rev_data = json.loads(rev_res.read().decode())['query_summary']
                        total_reviews = rev_data.get('total_reviews', 0)
                        pos = rev_data.get('total_positive', 0)
                        if total_reviews > 0:
                            rating_score = f"{round((pos / total_reviews) * 100)}%"
                except Exception:
                    pass

                price_data = item.get('price', {})
                numeric_price = (price_data.get('final', 0) / 100.0) if price_data else 0.0
                price_str = f"${numeric_price:.2f}" if numeric_price > 0 else ("Free" if item.get('is_free') else "N/A")
                discount = f"{price_data.get('discount_percent', 0)}%" if price_data else "0%"

                games.append({
                    "id": app_id,
                    "title": item.get('name', 'Unknown'),
                    "price": price_str,
                    "numericPrice": numeric_price,
                    "discount": discount,
                    "rating": rating_score,
                    "reviews": f"{total_reviews:,}"
                })
    except Exception as e:
        print("Search API Error:", e)

    return jsonify(games)

# Vercel's Python runtime looks for a WSGI-callable named `app`
# (no app.run() needed / used in production on Vercel)
