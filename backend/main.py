from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json

app = FastAPI(title="ChronoGrid API")

# CORS pour autoriser React à communiquer avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── BASE DE DONNÉES SIMULÉE (en mémoire) ───────────────────

users_db = [
    {"id": 1, "nom": "Konan", "prenom": "Aya", "email": "aya@canalplus.ci", "password": "aya123", "role": "admin"},
    {"id": 2, "nom": "Diallo", "prenom": "Sophie", "email": "sophie@canalplus.ci", "password": "sophie123", "role": "assistante"},
    {"id": 3, "nom": "Traoré", "prenom": "Marie", "email": "marie@canalplus.ci", "password": "marie123", "role": "assistante"},
]

chaines_db = [
    {"id": 1, "nom": "Novelas CI", "code": "NOV_CI"},
    {"id": 2, "nom": "Novelas Caraïbe", "code": "NOV_CAR"},
    {"id": 3, "nom": "Jumbo Jamboo", "code": "JJB"},
    {"id": 4, "nom": "Maboke", "code": "MBK"},
    {"id": 5, "nom": "Sunu Yeuf", "code": "SNY"},
]

creneaux_db = [
    # Novelas CI (grille_id: 1)
    {"id": 1, "grille_id": 1, "heure_debut": "06:00", "duree": 52, "titre": "Destinos", "type": "PROG", "ordre": 1, "modifie_par": None, "modifie_le": None},
    {"id": 2, "grille_id": 1, "heure_debut": "06:52", "duree": 3, "titre": "BA Novelas", "type": "BA", "ordre": 2, "modifie_par": None, "modifie_le": None},
    {"id": 3, "grille_id": 1, "heure_debut": "06:55", "duree": 5, "titre": "Écran pub", "type": "PUB", "ordre": 3, "modifie_par": None, "modifie_le": None},
    {"id": 4, "grille_id": 1, "heure_debut": "07:00", "duree": 45, "titre": "Amor Prohibido", "type": "PROG", "ordre": 4, "modifie_par": None, "modifie_le": None},
    {"id": 5, "grille_id": 1, "heure_debut": "07:45", "duree": 5, "titre": "Écran pub", "type": "PUB", "ordre": 5, "modifie_par": None, "modifie_le": None},
    {"id": 6, "grille_id": 1, "heure_debut": "07:50", "duree": 52, "titre": "La Reina del Sur", "type": "PROG", "ordre": 6, "modifie_par": None, "modifie_le": None},
    {"id": 7, "grille_id": 1, "heure_debut": "08:42", "duree": 3, "titre": "BA Novelas", "type": "BA", "ordre": 7, "modifie_par": None, "modifie_le": None},
    {"id": 8, "grille_id": 1, "heure_debut": "08:45", "duree": 45, "titre": "Pasión de Gavilanes", "type": "PROG", "ordre": 8, "modifie_par": None, "modifie_le": None},

    # Novelas Caraïbe (grille_id: 2)
    {"id": 9, "grille_id": 2, "heure_debut": "06:00", "duree": 45, "titre": "Thé au harem", "type": "PROG", "ordre": 1, "modifie_par": None, "modifie_le": None},
    {"id": 10, "grille_id": 2, "heure_debut": "06:45", "duree": 3, "titre": "BA Caraïbe", "type": "BA", "ordre": 2, "modifie_par": None, "modifie_le": None},
    {"id": 11, "grille_id": 2, "heure_debut": "06:48", "duree": 5, "titre": "Écran pub", "type": "PUB", "ordre": 3, "modifie_par": None, "modifie_le": None},
    {"id": 12, "grille_id": 2, "heure_debut": "06:53", "duree": 52, "titre": "Miel Amargo", "type": "PROG", "ordre": 4, "modifie_par": None, "modifie_le": None},
    {"id": 13, "grille_id": 2, "heure_debut": "07:45", "duree": 5, "titre": "Écran pub", "type": "PUB", "ordre": 5, "modifie_par": None, "modifie_le": None},
    {"id": 14, "grille_id": 2, "heure_debut": "07:50", "duree": 45, "titre": "Corazon Salvaje", "type": "PROG", "ordre": 6, "modifie_par": None, "modifie_le": None},

    # Jumbo Jamboo (grille_id: 3)
    {"id": 15, "grille_id": 3, "heure_debut": "06:00", "duree": 30, "titre": "Morning Show Ethiopia", "type": "PROG", "ordre": 1, "modifie_par": None, "modifie_le": None},
    {"id": 16, "grille_id": 3, "heure_debut": "06:30", "duree": 3, "titre": "BA Jumbo", "type": "BA", "ordre": 2, "modifie_par": None, "modifie_le": None},
    {"id": 17, "grille_id": 3, "heure_debut": "06:33", "duree": 5, "titre": "Écran pub", "type": "PUB", "ordre": 3, "modifie_par": None, "modifie_le": None},
    {"id": 18, "grille_id": 3, "heure_debut": "06:38", "duree": 60, "titre": "Ye Ethiopia Lij", "type": "PROG", "ordre": 4, "modifie_par": None, "modifie_le": None},
    {"id": 19, "grille_id": 3, "heure_debut": "07:38", "duree": 5, "titre": "Écran pub", "type": "PUB", "ordre": 5, "modifie_par": None, "modifie_le": None},
    {"id": 20, "grille_id": 3, "heure_debut": "07:43", "duree": 45, "titre": "Habesha Drama", "type": "PROG", "ordre": 6, "modifie_par": None, "modifie_le": None},

    # Maboke (grille_id: 4)
    {"id": 21, "grille_id": 4, "heure_debut": "06:00", "duree": 45, "titre": "Sango ya Mokili", "type": "PROG", "ordre": 1, "modifie_par": None, "modifie_le": None},
    {"id": 22, "grille_id": 4, "heure_debut": "06:45", "duree": 3, "titre": "BA Maboke", "type": "BA", "ordre": 2, "modifie_par": None, "modifie_le": None},
    {"id": 23, "grille_id": 4, "heure_debut": "06:48", "duree": 5, "titre": "Écran pub", "type": "PUB", "ordre": 3, "modifie_par": None, "modifie_le": None},
    {"id": 24, "grille_id": 4, "heure_debut": "06:53", "duree": 52, "titre": "Ndoto ya Maisha", "type": "PROG", "ordre": 4, "modifie_par": None, "modifie_le": None},
    {"id": 25, "grille_id": 4, "heure_debut": "07:45", "duree": 5, "titre": "Écran pub", "type": "PUB", "ordre": 5, "modifie_par": None, "modifie_le": None},
    {"id": 26, "grille_id": 4, "heure_debut": "07:50", "duree": 30, "titre": "Habari za Asubuhi", "type": "PROG", "ordre": 6, "modifie_par": None, "modifie_le": None},

    # Sunu Yeuf (grille_id: 5)
    {"id": 27, "grille_id": 5, "heure_debut": "06:00", "duree": 30, "titre": "Xibaar yi", "type": "PROG", "ordre": 1, "modifie_par": None, "modifie_le": None},
    {"id": 28, "grille_id": 5, "heure_debut": "06:30", "duree": 3, "titre": "BA Sunu Yeuf", "type": "BA", "ordre": 2, "modifie_par": None, "modifie_le": None},
    {"id": 29, "grille_id": 5, "heure_debut": "06:33", "duree": 5, "titre": "Écran pub", "type": "PUB", "ordre": 3, "modifie_par": None, "modifie_le": None},
    {"id": 30, "grille_id": 5, "heure_debut": "06:38", "duree": 45, "titre": "Dëkk yi", "type": "PROG", "ordre": 4, "modifie_par": None, "modifie_le": None},
    {"id": 31, "grille_id": 5, "heure_debut": "07:23", "duree": 5, "titre": "Écran pub", "type": "PUB", "ordre": 5, "modifie_par": None, "modifie_le": None},
    {"id": 32, "grille_id": 5, "heure_debut": "07:28", "duree": 52, "titre": "Lamb wi", "type": "PROG", "ordre": 6, "modifie_par": None, "modifie_le": None},
]

