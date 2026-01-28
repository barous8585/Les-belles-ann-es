#!/usr/bin/env python3
"""
🌱 Script de Peuplement de Données Démo
Les Belles Années - Plateforme Résidents

Crée un environnement de démo réaliste avec:
- 15 résidents actifs
- 2 gestionnaires
- 3 membres du personnel
- 20+ incidents (variés)
- 15+ événements
- 30+ annonces marketplace
- 40+ réservations
- Historique d'activité sur 30 jours
"""

import sqlite3
from datetime import datetime, timedelta
import random
from utils.database import hash_password

# Configuration
DB_PATH = "data/lba_platform.db"

# Données réalistes
RESIDENCES = [
    "Les Belles Années Angers",
    "Les Belles Années Lyon",
    "Les Belles Années Paris"
]

# Résidents (15)
RESIDENTS = [
    {"email": "marie.dupont@gmail.com", "nom": "Dupont", "prenom": "Marie", "logement": "A101", "telephone": "06 12 34 56 78", "points": 45},
    {"email": "lucas.martin@gmail.com", "nom": "Martin", "prenom": "Lucas", "logement": "A205", "telephone": "06 23 45 67 89", "points": 120},
    {"email": "emma.bernard@gmail.com", "nom": "Bernard", "prenom": "Emma", "logement": "B103", "telephone": "06 34 56 78 90", "points": 85},
    {"email": "hugo.petit@gmail.com", "nom": "Petit", "prenom": "Hugo", "logement": "B207", "telephone": "06 45 67 89 01", "points": 60},
    {"email": "lea.dubois@gmail.com", "nom": "Dubois", "prenom": "Léa", "logement": "C102", "telephone": "06 56 78 90 12", "points": 150},
    {"email": "nathan.moreau@gmail.com", "nom": "Moreau", "prenom": "Nathan", "logement": "C208", "telephone": "06 67 89 01 23", "points": 95},
    {"email": "chloe.laurent@gmail.com", "nom": "Laurent", "prenom": "Chloé", "logement": "D104", "telephone": "06 78 90 12 34", "points": 75},
    {"email": "tom.simon@gmail.com", "nom": "Simon", "prenom": "Tom", "logement": "D201", "telephone": "06 89 01 23 45", "points": 40},
    {"email": "lisa.michel@gmail.com", "nom": "Michel", "prenom": "Lisa", "logement": "E105", "telephone": "06 90 12 34 56", "points": 110},
    {"email": "theo.lefevre@gmail.com", "nom": "Lefèvre", "prenom": "Théo", "logement": "E203", "telephone": "06 01 23 45 67", "points": 55},
    {"email": "sarah.garcia@gmail.com", "nom": "Garcia", "prenom": "Sarah", "logement": "F101", "telephone": "06 12 34 56 89", "points": 135},
    {"email": "alex.roux@gmail.com", "nom": "Roux", "prenom": "Alex", "logement": "F206", "telephone": "06 23 45 67 90", "points": 80},
    {"email": "jade.fontaine@gmail.com", "nom": "Fontaine", "prenom": "Jade", "logement": "G102", "telephone": "06 34 56 78 01", "points": 65},
    {"email": "louis.chevalier@gmail.com", "nom": "Chevalier", "prenom": "Louis", "logement": "G204", "telephone": "06 45 67 89 12", "points": 100},
    {"email": "camille.girard@gmail.com", "nom": "Girard", "prenom": "Camille", "logement": "H103", "telephone": "06 56 78 90 23", "points": 90}
]

# Gestionnaires (2)
GESTIONNAIRES = [
    {"email": "gestionnaire@test.com", "nom": "Rousseau", "prenom": "Sophie", "logement": "Bureau", "telephone": "04 78 17 14 11"},
    {"email": "admin.angers@lesbellesannees.com", "nom": "Blanc", "prenom": "Pierre", "logement": "Direction", "telephone": "02 41 88 99 00"}
]

