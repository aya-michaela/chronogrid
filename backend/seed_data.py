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

