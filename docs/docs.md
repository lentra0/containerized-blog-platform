# 📚 Project Documentation

## Table of Contents

- [🖥️ Services & Ports](#️-services--ports)
- [🚀 Frontend](#-frontend)
- [🛠️ Backend API](#️-backend-api)
- [🗄️ Database & Cache](#️-database--cache)
- [📈 Monitoring](#️-monitoring)
- [🐞 Troubleshooting](#️-troubleshooting)
- [📸 Screenshots & Embedding](#️-screenshots--embedding)

---

## 🖥️ Services & Ports

| Service             | Description                              | Port    | URL                              |
|---------------------|------------------------------------------|--------:|----------------------------------|
| Frontend            | Next.js application                      | 3000    | http://localhost:3000            |
| Backend API         | FastAPI REST API                         | 8000    | http://localhost:8000            |
| PostgreSQL          | Database                                 | 5432    | postgresql://<user>:<password>@localhost:5432/<db> |
| Redis               | Cache                                    | 6379    | redis://localhost:6379           |
| Metrics (FastAPI)   | Prometheus metrics endpoint              | 8000    | http://localhost:8000/metrics    |
| Redis Exporter      | Redis metrics for Prometheus             | 9121    | http://localhost:9121/metrics    |
| Postgres Exporter   | Postgres metrics for Prometheus          | 9187    | http://localhost:9187/metrics    |
| Prometheus          | Monitoring & alerting                    | 9090    | http://localhost:9090            |
| Grafana             | Dashboards UI                            | 3001    | http://localhost:3001            |

---

## 🚀 Frontend

The frontend is built with **Next.js** and can run either via:

- **Docker Compose**: `docker-compose up --build -d`
  Copy `.env.example` to `.env` and populate it.
- **Locally**: 
  ```bash
  cd frontend
  npm install
  npm run dev
  ```

### Available Pages

| Route                       | Description                                         |
|-----------------------------|-----------------------------------------------------|
| `/`                         | List of blog posts                                  |
| `/login`                    | Registration/Login page                             |
| `/admin`                    | Admin panel to create new posts (requires login)    |
| `/posts/[id]`               | View single post with comments and likes            |

---

## 🛠️ Backend API

The backend uses **FastAPI**, exposing the following endpoints:

### Authentication

- **Register**  `POST /api/auth/register`
  - Body: `{ "username": "<username>", "password": "<password>" }`
  - Response: created `UserOut` object
- **Login**     `POST /api/auth/login`
  - Form data: `username`, `password`
  - Response: `{ access_token, token_type }`
- **Current User** `GET /api/auth/me`
  - Header: `Authorization: Bearer <token>`
  - Response: `UserOut`

### Posts

- **List Posts**     `GET /api/posts`
- **Get Post**       `GET /api/posts/{id}`
- **Create Post**    `POST /api/posts`
  - Body: `{ "title": "...", "content": "..." }`
  - Requires JWT in `Authorization` header; anonymous posts allowed if no token
- **Delete Post**    `DELETE /api/posts/{id}`
  - No authentication required in the current implementation. This is unsafe in production — require authentication and ownership checks.

Security: Store secrets using your preferred method.

### Comments

- **List Comments**  `GET /api/comments?post_id=<id>`
- **Create Comment** `POST /api/comments`
  - Body: `{ "post_id": <id>, "content": "..." }`
  - Requires JWT; anonymous allowed via `Anonymous` user

### Likes

- **Like Post**      `POST /api/likes`
  - Body: `post_id` in query or JSON
  - Requires JWT; toggles like, unique per user

---

## 🗄️ Database & Cache

- **PostgreSQL**: stores `users`, `posts`, `comments`, `likes`.
- **Redis**: available for caching; metrics via exporter.

Connection strings are configured via environment variables in `.env` or `docker-compose.yml`.

---

## 📈 Monitoring

- **Backend metrics**: exposed automatically at `/metrics` via `prometheus-fastapi-instrumentator`.
- **Prometheus**:
  - Configure in `monitoring/prometheus/prometheus.yml`.
  - Access at http://localhost:9090.
- **Grafana**:
  - Datasource preconfigured for Prometheus.
  - Access at http://localhost:3001 (`admin`/`admin`).
  - Import or build dashboards to visualize CPU, memory, request rates, response times, DB and Redis metrics.