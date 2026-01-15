import streamlit as st
from utils.database import get_connection, hash_password, verify_password

def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and verify_password(password, user[2]):
        return {
            "id": user[0],
            "email": user[1],
            "nom": user[3],
            "prenom": user[4],
            "type": user[5],
            "residence": user[6],
            "logement": user[7],
            "telephone": user[8],
            "points": user[10]
        }
    return None

def register_user(email, password, nom, prenom, type_utilisateur, residence, numero_logement, telephone):
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
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def is_authenticated():
    return "user" in st.session_state and st.session_state.user is not None

def get_current_user():
    return st.session_state.get("user", None)

def logout():
    if "user" in st.session_state:
        del st.session_state.user
    st.rerun()
