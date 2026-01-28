# 🌱 Guide d'Utilisation - Script de Peuplement Démo

## 📋 Vue d'ensemble

Le script `seed_demo_data.py` crée un **environnement de démo complet et réaliste** pour votre présentation de l'application Les Belles Années.

### ✨ Ce qui sera créé :

#### 👥 Utilisateurs (20 au total)
- **15 résidents** actifs avec profils variés
  - Marie Dupont (45 pts), Lucas Martin (120 pts), Emma Bernard (85 pts)...
  - Logements répartis : A101 à H103
  - Téléphones et emails réalistes
  
- **2 gestionnaires**
  - Sophie Rousseau (gestionnaire principal)
  - Pierre Blanc (admin Angers)
  
- **3 membres du personnel**
  - Marc Leroux, Julie Bonnet, David Fournier

#### 🔧 Incidents (20)
Variété réaliste :
- **Critique** : Ascenseur bloqué, Chauffage HS
- **Haute** : Fuites d'eau, Machine à laver en panne, Four défectueux
- **Moyenne** : WiFi instable, Robinets qui fuient, Fenêtres
- **Faible** : Ampoules grillées, Portes qui grincent

Statuts variés :
- Nouveaux (récents)
- En cours (en traitement)
- Résolus (avec notes de satisfaction 3-5/5)

#### 🎉 Événements (15)
Mix passés et futurs :
- **Sport** : Tournoi FIFA, Yoga, Salsa, Match de foot
- **Culture** : Atelier cuisine, Film, Photographie, Zéro déchet
- **Loisirs** : Soirée jeux, Karaoké, Blind test, Tacos party
- **Networking** : Afterwork, Brunch communautaire

Participants variables : 30-70% des places remplies

#### 🛍️ Marketplace (30 annonces)
Annonces réalistes :
- **Vente** : Canapé IKEA 80€, MacBook Pro 850€, Vélo 120€
- **Prêt** : Perceuse Bosch, Tapis yoga, Tente Quechua
- **Achat** : Cours particuliers maths 20€/h

Catégories : Meubles, Électronique, Livres, Vêtements, Sport, Autre

#### 📅 Réservations (40)
Sur 30 jours (passées et futures) :
- **Laverie** : 4 machines disponibles
- **Salle de sport** : 3 zones
- **Espaces communs** : Cuisine, Co-working, Terrasse, Salle réunion

Créneaux variés : 8h-20h, durées 30min-4h

---

## 🚀 Utilisation

### Étape 1 : Exécuter le script

```bash
# Dans le dossier de l'application
python seed_demo_data.py
```

### Étape 2 : Confirmer

Le script demande confirmation avant de supprimer les données existantes :

```
⚠️  ATTENTION: Cette opération va SUPPRIMER toutes les données existantes !
Continuer ? (oui/non): 
```

Tapez `oui` et appuyez sur Entrée.

### Étape 3 : Attendre la création

Le script va :
1. ✅ Vider les tables existantes
2. 👥 Créer 20 utilisateurs
3. 🔧 Créer 20 incidents
4. 🎉 Créer 15 événements avec participants
5. 🛍️ Créer 30 annonces marketplace
6. 📅 Créer 40 réservations

**Durée : 5-10 secondes**

### Étape 4 : Affichage du résumé

```
========================================================
📊 RÉSUMÉ DES DONNÉES CRÉÉES
========================================================
👤 Résidents: 15
👤 Gestionnaires: 2
👤 Personnels: 3

🔧 Incidents:
  • nouveau: 7
  • en_cours: 5
  • résolu: 8

🎉 Événements:
  • ouvert: 8
  • termine: 7

🛍️ Annonces marketplace: 30

📅 Réservations:
  • À venir: 20
  • Passées: 20

🎯 Participations événements: 87
========================================================
```

---

## 🔑 Comptes de Connexion

**TOUS les comptes utilisent le même mot de passe : `Password1`**

### 👥 Résidents (15 comptes)

