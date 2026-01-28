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

# Charger le CSS personnalisé
with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

init_database()

if not is_authenticated():
    st.markdown("""<style>[data-testid=\"stSidebar\"]{display:none}</style>""", unsafe_allow_html=True)
    
    # Page de connexion magnifique
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 0.5rem;">
                🏠 Les Belles Années
            </h1>
            <p style="font-size: 1.25rem; color: rgba(255,255,255,0.9); font-weight: 500;">
                Votre plateforme tout-en-un pour une vie étudiante enrichie
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        tab1, tab2 = st.tabs(["🔐 Connexion", "✨ Inscription"])
        
        with tab1:
            st.markdown("### Connexion à votre compte")
            with st.form("login_form"):
                email = st.text_input("📧 Email", placeholder="votre.email@exemple.com")
                password = st.text_input("🔒 Mot de passe", type="password", placeholder="••••••••")
                
                col_btn1, col_btn2 = st.columns([3, 1])
                with col_btn1:
                    submit = st.form_submit_button("🚀 Se connecter", use_container_width=True)
                
                if submit:
                    user, error_msg = login_user(email, password)
                    if user:
                        st.session_state.user = user
                        st.success(f"✅ Connexion réussie ! Bienvenue {user['prenom']} 👋")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ {error_msg if error_msg else 'Email ou mot de passe incorrect'}")
        
        with tab2:
            st.markdown("### Créer votre compte")
            with st.form("register_form"):
                col1, col2 = st.columns(2)
                with col1:
                    nom = st.text_input("👤 Nom", placeholder="Dupont")
                    prenom = st.text_input("👤 Prénom", placeholder="Marie")
                    email = st.text_input("📧 Email", key="reg_email", placeholder="marie.dupont@exemple.com")
                    password = st.text_input("🔒 Mot de passe", type="password", key="reg_password", placeholder="••••••••")
                    st.caption("🔒 Min 8 caractères, 1 majuscule, 1 chiffre")
                
                with col2:
                    type_user = st.selectbox("🎭 Type d'utilisateur", ["Résident", "Gestionnaire", "Personnel"])
                    
                    residences = get_residences_list()
                    
                    residence = st.selectbox("🏢 Résidence", residences)
                    numero_logement = st.text_input("🚪 Numéro de logement", placeholder="A205")
                    telephone = st.text_input("📱 Téléphone", placeholder="06 12 34 56 78")
                
                submit_reg = st.form_submit_button("✨ S'inscrire", use_container_width=True)
                
                if submit_reg:
                    if all([nom, prenom, email, password, residence]):
                        success, message = register_user(email, password, nom, prenom, type_user, residence, numero_logement, telephone)
                        if success:
                            st.success(f"✅ {message}")
                            st.balloons()
                        else:
                            st.error(f"❌ {message}")
                    else:
                        st.warning("⚠️ Veuillez remplir tous les champs obligatoires")

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
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="font-size: 2.5rem; font-weight: 700; color: #fff;">🏠 Bienvenue chez vous</h1>
                <p style="font-size: 1.1rem; color: rgba(255,255,255,0.8);">Votre espace personnel Les Belles Années</p>
            </div>
        """, unsafe_allow_html=True)
        
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
        
        # Cards stylisées avec HTML
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2); transition: transform 0.3s;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔧</div>
                    <div style="font-size: 2rem; font-weight: 700; color: #fff; margin-bottom: 0.3rem;">{incidents_actifs}</div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.9); font-weight: 500;">Mes incidents actifs</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2); transition: transform 0.3s;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎉</div>
                    <div style="font-size: 2rem; font-weight: 700; color: #fff; margin-bottom: 0.3rem;">{evenements_disponibles}</div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.9); font-weight: 500;">Événements à venir</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2); transition: transform 0.3s;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🛍️</div>
                    <div style="font-size: 2rem; font-weight: 700; color: #fff; margin-bottom: 0.3rem;">{annonces_marketplace}</div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.9); font-weight: 500;">Annonces marketplace</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2); transition: transform 0.3s;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">📅</div>
                    <div style="font-size: 2rem; font-weight: 700; color: #fff; margin-bottom: 0.3rem;">{reservations_actives}</div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.9); font-weight: 500;">Mes réservations</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Section Points de fidélité avec progression
        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 2rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.2);">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                    <div>
                        <h3 style="color: #fff; margin: 0; font-size: 1.5rem;">⭐ Programme Fidélité</h3>
                        <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0;">Vous avez <strong>{user['points']} points</strong></p>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 3rem;">🎁</div>
                    </div>
                </div>
                <div style="background: rgba(255,255,255,0.2); height: 12px; border-radius: 6px; overflow: hidden; margin-top: 1rem;">
                    <div style="background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%); height: 100%; width: {min(user['points'], 100)}%; border-radius: 6px; transition: width 0.3s;"></div>
                </div>
                <p style="color: rgba(255,255,255,0.7); margin-top: 0.5rem; font-size: 0.9rem;">Prochain palier : 100 points = 10€ de réduction loyer</p>
            </div>
        """, unsafe_allow_html=True)
    
    # DASHBOARD GESTIONNAIRE
    elif menu == "📊 Dashboard":
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="font-size: 2.5rem; font-weight: 700; color: #fff;">📊 Dashboard de Gestion</h1>
                <p style="font-size: 1.1rem; color: rgba(255,255,255,0.8);">Vue d'ensemble de votre résidence</p>
            </div>
        """, unsafe_allow_html=True)
        
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
            badge_color = "#ef4444" if incidents_nouveaux > 0 else "#10b981"
            st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="color: rgba(255,255,255,0.7); font-size: 0.9rem; font-weight: 500;">Incidents nouveaux</span>
                        <div style="background: {badge_color}; width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 10px {badge_color};"></div>
                    </div>
                    <div style="font-size: 2.5rem; font-weight: 700; color: #fff; margin-bottom: 0.3rem;">🆕 {incidents_nouveaux}</div>
                    <div style="font-size: 0.8rem; color: rgba(255,255,255,0.6);">À traiter en priorité</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="color: rgba(255,255,255,0.7); font-size: 0.9rem; font-weight: 500;">En cours</span>
                        <div style="background: #f59e0b; width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 10px #f59e0b;"></div>
                    </div>
                    <div style="font-size: 2.5rem; font-weight: 700; color: #fff; margin-bottom: 0.3rem;">⏳ {incidents_encours}</div>
                    <div style="font-size: 0.8rem; color: rgba(255,255,255,0.6);">Interventions en cours</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="color: rgba(255,255,255,0.7); font-size: 0.9rem; font-weight: 500;">Résidents</span>
                        <div style="background: #667eea; width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 10px #667eea;"></div>
                    </div>
                    <div style="font-size: 2.5rem; font-weight: 700; color: #fff; margin-bottom: 0.3rem;">👥 {nb_residents}</div>
                    <div style="font-size: 0.8rem; color: rgba(255,255,255,0.6);">Actifs dans la résidence</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="color: rgba(255,255,255,0.7); font-size: 0.9rem; font-weight: 500;">Réservations</span>
                        <div style="background: #10b981; width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 10px #10b981;"></div>
                    </div>
                    <div style="font-size: 2.5rem; font-weight: 700; color: #fff; margin-bottom: 0.3rem;">📅 {reservations_futures}</div>
                    <div style="font-size: 0.8rem; color: rgba(255,255,255,0.6);">À venir</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
            <h3 style="color: #fff; font-size: 1.5rem; margin-bottom: 1rem;">📈 Activité de la semaine</h3>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            cursor.execute("""
                SELECT COUNT(*) FROM incidents 
                WHERE residence = ? AND date_creation >= date('now', '-7 days')
            """, (user['residence'],))
            incidents_semaine = cursor.fetchone()[0]
            
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);">
                    <div style="font-size: 1rem; color: rgba(255,255,255,0.9); margin-bottom: 0.5rem;">Incidents signalés</div>
                    <div style="font-size: 2rem; font-weight: 700; color: #fff;">{incidents_semaine}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_b:
            cursor.execute("""
                SELECT COUNT(*) FROM participations p
                JOIN evenements e ON p.evenement_id = e.id
                WHERE e.residence = ? AND p.date_inscription >= date('now', '-7 days')
            """, (user['residence'],))
            participations_semaine = cursor.fetchone()[0]
            
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 1.5rem; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);">
                    <div style="font-size: 1rem; color: rgba(255,255,255,0.9); margin-bottom: 0.5rem;">Participations événements</div>
                    <div style="font-size: 2rem; font-weight: 700; color: #fff;">{participations_semaine}</div>
                </div>
            """, unsafe_allow_html=True)
        
        conn.close()
    
    # DASHBOARD PERSONNEL
    elif menu == "🏠 Mes Tâches":
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="font-size: 2.5rem; font-weight: 700; color: #fff;">🏠 Mes Tâches du Jour</h1>
                <p style="font-size: 1.1rem; color: rgba(255,255,255,0.8);">Interventions prioritaires</p>
            </div>
        """, unsafe_allow_html=True)
        
        conn = sqlite3.connect("data/lba_platform.db")
        cursor = conn.cursor()
        
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
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 10px 20px -3px rgba(239, 68, 68, 0.4); border: 2px solid rgba(255,255,255,0.2);">
                    <div style="font-size: 3.5rem; margin-bottom: 0.5rem; animation: pulse 2s infinite;">🔴</div>
                    <div style="font-size: 3rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem;">{critiques}</div>
                    <div style="font-size: 1.1rem; color: #fff; font-weight: 600;">Incidents Critiques</div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.8); margin-top: 0.5rem;">Intervention immédiate requise</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 10px 20px -3px rgba(245, 158, 11, 0.4); border: 2px solid rgba(255,255,255,0.2);">
                    <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🟠</div>
                    <div style="font-size: 3rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem;">{urgents}</div>
                    <div style="font-size: 1.1rem; color: #fff; font-weight: 600;">Incidents Urgents</div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.8); margin-top: 0.5rem;">À traiter rapidement</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 10px 20px -3px rgba(102, 126, 234, 0.4); border: 2px solid rgba(255,255,255,0.2);">
                    <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">📋</div>
                    <div style="font-size: 3rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem;">{taches_total}</div>
                    <div style="font-size: 1.1rem; color: #fff; font-weight: 600;">Total Tâches</div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.8); margin-top: 0.5rem;">En attente de traitement</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Ajouter animation pulse pour le badge critique
        st.markdown("""
            <style>
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
            </style>
        """, unsafe_allow_html=True)
        
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
