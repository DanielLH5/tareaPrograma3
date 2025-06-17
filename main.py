import tkinter as tk
import random
#python -m pip install wikipedia
import wikipedia
#python -m pip install google-generativeai
import google.generativeai as genai

from funciones import *

##################################################
# Ventanas Secundarias
##################################################
def ventanaRetroalimentacion(mensaje):
    """
    Funcionamiento: 
    Muestra una ventana con un mensaje de retroalimentación al usuario.
    Entradas: 
    - El mesnaje(str) de retroalimentación.
    Salidas: 
    - Se muestra la ventana de retroalimentación.
    """
    root = tk.Toplevel()
    root.geometry("300x100")
    root.title("Retroalimentación")
    title = tk.Label(root, text=mensaje, padx=10, pady=10)
    title.pack()
    boton = tk.Button(root, text="Aceptar", command=root.destroy)
    boton.pack(pady=10)

def ventanaConfirmacion(mensaje):
    """
    Funcionamiento: 
    Muestra una ventana con un mensaje de confirmación al usuario.
    Entradas: 
    - mensaje (str): El mensaje de confirmación.
    Salidas: 
    - Se muestra la ventana de confirmación.
    """
    root = tk.Toplevel()
    root.geometry("350x100")
    root.title("Confirmación")
    title = tk.Label(root, text=mensaje, padx=10, pady=10)
    title.pack()
    boton = tk.Button(root, text="Aceptar", command=root.destroy)
    boton.pack(pady=10)
    
def ventanaAprobacion(comandoAceptar):
    """
    Funcionamiento: 
    Muestra una ventana que solicita aprobación del usuario. Si el usuario acepta,
    se ejecuta la función proporcionada y se cierra la ventana. Si rechaza, solo se cierra.
    Entradas: 
    - comandoAceptar: Función que se ejecutará si el usuario presiona "Aceptar".
    Salidas: 
    - Se muestra la ventana de aprobación. Puede ejecutar una acción si se acepta.
    """
    root = tk.Toplevel()
    root.geometry("250x150")
    root.title("Aprobación")
    title = tk.Label(root, text="¿Deseas realizar esta acción?", padx=10, pady=10)
    title.pack()
    botonAceptar = tk.Button(root, text="Aceptar", command=lambda: [comandoAceptar(), root.destroy()])
    botonAceptar.pack(pady=5)
    botonRechazar = tk.Button(root, text="Rechazar", command=root.destroy)
    botonRechazar.pack(pady=5)

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

def crearObjetosAnimal(listaNombres):
    genai.configure(api_key="AIzaSyCj7ewGgJ0c7Cb_nHrHfzkN4lGDFlZ_iY0")
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    animales = []
    consecutivo = 1 #Para no generar consecutivos erroneos
    for nombre in listaNombres:
        nombreCientifico, tipo, url = obtenerDatosAnimalGemini(model, nombre)
        estado = random.randint(1, 5)
        calificacion = 1
        if "carn" in tipo:
            tipoAlimenticio = "c"
        elif "herb" in tipo:
            tipoAlimenticio = "h"
        else:
            tipoAlimenticio = "o"
        if tipoAlimenticio == "h":
            peso = random.uniform(80.0, 100.0)
        else:
            peso = random.uniform(0.0, 80.0)
        idAnimal = generarId(nombre, consecutivo)
        a = Animal()
        a.asignarId(idAnimal)
        a.asignarNombres((nombre, nombreCientifico))
        a.asignarUrl(url)
        a.asignarInformacion([estado, calificacion, tipoAlimenticio, round(peso, 2)])
        animales.append(a)
        consecutivo += 1 #Para no generar consecutivos repetidos
    return animales #Devuelve lista con los animales

def crearInventarioDesdeTxt():
    nombresSeleccionados = seleccionarAnimalesAleatorios("Animales", 20) #Genera 20 por indicaciones en la TP
    listaObjetos = crearObjetosAnimal(nombresSeleccionados) #Genera la lista con los objetos
    print("\nObjetos creados:") #Print temporal en terminal
    for animal in listaObjetos:
        print(animal.indicarDatos())
    guardarPickle("inventario.pkl", listaObjetos)
    ventanaConfirmacion("Inventario creado y guardado con éxito en 'inventario.pkl'.") #Guarda en pickle
    return listaObjetos

##################################################
# 1. Obtener lista
##################################################

