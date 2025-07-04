import random

def afficher_etats(etat_j1, etat_j2):
    def formater(etat):
        return "[" + ", ".join(str(x) if x is not None else " " for x in etat) + "]"

    print(f"Joueur 1 : {formater(etat_j1)}")
    print(f"Joueur 2 : {formater(etat_j2)}")

def placer_nombre_interface(joueur, etat_j1, etat_j2, nb):
    while True:
        print(f"\nTour {sum(x is not None for x in etat_j1 + etat_j2) + 1} - Nombre tiré pour Joueur {joueur} : {nb}")
        print("État du jeu :")
        afficher_etats(etat_j1, etat_j2)

        try:
            case = int(input(f"Joueur {joueur}, choisissez une case (1-3) vide : ")) - 1
            if 0 <= case < 3 and (etat_j1 if joueur == 1 else etat_j2)[case] is None:
                return case
            else:
                print("Case invalide ou déjà occupée.")
        except ValueError:
            print("Entrée invalide.")

def determiner_score(etat):
    return int("".join(str(x) for x in etat)) if any(x is not None for x in etat) else 0

def partie_joueur_contre_joueur():
    etat_j1 = [None] * 3
    etat_j2 = [None] * 3
    for tour in range(3):
        nb1 = random.randint(0, 9)
        c1 = placer_nombre_interface(1, etat_j1, etat_j2, nb1)
        etat_j1[c1] = nb1

        nb2 = random.randint(0, 9)
        c2 = placer_nombre_interface(2, etat_j1, etat_j2, nb2)
        etat_j2[c2] = nb2

    afficher_etats(etat_j1, etat_j2)
    s1 = determiner_score(etat_j1)
    s2 = determiner_score(etat_j2)
    print(f"\nRésultat : Joueur 1 = {s1}, Joueur 2 = {s2}")
    if s1 > s2:
        print("Joueur 1 gagne !")
        return 1
    elif s2 > s1:
        print("Joueur 2 gagne !")
        return 2
    else:
        print("Égalité !")
        return 0

def partie_joueur_contre_ia(ia):
    etat_j1 = [None] * 3
    etat_j2 = [None] * 3
    for tour in range(3):
        nb1 = random.randint(0, 9)
        c1 = placer_nombre_interface(1, etat_j1, etat_j2, nb1)
        etat_j1[c1] = nb1

        nb2 = random.randint(0, 9)
        c2 = ia(nb2, etat_j2[:], etat_j1[:])
        if c2 not in [1, 2, 3]:
            raise ValueError(f"L'IA a retourné une case invalide : {c2}")
        if etat_j2[c2 - 1] is not None:
            raise ValueError(f"L'IA a tenté de jouer dans une case occupée : {c2}")
        etat_j2[c2 - 1] = nb2

        print(f"\nTour {tour + 1} - Nombre tiré pour IA : {nb2}")
        afficher_etats(etat_j1, etat_j2)

    s1 = determiner_score(etat_j1)
    s2 = determiner_score(etat_j2)
    print(f"\nRésultat : Joueur = {s1}, IA = {s2}")
    if s1 > s2:
        print("Vous gagnez !")
        return 1
    elif s2 > s1:
        print("L'IA gagne !")
        return 2
    else:
        print("Égalité !")
        return 0

