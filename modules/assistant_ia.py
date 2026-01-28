import streamlit as st
from utils.auth import get_current_user
import sqlite3
from datetime import datetime

def show():
    user = get_current_user()
    
    if user['type'] == 'Résident':
        st.title("🤖 Assistant IA Personnel")
        st.info("💡 Posez-moi vos questions sur : réservations, aide administrative, informations résidence, bons plans locaux, etc.")
    elif user['type'] == 'Gestionnaire':
        st.title("🤖 Assistant Gestionnaire")
        st.info("💡 Posez-moi vos questions sur : gestion incidents, statistiques, réservations, modération, etc.")
    else:
        st.title("🤖 Assistant Personnel")
        st.info("💡 Posez-moi vos questions sur : interventions, maintenance, planning, etc.")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    for msg in st.session_state.chat_history:
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.write(msg["content"])
    
    user_message = st.chat_input("Tapez votre message...")
    
    if user_message:
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        
        with st.chat_message("user"):
            st.write(user_message)
        
        response = generer_reponse_ia(user_message, user)
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.write(response)
        
        conn = sqlite3.connect("data/lba_platform.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages_chat (user_id, message, reponse) VALUES (?, ?, ?)", 
                      (user['id'], user_message, response))
        conn.commit()
        conn.close()