# Personnel (3)
PERSONNEL = [
    {"email": "personnel@test.com", "nom": "Leroux", "prenom": "Marc", "logement": "Technique", "telephone": "06 11 22 33 44"},
    {"email": "technicien@lesbellesannees.com", "nom": "Bonnet", "prenom": "Julie", "logement": "Maintenance", "telephone": "06 22 33 44 55"},
    {"email": "maintenance@lesbellesannees.com", "nom": "Fournier", "prenom": "David", "logement": "Maintenance", "telephone": "06 33 44 55 66"}
]

# Incidents (variés, réalistes)
INCIDENTS_TEMPLATES = [
    {"titre": "Fuite d'eau salle de bain", "description": "L'évier de la salle de bain fuit depuis ce matin. L'eau coule en continu sous le lavabo.", "categorie": "Plomberie", "priorite": "Haute"},
    {"titre": "Ampoule grillée couloir", "description": "L'ampoule du couloir principal est grillée depuis 3 jours. C'est très sombre le soir.", "categorie": "Électricité", "priorite": "Faible"},
    {"titre": "Chauffage ne fonctionne plus", "description": "Le radiateur de ma chambre ne chauffe plus. Il fait très froid, surtout la nuit.", "categorie": "Chauffage/Climatisation", "priorite": "Critique"},
    {"titre": "WiFi instable", "description": "La connexion WiFi coupe régulièrement depuis 2 jours. Impossible de suivre mes cours en ligne.", "categorie": "Internet/WiFi", "priorite": "Moyenne"},
    {"titre": "Porte qui grince", "description": "La porte d'entrée de mon logement grince beaucoup et se ferme mal.", "categorie": "Serrurerie", "priorite": "Faible"},
    {"titre": "Machine à laver en panne", "description": "La machine à laver 2 de la laverie ne démarre plus. Le voyant rouge clignote.", "categorie": "Équipements (cuisine, salle de bain)", "priorite": "Haute"},
    {"titre": "Ascenseur bloqué", "description": "L'ascenseur du bâtiment B est bloqué au 1er étage depuis ce matin.", "categorie": "Ascenseur", "priorite": "Critique"},
    {"titre": "Bruit voisinage nocturne", "description": "Le voisin du dessus fait beaucoup de bruit après 23h (musique forte).", "categorie": "Nuisances sonores", "priorite": "Moyenne"},
    {"titre": "Fenêtre qui ferme mal", "description": "La fenêtre de la chambre ferme mal, il y a un courant d'air froid.", "categorie": "Autre", "priorite": "Moyenne"},
    {"titre": "Robinet qui fuit cuisine", "description": "Le robinet de la cuisine goutte en permanence. Gaspillage d'eau.", "categorie": "Plomberie", "priorite": "Moyenne"},
    {"titre": "Prise électrique défectueuse", "description": "La prise électrique près du bureau ne fonctionne plus.", "categorie": "Électricité", "priorite": "Moyenne"},
    {"titre": "Chasse d'eau bloquée", "description": "La chasse d'eau des toilettes reste bloquée et l'eau coule en continu.", "categorie": "Plomberie", "priorite": "Haute"},
    {"titre": "Interphone ne fonctionne plus", "description": "L'interphone de mon logement ne sonne plus. Je ne peux plus recevoir de visiteurs.", "categorie": "Autre", "priorite": "Faible"},
    {"titre": "Moisissures salle de bain", "description": "Des moisissures apparaissent sur le mur de la salle de bain près de la douche.", "categorie": "Autre", "priorite": "Moyenne"},
    {"titre": "Four qui ne chauffe pas", "description": "Le four de la cuisine ne chauffe plus correctement. Impossible de cuisiner.", "categorie": "Équipements (cuisine, salle de bain)", "priorite": "Haute"},
    {"titre": "Stores cassés", "description": "Les stores de la chambre sont cassés et ne descendent plus.", "categorie": "Autre", "priorite": "Faible"},
    {"titre": "Douche bouchée", "description": "L'évacuation de la douche est bouchée. L'eau ne s'écoule plus.", "categorie": "Plomberie", "priorite": "Haute"},
    {"titre": "Porte d'entrée qui claque", "description": "La porte d'entrée principale claque très fort à cause du courant d'air.", "categorie": "Autre", "priorite": "Faible"},
    {"titre": "Thermostat défectueux", "description": "Le thermostat du chauffage ne répond plus. Impossible de régler la température.", "categorie": "Chauffage/Climatisation", "priorite": "Haute"},
    {"titre": "Lumière extérieure cassée", "description": "L'éclairage extérieur devant le bâtiment C ne fonctionne plus.", "categorie": "Électricité", "priorite": "Moyenne"}
]

