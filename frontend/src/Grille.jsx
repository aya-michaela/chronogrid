import { useState, useEffect, useRef } from "react";
import { getCreneaux, modifierCreneau } from "./api";

const TYPE_COLORS = {
  PROG: "#1a3a5c",
  BA: "#3a2a1a",
  PUB: "#1a3a1a",
  HABILLAGE: "#2a1a3a",
};

export default function Grille({ user, chaine, onRetour }) {
  const [creneaux, setCreneaux] = useState([]);
  const [usersConnectes, setUsersConnectes] = useState([user.prenom]);
  const [notifications, setNotifications] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [editData, setEditData] = useState({});
  const wsRef = useRef(null);

  useEffect(() => {
    getCreneaux(chaine.id).then((res) => setCreneaux(res.data));
  }, [chaine.id]);

  useEffect(() => {
    const ws = new WebSocket(
      `wss://chronogrid-backend-rpow.onrender.com/ws/${chaine.id}/${user.prenom}`
    );
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "creneau_modifie") {
        setCreneaux((prev) =>
          prev.map((c) => (c.id === data.creneau.id ? data.creneau : c))
        );
        ajouterNotification(`✓ ${data.modifie_par} a modifié "${data.creneau.titre}"`);
      }
      if (data.type === "user_connected") {
        setUsersConnectes(data.users);
        ajouterNotification(`👤 ${data.message}`);
      }
      if (data.type === "user_disconnected") {
        setUsersConnectes(data.users);
      }
      if (data.type === "connected") {
        setUsersConnectes(data.users);
      }
    };

    return () => ws.close();
  }, [chaine.id, user.prenom]);

  const ajouterNotification = (message) => {
    const id = Date.now();
    setNotifications((prev) => [...prev, { id, message }]);
    setTimeout(() => {
      setNotifications((prev) => prev.filter((n) => n.id !== id));
    }, 4000);
  };

  const startEdit = (creneau) => {
    setEditingId(creneau.id);
    setEditData({
      titre: creneau.titre,
      heure_debut: creneau.heure_debut,
      duree: creneau.duree,
      type: creneau.type,
    });
  };

  const saveEdit = async (creneauId) => {
    try {
      const res = await modifierCreneau(creneauId, {
        ...editData,
        modifie_par: user.prenom,
      });
      setCreneaux((prev) =>
        prev.map((c) => (c.id === creneauId ? res.data : c))
      );
      ajouterNotification(`✓ Modification sauvegardée`);
    } catch (err) {
      ajouterNotification("❌ Erreur lors de la modification");
    }
    setEditingId(null);
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div style={styles.headerLeft}>
          <button onClick={onRetour} style={styles.retourBtn}>← Retour</button>
          <div>
            <h1 style={styles.chaineName}>{chaine.nom}</h1>
            <p style={styles.date}>Grille du {new Date().toLocaleDateString("fr-FR")}</p>
          </div>
        </div>
        <div style={styles.usersConnectes}>
          {usersConnectes.map((u, i) => (
            <div key={i} style={styles.avatar}>{u[0]}</div>
          ))}
          <span style={styles.usersLabel}>{usersConnectes.length} connecté(s)</span>
        </div>
      </div>

      <div style={styles.toastContainer}>
        {notifications.map((n) => (
          <div key={n.id} style={styles.toast}>{n.message}</div>
        ))}
      </div>

      <div style={styles.tableContainer}>
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.th}>HEURE</th>
              <th style={styles.th}>DURÉE</th>
              <th style={styles.th}>CONTENU</th>
              <th style={styles.th}>TYPE</th>
              <th style={styles.th}>MODIFIÉ PAR</th>
              <th style={styles.th}>ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            {creneaux.map((c, i) => (
              <tr key={c.id} style={{
                backgroundColor: editingId === c.id ? "#1a2a3a" : (i % 2 === 0 ? "#1a1a1a" : "#111"),
              }}>
                {editingId === c.id ? (
                  <>
                    <td style={styles.td}>
                      <input
                        value={editData.heure_debut}
                        onChange={(e) => setEditData({ ...editData, heure_debut: e.target.value })}
                        style={styles.inputEdit}
                      />
                    </td>
                    <td style={styles.td}>
                      <input
                        type="number"
                        value={editData.duree}
                        onChange={(e) => setEditData({ ...editData, duree: parseInt(e.target.value) })}
                        style={{ ...styles.inputEdit, width: "60px" }}
                      />
                    </td>
                    <td style={styles.td}>
                      <input
                        value={editData.titre}
                        onChange={(e) => setEditData({ ...editData, titre: e.target.value })}
                        style={{ ...styles.inputEdit, width: "200px" }}
                      />
                    </td>
                    <td style={styles.td}>
                      <select
                        value={editData.type}
                        onChange={(e) => setEditData({ ...editData, type: e.target.value })}
                        style={styles.inputEdit}
                      >
                        <option>PROG</option>
                        <option>BA</option>
                        <option>PUB</option>
                        <option>HABILLAGE</option>
                      </select>
                    </td>
                    <td style={styles.td} colSpan={2}>
                      <button onClick={() => saveEdit(c.id)} style={styles.saveBtn}>✓ Sauvegarder</button>
                      <button onClick={() => setEditingId(null)} style={styles.cancelBtn}>✕ Annuler</button>
                    </td>
                  </>
                ) : (
                  <>
                    <td style={styles.td}>{c.heure_debut}</td>
                    <td style={styles.td}>{c.duree} min</td>
                    <td style={styles.td}>
                      <span style={{
                        ...styles.badge,
                        backgroundColor: TYPE_COLORS[c.type] || "#222",
                      }}>
                        {c.titre}
                      </span>
                    </td>
                    <td style={styles.td}>
                      <span style={styles.typeBadge}>{c.type}</span>
                    </td>
                    <td style={styles.td}>
                      <span style={{ color: c.modifie_par ? "#E8000D" : "#444", fontSize: "12px" }}>
                        {c.modifie_par || "—"}
                      </span>
                    </td>
                    <td style={styles.td}>
                      <button onClick={() => startEdit(c)} style={styles.editBtn}>✏️ Modifier</button>
                    </td>
                  </>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={styles.footer}>
        <span style={styles.footerText}>
          {creneaux.length} créneaux • Modifications en temps réel via WebSocket
        </span>
      </div>
    </div>
  );
}

const styles = {
  container: { minHeight: "100vh", backgroundColor: "#111", fontFamily: "Arial, sans-serif" },
  header: { backgroundColor: "#1a1a1a", padding: "16px 24px", display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "2px solid #E8000D" },
  headerLeft: { display: "flex", alignItems: "center", gap: "16px" },
  retourBtn: { padding: "6px 12px", backgroundColor: "transparent", color: "#888", border: "1px solid #444", borderRadius: "4px", cursor: "pointer", fontSize: "13px" },
  chaineName: { color: "#fff", margin: 0, fontSize: "20px", fontFamily: "Arial Black" },
  date: { color: "#888", margin: 0, fontSize: "12px" },
  usersConnectes: { display: "flex", alignItems: "center", gap: "8px" },
  avatar: { width: "32px", height: "32px", borderRadius: "50%", backgroundColor: "#E8000D", color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "14px", fontWeight: "bold" },
  usersLabel: { color: "#888", fontSize: "13px" },
  toastContainer: { position: "fixed", top: "80px", right: "20px", zIndex: 1000, display: "flex", flexDirection: "column", gap: "8px" },
  toast: { backgroundColor: "#1a1a1a", color: "#fff", padding: "10px 16px", borderRadius: "4px", border: "1px solid #333", borderLeft: "3px solid #E8000D", fontSize: "13px", boxShadow: "0 2px 8px rgba(0,0,0,0.4)" },
  tableContainer: { padding: "24px", overflowX: "auto" },
  table: { width: "100%", borderCollapse: "collapse" },
  th: { backgroundColor: "#1a1a1a", color: "#888", padding: "12px 16px", textAlign: "left", fontSize: "11px", letterSpacing: "1px", borderBottom: "1px solid #333" },
  td: { padding: "10px 16px", color: "#ddd", fontSize: "14px", borderBottom: "1px solid #222" },
  badge: { padding: "4px 10px", borderRadius: "4px", fontSize: "13px" },
  typeBadge: { padding: "2px 8px", borderRadius: "3px", backgroundColor: "#222", color: "#E8000D", fontSize: "11px", fontWeight: "bold", letterSpacing: "1px" },
  editBtn: { padding: "4px 10px", backgroundColor: "transparent", color: "#888", border: "1px solid #444", borderRadius: "4px", cursor: "pointer", fontSize: "12px" },
  saveBtn: { padding: "6px 12px", backgroundColor: "#E8000D", color: "#fff", border: "none", borderRadius: "4px", cursor: "pointer", fontSize: "12px", marginRight: "8px" },
  cancelBtn: { padding: "6px 12px", backgroundColor: "transparent", color: "#888", border: "1px solid #444", borderRadius: "4px", cursor: "pointer", fontSize: "12px" },
  inputEdit: { padding: "4px 8px", backgroundColor: "#222", color: "#fff", border: "1px solid #E8000D", borderRadius: "4px", fontSize: "13px" },
  footer: { padding: "16px 24px", borderTop: "1px solid #222" },
  footerText: { color: "#444", fontSize: "12px" },
};