def partie_ia_contre_ia(ia1, ia2, nb_matchs=1, afficher=False):
    """
    Simule un tournoi entre deux IA avec barre de progression dynamique
    et estimation du temps d'exécution
    """
    import time
    import sys
    
    scores = [0, 0, 0]  # [IA1, IA2, Égalités]
    debut_total = time.time()
    debut_estimation = None
    temps_5_pourcent = None
    
    # Variables pour la barre de progression
    paliers = [i/20 for i in range(1, 21)]  # Paliers de 5% (5%, 10%, ... 100%)
    prochain_palier = 0
    
    print(f"Début du tournoi ({nb_matchs} matchs)")
    
    for match in range(nb_matchs):
        # Calcul du pourcentage d'avancement
        progression = (match + 1) / nb_matchs
        
        # Affichage de la barre de progression
        if progression >= paliers[prochain_palier]:
            pourcentage = paliers[prochain_palier] * 100
            bar_length = 20
            filled_length = int(bar_length * progression)
            bar = '=' * filled_length + ' ' * (bar_length - filled_length)
            
            # Calcul du temps écoulé pour les premiers 5%
            if pourcentage == 5:
                fin_5_pourcent = time.time()
                temps_5_pourcent = fin_5_pourcent - debut_total
                debut_estimation = fin_5_pourcent
                temps_estime_total = temps_5_pourcent * 20
                temps_restant = max(0, temps_estime_total - temps_5_pourcent)
                print(f"\r{pourcentage:3.0f}% [{bar}] Temps restant estimé: {temps_restant:.1f}s", end="")
            
            # Mise à jour de l'estimation après les 5 premiers %
            elif pourcentage > 5 and debut_estimation:
                temps_ecoule = time.time() - debut_estimation
                progression_ecoulee = (pourcentage - 5) / 95
                
                if progression_ecoulee > 0:
                    temps_restant = (temps_ecoule / progression_ecoulee) * (1 - progression_ecoulee)
                else:
                    temps_restant = 0
                    
                print(f"\r{pourcentage:3.0f}% [{bar}] Temps restant estimé: {temps_restant:.1f}s", end="")
            
            # Pour les 5 premiers %
            else:
                print(f"\r{pourcentage:3.0f}% [{bar}] Calcul de l'estimation...", end="")
            
            sys.stdout.flush()
            prochain_palier += 1
        
        # Jouer un match
        etat_j1 = [None] * 3
        etat_j2 = [None] * 3
        
        # Déterminer aléatoirement qui commence
        commencer = random.choice([1, 2])
        
        for tour in range(3):
            if commencer == 1:
                # IA1 joue en premier pour ce tour
                nb1 = random.randint(0, 9)
                case1 = ia1(nb1, etat_j1.copy(), etat_j2.copy())
                if case1 not in [1, 2, 3]:
                    raise ValueError(f"IA1 a retourné une case invalide : {case1}")
                if etat_j1[case1 - 1] is not None:
                    raise ValueError(f"IA1 a joué dans une case occupée : {case1}")
                etat_j1[case1 - 1] = nb1
                
                # IA2 joue ensuite
                nb2 = random.randint(0, 9)
                case2 = ia2(nb2, etat_j2.copy(), etat_j1.copy())
                if case2 not in [1, 2, 3]:
                    raise ValueError(f"IA2 a retourné une case invalide : {case2}")
                if etat_j2[case2 - 1] is not None:
                    raise ValueError(f"IA2 a joué dans une case occupée : {case2}")
                etat_j2[case2 - 1] = nb2
            else:
                # IA2 joue en premier pour ce tour
                nb2 = random.randint(0, 9)
                case2 = ia2(nb2, etat_j2.copy(), etat_j1.copy())
                if case2 not in [1, 2, 3]:
                    raise ValueError(f"IA2 a retourné une case invalide : {case2}")
                if etat_j2[case2 - 1] is not None:
                    raise ValueError(f"IA2 a joué dans une case occupée : {case2}")
                etat_j2[case2 - 1] = nb2
                
                # IA1 joue ensuite
                nb1 = random.randint(0, 9)
                case1 = ia1(nb1, etat_j1.copy(), etat_j2.copy())
                if case1 not in [1, 2, 3]:
                    raise ValueError(f"IA1 a retourné une case invalide : {case1}")
                if etat_j1[case1 - 1] is not None:
                    raise ValueError(f"IA1 a joué dans une case occupée : {case1}")
                etat_j1[case1 - 1] = nb1
            
            if afficher:
                print(f"\nTour {tour + 1}")
                print(f"IA1 a reçu : {nb1}")
                print(f"IA2 a reçu : {nb2}")
                afficher_etats(etat_j1, etat_j2)
        
        # Calcul des scores
        score1 = determiner_score(etat_j1)
        score2 = determiner_score(etat_j2)
        
        # Mise à jour des résultats
        if score1 > score2:
            scores[0] += 1
        elif score2 > score1:
            scores[1] += 1
        else:
            scores[2] += 1
    
    # Affichage final de la barre
    temps_total = time.time() - debut_total
    print(f"\r100% [{'=' * 20}] Temps total: {temps_total:.2f}s")
    
    return scores