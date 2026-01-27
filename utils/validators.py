import re

def validate_password(password):
    """
    Valide la force d'un mot de passe.
    Règles :
    - Minimum 8 caractères
    - Au moins 1 majuscule
    - Au moins 1 minuscule
    - Au moins 1 chiffre
    """
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    
    if not re.search(r'[A-Z]', password):
        return False, "Le mot de passe doit contenir au moins une majuscule"
    
    if not re.search(r'[a-z]', password):
        return False, "Le mot de passe doit contenir au moins une minuscule"
    
    if not re.search(r'\d', password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    
    return True, "Mot de passe valide"

def validate_email(email):
    """
    Valide le format d'une adresse email.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, "Email valide"
    return False, "Format d'email invalide"

def validate_telephone(telephone):
    """
    Valide le format d'un numéro de téléphone français.
    Accepte : 0612345678, 06 12 34 56 78, 06-12-34-56-78, +33612345678
    """
    if not telephone:
        return True, "Téléphone optionnel"
    
    telephone_clean = re.sub(r'[\s\-\.]', '', telephone)
    
    pattern_fr = r'^(0[1-9]|(\+33)[1-9])[0-9]{8}$'
    if re.match(pattern_fr, telephone_clean):
        return True, "Téléphone valide"
    
    return False, "Format de téléphone invalide (ex: 06 12 34 56 78)"

def validate_numero_logement(numero):
    """
    Valide le format d'un numéro de logement.
    Accepte : A101, 205, B-12, etc.
    """
    if not numero:
        return False, "Le numéro de logement est obligatoire"
    
    if len(numero) < 1 or len(numero) > 10:
        return False, "Le numéro de logement doit faire entre 1 et 10 caractères"
    
    pattern = r'^[A-Za-z0-9\-]+$'
    if re.match(pattern, numero):
        return True, "Numéro de logement valide"
    
    return False, "Le numéro de logement ne peut contenir que des lettres, chiffres et tirets"
