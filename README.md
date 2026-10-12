# SAE Déploiement - RMI

## 1. Définition
RMI (Remote Method Invocation) est un mécanisme Java permettant d'appeler des méthodes sur un objet résidant dans une autre machine virtuelle Java (JVM), sur la même machine ou à travers le réseau.

## 2. Client / Serveur
- **Serveur** : instancie l'objet distant, démarre le registre RMI sur le port 1099 (`LocateRegistry.createRegistry`) et l'enregistre dans l'annuaire (`Naming.rebind`).
- **Client** : récupère le `stub` via l'annuaire (`Naming.lookup`) et appelle la méthode comme si l'objet était local.

## 3. Notes
- **stub** : proxy côté client représentant l'objet distant.
- L'appel se fait de manière transparente pour le client (même syntaxe qu'un appel local).
