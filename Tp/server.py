from spyne import Application, rpc, ServiceBase, Integer, Unicode, Float, Iterable, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

# Catalogue de produits en mémoire
produits = [
    {"id": 1, "nom": "Clavier mécanique", "prix": 89.99, "stock": 15},
    {"id": 2, "nom": "Souris gaming",     "prix": 49.99, "stock": 32},
    {"id": 3, "nom": "Écran 27 pouces",   "prix": 299.00, "stock": 8},
    {"id": 4, "nom": "Casque audio",      "prix": 129.50, "stock": 20},
    {"id": 5, "nom": "Webcam HD",         "prix": 75.00,  "stock": 0},
]

# Définition du type complexe Produit
class Produit(ComplexModel):
    id    = Integer
    nom   = Unicode
    prix  = Float
    stock = Integer


class CatalogueProduitService(ServiceBase):

    @rpc(_returns=Iterable(Produit))
    def lister_produits(ctx):
        """
        Renvoie l'intégralité du catalogue de produits.
        """
        return [Produit(**p) for p in produits]

    @rpc(Integer, _returns=Produit)
    def obtenir_produit(ctx, id):
        """
        Retourne un produit à partir de son identifiant.
        Retourne None si l'identifiant n'existe pas.
        """
        trouve = next((p for p in produits if p["id"] == id), None)
        return Produit(**trouve) if trouve else None

    @rpc(Unicode, _returns=Iterable(Produit))
    def rechercher_par_nom(ctx, mot_cle):
        """
        Recherche les produits dont le nom contient le mot-clé (insensible à la casse).
        """
        mot_cle = mot_cle.lower() if mot_cle else ""
        return [Produit(**p) for p in produits if mot_cle in p["nom"].lower()]

    @rpc(Float, _returns=Iterable(Produit))
    def produits_moins_de(ctx, prix_max):
        """
        Retourne tous les produits dont le prix est inférieur ou égal à prix_max.
        """
        return [Produit(**p) for p in produits if p["prix"] <= prix_max]

    @rpc(Integer, _returns=Unicode)
    def verifier_disponibilite(ctx, id):
        """
        Vérifie si un produit est en stock.
        Retourne 'disponible', 'rupture de stock' ou 'produit introuvable'.
        """
        trouve = next((p for p in produits if p["id"] == id), None)
        if not trouve:
            return "produit introuvable"
        return "disponible" if trouve["stock"] > 0 else "rupture de stock"


# Configuration de l'application SOAP
application = Application(
    [CatalogueProduitService],
    tns="sae.deploiement.catalogue",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

wsgi_app = WsgiApplication(application)

if __name__ == "__main__":
    PORT = 8001
    print(f"[SOAP] Serveur CatalogueProduitService en écoute sur http://localhost:{PORT}")
    print(f"[SOAP] WSDL disponible sur : http://localhost:{PORT}/?wsdl")
    server = make_server("0.0.0.0", PORT, wsgi_app)
    server.serve_forever()
