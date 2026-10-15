# Service SOAP — CatalogueProduitService

Service web SOAP développé en Python avec la bibliothèque **Spyne**, exposant un catalogue de produits fictifs en mémoire. Il illustre la mise en place d'un Web Service interopérable basé sur le protocole SOAP 1.1, avec génération automatique du WSDL.

---

## Contexte

Ce TP s'inscrit dans le cadre de la SAE Déploiement. L'objectif est de comprendre le fonctionnement des **Web Services SOAP** : comment définir un contrat (WSDL), sérialiser des types complexes en XML, et exposer des méthodes distantes accessibles depuis n'importe quel client compatible SOAP (SoapUI, Python `zeep`, etc.).

---

## Prérequis

| Outil       | Version minimale |
|-------------|-----------------|
| Python      | 3.8+            |
| spyne       | 2.14+           |
| lxml        | toute version   |

Installation des dépendances :

```bash
pip install spyne lxml
```

---

## Structure du dossier

```
Tp/
├── server.py   # Serveur SOAP principal
└── README.md   # Ce fichier
```

---

## Modèle de données — `Produit`

Le type complexe `Produit` est sérialisé en XML via Spyne :

| Champ   | Type      | Description                          |
|---------|-----------|--------------------------------------|
| `id`    | `Integer` | Identifiant unique du produit        |
| `nom`   | `Unicode` | Nom commercial du produit            |
| `prix`  | `Float`   | Prix en euros (€)                    |
| `stock` | `Integer` | Quantité disponible en entrepôt      |

Le catalogue initial contient 5 produits (clavier, souris, écran, casque, webcam).

---

## Méthodes exposées

| Méthode                  | Paramètres       | Retour                  | Description                                            |
|--------------------------|------------------|-------------------------|--------------------------------------------------------|
| `lister_produits`        | —                | `Produit[]`             | Retourne l'ensemble du catalogue                       |
| `obtenir_produit`        | `id: Integer`    | `Produit`               | Retourne un produit par son identifiant                |
| `rechercher_par_nom`     | `mot_cle: str`   | `Produit[]`             | Filtre le catalogue sur le nom (insensible à la casse) |
| `produits_moins_de`      | `prix_max: Float`| `Produit[]`             | Filtre par prix maximum                                |
| `verifier_disponibilite` | `id: Integer`    | `Unicode`               | Renvoie `disponible`, `rupture de stock` ou `produit introuvable` |

---

## Lancer le serveur

```bash
python server.py
```

La console affichera :

```
[SOAP] Serveur CatalogueProduitService en écoute sur http://localhost:8001
[SOAP] WSDL disponible sur : http://localhost:8001/?wsdl
```

Le WSDL est accessible via le navigateur à l'adresse :  
`http://localhost:8001/?wsdl`

---

## Tester avec SoapUI

1. Ouvrir **SoapUI** → _File_ → _New SOAP Project_
2. Renseigner l'URL du WSDL : `http://localhost:8001/?wsdl`
3. SoapUI génère automatiquement les requêtes pour chaque méthode
4. Exemple de requête `obtenir_produit` (id=2) :

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:cat="sae.deploiement.catalogue">
   <soapenv:Header/>
   <soapenv:Body>
      <cat:obtenir_produit>
         <cat:id>2</cat:id>
      </cat:obtenir_produit>
   </soapenv:Body>
</soapenv:Envelope>
```

Réponse attendue :

```xml
<tns:obtenir_produitResponse>
   <tns:obtenir_produitResult>
      <tns:id>2</tns:id>
      <tns:nom>Souris gaming</tns:nom>
      <tns:prix>49.99</tns:prix>
      <tns:stock>32</tns:stock>
   </tns:obtenir_produitResult>
</tns:obtenir_produitResponse>
```

---

## Tester avec Python (`zeep`)

```python
from zeep import Client

client = Client("http://localhost:8001/?wsdl")

# Lister tous les produits
produits = client.service.lister_produits()
for p in produits:
    print(f"[{p.id}] {p.nom} — {p.prix}€ (stock: {p.stock})")

# Vérifier la disponibilité du produit 5 (webcam)
etat = client.service.verifier_disponibilite(5)
print(etat)  # → rupture de stock
```

---

## Points clés SOAP / Spyne

- **`ComplexModel`** : permet de définir des types de données personnalisés sérialisés en XML.
- **`@rpc`** : décorateur qui expose une méthode Python comme opération SOAP.
- **`Soap11`** avec `validator="lxml"` : valide les requêtes entrantes contre le schéma XSD.
- **`WsgiApplication`** : adaptateur WSGI standard, compatible avec n'importe quel serveur Python (gunicorn, uWSGI…).
- **WSDL auto-généré** : Spyne génère le contrat WSDL à partir des annotations Python, sans configuration XML manuelle.
