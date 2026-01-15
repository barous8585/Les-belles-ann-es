import streamlit as st
from utils.auth import get_current_user
import sqlite3
from datetime import datetime

def show():
    user = get_current_user()
    st.title("🔧 Gestion de la Maintenance")
    
    tab1, tab2, tab3 = st.tabs(["📝 Signaler un incident", "📊 Mes incidents", "📈 Statistiques"])
    
    with tab1:
        signaler_incident(user)
    
    with tab2:
        mes_incidents(user)
    
    with tab3:
        if user['type'] in ['Gestionnaire', 'Personnel']:
            statistiques_maintenance()
        else:
            st.info("Statistiques disponibles uniquement pour les gestionnaires")

def signaler_incident(user):
    st.subheader("Signaler un nouveau problème")
    
    with st.form("signalement_incident"):
        col1, col2 = st.columns(2)
        
        with col1:
            titre = st.text_input("Titre du problème")
            categorie = st.selectbox("Catégorie", [
                "Plomberie",
                "Électricité", 
                "Chauffage/Climatisation",
                "Ascenseur",
                "Serrurerie",
                "Équipements (cuisine, salle de bain)",
                "Internet/WiFi",
                "Nuisances sonores",
                "Propreté",
                "Autre"
            ])
            priorite = st.selectbox("Urgence", [
                "Faible - Peut attendre quelques jours",
                "Moyenne - À traiter cette semaine",
                "Haute - Urgent, intervention rapide nécessaire",
                "Critique - Danger ou problème majeur"
            ])
        
        with col2:
            description = st.text_area("Description détaillée du problème", height=150)
            photo = st.file_uploader("Photo (optionnel)", type=['jpg', 'jpeg', 'png'])
        
        submit = st.form_submit_button("📤 Envoyer le signalement")
        
        if submit:
            if titre and description:
                priorite_simple = priorite.split(" - ")[0]
                
                conn = sqlite3.connect("data/lba_platform.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO incidents (titre, description, categorie, priorite, residence, logement, user_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (titre, description, categorie, priorite_simple, user['residence'], user['logement'], user['id']))
                conn.commit()
                conn.close()
                
                st.success("✅ Incident signalé avec succès ! Notre équipe va intervenir rapidement.")
                st.balloons()
                st.rerun()
            else:
                st.error("Veuillez remplir tous les champs obligatoires")

def mes_incidents(user):
    st.subheader("Historique de vos signalements")
    
    conn = sqlite3.connect("data/lba_platform.db")
    cursor = conn.cursor()
    
    if user['type'] in ['Gestionnaire', 'Personnel']:
        cursor.execute("""
            SELECT i.id, i.titre, i.description, i.categorie, i.priorite, i.statut, 
                   i.date_creation, i.date_resolution, u.prenom, u.nom, i.logement
            FROM incidents i
            JOIN users u ON i.user_id = u.id
            WHERE i.residence = ?
            ORDER BY i.date_creation DESC
        """, (user['residence'],))
    else:
        cursor.execute("""
            SELECT id, titre, description, categorie, priorite, statut, date_creation, date_resolution
            FROM incidents
            WHERE user_id = ?
            ORDER BY date_creation DESC
        """, (user['id'],))
    
    incidents = cursor.fetchall()
    
    if incidents:
        statut_filter = st.multiselect(
            "Filtrer par statut",
            ["nouveau", "en_cours", "résolu"],
            default=["nouveau", "en_cours"]
        )
        
        for incident in incidents:
            if user['type'] in ['Gestionnaire', 'Personnel']:
                inc_id, titre, desc, cat, prio, statut, date_c, date_r, prenom, nom, logement = incident
            else:
                inc_id, titre, desc, cat, prio, statut, date_c, date_r = incident
            
            if statut not in statut_filter:
                continue
            
            statut_emoji = {"nouveau": "🆕", "en_cours": "⏳", "résolu": "✅"}
            priorite_emoji = {"Faible": "🟢", "Moyenne": "🟡", "Haute": "🟠", "Critique": "🔴"}
            
            with st.expander(f"{statut_emoji.get(statut, '')} {titre} - {statut}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Catégorie:** {cat}")
                    st.write(f"**Priorité:** {priorite_emoji.get(prio, '')} {prio}")
                    st.write(f"**Statut:** {statut}")
                    if user['type'] in ['Gestionnaire', 'Personnel']:
                        st.write(f"**Résident:** {prenom} {nom} - Logement {logement}")
                
                with col2:
                    st.write(f"**Date signalement:** {date_c}")
                    if date_r:
                        st.write(f"**Date résolution:** {date_r}")
                
                st.write(f"**Description:** {desc}")
                
                if user['type'] in ['Gestionnaire', 'Personnel'] and statut != "résolu":
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Marquer en cours", key=f"encours_{inc_id}"):
                            cursor.execute("UPDATE incidents SET statut = 'en_cours' WHERE id = ?", (inc_id,))
                            conn.commit()
                            st.rerun()
                    with col2:
                        if st.button("Marquer résolu", key=f"resolu_{inc_id}"):
                            cursor.execute("UPDATE incidents SET statut = 'résolu', date_resolution = ? WHERE id = ?", 
                                         (datetime.now(), inc_id))
                            conn.commit()
                            st.rerun()
                
                if statut == "résolu" and not incident[-1] if len(incident) > 8 else True:
                    st.write("**Évaluez notre intervention:**")
                    note = st.slider("Note de satisfaction", 1, 5, 3, key=f"note_{inc_id}")
                    if st.button("Envoyer l'évaluation", key=f"eval_{inc_id}"):
                        cursor.execute("UPDATE incidents SET note_satisfaction = ? WHERE id = ?", (note, inc_id))
                        cursor.execute("UPDATE users SET points_fidelite = points_fidelite + 5 WHERE id = ?", (user['id'],))
                        conn.commit()
                        st.success("Merci pour votre retour ! +5 points")
                        st.rerun()
    else:
        st.info("Aucun incident signalé")
    
    conn.close()

def statistiques_maintenance():
    st.subheader("📈 Statistiques de maintenance")
    
    conn = sqlite3.connect("data/lba_platform.db")
    cursor = conn.cursor()
    
    col1, col2, col3, col4 = st.columns(4)
    
    cursor.execute("SELECT COUNT(*) FROM incidents WHERE statut = 'nouveau'")
    nouveaux = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM incidents WHERE statut = 'en_cours'")
    en_cours = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM incidents WHERE statut = 'résolu'")
    resolus = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(note_satisfaction) FROM incidents WHERE note_satisfaction IS NOT NULL")
    satisfaction = cursor.fetchone()[0] or 0
    
    with col1:
        st.metric("🆕 Nouveaux", nouveaux)
    
    with col2:
        st.metric("⏳ En cours", en_cours)
    
    with col3:
        st.metric("✅ Résolus", resolus)
    
    with col4:
        st.metric("⭐ Satisfaction", f"{satisfaction:.1f}/5")
    
    st.markdown("### Répartition par catégorie")
    cursor.execute("SELECT categorie, COUNT(*) FROM incidents GROUP BY categorie ORDER BY COUNT(*) DESC")
    categories = cursor.fetchall()
    
    if categories:
        for cat, count in categories:
            st.write(f"**{cat}:** {count} incident(s)")
    
    conn.close()