def generer_reponse_ia(message, user):
    message_lower = message.lower()
    residence = user['residence']
    ville = residence.split()[-1] if residence else "votre ville"
    user_type = user['type']
    
    # RÉPONSES SPÉCIFIQUES GESTIONNAIRES
    if user_type in ['Gestionnaire', 'Personnel']:
        if any(word in message_lower for word in ["incident", "problème", "maintenance", "réparation"]):
            return f"""🔧 **Gestion des Incidents - {residence}**

**Vue d'ensemble :**
Allez dans **🔧 Maintenance** > **📈 Statistiques** pour voir :
- Incidents nouveaux à traiter
- Incidents en cours
- Taux de satisfaction
- Répartition par catégorie

**Actions rapides :**
- Changer statut : nouveau → en_cours → résolu
- Voir tous les incidents de la résidence
- Filtrer par priorité/catégorie

💡 Les incidents critiques sont en haut de la liste !"""
        
        elif any(word in message_lower for word in ["réservation", "planning", "occupation"]):
            return f"""📅 **Planning Global - {residence}**

**Accédez au planning :**
Menu **📅 Planning Global** pour :
- Voir toutes les réservations
- Filtrer par date/espace
- Bloquer des créneaux (maintenance)
- Statistiques d'utilisation

**Espaces les plus réservés :**
Consultez les statistiques pour optimiser la gestion !

💡 Vous pouvez annuler une réservation si nécessaire."""
        
        elif any(word in message_lower for word in ["modération", "marketplace", "événement", "annonce"]):
            return f"""👥 **Modération Communauté**

**Accédez à la modération :**
Menu **👥 Modération** pour :
- Modérer annonces marketplace
- Valider/Annuler événements
- Voir top contributeurs
- Statistiques communauté

**Actions possibles :**
- Supprimer/Restaurer annonces
- Annuler/Réactiver événements
- Contacter organisateurs

💡 Gardez la communauté saine et active !"""
        
        elif any(word in message_lower for word in ["statistique", "analytics", "kpi", "dashboard"]):
            return f"""📊 **Analytics & KPIs - {residence}**

**Dashboard principal :**
Menu **📊 Dashboard** affiche :
- Incidents nouveaux/en cours
- Nombre de résidents
- Réservations futures
- Activité de la semaine

**Analytics détaillées :**
Menu **📈 Analytics** pour graphiques avancés :
- Répartition incidents par catégorie
- Statuts (camembert)
- Priorités actives
- Taux de résolution

💡 Utilisez ces données pour optimiser la gestion !"""
        
        else:
            return f"""🤖 **Assistant Gestionnaire - {residence}**

**Modules disponibles :**

📊 **Dashboard** - Vue d'ensemble KPIs
🔧 **Maintenance** - Gérer tous les incidents
📅 **Planning Global** - Toutes les réservations
👥 **Modération** - Marketplace & Événements
📈 **Analytics** - Statistiques avancées

**Questions fréquentes :**
- "Combien d'incidents nouveaux ?"
- "Qui a réservé la laverie aujourd'hui ?"
- "Quelles annonces marketplace modérer ?"
- "Statistiques satisfaction résidents ?"

**Que puis-je faire pour vous ?**"""
    
    # RÉPONSES POUR RÉSIDENTS (suite du code original)
    # Réservations
    if any(word in message_lower for word in ["réserver", "réservation", "laverie", "salle", "sport", "booking", "réserve", "disponibilité", "dispo", "machine", "laver", "linge", "fitness", "gym", "entrainement"]):
        if "laverie" in message_lower:
            return f"""🧺 **Réservation de la laverie**

Pour réserver une machine :
1. Allez dans 📅 **Réservations** (menu de gauche)
2. Choisissez "Laverie" 
3. Sélectionnez votre machine (4 disponibles)
4. Choisissez date et créneau horaire
5. Confirmez !

💡 **Astuce** : Réservez à l'avance, les créneaux 18h-21h sont très demandés !
✨ Bonus : +3 points de fidélité par réservation"""
        elif "sport" in message_lower:
            return f"""🏋️ **Salle de sport**

Notre salle est équipée de :
- 🏃 Zone cardio (tapis, vélos, elliptiques)
- 💪 Zone musculation (haltères, machines guidées)
- 🧘 Espace stretching

**Horaires** : 6h-23h tous les jours
**Réservation** : Section 📅 Réservations
**Capacité** : 15 personnes maximum

💡 Créneaux calmes : 10h-12h et 14h-17h"""
        else:
            return f"""📅 **Espaces réservables à {residence}**

Vous pouvez réserver :
• 🧺 **Laverie** (4 machines, 24h/24)
• 🏋️ **Salle de sport** (6h-23h)
• 🍳 **Cuisine commune** (8h-22h)
• 💼 **Salle de réunion** (travail en groupe)
• ☕ **Espace co-working** (calme et wifi)
• 🌳 **Terrasse/Jardin** (événements)

➡️ Rendez-vous dans **📅 Réservations** pour réserver !"""
    
    # Incidents et maintenance
    elif any(word in message_lower for word in ["problème", "panne", "cassé", "incident", "réparation", "bug", "défaut", "fuite", "marche pas", "fonctionne pas", "dysfonctionnement", "help", "urgent", "sos"]):
        return f"""🔧 **Signalement d'incident**

Pour signaler un problème :
1. Menu **🔧 Maintenance**
2. Onglet **📝 Signaler un incident**
3. Remplissez le formulaire :
   - Titre court
   - Catégorie (plomberie, électricité, etc.)
   - Niveau d'urgence
   - Description détaillée
   - Photo si possible

⏱️ **Délais d'intervention** :
- 🔴 Critique : < 2h
- 🟠 Urgent : < 24h  
- 🟡 Moyen : < 3 jours
- 🟢 Faible : < 1 semaine

📊 Vous pouvez suivre l'état en temps réel dans "Mes incidents" !"""
    
    # Événements
    elif any(word in message_lower for word in ["événement", "activité", "soirée", "sortie", "fête", "animation", "event", "happening", "rencontre", "party", "atelier"]):
        conn = sqlite3.connect("data/lba_platform.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM evenements WHERE residence = ? AND statut = 'ouvert'", (residence,))
        count = cursor.fetchone()[0]
        conn.close()
        
        return f"""🎉 **Événements à {residence}**

📊 **{count} événement(s) disponible(s)** actuellement !

**Comment participer ?**
1. Menu **👥 Communauté**
2. Onglet **🎉 Événements**
3. Parcourez les activités
4. Cliquez "S'inscrire"

**Créer votre événement ?**
- Soirées jeux, sport, cuisine, culture...
- Gagnez **+25 points** en organisant !
- Les participants gagnent **+10 points** chacun

💡 Idées populaires : soirées jeux, sessions sport, ateliers cuisine, ciné-débats"""
    
    # Marketplace
    elif any(word in message_lower for word in ["vendre", "acheter", "marketplace", "annonce", "occasion", "vente", "achat", "vends", "achète", "cherche", "recherche", "seconde main"]):
        conn = sqlite3.connect("data/lba_platform.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM marketplace WHERE residence = ? AND statut = 'disponible'", (residence,))
        count = cursor.fetchone()[0]
        conn.close()
        
        return f"""🛍️ **Marketplace - {count} annonce(s) disponible(s)**

**Acheter :**
1. Menu **👥 Communauté** > **Marketplace**
2. Parcourez les annonces
3. Contactez le vendeur

**Vendre/Prêter :**
1. Cliquez "➕ Créer une annonce"
2. Type : Vente / Prêt / Échange
3. Décrivez votre objet
4. Fixez le prix

💡 **Catégories** : Meubles, Électronique, Livres, Vêtements, Sport...
✨ **Bonus** : +5 points par annonce publiée !"""
    
    # APL et aides
    elif any(word in message_lower for word in ["apl", "caf", "aide", "allocation"]) and "logement" in message_lower or "apl" in message_lower:
        return f"""📝 **Aides au Logement (APL/CAF)**

**Démarches :**
1. Créez un compte sur **caf.fr**
2. Faites une simulation
3. Déposez votre demande en ligne

**Documents nécessaires** :
✅ Attestation de logement (📄 Mon Compte > Documents)
✅ Copie bail de location
✅ RIB
✅ Pièce d'identité
✅ Avis d'imposition parents (si étudiant)

**Montant moyen APL étudiant** : 100-250€/mois selon ressources

💡 Délai de traitement : 2-3 mois, pensez à anticiper !
📞 CAF {ville} : 3230 (service gratuit)"""
    
    # Assurance
    elif "assurance" in message_lower:
        return f"""🛡️ **Assurance Habitation**

**OBLIGATOIRE pour tous les résidents !**

**Assurances étudiantes recommandées** :
- LMDE : dès 19€/an
- SMENO : dès 22€/an  
- MAE : dès 25€/an
- MAIF : dès 28€/an

**Garanties minimum** :
✅ Responsabilité civile
✅ Dégâts des eaux
✅ Incendie
✅ Vol (optionnel mais conseillé)

📄 Pensez à télécharger votre attestation dans **Mon Compte** pour la transmettre !"""
    
    # Points fidélité
    elif any(word in message_lower for word in ["point", "fidélité", "récompense", "gagner", "bonus", "points", "cadeau", "avantage", "promo", "réduction"]):
        return f"""⭐ **Programme de Fidélité - Vous avez {user['points']} points !**

**Comment gagner des points ?**
• +3 pts : Réserver un espace
• +5 pts : Publier une annonce marketplace
• +5 pts : Évaluer une intervention
• +10 pts : Participer à un événement
• +25 pts : Organiser un événement
• +50 pts : Parrainer un ami

**Récompenses disponibles :**
• 100 pts = 10€ de réduction loyer
• 250 pts = 25€ de réduction
• 500 pts = 50€ de réduction
• 1000 pts = 100€ + cadeau surprise 🎁

➡️ Consultez vos points dans **⚙️ Mon Compte** !"""
    
    # Horaires
    elif any(word in message_lower for word in ["horaire", "ouverture", "fermeture", "quand"]):
        return f"""🕐 **Horaires {residence}**

**Accueil Résidence**
📞 Lun-Ven : 9h-12h30 / 14h-18h
📞 Sam : 9h-12h
📞 Dim : Fermé

**Espaces Communs**
🧺 Laverie : 24h/24, 7j/7
🏋️ Salle de sport : 6h-23h
🍳 Cuisine commune : 8h-22h
☕ Espace co-working : 7h-23h

**Urgences 24/7** : 06 12 34 56 78"""
    
    # Contacts
    elif any(word in message_lower for word in ["contact", "téléphone", "email", "joindre", "appeler"]):
        return f"""📞 **Contacts Utiles**

**Accueil {residence}**
☎️ Standard : 04 78 17 14 11
📧 Email : contact@lesbellesannees.com
🏢 Horaires : Lun-Ven 9h-18h

**Urgences 24/7**
🚨 Téléphone urgence : 06 12 34 56 78
(pannes majeures, sécurité)

**Services Spécialisés**
🔧 Maintenance : maintenance@lesbellesannees.com
📄 Administratif : admin@lesbellesannees.com
💰 Comptabilité : compta@lesbellesannees.com

**Siège Social**
📍 94 quai Charles de Gaulle, 69006 Lyon"""
    
    # Restaurants
    elif any(word in message_lower for word in ["restaurant", "manger", "resto", "nourriture", "food"]):
        if "angers" in ville.lower():
            return f"""🍽️ **Bons plans restos - {ville}**

**Tarifs Étudiants** 🎓
• **Le Petit Gourmet** - Menu 8,50€ (carte étudiante)
• **La Cantine Bio** - Formule 9€ midi
• **Le Comptoir 49** - 10% réduction étudiants

**Fast Food / Budget** 🍕
• **O'Tacos** - 5-8€
• **Subway** - Formule 6,90€
• **Pitaya** - Menu 9,90€

**Livraison** 🛵
• Uber Eats, Deliveroo, Just Eat
• Code promo étudiant souvent dispo !

**CROUS** 🏫
• RU Belle-Beille : 3,30€ le repas !

💡 Appli **TooGoodToGo** pour paniers à -50% !"""
        else:
            return f"""🍽️ **Bons plans restos près de {residence}**

**Budget Étudiant (<10€)**
• Restaurants universitaires CROUS : 3,30€
• Kebabs / Sandwicheries : 5-7€
• Boulangeries (formules midi) : 5-6€

**Livraison**
• Uber Eats, Deliveroo : codes promo -50% nouveaux clients
• Appli **TooGoodToGo** : paniers surprise -50%

**Courses Économiques**
• Lidl, Aldi : budget mini
• Too Good To Go : anti-gaspi
• Marchés locaux : dimanche matin

💡 Cuisinez ensemble dans la cuisine commune = économies + convivialité !"""
    
    # Transports
    elif any(word in message_lower for word in ["transport", "bus", "métro", "tram", "vélo"]):
        if "angers" in ville.lower():
            return f"""🚌 **Transports - {ville}**

**Réseau IRIGO**
🎫 Abonnement -26 ans : 20€/mois (illimité)
🎫 Ticket : 1,60€ (1h)
📱 Appli IRIGO : horaires temps réel

**Lignes Utiles**
• Ligne 1 (Tram) : Centre-ville - Université
• Bus 6, 12 : Desserte résidence

**Vélo** 🚲
• IRIGO Vélo : 25€/an étudiants
• 50+ stations dans la ville

**Covoiturage**
• BlaBlaCar Daily
• Klaxit (trajets quotidiens)
• Groupe Facebook résidents LBA !

**Train** 🚂
• Gare SNCF à 15 min en tram
• Carte Avantage Jeune : -30% toute l'année"""
        else:
            return f"""🚌 **Transports près de {residence}**

**À proximité**
• Arrêts de bus à 2-5 min à pied
• Station métro/tram accessible
• Vélos en libre-service

**Tarifs Étudiants** 💰
• Abonnement mensuel jeunes : ~20-30€
• Carte annuelle : ~200-300€
• Réduction 50% sur justificatif

**Alternatives**
🚲 Vélo : économique et écolo !
🚗 BlaBlaCar : covoiturage longue distance
📱 Applis : Citymapper, Google Maps

💡 Demandez la fiche transports à l'accueil !"""
    
    # WiFi / Internet
    elif any(word in message_lower for word in ["wifi", "internet", "connexion", "réseau"]):
        return f"""📶 **WiFi et Internet**

**Réseau disponible**
• Nom : LBA-{residence.split()[-1].upper()}
• Mot de passe : Demandez à l'accueil

**Problème de connexion ?**
1. Redémarrez votre box
2. Vérifiez que vous êtes bien connecté
3. Si problème persiste : **🔧 Maintenance** > Signaler incident "Internet/WiFi"

**Débit**
• Download : jusqu'à 100 Mbps
• Upload : jusqu'à 50 Mbps

💡 Utilisez un câble Ethernet pour plus de stabilité (gaming, visio)

📱 **Hotspot 4G/5G** en cas d'urgence !"""
    
    # Voisinage / Bruit
    elif any(word in message_lower for word in ["bruit", "voisin", "nuisance", "silence"]):
        return f"""🔇 **Nuisances Sonores / Voisinage**

**Horaires de calme**
🌙 22h-8h : silence obligatoire
📚 Pendant examens : silence renforcé

**En cas de nuisance :**
1. Parlez calmement avec votre voisin (souvent efficace !)
2. Si récidive : contactez l'accueil
3. Signalement incident : **🔧 Maintenance** > "Nuisances sonores"

**Vos droits**
✅ Demander le respect du règlement
✅ Signalement anonyme possible

**Bon voisinage** 🤝
• Prévenez si vous organisez quelque chose
• Respectez les espaces communs
• La résidence = communauté !"""
    
    # Courrier
    elif any(word in message_lower for word in ["courrier", "colis", "boîte aux lettres", "courrier"]):
        return f"""📬 **Courrier et Colis**

**Boîte aux lettres**
• Numéro de boîte = Numéro de logement
• Hall d'entrée du bâtiment

**Colis** 📦
• Accueil vous prévient par SMS/email
• Retrait sur présentation carte d'identité
• Horaires : 9h-12h / 14h-18h

**Adresse à communiquer**
```
{user['prenom']} {user['nom']}
{residence}
Logement {user['logement']}
[Complétez avec l'adresse exacte]
```

💡 Demandez l'adresse complète à l'accueil pour vos envois !"""
    
    # Parking
    elif any(word in message_lower for word in ["parking", "voiture", "stationnement", "garage"]):
        return f"""🚗 **Parking et Stationnement**

**Parking résidence**
• Places réservées résidents
• Badge d'accès à demander à l'accueil
• Gratuit pour les résidents

**Parking visiteurs**
• Places limitées (2h max)
• Zones bleues à proximité

**Alternatives**
🚲 Local vélos sécurisé disponible
🏍️ Stationnement 2-roues dédié

💡 **Covoiturage** : créez un groupe entre résidents !"""
    
    # Ménage / Propreté
    elif any(word in message_lower for word in ["ménage", "propreté", "nettoyage", "sale"]):
        return f"""🧹 **Propreté et Ménage**

**Votre logement**
• Ménage quotidien : à votre charge
• Kit ménage de base fourni à l'arrivée

**Parties Communes**
• Nettoyage quotidien par notre équipe
• Si problème : **🔧 Maintenance** > "Propreté"

**Tri Sélectif** ♻️
• Poubelles tri dans local déchets
• Verre, papier, plastique, tout-venant

**Local Poubelles**
• Accessible 24h/24
• Vide-ordures si immeuble

💡 Participez aux opérations "Résidence propre" : +10 points !"""
    
    # Documents
    elif any(word in message_lower for word in ["document", "attestation", "certificat", "papier"]):
        return f"""📄 **Documents Administratifs**

**Disponibles dans ⚙️ Mon Compte > Documents** :

✅ Attestation de logement
✅ Certificat de résidence  
✅ Quittance de loyer (mensuelle)
✅ Règlement intérieur

**Autres documents** :
📧 Par email sur demande :
• Attestation assurance habitation
• Justificatif de domicile
• Copie du bail

⏱️ Délai : 24-48h maximum

💡 Besoin urgent ? Contactez l'accueil !"""
    
    # Parrainage
    elif any(word in message_lower for word in ["parrain", "filleul", "parrainer", "code"]):
        code_parrainage = f"LBA-{user['id']}-{user['nom'][:3].upper()}"
        return f"""🤝 **Programme de Parrainage**

**Votre code personnel :**
```
{code_parrainage}
```

**Comment ça marche ?**
1. Partagez votre code avec vos amis
2. Ils l'utilisent lors de l'inscription
3. Vous gagnez **50 points** chacun ! 🎉

**Avantages :**
• 50 points = 5€ de réduction immédiate
• Illimité : plus vous parrainez, plus vous gagnez
• Aidez vos amis à trouver leur logement

💡 Partagez dans **👥 Communauté** > **Parrainage** !"""
    
    # Message par défaut avec suggestions
    else:
        return f"""🤖 **Je suis là pour vous aider !**

Voici ce que je peux faire :

**🏠 Vie Pratique**
• Réservations (laverie, salle sport, espaces)
• Horaires et contacts
• Règlement intérieur

**🔧 Incidents**
• Signaler un problème
• Suivi des réparations
• Urgences

**🎉 Communauté**
• Événements à venir
• Marketplace
• Programme de parrainage

**📝 Administratif**
• Aides au logement (APL/CAF)
• Documents et attestations
• Assurance habitation

**🍽️ Bons Plans {ville}**
• Restaurants étudiants
• Transports
• Activités locales

**💡 Exemples de questions :**
- "Comment réserver la laverie ?"
- "Quels sont les horaires ?"
- "Comment faire ma demande APL ?"
- "Des bons restos pas chers ?"
- "Comment signaler un problème ?"

**Que puis-je faire pour vous ?** 😊"""
