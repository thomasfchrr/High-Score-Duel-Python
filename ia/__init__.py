import os
import importlib

def lister_ias():
    return sorted([
        f[:-3] for f in os.listdir(os.path.dirname(__file__))
        if f.endswith(".py") and f not in ["__init__.py"]
    ])

def charger_ia(nom):
    try:
        module = importlib.import_module(f"ia.{nom}")
        return module.ia
    except (ImportError, AttributeError):
        raise ValueError(f"Impossible de charger l'IA {nom}")