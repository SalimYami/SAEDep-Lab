# SAE Déploiement - RMI

## 1. Définition
RMI (Remote Method Invocation) est un mécanisme Java permettant d'appeler des méthodes sur un objet résidant dans une autre machine virtuelle Java (JVM), sur la même machine ou à travers le réseau.

## 2. Client / Serveur
- **Serveur** : instancie l'objet distant, démarre le registre RMI sur le port 1099 (`LocateRegistry.createRegistry`) et l'enregistre dans l'annuaire (`Naming.rebind`).
- **Client** : récupère la référence distante via l'annuaire (`Naming.lookup`) à travers l'interface commune, puis invoque les méthodes distantes.
