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
      background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
      color: #e5e7eb;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 28px 20px 40px;
    }

    .hero {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 20px;
      margin-bottom: 24px;
      flex-wrap: wrap;
    }

    .title {
      font-size: 40px;
      font-weight: 800;
      margin: 0 0 8px;
      letter-spacing: -0.02em;
    }

    .subtitle {
      margin: 0;
      color: #94a3b8;
      font-size: 16px;
    }

    .status-box {
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 18px;
      padding: 16px 18px;
      min-width: 300px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }

    .status-label {
      color: #94a3b8;
      font-size: 13px;
      margin-bottom: 6px;
    }

    .status-value {
      font-size: 16px;
      font-weight: 700;
    }

    .note {
      color: #94a3b8;
      font-size: 13px;
      margin-top: 8px;
      line-height: 1.5;
    }

    .section {
      margin-top: 28px;
    }

    .section-title {
      font-size: 24px;
      font-weight: 800;
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
      font-weight: 800;
      margin-bottom: 10px;
      line-height: 1.2;
      word-break: break-word;
    }

    .change {
      display: inline-block;
      font-size: 14px;
      font-weight: 700;
      padding: 7px 10px;
      border-radius: 999px;
    }

    .up {
      background: rgba(34, 197, 94, 0.12);
      color: #4ade80;
    }

    .down {
      background: rgba(239, 68, 68, 0.12);
      color: #f87171;
    }

    .neutral {
      background: rgba(148, 163, 184, 0.12);
      color: #cbd5e1;
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
      font-weight: 800;
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
      font-weight: 700;
      margin-bottom: 4px;
    }

    .summary-desc {
      color: #94a3b8;
      font-size: 13px;
    }

    .summary-trend {
      font-weight: 800;
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
    }

    @media (max-width: 900px) {
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
      <div>
        <h1 class="title">Piyasa Takip 🚀</h1>
        <p class="subtitle">Döviz, altın ve akıllı piyasa verilerini tek ekranda takip edin.</p>
      </div>
      <div class="status-box">
        <div class="status-label">Durum</div>
        <div class="status-value">Canlı döviz, altın ve Bitcoin aktif</div>
        <div class="note">Sayfa 60 saniyede bir otomatik yenilenir. Çeyrek / yarım / tam altın gram altından tahmini türetilir.</div>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Döviz</h2>
      <div class="grid">
        {% for item in doviz %}
        <div class="card">
          <div class="card-label">{{ item.name }}</div>
          <div class="card-price">₺ {{ item.price }}</div>
          <div class="change {% if item.change > 0 %}up{% elif item.change < 0 %}down{% else %}neutral{% endif %}">
            {% if item.change > 0 %}+{% endif %}{{ item.change }}
          </div>
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
          <div class="change neutral">{{ item.badge }}</div>
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
          <div class="summary-title">Global Yorum</div>
          <div class="footer-note">
            Bitcoin artık canlı gösteriliyor. Brent petrol ve Nasdaq alanları şimdilik yer tutucu olarak bırakıldı.
          </div>
          <div class="footer-note">
            İstersen bir sonraki adımda Brent petrol ve Nasdaq da canlı hale getirilebilir.
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
          <div class="change neutral">{{ item.note }}</div>
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

def get_try_rates():
    url = "https://open.er-api.com/v6/latest/TRY"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    rates = data["rates"]

    usd_try = round(1 / rates["USD"], 2)
    eur_try = round(1 / rates["EUR"], 2)
    gbp_try = round(1 / rates["GBP"], 2)
    pln_try = round(1 / rates["PLN"], 4)

    return usd_try, eur_try, gbp_try, pln_try

def get_exchange_data():
    usd_try, eur_try, gbp_try, _ = get_try_rates()

    return [
        {"name": "Dolar", "price": usd_try, "change": 0.12},
        {"name": "Euro", "price": eur_try, "change": -0.08},
        {"name": "Sterlin", "price": gbp_try, "change": 0.25},
    ]

def get_gold_data():
    _, _, _, pln_try = get_try_rates()

    gold_url = "https://api.nbp.pl/api/cenyzlota?format=json"
    gold_response = requests.get(gold_url, timeout=10)
    gold_response.raise_for_status()
    gold_json = gold_response.json()

    gold_pln_per_gram = gold_json[-1]["cena"]
    gram_altin = round(gold_pln_per_gram * pln_try, 2)

    ceyrek = round(gram_altin * 1.65, 2)
    yarim = round(ceyrek * 2, 2)
    tam = round(ceyrek * 4, 2)

    return [
        {"name": "Gram Altın", "price": gram_altin, "badge": "Canlı"},
        {"name": "Çeyrek Altın", "price": ceyrek, "badge": "Tahmini"},
        {"name": "Yarım Altın", "price": yarim, "badge": "Tahmini"},
        {"name": "Tam Altın", "price": tam, "badge": "Tahmini"},
    ]

def get_bitcoin_try():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=try"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        btc_try = data["bitcoin"]["try"]
        return f"₺ {safe_round(btc_try, 0):,.0f}".replace(",", ".")
    except Exception:
        return "Yüklenemedi"

def get_global_data():
    return [
        {"name": "Bitcoin", "value": get_bitcoin_try(), "note": "Canlı"},
        {"name": "Brent Petrol", "value": "Yakında", "note": "Hazırlanıyor"},
        {"name": "Nasdaq", "value": "Yakında", "note": "Hazırlanıyor"},
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

@app.route("/")
def home():
    doviz = get_exchange_data()
    altin = get_gold_data()
    global_data = get_global_data()
    summary = build_summary(doviz, altin)
    insight = build_insight(doviz, altin, global_data)
    updated_at = datetime.now().strftime("%d.%m.%Y %H:%M")

    return render_template_string(
        HTML,
        doviz=doviz,
        altin=altin,
        summary=summary,
        insight=insight,
        global_data=global_data,
        updated_at=updated_at
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)