# Événements
EVENEMENTS_TEMPLATES = [
    {"titre": "Soirée Jeux de Société", "description": "Venez passer une soirée conviviale autour de jeux de société ! Apportez vos jeux préférés.", "categorie": "Loisirs", "lieu": "Salle commune", "max_participants": 15},
    {"titre": "Tournoi FIFA 24", "description": "Grand tournoi FIFA 24 sur PS5 ! Inscriptions limitées. Prix pour les 3 premiers.", "categorie": "Sport", "lieu": "Salle de cinéma", "max_participants": 16},
    {"titre": "Atelier Cuisine Italienne", "description": "Apprenez à préparer des pâtes fraîches et une vraie pizza napolitaine avec un chef !", "categorie": "Culture", "lieu": "Cuisine commune", "max_participants": 10},
    {"titre": "Séance Yoga Matinale", "description": "Session de yoga pour bien commencer la journée. Tous niveaux acceptés. Amenez votre tapis.", "categorie": "Sport", "lieu": "Salle de sport", "max_participants": 12},
    {"titre": "Soirée Karaoké", "description": "Soirée karaoké endiablée ! Venez chanter vos tubes préférés dans une ambiance festive.", "categorie": "Loisirs", "lieu": "Salle commune", "max_participants": 25},
    {"titre": "Projection Film : Inception", "description": "Projection du film Inception en version originale. Pop-corn gratuit !", "categorie": "Culture", "lieu": "Salle de cinéma", "max_participants": 20},
    {"titre": "Afterwork Networking", "description": "Rencontre entre résidents pour échanger sur vos projets pro et perso. Apéro offert !", "categorie": "Networking", "lieu": "Terrasse", "max_participants": 30},
    {"titre": "Cours de Salsa Débutant", "description": "Initiez-vous à la salsa avec un prof diplômé. En couple ou solo, tout le monde est bienvenu !", "categorie": "Sport", "lieu": "Salle commune", "max_participants": 20},
    {"titre": "Brunch Communautaire", "description": "Grand brunch partagé ! Chacun apporte un plat à partager. Moment convivial garanti.", "categorie": "Loisirs", "lieu": "Terrasse", "max_participants": 40},
    {"titre": "Atelier Zéro Déchet", "description": "Apprenez à réduire vos déchets au quotidien. Fabrication de produits ménagers naturels.", "categorie": "Culture", "lieu": "Salle de réunion", "max_participants": 15},
    {"titre": "Match de Foot Inter-Résidences", "description": "Match amical contre Les Belles Années Lyon. Supporters bienvenus !", "categorie": "Sport", "lieu": "Stade municipal", "max_participants": 22},
    {"titre": "Soirée Blind Test", "description": "Testez vos connaissances musicales lors d'un blind test endiablé. Équipes de 4 personnes.", "categorie": "Loisirs", "lieu": "Salle commune", "max_participants": 20},
    {"titre": "Initiation Photographie", "description": "Atelier photo avec un photographe pro. Apprenez les bases de la composition et de la lumière.", "categorie": "Culture", "lieu": "Salle de réunion", "max_participants": 12},
    {"titre": "Soirée Tacos Party", "description": "Grande soirée tacos ! Venez garnir vos tacos avec plein d'ingrédients au choix.", "categorie": "Loisirs", "lieu": "Cuisine commune", "max_participants": 25},
    {"titre": "Cours de Méditation", "description": "Séance de méditation guidée pour apprendre à gérer le stress des examens.", "categorie": "Bien-être", "lieu": "Salle de sport", "max_participants": 15}
]

