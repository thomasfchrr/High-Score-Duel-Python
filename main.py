import os
import sys
import importlib
from game import partie_joueur_contre_joueur, partie_joueur_contre_ia, partie_ia_contre_ia
from ia import lister_ias, charger_ia

def menu():
    while True:
        try:
            print("\n=== MENU PRINCIPAL ===")
            print("1. Joueur contre joueur")
            print("2. Joueur contre machine")
            print("3. Tournoi de machines (IA vs IA)")
            print("4. Créateur d'IA")
            print("5. Entraîner une IA")
            print("6. Quitter")
            choix = input("Choisissez une option : ")

            if choix == "1":
                partie_joueur_contre_joueur()
            elif choix == "2":
                ia_disponibles = lister_ias()
                if not ia_disponibles:
                    print("Aucune IA disponible. Veuillez d'abord créer des IA.")
                    continue
                    
                print("\n=== Sélection de l'IA ===")
                for i, nom in enumerate(ia_disponibles):
                    print(f"{i + 1}. {nom}")
                
                try:
                    choix_ia = int(input("Choix : ")) - 1
                    if 0 <= choix_ia < len(ia_disponibles):
                        ia = charger_ia(ia_disponibles[choix_ia])
                        partie_joueur_contre_ia(ia)
                    else:
                        print("Choix invalide.")
                except ValueError:
                    print("Erreur: veuillez entrer un nombre.")
            elif choix == "3":
                ia_disponibles = lister_ias()
                if len(ia_disponibles) < 2:
                    print("Au moins deux IA sont nécessaires pour un tournoi.")
                    continue
                    
                print("\n=== Sélection de la première IA ===")
                for i, nom in enumerate(ia_disponibles):
                    print(f"{i + 1}. {nom}")
                try:
                    choix_ia1 = int(input("Choix : ")) - 1
                except ValueError:
                    print("Erreur: veuillez entrer un nombre.")
                    continue
                
                print("\n=== Sélection de la deuxième IA ===")
                for i, nom in enumerate(ia_disponibles):
                    print(f"{i + 1}. {nom}")
                try:
                    choix_ia2 = int(input("Choix : ")) - 1
                except ValueError:
                    print("Erreur: veuillez entrer un nombre.")
                    continue
                
                try:
                    nb_matchs = int(input("Nombre de matchs à simuler : "))
                except ValueError:
                    print("Erreur: veuillez entrer un nombre.")
                    continue
                
                if 0 <= choix_ia1 < len(ia_disponibles) and 0 <= choix_ia2 < len(ia_disponibles):
                    ia1 = charger_ia(ia_disponibles[choix_ia1])
                    ia2 = charger_ia(ia_disponibles[choix_ia2])
                    print(f"\nDébut du tournoi entre {ia_disponibles[choix_ia1]} et {ia_disponibles[choix_ia2]} ({nb_matchs} matchs)")
                    scores = partie_ia_contre_ia(ia1, ia2, nb_matchs, afficher=False)
                    print("\n=== STATISTIQUES FINALES ===")
                    print(f"{ia_disponibles[choix_ia1]}: {scores[0]} victoires ({scores[0]/nb_matchs*100:.1f}%)")
                    print(f"{ia_disponibles[choix_ia2]}: {scores[1]} victoires ({scores[1]/nb_matchs*100:.1f}%)")
                    print(f"Égalités: {scores[2]} ({scores[2]/nb_matchs*100:.1f}%)")
                else:
                    print("Choix invalide.")
            elif choix == "4":
                try:
                    from nn_creator import createur_ia
                    createur_ia()
                except Exception as e:
                    print(f"Erreur dans le créateur d'IA: {str(e)}")
            elif choix == "5":
                try:
                    from nn_trainer import entrainer_ia
                    entrainer_ia()
                except Exception as e:
                    print(f"Erreur dans l'entraîneur d'IA: {str(e)}")
            elif choix == "6":
                print("Au revoir !")
                sys.exit(0)
            else:
                print("Choix invalide.")
        except Exception as e:
            print(f"Erreur inattendue: {str(e)}")
            print("Retour au menu principal...")

if __name__ == "__main__":
    menu()