```
marie.dupont@gmail.com      → Marie Dupont (A101) - 45 pts
lucas.martin@gmail.com      → Lucas Martin (A205) - 120 pts
emma.bernard@gmail.com      → Emma Bernard (B103) - 85 pts
hugo.petit@gmail.com        → Hugo Petit (B207) - 60 pts
lea.dubois@gmail.com        → Léa Dubois (C102) - 150 pts
nathan.moreau@gmail.com     → Nathan Moreau (C208) - 95 pts
chloe.laurent@gmail.com     → Chloé Laurent (D104) - 75 pts
tom.simon@gmail.com         → Tom Simon (D201) - 40 pts
lisa.michel@gmail.com       → Lisa Michel (E105) - 110 pts
theo.lefevre@gmail.com      → Théo Lefèvre (E203) - 55 pts
sarah.garcia@gmail.com      → Sarah Garcia (F101) - 135 pts
alex.roux@gmail.com         → Alex Roux (F206) - 80 pts
jade.fontaine@gmail.com     → Jade Fontaine (G102) - 65 pts
louis.chevalier@gmail.com   → Louis Chevalier (G204) - 100 pts
camille.girard@gmail.com    → Camille Girard (H103) - 90 pts
```

### 👔 Gestionnaires (2 comptes)

```
gestionnaire@test.com                    → Sophie Rousseau
admin.angers@lesbellesannees.com        → Pierre Blanc
```

### 🔧 Personnel (3 comptes)

```
personnel@test.com                       → Marc Leroux
technicien@lesbellesannees.com          → Julie Bonnet
maintenance@lesbellesannees.com         → David Fournier
```

---

## 🎬 Scénarios de Démo Suggérés

### Scénario 1 : Vue Résident (5 min)

**Connexion : `marie.dupont@gmail.com` / `Password1`**

1. **Dashboard** → Voir métriques (incidents, événements, marketplace, réservations)
2. **Communauté** → 
   - Marketplace : Parcourir les 30 annonces (MacBook, Vélo, Canapé...)
   - Événements : S'inscrire au Tournoi FIFA ou Soirée Karaoké
3. **Maintenance** → Voir ses incidents, en signaler un nouveau avec photo
4. **Réservations** → Réserver la laverie pour demain 14h
5. **Mon Compte** → Voir progression fidélité (45 pts → proche de 100)

### Scénario 2 : Vue Gestionnaire (5 min)

**Connexion : `gestionnaire@test.com` / `Password1`**

1. **Dashboard** → 
   - KPIs : Incidents nouveaux (7), En cours (5), 15 résidents
   - Activité semaine : Graphiques incidents et participations
2. **Maintenance** → 
   - Voir tous les incidents de la résidence
   - Passer un incident "nouveau" → "en_cours"
   - Résoudre un incident "Ampoule grillée"
3. **Planning Global** → 
   - Voir toutes les réservations du jour
   - Bloquer un créneau laverie pour maintenance
4. **Modération** → 
   - Marketplace : Valider/supprimer annonces
   - Événements : Top contributeurs (Léa Dubois 150 pts)
5. **Analytics** → Graphiques Plotly détaillés

### Scénario 3 : Vue Personnel (3 min)

**Connexion : `personnel@test.com` / `Password1`**

1. **Dashboard** → 
   - Voir tâches prioritaires : 2 Critiques, 4 Urgents
   - Animation pulse sur badge "Critique"
2. **Interventions** → 
   - Liste filtrée par priorité
   - Traiter "Ascenseur bloqué" (Critique)
   - Passer en "résolu"

### Scénario 4 : Communauté Active (3 min)

**Connexion : `lucas.martin@gmail.com` / `Password1` (120 pts)**

1. **Communauté** → 
   - Créer un événement "Soirée Raclette" (25 pts bonus)
   - Publier annonce "MacBook Air M2" à vendre (5 pts bonus)
   - Participer au "Brunch Communautaire" (10 pts bonus)
2. **Mon Compte** → 
   - Voir points passer de 120 → 160 pts
   - Déverrouiller récompense 100 pts (10€ réduction)

