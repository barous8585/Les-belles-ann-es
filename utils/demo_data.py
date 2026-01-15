import sqlite3
from utils.database import get_connection, hash_password
from datetime import datetime, timedelta

def creer_donnees_demo():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("Création des comptes de démonstration...")
    
    users_demo = [
        ("demo.resident@lba.com", "demo123", "Dupont", "Marie", "Résident", "Les Belles Années Angers", "A205", "0612345678"),
        ("demo.gestionnaire@lba.com", "demo123", "Martin", "Jean", "Gestionnaire", "Les Belles Années Angers", "Bureau", "0612345679"),
        ("etudiant1@example.com", "demo123", "Bernard", "Pierre", "Résident", "Les Belles Années Lyon", "B102", "0612345680"),
        ("etudiant2@example.com", "demo123", "Petit", "Sophie", "Résident", "Les Belles Années Angers", "A301", "0612345681"),
    ]
    
    for email, password, nom, prenom, type_user, residence, logement, tel in users_demo:
        try:
            hashed_pw = hash_password(password)
            cursor.execute("""
                INSERT INTO users (email, password, nom, prenom, type_utilisateur, residence, numero_logement, telephone, points_fidelite)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (email, hashed_pw, nom, prenom, type_user, residence, logement, tel, 150))
            print(f"✅ Utilisateur créé : {email} (mot de passe: demo123)")
        except sqlite3.IntegrityError:
            print(f"⚠️ Utilisateur déjà existant : {email}")
    
    conn.commit()
    
    cursor.execute("SELECT id FROM users WHERE email = 'demo.resident@lba.com'")
    user_id = cursor.fetchone()[0]
    
    print("\nCréation d'événements de démonstration...")
    evenements_demo = [
        ("Soirée jeux de société", "Venez jouer aux jeux de société dans la salle commune !", "Soirée", 
         datetime.now() + timedelta(days=3), "Salle commune", "Les Belles Années Angers", 20),
        ("Session sport collectif", "Football et basketball au gymnase", "Sport",
         datetime.now() + timedelta(days=5), "Gymnase municipal", "Les Belles Années Angers", 15),
        ("Atelier cuisine internationale", "Apprenez à cuisiner des plats du monde entier", "Culture",
         datetime.now() + timedelta(days=7), "Cuisine commune", "Les Belles Années Angers", 10),
    ]
    
    for titre, desc, cat, date, lieu, res, max_part in evenements_demo:
        try:
            cursor.execute("""
                INSERT INTO evenements (titre, description, categorie, date_evenement, lieu, residence, organisateur_id, nombre_max_participants)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (titre, desc, cat, date, lieu, res, user_id, max_part))
            print(f"✅ Événement créé : {titre}")
        except:
            pass
    
    conn.commit()
    
    print("\nCréation d'annonces marketplace...")
    annonces_demo = [
        ("Vélo VTT en bon état", "Vélo VTT peu utilisé, excellent état, parfait pour la ville", "Vente", 80.0, "Sport", "Les Belles Années Angers"),
        ("Livres de cours informatique", "Lot de 5 livres de cours L1 informatique", "Vente", 30.0, "Livres", "Les Belles Années Angers"),
        ("Micro-ondes à prêter", "Prête mon micro-ondes pour quelques jours", "Prêt", 0.0, "Électronique", "Les Belles Années Angers"),
        ("Canapé 2 places", "Canapé confortable, à venir chercher", "Vente", 50.0, "Meubles", "Les Belles Années Angers"),
    ]
    
    for titre, desc, type_ann, prix, cat, res in annonces_demo:
        try:
            cursor.execute("""
                INSERT INTO marketplace (titre, description, type_annonce, prix, categorie, vendeur_id, residence)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (titre, desc, type_ann, prix, cat, user_id, res))
            print(f"✅ Annonce créée : {titre}")
        except:
            pass
    
    conn.commit()
    
    print("\nCréation d'incidents de démonstration...")
    incidents_demo = [
        ("Fuite d'eau salle de bain", "Petite fuite sous le lavabo", "Plomberie", "Moyenne", "Les Belles Années Angers", "A205"),
        ("Ampoule grillée couloir", "Ampoule du couloir étage 2 ne fonctionne plus", "Électricité", "Faible", "Les Belles Années Angers", "A205"),
    ]
    
    for titre, desc, cat, prio, res, logement in incidents_demo:
        try:
            cursor.execute("""
                INSERT INTO incidents (titre, description, categorie, priorite, residence, logement, user_id, statut)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (titre, desc, cat, prio, res, logement, user_id, "nouveau"))
            print(f"✅ Incident créé : {titre}")
        except:
            pass
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ DONNÉES DE DÉMONSTRATION CRÉÉES AVEC SUCCÈS !")
    print("="*60)
    print("\n🔐 Comptes de test :")
    print("\n1. Compte RÉSIDENT :")
    print("   Email    : demo.resident@lba.com")
    print("   Password : demo123")
    print("\n2. Compte GESTIONNAIRE :")
    print("   Email    : demo.gestionnaire@lba.com")
    print("   Password : demo123")
    print("\n" + "="*60)

if __name__ == "__main__":
    from database import init_database
    init_database()
    creer_donnees_demo()
