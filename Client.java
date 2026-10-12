import java.rmi.*;

public class Client {
    public static void main(String[] args) throws Exception {
        StockService service = (StockService) Naming.lookup("rmi://localhost/StockService");

        System.out.println(service.verifierStock("Pomme", 10));
        System.out.println(service.verifierStock("Banane", 3));
        System.out.println(service.verifierStock("Orange", 0));
        System.out.println(service.verifierStock("Poire", -1));
    }
}
