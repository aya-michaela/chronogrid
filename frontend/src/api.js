import axios from 'axios';

export const BASE_URL = 'https://chronogrid-backend-rpow.onrender.com';

const API = axios.create({ baseURL: BASE_URL });

// Jeton JWT gardé en mémoire (pas de localStorage : limite l'exposition en cas de XSS)
let token = null;
export const setToken = (t) => { token = t; };
export const getToken = () => token;

API.interceptors.request.use((config) => {
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
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