# Annonces Marketplace
MARKETPLACE_TEMPLATES = [
    {"titre": "Canapé 2 places IKEA", "description": "Canapé 2 places gris en bon état. Déménagement, doit partir rapidement.", "type": "Vente", "prix": 80, "categorie": "Meubles"},
    {"titre": "MacBook Pro 2020", "description": "MacBook Pro 13\" 2020, 8Go RAM, 256Go SSD. Très bon état, facture disponible.", "type": "Vente", "prix": 850, "categorie": "Électronique"},
    {"titre": "Livres droit 2ème année", "description": "Pack de 6 livres de droit L2. Annotations au crayon effaçables.", "type": "Vente", "prix": 45, "categorie": "Livres"},
    {"titre": "Vélo de ville", "description": "Vélo de ville homme, 6 vitesses, avec antivol. Quelques rayures mais fonctionne parfaitement.", "type": "Vente", "prix": 120, "categorie": "Sport"},
    {"titre": "Micro-ondes Samsung", "description": "Micro-ondes 20L, 800W, parfait état. Utilisé 6 mois seulement.", "type": "Vente", "prix": 40, "categorie": "Électronique"},
    {"titre": "Bureau en bois", "description": "Bureau en bois massif 120x60cm. Très solide, idéal pour étudier.", "type": "Vente", "prix": 60, "categorie": "Meubles"},
    {"titre": "Perceuse sans fil Bosch", "description": "Perceuse-visseuse sans fil Bosch 18V avec 2 batteries. Comme neuve.", "type": "Prêt", "prix": 0, "categorie": "Autre"},
    {"titre": "Aspirateur Dyson", "description": "Aspirateur balai Dyson V8. Excellent état. Déménagement à l'étranger.", "type": "Vente", "prix": 180, "categorie": "Électronique"},
    {"titre": "Raquettes de tennis", "description": "2 raquettes de tennis Wilson avec housse. Parfaites pour débuter.", "type": "Vente", "prix": 35, "categorie": "Sport"},
    {"titre": "Lampe de bureau LED", "description": "Lampe de bureau LED réglable, 3 modes d'éclairage. Neuve, jamais utilisée.", "type": "Vente", "prix": 15, "categorie": "Meubles"},
    {"titre": "PlayStation 4 + 5 jeux", "description": "PS4 500Go avec manette + 5 jeux (FIFA, GTA V, Uncharted, Spider-Man, COD).", "type": "Vente", "prix": 180, "categorie": "Électronique"},
    {"titre": "Chaise de bureau ergonomique", "description": "Chaise de bureau noire, réglable, très confortable. Achetée 120€.", "type": "Vente", "prix": 50, "categorie": "Meubles"},
    {"titre": "Encyclopédie Universalis", "description": "Collection complète Encyclopédie Universalis 20 volumes. Parfait étudiant.", "type": "Vente", "prix": 25, "categorie": "Livres"},
    {"titre": "Tapis de yoga + bloc", "description": "Tapis de yoga épais (6mm) violet + 2 blocs en liège. Excellent état.", "type": "Prêt", "prix": 0, "categorie": "Sport"},
    {"titre": "Enceinte Bluetooth JBL", "description": "Enceinte JBL Flip 5, son puissant, étanche. Autonomie 12h.", "type": "Vente", "prix": 70, "categorie": "Électronique"},
    {"titre": "Manteau d'hiver North Face", "description": "Doudoune North Face taille M, noire, très chaude. Portée une saison.", "type": "Vente", "prix": 90, "categorie": "Vêtements"},
    {"titre": "Machine à café Nespresso", "description": "Cafetière Nespresso Essenza Mini rouge. Fonctionne parfaitement.", "type": "Vente", "prix": 45, "categorie": "Électronique"},
    {"titre": "Étagère Billy IKEA", "description": "Étagère Billy IKEA blanche, 5 étagères, 80x202cm. Montée mais démontable.", "type": "Vente", "prix": 30, "categorie": "Meubles"},
    {"titre": "Roller en ligne K2", "description": "Rollers K2 taille 42, avec protections (genoux, coudes, poignets).", "type": "Prêt", "prix": 0, "categorie": "Sport"},
    {"titre": "Fer à repasser Philips", "description": "Fer à repasser vapeur Philips 2400W. Semelle céramique, anti-calcaire.", "type": "Vente", "prix": 20, "categorie": "Électronique"},
    {"titre": "Table basse en verre", "description": "Table basse moderne en verre trempé, 100x60cm. Pieds métal chromé.", "type": "Vente", "prix": 40, "categorie": "Meubles"},
    {"titre": "Sac de frappe + gants boxe", "description": "Sac de frappe 25kg avec fixation plafond + gants de boxe 12oz.", "type": "Vente", "prix": 60, "categorie": "Sport"},
    {"titre": "Cours particuliers Maths", "description": "Étudiant ingénieur propose cours particuliers maths lycée/prépa. 20€/h.", "type": "Achat", "prix": 20, "categorie": "Autre"},
    {"titre": "Imprimante HP", "description": "Imprimante HP multifonction (impression, scan, copie). WiFi intégré.", "type": "Vente", "prix": 55, "categorie": "Électronique"},
    {"titre": "Plantes d'intérieur", "description": "3 plantes d'intérieur (Monstera, Pothos, Ficus) avec cache-pots. Faciles d'entretien.", "type": "Vente", "prix": 15, "categorie": "Autre"},
    {"titre": "Tente 2 places Quechua", "description": "Tente 2 secondes Quechua, 2 places. Utilisée 3 fois. Parfait pour festivals.", "type": "Prêt", "prix": 0, "categorie": "Sport"},
    {"titre": "Baskets Nike Air Max", "description": "Baskets Nike Air Max taille 43, blanches et noires. Portées 10 fois max.", "type": "Vente", "prix": 75, "categorie": "Vêtements"},
    {"titre": "Cadre photo numérique", "description": "Cadre photo numérique 10\", WiFi, stockage 8Go. Neuf sous emballage.", "type": "Vente", "prix": 35, "categorie": "Électronique"},
    {"titre": "Guitare acoustique Yamaha", "description": "Guitare acoustique Yamaha F310 avec housse et accordeur. Débutant/intermédiaire.", "type": "Vente", "prix": 110, "categorie": "Autre"},
    {"titre": "Valise cabine Samsonite", "description": "Valise cabine rigide Samsonite noire, 4 roues. Parfait état, utilisée 2 fois.", "type": "Vente", "prix": 65, "categorie": "Autre"}
]

