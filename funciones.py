import unicodedata

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