import java.rmi.*;
import java.rmi.registry.*;

public class Server {
    public static void main(String[] args) throws Exception {
        StockServiceImpl obj = new StockServiceImpl();
        LocateRegistry.createRegistry(1099);
        Naming.rebind("rmi://localhost/StockService", obj);
        System.out.println("Serveur prêt !");
    }
}
