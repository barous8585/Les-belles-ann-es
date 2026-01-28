import streamlit as st
from utils.auth import get_current_user
import sqlite3
from datetime import datetime

def show():
    user = get_current_user()
    st.title("👥 Modération - Communauté")
    
    if user['type'] != 'Gestionnaire':
        st.error("⛔ Accès refusé - Réservé aux gestionnaires")
        return
    
    tab1, tab2, tab3 = st.tabs(["🛍️ Marketplace", "🎉 Événements", "📊 Statistiques"])
    
    with tab1:
        moderate_marketplace(user)
    
    with tab2:
        moderate_events(user)
    
    with tab3:
        show_community_stats(user)

def moderate_marketplace(user):
    st.subheader("🛍️ Modération Marketplace")
    
    conn = sqlite3.connect("data/lba_platform.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT m.id, m.titre, m.description, m.type_annonce, m.prix, m.categorie, m.statut,
               u.prenom, u.nom, u.email, m.date_creation
        FROM marketplace m
        JOIN users u ON m.vendeur_id = u.id
        WHERE m.residence = ?
        ORDER BY m.date_creation DESC
    """, (user['residence'],))
    
    annonces = cursor.fetchall()
    
    if annonces:
        for ann in annonces:
            ann_id, titre, desc, type_ann, prix, cat, statut, prenom, nom, email, date_c = ann
            
            statut_color = "🟢" if statut == "disponible" else "🔴" if statut == "supprimée" else "🟡"
            
            with st.expander(f"{statut_color} {titre} - {type_ann} ({statut})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Catégorie:** {cat}")
                    st.write(f"**Description:** {desc}")
                    if type_ann == "Vente":
                        st.write(f"**Prix:** {prix}€")
                    st.write(f"**Publié le:** {date_c}")
                
                with col2:
                    st.write(f"**Vendeur:** {prenom} {nom}")
                    st.write(f"**Email:** {email}")
                    st.write(f"**Statut:** {statut}")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    if statut != "supprimée":
                        if st.button("❌ Supprimer", key=f"del_ann_{ann_id}"):
                            cursor.execute("UPDATE marketplace SET statut = 'supprimée' WHERE id = ?", (ann_id,))
                            conn.commit()
                            st.success("Annonce supprimée")
                            st.rerun()
                
                with col_b:
                    if statut == "supprimée":
                        if st.button("✅ Restaurer", key=f"rest_ann_{ann_id}"):
                            cursor.execute("UPDATE marketplace SET statut = 'disponible' WHERE id = ?", (ann_id,))
                            conn.commit()
                            st.success("Annonce restaurée")
                            st.rerun()
    else:
        st.info("Aucune annonce")
    
    conn.close()

def moderate_events(user):
    st.subheader("🎉 Modération Événements")
    
    conn = sqlite3.connect("data/lba_platform.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT e.id, e.titre, e.description, e.categorie, e.date_evenement, e.lieu, 
               e.nombre_max_participants, e.statut, u.prenom, u.nom,
               (SELECT COUNT(*) FROM participations WHERE evenement_id = e.id) as nb_inscrits
        FROM evenements e
        JOIN users u ON e.organisateur_id = u.id
        WHERE e.residence = ?
        ORDER BY e.date_evenement DESC
    """, (user['residence'],))
    
    events = cursor.fetchall()
    
    if events:
        for evt in events:
            evt_id, titre, desc, cat, date_evt, lieu, max_part, statut, prenom, nom, nb_inscrits = evt
            
            statut_color = "🟢" if statut == "ouvert" else "🔴" if statut == "annulé" else "⚪"
            
            with st.expander(f"{statut_color} {titre} - {date_evt} ({statut})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Catégorie:** {cat}")
                    st.write(f"**Description:** {desc}")
                    st.write(f"**📍 Lieu:** {lieu}")
                    st.write(f"**📅 Date:** {date_evt}")
                
                with col2:
                    st.write(f"**Organisateur:** {prenom} {nom}")
                    st.write(f"**Participants:** {nb_inscrits}/{max_part or 'Illimité'}")
                    st.write(f"**Statut:** {statut}")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    if statut != "annulé":
                        if st.button("❌ Annuler", key=f"cancel_evt_{evt_id}"):
                            cursor.execute("UPDATE evenements SET statut = 'annulé' WHERE id = ?", (evt_id,))
                            conn.commit()
                            st.warning("Événement annulé")
                            st.rerun()
                
                with col_b:
                    if statut == "annulé":
                        if st.button("✅ Réactiver", key=f"react_evt_{evt_id}"):
                            cursor.execute("UPDATE evenements SET statut = 'ouvert' WHERE id = ?", (evt_id,))
                            conn.commit()
                            st.success("Événement réactivé")
                            st.rerun()
    else:
        st.info("Aucun événement")
    
    conn.close()

def show_community_stats(user):
    st.subheader("📊 Statistiques Communauté")
    
    conn = sqlite3.connect("data/lba_platform.db")
    cursor = conn.cursor()
    
    col1, col2, col3 = st.columns(3)
    
    cursor.execute("SELECT COUNT(*) FROM marketplace WHERE residence = ? AND statut = 'disponible'", (user['residence'],))
    annonces_actives = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM evenements WHERE residence = ? AND statut = 'ouvert'", (user['residence'],))
    events_ouverts = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(DISTINCT p.user_id)
        FROM participations p
        JOIN evenements e ON p.evenement_id = e.id
        WHERE e.residence = ? AND e.date_evenement >= date('now', '-30 days')
    """, (user['residence'],))
    users_actifs = cursor.fetchone()[0]
    
    with col1:
        st.metric("Annonces actives", annonces_actives)
    
    with col2:
        st.metric("Événements ouverts", events_ouverts)
    
    with col3:
        st.metric("Utilisateurs actifs (30j)", users_actifs)
    
    st.markdown("---")
    st.subheader("📈 Top Contributeurs")
    
    cursor.execute("""
        SELECT u.prenom, u.nom, COUNT(*) as nb_annonces
        FROM marketplace m
        JOIN users u ON m.vendeur_id = u.id
        WHERE m.residence = ?
        GROUP BY m.vendeur_id
        ORDER BY nb_annonces DESC
        LIMIT 5
    """, (user['residence'],))
    
    top_sellers = cursor.fetchall()
    
    if top_sellers:
        st.markdown("**🏆 Top Vendeurs Marketplace**")
        for i, (prenom, nom, nb) in enumerate(top_sellers, 1):
            st.write(f"{i}. {prenom} {nom} - {nb} annonce(s)")
    
    st.markdown("---")
    
    cursor.execute("""
        SELECT u.prenom, u.nom, COUNT(*) as nb_events
        FROM evenements e
        JOIN users u ON e.organisateur_id = u.id
        WHERE e.residence = ?
        GROUP BY e.organisateur_id
        ORDER BY nb_events DESC
        LIMIT 5
    """, (user['residence'],))
    
    top_organizers = cursor.fetchall()
    
    if top_organizers:
        st.markdown("**🎉 Top Organisateurs Événements**")
        for i, (prenom, nom, nb) in enumerate(top_organizers, 1):
            st.write(f"{i}. {prenom} {nom} - {nb} événement(s)")
    
    conn.close()