---

## 📊 Statistiques Intéressantes à Montrer

### Dashboard Gestionnaire :
- **Taux de résolution incidents** : 8/20 = 40%
- **Satisfaction moyenne** : 4.2/5
- **Taux de participation événements** : 87 inscriptions / 15 événements
- **Activité marketplace** : 30 annonces actives

### Engagement Communautaire :
- **Top résident** : Léa Dubois (150 pts) - Super active !
- **Événements les + populaires** : Brunch (25 participants), Karaoké (18)
- **Catégorie marketplace populaire** : Électronique (8 annonces)

### Réservations :
- **Espace le + réservé** : Laverie (15 réservations)
- **Créneau populaire** : 18h-20h
- **Taux d'occupation moyen** : 65%

---

## 🔄 Réinitialiser les Données

Pour repartir de zéro et recréer des données fraîches :

```bash
python seed_demo_data.py
```

Le script supprime automatiquement les anciennes données avant de créer les nouvelles.

---

## 💡 Conseils pour la Présentation

### Avant la démo :
1. ✅ Exécuter `seed_demo_data.py`
2. ✅ Lancer l'app : `streamlit run app.py`
3. ✅ Tester les 3 types de comptes rapidement
4. ✅ Préparer 2-3 fenêtres avec comptes différents

### Pendant la démo :
1. **Commencer par Résident** → Montrer l'UX user-friendly
2. **Passer à Gestionnaire** → Impressionner avec les KPIs
3. **Finir par Personnel** → Montrer l'efficacité opérationnelle
4. **Basculer Dark/Light** → Montrer que tout reste visible

### Points à mettre en avant :
- ✨ Design moderne et élégant
- 🎯 3 interfaces adaptées par rôle
- 📊 Analytics temps réel
- 🤝 Communauté active et engagée
- ⭐ Programme fidélité gamifié
- 📱 Responsive (tester sur mobile si possible)

---

## 🐛 Dépannage

### Erreur : "No module named 'utils.database'"

```bash
# Vérifier que vous êtes dans le bon dossier
pwd
# Devrait afficher : /Users/.../les belles années

# Installer les dépendances si nécessaire
pip install -r requirements.txt
```

### Erreur : "database is locked"

```bash
# Fermer l'application Streamlit d'abord
# Puis relancer le script
python seed_demo_data.py
```

### Base de données corrompue

```bash
# Supprimer la BDD et relancer
rm data/lba_platform.db
python seed_demo_data.py
```

---

## 📈 Données Avancées (Optionnel)

Si vous voulez encore plus de données pour impressionner :

### Option 1 : Doubler les résidents

Dans `seed_demo_data.py`, dupliquer la liste `RESIDENTS` :

```python
RESIDENTS = RESIDENTS * 2  # 30 résidents au lieu de 15
```

### Option 2 : Plus d'incidents

```python
INCIDENTS_TEMPLATES = INCIDENTS_TEMPLATES * 2  # 40 incidents
```

### Option 3 : Historique plus long

Dans les fonctions de création, changer :
```python
jours_avant = random.randint(0, 60)  # Au lieu de 30
```

---

## 🎉 Résultat Final

Avec ce script, vous aurez :

✅ **Une résidence vivante** avec 20 utilisateurs actifs
✅ **Activité réaliste** sur les 30 derniers jours
✅ **Tous les modules utilisés** (incidents, événements, marketplace, réservations)
✅ **Données cohérentes** (dates, statuts, participants)
✅ **Comptes de test prêts** pour la démo

**Parfait pour impressionner Les Belles Années lors de votre présentation ! 🚀**

---

## 📞 Support

En cas de problème avec le script, vérifier :
1. Python 3.11 installé
2. Toutes les dépendances installées (`pip install -r requirements.txt`)
3. Dossier `data/` existe
4. Permissions d'écriture sur `data/lba_platform.db`

**Prêt pour une démo qui impressionne ! 🏠✨**
