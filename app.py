from flask import Flask, render_template_string
from datetime import datetime
import requests

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
      max-width: 1220px;
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
        <p class="subtitle">Döviz, altın ve akıllı piyasa verilerini tek ekranda takip edin.</p>
      </div>

      <div class="hero-right">
        <div class="top-box">
          <div class="top-label">Durum</div>
          <div class="top-value">Canlı döviz, altın ve Bitcoin aktif</div>
          <div class="top-sub">Sayfa 60 saniyede bir otomatik yenilenir.</div>
        </div>

        <div class="top-box">
          <div class="top-label">Genel Piyasa Skoru</div>
          <div class="top-value">{{ market_score }}</div>
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
          <div class="card-price">₺ {{ item.price }}</div>
          <div class="pill-row">
            <div class="pill {% if item.change > 0 %}pill-up{% elif item.change < 0 %}pill-down{% else %}pill-neutral{% endif %}">
              {% if item.change > 0 %}+{% endif %}{{ item.change }}
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
            <div class="pill pill-neutral">{{ item.badge }}</div>
            <div class="pill pill-strong">{{ item.signal }}</div>
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
            Bu alanı daha sonra kişisel uyarılar, alarm sistemi ve favori listesi ile büyütebiliriz.
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
          <div class="card-price">{{ item.value }}</div>
          <div class="pill-row">
            <div class="pill pill-neutral">{{ item.note }}</div>
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

def safe_round(value, digits=2):
    try:
        return round(float(value), digits)
    except Exception:
        return value

