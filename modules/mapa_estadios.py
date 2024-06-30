import requests
import tkinter as tk
from tkinter import messagebox, ttk

class Estadio:
    """
    Clase que representa un estadio.

    Attributes:
    - id (int): Identificador único del estadio.
    - name (str): Nombre del estadio.
    - city (str): Ciudad donde está ubicado el estadio.
    - capacity (int): Capacidad total de asientos del estadio.
    - latitud (float, optional): Latitud geográfica del estadio.
    - longitud (float, optional): Longitud geográfica del estadio.
    """
    def __init__(self, id, name, city, capacity, latitud=None, longitud=None):
        self.id = id
        self.name = name
        self.city = city
        self.capacity = capacity
        self.latitud = latitud
        self.longitud = longitud

    def to_dict(self):
        """
        Método para convertir el objeto Estadio a un diccionario.

        Returns:
        dict: Diccionario con los atributos del estadio.
        """
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "capacity": self.capacity,
            "latitud": self.latitud,
            "longitud": self.longitud
        }

class MapaEstadios:
    """
    Clase que gestiona la carga de estadios y la selección de asientos en un estadio específico.

    Attributes:
    - estadios (list): Lista de objetos Estadio cargados.
    """
    def __init__(self):
        self.estadios = []

    def cargar_estadios(self, url):
        """
        Método para cargar datos de estadios desde una URL.

        Args:
        - url (str): URL de la API que devuelve datos de estadios en formato JSON.
        """
        response = requests.get(url)
        estadios_data = response.json()
        for estadio in estadios_data:
            nuevo_estadio = Estadio(
                estadio['id'],
                estadio['name'],
                estadio['city'],
                estadio['capacity'],
                estadio.get('latitud', None),
                estadio.get('longitud', None)
            )
            self.estadios.append(nuevo_estadio)

    def seleccionar_asiento(self, estadio_id, tipo_entrada):
        """
        Método para abrir una interfaz gráfica donde el usuario puede seleccionar un asiento en un estadio.

        Args:
        - estadio_id (int): ID del estadio donde se seleccionará el asiento.
        - tipo_entrada (str): Tipo de entrada ("VIP" o "Regular").

        Returns:
        list or None: Coordenadas del asiento seleccionado [fila, columna] o None si no se seleccionó ningún asiento.
        """
        estadio = next((e for e in self.estadios if e.id == estadio_id), None)
        if not estadio:
            return None

        asientos_disponibles = estadio.capacity[0] if tipo_entrada == "VIP" else estadio.capacity[1]

        def on_asiento_click(fila, columna):
            nonlocal root
            result = messagebox.askyesno("Confirmar Asiento", f"¿Desea seleccionar el asiento Fila {fila+1}, Columna {columna+1}?")
            if result:
                selected_seat[0], selected_seat[1] = fila, columna
                root.quit()

        root = tk.Tk()
        root.title(f"Seleccionar Asiento - {tipo_entrada}")

        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_x = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        selected_seat = [None, None]

        # calcula tamano de boton
        button_width = 5
        button_height = 2

        for fila in range(10):
            tk.Label(inner_frame, text=f"F{fila+1}").grid(row=fila, column=0, sticky='e')
            for columna in range(asientos_disponibles):
                text = f"{columna+1}"
                btn = tk.Button(inner_frame, text=text, width=button_width, height=button_height, command=lambda f=fila, c=columna: on_asiento_click(f, c))
                btn.grid(row=fila, column=columna+1)

        tk.Label(inner_frame, text="").grid(row=10, column=0)  

        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        root.mainloop()

        return selected_seat if selected_seat[0] is not None and selected_seat[1] is not None else None
