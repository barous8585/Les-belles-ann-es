import streamlit as st
from utils.auth import get_current_user
import sqlite3
from datetime import datetime

def show():
    user = get_current_user()
    st.title("👥 Vie Communautaire")
    
    tab1, tab2, tab3 = st.tabs(["🎉 Événements", "🛍️ Marketplace", "🤝 Parrainage"])
    
    with tab1:
        show_evenements(user)
    
    with tab2:
        show_marketplace(user)
    
    with tab3:
        show_parrainage(user)

def show_evenements(user):
    st.subheader("Événements dans votre résidence")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📅 Événements à venir")
        
        conn = sqlite3.connect("data/lba_platform.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id, e.titre, e.description, e.categorie, e.date_evenement, e.lieu, 
                   e.nombre_max_participants, u.prenom, u.nom,
                   (SELECT COUNT(*) FROM participations WHERE evenement_id = e.id) as nb_inscrits
            FROM evenements e
            JOIN users u ON e.organisateur_id = u.id
            WHERE e.residence = ? AND e.statut = 'ouvert'
            ORDER BY e.date_evenement
        """, (user['residence'],))
        evenements = cursor.fetchall()
        
        if evenements:
            for evt in evenements:
                evt_id, titre, description, categorie, date, lieu, max_part, prenom_org, nom_org, nb_inscrits = evt
                
                with st.expander(f"🎯 {titre} - {categorie}"):
                    st.write(f"**Description:** {description}")
                    st.write(f"**📍 Lieu:** {lieu}")
                    st.write(f"**📅 Date:** {date}")
                    st.write(f"**👤 Organisateur:** {prenom_org} {nom_org}")
                    st.write(f"**👥 Inscrits:** {nb_inscrits}/{max_part if max_part else 'Illimité'}")
                    
                    cursor.execute("SELECT * FROM participations WHERE evenement_id = ? AND user_id = ?", (evt_id, user['id']))
                    deja_inscrit = cursor.fetchone() is not None
                    
                    if deja_inscrit:
                        st.success("✅ Vous êtes inscrit !")
                        if st.button(f"Se désinscrire", key=f"unsub_{evt_id}"):
                            cursor.execute("DELETE FROM participations WHERE evenement_id = ? AND user_id = ?", (evt_id, user['id']))
                            conn.commit()
                            st.rerun()
                    else:
                        if st.button(f"S'inscrire", key=f"sub_{evt_id}"):
                            cursor.execute("INSERT INTO participations (evenement_id, user_id) VALUES (?, ?)", (evt_id, user['id']))
                            cursor.execute("UPDATE users SET points_fidelite = points_fidelite + 10 WHERE id = ?", (user['id'],))
                            conn.commit()
                            st.success("Inscription réussie ! +10 points de fidélité")
                            st.rerun()
        else:
            st.info("Aucun événement prévu pour le moment. Créez-en un !")
        
        conn.close()
    
    with col2:
        st.markdown("### ➕ Créer un événement")
        with st.form("create_event"):
            titre = st.text_input("Titre de l'événement")
            description = st.text_area("Description")
            categorie = st.selectbox("Catégorie", ["Soirée", "Sport", "Étude", "Culture", "Entraide", "Autre"])
            date_evt = st.date_input("Date")
            heure_evt = st.time_input("Heure")
            lieu = st.text_input("Lieu")
            max_participants = st.number_input("Nombre max de participants", min_value=0, value=20)
            
            if st.form_submit_button("Créer l'événement"):
                if titre and description:
                    date_complete = datetime.combine(date_evt, heure_evt)
                    conn = sqlite3.connect("data/lba_platform.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO evenements (titre, description, categorie, date_evenement, lieu, residence, organisateur_id, nombre_max_participants)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (titre, description, categorie, date_complete, lieu, user['residence'], user['id'], max_participants))
                    cursor.execute("UPDATE users SET points_fidelite = points_fidelite + 25 WHERE id = ?", (user['id'],))
                    conn.commit()
                    conn.close()
                    st.success("Événement créé avec succès ! +25 points")
                    st.rerun()

def show_marketplace(user):
    st.subheader("Marketplace - Acheter, Vendre, Échanger")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🛍️ Annonces disponibles")
        
        conn = sqlite3.connect("data/lba_platform.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.id, m.titre, m.description, m.type_annonce, m.prix, m.categorie, u.prenom, u.nom, m.date_creation
            FROM marketplace m
            JOIN users u ON m.vendeur_id = u.id
            WHERE m.residence = ? AND m.statut = 'disponible'
            ORDER BY m.date_creation DESC
        """, (user['residence'],))
        annonces = cursor.fetchall()
        
        if annonces:
            for annonce in annonces:
                ann_id, titre, desc, type_ann, prix, cat, prenom, nom, date_creation = annonce
                
                with st.expander(f"{titre} - {type_ann}"):
                    st.write(f"**Catégorie:** {cat}")
                    st.write(f"**Description:** {desc}")
                    if type_ann == "Vente":
                        st.write(f"**💰 Prix:** {prix}€")
                    elif type_ann == "Prêt":
                        st.write(f"**Prix:** Gratuit (prêt)")
                    st.write(f"**👤 Proposé par:** {prenom} {nom}")
                    st.write(f"**📅 Publié le:** {date_creation}")
                    st.button("Contacter", key=f"contact_{ann_id}")
        else:
            st.info("Aucune annonce pour le moment. Soyez le premier !")
        
        conn.close()
    
    with col2:
        st.markdown("### ➕ Créer une annonce")
        with st.form("create_annonce"):
            titre = st.text_input("Titre")
            description = st.text_area("Description")
            type_annonce = st.selectbox("Type", ["Vente", "Achat", "Prêt", "Échange"])
            categorie = st.selectbox("Catégorie", ["Meubles", "Électronique", "Livres", "Vêtements", "Sport", "Autre"])
            prix = st.number_input("Prix (€)", min_value=0.0, value=0.0)
            
            if st.form_submit_button("Publier l'annonce"):
                if titre and description:
                    conn = sqlite3.connect("data/lba_platform.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO marketplace (titre, description, type_annonce, prix, categorie, vendeur_id, residence)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (titre, description, type_annonce, prix, categorie, user['id'], user['residence']))
                    cursor.execute("UPDATE users SET points_fidelite = points_fidelite + 5 WHERE id = ?", (user['id'],))
                    conn.commit()
                    conn.close()
                    st.success("Annonce publiée ! +5 points")
                    st.rerun()

def show_parrainage(user):
    st.subheader("Programme de Parrainage")
    
    st.info("🎁 Parrainez un ami et gagnez 50 points chacun !")
    
    code_parrainage = f"LBA-{user['id']}-{user['nom'][:3].upper()}"
    
    st.markdown(f"### Votre code de parrainage")
    st.code(code_parrainage, language=None)
    
    st.markdown("""
    **Comment ça marche ?**
    1. Partagez votre code avec vos amis
    2. Ils l'utilisent lors de leur inscription
    3. Vous gagnez tous les deux 50 points de fidélité !
    
    **Avantages :**
    - 50 points par filleul
    - Réductions cumulables
    - Aide un ami à trouver son logement
    """)
    
    st.markdown("### 📊 Vos parrainages")
    st.metric("Nombre de filleuls", 0)
    st.metric("Points gagnés via parrainage", 0)
