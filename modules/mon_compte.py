import streamlit as st
from utils.auth import get_current_user, logout
import sqlite3
from datetime import datetime

def show():
    user = get_current_user()
    st.title("⚙️ Mon Compte" if user['type'] == 'Résident' else "⚙️ Paramètres")
    
    if user['type'] == 'Résident':
        tab1, tab2, tab3 = st.tabs(["👤 Profil", "⭐ Fidélité", "📄 Documents"])
        
        with tab1:
            show_profil(user)
        
        with tab2:
            show_fidelite(user)
        
        with tab3:
            show_documents(user)
    else:
        tab1, tab2 = st.tabs(["👤 Profil", "⚙️ Préférences"])
        
        with tab1:
            show_profil(user)
        
        with tab2:
            show_preferences_gestionnaire(user)

def show_profil(user):
    # Profil Card élégant
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);">
            <div style="display: flex; align-items: center; gap: 1.5rem;">
                <div style="background: rgba(255,255,255,0.2); width: 100px; height: 100px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 3rem; border: 4px solid rgba(255,255,255,0.3);">
                    👤
                </div>
                <div style="flex: 1;">
                    <h2 style="color: #fff; margin: 0; font-size: 1.8rem; font-weight: 700;">{user['prenom']} {user['nom']}</h2>
                    <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;">{user['type']}</p>
                    <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; color: #fff; font-size: 0.9rem;">
                            🏢 {user['residence']}
                        </span>
                        {f'<span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; color: #fff; font-size: 0.9rem;">🚪 Logement {user["logement"]}</span>' if user['type'] == 'Résident' else ''}
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 Informations de contact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">📧 Email</p>
                <p style="color: #fff; font-weight: 600; font-size: 1.1rem; margin: 0.5rem 0 0 0;">{user['email']}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">📱 Téléphone</p>
                <p style="color: #fff; font-weight: 600; font-size: 1.1rem; margin: 0.5rem 0 0 0;">{user['telephone'] if user['telephone'] else 'Non renseigné'}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("### ✏️ Modifier mes informations")
    
    with st.form("update_profile"):
        new_telephone = st.text_input("📱 Nouveau téléphone", value=user['telephone'], placeholder="06 12 34 56 78")
        new_password = st.text_input("🔒 Nouveau mot de passe", type="password", placeholder="Laisser vide pour ne pas changer")
        st.caption("💡 Le mot de passe doit contenir : min 8 caractères, 1 majuscule, 1 chiffre")
        
        if st.form_submit_button("💾 Enregistrer les modifications", use_container_width=True):
            conn = sqlite3.connect("data/lba_platform.db")
            cursor = conn.cursor()
            
            if new_telephone != user['telephone']:
                cursor.execute("UPDATE users SET telephone = ? WHERE id = ?", (new_telephone, user['id']))
            
            if new_password:
                from utils.database import hash_password
                from utils.validators import validate_password
                is_valid, msg = validate_password(new_password)
                if not is_valid:
                    st.error(f"❌ {msg}")
                else:
                    hashed_pw = hash_password(new_password)
                    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_pw, user['id']))
            
            conn.commit()
            conn.close()
            
            st.success("✅ Informations mises à jour !")
            st.balloons()
            st.session_state.user['telephone'] = new_telephone
            st.rerun()

def show_preferences_gestionnaire(user):
    st.subheader("⚙️ Préférences de Gestion")
    
    st.info("💡 Configuration avancée pour la gestion de votre résidence")
    
    st.markdown("### 🔔 Notifications")
    notif_incidents = st.checkbox("Recevoir notifications nouveaux incidents", value=True)
    notif_reservations = st.checkbox("Recevoir notifications nouvelles réservations", value=False)
    notif_marketplace = st.checkbox("Recevoir notifications nouvelles annonces", value=False)
    
    st.markdown("### 📊 Rapports")
    rapport_hebdo = st.checkbox("Rapport hebdomadaire par email", value=True)
    rapport_mensuel = st.checkbox("Rapport mensuel détaillé", value=True)
    
    if st.button("💾 Sauvegarder préférences"):
        st.success("✅ Préférences sauvegardées !")
        st.info("🚧 Fonctionnalité en cours de développement")

