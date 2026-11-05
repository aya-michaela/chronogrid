import json
from sqlalchemy import text
from database import SessionLocal
import models
from security import verify_password, create_token, decode_token


# ---- Tests unitaires ----
def test_password_is_hashed_not_plaintext(client):
    db = SessionLocal()
    u = db.query(models.User).filter_by(email="aya@canalplus.ci").first()
    assert u.password_hash != "aya123"
    assert verify_password("aya123", u.password_hash)
    assert not verify_password("mauvais", u.password_hash)
    db.close()


def test_token_roundtrip_and_tampering():
    t = create_token(1, "admin")
    assert decode_token(t)["sub"] == "1"
    assert decode_token(t + "x") is None
    assert decode_token("n'importe quoi") is None


# ---- Tests d'intégration ----
def test_login_ok(client):
    r = client.post("/auth/login", json={"email": "aya@canalplus.ci", "password": "aya123"})
    assert r.status_code == 200
    body = r.json()
    assert body["token_type"] == "bearer" and body["user"]["prenom"] == "Aya"
    assert "password" not in json.dumps(body)


def test_login_wrong_password(client):
    r = client.post("/auth/login", json={"email": "aya@canalplus.ci", "password": "faux"})
    assert r.status_code == 401


def test_routes_require_token(client):
    assert client.get("/chaines").status_code == 401
    assert client.get("/creneaux/1").status_code == 401
    assert client.patch("/creneaux/1", json={"titre": "X"}).status_code == 401


def test_invalid_token_rejected(client):
    r = client.get("/chaines", headers={"Authorization": "Bearer faux.jeton.ici"})
    assert r.status_code == 401


def test_list_chaines_and_creneaux(client, auth):
    assert len(client.get("/chaines", headers=auth).json()) == 5
    cr = client.get("/creneaux/1", headers=auth).json()
    assert len(cr) == 8
    assert [c["ordre"] for c in cr] == sorted(c["ordre"] for c in cr)


def test_patch_creneau_updates_and_logs_history(client, auth):
    r = client.patch("/creneaux/1", json={"titre": "Nouveau titre"}, headers=auth)
    assert r.status_code == 200
    assert r.json()["titre"] == "Nouveau titre"
    assert r.json()["modifie_par"] == "Aya"
    h = client.get("/historique/1", headers=auth).json()
    assert len(h) == 1 and h[0]["ancienne_valeur"]["titre"] == "Destinos"


def test_patch_unknown_creneau_404(client, auth):
    assert client.patch("/creneaux/9999", json={"titre": "X"}, headers=auth).status_code == 404


def test_patch_validation_errors(client, auth):
    assert client.patch("/creneaux/1", json={"heure_debut": "25:99"}, headers=auth).status_code == 422
    assert client.patch("/creneaux/1", json={"duree": -5}, headers=auth).status_code == 422
    assert client.patch("/creneaux/1", json={"type": "XXX"}, headers=auth).status_code == 422


def test_sql_injection_attempt_is_harmless(client, auth):
    client.post("/auth/login", json={"email": "' OR 1=1 --", "password": "x"})
    r = client.post("/auth/login", json={"email": "' OR 1=1 --", "password": "x"})
    assert r.status_code == 401
    r = client.patch("/creneaux/1", json={"titre": "'; DROP TABLE creneaux; --"}, headers=auth)
    assert r.status_code == 200
    assert len(client.get("/creneaux/1", headers=auth).json()) == 8


def test_websocket_requires_valid_token(client):
    import pytest
    from starlette.websockets import WebSocketDisconnect
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/ws/1?token=faux"):
            pass


def test_websocket_broadcast_on_patch(client, auth, token):
    with client.websocket_connect(f"/ws/1?token={token}") as ws:
        assert ws.receive_json()["type"] == "connected"
        client.patch("/creneaux/2", json={"titre": "BA modifiée"}, headers=auth)
        msg = ws.receive_json()
        assert msg["type"] == "creneau_modifie" and msg["creneau"]["titre"] == "BA modifiée"
