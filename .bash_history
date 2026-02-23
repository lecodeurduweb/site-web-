sudo apt update && sudo apt upgrade -y
curl -fsSL https://ollama.com/install.sh | sh
sudo apt update
sudo apt install python3-pip python3-venv -y
ollama pull phi3
pip3 install fastapi uvicorn ollama
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn ollama
nano main.py
ollama pull phi3
ollama serve
deactivate
ollama serve
ollama run phi3 "Bonjour, es-tu prêt ?"
cd ~/nomad-project
source venv/bin/activate
python3 main.py
deactivate
clear
mkdir -p /home/louis/static
source venv/bin/activate
python3 main.py
hostname -I
nano /home/louis/static/index.html
/home/louis/static/index.html
deconected
deactivate
nano /home/louis/static/index.html
sudo nano /etc/systemd/system/nomadpi.service
sudo systemctl daemon-reload
sudo systemctl enable nomadpi.service
sudo systemctl start nomadpi.service
sudo systemctl status nomadpi.service
sudo fuser -k 8000/tcp
sudo systemctl restart nomadpi.service
sudo systemctl status nomadpi.service
nano /home/louis/main.py
sudo systemctl restart nomadpi.service
sudo systemctl status nomadpi.service
nano /home/louis/static/login.html
exit 
clear
curl http://localhost:8000
ls -R /home/louis/static
nano /home/louis/static/index.html
python3 /home/louis/main.py
source /home/louis/venv/bin/activate
python3 /home/louis/main.py
exit 
/home/louis/static/index.html
nano /home/louis/static/index.html
nano /home/louis/static/matiere.html
nano /home/louis/static/index.html
nano /home/louis/static/cours.html
nano /home/louis/static/matiere.html
nano /home/louis/static/profil.html
nano /home/louis/static/index.html
nano /home/louis/static/settings.html
ano /home/louis/static/index.html
nano /home/louis/static/index.html
fuser -k 8000/tcp
python3 /home/louis/main.py
source /home/louis/venv/bin/activate
fuser -k 8000/tcp
python3 /home/louis/main.py
exit 
sudo systemctl status
systemctl status ollama
curl http://127.0.0.1:8000
ls /home/louis/static
cat /home/louis/main.py
nano /home/louis/main.py
pkill -9 python
python3 /home/louis/main.py
from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import ollama
import uvicorn
import os
import socket
app = FastAPI()
# Configuration des fichiers statiques
if not os.path.exists("static"):
app.mount("/static", StaticFiles(directory="static"), name="static")
# --- ROUTES NAVIGATION ---
@app.get("/")
def read_root():
@app.get("/dashboard")
def get_dashboard():
# --- LOGIQUE AUTHENTIFICATION ---
@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
@app.post("/register")
async def register(email: str = Form(...), password: str = Form(...)):
# --- LOGIQUE IA ---
@app.get("/ask")
def ask_ai(question: str):
nano /home/louis/main.py
source /home/louis/venv/bin/activate
pkill -9 python
python3 /home/louis/main.py
pip install python-multipart
python3 /home/louis/main.py
exit 
find /home/pi -mtime -2 -ls
find /home/louis -mtime -2 -ls
find /home/louis -name "*.py" -not -path "*/.*"
find /home/louis -name "*.py" -not -path "*/.*" -not -path "*/venv/*"
source /home/louis/venv/bin/activate
uvicorn main:app --reload
lsof -i :8000
fuser -k 8000/tcp
uvicorn main:app --reload
pkill -9 python
uvicorn main:app --reload
uvicorn main:app --reload --port 8001
python3 /home/louis/main.py
pkill -9 python
python3 /home/louis/main.py
deactivate
nano /home/louis/static/login.html
nano /home/louis/main.py
sudo apt update
sudo apt install postfix -y
nano /home/louis/main.py
source /home/louis/venv/bin/activate
pip install python-multipart
python3 /home/louis/main.py
nano /home/louis/main.py
python3 /home/louis/main.py
fuser -k 8000/tcp
python3 /home/louis/main.py
/home/louis/static/login.html
python3 /home/louis/main.py
deactivate
# On tue les anciens processus
pkill -9 python
# On active l'environnement
source /home/louis/venv/bin/activate
# On lance le serveur
python3 /home/louis/main.py
python3 /home/louis/main.py
nano /home/louis/main.py
nano/home/louis/static/login.html
nano /home/louis/static/login.html
nano /home/louis/static/admin.html
pkill -9 python
nano /home/louis/main.py
nano /home/louis/static/index.html
nano main.py
mkdir static
nano static/index.html
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pip install fastapi uvicorn python-multipart
source venv/bin/activate
pip install fastapi uvicorn python-multipart
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
fuser -k 8000/tcp
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
deactivate
nano main.py
nano static/login.html
nano static/index.html
fuser -k 8000/tcp
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
source venv/bin/activate
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
deactivate
nano main.py
nano static/login.html
nano main.py
nano static/login.html
nano main.py
nano static/index.html
fuser -k 8000/tcp
nano main.py
nano static/index.html
fuser -k 8000/tcp
nano main.py
shutdown -h now
sudo shutdown -h now
source /home/louis/venv/bin/activate
python3 /home/louis/main.py
deactivate
nano nano main.py
nano static/index.html
nano static/login.html
source /home/louis/venv/bin/activate
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
fuser -k 8000/tcp
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
fuser -k 8000/tcp
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
source venv/bin/activate
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
fuser -k 8000/tcp
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
fuser -k 8000/tcp
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
/home/louis/static/login.html
nano /home/louis/static/login.html
pkill -9 python
source /home/louis/venv/bin/activate
python3 /home/louis/main.py
deactivate
nano /home/louis/static/admin.html
nano /home/louis/static/login.html
nano /home/louis/static/main.html
nano /home/louis/main.py
ls -l /var/www/html/
cat /home/louis/main.py
nano /home/louis/main.py
pip install resend
source ~/mon_projet_env/bin/activate
source /home/louis/venv/bin/activate
pip install resend fastapi uvicorn python-multipart
deactivate
nano /home/louis/main.py
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
source /home/louis/venv/bin/activate
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
desactivate
deactivate
nano /home/louis/main.py
source /home/louis/venv/bin/activate
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
deactivate
nano /home/louis/main.py
source /home/louis/venv/bin/activate
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
EXIT
deactivate
exit
nano requirements.txt
nano /home/louis/main.py
ls -l /home/louis/
cd /home/louis/
sudo apt update && sudo apt install git -y
# 1. Initialise le dossier
git init
# 2. Ajoute tous tes fichiers (main.py, requirements.txt, dossier static)
git add .
# 3. Crée ton premier point de sauvegarde
git commit -m "Mise en ligne Nomad Pi"
# 4. Renomme la branche principale
git branch -M main
# 5. Connecte ton Pi à GitHub (lecodeurduweb)
git remote add origin https://github.com/lecodeurduweb/site-web.git
# 6. Envoie le code !
git push -u origin main
git config --global user.email "louis.sittler2012@outlook.fr"
git config --global user.name "lecodeurduweb"
# 1. Initialise le projet
git init
# 2. Crée un fichier pour ignorer les dossiers inutiles
echo "venv/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.db" >> .gitignore
# 1. Initialise le projet
git init
# 2. Crée un fichier pour ignorer les dossiers inutiles
echo "venv/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.db" >> .gitignore
git push -u origin main
git add .
git commit -m "Premier envoi du site Nomad Pi"
git branch -M main
git push -u origin main
git push -u origin maingit push -u origin maingit push -u origin maingit push -u origin maingit push -u origin main
git push -u origin main
git remote set-url origin https://github.com/lecodeurduweb/site-web.git
git push -u origin main
sudo poweroff
