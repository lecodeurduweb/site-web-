import os
import random
import resend
from fastapi import FastAPI, Form, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import shutil

app = FastAPI(title="Nomad Pi Online")

# --- SÉCURITÉ : CLÉ API ---
# Sur ton Pi, ça cherchera la clé. Sur Render, on la mettra dans les réglages.
resend.api_key = os.getenv("RESEND_API_KEY", "re_cm9PU8Ph_3M7vvqCSAspyWBHiiT2NDhQp")

# --- DOSSIERS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_ADMIN = os.path.join(BASE_DIR, "static/base_admin")
os.makedirs(DB_ADMIN, exist_ok=True)

# --- BASE DE DONNÉES ---
utilisateurs = {
    "admin@nomad.com": {
        "pseudo": "👑 Fondateur",
        "password": "nomad2026",
        "role": "admin",
        "points": 9999,
        "flammes": 100,
        "is_active": True
    }
}

# --- FONCTION D'ENVOI D'EMAIL ---
def envoyer_email_code(email_dest, pseudo, code):
    try:
        resend.Emails.send({
            "from": "Nomad Pi <onboarding@resend.dev>",
            "to": email_dest,
            "subject": f"Ton code Nomad Pi : {code} 🔥",
            "html": f"""
                <div style="font-family: sans-serif; border: 2px solid #ff4500; padding: 20px; border-radius: 10px;">
                    <h1 style="color: #ff4500;">Salut {pseudo} !</h1>
                    <p>Bienvenue dans l'aventure Nomad Pi.</p>
                    <p>Voici ton code de vérification pour activer tes <strong>flammes</strong> :</p>
                    <div style="background: #eee; padding: 10px; font-size: 25px; font-weight: bold; letter-spacing: 5px;">
                        {code}
                    </div>
                </div>
            """
        })
    except Exception as e:
        print(f"Erreur d'envoi mail : {e}")

# --- ROUTES ---

@app.post("/register")
async def register(background_tasks: BackgroundTasks, pseudo: str = Form(...), email: str = Form(...), password: str = Form(...)):
    if email in utilisateurs:
        return JSONResponse({"status": "error", "message": "Email déjà utilisé"}, status_code=400)
    
    code_verif = str(random.randint(100000, 999999))
    utilisateurs[email] = {
        "pseudo": pseudo,
        "password": password,
        "role": "eleve",
        "points": 50,
        "flammes": 1,
        "code_verif": code_verif,
        "is_active": False
    }
    
    background_tasks.add_task(envoyer_email_code, email, pseudo, code_verif)
    return {"status": "success", "message": "Code envoyé !"}

@app.post("/verify")
async def verify(email: str = Form(...), code: str = Form(...)):
    if email in utilisateurs and utilisateurs[email]["code_verif"] == code:
        utilisateurs[email]["is_active"] = True
        return {"status": "success", "message": "Compte activé ! Connexion autorisée."}
    return JSONResponse({"status": "error", "message": "Code incorrect"}, status_code=400)

@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    if email in utilisateurs and utilisateurs[email]["password"] == password:
        user = utilisateurs[email]
        if not user["is_active"]:
            return JSONResponse({"status": "pending", "message": "Compte non activé"}, status_code=403)
        return {"status": "success", "user": user}
    return JSONResponse({"status": "error", "message": "Identifiants incorrects"}, status_code=401)

# --- STATIQUES ---
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    # Par défaut, on affiche la page de login
    return FileResponse("static/login.html")

# Route pour accéder à la page de vérification
@app.get("/verification")
def page_verif():
    return FileResponse("static/verif.html")

if __name__ == "__main__":
    import uvicorn
    # Le port est récupéré dynamiquement pour Render
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
