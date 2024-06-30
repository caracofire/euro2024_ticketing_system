import json
from modules.ticket_sales import Entrada

class Boleto:
    """
    Clase que representa un boleto.

    Atributos:
        codigo (str): El código único del boleto.
        entrada (Entrada): La entrada asociada al boleto.
        utilizado (bool): Indica si el boleto ha sido utilizado.
    """

    def __init__(self, codigo, entrada):
        """
        Inicializa una instancia de la clase Boleto.

        Args:
            codigo (str): El código único del boleto.
            entrada (Entrada): La entrada asociada al boleto.
        """
        self.codigo = codigo
        self.entrada = entrada
        self.utilizado = False

    def to_dict(self):
        """
        Convierte el boleto a un diccionario.

        Returns:
            dict: Un diccionario que representa el boleto.
        """
        return {
            'codigo': self.codigo,
            'entrada': self.entrada.to_dict(),
            'utilizado': self.utilizado
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Boleto a partir de un diccionario.

        Args:
            data (dict): Un diccionario con los datos del boleto.

        Returns:
            Boleto: Una instancia de la clase Boleto.
        """
        entrada = Entrada.from_dict(data['entrada'])
        boleto = cls(data['codigo'], entrada)
        boleto.utilizado = data['utilizado']
        return boleto

class AttendanceManagement:
    """
    Clase que gestiona la asistencia mediante boletos.

    Atributos:
        boletos (list): Lista de boletos generados.
    """

    def __init__(self):
        """
        Inicializa una instancia de la clase AttendanceManagement.
        """
        self.boletos = []

    def generar_boleto(self, entrada):
        """
        Genera un nuevo boleto para una entrada dada.

        Args:
            entrada (Entrada): La entrada para la cual se genera el boleto.

        Returns:
            Boleto: El boleto generado.
        """
        codigo = self.generar_codigo_unico()
        nuevo_boleto = Boleto(codigo, entrada)
        self.boletos.append(nuevo_boleto)
        return nuevo_boleto

    def generar_codigo_unico(self):
        """
        Genera un código único para un boleto.

        Returns:
            str: Un código único.
        """
        from uuid import uuid4
        return str(uuid4())

    def validar_boleto(self, codigo):
        """
        Valida un boleto dado su código.

        Args:
            codigo (str): El código del boleto a validar.

        Returns:
            tuple: Un tuple con un booleano indicando si el boleto es válido y un mensaje.
        """
        boleto = next((b for b in self.boletos if b.codigo == codigo), None)
        if boleto is None:
            return False, "Boleto no válido."
        if boleto.utilizado:
            return False, "Boleto ya utilizado."
        boleto.utilizado = True
        return True, "Boleto válido. Entrada permitida."

    def guardar_datos(self, archivo):
        """
        Guarda los datos de los boletos en un archivo.

        Args:
            archivo (str): La ruta del archivo donde se guardarán los datos.
        """
        data = {
            'boletos': [boleto.to_dict() for boleto in self.boletos]
        }
        with open(archivo, 'w') as file:
            json.dump(data, file, indent=4)

    def cargar_datos(self, archivo):
        """
        Carga los datos de los boletos desde un archivo.

        Args:
            archivo (str): La ruta del archivo desde donde se cargarán los datos.
        """
        with open(archivo, 'r') as file:
            data = json.load(file)
            self.boletos = [Boleto.from_dict(b) for b in data['boletos']]
