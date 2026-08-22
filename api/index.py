import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

STEAM_SEARCH_URL = "https://store.steampowered.com/api/storesearch/"
STEAM_REVIEWS_URL = "https://store.steampowered.com/appreviews/{app_id}?json=1"
DEFAULT_QUERY = "Top Rated"
MAX_RESULTS = 12

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

HTML = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Steam Storefront Clone & Evaluator</title>
<style>
:root{--bg:#171a21;--card:#1b2838;--hover:#2a475e;--blue:#66c0f4;--green:#a4d007;--text:#c7d5e0}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font-family:Segoe UI,Arial,sans-serif}
header{background:#171a21;border-bottom:2px solid #000;padding:16px 40px;display:flex;align-items:center;justify-content:space-between;gap:20px}
.brand{font-size:1.55rem;font-weight:700;color:#fff;white-space:nowrap}.brand span{color:var(--blue)}
.search{display:flex;gap:10px;width:min(650px,60%)}.search input{flex:1;padding:11px 14px;border:1px solid #000;border-radius:4px;background:#316282;color:#fff;font-size:1rem;outline:none}
.search button{border:0;border-radius:4px;padding:0 22px;background:linear-gradient(90deg,#47bfff,#1a9fff);color:#fff;font-weight:700;cursor:pointer}
.search button:disabled{opacity:.6;cursor:wait}
.wrap{max-width:1400px;margin:22px auto;padding:0 20px;display:grid;grid-template-columns:1fr 330px;gap:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:16px}
.card{background:var(--card);border:1px solid #ffffff0d;border-radius:5px;overflow:hidden;transition:.2s}.card:hover{transform:translateY(-3px);background:var(--hover)}
.card img{display:block;width:100%;height:145px;object-fit:cover}.details{padding:12px}.title{display:block;color:#fff;text-decoration:none;font-size:1.05rem;font-weight:600;margin-bottom:8px}.title:hover{color:var(--blue)}
.metrics{font-size:.85rem;color:#8f98a0;margin-bottom:10px}.pricebar{display:flex;justify-content:space-between;align-items:center;padding:7px 9px;background:#00000040;border-radius:3px}.discount{background:#4c6b22;color:var(--green);padding:2px 6px;font-weight:700}.price{color:#fff;font-weight:700}
.keep{width:100%;margin-top:10px;padding:9px;border:0;border-radius:3px;background:#5c7e10;color:#fff;font-weight:700;cursor:pointer}.keep:hover{background:#8bc53f;color:#000}
.side{background:var(--card);border-radius:5px;padding:20px;height:max-content;position:sticky;top:20px}.side h2{margin:0 0 14px;color:var(--blue);font-size:1.3rem}.item{display:flex;justify-content:space-between;gap:10px;padding:9px 0;border-bottom:1px solid #2a475e}.remove{border:0;background:#a62a2a;color:#fff;border-radius:3px;padding:4px 7px;cursor:pointer}.total{margin-top:15px;color:#fff;font-weight:700}.total span{color:var(--green)}.export{width:100%;margin-top:15px;padding:11px;border:0;border-radius:4px;background:var(--blue);color:#171a21;font-weight:700;cursor:pointer}
#loading{display:none;text-align:center;padding:35px;color:var(--blue)}#error{display:none;margin-bottom:15px;padding:12px;border-radius:4px;background:#5c1f1f;color:#fff}
.empty{text-align:center;padding:40px;color:#8f98a0}
@media(max-width:900px){header{flex-direction:column;align-items:stretch;padding:15px 20px}.search{width:100%}.wrap{grid-template-columns:1fr}.side{position:static}}
@media(max-width:500px){.search{flex-direction:column}.search button{height:42px}.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<header>
  <div class="brand">🎮 STEAM <span>CLONE</span></div>
  <div class="search">
    <input id="query" type="text" placeholder="Search Steam games..." autocomplete="off">
    <button id="searchBtn">Search</button>
  </div>
</header>

<div class="wrap">
  <main>
    <div id="error"></div>
    <div id="loading">🔍 Fetching live data from Steam...</div>
    <div id="grid" class="grid"></div>
  </main>

  <aside class="side">
    <h2>🛒 My Shortlist</h2>
    <div id="shortlist"><p style="color:#8f98a0">No games added yet.</p></div>
    <div class="total">Total Estimated: <span id="total">$0.00</span></div>
    <button class="export" id="exportBtn">📥 Export to CSV</button>
  </aside>
</div>

<script>
const shortlist = {};
const $ = id => document.getElementById(id);

function escapeHtml(value){
  return String(value ?? "")
    .replaceAll("&","&amp;").replaceAll("<","&lt;")
    .replaceAll(">","&gt;").replaceAll('"',"&quot;")
    .replaceAll("'","&#039;");
}

function showError(message){
  $("error").textContent = message;
  $("error").style.display = "block";
}

async function performSearch(){
  const query = $("query").value.trim();
  if(!query) return;

  $("error").style.display = "none";
  $("grid").innerHTML = "";
  $("loading").style.display = "block";
  $("searchBtn").disabled = true;

  try{
    const response = await fetch("/api/search?q=" + encodeURIComponent(query), {
      headers: {"Accept":"application/json"},
      cache: "no-store"
    });

    const data = await response.json();

    if(!response.ok || data.error){
      throw new Error(data.details || data.error || "Steam search failed.");
    }

    $("loading").style.display = "none";

    if(!Array.isArray(data) || data.length === 0){
      $("grid").innerHTML = '<div class="empty">No Steam games found. Try another search.</div>';
      return;
    }

    data.forEach(game => {
      const card = document.createElement("article");
      card.className = "card";

      const image = document.createElement("img");
      image.src = game.image || ("https://cdn.akamai.steamstatic.com/steam/apps/" + game.id + "/header.jpg");
      image.alt = game.title;
      image.loading = "lazy";
      image.onerror = function(){
        this.src = "https://placehold.co/460x215/1b2838/66c0f4?text=Steam+Game";
      };

      const details = document.createElement("div");
      details.className = "details";

      const link = document.createElement("a");
      link.className = "title";
      link.href = "https://store.steampowered.com/app/" + game.id;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = game.title;

      const metrics = document.createElement("div");
      metrics.className = "metrics";
      metrics.innerHTML =
        "Rating: <strong style='color:var(--blue)'>" +
        escapeHtml(game.rating) +
        "</strong> (" + escapeHtml(game.reviews) + " reviews)";

      const pricebar = document.createElement("div");
      pricebar.className = "pricebar";

      const discount = document.createElement("span");
      discount.className = "discount";
      discount.textContent = game.discount;

      const price = document.createElement("span");
      price.className = "price";
      price.textContent = game.price;

      pricebar.append(discount, price);

      const button = document.createElement("button");
      button.className = "keep";
      button.textContent = "+ Keep Game";
      button.onclick = () => addToShortlist(game);

      details.append(link, metrics, pricebar, button);
      card.append(image, details);
      $("grid").appendChild(card);
    });

  }catch(error){
    $("loading").style.display = "none";
    showError("Search failed: " + error.message);
    console.error(error);
  }finally{
    $("searchBtn").disabled = false;
  }
}

function addToShortlist(game){
  shortlist[game.id] = game;
  renderShortlist();
}

function removeFromShortlist(id){
  delete shortlist[id];
  renderShortlist();
}

function renderShortlist(){
  const container = $("shortlist");
  container.innerHTML = "";

  const ids = Object.keys(shortlist);

  if(!ids.length){
    container.innerHTML = '<p style="color:#8f98a0">No games added yet.</p>';
    $("total").textContent = "$0.00";
    return;
  }

  let total = 0;

  ids.forEach(id => {
    const game = shortlist[id];
    total += Number(game.numericPrice) || 0;

    const row = document.createElement("div");
    row.className = "item";

    const info = document.createElement("div");

    const name = document.createElement("div");
    name.style.color = "#fff";
    name.style.fontWeight = "700";
    name.textContent = game.title;

    const cost = document.createElement("div");
    cost.style.color = "var(--green)";
    cost.style.fontSize = ".85rem";
    cost.textContent = game.price;

    info.append(name, cost);

    const remove = document.createElement("button");
    remove.className = "remove";
    remove.textContent = "X";
    remove.onclick = () => removeFromShortlist(id);

    row.append(info, remove);
    container.appendChild(row);
  });

  $("total").textContent = "$" + total.toFixed(2);
}

function exportCSV(){
  const ids = Object.keys(shortlist);

  if(!ids.length){
    alert("Please add at least one game first.");
    return;
  }

  const rows = [
    ["Game Title","Price","Discount","Rating","Reviews","App ID","Steam URL"]
  ];

  ids.forEach(id => {
    const g = shortlist[id];
    rows.push([
      g.title, g.price, g.discount, g.rating, g.reviews, id,
      "https://store.steampowered.com/app/" + id
    ]);
  });

  const csv = rows.map(row =>
    row.map(value => '"' + String(value).replaceAll('"','""') + '"').join(",")
  ).join("\n");

  const blob = new Blob([csv], {type:"text/csv;charset=utf-8"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "Steam_Storefront_Shortlist.csv";
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

$("searchBtn").addEventListener("click", performSearch);
$("exportBtn").addEventListener("click", exportCSV);

$("query").addEventListener("keydown", event => {
  if(event.key === "Enter") performSearch();
});

window.addEventListener("load", () => {
  $("query").value = "Top Rated";
  performSearch();
});
</script>
</body>
</html>
"""

def http_get_json(url, params=None, timeout=12):
    if params:
        query_string = "&".join(
            f"{quote(str(key))}={quote(str(value))}"
            for key, value in params.items()
        )
        separator = "&" if "?" in url else "?"
        url = url + separator + query_string

    req = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json,text/plain,*/*",
            "Accept-Language": "en-US,en;q=0.9",
        },
        method="GET",
    )

    with urlopen(req, timeout=timeout) as response:
        status = getattr(response, "status", 200)
        body = response.read().decode("utf-8")

    if status < 200 or status >= 300:
        raise RuntimeError(f"Steam returned HTTP {status}.")

    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Steam returned invalid JSON.") from exc


def steam_search(query):
    """Fetch games from Steam's public storefront search endpoint."""
    data = http_get_json(
        STEAM_SEARCH_URL,
        params={
            "term": query,
            "l": "english",
            "cc": "US",
        },
        timeout=15,
    )

    if not isinstance(data, dict):
        raise RuntimeError("Steam returned an unexpected response.")

    return data.get("items", [])[:MAX_RESULTS]


def get_review_info(app_id):
    """Reviews are optional; a review failure must not break search."""
    try:
        data = http_get_json(
            STEAM_REVIEWS_URL.format(app_id=app_id),
            params={
                "language": "all",
                "purchase_type": "all",
            },
            timeout=7,
        )

        summary = data.get("query_summary", {}) if isinstance(data, dict) else {}

        total = int(summary.get("total_reviews", 0) or 0)
        positive = int(summary.get("total_positive", 0) or 0)

        if total:
            rating = f"{round((positive / total) * 100)}%"
        else:
            rating = "N/A"

        return rating, total

    except Exception as exc:
        print(f"Review lookup failed for {app_id}: {exc}")
        return "N/A", 0


def make_game(item):
    app_id = str(item.get("id", ""))

    if not app_id:
        return None

    price_data = item.get("price") or {}

    try:
        final_cents = int(price_data.get("final", 0) or 0)
    except (TypeError, ValueError):
        final_cents = 0

    numeric_price = final_cents / 100

    if numeric_price > 0:
        price = f"${numeric_price:.2f}"
    elif item.get("is_free"):
        price = "Free"
    else:
        price = "N/A"

    try:
        discount_percent = int(
            price_data.get("discount_percent", 0) or 0
        )
    except (TypeError, ValueError):
        discount_percent = 0

    image = item.get("tiny_image") or (
        f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg"
    )

    return {
        "id": app_id,
        "title": item.get("name", "Unknown"),
        "price": price,
        "numericPrice": numeric_price,
        "discount": f"{discount_percent}%",
        "rating": "N/A",
        "reviews": "0",
        "image": image,
    }


@app.route("/", methods=["GET"])
@app.route("/api/index", methods=["GET"])
def home():
    return render_template_string(HTML)


@app.route("/api/search", methods=["GET"])
def api_search():
    query = request.args.get("q", DEFAULT_QUERY).strip()

    if not query:
        return jsonify([])

    try:
        items = steam_search(query)

    except (HTTPError, URLError, TimeoutError) as exc:
        print("Steam connection error:", repr(exc))
        return jsonify({
            "error": "Steam could not be reached.",
            "details": str(exc),
        }), 502

    except Exception as exc:
        print("Steam search error:", repr(exc))
        return jsonify({
            "error": "Steam search failed.",
            "details": str(exc),
        }), 502

    games = []

    for item in items:
        game = make_game(item)
        if game:
            games.append(game)

    if games:
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = {
                executor.submit(get_review_info, game["id"]): game
                for game in games
            }

            for future in as_completed(futures):
                game = futures[future]

                try:
                    rating, reviews = future.result()
                    game["rating"] = rating
                    game["reviews"] = f"{reviews:,}"
                except Exception as exc:
                    print(
                        f"Unexpected review worker error "
                        f"for {game['id']}: {exc}"
                    )

    return jsonify(games)


@app.route("/api/health", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "Steam Storefront Clone",
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Route not found",
        "path": request.path,
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "details": str(error),
    }), 500


if __name__ == "__main__":
    print("🚀 Steam Storefront Clone")
    print("📍 http://127.0.0.1:5000")
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )