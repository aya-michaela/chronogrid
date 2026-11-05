import { useState } from "react";
import { setToken } from "./api";
import Login from "./Login";
import Dashboard from "./Dashboard";
import Grille from "./Grille";

export default function App() {
  const [user, setUser] = useState(null);
  const [chaineSelectionnee, setChaineSelectionnee] = useState(null);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setToken(null);
    setUser(null);
    setChaineSelectionnee(null);
  };

  const handleSelectChaine = (chaine) => {
    setChaineSelectionnee(chaine);
  };

  const handleRetour = () => {
    setChaineSelectionnee(null);
  };

  // Pas connecté → page de login
  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  // Connecté + chaîne sélectionnée → éditeur de grille
  if (chaineSelectionnee) {
    return (
      <Grille
        user={user}
        chaine={chaineSelectionnee}
        onRetour={handleRetour}
      />
    );
  }

  // Connecté → tableau de bord
  return (
    <Dashboard
      user={user}
      onSelectChaine={handleSelectChaine}
      onLogout={handleLogout}
    />
  );
}
