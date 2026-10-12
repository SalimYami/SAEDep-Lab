import java.rmi.*;
import java.rmi.server.*;

public class StockServiceImpl extends UnicastRemoteObject
        implements StockService {

    public StockServiceImpl() throws RemoteException {}

    public String verifierStock(String produit, int quantite)
            throws RemoteException {

        if (quantite < 0) {
            return "Quantite invalide pour " + produit;
        } else if (quantite == 0) {
            return produit + " : rupture de stock";
        } else if (quantite < 5) {
            return produit + " : stock faible (" + quantite + ")";
        } else {
            return produit + " : stock suffisant (" + quantite + ")";
        }
    }
}