historique_db = []
sessions_actives = {}  # room_id -> liste de users connectés

# ─── MODÈLES ────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str
    password: str

class ModifCreneauRequest(BaseModel):
    titre: Optional[str] = None
    heure_debut: Optional[str] = None
    duree: Optional[int] = None
    type: Optional[str] = None
    modifie_par: str

# ─── GESTIONNAIRE WEBSOCKET ──────────────────────────────────

class WebSocketManager:
    def __init__(self):
        self.active_connections: dict[str, list] = {}

    async def connect(self, websocket: WebSocket, room_id: str, user_prenom: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append({"ws": websocket, "prenom": user_prenom})
        await self.broadcast(room_id, {
            "type": "user_connected",
            "message": f"{user_prenom} a rejoint la room",
            "users": self.get_users(room_id)
        }, exclude=websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            self.active_connections[room_id] = [
                c for c in self.active_connections[room_id] if c["ws"] != websocket
            ]

    def get_users(self, room_id: str):
        if room_id not in self.active_connections:
            return []
        return [c["prenom"] for c in self.active_connections[room_id]]

    async def broadcast(self, room_id: str, message: dict, exclude=None):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                if connection["ws"] != exclude:
                    await connection["ws"].send_json(message)

manager = WebSocketManager()

# ─── ROUTES ──────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "ChronoGrid API", "status": "ok"}

@app.post("/auth/login")
def login(request: LoginRequest):
    user = next((u for u in users_db if u["email"] == request.email and u["password"] == request.password), None)
    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    return {
        "id": user["id"],
        "nom": user["nom"],
        "prenom": user["prenom"],
        "email": user["email"],
        "role": user["role"]
    }

@app.get("/chaines")
def get_chaines():
    return chaines_db

@app.get("/creneaux/{grille_id}")
def get_creneaux(grille_id: int):
    creneaux = [c for c in creneaux_db if c["grille_id"] == grille_id]
    return creneaux

@app.patch("/creneaux/{creneau_id}")
async def modifier_creneau(creneau_id: int, request: ModifCreneauRequest):
    creneau = next((c for c in creneaux_db if c["id"] == creneau_id), None)
    if not creneau:
        raise HTTPException(status_code=404, detail="Créneau non trouvé")
    
    # Sauvegarder dans historique
    historique_db.append({
        "creneau_id": creneau_id,
        "user": request.modifie_par,
        "ancienne_valeur": dict(creneau),
        "date": datetime.now().isoformat()
    })
    
    # Modifier le créneau
    if request.titre: creneau["titre"] = request.titre
    if request.heure_debut: creneau["heure_debut"] = request.heure_debut
    if request.duree: creneau["duree"] = request.duree
    if request.type: creneau["type"] = request.type
    creneau["modifie_par"] = request.modifie_par
    creneau["modifie_le"] = datetime.now().isoformat()

    # Broadcaster à tous les connectés
    await manager.broadcast(str(creneau["grille_id"]), {
        "type": "creneau_modifie",
        "creneau": creneau,
        "modifie_par": request.modifie_par
    })

    return creneau

@app.get("/historique/{creneau_id}")
def get_historique(creneau_id: int):
    return [h for h in historique_db if h["creneau_id"] == creneau_id]

@app.websocket("/ws/{grille_id}/{user_prenom}")
async def websocket_endpoint(websocket: WebSocket, grille_id: str, user_prenom: str):
    await manager.connect(websocket, grille_id, user_prenom)
    try:
        # Envoyer la liste des users connectés au nouvel arrivant
        await websocket.send_json({
            "type": "connected",
            "message": f"Connecté à la room {grille_id}",
            "users": manager.get_users(grille_id)
        })
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, grille_id)
        await manager.broadcast(grille_id, {
            "type": "user_disconnected",
            "users": manager.get_users(grille_id)
        })