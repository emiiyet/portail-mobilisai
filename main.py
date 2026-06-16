from fastapi import FastAPI, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")



# ⚠️ Remplace par tes vrais identifiants
USERS = {
    "admin@mobilisai.com": "motdepasse123"
}

# Sessions actives
sessions = {}

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request, session_id: Optional[str] = Cookie(None)):
    # Si déjà connecté, aller directement à l'accueil
    if session_id and session_id in sessions:
        return RedirectResponse(url="/accueil", status_code=302)
    return templates.TemplateResponse(request, "login.html", {"error": None})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    if email in USERS and USERS[email] == password:
        # Créer une session
        import uuid
        session_id = str(uuid.uuid4())
        sessions[session_id] = email
        response = RedirectResponse(url="/accueil", status_code=302)
        response.set_cookie(key="session_id", value=session_id)
        return response
    return templates.TemplateResponse(request, "login.html", {"error": "Email ou mot de passe incorrect."})

@app.get("/accueil", response_class=HTMLResponse)
async def accueil(request: Request, session_id: Optional[str] = Cookie(None)):
    # Si pas connecté, rediriger vers login
    if not session_id or session_id not in sessions:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(request, "accueil.html", {})

@app.get("/logout")
async def logout(session_id: Optional[str] = Cookie(None)):
    # Supprimer la session
    if session_id and session_id in sessions:
        del sessions[session_id]
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("session_id")
    return response
