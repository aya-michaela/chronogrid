"""Mesure réelle des temps de réponse (à lancer en local : python tests/bench.py)."""
import os, sys, time, statistics
os.environ["DATABASE_URL"] = "sqlite:///./bench_chronogrid.db"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fastapi.testclient import TestClient
from database import Base, engine
import main

Base.metadata.drop_all(bind=engine); main.init_db()
N = 200
with TestClient(main.app) as c:
    tok = c.post("/auth/login", json={"email": "aya@canalplus.ci", "password": "aya123"}).json()["access_token"]
    h = {"Authorization": f"Bearer {tok}"}
    def bench(name, fn):
        t = []
        for _ in range(N):
            s = time.perf_counter(); fn(); t.append((time.perf_counter() - s) * 1000)
        t.sort()
        print(f"{name:28s} moy={statistics.mean(t):6.1f} ms  médiane={t[N//2]:6.1f}  p95={t[int(N*.95)]:6.1f}")
    bench("GET /chaines", lambda: c.get("/chaines", headers=h))
    bench("GET /creneaux/1", lambda: c.get("/creneaux/1", headers=h))
    bench("PATCH /creneaux/1", lambda: c.patch("/creneaux/1", json={"duree": 52}, headers=h))
    bench("POST /auth/login (bcrypt)", lambda: c.post("/auth/login", json={"email": "aya@canalplus.ci", "password": "aya123"}))
