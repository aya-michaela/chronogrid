import { useState } from "react";
import { login } from "./api";

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [erreur, setErreur] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErreur("");
    try {
      const res = await login(email, password);
      onLogin(res.data);
    } catch (err) {
      setErreur("Email ou mot de passe incorrect");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.header}>
          <h1 style={styles.logo}>ChronoGrid</h1>
          <p style={styles.subtitle}>Gestion collaborative de grilles de programmation</p>
        </div>
        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.field}>
            <label style={styles.label}>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="aya@canalplus.ci"
              style={styles.input}
              required
            />
          </div>
          <div style={styles.field}>
            <label style={styles.label}>Mot de passe</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              style={styles.input}
              required
            />
          </div>
          {erreur && <p style={styles.erreur}>{erreur}</p>}
          <button type="submit" style={styles.btn} disabled={loading}>
            {loading ? "Connexion..." : "SE CONNECTER"}
          </button>
        </form>
        <p style={styles.hint}>
          Comptes test : aya@canalplus.ci / aya123
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    backgroundColor: "#111111",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  card: {
    backgroundColor: "#1a1a1a",
    borderRadius: "8px",
    padding: "40px",
    width: "400px",
    boxShadow: "0 4px 20px rgba(0,0,0,0.5)",
  },
  header: {
    textAlign: "center",
    marginBottom: "32px",
  },
  logo: {
    color: "#E8000D",
    fontSize: "32px",
    fontWeight: "bold",
    margin: "0 0 8px 0",
    fontFamily: "Arial Black, sans-serif",
  },
  subtitle: {
    color: "#888",
    fontSize: "13px",
    margin: 0,
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "16px",
  },
  field: {
    display: "flex",
    flexDirection: "column",
    gap: "6px",
  },
  label: {
    color: "#ccc",
    fontSize: "13px",
  },
  input: {
    padding: "10px 14px",
    borderRadius: "4px",
    border: "1px solid #333",
    backgroundColor: "#222",
    color: "#fff",
    fontSize: "14px",
    outline: "none",
  },
  erreur: {
    color: "#E8000D",
    fontSize: "13px",
    margin: 0,
  },
  btn: {
    padding: "12px",
    backgroundColor: "#E8000D",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    fontSize: "14px",
    fontWeight: "bold",
    cursor: "pointer",
    letterSpacing: "1px",
    marginTop: "8px",
  },
  hint: {
    color: "#555",
    fontSize: "12px",
    textAlign: "center",
    marginTop: "20px",
  },
};