from src.client import Client

class ClientCollection:
    def __init__(self, clients: list[Client]):
        """
        Gestiona listas de objetos Client.
        """
        self.clients = clients

    def get_client_by_id(self, client_id: int) -> Client | None:
        """
        Devuelve un Client concreto.
        Si no existe, devuelve None.
        """
        for client in self.clients:
            if client.client_id == client_id:
                return client
        return None

    def clients_by_country(self, country: str) -> list[Client]:
        """
        Devuelve lista de cliente de un país.
        """
        clientes_country = []
        
        for client in self.clients:
            if client.country.lower() == country.lower():
                clientes_country.append(client)
                
        return clientes_country