import os
import numpy as np

def createur_ia():
    print("\n=== CRÉATEUR D'IA - RÉSEAUX DE NEURONES ===")
    
    # Vérifier que le dossier ia existe
    if not os.path.exists("ia"):
        try:
            os.makedirs("ia")
        except OSError as e:
            print(f"Erreur: Impossible de créer le dossier 'ia': {str(e)}")
            return
    
    # Demander les paramètres du réseau avec gestion d'erreurs
    while True:
        try:
            nb_couches = int(input("Nombre de couches cachées (1-10): "))
            if 1 <= nb_couches <= 10:
                break
            print("Erreur: le nombre doit être entre 1 et 10.")
        except ValueError:
            print("Erreur: veuillez entrer un nombre entier.")
    
    while True:
        try:
            nb_neurones = int(input("Nombre de neurones par couche (10-500): "))
            if 10 <= nb_neurones <= 500:
                break
            print("Erreur: le nombre doit être entre 10 et 500.")
        except ValueError:
            print("Erreur: veuillez entrer un nombre entier.")
    
    nom_base = f"NN_{nb_couches}_LAYERS_{nb_neurones}_NEURONS"
    nom_fichier = nom_base
    compteur = 1

    while os.path.exists(f"ia/{nom_fichier}.py"):
        nom_fichier = f"{nom_base}_{compteur}"
        compteur += 1

    try:
        creer_fichier_ia(nom_fichier, nb_couches, nb_neurones)
        print(f"\nIA '{nom_fichier}' créée avec succès dans le dossier ia/")
        print(f"Structure: {nb_couches} couches cachées avec {nb_neurones} neurones chacune")
        print("Vous pouvez maintenant entraîner cette IA dans le menu principal")
    except IOError as e:
        print(f"Erreur: Impossible d'écrire dans le fichier: {str(e)}")
    except Exception as e:
        print(f"Erreur inattendue lors de la création de l'IA: {str(e)}")

def creer_fichier_ia(nom_ia, nb_couches, nb_neurones):
    nom_fichier = f"ia/{nom_ia}.py"

    contenu = f"""# -*- coding: utf-8 -*-
import numpy as np
import os

class NeuralNetwork:
    def __init__(self):
        self.input_size = 7
        self.output_size = 3
        self.hidden_layers = {nb_couches}
        self.neurons_per_layer = {nb_neurones}
        self.initialize_weights()
    
    def initialize_weights(self):
        self.weights = []
        self.biases = []
        self.weights.append(np.random.randn(self.input_size, self.neurons_per_layer) * 0.1)
        self.biases.append(np.zeros((1, self.neurons_per_layer)))
        for _ in range(self.hidden_layers - 1):
            self.weights.append(np.random.randn(self.neurons_per_layer, self.neurons_per_layer) * 0.1)
            self.biases.append(np.zeros((1, self.neurons_per_layer)))
        self.weights.append(np.random.randn(self.neurons_per_layer, self.output_size) * 0.1)
        self.biases.append(np.zeros((1, self.output_size)))
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def relu_derivative(self, x):
        return (x > 0).astype(float)
    
    def softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def forward(self, X):
        self.a = [X]
        self.z = []
        for i in range(len(self.weights)):
            z = np.dot(self.a[-1], self.weights[i]) + self.biases[i]
            self.z.append(z)
            a = self.softmax(z) if i == len(self.weights) - 1 else self.relu(z)
            self.a.append(a)
        return self.a[-1]
    
    def backward(self, X, y, learning_rate):
        m = X.shape[0]
        self.delta = [self.a[-1] - y]
        for i in range(len(self.weights)-1, 0, -1):
            delta = np.dot(self.delta[0], self.weights[i].T) * self.relu_derivative(self.z[i-1])
            self.delta.insert(0, delta)
        for i in range(len(self.weights)):
            dw = np.dot(self.a[i].T, self.delta[i]) / m
            db = np.sum(self.delta[i], axis=0, keepdims=True) / m
            self.weights[i] -= learning_rate * dw
            self.biases[i] -= learning_rate * db
    
    def train(self, X_train, y_train, epochs, learning_rate=0.01, batch_size=32):
        n = X_train.shape[0]
        for epoch in range(epochs):
            permutation = np.random.permutation(n)
            X_shuffled = X_train[permutation]
            y_shuffled = y_train[permutation]
            for i in range(0, n, batch_size):
                X_batch = X_shuffled[i:i+batch_size]
                y_batch = y_shuffled[i:i+batch_size]
                self.forward(X_batch)
                self.backward(X_batch, y_batch, learning_rate)
    
    def save_weights(self, filename):
        np.savez(filename,
                 **{{f"w{{i}}": w for i, w in enumerate(self.weights)}},
                 **{{f"b{{i}}": b for i, b in enumerate(self.biases)}},
                 hidden_layers=self.hidden_layers,
                 neurons_per_layer=self.neurons_per_layer)

    def load_weights(self, filename):
        data = np.load(filename)
        self.hidden_layers = int(data['hidden_layers'])
        self.neurons_per_layer = int(data['neurons_per_layer'])
        self.weights = []
        self.biases = []
        i = 0
        while f"w{{i}}" in data:
            self.weights.append(data[f"w{{i}}"])
            i += 1
        i = 0
        while f"b{{i}}" in data:
            self.biases.append(data[f"b{{i}}"])
            i += 1

model = NeuralNetwork()

def ia(chiffre, cases_perso, cases_adversaire):
    X = np.zeros((1, 7))
    for i in range(3):
        X[0, i] = cases_perso[i] if cases_perso[i] is not None else -1
    for i in range(3):
        X[0, i+3] = cases_adversaire[i] if cases_adversaire[i] is not None else -1
    X[0, 6] = chiffre
    try:
        weight_file = os.path.splitext(__file__)[0] + ".npz"
        if os.path.exists(weight_file):
            try:
                model.load_weights(weight_file)
            except Exception as load_error:
                print("Attention: Impossible de charger les poids -", str(load_error))
                print("Utilisation des poids par défaut...")
                model.initialize_weights()
        predictions = model.forward(X)
        case_libre = [i for i, v in enumerate(cases_perso) if v is None]
        if not case_libre:
            return 1
        probas_cases_libres = [predictions[0, i] for i in case_libre]
        case_choisie = case_libre[np.argmax(probas_cases_libres)]
        return case_choisie + 1
    except Exception as prediction_error:
        print("Erreur dans l'IA:", str(prediction_error))
        case_libre = [i for i, v in enumerate(cases_perso) if v is None]
        if case_libre:
            return case_libre[0] + 1
        return 1
"""

    try:
        with open(nom_fichier, "w", encoding="utf-8") as f:
            f.write(contenu)
    except IOError as e:
        raise Exception(f"Impossible d'écrire dans le fichier: {str(e)}")
