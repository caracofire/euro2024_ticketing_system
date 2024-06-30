Sistema de Gestión Eurocup 2024 - README
Este sistema integral permite gestionar la venta de entradas, la asistencia a partidos, las ventas en restaurantes y las estadísticas asociadas al torneo Eurocup 2024.

Requisitos
Python 3.x: Asegúrate de tener instalada una versión reciente de Python.
Librerías:
requests: Para realizar peticiones HTTP a las APIs de datos.
json: Para trabajar con datos en formato JSON.
matplotlib: Para generar gráficos de estadísticas.
tkinter: Para la interfaz gráfica de usuario (si se utiliza).
difflib: Para encontrar coincidencias aproximadas en las búsquedas.
unidecode: Para manejar caracteres Unicode en las búsquedas.
APIs de Datos: El sistema espera que los datos de equipos, estadios y partidos estén disponibles en las siguientes URLs (o similares):
Equipos: "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json"
Estadios: "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json"
Partidos: "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json"
Restaurantes: "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json" (los datos de restaurantes están dentro de los estadios)
Archivos de Datos (Opcionales): Si existen, el sistema cargará datos previamente guardados de los siguientes archivos:
partidos.json
ventas.txt
asistencia.txt
restaurantes.json
Instrucciones de Uso
Clonar el Repositorio:

Bash
git clone <URL_DEL_REPOSITORIO>
Usa el código con precaución.
content_copy
Instalar Dependencias:

Bash
pip install requests matplotlib
Usa el código con precaución.
content_copy
Ejecutar el Sistema:

Bash
python main.py
Usa el código con precaución.
content_copy
Navegar por el Menú:

Gestión de Partidos y Estadios:
Ver la lista de partidos.
Buscar partidos por país, estadio o fecha.
Venta de Entradas:
Comprar entradas, seleccionando partido, tipo y asiento.
Gestión de Asistencia:
Validar boletos ingresando su código.
Gestión de Restaurantes:
Ver la lista de restaurantes.
Buscar restaurantes por nombre.
Ver los productos de un restaurante.
Venta en Restaurantes:
Realizar compras en restaurantes.
Indicadores de Gestión (Estadísticas):
Ver estadísticas generales, por país o por estadio (requiere datos de ventas y asistencia).
Ver Entradas Vendidas:
Mostrar un listado de las entradas vendidas.
Cargar/Guardar Datos:
Cargar datos desde las APIs o archivos locales.
Guardar datos en archivos locales.
Notas Adicionales
El sistema guardará automáticamente los datos en archivos locales después de cada venta o validación de boleto.
Asegúrate de tener conexión a internet para cargar los datos desde las APIs.
Si los archivos de datos locales no existen, el sistema los creará al guardar datos por primera vez.
¡Disfruta de la Eurocup 2024 y aprovecha al máximo este sistema de gestión!
