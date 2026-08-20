# ChronoGrid — README

## Présentation
ChronoGrid est une application web collaborative de gestion de grilles de programmation en temps réel, développée dans le cadre du Bachelor DBI à NEXA Digital School.

**Auteure :** Aya KONAN  
**Titre visé :** Chef de projet web — RNCP40857  
**Entreprise :** Canal+ Côte d'Ivoire  
**Année :** 2025-2026

## Stack technique
- **Front-end :** React.js + Vite
- **Back-end :** Python 3.14 + FastAPI
- **Temps réel :** WebSockets natif FastAPI
- **Base de données :** PostgreSQL
- **Hébergement :** Render

## Prérequis
- Python 3.10+
- Node.js 18+
- npm

## Installation

### Back-end
cd backend
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib python-multipart
uvicorn main:app --reload
API : http://127.0.0.1:8000
Swagger : http://127.0.0.1:8000/docs

### Front-end
cd frontend
npm install
npm run dev
App : http://localhost:5173

## Comptes de test
aya@canalplus.ci / aya123 (Admin)
sophie@canalplus.ci / sophie123 (Assistante)
marie@canalplus.ci / marie123 (Assistante)

## Fonctionnalités
- Authentification sécurisée
- Tableau de bord avec toutes les chaînes
- Éditeur de grille collaboratif en temps réel
- Modifications visibles instantanément via WebSockets
- Historique des modifications
- Notifications toast temps réel
- Présence des utilisateurs connectés

## Structure du projet
chronogrid/
├── backend/
│   ├── main.py
│   ├── chronogrid.sql
│   └── README.md
└── frontend/
    └── src/
        ├── App.jsx
        ├── Login.jsx
        ├── Dashboard.jsx
        ├── Grille.jsx
        └── api.js

## URL publique
https://chronogrid.onrender.com