from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Index
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    nom = Column(String(80), nullable=False)
    prenom = Column(String(80), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default="assistante")


class Chaine(Base):
    __tablename__ = "chaines"
    id = Column(Integer, primary_key=True)
    nom = Column(String(80), nullable=False)
    code = Column(String(20), unique=True, nullable=False)


class Creneau(Base):
    __tablename__ = "creneaux"
    id = Column(Integer, primary_key=True)
    grille_id = Column(Integer, ForeignKey("chaines.id"), nullable=False)
    heure_debut = Column(String(5), nullable=False)
    duree = Column(Integer, nullable=False)
    titre = Column(String(120), nullable=False)
    type = Column(String(10), nullable=False)
    ordre = Column(Integer, nullable=False)
    modifie_par = Column(String(80))
    modifie_le = Column(DateTime)
    __table_args__ = (Index("ix_creneaux_grille_ordre", "grille_id", "ordre"),)


class Historique(Base):
    __tablename__ = "historique"
    id = Column(Integer, primary_key=True)
    creneau_id = Column(Integer, ForeignKey("creneaux.id"), nullable=False, index=True)
    user = Column(String(80), nullable=False)
    ancienne_valeur = Column(Text, nullable=False)  # JSON
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
