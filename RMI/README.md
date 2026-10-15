# RMI — Remote Method Invocation Java

Implémentation d'un service de **vérification de stock** en Java via le mécanisme **RMI**. Ce projet illustre comment appeler une méthode sur un objet distant de façon transparente, comme s'il était local.

---

## Qu'est-ce que RMI ?

**Remote Method Invocation** est une API Java permettant à une JVM d'invoquer des méthodes sur un objet situé dans une autre JVM, potentiellement sur une machine différente, via le réseau. C'est l'équivalent Java des appels de procédures distantes (RPC).

RMI repose sur trois composants clés :

| Composant     | Rôle                                                                 |
|---------------|----------------------------------------------------------------------|
| **Interface** | Contrat partagé entre client et serveur (étend `Remote`)             |
| **Stub**      | Proxy côté client — intercepte les appels et les sérialise           |
| **Squelette** | Proxy côté serveur — désérialise les appels et invoque l'objet réel  |
| **Registre**  | Annuaire RMI sur le port 1099 — permet au client de trouver le stub  |

---

## Structure du dossier

```
RMI/
├── StockService.java       # Interface distante (contrat)
├── StockServiceImpl.java   # Implémentation du service (côté serveur)
├── Server.java             # Démarrage du serveur et enregistrement dans l'annuaire
├── Client.java             # Client RMI — consommation du service
└── README.md               # Ce fichier
```

---

## Description des fichiers

### `StockService.java` — Interface distante

```java
import java.rmi.*;

public interface StockService extends Remote {
    String verifierStock(String produit, int quantite) throws RemoteException;
}
```

Toute interface RMI doit :
- Étendre `java.rmi.Remote`
- Déclarer `throws RemoteException` sur chaque méthode (les appels réseau peuvent échouer)

---

### `StockServiceImpl.java` — Logique métier

La méthode `verifierStock` analyse la quantité et retourne un message :

| Condition            | Message retourné                          |
|----------------------|-------------------------------------------|
| `quantite < 0`       | `"Quantite invalide pour <produit>"`      |
| `quantite == 0`      | `"<produit> : rupture de stock"`          |
| `0 < quantite < 5`   | `"<produit> : stock faible (<quantite>)"` |
| `quantite >= 5`      | `"<produit> : stock suffisant (<quantite>)"` |

L'implémentation étend `UnicastRemoteObject` pour être exportée automatiquement dans la JVM.

---

### `Server.java` — Serveur RMI

```java
StockServiceImpl obj = new StockServiceImpl();
LocateRegistry.createRegistry(1099);          // Démarre l'annuaire RMI
Naming.rebind("rmi://localhost/StockService", obj); // Enregistre l'objet
```

---

### `Client.java` — Client RMI

```java
StockService stub = (StockService) Naming.lookup("rmi://localhost/StockService");
System.out.println(stub.verifierStock("Pomme",  10)); // stock suffisant
System.out.println(stub.verifierStock("Banane",  3)); // stock faible
System.out.println(stub.verifierStock("Orange",  0)); // rupture de stock
System.out.println(stub.verifierStock("Poire",  -1)); // quantite invalide
```

Le client récupère le **stub** via l'annuaire et appelle `verifierStock` comme une méthode locale, sans connaître l'emplacement réseau de l'objet.

---

## Compilation et exécution

### 1. Compiler tous les fichiers

```bash
cd RMI
javac *.java
```

### 2. Démarrer le serveur

```bash
java Server
```

```
Serveur prêt !
```

### 3. Lancer le client (dans un autre terminal)

```bash
java Client
```

Sortie attendue :

```
Pomme : stock suffisant (10)
Banane : stock faible (3)
Orange : rupture de stock
Quantite invalide pour Poire
```

---

## Flux d'exécution

```
Client                     Annuaire RMI          Serveur
  |                            |                    |
  |-- Naming.lookup() -------->|                    |
  |<-- stub (proxy) ----------|                    |
  |                            |                    |
  |-- stub.verifierStock() -------------------------------->|
  |                            |        (exécution réelle) |
  |<------- String réponse --------------------------------|
```

---

## Différences entre RMI et SOAP

| Critère          | RMI                             | SOAP                             |
|------------------|----------------------------------|----------------------------------|
| Langage          | Java uniquement                  | Interopérable (tous langages)    |
| Transport        | JRMP (Java propriétaire)         | HTTP                             |
| Format           | Sérialisation Java (binaire)     | XML                              |
| Facilité         | Simple en Java pur               | Plus verbeux mais standard       |
| Interopérabilité | JVM à JVM uniquement             | Client/serveur hétérogènes       |
