# 🚀 High-Performance Production Visitor Counter

A production-grade, secure, and containerized visitor counter application built with a **Flask Application Factory**, **Redis**, and **Gunicorn**, fully orchestrated using **Docker Compose** and styled with a stunning **Cyberpunk Glassmorphism Dark Mode UI**.

---

## ✨ Features

- **🌐 Premium Telemetry UI**: A modern dashboard built using HTML5, CSS3 transitions, ambient background glows, and interactive card modules utilizing the *Outfit* and *Inter* typography.
- **⚡ Real-Time Async Updates**: Increment and synchronize metrics instantly via backend JSON APIs without triggering browser page reloads.
- **🛡️ Hardened Security**: Containers are engineered using security best practices, executing operations under a non-root system user (`appuser`).
- **⚡ WSGI HTTP Server**: Serves requests using a multi-worker **Gunicorn** server to ensure stability, concurrency, and high availability.
- **🩺 Active Health Monitoring**: Integrates automated Docker health check probes for both the Web application (`wget`) and Redis database (`redis-cli ping`).
- **🧪 Test Suite**: Features fully mock-integrated unit and integration testing via **pytest** and **pytest-mock** to validate code stability and network fallback logic.

---

## 🛠️ Architecture Layout

```text
counter-app/
├── app/                      # Main Application Package
│   ├── __init__.py           # Application Factory Pattern (create_app)
│   ├── config.py             # Environment configurations (Dev/Test/Prod)
│   ├── routes.py             # API controllers and Blueprint routing
│   ├── templates/
│   │   └── index.html        # Telemetry dashboard frontend
│   └── static/
│       ├── css/
│       │   └── style.css     # Glassmorphic style sheet and animations
│       └── js/
│           └── main.js       # Asynchronous AJAX and UI controller
├── tests/                    # Test Automation
│   └── test_app.py           # Pytest test cases
├── Dockerfile                # Production-grade Docker multi-stage configuration
├── docker-compose.yml        # Service orchestration & health checks
├── run.py                    # Root WSGI application entry point
├── requirements.txt          # Python dependencies (gunicorn, pytest, etc.)
└── README.md                 # Project documentation
```

---

## 🚀 Getting Started

### 📋 Prerequisites

Ensure you have the following installed on your machine:
- **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** or Docker Engine
- **[Docker Compose](https://docs.docker.com/compose/install/)**

---

### 💻 1. Spin up the App

To build and run the services in detached (background) mode, run:

```bash
docker compose up --build -d
```

Once started, the application will be accessible at:
👉 **[http://localhost:5000](http://localhost:5000)**

---

### 🩺 2. Verify Container Health

Check the status and health check state of the services:

```bash
docker compose ps
```

You should see both containers marked as `healthy`:
```text
NAME                  STATUS                 PORTS
counter-app-redis-1   Up 1 minute (healthy)  6379/tcp
counter-app-web-1     Up 1 minute (healthy)  0.0.0.0:5000->5000/tcp
```

You can also request the raw JSON health payload at:
👉 **[http://localhost:5000/health](http://localhost:5000/health)**

---

### 🧪 3. Run the Automated Tests

To execute the Pytest test suite inside the running Web container:

```bash
docker compose exec web python -m pytest -p no:cacheprovider
```

---

### 🛑 4. Shutting Down

To stop the containers and tear down the network:

```bash
docker compose down
```
