from flask import Flask, render_template_string
from datetime import datetime
from zoneinfo import ZoneInfo
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
    :root {
      --bg1: #0b1220;
      --bg2: #111827;
      --text: #e5e7eb;
      --muted: #94a3b8;
      --card: rgba(255,255,255,0.05);
      --card-border: rgba(255,255,255,0.08);
      --soft: rgba(255,255,255,0.03);
      --shadow: 0 12px 30px rgba(0,0,0,0.22);
      --green-bg: rgba(34, 197, 94, 0.12);
      --green: #4ade80;
      --red-bg: rgba(239, 68, 68, 0.12);
      --red: #f87171;
      --gray-bg: rgba(148, 163, 184, 0.12);
      --gray: #cbd5e1;
      --purple-bg: rgba(168, 85, 247, 0.14);
      --purple: #d8b4fe;
      --accent: #facc15;
      --accent-soft: rgba(250, 204, 21, 0.16);
    }

    body.light-theme {
      --bg1: #f8fafc;
      --bg2: #e2e8f0;
      --text: #0f172a;
      --muted: #475569;
      --card: rgba(255,255,255,0.78);
      --card-border: rgba(15,23,42,0.08);
      --soft: rgba(15,23,42,0.04);
      --shadow: 0 10px 22px rgba(15,23,42,0.08);
      --green-bg: rgba(22, 163, 74, 0.10);
      --green: #15803d;
      --red-bg: rgba(220, 38, 38, 0.10);
      --red: #b91c1c;
      --gray-bg: rgba(100, 116, 139, 0.12);
      --gray: #334155;
      --purple-bg: rgba(147, 51, 234, 0.10);
      --purple: #7e22ce;
      --accent: #ca8a04;
      --accent-soft: rgba(202, 138, 4, 0.15);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: Inter, Arial, sans-serif;
      background: linear-gradient(180deg, var(--bg1) 0%, var(--bg2) 100%);
      color: var(--text);
      transition: background 0.25s ease, color 0.25s ease;
    }

    .container {
      max-width: 1280px;
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

    .title-row {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    .title {
      font-size: 42px;
      font-weight: 900;
      margin: 0;
      letter-spacing: -0.03em;
    }

    .signature {
      color: var(--muted);
      font-size: 14px;
      margin-top: 6px;
      margin-bottom: 8px;
    }

    .subtitle {
      margin: 0;
      color: var(--muted);
      font-size: 16px;
      line-height: 1.5;
    }

    .theme-btn {
      border: 1px solid var(--card-border);
      background: var(--card);
      color: var(--text);
      border-radius: 999px;
      padding: 10px 14px;
      cursor: pointer;
      font-weight: 800;
      box-shadow: var(--shadow);
    }

    .hero-right {
      display: grid;
      grid-template-columns: repeat(2, minmax(230px, 1fr));
      gap: 16px;
      flex: 1;
      min-width: 320px;
    }

    .top-box {
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 18px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(8px);
    }

    .top-label {
      color: var(--muted);
      font-size: 13px;
      margin-bottom: 8px;
    }

    .top-value {
      font-size: 18px;
      font-weight: 800;
      line-height: 1.4;
    }

    .top-sub {
      margin-top: 8px;
      font-size: 13px;
      color: var(--muted);
      line-height: 1.5;
    }

    .section {
      margin-top: 30px;
    }

    .section-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 14px;
    }

    .section-title {
      font-size: 24px;
      font-weight: 900;
      margin: 0;
    }

    .helper-text {
      color: var(--muted);
      font-size: 13px;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
      gap: 16px;
    }

    .card {
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 18px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(8px);
      position: relative;
    }

    .favorite-btn {
      position: absolute;
      top: 14px;
      right: 14px;
      border: 0;
      background: transparent;
      color: var(--muted);
      font-size: 22px;
      cursor: pointer;
      line-height: 1;
      transition: transform 0.15s ease, color 0.15s ease;
    }

    .favorite-btn:hover {
      transform: scale(1.08);
    }

    .favorite-btn.active {
      color: var(--accent);
      text-shadow: 0 0 12px var(--accent-soft);
    }

    .card-label {
      color: var(--muted);
      font-size: 14px;
      margin-bottom: 10px;
      padding-right: 32px;
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
      margin-bottom: 12px;
    }

    .pill {
      display: inline-block;
      font-size: 13px;
      font-weight: 800;
      padding: 7px 10px;
      border-radius: 999px;
    }

    .pill-up {
      background: var(--green-bg);
      color: var(--green);
    }

    .pill-down {
      background: var(--red-bg);
      color: var(--red);
    }

    .pill-neutral {
      background: var(--gray-bg);
      color: var(--gray);
    }

    .pill-strong {
      background: var(--purple-bg);
      color: var(--purple);
    }

    .chart-box {
      margin-top: 10px;
      margin-bottom: 10px;
      height: 70px;
      background: var(--soft);
      border-radius: 14px;
      padding: 6px;
      overflow: hidden;
    }

    .chart-box svg {
      width: 100%;
      height: 58px;
      display: block;
    }

    .card-note {
      margin-top: 10px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
    }

    .summary-grid {
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 16px;
    }

    .summary-box {
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 18px;
      box-shadow: var(--shadow);
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
      border-bottom: 1px solid var(--card-border);
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
      color: var(--muted);
      font-size: 13px;
    }

    .summary-trend {
      font-weight: 900;
      font-size: 22px;
      line-height: 1;
      min-width: 28px;
      text-align: center;
    }

    .trend-up {
      color: var(--green);
    }

    .trend-down {
      color: var(--red);
    }

    .trend-neutral {
      color: var(--gray);
    }

    .global-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
      gap: 16px;
    }

    .footer-note {
      margin-top: 14px;
      font-size: 13px;
      color: var(--muted);
      line-height: 1.6;
    }

    .toolbar {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
    }

    .tool-card {
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 18px;
      box-shadow: var(--shadow);
    }

    .alarm-grid {
      display: grid;
      grid-template-columns: 1fr 140px 160px 120px;
      gap: 10px;
      margin-top: 12px;
    }

    .input, .select, .button {
      width: 100%;
      border: 1px solid var(--card-border);
      background: var(--soft);
      color: var(--text);
      border-radius: 12px;
      padding: 12px 12px;
      font-size: 14px;
    }

    .button {
      cursor: pointer;
      font-weight: 800;
      background: var(--card);
    }

    .button.primary {
      background: var(--accent-soft);
      border-color: rgba(250, 204, 21, 0.18);
      color: var(--accent);
    }

    .alarm-list {
      display: grid;
      gap: 10px;
      margin-top: 14px;
    }

    .alarm-item {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      padding: 12px 14px;
      border-radius: 14px;
      background: var(--soft);
      border: 1px solid var(--card-border);
    }

    .alarm-left {
      flex: 1;
    }

    .alarm-title {
      font-weight: 800;
      margin-bottom: 4px;
    }

    .alarm-desc {
      color: var(--muted);
      font-size: 13px;
    }

    .alarm-actions {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .tiny-btn {
      border: 1px solid var(--card-border);
      background: transparent;
      color: var(--muted);
      border-radius: 10px;
      padding: 8px 10px;
      cursor: pointer;
      font-size: 13px;
      font-weight: 700;
    }

    .favorites-empty {
      color: var(--muted);
      font-size: 14px;
      padding: 14px 0;
    }

    @media (max-width: 980px) {
      .hero-right,
      .summary-grid,
      .alarm-grid {
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
        <div class="title-row">
          <h1 class="title">Piyasa Takip 🚀</h1>
          <button id="themeToggle" class="theme-btn">🌗 Tema</button>
        </div>
        <div class="signature">by Yiğit</div>
        <p class="subtitle">Döviz, altın ve önemli piyasa verilerini tek ekranda takip edin.</p>
      </div>

      <div class="hero-right">
        <div class="top-box">
          <div class="top-label">Durum</div>
          <div class="top-value">Canlı piyasa verileri, mini grafikler ve alarmlar aktif</div>
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
          <div class="top-label">Türkiye Saati</div>
          <div class="top-value" id="liveClock">{{ updated_at }}</div>
          <div class="top-sub">Europe/Istanbul saat dilimi kullanılır.</div>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-head">
        <h2 class="section-title">Favoriler ⭐</h2>
        <div class="helper-text">Yıldızladığın varlıklar burada görünür.</div>
      </div>
      <div id="favoritesGrid" class="grid"></div>
      <div id="favoritesEmpty" class="favorites-empty">Henüz favori seçmedin.</div>
    </div>

    <div class="section">
      <div class="section-head">
        <h2 class="section-title">Alarm Sistemi 🚨</h2>
        <div class="helper-text">Belirlediğin seviyeye gelince tarayıcı bildirimi ve uyarı üretir.</div>
      </div>
      <div class="tool-card">
        <div class="alarm-grid">
          <select id="alarmAsset" class="select"></select>
          <select id="alarmCondition" class="select">
            <option value="above">Üstüne çıkınca</option>
            <option value="below">Altına inince</option>
          </select>
          <input id="alarmThreshold" class="input" type="number" step="0.01" placeholder="Seviye gir">
          <button id="addAlarmBtn" class="button primary">Alarm Ekle</button>
        </div>

        <div class="toolbar" style="margin-top: 12px;">
          <button id="enableNotificationsBtn" class="button">Bildirim İzni Ver</button>
          <div class="helper-text">Tarayıcı bildirimleri için bir kez izin vermen gerekir.</div>
        </div>

        <div id="alarmList" class="alarm-list"></div>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Döviz</h2>
      <div class="grid">
        {% for item in doviz %}
        <div class="card asset-card"
             data-key="{{ item.key }}"
             data-name="{{ item.name }}"
             data-price="{{ item.raw_price }}"
             data-display-price="{{ item.currency_symbol }} {{ item.price }}"
             data-pct="{{ item.pct_text }}">
          <button class="favorite-btn" data-fav-key="{{ item.key }}" title="Favorilere ekle">☆</button>
          <div class="card-label">{{ item.name }}</div>
          <div class="card-price">{{ item.currency_symbol }} {{ item.price }}</div>
          <div class="pill-row">
            <div class="pill {% if item.pct_value > 0 %}pill-up{% elif item.pct_value < 0 %}pill-down{% else %}pill-neutral{% endif %}">
              {{ item.pct_text }}
            </div>
            <div class="pill pill-neutral">{{ item.signal }}</div>
          </div>
          <div class="chart-box">{{ item.chart|safe }}</div>
          <div class="card-note">{{ item.comment }}</div>
        </div>
        {% endfor %}
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Altın</h2>
      <div class="grid">
        {% for item in altin %}
        <div class="card asset-card"
             data-key="{{ item.key }}"
             data-name="{{ item.name }}"
             data-price="{{ item.raw_price }}"
             data-display-price="₺ {{ item.price }}"
             data-pct="{{ item.pct_text }}">
          <button class="favorite-btn" data-fav-key="{{ item.key }}" title="Favorilere ekle">☆</button>
          <div class="card-label">{{ item.name }}</div>
          <div class="card-price">₺ {{ item.price }}</div>
          <div class="pill-row">
            <div class="pill {% if item.pct_value > 0 %}pill-up{% elif item.pct_value < 0 %}pill-down{% else %}pill-neutral{% endif %}">
              {{ item.pct_text }}
            </div>
            <div class="pill pill-strong">{{ item.badge }}</div>
          </div>
          <div class="chart-box">{{ item.chart|safe }}</div>
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
            <div class="summary-trend">
              {% if item.trend in ["Yukarı", "Güçlü", "Takipte"] %}
                <span class="trend-up">▲</span>
              {% elif item.trend in ["Aşağı", "Baskılı"] %}
                <span class="trend-down">▼</span>
              {% else %}
                <span class="trend-neutral">•</span>
              {% endif %}
            </div>
          </div>
          {% endfor %}

          <div class="footer-note">{{ insight }}</div>
          <div class="footer-note">Son sunucu güncellemesi: {{ updated_at }}</div>
        </div>

        <div class="summary-box">
          <div class="summary-title">Genel Yorum</div>
          <div class="footer-note">{{ long_comment }}</div>
          <div class="footer-note">
            Bu sürümde BIST100, Brent Petrol ve Nasdaq canlı olarak izlenir. Mini grafikler kısa dönem hareketini gösterir.
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Global Veri</h2>
      <div class="global-grid">
        {% for item in global_data %}
        <div class="card asset-card"
             data-key="{{ item.key }}"
             data-name="{{ item.name }}"
             data-price="{{ item.raw_price }}"
             data-display-price="{{ item.prefix }}{{ item.price }}"
             data-pct="{{ item.pct_text }}">
          <button class="favorite-btn" data-fav-key="{{ item.key }}" title="Favorilere ekle">☆</button>
          <div class="card-label">{{ item.name }}</div>
          <div class="card-price">{{ item.prefix }}{{ item.price }}</div>
          <div class="pill-row">
            <div class="pill {% if item.pct_value > 0 %}pill-up{% elif item.pct_value < 0 %}pill-down{% else %}pill-neutral{% endif %}">
              {{ item.pct_text }}
            </div>
            <div class="pill pill-strong">{{ item.signal }}</div>
          </div>
          <div class="chart-box">{{ item.chart|safe }}</div>
          <div class="card-note">{{ item.comment }}</div>
        </div>
        {% endfor %}
      </div>
    </div>
  </div>

  <script>
    const ALL_ASSETS = {{ all_assets | tojson }};
    const FAVORITES_KEY = "piyasa_takip_favorites";
    const ALARMS_KEY = "piyasa_takip_alarms";
    const THEME_KEY = "piyasa_takip_theme";

    function getFavorites() {
      try {
        return JSON.parse(localStorage.getItem(FAVORITES_KEY)) || [];
      } catch {
        return [];
      }
    }

    function saveFavorites(items) {
      localStorage.setItem(FAVORITES_KEY, JSON.stringify(items));
    }

    function getAlarms() {
      try {
        return JSON.parse(localStorage.getItem(ALARMS_KEY)) || [];
      } catch {
        return [];
      }
    }

    function saveAlarms(items) {
      localStorage.setItem(ALARMS_KEY, JSON.stringify(items));
    }

    function getAssetMap() {
      const map = {};
      ALL_ASSETS.forEach(item => {
        map[item.key] = item;
      });
      return map;
    }

    function updateFavoriteButtons() {
      const favorites = getFavorites();
      document.querySelectorAll(".favorite-btn").forEach(btn => {
        const key = btn.dataset.favKey;
        const active = favorites.includes(key);
        btn.textContent = active ? "★" : "☆";
        btn.classList.toggle("active", active);
      });
    }

    function renderFavorites() {
      const favorites = getFavorites();
      const assetMap = getAssetMap();
      const grid = document.getElementById("favoritesGrid");
      const empty = document.getElementById("favoritesEmpty");

      grid.innerHTML = "";

      const selected = favorites
        .map(key => assetMap[key])
        .filter(Boolean);

      if (!selected.length) {
        empty.style.display = "block";
        grid.style.display = "none";
        return;
      }

      empty.style.display = "none";
      grid.style.display = "grid";

      selected.forEach(item => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
          <div class="card-label">${item.name}</div>
          <div class="card-price">${item.display_price}</div>
          <div class="pill-row">
            <div class="pill ${item.pct_value > 0 ? "pill-up" : item.pct_value < 0 ? "pill-down" : "pill-neutral"}">${item.pct_text}</div>
            <div class="pill pill-neutral">Favori</div>
          </div>
          <div class="card-note">Bu varlık favori listende tutuluyor.</div>
        `;
        grid.appendChild(card);
      });
    }

    function setupFavorites() {
      document.querySelectorAll(".favorite-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          const key = btn.dataset.favKey;
          let favorites = getFavorites();

          if (favorites.includes(key)) {
            favorites = favorites.filter(x => x !== key);
          } else {
            favorites.push(key);
          }

          saveFavorites(favorites);
          updateFavoriteButtons();
          renderFavorites();
        });
      });

      updateFavoriteButtons();
      renderFavorites();
    }

    function populateAlarmAssets() {
      const select = document.getElementById("alarmAsset");
      select.innerHTML = "";
      ALL_ASSETS.forEach(asset => {
        const option = document.createElement("option");
        option.value = asset.key;
        option.textContent = asset.name;
        select.appendChild(option);
      });
    }

    function renderAlarms() {
      const alarms = getAlarms();
      const assetMap = getAssetMap();
      const list = document.getElementById("alarmList");
      list.innerHTML = "";

      if (!alarms.length) {
        list.innerHTML = `<div class="favorites-empty">Henüz alarm eklemedin.</div>`;
        return;
      }

      alarms.forEach(alarm => {
        const asset = assetMap[alarm.assetKey];
        const currentPrice = asset ? asset.raw_price : null;
        const item = document.createElement("div");
        item.className = "alarm-item";
        item.innerHTML = `
          <div class="alarm-left">
            <div class="alarm-title">${alarm.assetName}</div>
            <div class="alarm-desc">
              ${alarm.condition === "above" ? "Üstüne çıkınca" : "Altına inince"}: ${alarm.threshold}
              ${currentPrice !== null ? ` • Güncel: ${currentPrice.toFixed(2)}` : ""}
              ${alarm.triggered ? " • Tetiklendi" : ""}
            </div>
          </div>
          <div class="alarm-actions">
            <button class="tiny-btn" data-reset-id="${alarm.id}">Sıfırla</button>
            <button class="tiny-btn" data-delete-id="${alarm.id}">Sil</button>
          </div>
        `;
        list.appendChild(item);
      });

      list.querySelectorAll("[data-delete-id]").forEach(btn => {
        btn.addEventListener("click", () => {
          const id = btn.dataset.deleteId;
          const alarms = getAlarms().filter(a => a.id !== id);
          saveAlarms(alarms);
          renderAlarms();
        });
      });

      list.querySelectorAll("[data-reset-id]").forEach(btn => {
        btn.addEventListener("click", () => {
          const id = btn.dataset.resetId;
          const alarms = getAlarms().map(a => a.id === id ? { ...a, triggered: false } : a);
          saveAlarms(alarms);
          renderAlarms();
        });
      });
    }

    function addAlarm() {
      const assetKey = document.getElementById("alarmAsset").value;
      const condition = document.getElementById("alarmCondition").value;
      const threshold = parseFloat(document.getElementById("alarmThreshold").value);
      const assetMap = getAssetMap();
      const asset = assetMap[assetKey];

      if (!asset || Number.isNaN(threshold)) {
        alert("Lütfen geçerli bir alarm oluştur.");
        return;
      }

      const alarms = getAlarms();
      alarms.push({
        id: String(Date.now()),
        assetKey,
        assetName: asset.name,
        condition,
        threshold,
        triggered: false
      });

      saveAlarms(alarms);
      document.getElementById("alarmThreshold").value = "";
      renderAlarms();
      checkAlarms();
    }

    function showBrowserNotification(title, body) {
      if (!("Notification" in window)) return;
      if (Notification.permission === "granted") {
        new Notification(title, { body });
      }
    }

    function checkAlarms() {
      const alarms = getAlarms();
      const assetMap = getAssetMap();
      let changed = false;

      const updated = alarms.map(alarm => {
        const asset = assetMap[alarm.assetKey];
        if (!asset) return alarm;
        if (alarm.triggered) return alarm;

        const current = asset.raw_price;
        let shouldTrigger = false;

        if (alarm.condition === "above" && current >= alarm.threshold) {
          shouldTrigger = true;
        }
        if (alarm.condition === "below" && current <= alarm.threshold) {
          shouldTrigger = true;
        }

        if (shouldTrigger) {
          changed = true;
          const message = `${alarm.assetName} için alarm tetiklendi. Güncel değer: ${current.toFixed(2)}`;
          showBrowserNotification("Piyasa Takip Alarmı", message);
          alert(message);
          return { ...alarm, triggered: true };
        }

        return alarm;
      });

      if (changed) {
        saveAlarms(updated);
        renderAlarms();
      }
    }

    function setupAlarms() {
      populateAlarmAssets();
      renderAlarms();
      document.getElementById("addAlarmBtn").addEventListener("click", addAlarm);
      document.getElementById("enableNotificationsBtn").addEventListener("click", async () => {
        if ("Notification" in window) {
          await Notification.requestPermission();
          alert("Bildirim izni durumu: " + Notification.permission);
        } else {
          alert("Tarayıcın bildirim desteklemiyor.");
        }
      });
      checkAlarms();
    }

    function applyTheme(theme) {
      document.body.classList.toggle("light-theme", theme === "light");
    }

    function setupTheme() {
      const savedTheme = localStorage.getItem(THEME_KEY) || "dark";
      applyTheme(savedTheme);

      document.getElementById("themeToggle").addEventListener("click", () => {
        const current = localStorage.getItem(THEME_KEY) || "dark";
        const next = current === "dark" ? "light" : "dark";
        localStorage.setItem(THEME_KEY, next);
        applyTheme(next);
      });
    }

    function setupClock() {
      const clock = document.getElementById("liveClock");

      function updateClock() {
        const now = new Date();
        const formatted = new Intl.DateTimeFormat("tr-TR", {
          timeZone: "Europe/Istanbul",
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit"
        }).format(now);
        clock.textContent = formatted;
      }

      updateClock();
      setInterval(updateClock, 1000);
    }

    setupTheme();
    setupFavorites();
    setupAlarms();
    setupClock();
  </script>
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

def quote_and_history_from_ticker(symbol, period="7d", interval="1d"):
    t = yf.Ticker(symbol)

    current = None
    previous = None
    history_points = []

    try:
        fi = t.fast_info
        current = fi.get("lastPrice")
        previous = fi.get("previousClose")
    except Exception:
        pass

    try:
        hist = t.history(period=period, interval=interval, auto_adjust=False)
        if not hist.empty:
            history_points = [float(x) for x in hist["Close"].tolist() if not math.isnan(float(x))]
            if current is None:
                current = float(hist["Close"].iloc[-1])
            if previous is None:
                if len(hist) >= 2:
                    previous = float(hist["Close"].iloc[-2])
                else:
                    previous = float(hist["Close"].iloc[-1])
    except Exception:
        pass

    if current is None:
        return None

    if previous in (None, 0):
        pct = 0.0
    else:
        pct = ((current - previous) / previous) * 100

    if not history_points:
        history_points = [float(current), float(current)]

    return {
        "current": float(current),
        "previous": float(previous if previous is not None else current),
        "pct": float(pct),
        "history": history_points,
    }

def build_sparkline_svg(points):
    if not points or len(points) < 2:
        points = [1, 1]

    width = 240
    height = 58
    padding = 4

    min_v = min(points)
    max_v = max(points)

    if max_v == min_v:
        max_v += 1

    coords = []
    for i, val in enumerate(points):
        x = padding + (i * (width - padding * 2) / (len(points) - 1))
        y = padding + ((max_v - val) * (height - padding * 2) / (max_v - min_v))
        coords.append((x, y))

    polyline = " ".join([f"{x:.1f},{y:.1f}" for x, y in coords])
    line_color = "#4ade80" if points[-1] >= points[0] else "#f87171"

    return f'''
    <svg viewBox="0 0 {width} {height}" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
      <polyline
        fill="none"
        stroke="{line_color}"
        stroke-width="3"
        stroke-linecap="round"
        stroke-linejoin="round"
        points="{polyline}"
      />
    </svg>
    '''

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
        ("USDTRY=X", "Dolar", "usdtry"),
        ("EURTRY=X", "Euro", "eurtry"),
        ("GBPTRY=X", "Sterlin", "gbptry"),
    ]

    items = []
    for symbol, name, key in mapping:
        q = quote_and_history_from_ticker(symbol)
        if q is None:
            price = None
            pct = 0.0
            chart = build_sparkline_svg([1, 1])
        else:
            price = q["current"]
            pct = q["pct"]
            chart = build_sparkline_svg(q["history"])

        items.append({
            "key": key,
            "name": name,
            "currency_symbol": "₺",
            "price": format_tr_number(price, 2),
            "pct_value": pct,
            "pct_text": format_percent(pct),
            "signal": signal_from_pct(pct),
            "comment": currency_comment(name, pct),
            "raw_price": float(price or 0.0),
            "chart": chart,
            "display_price": f"₺ {format_tr_number(price, 2)}",
        })

    return items

def get_gold_data():
    gold = quote_and_history_from_ticker("GC=F", period="1mo", interval="1d")
    usdtry = quote_and_history_from_ticker("USDTRY=X", period="1mo", interval="1d")

    if gold is None or usdtry is None:
        gram = None
        gram_pct = 0.0
        gram_history = [1, 1]
    else:
        gram = (gold["current"] * usdtry["current"]) / 31.1035
        gram_pct = gold["pct"] + usdtry["pct"]

        min_len = min(len(gold["history"]), len(usdtry["history"]))
        gram_history = []
        for i in range(min_len):
            gram_history.append((gold["history"][-min_len + i] * usdtry["history"][-min_len + i]) / 31.1035)

        if len(gram_history) < 2:
            gram_history = [gram, gram]

    if gram is None:
        ceyrek = yarim = tam = None
    else:
        ceyrek = gram * 1.65
        yarim = ceyrek * 2
        tam = ceyrek * 4

    items = [
        {"key": "gram_altin", "name": "Gram Altın", "price": gram, "badge": "Canlı", "pct": gram_pct, "history": gram_history},
        {"key": "ceyrek_altin", "name": "Çeyrek Altın", "price": ceyrek, "badge": "Tahmini", "pct": gram_pct, "history": [x * 1.65 for x in gram_history]},
        {"key": "yarim_altin", "name": "Yarım Altın", "price": yarim, "badge": "Tahmini", "pct": gram_pct, "history": [x * 3.3 for x in gram_history]},
        {"key": "tam_altin", "name": "Tam Altın", "price": tam, "badge": "Tahmini", "pct": gram_pct, "history": [x * 6.6 for x in gram_history]},
    ]

    for item in items:
        raw_price = float(item["price"] or 0.0) if item["price"] is not None else 0.0
        item["pct_value"] = item["pct"]
        item["pct_text"] = format_percent(item["pct"])
        item["signal"] = signal_from_pct(item["pct"])
        item["comment"] = market_comment(item["name"], item["pct"])
        item["price"] = format_tr_number(item["price"], 2)
        item["chart"] = build_sparkline_svg(item["history"])
        item["raw_price"] = raw_price
        item["display_price"] = f"₺ {item['price']}"

    return items

def get_global_data():
    mapping = [
        ("BTC-USD", "Bitcoin", "bitcoin", "$ ", 0),
        ("XU100.IS", "BIST100", "bist100", "", 2),
        ("BZ=F", "Brent Petrol", "brent", "$ ", 2),
        ("^IXIC", "Nasdaq", "nasdaq", "", 2),
    ]

    items = []
    for symbol, name, key, prefix, decimals in mapping:
        q = quote_and_history_from_ticker(symbol, period="1mo", interval="1d")
        if q is None:
            current = None
            pct = 0.0
            chart = build_sparkline_svg([1, 1])
        else:
            current = q["current"]
            pct = q["pct"]
            chart = build_sparkline_svg(q["history"])

        formatted_price = format_tr_number(current, decimals)
        items.append({
            "key": key,
            "name": name,
            "prefix": prefix,
            "price": formatted_price,
            "pct_value": pct,
            "pct_text": format_percent(pct),
            "signal": signal_from_pct(pct),
            "comment": market_comment(name, pct),
            "raw_price": float(current or 0.0),
            "chart": chart,
            "display_price": f"{prefix}{formatted_price}",
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
    return min(100, int(avg_move * 18 + 30))

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
        f"Brent petrol ve Nasdaq aynı ekranda yüzdesel değişimlerle takip edilebiliyor."
    )

@app.route("/")
def home():
    doviz = get_exchange_data()
    altin = get_gold_data()
    global_data = get_global_data()
    summary = build_summary(doviz, altin, global_data)
    insight = build_insight(doviz, altin, global_data)
    updated_at = datetime.now(ZoneInfo("Europe/Istanbul")).strftime("%d.%m.%Y %H:%M:%S")
    market_score = calculate_market_score(doviz, altin, global_data)
    market_score_note = get_market_score_note(market_score)
    top_asset = get_top_asset(doviz, altin, global_data)
    long_comment = build_long_comment(doviz, altin, global_data, market_score)

    all_assets = []
    for item in doviz:
        all_assets.append({
            "key": item["key"],
            "name": item["name"],
            "raw_price": item["raw_price"],
            "display_price": item["display_price"],
            "pct_value": item["pct_value"],
            "pct_text": item["pct_text"],
        })
    for item in altin:
        all_assets.append({
            "key": item["key"],
            "name": item["name"],
            "raw_price": item["raw_price"],
            "display_price": item["display_price"],
            "pct_value": item["pct_value"],
            "pct_text": item["pct_text"],
        })
    for item in global_data:
        all_assets.append({
            "key": item["key"],
            "name": item["name"],
            "raw_price": item["raw_price"],
            "display_price": item["display_price"],
            "pct_value": item["pct_value"],
            "pct_text": item["pct_text"],
        })

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
        long_comment=long_comment,
        all_assets=all_assets
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)