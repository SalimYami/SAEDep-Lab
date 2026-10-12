import java.rmi.*;

public interface StockService extends Remote {
    String verifierStock(String produit, int quantite)
            throws RemoteException;
}
