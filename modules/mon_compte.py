import streamlit as st
from utils.auth import get_current_user, logout
import sqlite3
from datetime import datetime

def show():
    user = get_current_user()
    st.title("⚙️ Mon Compte")
    
    tab1, tab2, tab3 = st.tabs(["👤 Profil", "⭐ Fidélité", "📄 Documents"])
    
    with tab1:
        show_profil(user)
    
    with tab2:
        show_fidelite(user)
    
    with tab3:
        show_documents(user)

def show_profil(user):
    st.subheader("Informations personnelles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Nom:** {user['nom']}")
        st.write(f"**Prénom:** {user['prenom']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Téléphone:** {user['telephone']}")
    
    with col2:
        st.write(f"**Type de compte:** {user['type']}")
        st.write(f"**Résidence:** {user['residence']}")
        st.write(f"**Logement:** {user['logement']}")
    
    st.markdown("---")
    
    st.subheader("Modifier mes informations")
    
    with st.form("update_profile"):
        new_telephone = st.text_input("Nouveau téléphone", value=user['telephone'])
        new_password = st.text_input("Nouveau mot de passe (laisser vide pour ne pas changer)", type="password")
        
        if st.form_submit_button("💾 Enregistrer les modifications"):
            conn = sqlite3.connect("data/lba_platform.db")
            cursor = conn.cursor()
            
            if new_telephone != user['telephone']:
                cursor.execute("UPDATE users SET telephone = ? WHERE id = ?", (new_telephone, user['id']))
            
            if new_password:
                from utils.database import hash_password
                hashed_pw = hash_password(new_password)
                cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_pw, user['id']))
            
            conn.commit()
            conn.close()
            
            st.success("✅ Informations mises à jour !")
            st.session_state.user['telephone'] = new_telephone
            st.rerun()

def show_fidelite(user):
    st.subheader("Programme de Fidélité")
    
    st.markdown(f"### ⭐ Vous avez **{user['points']}** points !")
    
    progression = (user['points'] % 100) / 100 * 100
    st.progress(progression / 100)
    st.caption(f"{100 - (user['points'] % 100)} points avant la prochaine récompense (10€ de réduction)")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Récompenses disponibles")
        
        recompenses = [
            (100, "10€ de réduction sur le loyer"),
            (250, "25€ de réduction sur le loyer"),
            (500, "50€ de réduction sur le loyer"),
            (1000, "100€ de réduction + cadeau surprise")
        ]
        
        for points_requis, recompense in recompenses:
            if user['points'] >= points_requis:
                st.success(f"✅ **{points_requis} pts:** {recompense}")
                if st.button(f"Utiliser ({points_requis} pts)", key=f"use_{points_requis}"):
                    st.info("Contactez l'accueil pour activer votre récompense !")
            else:
                st.info(f"🔒 **{points_requis} pts:** {recompense}")
    
    with col2:
        st.markdown("### 🎯 Comment gagner des points ?")
        
        st.write("**+3 pts** - Réserver un espace")
        st.write("**+5 pts** - Publier une annonce marketplace")
        st.write("**+5 pts** - Évaluer une intervention")
        st.write("**+10 pts** - Participer à un événement")
        st.write("**+25 pts** - Organiser un événement")
        st.write("**+50 pts** - Parrainer un ami")
    
    st.markdown("---")
    
    st.subheader("📊 Historique des points")
    
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
        for action, date, points in historique:
            st.write(f"**+{points} pts** - {action} - {date}")
    else:
        st.info("Aucun historique pour le moment")
    
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
