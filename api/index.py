import json
import urllib.parse
import urllib.request

from flask import Flask, jsonify, render_template_string, request


app = Flask(__name__)


# ============================================================
# HTML / CSS / JAVASCRIPT
# ============================================================

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

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Motiva Sans', 'Segoe UI', Arial, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            margin: 0;
            padding: 0;
        }

        /* =========================
           Header
        ========================= */

        header {
            background: #171a21;
            border-bottom: 2px solid #000;
            padding: 15px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1.6em;
            font-weight: bold;
            color: #fff;
            letter-spacing: 1px;
            white-space: nowrap;
        }

        .brand span {
            color: var(--accent-blue);
        }

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

        .search-container input::placeholder {
            color: #8f98a0;
        }

        .search-container button {
            background: linear-gradient(to right, #47bfff, #1a9fff);
            border: none;
            color: #fff;
            padding: 10px 20px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 3px;
        }

        .search-container button:hover {
            opacity: 0.9;
        }

        /* =========================
           Main Layout
        ========================= */

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
            grid-template-columns: repeat(
                auto-fill,
                minmax(280px, 1fr)
            );
            gap: 15px;
        }

        /* =========================
           Game Cards
        ========================= */

        .game-card {
            background: var(--bg-card);
            border-radius: 4px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition:
                transform 0.2s,
                background 0.2s;
            border: 1px solid rgba(255, 255, 255, 0.05);
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

        .game-title:hover {
            color: var(--accent-blue);
        }

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

        .price {
            color: #fff;
            font-weight: bold;
        }

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

        .btn-add:hover {
            background: #8bc53f;
            color: #000;
        }

        /* =========================
           Sidebar
        ========================= */

        .sidebar {
            background: var(--bg-card);
            border-radius: 4px;
            padding: 20px;
            height: fit-content;
            position: sticky;
            top: 20px;
        }

        .sidebar h2 {
            margin-top: 0;
            color: var(--accent-blue);
            font-size: 1.3em;
        }

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

        .btn-export:hover {
            background: var(--accent-green);
        }

        /* =========================
           Loading
        ========================= */

        #loading {
            display: none;
            text-align: center;
            grid-column: 1 / -1;
            padding: 40px;
            font-size: 1.2em;
            color: var(--accent-blue);
        }

        /* =========================
           Responsive Design
        ========================= */

        @media (max-width: 900px) {
            header {
                flex-direction: column;
                gap: 15px;
                padding: 15px 20px;
            }

            .search-container {
                width: 100%;
            }

            .wrapper {
                grid-template-columns: 1fr;
            }

            .sidebar {
                position: static;
            }
        }

        @media (max-width: 500px) {
            .search-container {
                flex-direction: column;
            }

            .search-container button {
                width: 100%;
            }

            .game-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>

<body>

    <!-- =========================
         Header
    ========================= -->

    <header>
        <div class="brand">
            🎮 STEAM <span>CLONE</span>
        </div>

        <div class="search-container">
            <input
                type="text"
                id="query"
                placeholder="Search Steam catalog..."
                onkeypress="handleKeyPress(event)"
            >

            <button onclick="performSearch()">
                Search
            </button>
        </div>
    </header>


    <!-- =========================
         Main Content
    ========================= -->

    <div class="wrapper">

        <div>
            <div id="loading">
                🔍 Fetching live data from Steam...
            </div>

            <div
                class="game-grid"
                id="game-grid"
            >
                <!-- Search results appear here -->
            </div>
        </div>


        <!-- =========================
             Shortlist Sidebar
        ========================= -->

        <div class="sidebar">

            <h2>🛒 My Shortlist</h2>

            <div id="shortlist-container">
                <p style="color: #8f98a0;">
                    No games added yet.
                    Search and click "Keep" to add.
                </p>
            </div>

            <div class="total-box">
                Total Estimated:

                <span
                    id="total-price"
                    style="color: var(--accent-green);"
                >
                    $0.00
                </span>
            </div>

            <button
                class="btn-export"
                onclick="exportCSV()"
            >
                📥 Export to Excel (CSV)
            </button>

        </div>

    </div>


    <!-- =========================
         JavaScript
    ========================= -->

    <script>

        let shortlist = {};


        /* =========================
           Enter Key Search
        ========================= */

        function handleKeyPress(event) {

            if (event.key === "Enter") {
                performSearch();
            }

        }


        /* =========================
           Search Steam
        ========================= */

        async function performSearch() {

            const queryElement =
                document.getElementById("query");

            const query =
                queryElement.value.trim();

            if (!query) {
                return;
            }


            const grid =
                document.getElementById("game-grid");

            const loading =
                document.getElementById("loading");


            grid.innerHTML = "";

            loading.style.display = "block";


            try {

                const response = await fetch(
                    `/api/search?q=${encodeURIComponent(query)}`
                );


                if (!response.ok) {
                    throw new Error(
                        `HTTP error: ${response.status}`
                    );
                }


                const games =
                    await response.json();


                loading.style.display = "none";


                if (!Array.isArray(games) || games.length === 0) {

                    grid.innerHTML = `
                        <p>
                            No games found.
                            Try a different query.
                        </p>
                    `;

                    return;
                }


                games.forEach(function(game) {

                    const card =
                        document.createElement("div");

                    card.className = "game-card";


                    const safeGame =
                        JSON.stringify(game)
                            .replace(/'/g, "&#39;");


                    card.innerHTML = `

                        <img
                            src="https://cdn.akamai.steamstatic.com/steam/apps/${game.id}/header.jpg"
                            onerror="this.src='https://via.placeholder.com/280x140?text=Steam+Game'"
                            alt="${escapeHtml(game.title)}"
                        >

                        <div class="game-details">

                            <a
                                href="https://store.steampowered.com/app/${game.id}"
                                target="_blank"
                                rel="noopener noreferrer"
                                class="game-title"
                            >
                                ${escapeHtml(game.title)}
                            </a>

                            <div class="metrics">

                                Rating:
                                <strong
                                    style="color: var(--accent-blue);"
                                >
                                    ${escapeHtml(game.rating)}
                                </strong>

                                (${escapeHtml(game.reviews)}
                                reviews)

                            </div>


                            <div class="price-bar">

                                <span class="discount-tag">
                                    ${escapeHtml(game.discount)}
                                </span>

                                <span class="price">
                                    ${escapeHtml(game.price)}
                                </span>

                            </div>


                            <button
                                class="btn-add"
                                onclick='addToShortlist(${safeGame})'
                            >
                                + Keep Game
                            </button>

                        </div>
                    `;


                    grid.appendChild(card);

                });

            }

            catch (error) {

                console.error(
                    "Search error:",
                    error
                );


                loading.style.display = "none";


                grid.innerHTML = `
                    <p style="color:#ff6b6b;">
                        Error fetching game data from Steam.
                        Please try again.
                    </p>
                `;

            }

        }


        /* =========================
           Basic HTML Escaping
        ========================= */

        function escapeHtml(value) {

            if (value === null || value === undefined) {
                return "";
            }


            return String(value)
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");

        }


        /* =========================
           Add Game
        ========================= */

        function addToShortlist(game) {

            shortlist[game.id] = game;

            renderShortlist();

        }


        /* =========================
           Remove Game
        ========================= */

        function removeFromShortlist(id) {

            delete shortlist[id];

            renderShortlist();

        }


        /* =========================
           Render Shortlist
        ========================= */

        function renderShortlist() {

            const container =
                document.getElementById(
                    "shortlist-container"
                );


            container.innerHTML = "";


            let total = 0.0;


            const keys =
                Object.keys(shortlist);


            if (keys.length === 0) {

                container.innerHTML = `
                    <p style="color: #8f98a0;">
                        No games added yet.
                    </p>
                `;


                document.getElementById(
                    "total-price"
                ).innerText = "$0.00";


                return;
            }


            keys.forEach(function(id) {

                const game =
                    shortlist[id];


                total +=
                    Number(game.numericPrice) || 0;


                const item =
                    document.createElement("div");


                item.className =
                    "shortlist-item";


                item.innerHTML = `

                    <div>

                        <div
                            style="
                                color: #fff;
                                font-weight: bold;
                            "
                        >
                            ${escapeHtml(game.title)}
                        </div>

                        <div
                            style="
                                color: var(--accent-green);
                                font-size: 0.85em;
                            "
                        >
                            ${escapeHtml(game.price)}
                        </div>

                    </div>


                    <button
                        class="btn-remove"
                        onclick="removeFromShortlist('${id}')"
                    >
                        X
                    </button>

                `;


                container.appendChild(item);

            });


            document.getElementById(
                "total-price"
            ).innerText =
                "$" + total.toFixed(2);

        }


        /* =========================
           Export CSV
        ========================= */

        function exportCSV() {

            const keys =
                Object.keys(shortlist);


            if (keys.length === 0) {

                alert(
                    "Please add at least one game to your shortlist!"
                );

                return;
            }


            let csv =
                "Game Title,Price,Discount,Rating,App ID,URL\\n";


            keys.forEach(function(id) {

                const game =
                    shortlist[id];


                const title =
                    String(game.title)
                        .replace(/"/g, '""');


                const price =
                    String(game.price)
                        .replace(/"/g, '""');


                const discount =
                    String(game.discount)
                        .replace(/"/g, '""');


                const rating =
                    String(game.rating)
                        .replace(/"/g, '""');


                csv +=
                    `"${title}","${price}","${discount}","${rating}","${id}","https://store.steampowered.com/app/${id}"\\n`;

            });


            const blob =
                new Blob(
                    [csv],
                    {
                        type: "text/csv;charset=utf-8;"
                    }
                );


            const url =
                URL.createObjectURL(blob);


            const link =
                document.createElement("a");


            link.href = url;

            link.download =
                "Steam_Storefront_Shortlist.csv";


            document.body.appendChild(link);

            link.click();

            document.body.removeChild(link);


            URL.revokeObjectURL(url);

        }


        /* =========================
           Automatic Search
        ========================= */

        window.onload = function() {

            document.getElementById(
                "query"
            ).value = "Top Rated";


            performSearch();

        };

    </script>

</body>
</html>
"""


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def index():

    return render_template_string(
        HTML_TEMPLATE
    )


# ============================================================
# STEAM SEARCH API
# ============================================================

@app.route("/api/search")
def api_search():

    query = request.args.get(
        "q",
        "action"
    ).strip()


    if not query:

        return jsonify([])


    encoded_query =urllib.parse.quote(query)


    # Steam Store Search API
    search_url = (
        "https://store.steampowered.com/api/storesearch/"
        f"?term={encoded_query}&l=english&cc=US"
    )


    request_object = urllib.request.Request(
        search_url,
        headers={
            "User-Agent":
                "Mozilla/5.0"
        }
    )


    games = []


    try:

        # ----------------------------------------------------
        # Get Steam search results
        # ----------------------------------------------------

        with urllib.request.urlopen(
            request_object,
            timeout=15
        ) as response:

            search_data = json.loads(
                response.read().decode("utf-8")
            )


        items =search_data.get("items",[])[:12]


        # ----------------------------------------------------
        # Process each game
        # ----------------------------------------------------

        for item in items:

            app_id =str(item.get("id", ""))


            if not app_id:
                continue


            # ------------------------------------------------
            # Get review information
            # ------------------------------------------------

            review_url = ("https://store.steampowered.com/appreviews/" f"{app_id}?json=1")


            review_request =urllib.request.Request(review_url,headers={"User-Agent":"Mozilla/5.0"})


            rating_score = "N/A"

            total_reviews = 0


            try:

                with urllib.request.urlopen(
                    review_request,
                    timeout=10
                ) as review_response:

                    review_json =json.loads(review_response.read().decode("utf-8"))


                review_summary =review_json.get("query_summary",{})


                total_reviews =review_summary.get("total_reviews",0)


                positive_reviews =review_summary.get("total_positive",0)


                if total_reviews > 0:

                    rating_score = (f"{round((positive_reviews / total_reviews)* 100)}%")


            except Exception as review_error:

                print(
                    "Review API Error:",
                    review_error
                )


            # ------------------------------------------------
            # Price information
            # ------------------------------------------------

            price_data = item.get(
                    "price",
                    {}
                )


            if price_data:

                final_price =price_data.get("final",0)


                numeric_price =final_price / 100.0


                if numeric_price > 0:

                    price_string =f"${numeric_price:.2f}"

                elif item.get("is_free"):

                    price_string = "Free"

                else:

                    price_string = "N/A"


                discount_percent = price_data.get("discount_percent",0)


                discount =f"{discount_percent}%"

            else:

                numeric_price = 0.0

                price_string = (
                    "Free"
                    if item.get("is_free")
                    else "N/A"
                )

                discount = "0%"


            # ------------------------------------------------
            # Add game
            # ------------------------------------------------

            games.append({

                "id":
                    app_id,

                "title":
                    item.get(
                        "name",
                        "Unknown"
                    ),

                "price":
                    price_string,

                "numericPrice":
                    numeric_price,

                "discount":
                    discount,

                "rating":
                    rating_score,

                "reviews":
                    f"{total_reviews:,}"

            })


    except Exception as error:

        print(
            "Search API Error:",
            error
        )


    return jsonify(games)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "ok"
    })


# ============================================================
# LOCAL DEVELOPMENT
# ============================================================
#
# Vercel does NOT use this section when deploying the Flask app.
# It is only for running the project locally with:
#
#     python api/index.py
#
# ============================================================

if __name__ == "__main__":

    print(
        "🚀 Steam Storefront Clone running on "
        "http://127.0.0.1:5000"
    )

    app.run(
        debug=True,
        port=5000
    )