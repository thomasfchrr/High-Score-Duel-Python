def ia(chiffre, cases_perso, cases_adversaire):
    # Essaie de placer le plus grand chiffre en tête
    libres = [i+1 for i, v in enumerate(cases_perso) if v is None]  # 1-3
    
    if not libres:
        return 1  # Sécurité
    
    if chiffre >= 7 and 1 in libres:
        return 1
    elif chiffre <= 3 and 3 in libres:
        return 3
    elif 2 in libres:
        return 2
    return libres[0]