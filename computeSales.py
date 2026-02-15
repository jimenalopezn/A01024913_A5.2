"""
Programa para calcular el costo total de ventas desde archivos JSON.

Este código lee un archivo de catálogo de precios y un archivo de registro
de ventas, calcula el total considerando posibles errores en los datos,
y reporta el tiempo de ejecución. Cumple con el estándar de PEP 8.
"""

import json
import sys
import time


def load_file(filename):
    """
    Carga y devuelve el contenido de un archivo JSON.

    Args:
        filename (str): Ruta del archivo a leer.

    Returns:
        list: Datos del archivo o None si hay error.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no fue encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo '{filename}' no tiene un formato válido.")
        return None


def create_price_catalogue(product_list):
    """
    Convierte la lista de productos en un diccionario para búsqueda rápida.

    Args:
        product_list (list): Lista de diccionarios con datos de productos.

    Returns:
        dict: Diccionario con {nombre_producto: precio}.
    """
    price_dict = {}
    for item in product_list:
        title = item.get("title")
        price = item.get("price")
        if title and isinstance(price, (int, float)):
            price_dict[title] = price
    return price_dict


def func_total_cost(price_dict, sales_list):
    """
    Calcula el costo total de las ventas.

    Args:
        price_dict (dict): Catálogo de precios.
        sales_list (list): Lista de ventas.

    Returns:
        float: Costo total acumulado.
    """
    total_cost = 0.0

    for sale in sales_list:
        product_name = sale.get("Product")
        quantity = sale.get("Quantity")

        # Validación básica de datos
        if not product_name:
            print(f"Advertencia: Venta sin nombre de producto: {sale}")
            continue

        if not isinstance(quantity, (int, float)):
            print(f"Advertencia: Cantidad inválida para '{product_name}': "
                  f"{quantity}")
            continue

        # Buscar precio
        if product_name in price_dict:
            price = price_dict[product_name]
            total_cost += price * quantity
        else:
            print(f"Advertencia: Producto '{product_name}' no encontrado "
                  "en el catálogo.")

    return total_cost


def main():
    """Función principal para ejecutar el cálculo de ventas."""
    if len(sys.argv) != 3:
        print("Uso correcto: python computeSales.py priceCatalogue.json "
              "salesRecord.json")
        sys.exit(1)

    price_file = sys.argv[1]
    sales_file = sys.argv[2]

    start_time = time.time()

    # Cargar datos
    product_data = load_file(price_file)
    sales_data = load_file(sales_file)

    if product_data is None or sales_data is None:
        sys.exit(1)

    # Procesar
    price_catalogue = create_price_catalogue(product_data)
    total_sales = func_total_cost(price_catalogue, sales_data)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Formatear resultados
    output_lines = [
        "Resultados de ventas",
        "-" * 30,
        f"Archivo de ventas : {sales_file}",
        f"Total de ventas   : {total_sales:,.2f}",
        f"Tiempo de ejecución: {elapsed_time:.4f} segundos",
        "-" * 30
    ]
    result_text = "\n".join(output_lines)

    # 1. Imprimir en consola
    print("\n" + result_text)

    # 2. Guardar en archivo (append para guardar historial)
    with open("SalesResults.txt", "a", encoding='utf-8') as result_file:
        result_file.write(result_text + "\n\n")


if __name__ == "__main__":
    main()
