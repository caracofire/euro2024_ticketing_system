import json
import matplotlib.pyplot as plt
from collections import defaultdict
from modules.match_management import MatchManagement
from modules.ticket_sales import TicketSales
from modules.restaurant_sales import RestaurantSales

class Estadisticas:
    """
    Clase que gestiona las estadísticas relacionadas con los partidos, ventas de boletos y ventas de restaurante.

    Atributos:
        gestor_partidos (MatchManagement): El gestor de partidos.
        sistema_ventas (TicketSales): El sistema de ventas de boletos.
        sistema_restaurante (RestaurantSales): El sistema de ventas del restaurante.
    """
    def __init__(self, gestor_partidos, sistema_ventas, sistema_restaurante):
        self.gestor_partidos = gestor_partidos
        self.sistema_ventas = sistema_ventas
        self.sistema_restaurante = sistema_restaurante

    def promedio_gasto_vip(self):
        total_gasto = 0
        total_vip = 0
        for venta in self.sistema_restaurante.ventas_restaurante:
            total_gasto += venta.calcular_total()['total']
            total_vip += 1
        return total_gasto / total_vip if total_vip > 0 else 0

    def asistencia_partidos(self):
        asistencia = defaultdict(int)
        for venta in self.sistema_ventas.entradas_vendidas:
            asistencia[venta.partido] += 1
        return sorted(asistencia.items(), key=lambda x: x[1], reverse=True)

    def partido_con_mayor_asistencia(self):
        asistencia = self.asistencia_partidos()
        return asistencia[0] if asistencia else None

    def partido_con_mayor_boletos_vendidos(self):
        return self.partido_con_mayor_asistencia()

    def top_productos_mas_vendidos(self):
        productos_vendidos = defaultdict(int)
        for venta in self.sistema_restaurante.ventas_restaurante:
            for producto in venta.productos:
                productos_vendidos[producto.nombre] += producto.cantidad
        return sorted(productos_vendidos.items(), key=lambda x: x[1], reverse=True)[:3]

    def top_clientes(self):
        clientes = defaultdict(int)
        for venta in self.sistema_ventas.entradas_vendidas:
            clientes[venta.cliente.nombre] += 1
        return sorted(clientes.items(), key=lambda x: x[1], reverse=True)[:3]

    def mostrar_grafico_asistencia(self):
        partidos = [f"{p.equipo_local.nombre} vs {p.equipo_visitante.nombre}" for p, _ in self.asistencia_partidos()]
        asistencias = [a for _, a in self.asistencia_partidos()]

        plt.figure(figsize=(10, 5))
        plt.barh(partidos, asistencias, color='skyblue')
        plt.xlabel('Asistencia')
        plt.ylabel('Partidos')
        plt.title('Asistencia a los partidos')
        plt.gca().invert_yaxis()
        plt.show()

    def mostrar_grafico_top_productos(self):
        top_productos = self.top_productos_mas_vendidos()
        productos = [producto for producto, _ in top_productos]
        cantidades = [cantidad for _, cantidad in top_productos]

        plt.figure(figsize=(10, 5))
        plt.bar(productos, cantidades, color='green')
        plt.xlabel('Productos')
        plt.ylabel('Cantidad Vendida')
        plt.title('Top 3 Productos Más Vendidos en el Restaurante')
        plt.show()

    def mostrar_grafico_top_clientes(self):
        top_clientes = self.top_clientes()
        clientes = [cliente for cliente, _ in top_clientes]
        cantidades = [cantidad for _, cantidad in top_clientes]

        plt.figure(figsize=(10, 5))
        plt.bar(clientes, cantidades, color='orange')
        plt.xlabel('Clientes')
        plt.ylabel('Cantidad de Boletos Comprados')
        plt.title('Top 3 Clientes que Más Compraron Boletos')
        plt.show()

    def guardar_datos(self, archivo):
        data = {
            'promedio_gasto_vip': self.promedio_gasto_vip(),
            'asistencia_partidos': self.asistencia_partidos(),
            'partido_con_mayor_asistencia': self.partido_con_mayor_asistencia(),
            'partido_con_mayor_boletos_vendidos': self.partido_con_mayor_boletos_vendidos(),
            'top_productos_mas_vendidos': self.top_productos_mas_vendidos(),
            'top_clientes': self.top_clientes()
        }
        with open(archivo, 'w') as file:
            json.dump(data, file, indent=4)

    def cargar_datos(self, archivo):
        with open(archivo, 'r') as file:
            data = json.load(file)
            self.promedio_gasto_vip = data['promedio_gasto_vip']
            self.asistencia_partidos = data['asistencia_partidos']
            self.partido_con_mayor_asistencia = data['partido_con_mayor_asistencia']
            self.partido_con_mayor_boletos_vendidos = data['partido_con_mayor_boletos_vendidos']
            self.top_productos_mas_vendidos = data['top_productos_mas_vendidos']
            self.top_clientes = data['top_clientes']

if __name__ == "__main__":
    gestor_partidos = MatchManagement()
    gestor_partidos.cargar_equipos("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json")
    gestor_partidos.cargar_estadios("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json")
    gestor_partidos.cargar_partidos("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json")

    sistema_ventas = TicketSales()
    sistema_restaurante = RestaurantSales()

    estadisticas = Estadisticas(gestor_partidos, sistema_ventas, sistema_restaurante)

    print("Promedio de gasto VIP:", estadisticas.promedio_gasto_vip())
    print("Partido con mayor asistencia:", estadisticas.partido_con_mayor_asistencia())
    print("Partido con mayor boletos vendidos:", estadisticas.partido_con_mayor_boletos_vendidos())
    print("Top 3 productos más vendidos:", estadisticas.top_productos_mas_vendidos())
    print("Top 3 clientes:", estadisticas.top_clientes())

    estadisticas.mostrar_grafico_asistencia()
    estadisticas.mostrar_grafico_top_productos()
    estadisticas.mostrar_grafico_top_clientes()

    # Guardar datos
    estadisticas.guardar_datos("estadisticas.txt")

    # Cargar datos
    estadisticas_nuevo = Estadisticas(gestor_partidos, sistema_ventas, sistema_restaurante)
    estadisticas_nuevo.cargar_datos("estadisticas.txt")
    print("Datos de estadísticas cargados:")
    print("Promedio de gasto VIP:", estadisticas_nuevo.promedio_gasto_vip())
    print("Partido con mayor asistencia:", estadisticas_nuevo.partido_con_mayor_asistencia())
    print("Partido con mayor boletos vendidos:", estadisticas_nuevo.partido_con_mayor_boletos_vendidos())
    print("Top 3 productos más vendidos:", estadisticas_nuevo.top_productos_mas_vendidos())
    print("Top 3 clientes:", estadisticas_nuevo.top_clientes())
