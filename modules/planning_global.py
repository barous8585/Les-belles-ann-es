import streamlit as st
from utils.auth import get_current_user
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def show():
    user = get_current_user()
    st.title("📅 Planning Global - Réservations")
    
    if user['type'] not in ['Gestionnaire', 'Personnel']:
        st.error("⛔ Accès refusé - Réservé aux gestionnaires et personnel")
        return
    
    st.info("📊 Vue d'ensemble de toutes les réservations de la résidence")
    
    tab1, tab2, tab3 = st.tabs(["📅 Planning", "📊 Statistiques", "⚙️ Gestion"])
    
    with tab1:
        show_planning(user)
    
    with tab2:
        show_statistics(user)
    
    with tab3:
        show_management(user)

def show_planning(user):
    st.subheader("Planning des réservations")
    
    conn = sqlite3.connect("data/lba_platform.db")
    cursor = conn.cursor()
    
    filter_date = st.date_input("Filtrer par date", datetime.now())
    
    cursor.execute("""
        SELECT r.id, r.type_espace, r.espace, r.date_debut, r.date_fin, r.statut,
               u.prenom, u.nom, u.numero_logement
        FROM reservations r
        JOIN users u ON r.user_id = u.id
        WHERE r.residence = ? AND DATE(r.date_debut) = ?
        ORDER BY r.date_debut
    """, (user['residence'], filter_date))
    
    reservations = cursor.fetchall()
    
    if reservations:
        for res in reservations:
            res_id, type_esp, espace, debut, fin, statut, prenom, nom, logement = res
            
            with st.expander(f"🎯 {espace} - {debut} → {fin}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Type:** {type_esp}")
                    st.write(f"**Espace:** {espace}")
                    st.write(f"**Début:** {debut}")
                    st.write(f"**Fin:** {fin}")
                
                with col2:
                    st.write(f"**Réservé par:** {prenom} {nom}")
                    st.write(f"**Logement:** {logement}")
                    st.write(f"**Statut:** {statut}")
                
                if user['type'] == 'Gestionnaire':
                    if st.button("❌ Annuler réservation", key=f"cancel_{res_id}"):
                        cursor.execute("UPDATE reservations SET statut = 'annulée' WHERE id = ?", (res_id,))
                        conn.commit()
                        st.success("Réservation annulée")
                        st.rerun()
    else:
        st.info("Aucune réservation pour cette date")
    
    conn.close()

def show_statistics(user):
    st.subheader("📊 Statistiques réservations")
    
    conn = sqlite3.connect("data/lba_platform.db")
    cursor = conn.cursor()
    
    col1, col2, col3 = st.columns(3)
    
    cursor.execute("""
        SELECT COUNT(*) FROM reservations 
        WHERE residence = ? AND date_debut >= date('now')
    """, (user['residence'],))
    total_futures = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT type_espace, COUNT(*) as count 
        FROM reservations 
        WHERE residence = ? AND date_debut >= date('now', '-7 days')
        GROUP BY type_espace
        ORDER BY count DESC
        LIMIT 1
    """, (user['residence'],))
    
    populaire = cursor.fetchone()
    
    cursor.execute("""
        SELECT AVG(count) FROM (
            SELECT user_id, COUNT(*) as count
            FROM reservations
            WHERE residence = ? AND date_debut >= date('now', '-30 days')
            GROUP BY user_id
        )
    """, (user['residence'],))
    
    avg_per_user = cursor.fetchone()[0] or 0
    
    with col1:
        st.metric("Réservations futures", total_futures)
    
    with col2:
        st.metric("Espace le plus populaire", populaire[0] if populaire else "N/A")
    
    with col3:
        st.metric("Moy. résa/résident (30j)", f"{avg_per_user:.1f}")
    
    st.markdown("---")
    st.subheader("📈 Utilisation par espace")
    
    cursor.execute("""
        SELECT espace, COUNT(*) as count
        FROM reservations
        WHERE residence = ? AND date_debut >= date('now', '-30 days')
        GROUP BY espace
        ORDER BY count DESC
    """, (user['residence'],))
    
    data = cursor.fetchall()
    
    if data:
        df = pd.DataFrame(data, columns=['Espace', 'Réservations'])
        st.bar_chart(df.set_index('Espace'))
    
    conn.close()

def show_management(user):
    st.subheader("⚙️ Gestion des espaces")
    
    if user['type'] != 'Gestionnaire':
        st.warning("Fonctionnalité réservée aux gestionnaires")
        return
    
    st.markdown("### Bloquer un créneau (maintenance)")
    
    with st.form("block_slot"):
        type_espace = st.selectbox("Type d'espace", ["Laverie", "Salle de sport", "Cuisine commune", "Salle de réunion"])
        espace = st.text_input("Nom de l'espace (ex: Machine 1)")
        date_debut = st.date_input("Date début")
        heure_debut = st.time_input("Heure début")
        date_fin = st.date_input("Date fin")
        heure_fin = st.time_input("Heure fin")
        raison = st.text_area("Raison du blocage")
        
        if st.form_submit_button("Bloquer"):
            debut = f"{date_debut} {heure_debut}"
            fin = f"{date_fin} {heure_fin}"
            
            conn = sqlite3.connect("data/lba_platform.db")
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO reservations (type_espace, espace, residence, user_id, date_debut, date_fin, statut)
                VALUES (?, ?, ?, ?, ?, ?, 'bloqué_maintenance')
            """, (type_espace, espace, user['residence'], user['id'], debut, fin))
            
            conn.commit()
            conn.close()
            
            st.success(f"✅ Créneau bloqué : {espace} du {debut} au {fin}")
            st.caption(f"Raison : {raison}")
