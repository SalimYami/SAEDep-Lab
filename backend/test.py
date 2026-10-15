from spyne import Application, rpc, ServiceBase, Integer, Float, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server


class CalculatriceService(ServiceBase):

    # Additionne deux nombres flottants
    @rpc(Float, Float, _returns=Float)
    def additionner(ctx, a, b):
        return a + b

    # Soustrait b de a
    @rpc(Float, Float, _returns=Float)
    def soustraire(ctx, a, b):
        return a - b

    # Multiplie deux nombres
    @rpc(Float, Float, _returns=Float)
    def multiplier(ctx, a, b):
        return a * b

    # Divise a par b — retourne un message d'erreur en cas de division par zéro
    @rpc(Float, Float, _returns=Unicode)
    def diviser(ctx, a, b):
        if b == 0:
            return "Erreur : division par zéro interdite"
        return str(round(a / b, 6))

    # Retourne le carré d'un entier
    @rpc(Integer, _returns=Integer)
    def carre(ctx, n):
        return n * n

    # Retourne le résumé d'une opération sous forme de phrase
    @rpc(Float, Float, _returns=Unicode)
    def resumer_operation(ctx, a, b):
        somme    = a + b
        produit  = a * b
        return (
            f"{a} + {b} = {somme} | "
            f"{a} × {b} = {produit}"
        )


# Configuration du service avec le protocole SOAP 1.1
application = Application(
    [CalculatriceService],
    tns="sae.deploiement.calculatrice",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

wsgi_app = WsgiApplication(application)

if __name__ == "__main__":
    PORT = 8000
    print(f"[SOAP] Serveur CalculatriceService en écoute sur http://localhost:{PORT}")
    print(f"[SOAP] WSDL disponible sur : http://localhost:{PORT}/?wsdl")
    server = make_server("0.0.0.0", PORT, wsgi_app)
    server.serve_forever()
