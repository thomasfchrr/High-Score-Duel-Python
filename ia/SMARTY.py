def choisir_case(chiffre, placement_ia, placement_adv):
    # Stratégie basique : chiffre élevé -> placer à gauche
    if chiffre >= 7 and placement_ia[0] is None:
        return 1
    elif chiffre >= 4 and placement_ia[1] is None:
        return 2
    elif placement_ia[2] is None:
        return 3

    # Adaptation : essayer de battre l'adversaire à une position
    for i in range(3):
        if placement_ia[i] is None and placement_adv[i] is not None:
            if chiffre > placement_adv[i]:
                return i + 1

    # Remplir la première case vide disponible
    for i in range(3):
        if placement_ia[i] is None:
            return i + 1

    # Sécurité
    return 1

ia = choisir_case