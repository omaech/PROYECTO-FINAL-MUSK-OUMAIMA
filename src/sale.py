class Sale:
    
    """
    Representa una venta
    """
    
    def __init__ (self, sale_id: int, client_id: int, product: str, category: str, amount: float, date: str):
        
        self.sale_id = sale_id
        self.client_id = client_id
        self.product = product
        self.category= category
        self.amount = amount
        self.date = date
        
    def to_dict(self) -> dict:
        """
        Convierte el objeto a un diccionario Python para poder exportarlo como JSON
        sin dificultad.
        """
        return {
            "sale_id": self.sale_id,
            "client_id": self.client_id,
            "product": self.product,
            "category": self.category,
            "amount": self.amount,
            "date": self.date
        }