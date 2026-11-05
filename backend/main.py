import json
import os
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import models
import seed_data
from database import Base, engine, get_db, SessionLocal
from security import hash_password, verify_password, create_token, decode_token

app = FastAPI(title="ChronoGrid API")

ORIGINS = ["http://localhost:5173", "https://chronogrid-frontend.onrender.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bearer = HTTPBearer(auto_error=False)
TYPES_VALIDES = {"PROG", "BA", "PUB"}


# ---------- Initialisation / données de démonstration ----------
def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(models.User).count() == 0:
            for u in seed_data.users_db:
                db.add(models.User(
                    id=u["id"], nom=u["nom"], prenom=u["prenom"], email=u["email"],
                    password_hash=hash_password(u["password"]), role=u["role"]))
            for c in seed_data.chaines_db:
                db.add(models.Chaine(**c))
            for c in seed_data.creneaux_db:
                db.add(models.Creneau(**c))
            db.commit()
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    init_db()


# ---------- Schémas ----------
class LoginRequest(BaseModel):
    email: str
    password: str


class ModifCreneauRequest(BaseModel):
    titre: Optional[str] = Field(None, min_length=1, max_length=120)
    heure_debut: Optional[str] = Field(None, pattern=r"^([01]\d|2[0-3]):[0-5]\d$")
    duree: Optional[int] = Field(None, gt=0, le=600)
    type: Optional[str] = None


# ---------- Authentification ----------
def current_user(
    cred: Optional[HTTPAuthorizationCredentials] = Depends(bearer),
    db: Session = Depends(get_db),
) -> models.User:
    payload = decode_token(cred.credentials) if cred else None
    if not payload:
        raise HTTPException(status_code=401, detail="Authentification requise")
    user = db.get(models.User, int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="Utilisateur inconnu")
    return user


def creneau_dict(c: models.Creneau) -> dict:
    return {
        "id": c.id, "grille_id": c.grille_id, "heure_debut": c.heure_debut,
        "duree": c.duree, "titre": c.titre, "type": c.type, "ordre": c.ordre,
        "modifie_par": c.modifie_par,
        "modifie_le": c.modifie_le.isoformat() if c.modifie_le else None,
    }


# ---------- WebSocket ----------
class WebSocketManager:
    def __init__(self):
        self.active_connections: dict[str, list] = {}

    async def connect(self, websocket: WebSocket, room_id: str, user_prenom: str):
        await websocket.accept()
        self.active_connections.setdefault(room_id, []).append({"ws": websocket, "prenom": user_prenom})
        await self.broadcast(room_id, {
            "type": "user_connected",
            "message": f"{user_prenom} a rejoint la room",
            "users": self.get_users(room_id),
        }, exclude=websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            self.active_connections[room_id] = [
                c for c in self.active_connections[room_id] if c["ws"] != websocket]

    def get_users(self, room_id: str):
        return [c["prenom"] for c in self.active_connections.get(room_id, [])]

    async def broadcast(self, room_id: str, message: dict, exclude=None):
        for connection in list(self.active_connections.get(room_id, [])):
            if connection["ws"] != exclude:
                await connection["ws"].send_json(message)


manager = WebSocketManager()


# ---------- Routes ----------
@app.get("/")
def root():
    return {"message": "ChronoGrid API", "status": "ok"}


@app.post("/auth/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    return {
        "access_token": create_token(user.id, user.role),
        "token_type": "bearer",
        "user": {"id": user.id, "nom": user.nom, "prenom": user.prenom,
                 "email": user.email, "role": user.role},
    }


@app.get("/chaines")
def get_chaines(db: Session = Depends(get_db), _: models.User = Depends(current_user)):
    return [{"id": c.id, "nom": c.nom, "code": c.code} for c in db.query(models.Chaine).all()]


@app.get("/creneaux/{grille_id}")
def get_creneaux(grille_id: int, db: Session = Depends(get_db), _: models.User = Depends(current_user)):
    rows = (db.query(models.Creneau).filter(models.Creneau.grille_id == grille_id)
            .order_by(models.Creneau.ordre).all())
    return [creneau_dict(c) for c in rows]


@app.patch("/creneaux/{creneau_id}")
async def modifier_creneau(
    creneau_id: int,
    request: ModifCreneauRequest,
    db: Session = Depends(get_db),
    user: models.User = Depends(current_user),
):
    creneau = db.get(models.Creneau, creneau_id)
    if not creneau:
        raise HTTPException(status_code=404, detail="Créneau non trouvé")
    if request.type is not None and request.type not in TYPES_VALIDES:
        raise HTTPException(status_code=422, detail="Type invalide (PROG, BA ou PUB)")

    db.add(models.Historique(
        creneau_id=creneau_id, user=user.prenom,
        ancienne_valeur=json.dumps(creneau_dict(creneau)), date=datetime.utcnow()))
    if request.titre: creneau.titre = request.titre
    if request.heure_debut: creneau.heure_debut = request.heure_debut
    if request.duree: creneau.duree = request.duree
    if request.type: creneau.type = request.type
    creneau.modifie_par = user.prenom  # identité issue du jeton, non falsifiable
    creneau.modifie_le = datetime.utcnow()
    db.commit()
    db.refresh(creneau)

    data = creneau_dict(creneau)
    await manager.broadcast(str(creneau.grille_id), {
        "type": "creneau_modifie", "creneau": data, "modifie_par": user.prenom})
    return data


@app.get("/historique/{creneau_id}")
def get_historique(creneau_id: int, db: Session = Depends(get_db), _: models.User = Depends(current_user)):
    rows = (db.query(models.Historique).filter(models.Historique.creneau_id == creneau_id)
            .order_by(models.Historique.id).all())
    return [{"creneau_id": h.creneau_id, "user": h.user,
             "ancienne_valeur": json.loads(h.ancienne_valeur),
             "date": h.date.isoformat()} for h in rows]


@app.websocket("/ws/{grille_id}")
async def websocket_endpoint(websocket: WebSocket, grille_id: str, token: str = Query(default="")):
    payload = decode_token(token)
    if not payload:
        await websocket.close(code=1008)  # policy violation
        return
    db = SessionLocal()
    try:
        user = db.get(models.User, int(payload["sub"]))
    finally:
        db.close()
    if not user:
        await websocket.close(code=1008)
        return
    prenom = user.prenom
    await manager.connect(websocket, grille_id, prenom)
    try:
        await websocket.send_json({
            "type": "connected",
            "message": f"Connecté à la room {grille_id}",
            "users": manager.get_users(grille_id)})
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, grille_id)
        await manager.broadcast(grille_id, {
            "type": "user_disconnected", "users": manager.get_users(grille_id)})