def clear_database():
    """Supprime toutes les données existantes (sauf structure)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    tables = ['users', 'incidents', 'evenements', 'participations', 'marketplace', 'reservations', 'messages_chat', 'login_attempts']
    
    for table in tables:
        try:
            cursor.execute(f"DELETE FROM {table}")
            print(f"✓ Table {table} vidée")
        except Exception as e:
            print(f"⚠ Erreur table {table}: {e}")
    
    conn.commit()
    conn.close()

def create_users():
    """Crée les utilisateurs (résidents, gestionnaires, personnel)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    password_hash = hash_password("Password1")
    user_ids = {}
    
    # Résidents
    print("\n👥 Création des résidents...")
    for resident in RESIDENTS:
        cursor.execute("""
            INSERT INTO users (email, password, nom, prenom, type_utilisateur, residence, numero_logement, telephone, points_fidelite)
            VALUES (?, ?, ?, ?, 'Résident', ?, ?, ?, ?)
        """, (resident['email'], password_hash, resident['nom'], resident['prenom'], 
              RESIDENCES[0], resident['logement'], resident['telephone'], resident['points']))
        user_ids[resident['email']] = cursor.lastrowid
        print(f"  ✓ {resident['prenom']} {resident['nom']} - {resident['logement']} ({resident['points']} pts)")
    
    # Gestionnaires
    print("\n👔 Création des gestionnaires...")
    for gest in GESTIONNAIRES:
        cursor.execute("""
            INSERT INTO users (email, password, nom, prenom, type_utilisateur, residence, numero_logement, telephone, points_fidelite)
            VALUES (?, ?, ?, ?, 'Gestionnaire', ?, ?, ?, 0)
        """, (gest['email'], password_hash, gest['nom'], gest['prenom'], 
              RESIDENCES[0], gest['logement'], gest['telephone']))
        user_ids[gest['email']] = cursor.lastrowid
        print(f"  ✓ {gest['prenom']} {gest['nom']} - {gest['logement']}")
    
    # Personnel
    print("\n🔧 Création du personnel...")
    for perso in PERSONNEL:
        cursor.execute("""
            INSERT INTO users (email, password, nom, prenom, type_utilisateur, residence, numero_logement, telephone, points_fidelite)
            VALUES (?, ?, ?, ?, 'Personnel', ?, ?, ?, 0)
        """, (perso['email'], password_hash, perso['nom'], perso['prenom'], 
              RESIDENCES[0], perso['logement'], perso['telephone']))
        user_ids[perso['email']] = cursor.lastrowid
        print(f"  ✓ {perso['prenom']} {perso['nom']} - {perso['logement']}")
    
    conn.commit()
    conn.close()
    
    return user_ids

