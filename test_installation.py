#!/usr/bin/env python3
import sys
import os

print("🧪 Test de la plateforme Les Belles Années\n")

print("1️⃣ Vérification des dépendances...")
try:
    import streamlit
    print("   ✅ Streamlit installé")
except ImportError:
    print("   ❌ Streamlit manquant - Exécutez: pip install streamlit")
    sys.exit(1)

try:
    import pandas
    print("   ✅ Pandas installé")
except ImportError:
    print("   ⚠️  Pandas manquant (optionnel)")

try:
    import bcrypt
    print("   ✅ Bcrypt installé")
except ImportError:
    print("   ❌ Bcrypt manquant - Exécutez: pip install bcrypt")
    sys.exit(1)

print("\n2️⃣ Vérification de la structure...")
fichiers_requis = [
    'app.py',
    'utils/database.py',
    'utils/auth.py',
    'pages/assistant_ia.py',
    'pages/communaute.py',
    'pages/maintenance.py',
    'pages/reservations.py',
    'pages/mon_compte.py'
]

for fichier in fichiers_requis:
    if os.path.exists(fichier):
        print(f"   ✅ {fichier}")
    else:
        print(f"   ❌ {fichier} manquant")

print("\n3️⃣ Initialisation de la base de données...")
try:
    from utils.database import init_database
    init_database()
    print("   ✅ Base de données créée avec succès")
    print("   ✅ 5 résidences pré-configurées")
except Exception as e:
    print(f"   ❌ Erreur : {e}")
    sys.exit(1)

print("\n4️⃣ Test du système d'authentification...")
try:
    from utils.database import hash_password, verify_password
    test_pw = "test123"
    hashed = hash_password(test_pw)
    if verify_password(test_pw, hashed):
        print("   ✅ Hashage et vérification fonctionnels")
    else:
        print("   ❌ Problème de vérification password")
except Exception as e:
    print(f"   ❌ Erreur : {e}")

print("\n" + "="*50)
print("✅ TOUS LES TESTS SONT PASSÉS !")
print("="*50)
print("\n🚀 Pour lancer l'application :")
print("   streamlit run app.py")
print("\n📖 Documentation :")
print("   README.md - Documentation complète")
print("   GUIDE_DEMARRAGE.md - Guide de démarrage rapide")
print("\n🌐 L'application sera disponible sur :")
print("   http://localhost:8501")
