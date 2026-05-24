from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ⚠️ Remplace par tes vrais identifiants
USERS = {
    "admin@mobilisai.com": "motdepasse123"
}

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"error": None})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    if email in USERS and USERS[email] == password:
        return RedirectResponse(url="/accueil", status_code=302)
    return templates.TemplateResponse(request, "login.html", {"error": "Email ou mot de passe incorrect."})

@app.get("/accueil", response_class=HTMLResponse)
async def accueil(request: Request):
    return templates.TemplateResponse(request, "accueil.html", {})

@app.get("/logout")
async def logout():
    return RedirectResponse(url="/", status_code=302)