def create_incidents(user_ids):
    """Crée des incidents variés avec statuts différents"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n🔧 Création des incidents...")
    
    resident_ids = [user_ids[r['email']] for r in RESIDENTS]
    statuts = ['nouveau', 'en_cours', 'résolu']
    
    for i, template in enumerate(INCIDENTS_TEMPLATES):
        # Varier les dates (derniers 30 jours)
        jours_avant = random.randint(0, 30)
        date_creation = datetime.now() - timedelta(days=jours_avant)
        
        # Statut selon l'ancienneté
        if jours_avant < 2:
            statut = 'nouveau'
            date_resolution = None
        elif jours_avant < 10:
            statut = random.choice(['nouveau', 'en_cours'])
            date_resolution = None
        else:
            statut = random.choice(['en_cours', 'résolu'])
            date_resolution = date_creation + timedelta(days=random.randint(1, 5)) if statut == 'résolu' else None
        
        user_id = random.choice(resident_ids)
        logement = next(r['logement'] for r in RESIDENTS if user_ids[r['email']] == user_id)
        
        cursor.execute("""
            INSERT INTO incidents (titre, description, categorie, priorite, statut, residence, logement, user_id, date_creation, date_resolution, note_satisfaction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (template['titre'], template['description'], template['categorie'], template['priorite'],
              statut, RESIDENCES[0], logement, user_id, date_creation, date_resolution,
              random.randint(3, 5) if statut == 'résolu' else None))
        
        print(f"  ✓ {template['titre']} - {statut} ({template['priorite']})")
    
    conn.commit()
    conn.close()