def show_fidelite(user):
    # Card principal avec progression
    progression = (user['points'] % 100) / 100 * 100
    points_restants = 100 - (user['points'] % 100)
    palier_actuel = (user['points'] // 100) * 100
    prochain_palier = palier_actuel + 100
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2.5rem; border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 20px 25px -5px rgba(240, 147, 251, 0.4);">
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <div style="font-size: 4rem; margin-bottom: 0.5rem;">⭐</div>
                <h2 style="color: #fff; margin: 0; font-size: 2.5rem; font-weight: 700;">{user['points']} Points</h2>
                <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;">Programme Fidélité Les Belles Années</p>
            </div>
            
            <div style="background: rgba(255,255,255,0.2); height: 16px; border-radius: 8px; overflow: hidden; margin-bottom: 1rem;">
                <div style="background: linear-gradient(90deg, #fff 0%, rgba(255,255,255,0.8) 100%); height: 100%; width: {progression}%; border-radius: 8px; transition: width 0.5s ease;"></div>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.95rem;">Palier actuel: {palier_actuel} pts</p>
                </div>
                <div style="text-align: right;">
                    <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.95rem; font-weight: 700;">
                        🎯 {points_restants} pts avant {prochain_palier}
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Récompenses disponibles")
        
        recompenses = [
            (100, "10€ de réduction loyer", "💵", "#10b981"),
            (250, "25€ de réduction loyer", "💰", "#3b82f6"),
            (500, "50€ de réduction loyer", "💸", "#f59e0b"),
            (1000, "100€ + cadeau surprise", "🎁", "#ef4444")
        ]
        
        for points_requis, recompense, icon, color in recompenses:
            if user['points'] >= points_requis:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {color}20 0%, {color}10 100%); padding: 1rem; border-radius: 12px; border-left: 4px solid {color}; margin-bottom: 0.75rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
                                <strong style="color: #fff;">{points_requis} pts</strong>
                                <p style="color: rgba(255,255,255,0.8); margin: 0.25rem 0 0 0; font-size: 0.9rem;">{recompense}</p>
                            </div>
                            <span style="background: {color}; padding: 0.25rem 0.75rem; border-radius: 20px; color: #fff; font-size: 0.85rem; font-weight: 600;">✅ Disponible</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"🎉 Utiliser ({points_requis} pts)", key=f"use_{points_requis}"):
                    st.success("✅ Contactez l'accueil pour activer votre récompense !")
                    st.balloons()
            else:
                progress_recompense = (user['points'] / points_requis) * 100
                st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 0.75rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <div>
                                <span style="font-size: 1.5rem; margin-right: 0.5rem; opacity: 0.5;">{icon}</span>
                                <strong style="color: rgba(255,255,255,0.7);">{points_requis} pts</strong>
                                <p style="color: rgba(255,255,255,0.6); margin: 0.25rem 0 0 0; font-size: 0.9rem;">{recompense}</p>
                            </div>
                            <span style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">🔒 {points_requis - user['points']} pts restants</span>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); height: 6px; border-radius: 3px; overflow: hidden;">
                            <div style="background: {color}; height: 100%; width: {progress_recompense}%; border-radius: 3px;"></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Comment gagner des points")
        
        actions = [
            ("🧺", "Réserver un espace", "+3 pts"),
            ("🛍️", "Publier annonce marketplace", "+5 pts"),
            ("⭐", "Évaluer intervention", "+5 pts"),
            ("🎉", "Participer événement", "+10 pts"),
            ("🎊", "Organiser événement", "+25 pts"),
            ("🤝", "Parrainer un ami", "+50 pts")
        ]
        
        for icon, action, points in actions:
            st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
                        <span style="color: rgba(255,255,255,0.9);">{action}</span>
                    </div>
                    <span style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 0.25rem 0.75rem; border-radius: 20px; color: #fff; font-size: 0.85rem; font-weight: 600;">{points}</span>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("### 📊 Historique des points")
    
    conn = sqlite3.connect("data/lba_platform.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 'Participation événement' as action, date_inscription as date, 10 as points
        FROM participations WHERE user_id = ?
        UNION ALL
        SELECT 'Création annonce', date_creation, 5
        FROM marketplace WHERE vendeur_id = ?
        UNION ALL
        SELECT 'Réservation', date_debut, 3
        FROM reservations WHERE user_id = ?
        ORDER BY date DESC LIMIT 20
    """, (user['id'], user['id'], user['id']))
    
    historique = cursor.fetchall()
    
    if historique:
        for action, date, points in historique[:10]:
            date_str = datetime.fromisoformat(str(date)).strftime('%d/%m/%Y %H:%M') if date else "Date inconnue"
            st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.1); padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #10b981;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="color: #10b981;">+{points} pts</strong>
                            <span style="color: rgba(255,255,255,0.9); margin-left: 0.5rem;">{action}</span>
                        </div>
                        <span style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">📅 {date_str}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 Aucun historique pour le moment. Commencez à participer pour gagner des points !")
    
    conn.close()

def show_documents(user):
    st.subheader("Documents administratifs")
    
    st.info("📄 Téléchargez vos documents officiels pour vos démarches")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Attestation de logement", use_container_width=True):
            generer_attestation(user)
        
        if st.button("📥 Quittance de loyer", use_container_width=True):
            st.info("Disponible dans votre espace locataire le 5 de chaque mois")
        
        if st.button("📥 Certificat de résidence", use_container_width=True):
            generer_certificat(user)
    
    with col2:
        if st.button("📥 Règlement intérieur", use_container_width=True):
            st.download_button(
                "Télécharger le règlement",
                "Règlement intérieur Les Belles Années...",
                "reglement_interieur.pdf"
            )
        
        if st.button("📥 Assurance habitation", use_container_width=True):
            st.info("Téléchargez votre attestation d'assurance fournie par votre assureur")
    
    st.markdown("---")
    
    st.subheader("📞 Contacts utiles")
    
    st.write("**🏢 Accueil résidence**")
    st.write(f"Résidence {user['residence']}")
    st.write("Téléphone : 04 78 17 14 11")
    st.write("Email : contact@lesbellesannees.com")
    st.write("Horaires : Lun-Ven 9h-18h")
    
    st.write("")
    st.write("**🚨 Urgences (24/7)**")
    st.write("Téléphone : 06 12 34 56 78")
    
    st.write("")
    st.write("**🛠️ Maintenance**")
    st.write("Email : maintenance@lesbellesannees.com")

def generer_attestation(user):
    attestation = f"""
    ATTESTATION DE LOGEMENT
    
    Je soussigné(e), représentant(e) de la société Les Belles Années,
    atteste que :
    
    Nom : {user['nom']}
    Prénom : {user['prenom']}
    
    Occupe le logement suivant :
    Résidence : {user['residence']}
    Logement : {user['logement']}
    
    Depuis le : [Date d'entrée]
    
    Fait pour servir et valoir ce que de droit.
    
    Date : {datetime.now().strftime('%d/%m/%Y')}
    
    Les Belles Années
    94 quai Charles de Gaulle, 69006 Lyon
    """
    
    st.download_button(
        "📥 Télécharger l'attestation",
        attestation,
        f"attestation_logement_{user['nom']}.txt",
        "text/plain"
    )

def generer_certificat(user):
    certificat = f"""
    CERTIFICAT DE RÉSIDENCE
    
    La société Les Belles Années certifie que :
    
    {user['prenom']} {user['nom']}
    Email : {user['email']}
    
    Est résident(e) de notre établissement :
    {user['residence']}
    Logement n°{user['logement']}
    
    Ce certificat est délivré pour servir et valoir ce que de droit.
    
    Fait à Lyon, le {datetime.now().strftime('%d/%m/%Y')}
    
    Les Belles Années
    contact@lesbellesannees.com
    04 78 17 14 11
    """
    
    st.download_button(
        "📥 Télécharger le certificat",
        certificat,
        f"certificat_residence_{user['nom']}.txt",
        "text/plain"
    )
