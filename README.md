# SAE Déploiement

Dépôt regroupant les travaux réalisés dans le cadre de la SAE Déploiement. Il couvre deux thématiques principales : les **Web Services SOAP** en Python et les appels de méthodes distantes en Java avec **RMI**.

---

## Structure du dépôt

```
SAE-Deploiement/
├── backend/               # Exemple introductif SOAP — CalculatriceService
│   ├── test.py
│   └── README.md
├── Tp/                    # Service SOAP avancé — CatalogueProduitService
│   ├── server.py
│   └── README.md
├── RMI/                   # Remote Method Invocation en Java — StockService
│   ├── StockService.java
│   ├── StockServiceImpl.java
│   ├── Server.java
│   ├── Client.java
│   └── README.md
└── README.md              # Ce fichier
```

---

## Modules

### `backend/` — Premier contact avec SOAP

Service de **calculatrice arithmétique** exposé via SOAP. Ce module sert d'introduction au protocole avant de passer à des modèles de données plus complexes. Il couvre les opérations `additionner`, `soustraire`, `multiplier`, `diviser`, `carre` et `resumer_operation` sur des types primitifs (`Float`, `Integer`).

→ [Voir le README détaillé](backend/README.md)

---

### `Tp/` — Service SOAP avec type complexe

Service de **gestion d'un catalogue de produits** exposé via SOAP 1.1. Il illustre la définition d'un `ComplexModel` Spyne (`Produit`), le retour de listes d'objets (`Iterable`), et des méthodes de filtrage avancées (par nom, par prix, disponibilité). Le WSDL est auto-généré et testable avec SoapUI ou `zeep`.

→ [Voir le README détaillé](Tp/README.md)

---

### `RMI/` — Remote Method Invocation Java

Implémentation d'un service de **vérification de stock** en Java via RMI. Le client appelle la méthode `verifierStock(produit, quantite)` comme si l'objet était local, alors qu'il s'exécute sur un serveur distant. Illustre le mécanisme de stub/squelette et l'annuaire RMI.

→ [Voir le README détaillé](RMI/README.md)

---

## Démarrage rapide

### Services SOAP (Python)

```bash
# Dépendances
pip install spyne lxml

# Exemple introductif (port 8000)
python backend/test.py

# Service catalogue (port 8001)
python Tp/server.py
```

### Service RMI (Java)

```bash
# Compilation
javac RMI/*.java

# Démarrer le serveur
java -cp RMI Server

# Dans un autre terminal, lancer le client
java -cp RMI Client
```

---

## Technologies utilisées

| Technologie | Usage                                 |
|-------------|---------------------------------------|
| Python 3    | Serveurs SOAP (`backend/`, `Tp/`)     |
| Spyne       | Framework Web Service SOAP en Python  |
| WSGI        | Serveur HTTP intégré                  |
| Java        | Service RMI (`RMI/`)                  |
| SoapUI      | Tests des endpoints SOAP              |
