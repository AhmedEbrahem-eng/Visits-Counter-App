# Counter App

A simple hit-counter web application built with **Flask** and **Redis**, containerized with **Docker**.

## How It Works

Every time you visit the root URL (`/`), a counter stored in Redis is incremented and the current count is displayed.

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Run the App

```bash
docker compose up --build
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

### Stop the App

```bash
docker compose down
```

## Project Structure

```
counter-app/
├── app.py                 # Flask application
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker image definition
├── README.md              # This file
└── requirements.txt       # Python dependencies
```
