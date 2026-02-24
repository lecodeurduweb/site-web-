import os
import random
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Form, Request, BackgroundTasks
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Nomad Pi Online")

# --- CONFIGURATION ---
# Récupère l'URL Neon que tu as mise dans Render
DATABASE_URL = os.getenv("DATABASE_URL")

# Configuration des templates et fichiers statiques
templates = Jinja2Templates(directory="static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- FONCTIONS BASE DE DONNÉES ---

def get_db_connection():
    # Connexion directe avec ton lien binding=require
    return psycopg2.connect(DATABASE_URL)

def init_db():
    """ Crée la table et l'admin si nécessaire au démarrage """
    conn = get_db_connection()
    cur = conn.cursor()
    # Création de la table utilisateurs
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            pseudo TEXT,
            password TEXT,
            role TEXT,
            code_verif TEXT,
            is_active BOOLEAN DEFAULT FALSE
        );
    ''')
    # Insertion de l'admin (Louis)
    cur.execute('''
        INSERT INTO users (email, pseudo, password, role, code_verif, is_active)
        VALUES ('admin@nomad.com', 'Louis', 'nomad2026', 'Fondateur', '000000', TRUE)
        ON CONFLICT (email) DO NOTHING;
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Lancement de la base de données
@app.on_event("startup")
async def startup_event():
    try:
        if DATABASE_URL:
            init_db()
            print("✅ SQL CONNECTÉ : La base de données est prête !")
        else:
            print("❌ ERREUR : La variable DATABASE_URL est vide sur Render !")
    except Exception as e:
        print(f"❌ ERREUR SQL : {e}")

# --- ROUTES ---

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/register")
async def register(pseudo: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Vérifier si l'email existe déjà
        cur.execute("SELECT email FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return JSONResponse({"status": "error", "message": "Email déjà utilisé"}, status_code=400)

        # Créer le compte (non activé)
        code_verif = str(random.randint(100000, 999999))
        cur.execute("INSERT INTO users (email, pseudo, password, role, code_verif) VALUES (%s, %s, %s, %s, %s)",
                    (email, pseudo, password, "eleve", code_verif))
        conn.commit()
        cur.close()
        conn.close()
        
        # AFFICHER LE CODE DANS LES LOGS RENDER
        print(f"🔑 [NOUVEAU COMPTE] Email: {email} | Code: {code_verif}")
        
        return RedirectResponse(url=f"/verification?email={email}", status_code=303)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.get("/verification")
async def page_verif(request: Request, email: str):
    return templates.TemplateResponse("verif.html", {"request": request, "email": email})

@app.post("/verify")
async def verify(email: str = Form(...), code: str = Form(...)):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT code_verif FROM users WHERE email = %s", (email,))
    res = cur.fetchone()

    if res and res[0] == code:
        cur.execute("UPDATE users SET is_active = TRUE WHERE email = %s", (email,))
        conn.commit()
        cur.close()
        conn.close()
        return RedirectResponse(url="/dashboard", status_code=303)
    
    cur.close()
    conn.close()
    return JSONResponse({"status": "error", "message": "Code incorrect"}, status_code=400)

@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT pseudo, role, is_active FROM users WHERE email = %s AND password = %s", (email, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        if not user['is_active']:
            return JSONResponse({"status": "error", "message": "Compte non activé"}, status_code=403)
        return {"status": "success", "user": user}
    
    return JSONResponse({"status": "error", "message": "Identifiants incorrects"}, status_code=401)

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    # Récupère le port de Render (souvent 10000)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
