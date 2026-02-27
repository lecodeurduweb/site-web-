from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import psycopg2
import random
import os
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# Montage des fichiers statiques (pour le CSS et le JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- CONFIGURATION BASE DE DONNÉES (NEON) ---
DB_URL = "postgresql://neondb_owner:npg_u3BfN1YvAatL@ep-fancy-grass-a2v330p9-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require"

# --- CONFIGURATION EMAIL (OUTLOOK) ---
EMAIL_ADDRESS = "nomadpi2026@outlook.fr"
EMAIL_APP_PASSWORD = "fnnvcovbfmpumudd" # <--- METS TES 16 LETTRES ICI

def envoyer_email_code(destinataire, code):
    """Fonction qui envoie le mail via le serveur SMTP d'Outlook"""
    msg = MIMEText(f"Bienvenue sur NOMAD PI !\n\nTon code de vérification est : {code}")
    msg['Subject'] = "🔑 Code de vérification - NOMAD PI"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = destinataire

    try:
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()  # Sécurise la connexion
            server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            server.send_message(msg)
        print(f"✅ Email envoyé avec succès à {destinataire}")
    except Exception as e:
        print(f"❌ Erreur d'envoi d'email : {e}")

# --- ROUTES ---

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/register")
async def register(email: str = Form(...), password: str = Form(...)):
    code_verif = str(random.randint(100000, 999999))
    
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        # On insère l'utilisateur (non vérifié par défaut)
        cur.execute(
            "INSERT INTO utilisateurs (email, password, code_verif, verifie, role) VALUES (%s, %s, %s, %s, %s)",
            (email, password, code_verif, False, 'user')
        )
        conn.commit()
        cur.close()
        conn.close()
        
        # 🔥 NOUVEAUTÉ : On envoie le mail après l'inscription
        envoyer_email_code(email, code_verif)
        print(f"🔑 [LOG] Code pour {email} : {code_verif}")

        return RedirectResponse(url=f"/verification?email={email}", status_code=303)
    except Exception as e:
        print(f"❌ Erreur SQL : {e}")
        return {"error": "Email déjà utilisé ou erreur base de données"}

@app.get("/verification", response_class=HTMLResponse)
async def page_verif(email: str):
    with open("static/verif.html", "r", encoding="utf-8") as f:
        content = f.read()
    return content.replace("{{ email }}", email)

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
            cur.close()
            conn.close()
            # Redirection vers l'accueil ou login une fois validé
            return RedirectResponse(url="/?status=success", status_code=303)
        else:
            return {"error": "Code incorrect"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
