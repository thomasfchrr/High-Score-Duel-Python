import os
import numpy as np
import importlib
import time
import random
from ia import lister_ias, charger_ia

def entrainer_ia():
    print("\n=== ENTRAÎNEMENT D'IA - RÉSEAUX DE NEURONES ===")
    
    # Lister les IA neuronales disponibles
    ia_disponibles = lister_ias()
    ia_nn = [ia for ia in ia_disponibles if ia.startswith("NN_")]
    
    if not ia_nn:
        print("Aucune IA neuronale disponible. Veuillez d'abord en créer une.")
        return
    
    # Sélectionner l'IA à entraîner
    print("\n=== Sélection de l'IA à entraîner ===")
    for i, nom in enumerate(ia_nn):
        print(f"{i + 1}. {nom}")
    
    while True:
        try:
            choix_ia = int(input("Choix : ")) - 1
            if 0 <= choix_ia < len(ia_nn):
                break
            print("Choix invalide. Veuillez entrer un numéro valide.")
        except ValueError:
            print("Erreur: veuillez entrer un nombre.")
    
    ia_nom = ia_nn[choix_ia]
    
    # Sélectionner l'IA adverse
    print("\n=== Sélection de l'IA adverse ===")
    ia_adversaires = [ia for ia in ia_disponibles if ia != ia_nom]
    for i, nom in enumerate(ia_adversaires):
        print(f"{i + 1}. {nom}")
    
    while True:
        try:
            choix_adversaire = int(input("Choix : ")) - 1
            if 0 <= choix_adversaire < len(ia_adversaires):
                break
            print("Choix invalide. Veuillez entrer un numéro valide.")
        except ValueError:
            print("Erreur: veuillez entrer un nombre.")
    
    adversaire_nom = ia_adversaires[choix_adversaire]
    
    # Paramètres d'entraînement
    while True:
        try:
            epochs = int(input("Nombre d'époques d'entraînement (1-1000): "))
            if 1 <= epochs <= 1000:
                break
            print("Erreur: le nombre doit être entre 1 et 1000.")
        except ValueError:
            print("Erreur: veuillez entrer un nombre entier.")
    
    while True:
        try:
            nb_parties = int(input("Nombre de parties par époque (10-1000): "))
            if 10 <= nb_parties <= 1000:
                break
            print("Erreur: le nombre doit être entre 10 et 1000.")
        except ValueError:
            print("Erreur: veuillez entrer un nombre entier.")
    
    while True:
        try:
            learning_rate = float(input("Taux d'apprentissage (0.001-0.1): "))
            if 0.001 <= learning_rate <= 0.1:
                break
            print("Erreur: le taux doit être entre 0.001 et 0.1.")
        except ValueError:
            print("Erreur: veuillez entrer un nombre décimal.")
    
    try:
        # Charger les IA
        ia_entrainement = charger_ia(ia_nom)
        ia_adversaire = charger_ia(adversaire_nom)
        
        # Charger le modèle neuronal
        module = importlib.import_module(f"ia.{ia_nom}")
        model = module.model
        
        # Chemin du fichier de poids
        weight_file = f"ia/{ia_nom}.npz"
        
        # Charger les poids si le fichier existe
        if os.path.exists(weight_file):
            try:
                model.load_weights(weight_file)
                print(f"Poids existants chargés depuis {weight_file}")
            except Exception as e:
                print(f"Erreur lors du chargement des poids: {str(e)}")
                print("Initialisation avec de nouveaux poids...")
                model.initialize_weights()
        else:
            model.initialize_weights()
            print("Initialisation avec de nouveaux poids")
        
        print(f"\nDébut de l'entraînement de '{ia_nom}' contre '{adversaire_nom}'")
        print(f"Configuration: {epochs} époques, {nb_parties} parties/époque, learning_rate={learning_rate}")
        print("Structure du réseau:")
        print(f"- Couches cachées: {model.hidden_layers}")
        print(f"- Neurones/couche: {model.neurons_per_layer}")
        print(f"- Fonction d'activation: ReLU (couches cachées), Softmax (sortie)")
        
        # Entraînement
        debut = time.time()
        for epoch in range(epochs):
            epoch_debut = time.time()
            try:
                X_train, y_train = generer_donnees_entrainement(ia_entrainement, ia_adversaire, nb_parties)
                
                # Entraîner le modèle avec les données générées
                model.train(X_train, y_train, epochs=1, learning_rate=learning_rate)
                
                # Sauvegarder les poids après chaque époque
                model.save_weights(weight_file)
                
                # Calculer la précision
                predictions = model.forward(X_train)
                y_pred = np.argmax(predictions, axis=1)
                y_true = np.argmax(y_train, axis=1)
                accuracy = np.mean(y_pred == y_true)
                
                epoch_temps = time.time() - epoch_debut
                print(f"Époque {epoch+1}/{epochs} - Précision: {accuracy:.2f} - Temps: {epoch_temps:.1f}s")
            
            except Exception as e:
                print(f"Erreur pendant l'époque {epoch+1}: {str(e)}")
                print("Poursuite de l'entraînement...")
        
        temps_total = time.time() - debut
        print(f"\nEntraînement terminé en {temps_total:.1f} secondes")
        print(f"Poids sauvegardés dans {weight_file}")
    
    except Exception as e:
        print(f"Erreur critique pendant l'entraînement: {str(e)}")
        print("L'entraînement a été interrompu.")