def create_evenements(user_ids):
    """Crée des événements passés et à venir"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n🎉 Création des événements...")
    
    resident_ids = [user_ids[r['email']] for r in RESIDENTS]
    
    for i, template in enumerate(EVENEMENTS_TEMPLATES):
        # Événements passés (-15 à -1 jours) et futurs (+1 à +30 jours)
        if i % 2 == 0:
            jours = random.randint(1, 30)  # Futur
            statut = 'ouvert'
        else:
            jours = -random.randint(1, 15)  # Passé
            statut = 'termine'
        
        date_evenement = datetime.now() + timedelta(days=jours)
        organisateur_id = random.choice(resident_ids)
        
        cursor.execute("""
            INSERT INTO evenements (titre, description, categorie, date_evenement, lieu, residence, organisateur_id, nombre_max_participants, statut, date_creation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (template['titre'], template['description'], template['categorie'], date_evenement,
              template['lieu'], RESIDENCES[0], organisateur_id, template['max_participants'], 
              statut, datetime.now() - timedelta(days=random.randint(1, 40))))
        
        event_id = cursor.lastrowid
        
        # Ajouter des participants (30-70% des places)
        nb_participants = random.randint(int(template['max_participants'] * 0.3), 
                                        int(template['max_participants'] * 0.7))
        participants = random.sample(resident_ids, min(nb_participants, len(resident_ids)))
        
        for participant_id in participants:
            cursor.execute("""
                INSERT INTO participations (evenement_id, user_id, date_inscription)
                VALUES (?, ?, ?)
            """, (event_id, participant_id, datetime.now() - timedelta(days=random.randint(1, 20))))
        
        print(f"  ✓ {template['titre']} - {len(participants)}/{template['max_participants']} participants")
    
    conn.commit()
    conn.close()

def create_marketplace(user_ids):
    """Crée des annonces marketplace actives"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n🛍️ Création des annonces marketplace...")
    
    resident_ids = [user_ids[r['email']] for r in RESIDENTS]
    
    for template in MARKETPLACE_TEMPLATES:
        vendeur_id = random.choice(resident_ids)
        jours_avant = random.randint(1, 60)
        date_creation = datetime.now() - timedelta(days=jours_avant)
        
        cursor.execute("""
            INSERT INTO marketplace (titre, description, type_annonce, prix, categorie, statut, vendeur_id, residence, date_creation)
            VALUES (?, ?, ?, ?, ?, 'disponible', ?, ?, ?)
        """, (template['titre'], template['description'], template['type'], template['prix'],
              template['categorie'], vendeur_id, RESIDENCES[0], date_creation))
        
        print(f"  ✓ {template['titre']} - {template['type']} {template['prix']}€")
    
    conn.commit()
    conn.close()

def create_reservations(user_ids):
    """Crée des réservations d'espaces (passées et futures)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n📅 Création des réservations...")
    
    resident_ids = [user_ids[r['email']] for r in RESIDENTS]
    
    espaces = {
        "Laverie": ["Machine à laver 1", "Machine à laver 2", "Sèche-linge 1", "Sèche-linge 2"],
        "Salle de sport": ["Salle principale", "Zone cardio", "Zone musculation"],
        "Salle de réunion": ["Salle de réunion"],
        "Espace co-working": ["Espace co-working"],
        "Cuisine commune": ["Cuisine commune"],
        "Terrasse/Jardin": ["Terrasse/Jardin"]
    }
    
    durees = [0.5, 1, 1.5, 2, 3, 4]  # En heures
    
    # Créer 40 réservations sur 30 jours (passé et futur)
    for _ in range(40):
        type_espace = random.choice(list(espaces.keys()))
        espace = random.choice(espaces[type_espace])
        user_id = random.choice(resident_ids)
        
        # Mix passé/futur
        jours = random.randint(-15, 15)
        heure = random.randint(8, 20)
        
        debut = datetime.now() + timedelta(days=jours)
        debut = debut.replace(hour=heure, minute=0, second=0, microsecond=0)
        fin = debut + timedelta(hours=random.choice(durees))
        
        cursor.execute("""
            INSERT INTO reservations (type_espace, espace, residence, user_id, date_debut, date_fin, statut)
            VALUES (?, ?, ?, ?, ?, ?, 'confirmee')
        """, (type_espace, espace, RESIDENCES[0], user_id, debut, fin))
    
    print(f"  ✓ 40 réservations créées")
    
    conn.commit()
    conn.close()

