import streamlit as st
from utils.database import get_connection, hash_password, verify_password
from utils.validators import validate_password, validate_email, validate_telephone, validate_numero_logement
from datetime import datetime, timedelta
import sqlite3

def check_login_attempts(email):
    """
    Vérifie le nombre de tentatives de connexion échouées.
    Retourne True si l'utilisateur peut essayer, False si bloqué.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    time_limit = datetime.now() - timedelta(minutes=15)
    
    cursor.execute("""
        SELECT COUNT(*) FROM login_attempts 
        WHERE email = ? AND success = 0 AND attempt_time > ?
    """, (email, time_limit))
    
    failed_attempts = cursor.fetchone()[0]
    conn.close()
    
    return failed_attempts < 5

def record_login_attempt(email, success):
    """
    Enregistre une tentative de connexion.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO login_attempts (email, success) VALUES (?, ?)
    """, (email, 1 if success else 0))
    conn.commit()
    conn.close()

def login_user(email, password):
    if not check_login_attempts(email):
        return None, "Trop de tentatives échouées. Veuillez réessayer dans 15 minutes."
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, password, nom, prenom, type_utilisateur, residence, numero_logement, telephone, points_fidelite FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and verify_password(password, user[2]):
        record_login_attempt(email, True)
        return {
            "id": user[0],
            "email": user[1],
            "nom": user[3],
            "prenom": user[4],
            "type": user[5],
            "residence": user[6],
            "logement": user[7],
            "telephone": user[8],
            "points": user[9]
        }, None
    
    record_login_attempt(email, False)
    return None, "Email ou mot de passe incorrect"

def register_user(email, password, nom, prenom, type_utilisateur, residence, numero_logement, telephone):
    is_valid_email, email_msg = validate_email(email)
    if not is_valid_email:
        return False, email_msg
    
    is_valid_password, password_msg = validate_password(password)
    if not is_valid_password:
        return False, password_msg
    
    is_valid_tel, tel_msg = validate_telephone(telephone)
    if not is_valid_tel:
        return False, tel_msg
    
    is_valid_logement, logement_msg = validate_numero_logement(numero_logement)
    if not is_valid_logement:
        return False, logement_msg
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        hashed_pw = hash_password(password)
        cursor.execute('''
            INSERT INTO users (email, password, nom, prenom, type_utilisateur, residence, numero_logement, telephone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (email, hashed_pw, nom, prenom, type_utilisateur, residence, numero_logement, telephone))
        conn.commit()
        conn.close()
        return True, "Compte créé avec succès !"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Cet email est déjà utilisé"

def is_authenticated():
    return "user" in st.session_state and st.session_state.user is not None

def get_current_user():
    return st.session_state.get("user", None)

def logout():
    if "user" in st.session_state:
        del st.session_state.user
    st.rerun()