def obtenerLista(numeroTotales):
    try:
        # Configurar Wikipedia
        wikipedia.set_lang("es")
        contenido = wikipedia.summary("Animales", sentences=5)
        # Configurar Gemini
        genai.configure(api_key="AIzaSyCj7ewGgJ0c7Cb_nHrHfzkN4lGDFlZ_iY0")
        model = genai.GenerativeModel(model_name = "gemini-1.5-flash")
        response = model.generate_content(
        f"Genérame una lista de {numeroTotales} animales distintos, asegurándote de que cada uno sea específico y único. " +
        "Utiliza únicamente nombres comunes detallados (por ejemplo: 'Águila real', 'Zorro ártico', 'Delfín nariz de botella', 'Mariposa monarca'). " +
        "No uses nombres genéricos como 'Águila', 'Zorro' o 'Mariposa'. " +
        "Devuélvelos estrictamente en este formato: solo el nombre común, sin numeración ni negritas ni texto adicional. " +
        "Ejemplo de formato: León africano") #Prompt modificado para generar nombres mas especificos
        resultado = response.text
        resultado = limpiarTexto(resultado)
        lineas = resultado.splitlines()
        listaAnimales = []
        for linea in lineas:
            lineaLimpia = linea.strip()
            if lineaLimpia != "": #Verificar que la línea no esté vacía
                listaAnimales.append(lineaLimpia) #Agregar la línea limpia a la lista
        resultadoLimpio = "\n".join(listaAnimales)
        print(resultadoLimpio)
        grabaTxt("Animales", resultadoLimpio)
        mensaje = f"Se ha creado el txt con los {numeroTotales} animales."
        ventanaConfirmacion(mensaje)
    except Exception as e:
        print(f"Ha ocurrido un error con: {e}")

def validarObtenerLista(numeroTotales):
    if not numeroTotales.isdigit():
        mensaje = "El valor tiene que ser un valor numérico."
        return ventanaRetroalimentacion(mensaje)
    numeroTotales = int(numeroTotales)
    if numeroTotales < 20:
        mensaje = "Tiene que tener por lo menos 20 animales."
        return ventanaRetroalimentacion(mensaje)
    else:
        return obtenerLista(numeroTotales)

def ventanaObtenerLista():
    search = tk.Toplevel()
    search.title("Obtener animales")
    search.geometry("300x200")
    diccGlobal["numero"] = tk.StringVar()
    cantidad = tk.Entry(search, width=30, textvariable=diccGlobal["numero"])
    cantidad.pack()
    searchButton = tk.Button(search, text="Buscar", width=30, command=lambda: validarObtenerLista(diccGlobal["numero"].get()))
    searchButton.pack()
    search.mainloop()

##################################################
# Ventana Principal
##################################################

def main():
    """
    Funcionamiento:
    Muestra la ventana principal del programa con los botones del menú.
    Entradas:
    - NA
    Salidas:
    - Inicia la interfaz gráfica principal y muestra los botones con sus respectivas funciones.
    """
    root = tk.Tk()
    root.geometry("300x250")
    root.title("Ventana Principal")
    diccGlobal["root"] = root
    title = tk.Label(root, text="Zooinventario")
    title.pack()

    diccGlobal["botones"]["boton1"] = tk.Button(root, text="1. Obtener lista", width=20, command=ventanaObtenerLista)
    diccGlobal["botones"]["boton1"].pack()  
    diccGlobal["botones"]["boton2"] = tk.Button(root, text="2. Crear Inventario", width=20, command=crearInventarioDesdeTxt)
    diccGlobal["botones"]["boton2"].pack()
    diccGlobal["botones"]["boton3"] = tk.Button(root, text="3. Mostrar Inventario", width=20)
    diccGlobal["botones"]["boton3"].pack()
    diccGlobal["botones"]["boton4"] = tk.Button(root, text="4. Estadística * estado", width=20) #nunca se va a usar
    diccGlobal["botones"]["boton4"].pack()
    diccGlobal["botones"]["boton5"] = tk.Button(root, text="5. Crear HTML", width=20)
    diccGlobal["botones"]["boton5"].pack()
    diccGlobal["botones"]["boton6"] = tk.Button(root, text="6. Generar PDF", width=20)
    diccGlobal["botones"]["boton6"].pack()
    diccGlobal["botones"]["boton7"] = tk.Button(root, text="7. Generar .csv", width=20)
    diccGlobal["botones"]["boton7"].pack()
    diccGlobal["botones"]["boton8"] = tk.Button(root, text="8. Búsqueda por nombre", width=20)
    diccGlobal["botones"]["boton8"].pack()
    root.mainloop()

diccGlobal = {
    "root": None,
    "botones": {}
}
main()