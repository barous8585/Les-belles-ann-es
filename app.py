import streamlit as st
from utils.database import init_database, get_residences_list
from utils.auth import login_user, register_user, is_authenticated, get_current_user, logout
import sqlite3

st.set_page_config(
    page_title="Les Belles Années - Plateforme Résidents",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_database()

if not is_authenticated():
    st.markdown("""<style>[data-testid=\"stSidebar\"]{display:none}</style>""", unsafe_allow_html=True)
    st.title("🏠 Les Belles Années")
    st.subheader("Votre plateforme tout-en-un pour une vie étudiante enrichie")
    
    tab1, tab2 = st.tabs(["🔐 Connexion", "✨ Inscription"])
    
    with tab1:
        st.subheader("Connexion à votre compte")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("Se connecter")
            
            if submit:
                user, error_msg = login_user(email, password)
                if user:
                    st.session_state.user = user
                    st.success("Connexion réussie ! Bienvenue " + user['prenom'])
                    st.rerun()
                else:
                    st.error(error_msg if error_msg else "Email ou mot de passe incorrect")
    
    with tab2:
        st.subheader("Créer votre compte")
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            with col1:
                nom = st.text_input("Nom")
                prenom = st.text_input("Prénom")
                email = st.text_input("Email", key="reg_email")
                password = st.text_input("Mot de passe", type="password", key="reg_password")
                st.caption("🔒 Min 8 caractères, 1 majuscule, 1 chiffre")
            
            with col2:
                type_user = st.selectbox("Type d utilisateur", ["Résident", "Gestionnaire", "Personnel"])
                
                residences = get_residences_list()
                
                residence = st.selectbox("Résidence", residences)
                numero_logement = st.text_input("Numéro de logement")
                telephone = st.text_input("Téléphone")
            
            submit_reg = st.form_submit_button("S inscrire")
            
            if submit_reg:
                if all([nom, prenom, email, password, residence]):
                    success, message = register_user(email, password, nom, prenom, type_user, residence, numero_logement, telephone)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.warning("Veuillez remplir tous les champs obligatoires")

else:
    user = get_current_user()
    
    with st.sidebar:
        st.markdown(f"### 👋 Bonjour {user['prenom']} !")
        st.markdown(f"**Résidence:** {user['residence']}")
        st.markdown(f"**Logement:** {user['logement']}")
        st.markdown(f"**Points fidélité:** {user['points']}")
        
        st.markdown("---")
        
        menu = st.radio(
            "Navigation",
            ["🏠 Accueil", "🤖 Assistant IA", "👥 Communauté", "🔧 Maintenance", "📅 Réservations", "⚙️ Mon Compte"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button("🚪 Déconnexion", use_container_width=True):
            logout()
    
    if menu == "🏠 Accueil":
        st.title("🏠 Tableau de bord")
        
        col1, col2, col3, col4 = st.columns(4)
        
        conn = sqlite3.connect("data/lba_platform.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM incidents WHERE user_id = ? AND statut != 'résolu'", (user['id'],))
        incidents_actifs = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM evenements WHERE residence = ? AND statut = 'ouvert'", (user['residence'],))
        evenements_disponibles = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM marketplace WHERE residence = ? AND statut = 'disponible'", (user['residence'],))
        annonces_marketplace = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM reservations WHERE user_id = ?", (user['id'],))
        reservations_actives = cursor.fetchone()[0]
        
        conn.close()
        
        with col1:
            st.metric("Incidents actifs", incidents_actifs)
        
        with col2:
            st.metric("Événements à venir", evenements_disponibles)
        
        with col3:
            st.metric("Annonces marketplace", annonces_marketplace)
        
        with col4:
            st.metric("Mes réservations", reservations_actives)
    
    elif menu == "🤖 Assistant IA":
        from modules import assistant_ia
        assistant_ia.show()
    
    elif menu == "👥 Communauté":
        from modules import communaute
        communaute.show()
    
    elif menu == "🔧 Maintenance":
        from modules import maintenance
        maintenance.show()
    
    elif menu == "📅 Réservations":
        from modules import reservations
        reservations.show()
    
    elif menu == "⚙️ Mon Compte":
        from modules import mon_compte
        mon_compte.show()
