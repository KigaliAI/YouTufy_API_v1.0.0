import os
import secrets
import logging
from dotenv import load_dotenv
# Load local .env early
load_dotenv(dotenv_path="/app/.env")

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from api.routes import reset

# Logging
logging.basicConfig(level=logging.DEBUG)

# Create DB tables on startup
from backend.database import create_tables
create_tables()

# Detect environment
ENV = os.getenv("ENV", "development")
print(f"🔧 ENV: {ENV}")
print(f"📦 DATABASE_URL: {os.getenv('DATABASE_URL')}")
print("🚀 Starting YouTufy...")

# FastAPI app setup
app = FastAPI(title="YouTufy API", version="1.0.0")

# Sessions
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="session_id",
    max_age=86400,
    same_site="Lax",
    https_only=False  # Set to True if NGINX handles HTTPS termination
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.youtufy.com"],  # frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
allow_origins=["*"]  

# Allow HEAD requests
@app.middleware("http")
async def allow_head_request(request: Request, call_next):
    if request.method == "HEAD":
        response = await call_next(request)
        response.body = b""
        return response
    return await call_next(request)

# Static files and templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(os.path.join("static", "favicon.ico"))

# Health check endpoint
@app.get("/health")
@app.head("/")
def health_check():
    return {"status": "ok"}

# Root landing page
@app.get("/", response_class=HTMLResponse)
def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Welcome to YouTufy API",
        "description": "A YouTube subscription manager powered by FastAPI."
    })

# Import and register routes
from api.routes import auth, users, youtube, google_oauth, reset, verify, admin
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(youtube.router, prefix="/youtube", tags=["YouTube"])
app.include_router(google_oauth.router, prefix="/oauth", tags=["Google OAuth"])
app.include_router(reset.router, prefix="/auth", tags=["Reset"])
app.include_router(verify.router, prefix="/auth", tags=["Verify"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

# App startup
@app.on_event("startup")
async def startup_event():
    create_tables()
    print("🚀 App running in development")

# Entry point for running locally (optional inside Docker)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
