from src.sale import Sale

def filter_sales_by_category(sales: list[Sale], category: str) -> list[Sale]:
    """
    Filtra las ventas por una categoría usando filter y lambda.
    """
    categoria_buscada = category.lower()
    
    resultado = filter(lambda s: s.category.lower() == categoria_buscada, sales)
    
    return list(resultado)


def filter_sales_by_client(sales: list[Sale], client_id: int) -> list[Sale]:
    """
    Filtra las ventas de un cliente usando filter y lambda.
    """
    resultado = filter(lambda s: s.client_id == client_id, sales)
            
    return list(resultado)