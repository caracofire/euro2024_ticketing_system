import json
import tkinter as tk
from tkinter import messagebox
from modules.match_management import Equipo, Estadio, Partido

class Cliente:
    """
    Clase que representa un cliente.

    Attributes:
        nombre (str): Nombre del cliente.
        cedula (str): Número de cédula del cliente.
        edad (int): Edad del cliente.
    """

    def __init__(self, nombre, cedula, edad):
        """
        Inicializa un objeto Cliente con nombre, cédula y edad.

        Args:
            nombre (str): Nombre del cliente.
            cedula (str): Número de cédula del cliente.
            edad (int): Edad del cliente.
        """
        self.nombre = nombre
        self.cedula = cedula
        self.edad = edad

    def to_dict(self):
        """
        Convierte el objeto Cliente a un diccionario serializable.

        Returns:
            dict: Diccionario con los atributos del cliente.
        """
        return {
            'nombre': self.nombre,
            'cedula': self.cedula,
            'edad': self.edad
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crea un objeto Cliente a partir de un diccionario.

        Args:
            data (dict): Diccionario con los datos del cliente.

        Returns:
            Cliente: Objeto Cliente creado a partir del diccionario.
        """
        return cls(data['nombre'], data['cedula'], data['edad'])

class Entrada:
    """
    Clase que representa una entrada vendida para un partido.

    Attributes:
        cliente (Cliente): Cliente que compró la entrada.
        partido (Partido): Partido al cual corresponde la entrada.
        tipo_entrada (str): Tipo de entrada ('General' o 'VIP').
        asiento (tuple): Coordenadas del asiento seleccionado.
    """

    def __init__(self, cliente, partido, tipo_entrada, asiento):
        """
        Inicializa una entrada con el cliente, partido, tipo de entrada y asiento.

        Args:
            cliente (Cliente): Cliente que compra la entrada.
            partido (Partido): Partido al cual corresponde la entrada.
            tipo_entrada (str): Tipo de entrada ('General' o 'VIP').
            asiento (tuple): Coordenadas del asiento seleccionado.
        """
        self.cliente = cliente
        self.partido = partido
        self.tipo_entrada = tipo_entrada
        self.asiento = asiento

    def calcular_precio(self):
        """
        Calcula el precio de la entrada considerando descuentos y IVA.

        Returns:
            dict: Diccionario con los detalles del precio calculado (subtotal, descuento, IVA, total).
        """
        base_price = 35 if self.tipo_entrada == 'General' else 75
        descuento = 0.15 if self.es_numero_perfecto(self.cliente.cedula) else 0
        precio_con_descuento = base_price * (1 - descuento)
        iva = precio_con_descuento * 0.16
        total = precio_con_descuento + iva
        return {
            'subtotal': base_price,
            'descuento': descuento * base_price,
            'iva': iva,
            'total': total
        }

    def es_numero_perfecto(self, n):
        """
        Verifica si un número es perfecto.

        Args:
            n (str): Número a verificar.

        Returns:
            bool: True si el número es perfecto, False en caso contrario.
        """
        n = int(n)
        if n < 2:
            return False
        suma = 1
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                suma += i
                if i != n // i:
                    suma += n // i
        return suma == n

    def to_dict(self):
        """
        Convierte la entrada a un diccionario serializable.

        Returns:
            dict: Diccionario con los atributos de la entrada.
        """
        return {
            'cliente': self.cliente.to_dict(),
            'partido': self.partido.to_dict(),
            'tipo_entrada': self.tipo_entrada,
            'asiento': self.asiento
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crea un objeto Entrada a partir de un diccionario.

        Args:
            data (dict): Diccionario con los datos de la entrada.

        Returns:
            Entrada: Objeto Entrada creado a partir del diccionario.
        """
        cliente = Cliente.from_dict(data['cliente'])
        partido = Partido.from_dict(data['partido'])
        return cls(cliente, partido, data['tipo_entrada'], data['asiento'])

class TicketSales:
    """
    Clase que gestiona la venta de entradas para partidos.

    Attributes:
        entradas_vendidas (list): Lista de entradas vendidas.
    """

    def __init__(self):
        """
        Inicializa un sistema de venta de entradas vacío.
        """
        self.entradas_vendidas = []

    def vender_entrada(self, cliente, partido, tipo_entrada, asiento):
        """
        Vende una entrada para un partido específico.

        Args:
            cliente (Cliente): Cliente que compra la entrada.
            partido (Partido): Partido al cual corresponde la entrada.
            tipo_entrada (str): Tipo de entrada ('General' o 'VIP').
            asiento (tuple): Coordenadas del asiento seleccionado.

        Returns:
            tuple: Objeto Entrada creado y el precio calculado.
        """
        nueva_entrada = Entrada(cliente, partido, tipo_entrada, asiento)
        precio = nueva_entrada.calcular_precio()
        self.entradas_vendidas.append(nueva_entrada)
        return nueva_entrada, precio

    def mostrar_partidos(self, gestor_partidos):
        """
        Muestra los partidos disponibles para la venta de entradas.

        Args:
            gestor_partidos (MatchManagement): Gestor de partidos que contiene la lista de partidos.
        """
        for idx, partido in enumerate(gestor_partidos.partidos):
            print(f"{idx}. {partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre} en {partido.estadio.nombre} el {partido.fecha_hora}")

    def seleccionar_asiento(self, estadio, tipo_entrada):
        """
        Abre una ventana para que el usuario seleccione un asiento.

        Args:
            estadio (Estadio): Estadio donde se realizará el evento.
            tipo_entrada (str): Tipo de entrada ('General' o 'VIP').

        Returns:
            tuple: Coordenadas del asiento seleccionado.
        """
        root = tk.Tk()
        app = SeatSelectionApp(root, estadio, tipo_entrada)
        root.mainloop()
        return app.selected_seat

    def seleccionar_tipo_entrada(self):
        """
        Abre una ventana para que el usuario seleccione el tipo de entrada.

        Returns:
            str: Tipo de entrada seleccionado ('General' o 'VIP').
        """
        root = tk.Tk()
        app = TipoEntradaApp(root)
        root.mainloop()
        return app.tipo_entrada

    def guardar_datos(self, archivo):
        """
        Guarda los datos de las entradas vendidas en un archivo JSON.

        Args:
            archivo (str): Nombre del archivo donde se guardarán los datos.
        """
        data = {
            'entradas_vendidas': [entrada.to_dict() for entrada in self.entradas_vendidas]
        }
        with open(archivo, 'w') as file:
            json.dump(data, file, indent=4)

    def cargar_datos(self, archivo):
        """
        Carga los datos de las entradas vendidas desde un archivo JSON.

        Args:
            archivo (str): Nombre del archivo desde donde se cargarán los datos.
        """
        with open(archivo, 'r') as file:
            data = json.load(file)
            self.entradas_vendidas = [Entrada.from_dict(e) for e in data['entradas_vendidas']]

class TipoEntradaApp:
    """
    Clase que representa la interfaz para seleccionar el tipo de entrada.

    Attributes:
        master (tk.Tk): Ventana principal de la aplicación.
        tipo_entrada (str): Tipo de entrada seleccionado ('General' o 'VIP').
    """

    def __init__(self, master):
        """
        Inicializa la interfaz para seleccionar el tipo de entrada.

        Args:
            master (tk.Tk): Ventana principal de la aplicación.
        """
        self.master = master
        self.master.title("Seleccione Tipo de Entrada")
        self.tipo_entrada = None

        self.general_button = tk.Button(master, text="General", width=20, command=self.select_general)
        self.general_button.pack(pady=10)

        self.vip_button = tk.Button(master, text="VIP", width=20, command=self.select_vip)
        self.vip_button.pack(pady=10)

    def select_general(self):
        """
        Asigna 'General' como el tipo de entrada seleccionado y cierra la ventana.
        """
        self.tipo_entrada = "General"
        self.master.destroy()

    def select_vip(self):
        """
        Asigna 'VIP' como el tipo de entrada seleccionado y cierra la ventana.
        """
        self.tipo_entrada = "VIP"
        self.master.destroy()

class SeatSelectionApp:
    """
    Clase que representa la interfaz para seleccionar un asiento en el estadio.

    Attributes:
        master (tk.Tk): Ventana principal de la aplicación.
        selected_seat (tuple): Coordenadas del asiento seleccionado.
        estadio (Estadio): Estadio donde se realizará el evento.
        tipo_entrada (str): Tipo de entrada ('General' o 'VIP').
    """

    def __init__(self, master, estadio, tipo_entrada):
        """
        Inicializa la interfaz para seleccionar un asiento en el estadio.

        Args:
            master (tk.Tk): Ventana principal de la aplicación.
            estadio (Estadio): Estadio donde se realizará el evento.
            tipo_entrada (str): Tipo de entrada ('General' o 'VIP').
        """
        self.master = master
        self.master.title("Selección de Asientos")
        self.selected_seat = None
        self.estadio = estadio
        self.tipo_entrada = tipo_entrada

        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar_y = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.pack(side="right", fill="y")

        self.scrollbar_x = tk.Scrollbar(self.master, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_x.pack(side="bottom", fill="x")

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", self.on_frame_configure)
        self.create_seat_map()

        self.confirm_button = tk.Button(self.master, text="Confirmar Asiento", command=self.confirm_seat)
        self.confirm_button.pack(pady=10)

    def on_frame_configure(self, event):
        """
        Configura la región de desplazamiento del canvas cuando cambia el tamaño del frame.
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_seat_map(self):
        """
        Crea el mapa de asientos en función del tipo de entrada y capacidad del estadio.
        """
        if self.tipo_entrada == "General":
            filas, columnas = self.estadio.capacity[0] // 10, 10
        else:
            filas, columnas = self.estadio.capacity[1] // 10, 10
        self.seat_buttons = {}

        for i in range(filas):
            for j in range(columnas):
                btn = tk.Button(self.frame, text=f"{i+1}-{j+1}", width=5, height=2, command=lambda i=i, j=j: self.select_seat(i, j))
                btn.grid(row=i, column=j, padx=1, pady=1)
                self.seat_buttons[(i, j)] = btn

    def select_seat(self, i, j):
        """
        Maneja la selección de un asiento cambiando su color y guardando las coordenadas del asiento seleccionado.

        Args:
            i (int): Fila del asiento seleccionado.
            j (int): Columna del asiento seleccionado.
        """
        if self.selected_seat:
            self.seat_buttons[self.selected_seat].config(bg="SystemButtonFace")
        self.selected_seat = (i, j)
        self.seat_buttons[(i, j)].config(bg="blue")

    def confirm_seat(self):
        """
        Confirma la selección del asiento mostrando un mensaje de confirmación o advertencia si no se ha seleccionado ningún asiento.
        """
        if self.selected_seat:
            messagebox.showinfo("Asiento Confirmado", f"Has seleccionado el asiento: {self.selected_seat[0]+1}-{self.selected_seat[1]+1}")
            self.master.destroy()
        else:
            messagebox.showwarning("Sin selección", "Por favor, selecciona un asiento.")
