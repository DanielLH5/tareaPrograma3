import unicodedata
import pickle
import random
import wikipedia
import google.generativeai as genai

##################################################
#Funciones de manipulación de datos
##################################################

def grabaTxt(archivoTxt,datos):
    """
    Funcionamiento:
    Guarda los datos proporcionados en un archivo de texto, sobrescribiendo el contenido anterior.
    Entradas:
    - archivoTxt (str): Nombre del archivo de texto a escribir.
    - datos (str): El texto que se escribirá en el archivo.
    Salidas:
    - NA
    """
    try:
        f=open(archivoTxt,"w")
        f.write(datos)
        f.close()
    except:
        print(f"Error al leer el archivo: {archivoTxt}")
    return

def guardarPickle(nombreArchivo, datos):
    """
    Funcionamiento:
    Guarda datos serializados en un archivo usando pickle.
    Entradas:
    - nombreArchivo (str): Nombre del archivo donde guardar (ej. "inventarioAnimales.pkl").
    - datos (cualquier objeto): Datos a guardar.
    Salidas:
    - NA
    """
    try:
        with open(nombreArchivo, "wb") as f:
            pickle.dump(datos, f)
    except Exception as e:
        print(f"Error al guardar con pickle: {e}")
        
def cargarPickle(nombreArchivo):
    try:
        with open(nombreArchivo, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error al cargar con pickle: {e}")
        return []

##################################################
# 8. Búsqueda por orden
##################################################

def formatoHTMLBPO(tituloDieta, matrizDatos):
    """
    Funcionamiento:
    Genera una plantilla HTML que contiene una tabla con información sobre animales
    pertenecientes a una dieta específica (por ejemplo, hervíboros, carnívoros u omnívoros).
    Cada fila incluye un número de orden, código, nombre común, nombre científico y una imagen.
    Entradas:
    - tituloDieta (str): título descriptivo de la dieta (por ejemplo: "Carnívoros").
    - matrizDatos (list): lista de tuplas con los datos de cada animal en el formato:
    (id, nombre_col, nombre_cient, url_foto)
    Salidas:
    - contenido (str): código HTML generado como string listo para ser guardado en un archivo.
    """
    contenido = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Animales {tituloDieta}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
        }}
        .container {{
            border: 2px solid #24465a;
            border-radius: 30px;
            padding: 10px 15px;
            width: 850px;
            margin: 20px auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        caption {{
            caption-side: top;
            font-weight: normal;
            font-size: 1.2em;
            margin-bottom: 10px;
        }}
        th, td {{
            border: 1px solid black;
            padding: 5px;
            text-align: center;
        }}
        th {{
            font-weight: bold;
            font-style: italic;
        }}
        td img {{
            max-width: 100px;
        }}
        /* Alternar colores de filas */
        tbody tr:nth-child(odd) {{
            background-color: #f2f2f2;
        }}
        tbody tr:nth-child(even) {{
            background-color: #ffffff;
        }}
    </style>
</head>
<body>
    <div class="container">
        <table>
            <caption>Animales <span>{tituloDieta}</span></caption>
            <thead>
                <tr>
                    <th>#</th>
                    <th><em>Código</em></th>
                    <th><em>Nombre común</em></th>
                    <th><em>Nombre Científico</em></th>
                    <th><em>Foto</em></th>
                </tr>
            </thead>
            <tbody>
"""
    for i, info in enumerate(matrizDatos, start=1):
        contenido += f"""
                <tr>
                    <td>{i}</td>  <!-- Enumeración en la primera columna -->
                    <td>{info[0]}</td>
                    <td>{info[1]}</td>
                    <td>{info[2]}</td>
                    <td><img src="{info[3]}" alt="{info[1]}"></td>
                </tr>
"""
    contenido += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""
    return contenido

def obtenerMatrizDatosBPO(listaPorDieta, documento):
    """
    Funcionamiento:
    Extrae de un documento (lista de objetos animal) los datos necesarios de los animales
    que están incluidos en una lista por dieta específica. Extrae: ID, nombre común, nombre
    científico y URL de la imagen.
    Entradas:
    - listaPorDieta (list): lista de nombres comunes de animales filtrados por dieta.
    - documento (list): lista de objetos (presumiblemente de tipo 'Animal') con sus métodos internos.
    Salidas:
    - matrizDatos (list): lista de tuplas con la información completa:
    (id, nombre común, nombre científico, url)
    """
    matrizDatos = []
    for nombreAnimal in listaPorDieta:
        for datoAnimal in documento:
            nombreColoquial = datoAnimal.mostrarNombres()[0]
            if nombreColoquial == nombreAnimal:
                id = datoAnimal.mostrarId()
                nombreCientifico = datoAnimal.mostrarNombres()[1]
                foto = datoAnimal.mostrarUrl()
                informacionCadaAnimal = (id, nombreColoquial, nombreCientifico, foto)
                matrizDatos.append(informacionCadaAnimal)
    return matrizDatos

##################################################
# 5. Crear HTML
##################################################

def ordenarPorPeso(listaNombrePeso): # Este es el método de ordenamineto por burbuja.
    """
    Funcionamiento:
    Ordena una lista de tuplas (peso, nombre) de forma descendente usando el algoritmo de burbuja,
    comparando por el valor del peso.
    Entradas:
    - listaNombrePeso (list[tuple[float, str]]): Lista de tuplas donde cada una contiene el peso y nombre del animal.
    Salidas:
    - list[tuple[float, str]]: Lista ordenada de mayor a menor peso.
    """
    n = len(listaNombrePeso)
    for i in range(n):
        for j in range(0, n - i - 1):
            # Comparar pesos (primer elemento de la tupla)
            if listaNombrePeso[j][0] < listaNombrePeso[j + 1][0]:
                # Intercambiar posiciones si está desordenado
                listaNombrePeso[j], listaNombrePeso[j + 1] = listaNombrePeso[j + 1], listaNombrePeso[j]
    print(listaNombrePeso)
    return listaNombrePeso

def obtenerPesoPorDieta(tipoAnimal, documento):
    """
    Funcionamiento:
    Busca los pesos de los animales en el inventario que coincidan con los nombres proporcionados y 
    devuelve una lista de tuplas (peso, nombre) ordenada de forma descendente por peso.
    Entradas:
    - tipoAnimal (list[str]): Lista de nombres coloquiales de los animales de una dieta específica.
    - documento (list[objeto]): Lista de objetos del inventario cargado.
    Salidas:
    - list[tuple[float, str]]: Lista ordenada de tuplas (peso, nombre).
    """
    listaNombrePeso = []
    for nombreAnimal in tipoAnimal:
        for datoAnimal in documento:
            nombres = datoAnimal.mostrarNombres()
            nombreColoquial = nombres[0]
            if nombreColoquial == nombreAnimal:
                info = datoAnimal.mostrarInformacion()
                peso = info[3]
                informacionCadaAnimal = (peso, nombreColoquial)
                listaNombrePeso.append(informacionCadaAnimal)
    return ordenarPorPeso(listaNombrePeso)

def obtenerAnimalesPorDieta(dieta, documento): #"h", "c" o "o"
    """
    Funcionamiento:
    Filtra y devuelve una lista de nombres coloquiales de animales que tienen una dieta específica.
    Entradas:
    - dieta (str): Tipo de dieta ('h' = herbívoro, 'c' = carnívoro, 'o' = omnívoro).
    - documento (list[objeto]): Lista de objetos del inventario cargado.
    Salidas:
    - tuple: (listaAnimalesDieta, documento)
        - listaAnimalesDieta (list[str]): Lista de nombres coloquiales de animales con la dieta indicada.
        - documento (list[objeto]): Documento original (retornado sin cambios).
    """
    listaAnimalesDieta = []
    for animal in documento:
        info = animal.mostrarInformacion()
        if info[2] == dieta:
            nombres = animal.mostrarNombres()
            listaAnimalesDieta.append(nombres[0]) #Nombre coloquial.
    return (listaAnimalesDieta, documento)
    
def formatoHTMLCategoria(categoria, listaNombrePeso):
    """
    Funcionamiento:
    Genera el bloque HTML con filas de una tabla para una categoría de dieta específica 
    (herbívoros, carnívoros u omnívoros), usando la lista de tuplas (peso, nombre).
    Entradas:
    - categoria (str): Nombre de la categoría ("Herbívoro", "Carnívoro", "Omnívoro").
    - listaNombrePeso (list[tuple[float, str]]): Lista de tuplas con peso y nombre.
    Salidas:
    - str: Bloque de texto HTML con las filas correspondientes a esa categoría.
    """
    filas = len(listaNombrePeso)
    formato = f"""<!-- {categoria} -->
        <tr><td class="orden" rowspan="{filas}">{categoria}</td><td>{listaNombrePeso[0][0]}</td><td>{listaNombrePeso[0][1]}</td></tr>\n"""  
    for i in range(1, filas):
        nuevaLinea = f"\t<tr><td>{listaNombrePeso[i][0]}</td><td>{listaNombrePeso[i][1]}</td></tr>\n"
        formato += nuevaLinea
    return formato
    
def formatoHTMLPesoDieta(herNombrePeso, carNombrePeso, omnNombrePeso):
    """
    Funcionamiento:
    Une los bloques de HTML de las tres categorías (herbívoros, carnívoros y omnívoros) y arma
    una página HTML completa con estilos y una tabla que muestra peso y nombre común.
    Entradas:
    - herNombrePeso (list[tuple[float, str]]): Lista de herbívoros.
    - carNombrePeso (list[tuple[float, str]]): Lista de carnívoros.
    - omnNombrePeso (list[tuple[float, str]]): Lista de omnívoros.
    Salidas:
    - str: Texto HTML completo como string.
    """
    formatoHer = formatoHTMLCategoria("Herbívoro", herNombrePeso)
    formatoCar = formatoHTMLCategoria("Carnívoro", carNombrePeso)
    formatoOmn = formatoHTMLCategoria("Omnívoro", omnNombrePeso)
    formato = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Estadística por Orden</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 30px;
        }}
        h2 {{
            text-align: center;
        }}
        table {{
            border-collapse: collapse;
            width: 60%;
            margin: auto;
        }}
        th, td {{
            border: 1px solid #333;
            padding: 8px;
            text-align: center;
        }}
        tr:nth-child(even) {{
            background-color: #ffffff;
        }}
        tr:nth-child(odd) {{
            background-color: #e9e9e9;
        }}
        .orden {{
            background-color: #f0f0f0;
            font-weight: bold;
        }}
        .totales {{
            margin-top: 20px;
            text-align: center;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h2>Estadística por Orden</h2>
    <table>
        <tr>
            <th>Orden</th>
            <th>Peso</th>
            <th>Nombre común</th>
        </tr>
        {formatoHer}
        {formatoCar}
        {formatoOmn}
    </table>
    <div class="totales">
        Total de Herbívoros: {len(herNombrePeso)}<br>
        Total de Carnívoros: {len(carNombrePeso)}<br>
        Total de Omnívoros: {len(omnNombrePeso)}
    </div>
</body>
</html>"""
    return formato

##################################################
# 4. Estadística por estado
##################################################

def obtenerPorcentajes(estadisticas):
    """
    Funcionamiento:
    Calcula el porcentaje de animales en cada uno de los cinco estados con respecto a un total de 20 animales.
    Redondea cada porcentaje a un decimal.
    Entradas:
    - estadisticas (tuple[int]): Tupla con 5 valores enteros representando la cantidad de animales en cada estado:
    (vivo, enfermo, en translado, muerto en museo, muerto)
    Salidas:
    - tuple[float]: Porcentajes de cada estado en el mismo orden, redondeados a un decimal.
    """
    pVivo = (estadisticas[0] / 20) * 100
    pVivo = round(pVivo, 1)
    pEnfermo = (estadisticas[1] / 20) * 100
    pEnfermo = round(pEnfermo, 1)
    pTranslado = (estadisticas[2] / 20) * 100
    pTranslado = round(pTranslado, 1)
    pMuertoEnMuseo = (estadisticas[3] / 20) * 100
    pMuertoEnMuseo = round(pMuertoEnMuseo, 1)
    pMuerto = (estadisticas[4] / 20) * 100
    pMuerto = round(pMuerto, 1)
    return (pVivo, pEnfermo, pTranslado, pMuertoEnMuseo, pMuerto)

def obtenerCantidadPorEstado(estado, estados):
    """
    Funcionamiento:
    Cuenta cuántos animales se encuentran en un estado específico dentro de una lista de estados.
    Entradas:
    - estado (int): Número que representa un estado específico (1 = vivo, 2 = enfermo...).
    - estados (list[tuple]): Lista de tuplas donde el primer valor indica el estado del animal.
    Salidas:
    - contador (int): Cantidad de animales que están en el estado especificado.
    """
    contador = 0
    for info in estados:
        if info[0] == estado:
            contador += 1
    return contador

def contarEstadosAnimales(estados):
    """
    Funcionamiento:
    Cuenta cuántos animales hay en cada uno de los 5 estados posibles utilizando la función obtenerCantidadPorEstado.
    Entradas:
    - estados (list[tuple]): Lista de tuplas donde el primer elemento representa el estado de cada animal.
    Salidas:
    - tuple[int]: Tupla con la cantidad de animales por estado en el siguiente orden:
    (vivo, enfermo, en translado, muerto en museo, muerto)
    """
    vivo = obtenerCantidadPorEstado(1, estados)
    enfermo = obtenerCantidadPorEstado(2, estados)
    translado = obtenerCantidadPorEstado(3, estados)
    muertoEnMuseo = obtenerCantidadPorEstado(4, estados)
    muerto = obtenerCantidadPorEstado(5, estados)
    return (vivo, enfermo, translado, muertoEnMuseo, muerto)

##################################################
# 2. Crear inventario
##################################################

def seleccionarAnimalesAleatorios(rutaArchivo, cantidad=20): #Lee cada linea del txt y toma 20 animales
    with open(rutaArchivo, "r", encoding="utf-8") as f:
        nombres = f.read().splitlines()
    seleccionados = random.sample(nombres, cantidad)
    print("Animales seleccionados para buscar en Wikipedia:") #Mostrar temporalmente los animales seleccionados en terminal
    for nombre in seleccionados:
        print(nombre)
    return seleccionados

def generarId(nombre, consecutivo): #Generar id único del nombre
    nombre = nombre.lower()
    primera = nombre[0]
    ultima = nombre[-1]
    return f"{primera}{ultima}{consecutivo:02d}"

def obtenerDatosAnimalWikipedia(nombreComun):
    try:
        wikipedia.set_lang("es")
        page = wikipedia.page(nombreComun)
        resumen = wikipedia.summary(nombreComun, sentences=2).lower()
        imagenValida = ""
        for img in page.images: #Recorre todas las URLs de imágenes que encontró Wikipedia
            #Filtra para evitar imágenes que sean logos o imágenes en formato .svg
            if not any(excluido in img for excluido in ["commons-logo", "wikimedia-logo", ".svg"]):
                imagenValida = img
                break
        tipo = "omnívoro" #De base que sea omnívoro
        if "herbívor" in resumen:
            tipo = "herbívoro"
        elif "carnívor" in resumen:
            tipo = "carnívoro"
        return nombreComun, tipo, imagenValida
    except:
        return "desconocido", "omnívoro", ""

def obtenerDatosAnimal(nombreComun, model):
    nombreCientifico, tipoAlimentacion, urlImagen = obtenerDatosAnimalWikipedia(nombreComun) #Buscar de wikipedia
    if urlImagen:
        return nombreCientifico, tipoAlimentacion, urlImagen
    try:#En caso de que Wikipedia falle, se piden los datos a gemini
        #Prompt a utilizar con Gemini
        prompt = (
            f"Dame el nombre científico, el tipo de alimentación (solo responde 'carnívoro', 'herbívoro' u 'omnívoro') "
            f"y una URL de imagen del animal '{nombreComun}'. No uses viñetas ni encabezados. Responde separado por saltos de línea.")
        response = model.generate_content(prompt)
        datos = response.text.strip().split("\n")
        nombreCientifico = datos[0].strip()
        tipoAlimentacion = datos[1].strip().lower()
        urlImagen = datos[2].strip()
        return nombreCientifico, tipoAlimentacion, urlImagen
    except Exception as e:
        print(f"Error al obtener datos de {nombreComun} con Gemini: {e}")
        return "desconocido", "omnívoro", ""

##################################################
# 1. Obtener lista
##################################################

def peticionGeminiAnimales(numeroTotales, contenido):
    """
    Funcionamiento:
    Genera un mensaje estructurado para enviar a la API de Gemini. Este mensaje solicita una lista
    específica de animales únicos y detallados, exclusivamente basada en información de Wikipedia.
    Entradas:
    - numeroTotales (int): Número de animales que se desea generar.
    - contenido (str): Texto resumido extraído de Wikipedia sobre animales.
    Salidas:
    - mensaje (str): Prompt listo para enviar al modelo de lenguaje.
    """
    mensaje = (
        f"Genérame una lista de únicamnete {numeroTotales} animales distintos, asegurándote de que cada uno sea específico y único." +
        f"Usa exclusivamente los animales mencionados en Wikipedia." +
        "Utiliza únicamente nombres comunes detallados (por ejemplo: 'Águila real', 'Zorro ártico', 'Delfín nariz de botella', 'Mariposa monarca')." +
        "No uses nombres genéricos como 'Águila', 'Zorro' o 'Mariposa'." +
        "Devuélvelos estrictamente en este formato: solo el nombre común, sin numeración ni negritas ni texto adicional." +
        "Ejemplo de formato: León africano")
    return mensaje

def obtenerTextoAniLimpio(lineas):
    """
    Funcionamiento:
    Procesa una lista de líneas de texto, eliminando espacios en blanco innecesarios y omitiendo líneas vacías.
    Une el contenido limpio en un solo string separado por saltos de línea.
    Entradas:
    - lineas (list[str]): Lista de líneas de texto.
    Salidas:
    - resultadoLimpio (str): Texto depurado y unido, una línea por animal.
    """
    listaAnimales = []
    for linea in lineas:
        lineaLimpia = linea.strip()
        if lineaLimpia != "": #Verificar que la línea no esté vacía
            listaAnimales.append(lineaLimpia) #Agregar la línea limpia a la lista
    resultadoLimpio = "\n".join(listaAnimales)
    print(resultadoLimpio)
    return resultadoLimpio

def limpiarTexto(texto): #Permite limpiar texto, permitiendo tildes y caracteres únicamente disponibles en el español.
    """
    Funcionamiento:
    Limpia un texto eliminando caracteres especiales o con tildes, convirtiéndolos a su forma básica (ASCII).
    Esto permite un procesamiento posterior más limpio y compatible.
    Entradas:
    - texto (str): Texto original, posiblemente con tildes o símbolos del idioma español.
    Salidas:
    - textoAscii (str): Texto limpio solo con caracteres ASCII.
    """
    textoNorm = unicodedata.normalize('NFKD', texto) #Convierte letras con tildes o símbolos especiales a una forma descompuesta.
    textoAscii = textoNorm.encode('ascii', 'ignore').decode('ascii') #Elimina caracteres que no admite ASCII y .decode("ascii") devuelve texto plano.
    return textoAscii

##################################################
# Clase Animal
##################################################

class Animal:
    """
    Funcionamiento: La clase animal.
    Entradas: NA.
    Salidas: El init, las funciones de asignar y mostrar, indicar datos.
    """
    def __init__(self):
        self.id=""
        self.nombres=("","")
        self.url=""
        self.informacion=[int,int,str,float]
        return
    def asignarId(self,pId):   
        self.id=pId
        return 
    def asignarNombres(self,pNombres):
        self.nombres=pNombres
        return
    def asignarUrl(self,pUrl):
        self.url=pUrl
        return 
    def asignarInformacion(self,pInformacion):
        self.informacion=pInformacion
        return 
    def mostrarId(self):
        return self.id
    def mostrarNombres(self):
        return self.nombres
    def mostrarUrl(self):
        return self.url
    def mostrarInformacion(self):
        return self.informacion
    def indicarDatos(self):
        return self.id,self.nombres,self.url,self.informacion
    
##################################################
# Nombre de archivos
##################################################    

inventarioPkl = "inventario.pkl"
animalesTxt = "animales.txt"