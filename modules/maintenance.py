import streamlit as st
from utils.auth import get_current_user
import sqlite3
from datetime import datetime
import os
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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
                
                photo_path = None
                if photo:
                    os.makedirs("data/uploads/incidents", exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    photo_filename = f"incident_{timestamp}_{user['id']}.{photo.name.split('.')[-1]}"
                    photo_path = f"data/uploads/incidents/{photo_filename}"
                    
                    with open(photo_path, "wb") as f:
                        f.write(photo.getbuffer())
                
                conn = sqlite3.connect("data/lba_platform.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO incidents (titre, description, categorie, priorite, residence, logement, user_id, photo_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (titre, description, categorie, priorite_simple, user['residence'], user['logement'], user['id'], photo_path))
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
                   i.date_creation, i.date_resolution, u.prenom, u.nom, i.logement, i.photo_path
            FROM incidents i
            JOIN users u ON i.user_id = u.id
            WHERE i.residence = ?
            ORDER BY i.date_creation DESC
        """, (user['residence'],))
    else:
        cursor.execute("""
            SELECT id, titre, description, categorie, priorite, statut, date_creation, date_resolution, photo_path
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
                inc_id, titre, desc, cat, prio, statut, date_c, date_r, prenom, nom, logement, photo_path = incident
            else:
                inc_id, titre, desc, cat, prio, statut, date_c, date_r, photo_path = incident
            
            if statut not in statut_filter:
                continue
            
            # Badges élégants avec couleurs
            statut_badges = {
                "nouveau": '<span style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 0.25rem 0.75rem; border-radius: 20px; color: #fff; font-size: 0.85rem; font-weight: 600;">🆕 Nouveau</span>',
                "en_cours": '<span style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 0.25rem 0.75rem; border-radius: 20px; color: #fff; font-size: 0.85rem; font-weight: 600;">⏳ En cours</span>',
                "résolu": '<span style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 0.25rem 0.75rem; border-radius: 20px; color: #fff; font-size: 0.85rem; font-weight: 600;">✅ Résolu</span>'
            }
            
            priorite_badges = {
                "Faible": '<span style="background: #10b981; padding: 0.25rem 0.75rem; border-radius: 20px; color: #fff; font-size: 0.85rem; font-weight: 600;">🟢 Faible</span>',
                "Moyenne": '<span style="background: #f59e0b; padding: 0.25rem 0.75rem; border-radius: 20px; color: #fff; font-size: 0.85rem; font-weight: 600;">🟡 Moyenne</span>',
                "Haute": '<span style="background: #f97316; padding: 0.25rem 0.75rem; border-radius: 20px; color: #fff; font-size: 0.85rem; font-weight: 600;">🟠 Haute</span>',
                "Critique": '<span style="background: #ef4444; padding: 0.25rem 0.75rem; border-radius: 20px; color: #fff; font-size: 0.85rem; font-weight: 600; animation: pulse-badge 2s infinite;">🔴 Critique</span>'
            }
            
            # Titre avec badge
            st.markdown(f"""
                <style>
                @keyframes pulse-badge {{
                    0%, 100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }}
                    50% {{ box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }}
                }}
                </style>
                <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 12px; margin-bottom: 1rem; border: 1px solid rgba(255,255,255,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                        <h4 style="color: #fff; margin: 0; font-size: 1.1rem;">{titre}</h4>
                        <div>{statut_badges.get(statut, '')}</div>
                    </div>
                    <div style="display: flex; gap: 0.5rem; align-items: center;">
                        {priorite_badges.get(prio, '')}
                        <span style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">• {cat}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📄 Voir les détails", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
                            <p style="color: rgba(255,255,255,0.9); margin: 0;"><strong>Description :</strong></p>
                            <p style="color: rgba(255,255,255,0.8); margin-top: 0.5rem;">{desc}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if user['type'] in ['Gestionnaire', 'Personnel']:
                        st.markdown(f"""
                            <div style="background: rgba(102, 126, 234, 0.1); padding: 0.75rem; border-radius: 8px; border-left: 3px solid #667eea;">
                                <p style="color: rgba(255,255,255,0.9); margin: 0;">👤 <strong>{prenom} {nom}</strong> - Logement {logement}</p>
                            </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 8px;">
                            <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">📅 Signalé le</p>
                            <p style="color: #fff; font-weight: 600; margin: 0.25rem 0 0 0;">{date_c}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if date_r:
                        st.markdown(f"""
                            <div style="background: rgba(16, 185, 129, 0.1); padding: 1rem; border-radius: 8px; margin-top: 0.5rem;">
                                <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">✅ Résolu le</p>
                                <p style="color: #10b981; font-weight: 600; margin: 0.25rem 0 0 0;">{date_r}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    if photo_path and os.path.exists(photo_path):
                        try:
                            image = Image.open(photo_path)
                            st.image(image, caption="📸 Photo incident", use_container_width=True)
                        except:
                            st.caption("📷 Photo disponible")
                
                if user['type'] in ['Gestionnaire', 'Personnel'] and statut != "résolu":
                    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("⏳ Marquer en cours", key=f"encours_{inc_id}", use_container_width=True):
                            cursor.execute("UPDATE incidents SET statut = 'en_cours' WHERE id = ?", (inc_id,))
                            conn.commit()
                            st.rerun()
                    with col2:
                        if st.button("✅ Marquer résolu", key=f"resolu_{inc_id}", use_container_width=True):
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
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("### 📊 Répartition par catégorie")
        cursor.execute("SELECT categorie, COUNT(*) as count FROM incidents GROUP BY categorie ORDER BY count DESC")
        categories_data = cursor.fetchall()
        
        if categories_data:
            df_cat = pd.DataFrame(categories_data, columns=['Catégorie', 'Nombre'])
            fig_cat = px.bar(df_cat, x='Catégorie', y='Nombre', 
                            color='Nombre',
                            color_continuous_scale='Blues')
            fig_cat.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_cat, use_container_width=True)
    
    with col_chart2:
        st.markdown("### 🎯 Statuts des incidents")
        statuts_data = [
            {'Statut': 'Nouveaux', 'Nombre': nouveaux},
            {'Statut': 'En cours', 'Nombre': en_cours},
            {'Statut': 'Résolus', 'Nombre': resolus}
        ]
        df_statuts = pd.DataFrame(statuts_data)
        fig_statuts = px.pie(df_statuts, values='Nombre', names='Statut',
                             color_discrete_sequence=['#ff6b6b', '#ffd93d', '#6bcf7f'])
        fig_statuts.update_layout(height=300)
        st.plotly_chart(fig_statuts, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 🔥 Priorités des incidents actifs")
    cursor.execute("""
        SELECT priorite, COUNT(*) as count 
        FROM incidents 
        WHERE statut != 'résolu'
        GROUP BY priorite
        ORDER BY 
            CASE priorite
                WHEN 'Critique' THEN 1
                WHEN 'Haute' THEN 2
                WHEN 'Moyenne' THEN 3
                WHEN 'Faible' THEN 4
            END
    """)
    priorites_data = cursor.fetchall()
    
    if priorites_data:
        df_prio = pd.DataFrame(priorites_data, columns=['Priorité', 'Nombre'])
        fig_prio = go.Figure(data=[
            go.Bar(x=df_prio['Priorité'], y=df_prio['Nombre'],
                  marker_color=['#e74c3c', '#e67e22', '#f39c12', '#27ae60'])
        ])
        fig_prio.update_layout(height=300, title="Incidents actifs par priorité")
        st.plotly_chart(fig_prio, use_container_width=True)
    
    st.markdown("### 📋 Détails par catégorie")
    cursor.execute("""
        SELECT categorie, COUNT(*) as total,
               SUM(CASE WHEN statut = 'résolu' THEN 1 ELSE 0 END) as resolus
        FROM incidents 
        GROUP BY categorie 
        ORDER BY total DESC
    """)
    details = cursor.fetchall()
    
    if details:
        for cat, total, res in details:
            taux = (res / total * 100) if total > 0 else 0
            st.write(f"**{cat}:** {total} incident(s) - {res} résolu(s) ({taux:.0f}%)")
            st.progress(taux / 100)
    
    conn.close()
