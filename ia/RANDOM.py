import random

def ia(chiffre, cases_perso, cases_adversaire):
    libres = [i+1 for i, v in enumerate(cases_perso) if v is None]  # Retourne 1-3
    return random.choice(libres) if libres else 1  # Sécurité si aucune case libre