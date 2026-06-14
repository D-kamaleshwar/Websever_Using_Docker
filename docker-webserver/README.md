# 🐳 Task 4 — Web Server using Docker

> A containerized web server project demonstrating Docker fundamentals — multi-container orchestration, reverse proxying, health monitoring, and CI/CD via GitHub Actions.

---

## 📸 Preview

![App Preview](images/preview.png)

---

## 🏗️ Architecture

```
Browser (http://localhost)
        │
        ▼
┌─────────────────────┐
│   Nginx Container   │  ← Port 80 (public)
│   Reverse Proxy     │
└────────┬────────────┘
         │ proxy_pass
         ▼
┌─────────────────────┐
│   Flask Container   │  ← Port 5000 (internal only)
│   Python Web App    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Volume: app_data   │  ← Persistent storage
└─────────────────────┘

Both containers share → docker network: webnet
```

---

## 📁 Project Structure

```
docker-webserver/
├── app/
│   ├── Dockerfile           # Flask container image
│   ├── app.py               # Flask web application
│   └── requirements.txt     # Python dependencies
├── nginx/
│   ├── Dockerfile           # Nginx container image
│   └── nginx.conf           # Reverse proxy config
├── static/
│   └── index.html           # Static page served by Nginx
├── docker-compose.yml       # Multi-container orchestration
├── .github/
│   └── workflows/
│       └── docker-ci.yml    # GitHub Actions CI pipeline
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Git

### Run the app

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/docker-webserver.git
cd docker-webserver

# 2. Build and start all containers
docker compose up --build -d

# 3. Open in browser
# http://localhost
```

---

## 🌐 Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Main dashboard — container info, uptime, endpoints |
| `GET /api/health` | JSON health check response |
| `GET /api/info` | App version and environment info |
| `GET /nginx-health` | Nginx proxy status |
| `GET /static/index.html` | Static file served directly by Nginx |

---

## 🐳 Core Docker Commands

```bash
# View running containers
docker ps

# Stream live logs
docker logs flask-webserver
docker logs nginx-proxy

# Monitor CPU and memory usage
docker stats

# Inspect container health
docker inspect flask-webserver | grep -A 10 "Health"

# Open a shell inside the container
docker exec -it flask-webserver bash

# Stop all containers
docker compose down

# Stop and remove volumes too
docker compose down -v
```

---

## ❤️ Health Monitoring

Both containers use Docker's built-in `HEALTHCHECK` — Docker automatically monitors them and restarts on failure.

**Flask app (`app/Dockerfile`):**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health')" || exit 1
```

**Nginx (`nginx/Dockerfile`):**
```dockerfile
HEALTHCHECK --interval=30s --timeout=5s \
  CMD wget -q --spider http://localhost/nginx-health || exit 1
```

Nginx only starts **after** Flask is confirmed healthy:
```yaml
depends_on:
  flask-app:
    condition: service_healthy
```

---

## ⚙️ CI/CD Pipeline

GitHub Actions runs automatically on every push to `main`:

```
Push to main
    │
    ▼
Build Flask image
    │
    ▼
Build Nginx image
    │
    ▼
docker compose up -d
    │
    ▼
Health check (wait 15s)
    │
    ▼
curl all endpoints ✓
    │
    ▼
Print logs & status
    │
    ▼
docker compose down
```

---

## 📚 DevOps Concepts Covered

| Concept | Implementation |
|---|---|
| **Containerization** | Dockerfiles for Flask and Nginx |
| **Container lifecycle** | build → run → exec → stop → remove |
| **Multi-container apps** | `docker-compose.yml` orchestration |
| **Reverse proxy** | Nginx forwarding traffic to Flask |
| **Health monitoring** | `HEALTHCHECK`, `docker stats`, `docker inspect` |
| **Volume management** | Named volume `app_data` for persistence |
| **Network isolation** | Custom bridge network `webnet` |
| **Restart policies** | `restart: unless-stopped` for resilience |
| **CI/CD integration** | GitHub Actions automated pipeline |

---

## 🛡️ Deployment Best Practices Applied

- Flask port `5000` is **internal only** — only Nginx port `80` is published
- Nginx starts only **after** Flask passes its health check
- Slim base images (`python:3.11-slim`, `nginx:alpine`) keep sizes small
- Named volumes ensure data survives container restarts
- Containers auto-recover from crashes via restart policies
- Nginx handles routing and static files; Flask handles app logic only

---

## 🧪 Sample API Responses

**`GET /api/health`**
```json
{
  "status": "healthy",
  "container": "a3f9d12b8e4c",
  "timestamp": "2026-06-14T10:30:00"
}
```

**`GET /api/info`**
```json
{
  "app": "Docker Web Server Project",
  "version": "1.0.0",
  "python_version": "3.11.9",
  "platform": "Linux"
}
```

---

## 👤 Author

**Kamaleshwar D** — AIML Student  
GitHub: [github.com/yourusername](https://github.com/yourusername)

---

## 📄 License

MIT License — free to use and modify.