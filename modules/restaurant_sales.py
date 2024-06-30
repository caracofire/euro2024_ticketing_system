import json
from modules.ticket_sales import Cliente
from modules.restaurant_management import Producto

class VentaRestaurante:
    """
    Clase que representa una venta en el restaurante.

    Atributos:
        cliente (Cliente): El cliente que realiza la compra.
        productos (list): Lista de productos comprados.
    """
    def __init__(self, cliente, productos):
        """
        Inicializa una instancia de la clase VentaRestaurante.

        Args:
            cliente (Cliente): El cliente que realiza la compra.
            productos (list): Lista de productos comprados.
        """
        self.cliente = cliente
        self.productos = productos

    @property
    def total(self):
        """
        Calcula el total de la venta, incluyendo descuento e IVA.

        Returns:
            float: El total de la venta.
        """
        return sum(producto.precio * producto.cantidad for producto in self.productos)

    def calcular_total(self):
        """
        Calcula el total de la venta, incluyendo descuento e IVA.

        Returns:
            dict: Un diccionario con el desglose del total de la venta (subtotal, descuento, IVA, total).
        """
        subtotal = sum(producto.precio for producto in self.productos)
        descuento = 0.15 if self.es_perfecto(int(self.cliente.cedula)) else 0
        total_descuento = subtotal * descuento
        iva = (subtotal - total_descuento) * 0.16
        total = subtotal - total_descuento + iva
        return {
            'subtotal': subtotal,
            'descuento': total_descuento,
            'iva': iva,
            'total': total
        }

    def es_perfecto(self, n):
        """
        Verifica si un número es perfecto.

        Args:
            n (int): El número a verificar.

        Returns:
            bool: True si el número es perfecto, False en caso contrario.
        """
        if n < 2:
            return False
        suma = 1
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                suma += i
                if i != n // i:
                    suma += n // i
        return suma == n

    def to_dict(self):
        """
        Convierte la venta a un diccionario.

        Returns:
            dict: Un diccionario que representa la venta.
        """
        return {
            'cliente': self.cliente.to_dict(),
            'productos': [producto.to_dict() for producto in self.productos]
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de VentaRestaurante a partir de un diccionario.

        Args:
            data (dict): Un diccionario con los datos de la venta.

        Returns:
            VentaRestaurante: Una instancia de la clase VentaRestaurante.
        """
        cliente = Cliente.from_dict(data['cliente'])
        productos = [Producto.from_dict(p) for p in data['productos']]
        return cls(cliente, productos)

class RestaurantSales:
    """
    Clase que gestiona las ventas del restaurante y los clientes VIP.

    Atributos:
        ventas_restaurante (list): Lista de ventas realizadas en el restaurante.
        clientes_vip (list): Lista de clientes VIP.
    """
    def __init__(self):
        """
        Inicializa una instancia de la clase RestaurantSales.
        """
        self.ventas_restaurante = []
        self.clientes_vip = []

    def realizar_venta(self, cliente, productos):
        """
        Realiza una venta y la agrega a la lista de ventas.

        Args:
            cliente (Cliente): El cliente que realiza la compra.
            productos (list): Lista de productos comprados.

        Returns:
            tuple: Una tupla que contiene la venta realizada y el total de la venta.
        """
        if cliente not in self.clientes_vip:
            self.clientes_vip.append(cliente)
        nueva_venta = VentaRestaurante(cliente, productos)
        total = nueva_venta.calcular_total()
        self.ventas_restaurante.append(nueva_venta)
        return nueva_venta, total

    def guardar_datos(self, archivo):
        """
        Guarda los datos de las ventas y los clientes VIP en un archivo.

        Args:
            archivo (str): La ruta del archivo donde se guardarán los datos.
        """
        data = {
            'ventas_restaurante': [venta.to_dict() for venta in self.ventas_restaurante],
            'clientes_vip': [cliente.to_dict() for cliente in self.clientes_vip]
        }
        with open(archivo, 'w') as file:
            json.dump(data, file, indent=4)

    def cargar_datos(self, archivo):
        """
        Carga los datos de las ventas y los clientes VIP desde un archivo.

        Args:
            archivo (str): La ruta del archivo desde donde se cargarán los datos.
        """
        with open(archivo, 'r') as file:
            data = json.load(file)
            self.ventas_restaurante = [VentaRestaurante.from_dict(v) for v in data['ventas_restaurante']]
            self.clientes_vip = [Cliente.from_dict(c) for c in data['clientes_vip']]
