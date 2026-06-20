from fastapi import FastAPI, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ⚠️ Remplace par tes vrais identifiants
# Chaque utilisateur a maintenant un rôle associé
USERS = {
    "admin@mobilisai.com": {
        "password": "motdepasse123",
        "role": "oss"
    },
    "finance@mobilisai.com": {
        "password": "motdepasse456",
        "role": "finance"
    }
}

# Redirections selon le rôle
ROLE_REDIRECTS = {
    "oss": "/accueil",
    "finance": "https://knowledgeval.onrender.com"
}

# Sessions actives
sessions = {}


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request, session_id: Optional[str] = Cookie(None)):
    if session_id and session_id in sessions:
        role = sessions[session_id]["role"]
        return RedirectResponse(url=ROLE_REDIRECTS[role], status_code=302)
    return templates.TemplateResponse(request, "login.html", {"error": None})


@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = USERS.get(email)

    if user and user["password"] == password:
        session_id = str(uuid.uuid4())
        sessions[session_id] = {"email": email, "role": user["role"]}

        response = RedirectResponse(url=ROLE_REDIRECTS[user["role"]], status_code=302)
        response.set_cookie(key="session_id", value=session_id)
        return response

    return templates.TemplateResponse(request, "login.html", {"error": "Email ou mot de passe incorrect."})


@app.get("/accueil", response_class=HTMLResponse)
async def accueil(request: Request, session_id: Optional[str] = Cookie(None)):
    if not session_id or session_id not in sessions:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(request, "accueil.html", {})


@app.get("/logout")
async def logout(session_id: Optional[str] = Cookie(None)):
    if session_id and session_id in sessions:
        del sessions[session_id]
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("session_id")
    return response
