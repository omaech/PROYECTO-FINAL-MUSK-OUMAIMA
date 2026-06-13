from src.sale import Sale

class SalesCollection:
    def __init__(self, sales: list[Sale]):
        """
        Gestiona listas de objetos Sale.
        """
        self.sales = sales

    def sales_by_client(self, client_id: int) -> list[Sale]:
        """
        Devuelve todas las ventas de un cliente.
        """
        ventas_cliente = []
        for sale in self.sales:
            if sale.client_id == client_id:
                ventas_cliente.append(sale)
        return ventas_cliente

    def total_amount_by_client(self, client_id: int) -> float:
        """
        Calcula la suma total de los importes de un cliente.
        """
        ventas_cliente = self.sales_by_client(client_id)
        
        suma_total = 0.0
        for sale in ventas_cliente:
            suma_total = suma_total + sale.amount
            
        return suma_total

    def total_amount_by_category(self, category: str) -> float:
        """
        Calcula la suma total de las ventas de una categoría.
        """
        suma_categoria = 0.0
        for sale in self.sales:
            if sale.category.lower() == category.lower():
                suma_categoria = suma_categoria + sale.amount
                
        return suma_categoria
    def average_sale_by_client(self, client_id: int) -> float:
        """
        Calcula la media de gasto por venta para un cliente.
        Si no tiene ventas, devuelve 0.0.
        """
        ventas_cliente = self.sales_by_client(client_id)
        
        # Comprobamos si la lista está vacía para evitar dividir por 0
        if len(ventas_cliente) == 0:
            return 0.0
            
        total_gastado = self.total_amount_by_client(client_id)
        media = total_gastado / len(ventas_cliente)
        
        return media