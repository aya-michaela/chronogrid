import { useState, useEffect } from "react";
import { getChaines } from "./api";

export default function Dashboard({ user, onSelectChaine, onLogout }) {
  const [chaines, setChaines] = useState([]);

  useEffect(() => {
    getChaines().then((res) => setChaines(res.data));
  }, []);

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <h1 style={styles.logo}>ChronoGrid</h1>
        <div style={styles.userInfo}>
          <span style={styles.userName}>👤 {user.prenom} {user.nom}</span>
          <button onClick={onLogout} style={styles.logoutBtn}>Déconnexion</button>
        </div>
      </div>

      {/* Contenu */}
      <div style={styles.content}>
        <h2 style={styles.welcome}>Bonjour {user.prenom} 👋</h2>
        <p style={styles.subtitle}>Sélectionnez une chaîne pour accéder à sa grille de programmation</p>

        {/* Grille des chaînes */}
        <div style={styles.grid}>
          {chaines.map((chaine) => (
            <div
              key={chaine.id}
              style={styles.chaineCard}
              onClick={() => onSelectChaine(chaine)}
              onMouseEnter={(e) => e.currentTarget.style.borderColor = "#E8000D"}
              onMouseLeave={(e) => e.currentTarget.style.borderColor = "#333"}
            >
              <div style={styles.chaineCode}>{chaine.code}</div>
              <div style={styles.chaineName}>{chaine.nom}</div>
              <div style={styles.chaineAction}>Ouvrir la grille →</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    backgroundColor: "#111111",
    fontFamily: "Arial, sans-serif",
  },
  header: {
    backgroundColor: "#1a1a1a",
    padding: "16px 32px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    borderBottom: "2px solid #E8000D",
  },
  logo: {
    color: "#E8000D",
    margin: 0,
    fontSize: "24px",
    fontFamily: "Arial Black, sans-serif",
  },
  userInfo: {
    display: "flex",
    alignItems: "center",
    gap: "16px",
  },
  userName: {
    color: "#ccc",
    fontSize: "14px",
  },
  logoutBtn: {
    padding: "6px 14px",
    backgroundColor: "transparent",
    color: "#888",
    border: "1px solid #444",
    borderRadius: "4px",
    cursor: "pointer",
    fontSize: "13px",
  },
  content: {
    padding: "40px 32px",
  },
  welcome: {
    color: "#fff",
    fontSize: "28px",
    margin: "0 0 8px 0",
  },
  subtitle: {
    color: "#888",
    fontSize: "14px",
    marginBottom: "32px",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
    gap: "20px",
  },
  chaineCard: {
    backgroundColor: "#1a1a1a",
    border: "1px solid #333",
    borderRadius: "8px",
    padding: "24px",
    cursor: "pointer",
    transition: "border-color 0.2s",
  },
  chaineCode: {
    color: "#E8000D",
    fontSize: "12px",
    fontWeight: "bold",
    letterSpacing: "2px",
    marginBottom: "8px",
  },
  chaineName: {
    color: "#fff",
    fontSize: "18px",
    fontWeight: "bold",
    marginBottom: "16px",
  },
  chaineAction: {
    color: "#666",
    fontSize: "13px",
  },
};