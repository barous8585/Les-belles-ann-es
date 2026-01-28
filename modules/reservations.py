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
    st.markdown("### 📋 Vos Réservations")
    
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
        
        # CSS pour timeline
        st.markdown("""
            <style>
            .timeline-card {
                background: rgba(255,255,255,0.05);
                backdrop-filter: blur(10px);
                padding: 1.5rem;
                border-radius: 12px;
                border-left: 4px solid;
                margin-bottom: 1rem;
                transition: all 0.3s;
            }
            .timeline-card:hover {
                transform: translateX(5px);
                box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.2);
            }
            .timeline-card.active {
                border-left-color: #10b981;
                background: rgba(16, 185, 129, 0.05);
            }
            .timeline-card.past {
                border-left-color: rgba(255,255,255,0.3);
                background: rgba(255,255,255,0.02);
            }
            </style>
        """, unsafe_allow_html=True)
        
        with tab_actives:
            actives = [r for r in reservations if datetime.fromisoformat(r[4]) >= datetime.now()]
            
            if actives:
                for resa in actives:
                    resa_id, type_esp, espace, debut, fin, statut = resa
                    debut_dt = datetime.fromisoformat(debut)
                    fin_dt = datetime.fromisoformat(fin)
                    
                    # Icônes par type d'espace
                    espace_icons = {
                        "Laverie": "🧺",
                        "Salle de sport": "🏋️",
                        "Salle de réunion": "💼",
                        "Espace co-working": "💻",
                        "Cuisine commune": "🍳",
                        "Terrasse/Jardin": "🌳",
                        "Salle de cinéma": "🎬"
                    }
                    
                    duree = (fin_dt - debut_dt).total_seconds() / 3600
                    maintenant = datetime.now()
                    
                    # Badge statut
                    if debut_dt > maintenant:
                        badge_statut = '<span style="background: #3b82f6; padding: 0.25rem 0.75rem; border-radius: 20px; color: #fff; font-size: 0.85rem; font-weight: 600;">📅 À venir</span>'
                    else:
                        badge_statut = '<span style="background: #10b981; padding: 0.25rem 0.75rem; border-radius: 20px; color: #fff; font-size: 0.85rem; font-weight: 600;">✅ En cours</span>'
                    
                    st.markdown(f"""
                        <div class="timeline-card active">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                                <h4 style="color: #fff; margin: 0; font-size: 1.1rem;">
                                    {espace_icons.get(type_esp, '📍')} {type_esp} - {espace}
                                </h4>
                                {badge_statut}
                            </div>
                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1rem;">
                                <div>
                                    <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">📅 Date</p>
                                    <p style="color: #fff; font-weight: 600; margin: 0.25rem 0 0 0;">{debut_dt.strftime('%d/%m/%Y')}</p>
                                </div>
                                <div>
                                    <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">🕐 Horaires</p>
                                    <p style="color: #fff; font-weight: 600; margin: 0.25rem 0 0 0;">{debut_dt.strftime('%H:%M')} - {fin_dt.strftime('%H:%M')}</p>
                                </div>
                                <div>
                                    <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">⏱️ Durée</p>
                                    <p style="color: #fff; font-weight: 600; margin: 0.25rem 0 0 0;">{duree:.1f}h</p>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if datetime.now() < debut_dt - timedelta(hours=1):
                        if st.button("🗑️ Annuler la réservation", key=f"cancel_{resa_id}"):
                            cursor.execute("UPDATE reservations SET statut = 'annulee' WHERE id = ?", (resa_id,))
                            conn.commit()
                            st.success("✅ Réservation annulée")
                            st.rerun()
                    else:
                        st.caption("⏰ Annulation impossible (< 1h avant le début)")
            else:
                st.info("📭 Aucune réservation active ou à venir")
        
        with tab_passees:
            passees = [r for r in reservations if datetime.fromisoformat(r[4]) < datetime.now()]
            
            if passees:
                for resa in passees[:10]:
                    resa_id, type_esp, espace, debut, fin, statut = resa
                    debut_dt = datetime.fromisoformat(debut)
                    fin_dt = datetime.fromisoformat(fin)
                    
                    espace_icons = {
                        "Laverie": "🧺",
                        "Salle de sport": "🏋️",
                        "Salle de réunion": "💼",
                        "Espace co-working": "💻",
                        "Cuisine commune": "🍳",
                        "Terrasse/Jardin": "🌳",
                        "Salle de cinéma": "🎬"
                    }
                    
                    duree = (fin_dt - debut_dt).total_seconds() / 3600
                    
                    st.markdown(f"""
                        <div class="timeline-card past">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                                <h4 style="color: rgba(255,255,255,0.7); margin: 0; font-size: 1rem;">
                                    {espace_icons.get(type_esp, '📍')} {type_esp} - {espace}
                                </h4>
                                <span style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">✅ Terminée</span>
                            </div>
                            <div style="display: flex; gap: 2rem;">
                                <div>
                                    <p style="color: rgba(255,255,255,0.5); font-size: 0.85rem; margin: 0;">📅 {debut_dt.strftime('%d/%m/%Y')}</p>
                                    <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0.25rem 0 0 0;">🕐 {debut_dt.strftime('%H:%M')} - {fin_dt.strftime('%H:%M')}</p>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("📭 Aucune réservation passée")
    else:
        st.info("📭 Vous n'avez aucune réservation. Créez-en une !")
    
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
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
        if laverie_occupee == 0:
            st.markdown("""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 1.5rem; border-radius: 12px; text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧺</div>
                    <div style="color: #fff; font-weight: 700; font-size: 1.1rem;">Laverie</div>
                    <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem; margin-top: 0.5rem;">🟢 Disponible</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 1.5rem; border-radius: 12px; text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧺</div>
                    <div style="color: #fff; font-weight: 700; font-size: 1.1rem;">Laverie</div>
                    <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem; margin-top: 0.5rem;">🔴 Occupée ({laverie_occupee})</div>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if sport_occupe == 0:
            st.markdown("""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 1.5rem; border-radius: 12px; text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏋️</div>
                    <div style="color: #fff; font-weight: 700; font-size: 1.1rem;">Salle de sport</div>
                    <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem; margin-top: 0.5rem;">🟢 Disponible</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 1.5rem; border-radius: 12px; text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏋️</div>
                    <div style="color: #fff; font-weight: 700; font-size: 1.1rem;">Salle de sport</div>
                    <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem; margin-top: 0.5rem;">🟡 {sport_occupe} personne(s)</div>
                </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.metric("Espaces communs", "🟢 Disponibles")
