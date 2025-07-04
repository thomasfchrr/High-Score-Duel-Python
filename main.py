from game import partie_joueur_contre_joueur, partie_joueur_contre_ia, partie_ia_contre_ia
from ia import lister_ias, charger_ia
import sys

def menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Joueur contre joueur")
        print("2. Joueur contre machine")
        print("3. Tournoi de machines (IA vs IA)")
        print("4. Quitter")
        choix = input("Choisissez une option : ")

        if choix == "1":
            partie_joueur_contre_joueur()
        elif choix == "2":
            ia_disponibles = lister_ias()
            print("\n=== Sélection de l'IA ===")
            for i, nom in enumerate(ia_disponibles):
                print(f"{i + 1}. {nom}")
            choix_ia = int(input("Choix : ")) - 1
            if 0 <= choix_ia < len(ia_disponibles):
                ia = charger_ia(ia_disponibles[choix_ia])
                partie_joueur_contre_ia(ia)
            else:
                print("Choix invalide.")
        elif choix == "3":
            ia_disponibles = lister_ias()
            print("\n=== Sélection de la première IA ===")
            for i, nom in enumerate(ia_disponibles):
                print(f"{i + 1}. {nom}")
            choix_ia1 = int(input("Choix : ")) - 1
            print("\n=== Sélection de la deuxième IA ===")
            for i, nom in enumerate(ia_disponibles):
                print(f"{i + 1}. {nom}")
            choix_ia2 = int(input("Choix : ")) - 1
            nb_matchs = int(input("Nombre de matchs à simuler : "))
            
            if 0 <= choix_ia1 < len(ia_disponibles) and 0 <= choix_ia2 < len(ia_disponibles):
                ia1 = charger_ia(ia_disponibles[choix_ia1])
                ia2 = charger_ia(ia_disponibles[choix_ia2])
                print(f"\nDébut du tournoi entre {ia_disponibles[choix_ia1]} et {ia_disponibles[choix_ia2]} ({nb_matchs} matchs)")
                
                scores = partie_ia_contre_ia(ia1, ia2, nb_matchs, afficher=False)
                
                # Affichage amélioré avec les noms des IAs
                print("\n=== STATISTIQUES FINALES ===")
                total_matchs = sum(scores)
                print(f"{ia_disponibles[choix_ia1]}:")
                print(f"  Victoires: {scores[0]} ({scores[0]/total_matchs*100:.1f}%)")
                print(f"{ia_disponibles[choix_ia2]}:")
                print(f"  Victoires: {scores[1]} ({scores[1]/total_matchs*100:.1f}%)")
                print(f"Égalités: {scores[2]} ({scores[2]/total_matchs*100:.1f}%)")
                
                # Détermination du vainqueur global
                if scores[0] > scores[1]:
                    print(f"\nVAINQUEUR FINAL: {ia_disponibles[choix_ia1]}")
                elif scores[1] > scores[0]:
                    print(f"\nVAINQUEUR FINAL: {ia_disponibles[choix_ia2]}")
                else:
                    print("\nTOURNOI TERMINÉ AVEC ÉGALITÉ PARFAITE!")
            else:
                print("Choix invalide.")
        elif choix == "4":
            print("Au revoir !")
            sys.exit(0)
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    menu()