import java.rmi.*;

public class Client {
    public static void main(String[] args) throws Exception {
        // Recuperation du stub (proxy client) depuis l'annuaire RMI
        StockService stub = (StockService) Naming.lookup("rmi://localhost/StockService");

        // Le client appelle verifierStock comme si l'objet etait local
        System.out.println(stub.verifierStock("Pomme", 10));
        System.out.println(stub.verifierStock("Banane", 3));
        System.out.println(stub.verifierStock("Orange", 0));
        System.out.println(stub.verifierStock("Poire", -1));
    }
}