def print_summary():
    """Affiche un résumé des données créées"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES DONNÉES CRÉÉES")
    print("="*60)
    
    # Users
    cursor.execute("SELECT type_utilisateur, COUNT(*) FROM users GROUP BY type_utilisateur")
    for type_user, count in cursor.fetchall():
        print(f"👤 {type_user}s: {count}")
    
    # Incidents
    cursor.execute("SELECT statut, COUNT(*) FROM incidents GROUP BY statut")
    print("\n🔧 Incidents:")
    for statut, count in cursor.fetchall():
        print(f"  • {statut}: {count}")
    
    # Événements
    cursor.execute("SELECT statut, COUNT(*) FROM evenements GROUP BY statut")
    print("\n🎉 Événements:")
    for statut, count in cursor.fetchall():
        print(f"  • {statut}: {count}")
    
    # Marketplace
    cursor.execute("SELECT COUNT(*) FROM marketplace WHERE statut = 'disponible'")
    print(f"\n🛍️ Annonces marketplace: {cursor.fetchone()[0]}")
    
    # Réservations
    cursor.execute("SELECT COUNT(*) FROM reservations WHERE date_debut >= datetime('now')")
    futures = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM reservations WHERE date_debut < datetime('now')")
    passees = cursor.fetchone()[0]
    print(f"\n📅 Réservations:")
    print(f"  • À venir: {futures}")
    print(f"  • Passées: {passees}")
    
    # Participations événements
    cursor.execute("SELECT COUNT(*) FROM participations")
    print(f"\n🎯 Participations événements: {cursor.fetchone()[0]}")
    
    conn.close()
    
    print("\n" + "="*60)
    print("✅ BASE DE DONNÉES PEUPLÉE AVEC SUCCÈS !")
    print("="*60)
    print("\n🔑 Comptes de connexion créés:")
    print("\n👥 RÉSIDENTS (tous avec mot de passe: Password1):")
    for i, r in enumerate(RESIDENTS[:5], 1):
        print(f"  {i}. {r['email']} - {r['prenom']} {r['nom']} ({r['logement']}) - {r['points']} pts")
    print(f"  ... et {len(RESIDENTS) - 5} autres résidents\n")
    
    print("👔 GESTIONNAIRES:")
    for g in GESTIONNAIRES:
        print(f"  • {g['email']} - {g['prenom']} {g['nom']}")
    
    print("\n🔧 PERSONNEL:")
    for p in PERSONNEL:
        print(f"  • {p['email']} - {p['prenom']} {p['nom']}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    print("="*60)
    print("🌱 PEUPLEMENT BASE DE DONNÉES - LES BELLES ANNÉES")
    print("="*60)
    
    print("\n⚠️  ATTENTION: Cette opération va SUPPRIMER toutes les données existantes !")
    response = input("Continuer ? (oui/non): ")
    
    if response.lower() in ['oui', 'o', 'yes', 'y']:
        print("\n🗑️  Nettoyage de la base de données...")
        clear_database()
        
        print("\n🌱 Création des données de démo...")
        user_ids = create_users()
        create_incidents(user_ids)
        create_evenements(user_ids)
        create_marketplace(user_ids)
        create_reservations(user_ids)
        
        print_summary()
        
        print("\n🚀 Vous pouvez maintenant lancer l'application:")
        print("   streamlit run app.py")
        print("\n💡 Connectez-vous avec un des comptes ci-dessus (mot de passe: Password1)")
    else:
        print("\n❌ Opération annulée.")
