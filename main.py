import json
from modules.match_management import MatchManagement
from modules.ticket_sales import TicketSales, Cliente
from modules.attendance_management import AttendanceManagement
from modules.restaurant_management import RestaurantManagement, Producto
from modules.restaurant_sales import RestaurantSales, VentaRestaurante
from modules.statistics import Estadisticas
from modules.mapa_estadios import MapaEstadios
import os
import unidecode

def menu_principal():
    """
    Muestra el menú principal del sistema.
    """
    print("\nMenú Principal")
    print("1. Gestión de Partidos y Estadios")
    print("2. Venta de Entradas")
    print("3. Gestión de Asistencia")
    print("4. Gestión de Restaurantes")
    print("5. Venta en Restaurantes")
    print("6. Indicadores de Gestión (Estadísticas)")
    print("7. Ver Entradas Vendidas")
    print("8. Cargar Datos")
    print("9. Guardar Datos")
    print("10. Salir")

def gestion_partidos(gestor_partidos):
    """
    Función para gestionar los partidos y estadios.

    Args:
    - gestor_partidos (MatchManagement): Instancia del gestor de partidos.
    """
    while True:
        print("\nGestión de Partidos y Estadios")
        print("1. Mostrar Partidos")
        print("2. Buscar Partidos por País")
        print("3. Buscar Partidos por Estadio")
        print("4. Buscar Partidos por Fecha")
        print("5. Volver al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            gestor_partidos.mostrar_partidos()
        elif opcion == "2":
            codigo_fifa = input("Ingrese el código FIFA del país: ")
            partidos = gestor_partidos.buscar_partidos_por_pais(codigo_fifa)
            for partido in partidos:
                print(f"{partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre} en {partido.estadio.nombre} el {partido.fecha_hora}")
        elif opcion == "3":
            nombre_estadio = input("Ingrese el nombre del estadio: ")
            partidos = gestor_partidos.buscar_partidos_por_estadio(nombre_estadio)
            for partido in partidos:
                print(f"{partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre} en {partido.estadio.nombre} el {partido.fecha_hora}")
        elif opcion == "4":
            fecha = input("Ingrese la fecha (AAAA-MM-DD): ")
            partidos = gestor_partidos.buscar_partidos_por_fecha(fecha)
            for partido in partidos:
                print(f"{partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre} en {partido.estadio.nombre} el {partido.fecha_hora}")
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")

def mostrar_partidos(gestor_partidos):
    """
    Muestra la lista de partidos disponibles.

    Args:
    - gestor_partidos (MatchManagement): Instancia del gestor de partidos.

    Returns:
    - list: Lista de objetos de partido.
    """
    partidos = gestor_partidos.partidos
    for i, partido in enumerate(partidos):
        print(f"{i + 1}. {partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre} en {partido.estadio.nombre} el {partido.fecha_hora}")
    return partidos

def seleccionar_tipo_entrada():
    """
    Permite al usuario seleccionar el tipo de entrada.

    Returns:
    - str: Tipo de entrada seleccionada ('General' o 'VIP').
    """
    while True:
        tipo = input("Seleccione el tipo de entrada (G)eneral o (V)IP: ").upper()
        if tipo in ['G', 'V']:
            return 'General' if tipo == 'G' else 'VIP'
        else:
            print("Opción no válida. Intente de nuevo.")

def venta_entradas(sistema_ventas, gestor_partidos, mapa_estadios):
    """
    Función para la venta de entradas.

    Args:
    - sistema_ventas (TicketSales): Instancia del sistema de ventas de entradas.
    - gestor_partidos (MatchManagement): Instancia del gestor de partidos.
    - mapa_estadios (MapaEstadios): Instancia del mapa de estadios.
    """
    while True:
        print("\nVenta de Entradas")
        print("1. Comprar Entrada")
        print("2. Volver al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese su nombre y apellido: ")
            cedula = input("Ingrese su cédula: ")
            edad = int(input("Ingrese su edad: "))
            if edad < 18:
                print("Lo siento, no puede comprar entradas si es menor de 18 años.")
                continue

            partidos = mostrar_partidos(gestor_partidos)
            partido_idx = int(input("Seleccione el número del partido que desea ver: ")) - 1

            if partido_idx < 0 or partido_idx >= len(partidos):
                print("Número de partido inválido. Intente de nuevo.")
                continue

            partido = partidos[partido_idx]

            tipo_entrada = seleccionar_tipo_entrada()
            asiento = mapa_estadios.seleccionar_asiento(partido.estadio.id, tipo_entrada)
            if asiento is None:
                print("Selección de asiento cancelada.")
                continue

            fila, columna = asiento
            asiento_str = f"Fila {fila + 1}, Columna {columna + 1}"

            cliente = Cliente(nombre, cedula, edad)
            entrada, precio = sistema_ventas.vender_entrada(cliente, partido, tipo_entrada, asiento_str)

            print(f"\nVenta Exitosa")
            print(f"Cliente: {cliente.nombre}")
            print(f"Partido: {partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre} en {partido.estadio.nombre} el {partido.fecha_hora}")
            print(f"Asiento: {asiento_str}")
            print(f"Precio: {precio['total']} (Subtotal: {precio['subtotal']}, Descuento: {precio['descuento']}, IVA: {precio['iva']})")

            sistema_ventas.guardar_datos("ventas.txt")
        elif opcion == "2":
            break
        else:
            print("Opción no válida.")

def gestion_asistencia(sistema_asistencia, sistema_ventas):
    """
    Función para gestionar la asistencia.

    Args:
    - sistema_asistencia (AttendanceManagement): Instancia del sistema de asistencia.
    - sistema_ventas (TicketSales): Instancia del sistema de ventas de entradas.
    """
    while True:
        print("\nGestión de Asistencia")
        print("1. Validar Boleto")
        print("2. Volver al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            codigo_boleto = input("Ingrese el código del boleto para validar: ")
            valido, mensaje = sistema_asistencia.validar_boleto(codigo_boleto)
            print(mensaje)

            sistema_asistencia.guardar_datos("asistencia.txt")
        elif opcion == "2":
            break
        else:
            print("Opción no válida.")

def mostrar_lista_navegable(lista, titulo="Lista", elementos_por_pagina=10):
    """
    Muestra una lista de manera paginada y navegable.

    Args:
    - lista (list): Lista de elementos a mostrar.
    - titulo (str): Título para mostrar encima de la lista (default: "Lista").
    - elementos_por_pagina (int): Número de elementos a mostrar por página (default: 10).
    """
    total_elementos = len(lista)
    if total_elementos == 0:
        print("\nNo hay elementos para mostrar.")
        return

    paginas = (total_elementos + elementos_por_pagina - 1) // elementos_por_pagina
    pagina_actual = 0

    while True:
        inicio = pagina_actual * elementos_por_pagina
        fin = inicio + elementos_por_pagina
        print(f"\n{titulo} (Página {pagina_actual + 1} de {paginas})")
        for i, elemento in enumerate(lista[inicio:fin], inicio + 1):
            print(f"{i + 1}. {elemento}")

        if paginas == 1:
            break

        print("\nNavegar: (S)iguiente, (A)nterior, (E)xit")
        opcion = input("Seleccione una opción: ").lower()
        if opcion == 's' and pagina_actual < paginas - 1:
            pagina_actual += 1
        elif opcion == 'a' and pagina_actual > 0:
            pagina_actual -= 1
        elif opcion == 'e':
            break
        else:
            print("Opción no válida.")

def gestion_restaurantes(sistema_restaurante):
    """
    Función para gestionar los restaurantes.

    Args:
    - sistema_restaurante (RestaurantManagement): Instancia del sistema de gestión de restaurantes.
    """
    while True:
        print("\nGestión de Restaurantes")
        print("1. Mostrar Restaurantes")
        print("2. Buscar Restaurantes por Nombre")
        print("3. Mostrar Productos de un Restaurante")
        print("4. Volver al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            restaurantes = sistema_restaurante.mostrar_restaurantes()
            mostrar_lista_navegable(restaurantes, "Restaurantes")
        elif opcion == "2":
            nombre_restaurante = input("Ingrese el nombre del restaurante: ")
            restaurantes = sistema_restaurante.buscar_restaurantes_por_nombre(nombre_restaurante)
            mostrar_lista_navegable(restaurantes, f"Restaurantes con Nombre '{nombre_restaurante}'")
        elif opcion == "3":
            nombre_restaurante = input("Ingrese el nombre del restaurante: ")
            productos = sistema_restaurante.mostrar_productos_restaurante(nombre_restaurante)
            mostrar_lista_navegable(productos, f"Productos de {nombre_restaurante}")
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")

def venta_restaurantes(sistema_ventas, sistema_restaurante):
    """
    Función para la venta en restaurantes.

    Args:
    - sistema_ventas (TicketSales): Instancia del sistema de ventas de entradas.
    - sistema_restaurante (RestaurantManagement): Instancia del sistema de gestión de restaurantes.
    """
    while True:
        print("\nVenta en Restaurantes")
        print("1. Realizar Venta en Restaurante")
        print("2. Volver al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese su nombre y apellido: ")
            cedula = input("Ingrese su cédula: ")
            edad = int(input("Ingrese su edad: "))
            if edad < 18:
                print("Lo siento, no puede realizar ventas si es menor de 18 años.")
                continue

            restaurantes = sistema_restaurante.mostrar_restaurantes()
            restaurante_idx = int(input("Seleccione el número del restaurante donde desea comprar: ")) - 1

            if restaurante_idx < 0 or restaurante_idx >= len(restaurantes):
                print("Número de restaurante inválido. Intente de nuevo.")
                continue

            restaurante = restaurantes[restaurante_idx]
            productos = sistema_restaurante.mostrar_productos_restaurante(restaurante.nombre)
            mostrar_lista_navegable(productos, f"Productos de {restaurante.nombre}")

            producto_idx = int(input("Seleccione el número del producto que desea comprar: ")) - 1
            if producto_idx < 0 or producto_idx >= len(productos):
                print("Número de producto inválido. Intente de nuevo.")
                continue

            producto = productos[producto_idx]

            cliente = Cliente(nombre, cedula, edad)
            cantidad = int(input("Ingrese la cantidad que desea comprar: "))
            venta = VentaRestaurante(cliente, restaurante, producto, cantidad)
            total = sistema_ventas.realizar_venta_restaurante(venta)

            print(f"\nVenta Exitosa")
            print(f"Cliente: {cliente.nombre}")
            print(f"Restaurante: {restaurante.nombre}")
            print(f"Producto: {producto.nombre}")
            print(f"Cantidad: {cantidad}")
            print(f"Total: {total}")

            sistema_ventas.guardar_datos("ventas.txt")
        elif opcion == "2":
            break
        else:
            print("Opción no válida.")

def indicadores_gestion(estadisticas, gestor_partidos):
    """
    Función para mostrar indicadores de gestión.

    Args:
    - estadisticas (Estadisticas): Instancia del sistema de estadísticas.
    - gestor_partidos (MatchManagement): Instancia del gestor de partidos.
    """
    while True:
        print("\nIndicadores de Gestión")
        print("1. Mostrar Estadísticas Generales")
        print("2. Mostrar Estadísticas por País")
        print("3. Mostrar Estadísticas por Estadio")
        print("4. Volver al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            estadisticas.mostrar_estadisticas_generales(gestor_partidos)
        elif opcion == "2":
            codigo_fifa = input("Ingrese el código FIFA del país: ")
            estadisticas.mostrar_estadisticas_por_pais(gestor_partidos, codigo_fifa)
        elif opcion == "3":
            nombre_estadio = input("Ingrese el nombre del estadio: ")
            estadisticas.mostrar_estadisticas_por_estadio(gestor_partidos, nombre_estadio)
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")

def main():
    """
    Función principal que ejecuta el sistema de gestión de venta de entradas para el Eurocup 2024.
    """
    gestor_partidos = MatchManagement()
    sistema_ventas = TicketSales()
    sistema_asistencia = AttendanceManagement()
    sistema_restaurante = RestaurantManagement()
    estadisticas = Estadisticas()
    mapa_estadios = MapaEstadios()

    if os.path.isfile("partidos.json"):
        gestor_partidos.cargar_datos("partidos.json")
    if os.path.isfile("ventas.txt"):
        sistema_ventas.cargar_datos("ventas.txt")
    if os.path.isfile("asistencia.txt"):
        sistema_asistencia.cargar_datos("asistencia.txt")
    if os.path.isfile("restaurantes.json"):
        sistema_restaurante.cargar_datos("restaurantes.json")

    while True:
        menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            gestion_partidos(gestor_partidos)
        elif opcion == "2":
            venta_entradas(sistema_ventas, gestor_partidos, mapa_estadios)
        elif opcion == "3":
            gestion_asistencia(sistema_asistencia, sistema_ventas)
        elif opcion == "4":
            gestion_restaurantes(sistema_restaurante)
        elif opcion == "5":
            venta_restaurantes(sistema_ventas, sistema_restaurante)
        elif opcion == "6":
            indicadores_gestion(estadisticas, gestor_partidos)
        elif opcion == "7":
            sistema_ventas.mostrar_entradas_vendidas()
        elif opcion == "8":
            gestor_partidos.cargar_datos("partidos.json")
            sistema_ventas.cargar_datos("ventas.txt")
            sistema_asistencia.cargar_datos("asistencia.txt")
            sistema_restaurante.cargar_datos("restaurantes.json")
        elif opcion == "9":
            gestor_partidos.guardar_datos("partidos.json")
            sistema_ventas.guardar_datos("ventas.txt")
            sistema_asistencia.guardar_datos("asistencia.txt")
            sistema_restaurante.guardar_datos("restaurantes.json")
        elif opcion == "10":
            print("Gracias por usar el sistema de gestión Eurocup 2024. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
