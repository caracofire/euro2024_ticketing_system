import requests
import json
from difflib import get_close_matches

class Equipo:
    """
    Clase que representa un equipo participante en el torneo.

    Attributes:
    - id (int): Identificador único del equipo.
    - nombre (str): Nombre del equipo.
    - codigo_fifa (str): Código FIFA del equipo.
    - grupo (str): Grupo al que pertenece el equipo.
    """
    def __init__(self, id, nombre, codigo_fifa, grupo):
        self.id = id
        self.nombre = nombre
        self.codigo_fifa = codigo_fifa
        self.grupo = grupo

    def to_dict(self):
        """
        Método para convertir el objeto Equipo a un diccionario.

        Returns:
        dict: Diccionario con los atributos del equipo.
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'codigo_fifa': self.codigo_fifa,
            'grupo': self.grupo
        }

    @classmethod
    def from_dict(cls, data):
        """
        Método de clase para crear un objeto Equipo a partir de un diccionario.

        Args:
        - data (dict): Diccionario con los datos del equipo.

        Returns:
        Equipo: Objeto Equipo creado desde el diccionario.
        """
        return cls(data['id'], data['nombre'], data['codigo_fifa'], data['grupo'])

class Estadio:
    """
    Clase que representa un estadio donde se llevará a cabo un partido.

    Attributes:
    - id (int): Identificador único del estadio.
    - nombre (str): Nombre del estadio.
    - ubicacion (str): Ubicación del estadio.
    - capacidad (int): Capacidad del estadio.
    - latitud (float): Latitud geográfica del estadio (opcional).
    - longitud (float): Longitud geográfica del estadio (opcional).
    """
    def __init__(self, id, nombre, ubicacion, capacidad, latitud=None, longitud=None):
        self.id = id
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.capacidad = capacidad
        self.latitud = latitud
        self.longitud = longitud

    def to_dict(self):
        """
        Método para convertir el objeto Estadio a un diccionario.

        Returns:
        dict: Diccionario con los atributos del estadio.
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'ubicacion': self.ubicacion,
            'capacidad': self.capacidad,
            'latitud': self.latitud,
            'longitud': self.longitud
        }

    @classmethod
    def from_dict(cls, data):
        """
        Método de clase para crear un objeto Estadio a partir de un diccionario.

        Args:
        - data (dict): Diccionario con los datos del estadio.

        Returns:
        Estadio: Objeto Estadio creado desde el diccionario.
        """
        return cls(data['id'], data['nombre'], data['ubicacion'], data['capacidad'], data.get('latitud'), data.get('longitud'))

