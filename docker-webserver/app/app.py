from flask import Flask, jsonify, render_template_string
import os, datetime, platform

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>DockerWeb — Live</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg:       #0b0f1a;
      --surface:  #111827;
      --border:   #1f2d45;
      --accent:   #38bdf8;
      --accent2:  #818cf8;
      --green:    #34d399;
      --red:      #f87171;
      --text:     #e2e8f0;
      --muted:    #64748b;
      --mono:     'JetBrains Mono', monospace;
      --sans:     'Space Grotesk', sans-serif;
    }

    html { scroll-behavior: smooth; }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--sans);
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* ── Grid background ── */
    body::before {
      content: '';
      position: fixed; inset: 0;
      background-image:
        linear-gradient(rgba(56,189,248,.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56,189,248,.04) 1px, transparent 1px);
      background-size: 40px 40px;
      pointer-events: none;
      z-index: 0;
    }

    /* ── Glow orbs ── */
    .orb {
      position: fixed;
      border-radius: 50%;
      filter: blur(120px);
      pointer-events: none;
      z-index: 0;
    }
    .orb-1 { width: 500px; height: 500px; background: rgba(56,189,248,.07); top: -150px; left: -150px; }
    .orb-2 { width: 400px; height: 400px; background: rgba(129,140,248,.06); bottom: -100px; right: -100px; }

    /* ── Layout ── */
    .page { position: relative; z-index: 1; max-width: 900px; margin: 0 auto; padding: 48px 24px 80px; }

    /* ── Nav bar ── */
    nav {
      display: flex; align-items: center; justify-content: space-between;
      margin-bottom: 72px;
    }
    .nav-logo {
      font-family: var(--mono);
      font-size: 13px;
      color: var(--accent);
      letter-spacing: .08em;
    }
    .nav-logo span { color: var(--muted); }
    .status-pill {
      display: flex; align-items: center; gap: 8px;
      background: rgba(52,211,153,.08);
      border: 1px solid rgba(52,211,153,.2);
      border-radius: 999px;
      padding: 6px 14px;
      font-family: var(--mono);
      font-size: 11px;
      color: var(--green);
      letter-spacing: .06em;
    }
    .dot {
      width: 7px; height: 7px; border-radius: 50%;
      background: var(--green);
      animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse {
      0%,100% { opacity: 1; transform: scale(1); }
      50%      { opacity: .4; transform: scale(.85); }
    }

    /* ── Hero ── */
    .hero { margin-bottom: 64px; }
    .eyebrow {
      font-family: var(--mono);
      font-size: 11px;
      letter-spacing: .16em;
      color: var(--accent);
      text-transform: uppercase;
      margin-bottom: 20px;
    }
    h1 {
      font-size: clamp(36px, 6vw, 64px);
      font-weight: 700;
      line-height: 1.05;
      letter-spacing: -.02em;
      margin-bottom: 20px;
    }
    h1 .dim { color: var(--muted); font-weight: 300; }
    .hero-sub {
      font-size: 17px;
      color: var(--muted);
      line-height: 1.65;
      max-width: 520px;
    }

    /* ── Terminal block ── */
    .terminal {
      background: #070b13;
      border: 1px solid var(--border);
      border-radius: 10px;
      overflow: hidden;
      margin-bottom: 48px;
      box-shadow: 0 24px 60px rgba(0,0,0,.5);
    }
    .term-bar {
      background: #0f1623;
      border-bottom: 1px solid var(--border);
      padding: 12px 16px;
      display: flex; align-items: center; gap: 8px;
    }
    .term-dot { width: 11px; height: 11px; border-radius: 50%; }
    .term-dot.r { background: #f87171; }
    .term-dot.y { background: #fbbf24; }
    .term-dot.g { background: #34d399; }
    .term-title {
      font-family: var(--mono); font-size: 11px;
      color: var(--muted); margin-left: 8px; letter-spacing: .05em;
    }
    .term-body { padding: 24px; font-family: var(--mono); font-size: 13px; line-height: 2; }
    .term-prompt { color: var(--accent2); }
    .term-cmd    { color: var(--text); }
    .term-out    { color: var(--muted); padding-left: 0; }
    .term-key    { color: var(--accent); }
    .term-val    { color: var(--green); }
    .term-line   { display: block; }

    /* ── Stat cards ── */
    .cards {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 48px;
    }
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 20px 22px;
      transition: border-color .2s, transform .2s;
    }
    .card:hover { border-color: var(--accent); transform: translateY(-3px); }
    .card-label {
      font-family: var(--mono); font-size: 10px;
      letter-spacing: .12em; text-transform: uppercase;
      color: var(--muted); margin-bottom: 10px;
    }
    .card-val {
      font-size: 22px; font-weight: 600; color: var(--text);
      word-break: break-all;
    }
    .card-val.accent  { color: var(--accent); }
    .card-val.green   { color: var(--green); }
    .card-val.purple  { color: var(--accent2); }

    /* ── Endpoints section ── */
    .section-label {
      font-family: var(--mono); font-size: 11px;
      letter-spacing: .14em; text-transform: uppercase;
      color: var(--muted); margin-bottom: 16px;
    }
    .endpoints { display: flex; flex-direction: column; gap: 10px; margin-bottom: 48px; }
    .ep {
      display: flex; align-items: center; gap: 14px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px 18px;
      text-decoration: none;
      color: var(--text);
      transition: border-color .2s, background .2s;
    }
    .ep:hover { border-color: var(--accent); background: rgba(56,189,248,.04); }
    .ep-method {
      font-family: var(--mono); font-size: 10px;
      background: rgba(56,189,248,.1);
      color: var(--accent);
      border: 1px solid rgba(56,189,248,.2);
      border-radius: 4px;
      padding: 3px 8px;
      letter-spacing: .06em;
      white-space: nowrap;
    }
    .ep-path { font-family: var(--mono); font-size: 13px; color: var(--text); }
    .ep-desc { font-size: 13px; color: var(--muted); margin-left: auto; }

    /* ── Footer ── */
    footer {
      border-top: 1px solid var(--border);
      margin-top: 64px; padding-top: 28px;
      display: flex; justify-content: space-between; align-items: center;
      flex-wrap: wrap; gap: 12px;
    }
    footer p { font-family: var(--mono); font-size: 11px; color: var(--muted); }
    footer a { color: var(--accent); text-decoration: none; }

    @media (max-width: 600px) {
      .ep-desc { display: none; }
      nav { flex-direction: column; gap: 16px; align-items: flex-start; }
    }
  </style>
</head>
<body>
  <div class="orb orb-1"></div>
  <div class="orb orb-2"></div>

  <div class="page">
    <!-- Nav -->
    <nav>
      <div class="nav-logo">docker<span>/</span>webserver <span>v1.0.0</span></div>
      <div class="status-pill">
        <div class="dot"></div>
        CONTAINER HEALTHY
      </div>
    </nav>

    <!-- Hero -->
    <div class="hero">
      <div class="eyebrow">Task 4 — DevOps Project</div>
      <h1>Web server<br/><span class="dim">inside Docker.</span></h1>
      <p class="hero-sub">
        Flask app running behind an Nginx reverse proxy.
        Two containers, one network, zero friction.
      </p>
    </div>

    <!-- Terminal -->
    <div class="terminal">
      <div class="term-bar">
        <div class="term-dot r"></div>
        <div class="term-dot y"></div>
        <div class="term-dot g"></div>
        <span class="term-title">container info</span>
      </div>
      <div class="term-body">
        <span class="term-line"><span class="term-prompt">$ </span><span class="term-cmd">docker inspect flask-webserver</span></span>
        <span class="term-line term-out">{</span>
        <span class="term-line term-out">&nbsp;&nbsp;<span class="term-key">"ContainerID"</span>: <span class="term-val">"{{ container_id }}"</span>,</span>
        <span class="term-line term-out">&nbsp;&nbsp;<span class="term-key">"Status"</span>: <span class="term-val">"healthy"</span>,</span>
        <span class="term-line term-out">&nbsp;&nbsp;<span class="term-key">"Platform"</span>: <span class="term-val">"{{ platform }}"</span>,</span>
        <span class="term-line term-out">&nbsp;&nbsp;<span class="term-key">"Python"</span>: <span class="term-val">"{{ python_ver }}"</span>,</span>
        <span class="term-line term-out">&nbsp;&nbsp;<span class="term-key">"Timestamp"</span>: <span class="term-val">"{{ timestamp }}"</span></span>
        <span class="term-line term-out">}</span>
      </div>
    </div>

    <!-- Stat cards -->
    <div class="cards">
      <div class="card">
        <div class="card-label">Container ID</div>
        <div class="card-val accent">{{ container_short }}</div>
      </div>
      <div class="card">
        <div class="card-label">Status</div>
        <div class="card-val green">● Healthy</div>
      </div>
      <div class="card">
        <div class="card-label">Port</div>
        <div class="card-val purple">5000</div>
      </div>
      <div class="card">
        <div class="card-label">Uptime since</div>
        <div class="card-val">{{ uptime }}</div>
      </div>
    </div>

    <!-- Endpoints -->
    <div class="section-label">Available endpoints</div>
    <div class="endpoints">
      <a class="ep" href="/">
        <span class="ep-method">GET</span>
        <span class="ep-path">/</span>
        <span class="ep-desc">This page</span>
      </a>
      <a class="ep" href="/api/health">
        <span class="ep-method">GET</span>
        <span class="ep-path">/api/health</span>
        <span class="ep-desc">JSON health check</span>
      </a>
      <a class="ep" href="/api/info">
        <span class="ep-method">GET</span>
        <span class="ep-path">/api/info</span>
        <span class="ep-desc">App version and environment</span>
      </a>
      <a class="ep" href="/nginx-health">
        <span class="ep-method">GET</span>
        <span class="ep-path">/nginx-health</span>
        <span class="ep-desc">Nginx proxy status</span>
      </a>
      <a class="ep" href="/static/index.html">
        <span class="ep-method">GET</span>
        <span class="ep-path">/static/index.html</span>
        <span class="ep-desc">Static file served by Nginx</span>
      </a>
    </div>

    <!-- Footer -->
    <footer>
      <p>Built with Flask + Nginx + Docker &mdash; Task 4 DevOps Project</p>
      <p><a href="https://github.com/yourusername/docker-webserver">github.com/yourusername/docker-webserver</a></p>
    </footer>
  </div>
</body>
</html>"""

import time
START_TIME = time.time()

@app.route("/")
def home():
    now = datetime.datetime.now()
    container_id = os.environ.get("HOSTNAME", "local")
    uptime_secs = int(time.time() - START_TIME)
    uptime_str = f"{uptime_secs // 60}m {uptime_secs % 60}s"
    return render_template_string(HTML,
        container_id=container_id,
        container_short=container_id[:12],
        platform=platform.system() + " " + platform.release(),
        python_ver=platform.python_version(),
        timestamp=now.strftime("%Y-%m-%dT%H:%M:%S"),
        uptime=uptime_str
    )

@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "container": os.environ.get("HOSTNAME", "unknown"),
        "timestamp": str(datetime.datetime.now())
    })

@app.route("/api/info")
def info():
    return jsonify({
        "app": "Docker Web Server Project",
        "version": "1.0.0",
        "python_version": platform.python_version(),
        "platform": platform.system()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)