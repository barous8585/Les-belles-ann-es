# 🧪 GUIDE DE TEST RAPIDE - LES BELLES ANNÉES

## ⚡ Test Local (5 minutes)

### 1. Lancer l'application
```bash
streamlit run app.py
```

### 2. Tests à effectuer

#### ✅ Test 1: Inscription avec validation mot de passe
1. Aller sur l'onglet "✨ Inscription"
2. Essayer un mot de passe faible: `test123` → ❌ Doit refuser
3. Essayer un mot de passe fort: `Test1234` → ✅ Doit accepter
4. Essayer email invalide: `test@test` → ❌ Doit refuser
5. Essayer email valide: `test@test.com` → ✅ Doit accepter

#### ✅ Test 2: Protection brute-force
1. Aller sur "🔐 Connexion"
2. Essayer 5 fois avec mauvais mot de passe
3. 6ème tentative → ❌ Message "Trop de tentatives, attendez 15 min"

#### ✅ Test 3: Upload photo incident
1. Se connecter avec: `demo.resident@lba.com` / `demo123`
2. Menu "🔧 Maintenance" > "📝 Signaler un incident"
3. Remplir le formulaire
4. **Ajouter une photo** (JPG/PNG)
5. Envoyer
6. Aller sur "📊 Mes incidents"
7. Vérifier que la **photo s'affiche** en miniature

#### ✅ Test 4: Marketplace - Contacter
1. Menu "👥 Communauté" > "🛍️ Marketplace"
2. Tester les **filtres** (Type + Catégorie)
3. Cliquer sur une annonce
4. Cliquer "📧 Voir les coordonnées"
5. Vérifier que **email et téléphone** s'affichent

#### ✅ Test 5: Dashboard gestionnaire
1. Se connecter avec: `demo.gestionnaire@lba.com` / `demo123`
2. Menu "🔧 Maintenance" > "📈 Statistiques"
3. Vérifier que **3 graphiques** s'affichent:
   - Barre (catégories)
   - Camembert (statuts)
   - Barre (priorités)

#### ✅ Test 6: Assistant IA amélioré
1. Menu "🤖 Assistant IA"
2. Tester avec synonymes:
   - "je veux réserver la gym" → ✅ Réponse salle de sport
   - "help problème fuite" → ✅ Réponse signalement
   - "cherche vélo occasion" → ✅ Réponse marketplace

---

## 📊 Résultats attendus

| Test | Attendu | Statut |
|------|---------|--------|
| Mot de passe faible | Refusé | ⬜ |
| Mot de passe fort | Accepté | ⬜ |
| Brute-force (6ème) | Bloqué | ⬜ |
| Upload photo | Visible historique | ⬜ |
| Contacter marketplace | Email/tél affiché | ⬜ |
| Filtres marketplace | Fonctionnent | ⬜ |
| Dashboard graphiques | 3 graphiques | ⬜ |
| Assistant IA synonymes | Bonnes réponses | ⬜ |

---

## 🚀 Déploiement Streamlit Cloud

### Étapes
1. Pusher sur GitHub:
```bash
git push origin main
```

2. Aller sur https://share.streamlit.io/
3. Redéployer l'app (detecte automatiquement les changements)
4. Attendre 2-3 minutes
5. Tester la version déployée

### ⚠️ IMPORTANT
**Photos sur Streamlit Cloud**: Les uploads fonctionnent mais sont **temporaires** (perdus au redémarrage).

**Solution pour production**:
- Migrer vers AWS S3, Cloudinary, ou Google Cloud Storage
- Coût: ~5€/mois pour 10GB

---

## 🐛 En cas de problème

### Erreur: "table login_attempts doesn't exist"
```bash
# Supprimer la DB et relancer
rm data/lba_platform.db
streamlit run app.py
```

### Erreur: "Module plotly not found"
```bash
pip install plotly
```

### Photos ne s'affichent pas
```bash
mkdir -p data/uploads/incidents
chmod 755 data/uploads/incidents
```

---

## ✅ Checklist déploiement production

- [ ] Tous les tests passent ✅
- [ ] App fonctionne en local
- [ ] Pusher sur GitHub
- [ ] Déployer sur Streamlit Cloud
- [ ] **Rendre l'app PUBLIQUE** (Settings > Sharing > Public)
- [ ] Tester en navigation privée
- [ ] Envoyer email à Les Belles Années

---

**Bon test ! 🎉**