class Partido:
    """
    Clase que representa un partido entre dos equipos en un estadio y fecha específicos.

    Attributes:
    - id (int): Identificador único del partido.
    - number (int): Número de partido.
    - equipo_local (Equipo): Objeto Equipo que representa al equipo local.
    - equipo_visitante (Equipo): Objeto Equipo que representa al equipo visitante.
    - fecha_hora (str): Fecha y hora del partido.
    - grupo (str): Grupo al que pertenece el partido.
    - estadio (Estadio): Objeto Estadio donde se llevará a cabo el partido.
    """
    def __init__(self, id, number, equipo_local, equipo_visitante, fecha_hora, grupo, estadio):
        self.id = id
        self.number = number
        self.equipo_local = equipo_local
        self.equipo_visitante = equipo_visitante
        self.fecha_hora = fecha_hora
        self.grupo = grupo
        self.estadio = estadio

    def to_dict(self):
        """
        Método para convertir el objeto Partido a un diccionario.

        Returns:
        dict: Diccionario con los atributos del partido.
        """
        return {
            'id': self.id,
            'number': self.number,
            'equipo_local': self.equipo_local.to_dict(),
            'equipo_visitante': self.equipo_visitante.to_dict(),
            'fecha_hora': self.fecha_hora,
            'grupo': self.grupo,
            'estadio': self.estadio.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        """
        Método de clase para crear un objeto Partido a partir de un diccionario.

        Args:
        - data (dict): Diccionario con los datos del partido.

        Returns:
        Partido: Objeto Partido creado desde el diccionario.
        """
        equipo_local = Equipo.from_dict(data['equipo_local'])
        equipo_visitante = Equipo.from_dict(data['equipo_visitante'])
        estadio = Estadio.from_dict(data['estadio'])
        return cls(data['id'], data['number'], equipo_local, equipo_visitante, data['fecha_hora'], data['grupo'], estadio)

class MatchManagement:
    """
    Clase para gestionar la carga, almacenamiento y búsqueda de partidos, equipos y estadios.

    Attributes:
    - equipos (list): Lista de objetos Equipo.
    - estadios (list): Lista de objetos Estadio.
    - partidos (list): Lista de objetos Partido.
    """
    def __init__(self):
        self.equipos = []
        self.estadios = []
        self.partidos = []

    def cargar_equipos(self, url):
        """
        Método para cargar datos de equipos desde una URL.

        Args:
        - url (str): URL de la API que devuelve datos de equipos en formato JSON.
        """
        response = requests.get(url)
        equipos_data = response.json()
        for equipo in equipos_data:
            nuevo_equipo = Equipo(equipo['id'], equipo['name'], equipo['code'], equipo['group'])
            self.equipos.append(nuevo_equipo)

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

    def cargar_partidos(self, url):
        """
        Método para cargar datos de partidos desde una URL.

        Args:
        - url (str): URL de la API que devuelve datos de partidos en formato JSON.
        """
        response = requests.get(url)
        partidos_data = response.json()
        for partido in partidos_data:
            equipo_local = next((e for e in self.equipos if e.id == partido['home']['id']), None)
            equipo_visitante = next((e for e in self.equipos if e.id == partido['away']['id']), None)
            estadio = next((e for e in self.estadios if e.id == partido['stadium_id']), None)
            if equipo_local and equipo_visitante and estadio:
                nuevo_partido = Partido(
                    partido['id'],
                    partido['number'],
                    equipo_local,
                    equipo_visitante,
                    partido['date'],
                    partido['group'],
                    estadio
                )
                self.partidos.append(nuevo_partido)

    def guardar_datos(self, archivo):
        """
        Método para guardar los datos de equipos, estadios y partidos en un archivo JSON.

        Args:
        - archivo (str): Nombre del archivo donde se guardarán los datos.
        """
        data = {
            'equipos': [equipo.to_dict() for equipo in self.equipos],
            'estadios': [estadio.to_dict() for estadio in self.estadios],
            'partidos': [partido.to_dict() for partido in self.partidos]
        }
        with open(archivo, 'w') as file:
            json.dump(data, file, indent=4)

    def cargar_datos(self, archivo):
        """
        Método para cargar los datos de equipos, estadios y partidos desde un archivo JSON.

        Args:
        - archivo (str): Nombre del archivo desde donde se cargarán los datos.
        """
        with open(archivo, 'r') as file:
            data = json.load(file)
            self.equipos = [Equipo.from_dict(e) for e in data['equipos']]
            self.estadios = [Estadio.from_dict(e) for e in data['estadios']]
            self.partidos = [Partido.from_dict(p) for p in data['partidos']]

    def buscar_partidos_por_pais(self, codigo_fifa):
        """
        Método para buscar partidos por código FIFA de un equipo.

        Args:
        - codigo_fifa (str): Código FIFA del equipo.

        Returns:
        list: Lista de objetos Partido que coinciden con el código FIFA proporcionado.
        """
        coincidencias_exactas = [p for p in self.partidos if p.equipo_local.codigo_fifa == codigo_fifa or p.equipo_visitante.codigo_fifa == codigo_fifa]
        codigos_fifa = [e.codigo_fifa for e in self.equipos]
        coincidencias_cercanas = get_close_matches(codigo_fifa, codigos_fifa)
        return coincidencias_exactas + [p for p in self.partidos if (p.equipo_local.codigo_fifa in coincidencias_cercanas or p.equipo_visitante.codigo_fifa in coincidencias_cercanas) and p not in coincidencias_exactas]

    def buscar_partidos_por_estadio(self, nombre_estadio):
        """
        Método para buscar partidos por nombre de estadio.

        Args:
        - nombre_estadio (str): Nombre del estadio.

        Returns:
        list: Lista de objetos Partido que coinciden con el nombre del estadio proporcionado.
        """
        nombre_estadio = nombre_estadio.lower()
        coincidencias_exactas = [p for p in self.partidos if nombre_estadio in p.estadio.nombre.lower()]
        nombres_estadios = [e.nombre.lower() for e in self.estadios]
        coincidencias_cercanas = get_close_matches(nombre_estadio, nombres_estadios)
        return coincidencias_exactas + [p for p in self.partidos if p.estadio.nombre.lower() in coincidencias_cercanas and p not in coincidencias_exactas]

    def buscar_partidos_por_fecha(self, fecha):
        """
        Método para buscar partidos por fecha y hora.

        Args:
        - fecha (str): Fecha y hora del partido.

        Returns:
        list: Lista de objetos Partido que coinciden con la fecha y hora proporcionadas.
        """
        coincidencias_exactas = [p for p in self.partidos if p.fecha_hora == fecha]
        fechas = [p.fecha_hora for p in self.partidos]
        coincidencias_cercanas = get_close_matches(fecha, fechas)
        return coincidencias_exactas + [p for p in self.partidos if p.fecha_hora in coincidencias_cercanas and p not in coincidencias_exactas]

    def mostrar_partidos(self):
        """
        Método para imprimir en consola la lista de partidos cargados.
        """
        for i, partido in enumerate(self.partidos):
            print(f"{i + 1}. {partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre} en {partido.estadio.nombre} el {partido.fecha_hora}")
