import os
import random
import smtplib
import psycopg2
from email.mime.text import MIMEText
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# --- CONFIGURATION DES CHEMINS (Indispensable pour Render) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# On rend accessible le dossier static (pour le CSS/JS)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# --- CONFIGURATION BASE DE DONNÉES (NEON) ---
DB_URL = "postgresql://neondb_owner:npg_u3BfN1YvAatL@ep-fancy-grass-a2v330p9-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require"

# --- CONFIGURATION EMAIL (OUTLOOK) ---
EMAIL_ADDRESS = "nomadpi2026@outlook.fr"
EMAIL_APP_PASSWORD = "fnnvcovbfmpumudd" # <--- METS TES 16 LETTRES ICI

def envoyer_email_code(destinataire, code):
    msg = MIMEText(f"Bienvenue sur NOMAD PI !\n\nTon code de vérification est : {code}")
    msg['Subject'] = "🔑 Ton code de vérification"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = destinataire
    try:
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            server.send_message(msg)
        print(f"✅ Email envoyé à {destinataire}")
    except Exception as e:
        print(f"❌ Erreur email : {e}")

# --- ROUTES D'AFFICHAGE (GET) ---

@app.get("/", response_class=HTMLResponse)
async def home():
    """Affiche la page d'inscription"""
    path = os.path.join(STATIC_DIR, "index.html")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "❌ Fichier index.html introuvable dans le dossier static."

@app.get("/login-page", response_class=HTMLResponse)
async def login_page():
    """Affiche la page de connexion"""
    path = os.path.join(STATIC_DIR, "login.html")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "❌ Fichier login.html introuvable."

@app.get("/verification", response_class=HTMLResponse)
async def page_verif(email: str):
    """Affiche la page pour entrer le code"""
    path = os.path.join(STATIC_DIR, "verif.html")
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return content.replace("{{ email }}", email)
    except FileNotFoundError:
        return "❌ Fichier verif.html introuvable."

# --- ROUTES D'ACTION (POST) ---

@app.post("/register")
async def register(
    email: str = Form(...), 
    password: str = Form(...),
    pseudo: str = Form(None),
    etablissement: str = Form(None),
    niveau: str = Form(None)
):
    code_verif = str(random.randint(100000, 999999))
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # On insère toutes les infos reçues du formulaire
        query = """
            INSERT INTO utilisateurs (email, password, pseudo, etablissement, niveau, code_verif, verifie, role)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (email, password, pseudo, etablissement, niveau, code_verif, False, 'user'))
        
        conn.commit()
        cur.close()
        conn.close()
        
        envoyer_email_code(email, code_verif)
        
        # Redirection vers la page de saisie du code
        return RedirectResponse(url=f"/verification?email={email}", status_code=303)
        
    except Exception as e:
        print(f"🔥 Erreur : {e}")
        return {"error": "L'email existe déjà ou la table n'est pas prête sur Neon."}

@app.post("/verify")
async def verify(email: str = Form(...), code: str = Form(...)):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT code_verif FROM utilisateurs WHERE email = %s", (email,))
        result = cur.fetchone()
        
        if result and result[0] == code:
            cur.execute("UPDATE utilisateurs SET verifie = True WHERE email = %s", (email,))
            conn.commit()
            return RedirectResponse(url="/login-page?status=verified", status_code=303)
        else:
            return {"error": "Code incorrect"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
