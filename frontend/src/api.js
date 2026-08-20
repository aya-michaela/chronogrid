import axios from 'axios';

const API = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

// Auth
export const login = (email, password) =>
  API.post('/auth/login', { email, password });

// Chaînes
export const getChaines = () => API.get('/chaines');

// Créneaux
export const getCreneaux = (grilleId) => API.get(`/creneaux/${grilleId}`);

// Modifier un créneau
export const modifierCreneau = (creneauId, data) =>
  API.patch(`/creneaux/${creneauId}`, data);

// Historique
export const getHistorique = (creneauId) =>
  API.get(`/historique/${creneauId}`);

export default API;