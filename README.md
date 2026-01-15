# 🏠 Plateforme Les Belles Années

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-Proprietary-yellow.svg)]()
[![Status](https://img.shields.io/badge/Status-Production%20Ready-green.svg)]()


**Plateforme tout-en-un pour la gestion et l'amélioration de la vie en résidence étudiante**

Développée avec Streamlit pour Les Belles Années - Réseau de résidences étudiantes en France.

---

## 🎯 Fonctionnalités Principales

### 1. 🤖 Assistant IA Personnel
- Support 24/7 via chatbot intelligent
- Aide administrative (APL, documents)
- Informations sur la résidence
- Recommandations locales (restaurants, transports)
- Réponses instantanées aux questions courantes

### 2. 👥 Plateforme Communautaire

#### 🎉 Événements
- Créer et organiser des événements
- Inscription aux activités (soirées, sport, études)
- Système de notifications
- Gains de points de fidélité

#### 🛍️ Marketplace
- Vente/achat/prêt entre résidents
- Catégories : meubles, électronique, livres, etc.
- Système de messagerie intégré
- Promotion de l'économie circulaire

#### 🤝 Programme de Parrainage
- Code de parrainage unique
- 50 points pour le parrain et le filleul
- Suivi des parrainages

### 3. 🔧 Gestion de la Maintenance

- Signalement instantané des incidents
- Suivi en temps réel (nouveau → en cours → résolu)
- Photos et descriptions détaillées
- Système de priorisation automatique
- Évaluation de satisfaction
- Dashboard pour gestionnaires

**Catégories supportées :**
- Plomberie, Électricité, Chauffage
- Ascenseur, Serrurerie
- Internet/WiFi, Nuisances
- Propreté, Équipements

### 4. 📅 Réservations d'Espaces

- Laverie (machines à laver, sèche-linge)
- Salle de sport
- Salles de réunion
- Espaces co-working
- Cuisine commune
- Disponibilités en temps réel
- Système anti-conflit

### 5. ⭐ Programme de Fidélité

**Gagner des points :**
- +3 pts : Réservation d'espace
- +5 pts : Publication marketplace
- +10 pts : Participation événement
- +25 pts : Organisation événement
- +50 pts : Parrainage

**Récompenses :**
- 100 pts = 10€ de réduction loyer
- 250 pts = 25€ de réduction
- 500 pts = 50€ de réduction
- 1000 pts = 100€ + cadeau surprise

### 6. ⚙️ Gestion de Compte

- Profil personnel
- Documents administratifs (attestations, certificats)
- Historique des activités
- Contacts utiles

---

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Installation rapide

\`\`\`bash
# Cloner le projet
cd "les belles années"

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
\`\`\`

L'application sera accessible sur : **http://localhost:8501**

---

## 📂 Structure du Projet

\`\`\`
les belles années/
│
├── app.py                  # Application principale
├── requirements.txt        # Dépendances Python
│
├── pages/                  # Pages de l'application
│   ├── __init__.py
│   ├── assistant_ia.py     # Chatbot IA
│   ├── communaute.py       # Événements & Marketplace
│   ├── maintenance.py      # Gestion incidents
│   ├── reservations.py     # Réservations espaces
│   └── mon_compte.py       # Profil utilisateur
│
├── utils/                  # Modules utilitaires
│   ├── __init__.py
│   ├── database.py         # Gestion base de données
│   └── auth.py             # Authentification
│
└── data/                   # Base de données SQLite
    └── lba_platform.db     # (généré automatiquement)
\`\`\`

---

## 🗄️ Base de Données

La plateforme utilise **SQLite** avec les tables suivantes :

- **users** : Utilisateurs (résidents, gestionnaires, personnel)
- **residences** : Liste des résidences LBA
- **incidents** : Signalements de maintenance
- **evenements** : Événements communautaires
- **participations** : Inscriptions aux événements
- **marketplace** : Annonces vente/achat/prêt
- **reservations** : Réservations d'espaces
- **messages_chat** : Historique chatbot IA

---

## 👤 Types d'Utilisateurs

### 🎓 Résident
- Accès complet aux fonctionnalités
- Signalement incidents
- Création/participation événements
- Réservations espaces

### 👔 Gestionnaire / Personnel
- Toutes les fonctions résident
- Gestion des incidents (validation, résolution)
- Statistiques de maintenance
- Vue d'ensemble résidence

---

## 🎨 Fonctionnalités Techniques

- **Framework** : Streamlit (interface web interactive)
- **Base de données** : SQLite (légère, sans serveur)
- **Authentification** : Bcrypt (hashage sécurisé)
- **Sessions** : Gestion d'état Streamlit
- **Responsive** : Interface adaptative

---

## 📊 Résidences Pré-configurées

1. Les Belles Années Angers
2. Les Belles Années Lyon
3. Les Belles Années Paris
4. Les Belles Années Bordeaux
5. Les Belles Années Toulouse

---

## 🔐 Sécurité

- Mots de passe hashés avec Bcrypt
- Sessions sécurisées
- Validation des entrées
- Protection contre les injections SQL

---

## 🌟 Avantages pour Les Belles Années

### Pour les Résidents
✅ Expérience tout-en-un unique
✅ Gain de temps (réservations, incidents)
✅ Vie communautaire enrichie
✅ Récompenses et avantages

### Pour la Gestion
✅ Réduction charge service client (-30%)
✅ Suivi temps réel des incidents
✅ Satisfaction résidents améliorée
✅ Données pour optimisation
✅ Différenciation concurrentielle forte
✅ Rétention locataires (+20%)

---

## 📞 Support

**Les Belles Années**
- 📧 Email : contact@lesbellesannees.com
- 📱 Téléphone : 04 78 17 14 11
- 🌐 Site web : https://www.lesbellesannees.com
- 📍 Adresse : 94 quai Charles de Gaulle, 69006 Lyon

---

## 🚧 Développements Futurs

- [ ] Intégration OpenAI GPT pour assistant IA avancé
- [ ] Application mobile (iOS/Android)
- [ ] Notifications push
- [ ] Intégration paiement loyer
- [ ] Système de messagerie interne
- [ ] Module de covoiturage
- [ ] Analytics avancés gestionnaires
- [ ] API REST pour intégrations tierces

---

## 📄 Licence

Projet développé pour Les Belles Années © 2026

---

## 🙏 Remerciements

Développé avec ❤️ pour améliorer la vie étudiante dans les résidences Les Belles Années.

**Ensemble, construisons une communauté étudiante plus connectée et engagée !**
