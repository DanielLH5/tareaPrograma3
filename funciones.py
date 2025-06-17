import unicodedata
import pickle

def limpiarTexto(texto):
    textoNorm = unicodedata.normalize('NFKD', texto)
    textoAscii = textoNorm.encode('ascii', 'ignore').decode('ascii')
    return textoAscii

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

#Clase Animal
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