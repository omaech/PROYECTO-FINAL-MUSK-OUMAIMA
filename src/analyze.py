import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import os
import pandas as pd

# Importamos las clases y funciones implementadas anteriormente 
from src.client import Client
from src.sale import Sale
from src.client_collection import ClientCollection
from src.sales_collection import SalesCollection
from src.functional_utils import filter_sales_by_category, filter_sales_by_client

def generate_report():
    # 1. Rutas y lectura de archivos
    clientes = os.path.join("data", "clients.json")
    ventas = os.path.join("data", "sales.csv")

    # Leer los datos en bruto
    with open(clientes, "r", encoding="utf-8") as f:
        datos_json_clientes = json.load(f)
        
    df_ventas = pd.read_csv(ventas)

    # 2. Creamos los objetos (POO)
    objetos_clientes = []
    for cliente in datos_json_clientes:
        objeto_cliente = Client(
            client_id=int(cliente["client_id"]),
            name=str(cliente["name"]),
            country=str(cliente["country"]),
            signup_date=str(cliente["signup_date"])
        )
        objetos_clientes.append(objeto_cliente)

    objetos_ventas = []
    for index, venta in df_ventas.iterrows():
        objeto_venta = Sale(
            sale_id=str(venta["sale_id"]),
            client_id=int(venta["client_id"]),
            product=str(venta["product"]),
            category=str(venta["category"]),
            amount=float(venta["amount"]),
            date=str(venta["date"])
        )
        objetos_ventas.append(objeto_venta)

    # Instanciamos las colecciones
    coleccion_clientes = ClientCollection(objetos_clientes)
    coleccion_ventas = SalesCollection(objetos_ventas)

    # 3. Implentación de los 10 cálculos 

    # --- C.1: Número total de clientes ---
    total_clientes = len(coleccion_clientes.clients)

    # --- C.2: Número total de ventas ---
    total_ventas = len(coleccion_ventas.sales)

    # --- C. 3, 4 y 5: Métricas por cliente ---
    lista_clientes = []
    suma_ingresos_totales = 0.0

    for cliente in coleccion_clientes.clients:
        id_act = cliente.client_id
        
        # C.3: Total ingresos por cliente
        gasto_total = coleccion_ventas.total_amount_by_client(id_act)
        suma_ingresos_totales = suma_ingresos_totales + gasto_total
        
        # C.4: Número de ventas por cliente
        num_ventas = len(coleccion_ventas.sales_by_client(id_act))
        
        # C.5: Ingreso promedio por venta de cada cliente
        promedio_gasto = coleccion_ventas.average_sale_by_client(id_act)
        
        # Estructuramos la lista "clients" del JSON
        diccionario_cliente = {
            "client_id": id_act,
            "name": cliente.name,
            "total_spent":  round(float(gasto_total),2),
            "sale_count": int(num_ventas),
            "average_sale": round(float(promedio_gasto), 2)
        }
        lista_clientes.append(diccionario_cliente)

    # --- C.6: Cliente con mayor gasto por país ---
    # Agrupamos primero qué clientes pertenecen a cada país
    paises = {}
    for cliente in coleccion_clientes.clients:
        pais = cliente.country
        if pais not in paises:
            paises[pais] = []
        paises[pais].append(cliente)

    # Buscamos el cliente que más gastó en cada país
    cliente_por_pais = {}
    for pais, lista_clientes_pais in paises.items():
        max_gasto = -1.0
        nombre_cliente = None
        
        for cliente in lista_clientes_pais:
            gasto = coleccion_ventas.total_amount_by_client(cliente.client_id)
            if gasto > max_gasto:
                max_gasto = gasto
                nombre_cliente = cliente.name
                
        cliente_por_pais[pais] = nombre_cliente

    # --- C.7: Total de ventas por categoría ---
    ventas_por_categoria = df_ventas.groupby("category")["amount"].sum()
    categorias = {}
    for cat, total in ventas_por_categoria.items():
        categorias[str(cat)] =  round(float(total),2)

    # --- C.8: Cliente con más ventas en una categoría específica ---
    # Usamos la función de functional_utils para filtrar una categoría 
    categoria_objetivo = "Electronics"
    ventas_categoria_objetivo = filter_sales_by_category(coleccion_ventas.sales, categoria_objetivo)
    
    max_ventas_categoria = 0
    id_cliente_top_categoria = None
    
    for cliente in coleccion_clientes.clients:
        ventas_cliente_en_categoria = filter_sales_by_client(ventas_categoria_objetivo, cliente.client_id)
        cantidad = len(ventas_cliente_en_categoria)
        if cantidad > max_ventas_categoria:
            max_ventas_categoria = cantidad
            id_cliente_top_categoria = cliente.client_id

    # --- C.9: Número de clientes que superan un gasto mínimo (Mínimo: 500€) ---
    lista_clientes_max_gasto = []
    for cliente in coleccion_clientes.clients:
        gasto = coleccion_ventas.total_amount_by_client(cliente.client_id)
        if gasto > 500.0:
            lista_clientes_max_gasto.append(cliente.name)

    # --- C.10: Ventas acumuladas mes a mes ---
    df_ventas_acumulado = df_ventas.copy()
    df_ventas_acumulado["date"] = pd.to_datetime(df_ventas_acumulado["date"])
    df_ventas_acumulado["mes"] = df_ventas_acumulado["date"].dt.to_period("M")
    
    ventas_mensuales = df_ventas_acumulado.groupby("mes")["amount"].sum()
    
    dic_mensual = {}
    for mes, total in ventas_mensuales.items():
        dic_mensual[str(mes)] =  round(float(total), 2)

    # 4. ESTRUCTURACIÓN Y EXPORTACIÓN DEL INFORME JSON
    estructura_final = {
        "summary": {
            "total_clients": int(total_clientes),
            "total_sales": int(total_ventas),
            "total_revenue":  round(float(suma_ingresos_totales), 2)
        },
        "clients": lista_clientes,
        "top_client_by_country": cliente_por_pais,
        "sales_by_category": categorias,
        "high_spending_clients": lista_clientes_max_gasto,
        "monthly_sales": dic_mensual
    }

    # Guardamos el archivo output_report.json
    ruta_salida = "output_report.json"
    with open(ruta_salida, "w", encoding="utf-8") as fichero:
        json.dump(estructura_final, fichero, indent=2, ensure_ascii=False)
    
    return estructura_final

if __name__ == "__main__":
    generate_report()