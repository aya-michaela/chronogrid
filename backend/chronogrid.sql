-- ============================================
-- ChronoGrid — Script SQL
-- Bachelor DBI — NEXA Digital School
-- Aya KONAN — 2025-2026
-- ============================================

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    role VARCHAR(50) DEFAULT 'assistante',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des chaînes
CREATE TABLE IF NOT EXISTS chaines (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des grilles
CREATE TABLE IF NOT EXISTS grilles (
    id SERIAL PRIMARY KEY,
    chaine_id INTEGER REFERENCES chaines(id),
    date_diffusion DATE NOT NULL,
    statut VARCHAR(20) DEFAULT 'brouillon',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    validated_at TIMESTAMP,
    validated_by INTEGER REFERENCES users(id)
);

-- Table des créneaux
CREATE TABLE IF NOT EXISTS creneaux (
    id SERIAL PRIMARY KEY,
    grille_id INTEGER REFERENCES grilles(id),
    heure_debut TIME NOT NULL,
    duree INTEGER NOT NULL,
    titre VARCHAR(200) NOT NULL,
    type_contenu VARCHAR(20) NOT NULL,
    ordre INTEGER NOT NULL,
    last_modified_by INTEGER REFERENCES users(id),
    last_modified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table de l'historique des modifications
CREATE TABLE IF NOT EXISTS historique_modifications (
    id SERIAL PRIMARY KEY,
    creneau_id INTEGER REFERENCES creneaux(id),
    user_id INTEGER REFERENCES users(id),
    champ_modifie VARCHAR(100),
    ancienne_valeur TEXT,
    nouvelle_valeur TEXT,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des sessions room
CREATE TABLE IF NOT EXISTS sessions_room (
    id SERIAL PRIMARY KEY,
    grille_id INTEGER REFERENCES grilles(id),
    user_id INTEGER REFERENCES users(id),
    connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    disconnected_at TIMESTAMP
);

-- ============================================
-- DONNÉES DE TEST
-- ============================================

-- Utilisateurs
INSERT INTO users (nom, prenom, email, password_hash, role) VALUES
('Konan', 'Aya', 'aya@canalplus.ci', 'aya123', 'admin'),
('Diallo', 'Sophie', 'sophie@canalplus.ci', 'sophie123', 'assistante'),
('Traoré', 'Marie', 'marie@canalplus.ci', 'marie123', 'assistante');

-- Chaînes
INSERT INTO chaines (nom, code, description) VALUES
('Novelas CI', 'NOV_CI', 'Chaîne de telenovelas Côte d Ivoire'),
('Novelas Caraïbe', 'NOV_CAR', 'Chaîne de telenovelas Caraïbe'),
('Jumbo Jamboo', 'JJB', 'Chaîne éthiopienne'),
('Maboke', 'MBK', 'Chaîne africaine'),
('Sunu Yeuf', 'SNY', 'Chaîne sénégalaise');

-- Grilles
INSERT INTO grilles (chaine_id, date_diffusion, statut) VALUES
(1, CURRENT_DATE, 'brouillon'),
(2, CURRENT_DATE, 'brouillon'),
(3, CURRENT_DATE, 'brouillon'),
(4, CURRENT_DATE, 'brouillon'),
(5, CURRENT_DATE, 'brouillon');

-- Créneaux Novelas CI
INSERT INTO creneaux (grille_id, heure_debut, duree, titre, type_contenu, ordre) VALUES
(1, '06:00', 52, 'Destinos', 'PROG', 1),
(1, '06:52', 3, 'BA Novelas', 'BA', 2),
(1, '06:55', 5, 'Écran pub', 'PUB', 3),
(1, '07:00', 45, 'Amor Prohibido', 'PROG', 4),
(1, '07:45', 5, 'Écran pub', 'PUB', 5),
(1, '07:50', 52, 'La Reina del Sur', 'PROG', 6),
(1, '08:42', 3, 'BA Novelas', 'BA', 7),
(1, '08:45', 45, 'Pasión de Gavilanes', 'PROG', 8);

-- Créneaux Jumbo Jamboo
INSERT INTO creneaux (grille_id, heure_debut, duree, titre, type_contenu, ordre) VALUES
(3, '06:00', 30, 'Morning Show Ethiopia', 'PROG', 1),
(3, '06:30', 3, 'BA Jumbo', 'BA', 2),
(3, '06:33', 5, 'Écran pub', 'PUB', 3),
(3, '06:38', 60, 'Ye Ethiopia Lij', 'PROG', 4),
(3, '07:38', 5, 'Écran pub', 'PUB', 5),
(3, '07:43', 45, 'Habesha Drama', 'PROG', 6);