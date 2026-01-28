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
        
        if user['type'] == 'Résident':
            st.markdown(f"**Résidence:** {user['residence']}")
            st.markdown(f"**Logement:** {user['logement']}")
            st.markdown(f"**Points fidélité:** {user['points']}")
        elif user['type'] in ['Gestionnaire', 'Personnel']:
            st.markdown(f"**Résidence:** {user['residence']}")
            st.markdown(f"**Rôle:** {user['type']}")
        
        st.markdown("---")
        
        if user['type'] == 'Résident':
            menu_options = ["🏠 Accueil", "🤖 Assistant IA", "👥 Communauté", "🔧 Maintenance", "📅 Réservations", "⚙️ Mon Compte"]
        elif user['type'] == 'Gestionnaire':
            menu_options = ["📊 Dashboard", "🔧 Maintenance", "📅 Planning Global", "👥 Modération", "📈 Analytics", "⚙️ Paramètres"]
        else:
            menu_options = ["🏠 Mes Tâches", "🔧 Interventions", "📅 Planning", "💬 Communication", "⚙️ Mon Compte"]
        
        menu = st.radio(
            "Navigation",
            menu_options,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button("🚪 Déconnexion", use_container_width=True):
            logout()
    
    # DASHBOARD RÉSIDENT
    if menu == "🏠 Accueil":
        st.title("🏠 Mon Tableau de bord")
        
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
            st.metric("Mes incidents actifs", incidents_actifs)
        
        with col2:
            st.metric("Événements à venir", evenements_disponibles)
        
        with col3:
            st.metric("Annonces marketplace", annonces_marketplace)
        
        with col4:
            st.metric("Mes réservations", reservations_actives)
    
    # DASHBOARD GESTIONNAIRE
    elif menu == "📊 Dashboard":
        st.title("📊 Dashboard Résidence")
        
        conn = sqlite3.connect("data/lba_platform.db")
        cursor = conn.cursor()
        
        col1, col2, col3, col4 = st.columns(4)
        
        cursor.execute("SELECT COUNT(*) FROM incidents WHERE residence = ? AND statut = 'nouveau'", (user['residence'],))
        incidents_nouveaux = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM incidents WHERE residence = ? AND statut = 'en_cours'", (user['residence'],))
        incidents_encours = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE residence = ? AND type_utilisateur = 'Résident'", (user['residence'],))
        nb_residents = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM reservations WHERE residence = ? AND date_debut >= date('now')", (user['residence'],))
        reservations_futures = cursor.fetchone()[0]
        
        with col1:
            st.metric("🆕 Incidents nouveaux", incidents_nouveaux, delta=None if incidents_nouveaux == 0 else f"+{incidents_nouveaux}")
        
        with col2:
            st.metric("⏳ Incidents en cours", incidents_encours)
        
        with col3:
            st.metric("👥 Résidents", nb_residents)
        
        with col4:
            st.metric("📅 Réservations futures", reservations_futures)
        
        st.markdown("---")
        st.subheader("📈 Activité de la semaine")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            cursor.execute("""
                SELECT COUNT(*) FROM incidents 
                WHERE residence = ? AND date_creation >= date('now', '-7 days')
            """, (user['residence'],))
            incidents_semaine = cursor.fetchone()[0]
            st.metric("Incidents cette semaine", incidents_semaine)
        
        with col_b:
            cursor.execute("""
                SELECT COUNT(*) FROM participations p
                JOIN evenements e ON p.evenement_id = e.id
                WHERE e.residence = ? AND p.date_inscription >= date('now', '-7 days')
            """, (user['residence'],))
            participations_semaine = cursor.fetchone()[0]
            st.metric("Participations événements", participations_semaine)
        
        conn.close()
    
    # DASHBOARD PERSONNEL
    elif menu == "🏠 Mes Tâches":
        st.title("🏠 Mes Tâches du Jour")
        
        conn = sqlite3.connect("data/lba_platform.db")
        cursor = conn.cursor()
        
        st.info("💡 Interface Personnel - Incidents à traiter en priorité")
        
        cursor.execute("""
            SELECT COUNT(*) FROM incidents 
            WHERE residence = ? AND statut IN ('nouveau', 'en_cours')
            ORDER BY 
                CASE priorite
                    WHEN 'Critique' THEN 1
                    WHEN 'Haute' THEN 2
                    WHEN 'Moyenne' THEN 3
                    WHEN 'Faible' THEN 4
                END
        """, (user['residence'],))
        
        taches_total = cursor.fetchone()[0]
        
        col1, col2, col3 = st.columns(3)
        
        cursor.execute("SELECT COUNT(*) FROM incidents WHERE residence = ? AND priorite = 'Critique' AND statut != 'résolu'", (user['residence'],))
        critiques = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM incidents WHERE residence = ? AND priorite = 'Haute' AND statut != 'résolu'", (user['residence'],))
        urgents = cursor.fetchone()[0]
        
        with col1:
            st.metric("🔴 Critiques", critiques)
        
        with col2:
            st.metric("🟠 Urgents", urgents)
        
        with col3:
            st.metric("📋 Total tâches", taches_total)
        
        conn.close()
    
    elif menu == "🤖 Assistant IA":
        from modules import assistant_ia
        assistant_ia.show()
    
    elif menu == "👥 Communauté":
        from modules import communaute
        communaute.show()
    
    elif menu == "🔧 Maintenance" or menu == "🔧 Interventions":
        from modules import maintenance
        maintenance.show()
    
    elif menu == "📅 Réservations" or menu == "📅 Planning":
        from modules import reservations
        reservations.show()
    
    elif menu == "📅 Planning Global":
        from modules import planning_global
        planning_global.show()
    
    elif menu == "👥 Modération":
        from modules import moderation
        moderation.show()
    
    elif menu == "📈 Analytics":
        from modules import maintenance
        maintenance.statistiques_maintenance()
    
    elif menu == "⚙️ Paramètres" or menu == "⚙️ Mon Compte":
        from modules import mon_compte
        mon_compte.show()
    
    elif menu == "💬 Communication":
        st.title("💬 Communication Résidents")
        st.info("🚧 Module en développement - Messagerie avec les résidents")
