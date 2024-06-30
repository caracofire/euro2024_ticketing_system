import json
import requests
from difflib import get_close_matches
import unidecode

class Producto:
    """
    Clase que representa un producto en el restaurante.

    Atributos:
        nombre (str): El nombre del producto.
        tipo (str): El tipo del producto (alimento o bebida).
        precio (float): El precio del producto.
        cantidad (int): La cantidad disponible del producto.
        stock (int): El stock disponible del producto.
        adicional (str): Información adicional sobre el producto.
    """
    def __init__(self, nombre, tipo, precio, cantidad, stock, adicional):
        """
        Inicializa una instancia de la clase Producto.

        Args:
            nombre (str): El nombre del producto.
            tipo (str): El tipo del producto.
            precio (float): El precio del producto.
            cantidad (int): La cantidad disponible del producto.
            stock (int): El stock disponible del producto.
            adicional (str): Información adicional sobre el producto.
        """
        self.nombre = nombre
        self.tipo = tipo
        self.precio = precio
        self.cantidad = cantidad
        self.stock = stock
        self.adicional = adicional

    def to_dict(self):
        """
        Convierte el producto a un diccionario.

        Returns:
            dict: Un diccionario que representa el producto.
        """
        return {
            'nombre': self.nombre,
            'tipo': self.tipo,
            'precio': self.precio,
            'cantidad': self.cantidad,
            'stock': self.stock,
            'adicional': self.adicional
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Producto a partir de un diccionario.

        Args:
            data (dict): Un diccionario con los datos del producto.

        Returns:
            Producto: Una instancia de la clase Producto.
        """
        return cls(data['name'], data['adicional'], float(data['price']), data['quantity'], data['stock'], data['adicional'])

class RestaurantManagement:
    """
    Clase que gestiona los productos del restaurante.

    Atributos:
        productos (list): Lista de productos del restaurante.
    """
    def __init__(self):
        """
        Inicializa una instancia de la clase RestaurantManagement.
        """
        self.productos = []
        self.ventas_restaurante = []

    def cargar_productos(self, url):
        """
        Carga los productos desde una URL y los añade a la lista de productos.

        Args:
            url (str): La URL de la cual cargar los productos.
        """
        response = requests.get(url)
        estadios_data = response.json()
        for estadio in estadios_data:
            for restaurante in estadio['restaurants']:
                for producto in restaurante['products']:
                    nuevo_producto = Producto(producto['name'], producto['adicional'], float(producto['price']), producto['quantity'], producto['stock'], producto['adicional'])
                    self.productos.append(nuevo_producto)

    def buscar_productos_por_nombre(self, nombre):
        """
        Busca productos por nombre.

        Args:
            nombre (str): El nombre del producto a buscar.

        Returns:
            list: Lista de productos cuyo nombre contiene la cadena buscada.
        """
        nombre = unidecode.unidecode(nombre.lower())
        coincidencias_exactas = [p for p in self.productos if unidecode.unidecode(p.nombre.lower()).find(nombre) != -1]
        nombres_productos = [unidecode.unidecode(p.nombre.lower()) for p in self.productos]
        coincidencias_cercanas = get_close_matches(nombre, nombres_productos)
        return coincidencias_exactas + [p for p in self.productos if unidecode.unidecode(p.nombre.lower()) in coincidencias_cercanas and p not in coincidencias_exactas]

    def buscar_productos_por_tipo(self, tipo):
        """
        Busca productos por tipo.

        Args:
            tipo (str): El tipo de producto a buscar (plate, bebida, alcoholic, non-alcoholic).

        Returns:
            list: Lista de productos que coinciden con el tipo buscado.
        """
        tipo = tipo.lower()
        return [p for p in self.productos if p.tipo.lower() == tipo]

    def buscar_productos_por_rango_precio(self, precio_min, precio_max):
        """
        Busca productos dentro de un rango de precios.

        Args:
            precio_min (float): El precio mínimo.
            precio_max (float): El precio máximo.

        Returns:
            list: Lista de productos cuyo precio está dentro del rango especificado.
        """
        rango_flexible = 0.10  # 10% de flexibilidad en el rango de precios
        return [p for p in self.productos if precio_min * (1 - rango_flexible) <= p.precio <= precio_max * (1 + rango_flexible)]

    def buscar_productos_por_stock(self, stock_min, stock_max):
        """
        Busca productos dentro de un rango de stock.

        Args:
            stock_min (int): El stock mínimo.
            stock_max (int): El stock máximo.

        Returns:
            list: Lista de productos cuyo stock está dentro del rango especificado.
        """
        return [p for p in self.productos if stock_min <= p.stock <= stock_max]

    def guardar_datos(self, archivo):
        """
        Guarda los datos de los productos en un archivo.

        Args:
            archivo (str): La ruta del archivo donde se guardarán los datos.
        """
        data = {
            'productos': [producto.to_dict() for producto in self.productos]
        }
        with open(archivo, 'w') as file:
            json.dump(data, file, indent=4)

    def cargar_datos(self, archivo):
        """
        Carga los datos de los productos desde un archivo.

        Args:
            archivo (str): La ruta del archivo desde donde se cargarán los datos.
        """
        with open(archivo, 'r') as file:
            data = json.load(file)
            self.productos = [Producto.from_dict(p) for p in data['productos']]

    def registrar_venta(self, venta):
        """
        Registra una venta de productos en el restaurante.

        Args:
            venta (VentaRestaurante): La venta a registrar.
        """
        self.ventas_restaurante.append(venta)
