## YouTufy – Your Personalized YouTube Dashboard (v1.0.0)

**YouTufy** is a full-stack web application that connects to your YouTube account via Google OAuth and visualizes your channel subscriptions, statistics, and latest video uploads — all within a clean, privacy-conscious dashboard.

---

## Features

- 🔐 **Google OAuth 2.0** authentication
- 📺 **Fetch YouTube subscriptions** (title, thumbnail, views, etc.)
- 🗓️ **Latest video upload date** for each channel
- 📊 **Personalized dashboard** (frontend on Netlify)
- 🗃️ **PostgreSQL** for optional token/session storage
- 🐳 **Dockerized** setup for backend + DB

---

##Tech Stack

| Layer      | Technology |
|------------|------------|
| **Backend** | [FastAPI](https://fastapi.tiangolo.com) + SQLAlchemy |
| **Auth**    | Google OAuth 2.0 (`google-auth`, `oauthlib`) |
| **Frontend** | Static SPA hosted via **Netlify** |
| **Database** | PostgreSQL (via Docker, or GCP Cloud SQL) |
| **Deployment** | Docker + Docker Compose |

---

## Live Deployment

- **Frontend (Netlify):** [https://www.youtufy.com](https://www.youtufy.com)
- **Backend API (FastAPI):** [https://api.youtufy.com](https://api.youtufy.com)
- **Swagger Docs:** [https://api.youtufy.com/docs](https://api.youtufy.com/docs)

---

## Project Structure

youtufy_api/
├── backend/ # Business logic (OAuth, DB, YouTube API)
├── api/routes/ # FastAPI route handlers
├── templates/ # Jinja2 HTML templates (SSR views)
├── static/ # Static assets (favicon, CSS, logo)
├── users/ # User-specific stored JSON data
├── Dockerfile
├── docker-compose.yml
└── .env


---

## 📦 Requirements

- Python 3.11+
- Docker + Docker Compose
- Google OAuth Client ID / Secret
- Netlify (for frontend deployment)

---

## 🧪 Local Development (via Docker)

```bash
# Clone repo
git clone https://github.com/<your-username>/YouTufy_API.git
cd YouTufy_API

# Create .env and .env.production files

# Start the app
docker-compose up --build

---

## Contributing
We welcome pull requests, feature suggestions, or issue reports!

-Fork this repo and create a PR

-Or submit feedback via: https://github.com/KigaliAI/youtufy-1.0.1

---

## License
This project is licensed under the MIT License.
© 2025 YouTufy