def generer_donnees_entrainement(ia_entrainement, ia_adversaire, nb_parties):
    """
    Génère des données d'entraînement en simulant des parties
    Retourne:
        X: tableau numpy des états du jeu (shape: [n, 7])
        y: tableau numpy des coups idéaux (one-hot encoded, shape: [n, 3])
    """
    X_data = []
    y_data = []
    
    for partie in range(nb_parties):
        try:
            etat_j1 = [None] * 3
            etat_j2 = [None] * 3
            
            for tour in range(3):
                # Générer un chiffre pour l'IA à entraîner
                nb = random.randint(0, 9)
                
                # Créer une copie des états pour la prédiction
                etat_j1_copy = etat_j1.copy()
                etat_j2_copy = etat_j2.copy()
                
                # Demander à l'IA experte (adversaire) quel coup elle jouerait
                coup_expert = ia_adversaire(nb, etat_j1_copy, etat_j2_copy) - 1
                
                # Vérifier que le coup est valide
                if coup_expert not in [0, 1, 2]:
                    coup_expert = 0  # Valeur par défaut si invalide
                
                # Enregistrer les données
                X = np.zeros(7)
                
                # Cases du joueur (remplace None par -1)
                for i in range(3):
                    X[i] = etat_j1_copy[i] if etat_j1_copy[i] is not None else -1
                
                # Cases adversaire (remplace None par -1)
                for i in range(3):
                    X[i+3] = etat_j2_copy[i] if etat_j2_copy[i] is not None else -1
                
                # Chiffre à placer
                X[6] = nb
                
                # Encodage one-hot du coup idéal
                y = np.zeros(3)
                y[coup_expert] = 1
                
                X_data.append(X)
                y_data.append(y)
                
                # Jouer le coup avec l'IA à entraîner (pour faire avancer la partie)
                coup = ia_entrainement(nb, etat_j1, etat_j2) - 1
                if 0 <= coup < 3 and etat_j1[coup] is None:
                    etat_j1[coup] = nb
                else:
                    # Trouver une case libre au cas où
                    for i in range(3):
                        if etat_j1[i] is None:
                            etat_j1[i] = nb
                            break
                
                # Faire jouer l'adversaire
                nb_adv = random.randint(0, 9)
                coup_adv = ia_adversaire(nb_adv, etat_j2, etat_j1) - 1
                if 0 <= coup_adv < 3 and etat_j2[coup_adv] is None:
                    etat_j2[coup_adv] = nb_adv
                else:
                    # Trouver une case libre au cas où
                    for i in range(3):
                        if etat_j2[i] is None:
                            etat_j2[i] = nb_adv
                            break
        
        except Exception as e:
            print(f"Erreur dans la partie {partie+1}: {str(e)}")
            continue
    
    return np.array(X_data), np.array(y_data)