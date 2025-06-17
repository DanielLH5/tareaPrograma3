import unicodedata
import pickle
import random

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
    return f"{primera}{ultima}{consecutivo:02d}" #Devuelve primer, última letra y consecutivo con dos dígitos

def obtenerDatosAnimalGemini(model, nombreComun):
    #Prompt utilizado para generar los datos del animal
    prompt = (
        f"Dame el nombre científico, el tipo de alimentación (solo responde 'carnívoro', 'herbívoro' u 'omnívoro') "
        f"y una URL de imagen del animal '{nombreComun}'. No uses viñetas ni encabezados. Responde separado por saltos de línea.")
    try:
        response = model.generate_content(prompt)
        datos = response.text.strip().split("\n")
        nombreCientifico = datos[0].strip()
        tipoAlimentacion = datos[1].strip().lower()
        urlImagen = datos[2].strip()
        return nombreCientifico, tipoAlimentacion, urlImagen
    except Exception as e:
        print(f"Error al obtener datos de {nombreComun}: {e}") #Puede dar error por límite de cuotas de Gemini
        return "desconocido", "omnívoro", ""

##################################################
# 1. Obtener lista
##################################################

def peticionGeminiAnimales(numeroTotales, contenido):
    mensaje = (
        f"Genérame una lista de únicamnete {numeroTotales} animales distintos, asegurándote de que cada uno sea específico y único." +
        f"Usa exclusivamente los animales mencionados en el siguiente texto de Wikipedia: {contenido}" +
        "Utiliza únicamente nombres comunes detallados (por ejemplo: 'Águila real', 'Zorro ártico', 'Delfín nariz de botella', 'Mariposa monarca')." +
        "No uses nombres genéricos como 'Águila', 'Zorro' o 'Mariposa'." +
        "Devuélvelos estrictamente en este formato: solo el nombre común, sin numeración ni negritas ni texto adicional." +
        "Ejemplo de formato: León africano")
    return mensaje

def obtenerTextoAniLimpio(lineas):
    listaAnimales = []
    for linea in lineas:
        lineaLimpia = linea.strip()
        if lineaLimpia != "": #Verificar que la línea no esté vacía
            listaAnimales.append(lineaLimpia) #Agregar la línea limpia a la lista
    resultadoLimpio = "\n".join(listaAnimales)
    print(resultadoLimpio)
    return resultadoLimpio

def limpiarTexto(texto): #Permite limpiar texto, permitiendo tildes y caracteres únicamente disponibles en el español.
    textoNorm = unicodedata.normalize('NFKD', texto) #Convierte letras con tildes o símbolos especiales a una forma descompuesta.
    textoAscii = textoNorm.encode('ascii', 'ignore').decode('ascii') #Elimina caracteres que no admite ASCII y .decode('ascii') devuelve texto plano
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