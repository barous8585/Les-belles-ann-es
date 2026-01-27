import sqlite3
import bcrypt
from datetime import datetime
import os
import streamlit as st

DB_PATH = "data/lba_platform.db"

def init_database():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            type_utilisateur TEXT NOT NULL,
            residence TEXT,
            numero_logement TEXT,
            telephone TEXT,
            date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            points_fidelite INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS residences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            ville TEXT NOT NULL,
            adresse TEXT NOT NULL,
            capacite INTEGER,
            gestionnaire_id INTEGER,
            FOREIGN KEY (gestionnaire_id) REFERENCES users(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            description TEXT NOT NULL,
            categorie TEXT NOT NULL,
            priorite TEXT NOT NULL,
            statut TEXT DEFAULT 'nouveau',
            residence TEXT NOT NULL,
            logement TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            photo_path TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_resolution TIMESTAMP,
            note_satisfaction INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evenements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            description TEXT NOT NULL,
            categorie TEXT NOT NULL,
            date_evenement TIMESTAMP NOT NULL,
            lieu TEXT NOT NULL,
            residence TEXT NOT NULL,
            organisateur_id INTEGER NOT NULL,
            nombre_max_participants INTEGER,
            statut TEXT DEFAULT 'ouvert',
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (organisateur_id) REFERENCES users(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS participations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evenement_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (evenement_id) REFERENCES evenements(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(evenement_id, user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS marketplace (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            description TEXT NOT NULL,
            type_annonce TEXT NOT NULL,
            prix REAL,
            categorie TEXT NOT NULL,
            statut TEXT DEFAULT 'disponible',
            vendeur_id INTEGER NOT NULL,
            residence TEXT NOT NULL,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vendeur_id) REFERENCES users(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_espace TEXT NOT NULL,
            espace TEXT NOT NULL,
            residence TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            date_debut TIMESTAMP NOT NULL,
            date_fin TIMESTAMP NOT NULL,
            statut TEXT DEFAULT 'confirmee',
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages_chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            reponse TEXT,
            date_message TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            ip_address TEXT,
            attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            success INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    
    try:
        cursor.execute("ALTER TABLE incidents ADD COLUMN photo_path TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    
    cursor.execute("SELECT COUNT(*) FROM residences")
    if cursor.fetchone()[0] == 0:
        residences_initiales = [
            ("Les Belles Années Angers", "Angers", "12 Rue de la Paix, 49000 Angers", 150),
            ("Les Belles Années Lyon", "Lyon", "94 Quai Charles de Gaulle, 69006 Lyon", 200),
            ("Les Belles Années Paris", "Paris", "25 Avenue des Champs, 75008 Paris", 180),
            ("Les Belles Années Bordeaux", "Bordeaux", "45 Rue Sainte-Catherine, 33000 Bordeaux", 120),
            ("Les Belles Années Toulouse", "Toulouse", "18 Place du Capitole, 31000 Toulouse", 140),
        ]
        cursor.executemany("INSERT INTO residences (nom, ville, adresse, capacite) VALUES (?, ?, ?, ?)", residences_initiales)
        conn.commit()
    
    conn.close()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def get_connection():
    return sqlite3.connect(DB_PATH)

@st.cache_data(ttl=300)
def get_residences_list():
    """Cache la liste des résidences (TTL: 5 minutes)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nom FROM residences")
    residences = [r[0] for r in cursor.fetchall()]
    conn.close()
    return residences

@st.cache_data(ttl=60)
def get_user_stats(user_id):
    """Cache les statistiques utilisateur (TTL: 1 minute)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM incidents WHERE user_id = ? AND statut != 'résolu'", (user_id,))
    incidents_actifs = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM reservations WHERE user_id = ?", (user_id,))
    reservations_actives = cursor.fetchone()[0]
    
    cursor.execute("SELECT points_fidelite FROM users WHERE id = ?", (user_id,))
    points = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'incidents_actifs': incidents_actifs,
        'reservations_actives': reservations_actives,
        'points': points
    }
