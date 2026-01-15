import streamlit as st
from utils.auth import get_current_user
import sqlite3
from datetime import datetime, timedelta

def show():
    user = get_current_user()
    st.title("📅 Réservations d'Espaces")
    
    tab1, tab2 = st.tabs(["🆕 Nouvelle réservation", "📋 Mes réservations"])
    
    with tab1:
        nouvelle_reservation(user)
    
    with tab2:
        mes_reservations(user)

def nouvelle_reservation(user):
    st.subheader("Réserver un espace commun")
    
    st.info("💡 Réservez gratuitement la laverie, salle de sport, ou espaces communs de votre résidence !")
    
    with st.form("reservation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            type_espace = st.selectbox("Type d'espace", [
                "Laverie",
                "Salle de sport",
                "Salle de réunion",
                "Espace co-working",
                "Cuisine commune",
                "Terrasse/Jardin",
                "Salle de cinéma"
            ])
            
            if type_espace == "Laverie":
                espace_specifique = st.selectbox("Machine", [
                    "Machine à laver 1",
                    "Machine à laver 2",
                    "Sèche-linge 1",
                    "Sèche-linge 2"
                ])
            elif type_espace == "Salle de sport":
                espace_specifique = st.selectbox("Zone", [
                    "Salle principale",
                    "Zone cardio",
                    "Zone musculation"
                ])
            else:
                espace_specifique = type_espace
            
            date_resa = st.date_input("Date", min_value=datetime.now().date())
        
        with col2:
            heure_debut = st.time_input("Heure de début", value=datetime.now().time())
            duree = st.selectbox("Durée", [
                "30 minutes",
                "1 heure",
                "1h30",
                "2 heures",
                "3 heures",
                "Demi-journée (4h)",
                "Journée complète"
            ])
        
        notes = st.text_area("Notes / Commentaires (optionnel)")
        
        submit = st.form_submit_button("📅 Confirmer la réservation")
        
        if submit:
            duree_map = {
                "30 minutes": 0.5,
                "1 heure": 1,
                "1h30": 1.5,
                "2 heures": 2,
                "3 heures": 3,
                "Demi-journée (4h)": 4,
                "Journée complète": 8
            }
            
            debut = datetime.combine(date_resa, heure_debut)
            fin = debut + timedelta(hours=duree_map[duree])
            
            conn = sqlite3.connect("data/lba_platform.db")
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) FROM reservations 
                WHERE espace = ? AND residence = ? 
                AND ((date_debut <= ? AND date_fin >= ?) OR (date_debut <= ? AND date_fin >= ?))
                AND statut = 'confirmee'
            """, (espace_specifique, user['residence'], debut, debut, fin, fin))
            
            conflit = cursor.fetchone()[0]
            
            if conflit > 0:
                conn.close()
                st.error("❌ Cet espace est déjà réservé sur ce créneau. Veuillez choisir un autre horaire.")
            else:
                cursor.execute("""
                    INSERT INTO reservations (type_espace, espace, residence, user_id, date_debut, date_fin)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (type_espace, espace_specifique, user['residence'], user['id'], debut, fin))
                cursor.execute("UPDATE users SET points_fidelite = points_fidelite + 3 WHERE id = ?", (user['id'],))
                conn.commit()
                conn.close()
                st.success("✅ Réservation confirmée ! +3 points de fidélité")
                st.balloons()
                st.rerun()

def mes_reservations(user):
    st.subheader("Vos réservations")
    
    conn = sqlite3.connect("data/lba_platform.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, type_espace, espace, date_debut, date_fin, statut
        FROM reservations
        WHERE user_id = ?
        ORDER BY date_debut DESC
        LIMIT 50
    """, (user['id'],))
    
    reservations = cursor.fetchall()
    
    if reservations:
        tab_actives, tab_passees = st.tabs(["🟢 Actives/À venir", "⚪ Passées"])
        
        with tab_actives:
            actives = [r for r in reservations if datetime.fromisoformat(r[4]) >= datetime.now()]
            
            if actives:
                for resa in actives:
                    resa_id, type_esp, espace, debut, fin, statut = resa
                    debut_dt = datetime.fromisoformat(debut)
                    fin_dt = datetime.fromisoformat(fin)
                    
                    with st.expander(f"📅 {type_esp} - {espace} - {debut_dt.strftime('%d/%m/%Y %H:%M')}"):
                        st.write(f"**Type:** {type_esp}")
                        st.write(f"**Espace:** {espace}")
                        st.write(f"**Début:** {debut_dt.strftime('%d/%m/%Y à %H:%M')}")
                        st.write(f"**Fin:** {fin_dt.strftime('%d/%m/%Y à %H:%M')}")
                        st.write(f"**Statut:** {statut}")
                        
                        if datetime.now() < debut_dt - timedelta(hours=1):
                            if st.button("🗑️ Annuler la réservation", key=f"cancel_{resa_id}"):
                                cursor.execute("UPDATE reservations SET statut = 'annulee' WHERE id = ?", (resa_id,))
                                conn.commit()
                                st.success("Réservation annulée")
                                st.rerun()
                        else:
                            st.info("⏰ Trop tard pour annuler (moins d'1h avant le début)")
            else:
                st.info("Aucune réservation active ou à venir")
        
        with tab_passees:
            passees = [r for r in reservations if datetime.fromisoformat(r[4]) < datetime.now()]
            
            if passees:
                for resa in passees:
                    resa_id, type_esp, espace, debut, fin, statut = resa
                    debut_dt = datetime.fromisoformat(debut)
                    fin_dt = datetime.fromisoformat(fin)
                    
                    with st.expander(f"📅 {type_esp} - {espace} - {debut_dt.strftime('%d/%m/%Y %H:%M')}"):
                        st.write(f"**Type:** {type_esp}")
                        st.write(f"**Espace:** {espace}")
                        st.write(f"**Début:** {debut_dt.strftime('%d/%m/%Y à %H:%M')}")
                        st.write(f"**Fin:** {fin_dt.strftime('%d/%m/%Y à %H:%M')}")
                        st.write(f"**Statut:** {statut}")
            else:
                st.info("Aucune réservation passée")
    else:
        st.info("Vous n'avez aucune réservation. Créez-en une !")
    
    st.markdown("---")
    st.markdown("### 📊 Disponibilités en temps réel")
    
    maintenant = datetime.now()
    
    col1, col2, col3 = st.columns(3)
    
    cursor.execute("""
        SELECT COUNT(*) FROM reservations 
        WHERE type_espace = 'Laverie' AND residence = ? 
        AND date_debut <= ? AND date_fin >= ? AND statut = 'confirmee'
    """, (user['residence'], maintenant, maintenant))
    laverie_occupee = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) FROM reservations 
        WHERE type_espace = 'Salle de sport' AND residence = ? 
        AND date_debut <= ? AND date_fin >= ? AND statut = 'confirmee'
    """, (user['residence'], maintenant, maintenant))
    sport_occupe = cursor.fetchone()[0]
    
    conn.close()
    
    with col1:
        statut_laverie = "🟢 Disponible" if laverie_occupee == 0 else f"🔴 Occupée ({laverie_occupee})"
        st.metric("Laverie", statut_laverie)
    
    with col2:
        statut_sport = "🟢 Disponible" if sport_occupe == 0 else f"🟡 {sport_occupe} personne(s)"
        st.metric("Salle de sport", statut_sport)
    
    with col3:
        st.metric("Espaces communs", "🟢 Disponibles")