def format_try(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_try_no_decimals(value):
    return f"{value:,.0f}".replace(",", ".")

def get_try_rates():
    url = "https://open.er-api.com/v6/latest/TRY"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()
    rates = data["rates"]

    usd_try = round(1 / rates["USD"], 2)
    eur_try = round(1 / rates["EUR"], 2)
    gbp_try = round(1 / rates["GBP"], 2)
    pln_try = round(1 / rates["PLN"], 4)

    return usd_try, eur_try, gbp_try, pln_try

def signal_for_currency(price, name):
    if name == "Dolar":
        if price >= 44:
            return "Yüksek"
        if price >= 40:
            return "Dengeli"
        return "Sakin"
    if name == "Euro":
        if price >= 50:
            return "Güçlü"
        if price >= 45:
            return "Dengeli"
        return "Sakin"
    if name == "Sterlin":
        if price >= 58:
            return "Güçlü"
        if price >= 54:
            return "Dengeli"
        return "Sakin"
    return "Takipte"

def comment_for_currency(price, name):
    signal = signal_for_currency(price, name)
    if signal == "Güçlü":
        return f"{name} yüksek bandın üst tarafında izleniyor."
    if signal == "Yüksek":
        return f"{name} dikkat çeken yüksek seviyelerde kalmaya devam ediyor."
    if signal == "Dengeli":
        return f"{name} güçlü ama daha dengeli bir bölgede."
    return f"{name} daha sakin bir görünüm sergiliyor."

def get_exchange_data():
    usd_try, eur_try, gbp_try, _ = get_try_rates()

    items = [
        {"name": "Dolar", "price": usd_try, "change": 0.12},
        {"name": "Euro", "price": eur_try, "change": -0.08},
        {"name": "Sterlin", "price": gbp_try, "change": 0.25},
    ]

    for item in items:
        item["signal"] = signal_for_currency(item["price"], item["name"])
        item["comment"] = comment_for_currency(item["price"], item["name"])
        item["price"] = format_try(item["price"])

    return items

def signal_for_gold(price, name):
    if name == "Gram Altın":
        if price >= 6500:
            return "Güçlü"
        if price >= 5000:
            return "Takipte"
        return "Sakin"
    return "Tahmini"

def comment_for_gold(name, signal):
    if signal == "Güçlü":
        return f"{name} güçlü ve dikkat çeken bir seviyede."
    if signal == "Takipte":
        return f"{name} yükseliş eğilimi açısından yakından izlenebilir."
    if signal == "Tahmini":
        return f"{name} gram altından türetilmiş yaklaşık değerdir."
    return f"{name} sakin görünümde."

def get_gold_data():
    _, _, _, pln_try = get_try_rates()

    gold_url = "https://api.nbp.pl/api/cenyzlota?format=json"
    gold_response = requests.get(gold_url, timeout=15)
    gold_response.raise_for_status()
    gold_json = gold_response.json()

    gold_pln_per_gram = gold_json[-1]["cena"]
    gram_altin = round(gold_pln_per_gram * pln_try, 2)

    ceyrek = round(gram_altin * 1.65, 2)
    yarim = round(ceyrek * 2, 2)
    tam = round(ceyrek * 4, 2)

    items = [
        {"name": "Gram Altın", "price": gram_altin, "badge": "Canlı"},
        {"name": "Çeyrek Altın", "price": ceyrek, "badge": "Tahmini"},
        {"name": "Yarım Altın", "price": yarim, "badge": "Tahmini"},
        {"name": "Tam Altın", "price": tam, "badge": "Tahmini"},
    ]

    for item in items:
        item["signal"] = signal_for_gold(item["price"], item["name"])
        item["comment"] = comment_for_gold(item["name"], item["signal"])
        item["price"] = format_try(item["price"])

    return items

def get_bitcoin_try():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=try"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        btc_try = data["bitcoin"]["try"]
        return btc_try
    except Exception:
        return None

def get_global_data():
    btc_try = get_bitcoin_try()

    if btc_try is not None:
        btc_value = f"₺ {format_try_no_decimals(btc_try)}"
        btc_signal = "Canlı"
        btc_comment = "Bitcoin güncel piyasa verisiyle gösteriliyor."
    else:
        btc_value = "Yüklenemedi"
        btc_signal = "Sorun"
        btc_comment = "Bitcoin verisi şu anda alınamadı."

    return [
        {"name": "Bitcoin", "value": btc_value, "note": "Canlı", "signal": btc_signal, "comment": btc_comment},
        {"name": "Brent Petrol", "value": "Yakında", "note": "Hazırlanıyor", "signal": "Sırada", "comment": "İleride canlı petrol verisi bağlanabilir."},
        {"name": "Nasdaq", "value": "Yakında", "note": "Hazırlanıyor", "signal": "Sırada", "comment": "İleride canlı Nasdaq verisi bağlanabilir."},
    ]

def build_summary(doviz, altin):
    return [
        {"name": "Dolar", "desc": f"Güncel seviye ₺ {doviz[0]['price']}", "trend": "Yukarı"},
        {"name": "Euro", "desc": f"Güncel seviye ₺ {doviz[1]['price']}", "trend": "Stabil"},
        {"name": "Sterlin", "desc": f"Güncel seviye ₺ {doviz[2]['price']}", "trend": "Güçlü"},
        {"name": "Gram Altın", "desc": f"Referans fiyat ₺ {altin[0]['price']}", "trend": "Takipte"},
    ]

def build_insight(doviz, altin, global_data):
    btc_value = global_data[0]["value"]
    return (
        f"Dolar ₺{doviz[0]['price']}, Euro ₺{doviz[1]['price']} ve gram altın ₺{altin[0]['price']} "
        f"seviyesinde izleniyor. Bitcoin tarafında güncel değer {btc_value}."
    )

def calculate_market_score(doviz, altin):
    # formatlı stringleri tekrar sayıya çevirelim
    def parse_tr(value):
        return float(value.replace(".", "").replace(",", "."))

    usd = parse_tr(doviz[0]["price"])
    eur = parse_tr(doviz[1]["price"])
    gram = parse_tr(altin[0]["price"])

    score = 0

    if usd >= 44:
        score += 35
    elif usd >= 40:
        score += 25
    else:
        score += 15

    if eur >= 50:
        score += 30
    elif eur >= 45:
        score += 20
    else:
        score += 10

    if gram >= 6500:
        score += 35
    elif gram >= 5000:
        score += 25
    else:
        score += 15

    return min(score, 100)

def get_market_score_note(score):
    if score >= 85:
        return "Piyasada güçlü ve yüksek seviye görünümü var."
    if score >= 65:
        return "Piyasa aktif ve dikkat isteyen bölgede."
    if score >= 45:
        return "Piyasa dengeli ama izlemeye değer."
    return "Piyasa daha sakin görünümde."

def get_top_asset(doviz, altin):
    gram = float(altin[0]["price"].replace(".", "").replace(",", "."))
    sterlin = float(doviz[2]["price"].replace(".", "").replace(",", "."))

    if gram >= 6500:
        return {"name": "Gram Altın", "reason": "Yüksek ve güçlü görünüm."}
    if sterlin >= 58:
        return {"name": "Sterlin", "reason": "Döviz tarafında öne çıkıyor."}
    return {"name": "Dolar", "reason": "Genel takipte ana referans."}

def build_long_comment(doviz, altin, global_data, market_score):
    return (
        f"Genel piyasa skoru {market_score}/100 seviyesinde. Döviz tarafında dolar ve sterlin güçlü görünürken, "
        f"altın tarafında gram altın dikkat çekici bir seviyede. Global tarafta Bitcoin canlı olarak izleniyor; "
        f"Brent petrol ve Nasdaq alanları bir sonraki sürüm için hazır bekliyor."
    )

@app.route("/")
def home():
    doviz = get_exchange_data()
    altin = get_gold_data()
    global_data = get_global_data()
    summary = build_summary(doviz, altin)
    insight = build_insight(doviz, altin, global_data)
    updated_at = datetime.now().strftime("%d.%m.%Y %H:%M")
    market_score = calculate_market_score(doviz, altin)
    market_score_note = get_market_score_note(market_score)
    top_asset = get_top_asset(doviz, altin)
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