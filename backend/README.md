# Exemple de service web SOAP — CalculatriceService

Ce projet est un exemple introductif de **service web SOAP** écrit en Python avec **Spyne**. Il expose une calculatrice arithmétique via le protocole SOAP 1.1 et illustre les mécanismes de base : définition de méthodes distantes, typage fort des paramètres et génération automatique du WSDL.

---

## Objectif pédagogique

Avant d'aborder des modèles complexes (types personnalisés, listes), il est utile de comprendre comment SOAP fonctionne sur des types primitifs. Ce service permet de :

- Comprendre la structure d'une requête/réponse SOAP
- Observer le WSDL généré par Spyne
- Tester avec SoapUI avant de passer au service principal (`Tp/`)

---

## Prérequis

```bash
pip install spyne lxml
```

---

## Méthodes exposées

| Méthode             | Paramètres            | Retour    | Description                                |
|---------------------|-----------------------|-----------|--------------------------------------------|
| `additionner`       | `a: Float, b: Float`  | `Float`   | Calcule `a + b`                            |
| `soustraire`        | `a: Float, b: Float`  | `Float`   | Calcule `a - b`                            |
| `multiplier`        | `a: Float, b: Float`  | `Float`   | Calcule `a × b`                            |
| `diviser`           | `a: Float, b: Float`  | `Unicode` | Calcule `a / b` (gère la division par 0)   |
| `carre`             | `n: Integer`          | `Integer` | Retourne `n²`                              |
| `resumer_operation` | `a: Float, b: Float`  | `Unicode` | Retourne une phrase résumant `+` et `×`    |

---

## Lancer le serveur

```bash
python test.py
```

```
[SOAP] Serveur CalculatriceService en écoute sur http://localhost:8000
[SOAP] WSDL disponible sur : http://localhost:8000/?wsdl
```

---

## Exemple de requête SOAP

Requête pour multiplier 6 par 7 :

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:calc="sae.deploiement.calculatrice">
   <soapenv:Header/>
   <soapenv:Body>
      <calc:multiplier>
         <calc:a>6</calc:a>
         <calc:b>7</calc:b>
      </calc:multiplier>
   </soapenv:Body>
</soapenv:Envelope>
```

Réponse :

```xml
<tns:multiplierResponse>
   <tns:multiplierResult>42.0</tns:multiplierResult>
</tns:multiplierResponse>
```

---

## Tester avec Python (`zeep`)

```python
from zeep import Client

client = Client("http://localhost:8000/?wsdl")

print(client.service.additionner(10.5, 4.5))   # → 15.0
print(client.service.carre(7))                  # → 49
print(client.service.diviser(10, 0))            # → "Erreur : division par zéro interdite"
print(client.service.resumer_operation(3, 5))   # → "3.0 + 5.0 = 8.0 | 3.0 × 5.0 = 15.0"
```

---

## Différence avec le service `Tp/`

| Aspect          | `backend/` (ce fichier)     | `Tp/`                             |
|-----------------|-----------------------------|-----------------------------------|
| Complexité      | Types primitifs uniquement  | `ComplexModel` (type Produit)     |
| Retour liste    | Non                         | Oui (`Iterable(Produit)`)         |
| Cas d'usage     | Premier contact avec SOAP   | Gestion d'un catalogue réel       |
| Port            | 8000                        | 8001                              |
