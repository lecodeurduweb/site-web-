import os
import random
import resend
from fastapi import FastAPI, Form, BackgroundTasks, Request
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Nomad Pi Online")

# --- SÉCURITÉ ---
resend.api_key = os.getenv("re_Ka89XhjQ_A3dQSgJjLuhBuLSoU2WKdYPf")

# --- CONFIGURATION ---
# On utilise Jinja2 pour pouvoir passer l'e-mail d'une page à l'autre dynamiquement
templates = Jinja2Templates(directory="static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Base de données temporaire (RAM)
utilisateurs = {
    "admin@nomad.com": {
        "pseudo": "👑 Fondateur",
        "password": "nomad2026",
        "role": "admin",
        "is_active": True
    }
}

def envoyer_email_code(email_dest, pseudo, code):
    try:
        resend.Emails.send({
            "from": "Nomad Pi <onboarding@resend.dev>",
            "to": email_dest,
            "subject": f"Ton code Nomad Pi : {code} 🔥",
            "html": f"<h1>Salut {pseudo} !</h1><p>Ton code est : <strong>{code}</strong></p>"
        })
    except Exception as e:
        print(f"Erreur mail : {e}")

# --- ROUTES ---

@app.get("/")
def home():
    return FileResponse("static/login.html")

@app.post("/register")
async def register(background_tasks: BackgroundTasks, pseudo: str = Form(...), email: str = Form(...), password: str = Form(...)):
    if email in utilisateurs:
        return JSONResponse({"status": "error", "message": "Email déjà utilisé"}, status_code=400)

    code_verif = str(random.randint(100000, 999999))
    utilisateurs[email] = {
        "pseudo": pseudo,
        "password": password,
        "role": "eleve",
        "code_verif": code_verif,
        "is_active": False
    }

    background_tasks.add_task(envoyer_email_code, email, pseudo, code_verif)
    
    # Redirection vers la page de vérification en passant l'email dans l'URL
    return RedirectResponse(url=f"/verification?email={email}", status_code=303)

@app.get("/verification")
async def page_verif(request: Request, email: str):
    # Cette route affiche la page verif.html (il faudra la transformer en template Jinja2)
    return templates.TemplateResponse("verif.html", {"request": request, "email": email})

@app.post("/verify")
async def verify(email: str = Form(...), code: str = Form(...)):
    if email in utilisateurs and utilisateurs[email]["code_verif"] == code:
        utilisateurs[email]["is_active"] = True
        # Une fois vérifié, on envoie direct au dashboard
        return RedirectResponse(url="/dashboard", status_code=303)
    
    return JSONResponse({"status": "error", "message": "Code incorrect ou e-mail inconnu"}, status_code=400)

@app.get("/dashboard")
def dashboard():
    return FileResponse("static/dashboard.html")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
