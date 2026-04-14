from flask import Flask, render_template_string
from datetime import datetime
import math
import yfinance as yf

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Piyasa Takip</title>
  <meta http-equiv="refresh" content="60">
  <style>
    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: Inter, Arial, sans-serif;
      background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
      color: #e5e7eb;
    }

    .container {
      max-width: 1240px;
      margin: 0 auto;
      padding: 28px 20px 40px;
    }

    .hero {
      display: flex;
      justify-content: space-between;
      align-items: stretch;
      gap: 18px;
      margin-bottom: 24px;
      flex-wrap: wrap;
    }

    .hero-left {
      flex: 1;
      min-width: 280px;
    }

    .title {
      font-size: 42px;
      font-weight: 900;
      margin: 0 0 8px;
      letter-spacing: -0.03em;
    }

    .subtitle {
      margin: 0;
      color: #94a3b8;
      font-size: 16px;
      line-height: 1.5;
    }

    .hero-right {
      display: grid;
      grid-template-columns: repeat(2, minmax(220px, 1fr));
      gap: 16px;
      flex: 1;
      min-width: 320px;
    }

    .top-box {
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 20px;
      padding: 18px;
      box-shadow: 0 12px 30px rgba(0,0,0,0.22);
      backdrop-filter: blur(8px);
    }

    .top-label {
      color: #94a3b8;
      font-size: 13px;
      margin-bottom: 8px;
    }

    .top-value {
      font-size: 18px;
      font-weight: 800;
    }

    .top-sub {
      margin-top: 8px;
      font-size: 13px;
      color: #94a3b8;
      line-height: 1.5;
    }

    .section {
      margin-top: 28px;
    }

    .section-title {
      font-size: 24px;
      font-weight: 900;
      margin: 0 0 14px;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 16px;
    }

    .card {
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 20px;
      padding: 18px;
      box-shadow: 0 12px 30px rgba(0,0,0,0.22);
      backdrop-filter: blur(8px);
    }

    .card-label {
      color: #94a3b8;
      font-size: 14px;
      margin-bottom: 10px;
    }

    .card-price {
      font-size: 30px;
      font-weight: 900;
      margin-bottom: 10px;
      line-height: 1.2;
      word-break: break-word;
    }

    .pill-row {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
    }

    .pill {
      display: inline-block;
      font-size: 13px;
      font-weight: 800;
      padding: 7px 10px;
      border-radius: 999px;
    }

    .pill-up {
      background: rgba(34, 197, 94, 0.12);
      color: #4ade80;
    }

    .pill-down {
      background: rgba(239, 68, 68, 0.12);
      color: #f87171;
    }

    .pill-neutral {
      background: rgba(148, 163, 184, 0.12);
      color: #cbd5e1;
    }

    .pill-strong {
      background: rgba(168, 85, 247, 0.14);
      color: #d8b4fe;
    }

    .card-note {
      margin-top: 12px;
      color: #94a3b8;
      font-size: 13px;
      line-height: 1.5;
    }

    .summary-grid {
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 16px;
    }

    .summary-box {
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 20px;
      padding: 18px;
      box-shadow: 0 12px 30px rgba(0,0,0,0.22);
    }

    .summary-title {
      font-size: 20px;
      font-weight: 900;
      margin-bottom: 14px;
    }

    .summary-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding: 12px 0;
      border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    .summary-row:last-child {
      border-bottom: none;
      padding-bottom: 0;
    }

    .summary-left {
      flex: 1;
    }

    .summary-name {
      font-weight: 800;
      margin-bottom: 4px;
    }

    .summary-desc {
      color: #94a3b8;
      font-size: 13px;
    }

    .summary-trend {
      font-weight: 900;
      font-size: 15px;
    }

    .global-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 16px;
    }

    .footer-note {
      margin-top: 14px;
      font-size: 13px;
      color: #94a3b8;
      line-height: 1.6;
    }

    @media (max-width: 950px) {
      .hero-right {
        grid-template-columns: 1fr;
      }

      .summary-grid {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 640px) {
      .title { font-size: 32px; }
      .card-price { font-size: 24px; }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="hero">
      <div class="hero-left">
        <h1 class="title">Piyasa Takip 🚀</h1>
        <p class="subtitle">Döviz, altın ve önemli piyasa verilerini tek ekranda takip edin.</p>
      </div>

      <div class="hero-right">
        <div class="top-box">
          <div class="top-label">Durum</div>
          <div class="top-value">Canlı piyasa verileri aktif</div>
          <div class="top-sub">Sayfa 60 saniyede bir otomatik yenilenir.</div>
        </div>

        <div class="top-box">
          <div class="top-label">Genel Piyasa Skoru</div>
          <div class="top-value">{{ market_score }}/100</div>
          <div class="top-sub">{{ market_score_note }}</div>
        </div>

        <div class="top-box">
          <div class="top-label">En Güçlü Varlık</div>
          <div class="top-value">{{ top_asset.name }}</div>
          <div class="top-sub">{{ top_asset.reason }}</div>
        </div>

        <div class="top-box">
          <div class="top-label">Son Güncelleme</div>
          <div class="top-value">{{ updated_at }}</div>
          <div class="top-sub">Render üzerinde canlı yayınlanan sürüm.</div>
        </div>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Döviz</h2>
      <div class="grid">
        {% for item in doviz %}
        <div class="card">
          <div class="card-label">{{ item.name }}</div>
          <div class="card-price">{{ item.currency_symbol }} {{ item.price }}</div>
          <div class="pill-row">
            <div class="pill {% if item.pct_value > 0 %}pill-up{% elif item.pct_value < 0 %}pill-down{% else %}pill-neutral{% endif %}">
              {{ item.pct_text }}
            </div>
            <div class="pill pill-neutral">{{ item.signal }}</div>
          </div>
          <div class="card-note">{{ item.comment }}</div>
        </div>
        {% endfor %}
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Altın</h2>
      <div class="grid">
        {% for item in altin %}
        <div class="card">
          <div class="card-label">{{ item.name }}</div>
          <div class="card-price">₺ {{ item.price }}</div>
          <div class="pill-row">
            <div class="pill {% if item.pct_value > 0 %}pill-up{% elif item.pct_value < 0 %}pill-down{% else %}pill-neutral{% endif %}">
              {{ item.pct_text }}
            </div>
            <div class="pill pill-strong">{{ item.badge }}</div>
          </div>
          <div class="card-note">{{ item.comment }}</div>
        </div>
        {% endfor %}
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Akıllı Piyasa Özeti</h2>
      <div class="summary-grid">
        <div class="summary-box">
          <div class="summary-title">Piyasa Özeti</div>

          {% for item in summary %}
          <div class="summary-row">
            <div class="summary-left">
              <div class="summary-name">{{ item.name }}</div>
              <div class="summary-desc">{{ item.desc }}</div>
            </div>
            <div class="summary-trend">{{ item.trend }}</div>
          </div>
          {% endfor %}

          <div class="footer-note">{{ insight }}</div>
          <div class="footer-note">Son güncelleme: {{ updated_at }}</div>
        </div>

        <div class="summary-box">
          <div class="summary-title">Genel Yorum</div>
          <div class="footer-note">{{ long_comment }}</div>
          <div class="footer-note">
            Bu sürümde BIST100, Brent Petrol ve Nasdaq ekranda canlı alan olarak hazırlandı.
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Global Veri</h2>
      <div class="global-grid">
        {% for item in global_data %}
        <div class="card">
          <div class="card-label">{{ item.name }}</div>
          <div class="card-price">{{ item.prefix }}{{ item.price }}</div>
          <div class="pill-row">
            <div class="pill {% if item.pct_value > 0 %}pill-up{% elif item.pct_value < 0 %}pill-down{% else %}pill-neutral{% endif %}">
              {{ item.pct_text }}
            </div>
            <div class="pill pill-strong">{{ item.signal }}</div>
          </div>
          <div class="card-note">{{ item.comment }}</div>
        </div>
        {% endfor %}
      </div>
    </div>
  </div>
</body>
</html>
"""

def format_tr_number(value, decimals=2):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "Yüklenemedi"
    formatted = f"{value:,.{decimals}f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")

def format_percent(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "% 0,00"
    sign = "+" if value > 0 else ""
    formatted = f"{value:.2f}".replace(".", ",")
    return f"{sign}% {formatted}"

def quote_from_ticker(symbol):
    t = yf.Ticker(symbol)

    current = None
    previous = None

    try:
        fi = t.fast_info
        current = fi.get("lastPrice")
        previous = fi.get("previousClose")
    except Exception:
        pass

    if current is None or previous is None:
        try:
            hist = t.history(period="5d", interval="1d", auto_adjust=False)
            if not hist.empty:
                current = float(hist["Close"].iloc[-1])
                if len(hist) >= 2:
                    previous = float(hist["Close"].iloc[-2])
                else:
                    previous = current
        except Exception:
            pass

    if current is None:
        return None

    if previous in (None, 0):
        pct = 0.0
    else:
        pct = ((current - previous) / previous) * 100

    return {
        "current": float(current),
        "previous": float(previous if previous is not None else current),
        "pct": float(pct),
    }

def signal_from_pct(pct):
    if pct >= 2:
        return "Güçlü"
    if pct > 0:
        return "Yukarı"
    if pct <= -2:
        return "Baskılı"
    if pct < 0:
        return "Aşağı"
    return "Dengeli"

def currency_comment(name, pct):
    signal = signal_from_pct(pct)
    if signal == "Güçlü":
        return f"{name} gün içinde güçlü pozitif bölgede."
    if signal == "Yukarı":
        return f"{name} hafif pozitif görünümde."
    if signal == "Baskılı":
        return f"{name} satış baskısı altında görünüyor."
    if signal == "Aşağı":
        return f"{name} zayıf bölgede fiyatlanıyor."
    return f"{name} dengeli seyrediyor."

def market_comment(name, pct):
    signal = signal_from_pct(pct)
    if signal == "Güçlü":
        return f"{name} güçlü yükseliş eğiliminde."
    if signal == "Yukarı":
        return f"{name} pozitif görünümde."
    if signal == "Baskılı":
        return f"{name} belirgin geri çekilme yaşıyor."
    if signal == "Aşağı":
        return f"{name} hafif negatif bölgede."
    return f"{name} yatay / dengeli görünümde."

def get_exchange_data():
    mapping = [
        ("USDTRY=X", "Dolar"),
        ("EURTRY=X", "Euro"),
        ("GBPTRY=X", "Sterlin"),
    ]

    items = []
    for symbol, name in mapping:
        q = quote_from_ticker(symbol)
        if q is None:
            price = None
            pct = 0.0
        else:
            price = q["current"]
            pct = q["pct"]

        items.append({
            "name": name,
            "currency_symbol": "₺",
            "price": format_tr_number(price, 2),
            "pct_value": pct,
            "pct_text": format_percent(pct),
            "signal": signal_from_pct(pct),
            "comment": currency_comment(name, pct),
            "raw_price": price or 0.0,
        })

    return items

def get_gold_data():
    gold = quote_from_ticker("GC=F")
    usdtry = quote_from_ticker("USDTRY=X")

    if gold is None or usdtry is None:
        gram = None
        gram_pct = 0.0
    else:
        # ons altın USD fiyatını gram/TL'ye yaklaşık çevirme
        gram = (gold["current"] * usdtry["current"]) / 31.1035
        gram_pct = gold["pct"] + usdtry["pct"]

    if gram is None:
        ceyrek = yarim = tam = None
    else:
        ceyrek = gram * 1.65
        yarim = ceyrek * 2
        tam = ceyrek * 4

    items = [
        {"name": "Gram Altın", "price": gram, "badge": "Canlı", "pct": gram_pct},
        {"name": "Çeyrek Altın", "price": ceyrek, "badge": "Tahmini", "pct": gram_pct},
        {"name": "Yarım Altın", "price": yarim, "badge": "Tahmini", "pct": gram_pct},
        {"name": "Tam Altın", "price": tam, "badge": "Tahmini", "pct": gram_pct},
    ]

    for item in items:
        item["pct_value"] = item["pct"]
        item["pct_text"] = format_percent(item["pct"])
        item["signal"] = signal_from_pct(item["pct"])
        item["comment"] = market_comment(item["name"], item["pct"])
        item["price"] = format_tr_number(item["price"], 2)
        item["raw_price"] = item["price"]

    return items

def get_global_data():
    mapping = [
        ("BTC-TRY", "Bitcoin", "₺ ", 0),
        ("XU100.IS", "BIST100", "", 2),
        ("BZ=F", "Brent Petrol", "$ ", 2),
        ("^IXIC", "Nasdaq", "", 2),
    ]

    items = []
    for symbol, name, prefix, decimals in mapping:
        q = quote_from_ticker(symbol)
        if q is None:
            current = None
            pct = 0.0
        else:
            current = q["current"]
            pct = q["pct"]

        items.append({
            "name": name,
            "prefix": prefix,
            "price": format_tr_number(current, decimals),
            "pct_value": pct,
            "pct_text": format_percent(pct),
            "signal": signal_from_pct(pct),
            "comment": market_comment(name, pct),
            "raw_price": current or 0.0,
        })

    return items

def build_summary(doviz, altin, global_data):
    return [
        {"name": "Dolar", "desc": f"Güncel seviye ₺ {doviz[0]['price']}", "trend": doviz[0]['signal']},
        {"name": "Euro", "desc": f"Güncel seviye ₺ {doviz[1]['price']}", "trend": doviz[1]['signal']},
        {"name": "Gram Altın", "desc": f"Referans fiyat ₺ {altin[0]['price']}", "trend": altin[0]['signal']},
        {"name": "BIST100", "desc": f"Güncel seviye {global_data[1]['price']}", "trend": global_data[1]['signal']},
    ]

def build_insight(doviz, altin, global_data):
    return (
        f"Dolar {doviz[0]['pct_text']}, Euro {doviz[1]['pct_text']} ve gram altın {altin[0]['pct_text']} "
        f"değişim gösteriyor. BIST100 tarafında son görünüm {global_data[1]['signal']}."
    )

def calculate_market_score(doviz, altin, global_data):
    all_pcts = [abs(x["pct_value"]) for x in doviz]
    all_pcts.append(abs(altin[0]["pct_value"]))
    all_pcts.extend(abs(x["pct_value"]) for x in global_data)

    avg_move = sum(all_pcts) / len(all_pcts) if all_pcts else 0
    score = min(100, int(avg_move * 18 + 30))
    return score

def get_market_score_note(score):
    if score >= 85:
        return "Piyasada oldukça yüksek hareketlilik var."
    if score >= 65:
        return "Piyasa aktif ve yakından izlenmeli."
    if score >= 45:
        return "Piyasa dengeli ama canlı."
    return "Piyasa daha sakin görünümde."

def get_top_asset(doviz, altin, global_data):
    candidates = [
        {"name": "Dolar", "pct": abs(doviz[0]["pct_value"]), "reason": doviz[0]["comment"]},
        {"name": "Gram Altın", "pct": abs(altin[0]["pct_value"]), "reason": altin[0]["comment"]},
        {"name": "Bitcoin", "pct": abs(global_data[0]["pct_value"]), "reason": global_data[0]["comment"]},
        {"name": "BIST100", "pct": abs(global_data[1]["pct_value"]), "reason": global_data[1]["comment"]},
        {"name": "Brent Petrol", "pct": abs(global_data[2]["pct_value"]), "reason": global_data[2]["comment"]},
        {"name": "Nasdaq", "pct": abs(global_data[3]["pct_value"]), "reason": global_data[3]["comment"]},
    ]
    return max(candidates, key=lambda x: x["pct"])

def build_long_comment(doviz, altin, global_data, market_score):
    return (
        f"Genel piyasa skoru {market_score}/100 seviyesinde. Döviz tarafında dolar ve euro izlenirken, "
        f"gram altın {altin[0]['pct_text']} değişimle dikkat çekiyor. Global tarafta Bitcoin, BIST100, "
        f"Brent petrol ve Nasdaq aynı ekranda takip edilebiliyor."
    )

@app.route("/")
def home():
    doviz = get_exchange_data()
    altin = get_gold_data()
    global_data = get_global_data()
    summary = build_summary(doviz, altin, global_data)
    insight = build_insight(doviz, altin, global_data)
    updated_at = datetime.now().strftime("%d.%m.%Y %H:%M")
    market_score = calculate_market_score(doviz, altin, global_data)
    market_score_note = get_market_score_note(market_score)
    top_asset = get_top_asset(doviz, altin, global_data)
    long_comment = build_long_comment(doviz, altin, global_data, market_score)

    return render_template_string(
        HTML,
        doviz=doviz,
        altin=altin,
        summary=summary,
        insight=insight,
        global_data=global_data,
        updated_at=updated_at,
        market_score=market_score,
        market_score_note=market_score_note,
        top_asset=top_asset,
        long_comment=long_comment
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)