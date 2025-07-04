import random
import numpy as np

def ia(chiffre, cases_perso, cases_adversaire):
    # Calculer le tour actuel
    tour = 3 - cases_perso.count(None)
    
    # Statistiques des tirages précédents
    tirages = [x for x in cases_perso + cases_adversaire if x is not None]
    moyenne_tirages = np.mean(tirages) if tirages else 4.5
    ecart_type = np.std(tirages) if len(tirages) > 1 else 3.0
    
    # Évaluer l'état du jeu
    positions_libres = [i for i, v in enumerate(cases_perso) if v is None]
    
    # Stratégie différente selon le tour
    if tour == 0:  # Premier tour
        # Si le chiffre est très élevé, le placer en position de centaines
        if chiffre >= 8:
            return 1
        # Si le chiffre est très bas, le placer en position d'unités
        elif chiffre <= 2:
            return 3
        # Sinon, milieu
        else:
            return 2
    
    elif tour == 1:  # Deuxième tour
        # Analyse du plateau adverse
        adversaire_gauche = cases_adversaire[0]
        
        # Si l'adversaire a un chiffre élevé à gauche
        if adversaire_gauche is not None and adversaire_gauche >= 7:
            # Si on a un chiffre supérieur, essayer de le battre
            if chiffre > adversaire_gauche and 0 in positions_libres:
                return 1
            # Sinon, se concentrer sur d'autres positions
            elif 1 in positions_libres:
                return 2
            else:
                return 3
        
        # Si notre position de centaines est vide et qu'on a un bon chiffre
        if cases_perso[0] is None and chiffre >= 6:
            return 1
        
        # Si le chiffre est très bas, le mettre en unités
        if chiffre <= 3 and 2 in positions_libres:
            return 3
        
        # Stratégie par défaut: placer dans la position la plus avantageuse
        return meilleure_position(chiffre, cases_perso, cases_adversaire, moyenne_tirages)
    
    else:  # Dernier tour
        # Calculer le score potentiel pour chaque position libre
        scores_potentiels = []
        for pos in positions_libres:
            temp_cases = cases_perso.copy()
            temp_cases[pos] = chiffre
            score = determiner_score(temp_cases)
            scores_potentiels.append((pos, score))
        
        # Choisir la position qui maximise notre score
        meilleur_pos = max(scores_potentiels, key=lambda x: x[1])[0]
        return meilleur_pos + 1

def determiner_score(etat):
    """Calcule le score numérique à partir des cases"""
    return int("".join(str(x) for x in etat))

def meilleure_position(chiffre, cases_perso, cases_adversaire, moyenne_tirages):
    """Détermine la meilleure position en fonction des probabilités futures"""
    positions_libres = [i for i, v in enumerate(cases_perso) if v is None]
    valeurs_positions = []
    
    # Poids des positions (centaines, dizaines, unités)
    poids = [100, 10, 1]
    
    for pos in positions_libres:
        # Valeur immédiate
        valeur_immediate = chiffre * poids[pos]
        
        # Valeur potentielle future
        cases_futures = cases_perso.copy()
        cases_futures[pos] = chiffre
        
        # Estimer la valeur des futures positions
        valeur_potentielle = 0
        positions_restantes = [i for i in range(3) if cases_futures[i] is None]
        for i, p in enumerate(positions_restantes):
            # Estimation basée sur la moyenne des tirages
            valeur_potentielle += moyenne_tirages * poids[p] * (0.8 ** i)
        
        # Pénalité si l'adversaire domine cette position
        if cases_adversaire[pos] is not None and chiffre < cases_adversaire[pos]:
            valeur_immediate *= 0.7  # Réduction de 30%
        
        # Score total pour cette position
        score_total = valeur_immediate + valeur_potentielle
        valeurs_positions.append((pos, score_total))
    
    # Choisir la position avec le score total le plus élevé
    meilleur_pos = max(valeurs_positions, key=lambda x: x[1])[0]
    return meilleur_pos + 1