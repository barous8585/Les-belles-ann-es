# 🚀 Guide de Déploiement

## Déploiement sur Streamlit Cloud (GRATUIT)

### Étape 1 : Prérequis
- Compte GitHub (✅ déjà fait)
- Repository public (✅ déjà fait)

### Étape 2 : Déployer sur Streamlit Cloud

1. Allez sur https://share.streamlit.io/
2. Connectez-vous avec votre compte GitHub
3. Cliquez "New app"
4. Sélectionnez :
   - Repository: `barous8585/Les-belles-ann-es`
   - Branch: `main`
   - Main file path: `app.py`
5. Cliquez "Deploy"

### Étape 3 : Configuration

Aucune configuration supplémentaire nécessaire !
La base de données SQLite sera créée automatiquement.

### URL de l'application

Après déploiement, votre app sera accessible sur :
`https://barous8585-les-belles-ann-es.streamlit.app`

---

## Déploiement Local

```bash
# Cloner le repository
git clone https://github.com/barous8585/Les-belles-ann-es.git
cd Les-belles-ann-es

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

---

## Variables d'Environnement (Optionnel)

Si vous souhaitez utiliser OpenAI pour l'assistant IA :

1. Créer `.streamlit/secrets.toml`
2. Ajouter :
```toml
OPENAI_API_KEY = "votre_clé_ici"
```

---

## Support

Pour toute question : contact@lesbellesannees.com
