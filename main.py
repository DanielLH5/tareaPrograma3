import tkinter as tk
from tkinter import ttk, messagebox
import random
#python -m pip install wikipedia
import wikipedia
#python -m pip install google-generativeai
import google.generativeai as genai
from PIL import Image, ImageTk
import urllib.request
import io

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
# 8. Búsqueda por orden
##################################################

def mostrarBPO():
    """
    Funcionamiento:
    Dependiendo de la opción seleccionada en el menú desplegable (herbívoro, carnívoro, omnívoro),
    genera un archivo HTML que muestra una tabla con los animales de esa categoría, utilizando los datos
    del archivo inventarioPkl.
    Entradas:
    - No tiene parámetros de entrada explícitos.
    - Utiliza diccGlobal["seleccionVariable"] para saber qué categoría fue seleccionada.
    Salidas:
    - Genera un archivo HTML con la información correspondiente.
    - Si no se selecciona ninguna opción válida, muestra una ventana de retroalimentación con un mensaje de advertencia.
    """
    seleccion = diccGlobal["seleccionVariable"].get()
    documento = cargarPickle(inventarioPkl)
    if seleccion == "--Seleccionar--":
        mensaje = "Tiene que seleccionar una de las opciones."
        ventanaRetroalimentacion(mensaje)
    else:
        if seleccion == "Hervíboro":
            (listaHerbivoros, documento) = obtenerAnimalesPorDieta('h', documento)
            matrizDatos = obtenerMatrizDatosBPO(listaHerbivoros, documento)
            formato = formatoHTMLBPO("Hervíboros", matrizDatos)
            with open(f"animalesHervíboros.html", "w", encoding="utf-8") as archivo:
                archivo.write(formato)
            ventanaConfirmacion("Se ha creado exitosamente el archivo animalesHervíboros.html")
        if seleccion == "Carnívoro":
            (listaCarnivoros, documento) = obtenerAnimalesPorDieta('c', documento)
            matrizDatos = obtenerMatrizDatosBPO(listaCarnivoros, documento)
            formato = formatoHTMLBPO("Carnívoros", matrizDatos)
            with open(f"animalesCarnívoros.html", "w", encoding="utf-8") as archivo:
                archivo.write(formato)
            ventanaConfirmacion("Se ha creado exitosamente el archivo animalesCarnívoros.html")
        if seleccion == "Omnívoro":
            (listaOmnivoros, documento) = obtenerAnimalesPorDieta('o', documento)
            matrizDatos = obtenerMatrizDatosBPO(listaOmnivoros, documento)
            formato = formatoHTMLBPO("Omnívoros", matrizDatos)
            with open(f"animalesOmnívoros.html", "w", encoding="utf-8") as archivo:
                archivo.write(formato)
            ventanaConfirmacion("Se ha creado exitosamente el archivo animalesOmnívoros.html")
    
def limpiarBPO():
    """
    Funcionamiento:
    Restablece la opción del menú desplegable a su valor por defecto ("--Seleccionar--").
    Entradas:
    - NA.
    Salidas:
    - NA.
    """
    diccGlobal["seleccionVariable"].set("--Seleccionar--")

def ventanaBusquedaPorOrden():
    """
    Funcionamiento:
    Crea una nueva ventana emergente que permite al usuario seleccionar una categoría de animales
    según su tipo de dieta ("Carnívoro", "Hervíboro", "Omnívoro") y generar un archivo HTML con los datos.
    Incluye un menú desplegable para seleccionar la categoría y dos botones: "Mostrar" y "Limpiar".
    Entradas:
    - NA.
    Salidas:
    - Ventana interactiva con un menú y botones.
    """
    # Crear la ventana
    ventana = tk.Toplevel(diccGlobal["root"])  # Ventana hija, no raíz
    ventana.title("Mostrar por Orden")
    ventana.geometry("300x200")
    # Etiqueta título
    titulo = tk.Label(ventana, text="Mostrar por Orden", font=("Arial", 12))
    titulo.pack(pady=10)
    # Frame para el menú
    frame = tk.Frame(ventana)
    frame.pack()
    # Etiqueta y Combobox
    tk.Label(frame, text="Orden").grid(row=0, column=0, padx=5, pady=5)
    diccGlobal["seleccionVariable"] = tk.StringVar(value="--Seleccionar--")
    selecciones = ttk.Combobox(frame, textvariable=diccGlobal["seleccionVariable"], state="readonly")
    selecciones['values'] = ("--Seleccionar--", "Carnívoro", "Hervíboro", "Omnívoro")
    selecciones.grid(row=0, column=1, padx=5, pady=5)
    # Botones
    botonFrame = tk.Frame(ventana)
    botonFrame.pack(pady=10)
    tk.Button(botonFrame, text="Mostrar", command=mostrarBPO).pack(side="left", padx=5)
    tk.Button(botonFrame, text="Limpiar", command=limpiarBPO).pack(side="left", padx=5)
    ventana.mainloop()

##################################################
# 5. Crear HTML
##################################################

def crearHTML():
    """
    Funcionamiento:
    Genera un archivo HTML que muestra una tabla con los animales ordenados por tipo de dieta 
    (herbívoros, carnívoros, omnívoros) y ordenados por peso de forma descendente.
    Utiliza funciones auxiliares para filtrar, ordenar y dar formato a los datos.
    Entradas:
    - NA
    Salidas:
    - Crea el archivo "estadisticaPorOrden.html" con la tabla generada.
    """
    documento = cargarPickle(inventarioPkl)
    (listaHerbivoros, documento) = obtenerAnimalesPorDieta('h', documento)
    (listaCarnivoros, documento) = obtenerAnimalesPorDieta('c', documento)
    (listaOmnivoros, documento) = obtenerAnimalesPorDieta('o', documento)
    herNombrePeso = obtenerPesoPorDieta(listaHerbivoros, documento)
    carNombrePeso = obtenerPesoPorDieta(listaCarnivoros, documento)
    omnNombrePeso = obtenerPesoPorDieta(listaOmnivoros, documento)
    formato = formatoHTMLPesoDieta(herNombrePeso, carNombrePeso, omnNombrePeso)
    with open(f"estadisticaPorOrden.html", "w", encoding="utf-8") as archivo:
        archivo.write(formato)
    mensaje = "Se ha creado exitosamente el archivo estadisticaPorOrden.html."
    ventanaConfirmacion(mensaje)

##################################################
# 4. Estadística por estado
##################################################

def obtenerEstadísticaPorEstado():
    """
    Funcionamiento:
    Recupera la información del inventario desde un archivo .pkl, extrae los estados de todos los animales,
    calcula estadísticas y porcentajes por estado, y finalmente muestra esta información en una ventana gráfica.
    Entradas:
    - NA.
    Salidas:
    - Muestra la ventana generada por ventanaEstadisticaPorEstado.
    """
    documento = cargarPickle(inventarioPkl)
    estados = []
    for animal in documento:
        info = animal.mostrarInformacion()
        estados.append(info)
    estadisticas = contarEstadosAnimales(estados)
    porcentajes = obtenerPorcentajes(estadisticas)
    return ventanaEstadisticaPorEstado(estadisticas, porcentajes)
    
def ventanaEstadisticaPorEstado(estadisticas, porcentajes):
    """
    Funcionamiento:
    Crea una ventana emergente que muestra en forma tabular la cantidad y el porcentaje de animales
    en cada uno de los 5 estados: Vivo, Enfermo, Traslado, Muerto en museo, y Muerto.
    Entradas:
    - estadisticas (tuple[int]): Cantidad de animales por estado.
    - porcentajes (tuple[float]): Porcentaje de animales por estado (basado en un total de 20).
    Salidas:
    - NA.
    """
    ventana = tk.Toplevel()
    ventana.title("Estadística por estado")
    ventana.geometry("350x200")
    titulo = tk.Label(ventana, text="Estadística por estado", font=(14)) # font es tamaño de letra
    titulo.grid(row=0, column=0, pady=10)
    # Encabezados
    tk.Label(ventana, text="").grid(row=1, column=0)
    tk.Label(ventana, text="Cantidad").grid(row=1, column=1)
    tk.Label(ventana, text="Porcentaje").grid(row=1, column=2)
    estados = ["Vivo", "Enfermo", "Traslado", "Muerto en museo", "Muerto"]
    for i in range(len(estados)):
        tk.Label(ventana, text=estados[i]).grid(row=i+2, column=0, sticky="w", padx=5) # sticky="w" es pegado a la izquierda.
        tk.Entry(ventana, width=5).grid(row=i+2, column=1)
        tk.Entry(ventana, width=5).grid(row=i+2, column=2)
        # Insertar datos en los campos
        e1 = tk.Entry(ventana, width=5)
        e1.insert(0, estadisticas[i])
        e1.config(state='readonly') # No se puede modificar este espacio
        e1.grid(row=i+2, column=1)
        e2 = tk.Entry(ventana, width=5)
        e2.insert(0, porcentajes[i])
        e2.config(state='readonly')
        e2.grid(row=i+2, column=2)
    ventana.mainloop()
    
##################################################
# 3. Mostrar inventario
##################################################

simbolos = {2: "🚑", 3: "🚑", 4: "🏛️", 5: "💀"} #Me da TOC el museo que se hace a la izquierda.
emojis = {2: "👍", 3: "🌟", 4: "😢", 5: "😠"}

def mostrarInventario():
    listaAnimales = cargarPickle("inventario.pkl")
    indice = 0 
    root = tk.Toplevel()
    root.title("Inventario :3")
    root.geometry("600x500")
    root.resizable(False, False) #Desactiva la redimension
    contenedor = tk.Frame(root)
    contenedor.pack()
    framesAnimales = []
    def mostrarActuales():
        nonlocal framesAnimales, indice #Reasigna la lista de frames definida en la función principal
        for frame in framesAnimales:
            frame.destroy()
        framesAnimales = []
        actuales = listaAnimales[indice:indice+4] #De donde esté, a tres mas
        for idx, animal in enumerate(actuales):
            fila = idx // 2
            columna = idx % 2
            frame = tk.Frame(contenedor, relief="ridge", borderwidth=2, padx=10, pady=10)
            frame.grid(row=fila, column=columna, padx=10, pady=10)
            framesAnimales.append(frame)
            mostrarAnimal(frame, animal)
    def mostrarAnimal(frame, animal):
        id, (nombreComun, _), url, [estado, calificacion, _, _] = animal.indicarDatos() #_ para datos que no se usan
        tk.Label(frame, text=nombreComun, font=("Arial", 10, "bold"), wraplength=150).pack(pady=2)
        if estado == 1:
            try:
                with urllib.request.urlopen(url) as u:
                    raw_data = u.read()
                im = Image.open(io.BytesIO(raw_data))
                im = im.resize((100, 100))
                photo = ImageTk.PhotoImage(im)
                lbl = tk.Label(frame, image=photo)
                lbl.image = photo
                lbl.pack()
            except:
                tk.Label(frame, text="Imagen en mantenimiento.").pack() #En caso de que no cargue la imagen
        else:
            simbolo = simbolos.get(estado, "?")
            tk.Label(frame, text=simbolo, font=("Arial", 48)).pack()
        botones = tk.Frame(frame)
        botones.pack(pady=5)
        for val, emoji in emojis.items():
            estadoValido = ((val == 4 and estado in [2, 5]) or
                            (val == 5 and estado == 3) or
                            (val in [2, 3]))
            b = tk.Button(botones, text=emoji, width=3, font=("Segoe UI Emoji", 14),
                          command=lambda a=animal, v=val: calificarAnimal(a, v))
            if not estadoValido:
                b.config(state="disabled")
            if val == calificacion:
                b.config(relief="sunken")
            b.pack(side="left")
    def calificarAnimal(animal, valor):
        animal.informacion[1] = valor
        guardarPickle("inventario.pkl", listaAnimales)
        mostrarActuales()
    def mostrarSiguiente():
        nonlocal indice #Se usa nonlocal para modificar "indice" que está en la función externa
        if indice + 4 < len(listaAnimales):
            indice += 4
            mostrarActuales()
    def mostrarAnterior():
        nonlocal indice #Se usa nonlocal para modificar "indice" que está en la función externa
        if indice - 4 >= 0:
            indice -= 4
            mostrarActuales()
    nav = tk.Frame(root)
    nav.pack(pady=10)
    tk.Button(nav, text="<< Anterior", command=mostrarAnterior).pack(side="left")
    tk.Button(nav, text="Siguiente >>", command=mostrarSiguiente).pack(side="left")
    mostrarActuales()

##################################################
# 2. Crear inventario
##################################################

def crearObjetosAnimal(listaNombres):
    genai.configure(api_key="AIzaSyCj7ewGgJ0c7Cb_nHrHfzkN4lGDFlZ_iY0")
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    animales = []
    consecutivo = 1
    for nombre in listaNombres:
        nombreCientifico, tipo, url = obtenerDatosAnimal(nombre, model)
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
        consecutivo += 1
    return animales

def crearInventarioDesdeTxt():
    nombresSeleccionados = seleccionarAnimalesAleatorios("Animales", 20)
    listaObjetos = crearObjetosAnimal(nombresSeleccionados)
    print("\nObjetos creados:")
    for animal in listaObjetos:
        print(animal.indicarDatos())
    guardarPickle("inventario.pkl", listaObjetos)
    ventanaConfirmacion("Inventario creado y guardado con éxito en inventario.pkl.")
    return listaObjetos

##################################################
# 1. Obtener lista
##################################################

def obtenerLista(numeroTotales):
    """
    Funcionamiento:
    Obtiene una lista de animales desde Wikipedia, solicita a la API de Gemini que genere nombres específicos de animales,
    limpia el texto recibido y lo guarda en un archivo de texto. Muestra una ventana de confirmación al finalizar.
    Entradas:
    - numeroTotales (int): Cantidad de animales que se desea obtener.
    Salidas:
    - NA.
    """
    try:
        # Configurar Wikipedia
        wikipedia.set_lang("es")
        contenido = wikipedia.summary(animalesTxt, sentences=5)
        # Configurar Gemini
        genai.configure(api_key="AIzaSyCj7ewGgJ0c7Cb_nHrHfzkN4lGDFlZ_iY0")
        model = genai.GenerativeModel(model_name = "gemini-1.5-flash")
        mensajePeticion = peticionGeminiAnimales(numeroTotales, contenido)
        response = model.generate_content(mensajePeticion) #Prompt modificado para generar nombres mas especificos
        resultado = response.text
        resultado = limpiarTexto(resultado)
        lineas = resultado.splitlines()
        resultadoLimpio = obtenerTextoAniLimpio(lineas)
        grabaTxt("Animales", resultadoLimpio)
        mensaje = f"Se ha creado el txt con los {numeroTotales} animales."
        ventanaConfirmacion(mensaje)
    except Exception as e:
        print(f"Ha ocurrido un error con: {e}")

def validarObtenerLista(numeroTotales):
    """
    Funcionamiento:
    Valida que el valor ingresado sea numérico y mayor o igual a 20. Si cumple con los requisitos,
    llama a la función obtenerLista. Si no, muestra un mensaje de retroalimentación.
    Entradas:
    - numeroTotales (str): Valor ingresado por el usuario como string.
    Salidas:
    - Llama a obtenerLista(numeroTotales) si es válido.
    - Muestra retroalimentación si no es válido.
    """
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
    """
    Funcionamiento:
    Crea una ventana emergente con una interfaz gráfica que permite al usuario ingresar
    un número para especificar cuántos animales desea obtener. El botón "Buscar" valida ese número.
    Entradas:
    - NA.
    Salidas:
    - NA (la función invoca otras funciones en base a la interacción del usuario).
    """
    search = tk.Toplevel()
    search.title("Obtener animales")
    search.geometry("300x200")
    etiqueta = tk.Label(search, text="Ingrese el número de animales:")
    etiqueta.pack(pady=(10, 5)) #5 píxeles arriba y 10 abajo
    diccGlobal["numero"] = tk.StringVar()
    cantidad = tk.Entry(search, width=30, textvariable=diccGlobal["numero"])
    cantidad.pack(pady=5) #5 pixeles arriba y abajo
    searchButton = tk.Button(search, text="Buscar", width=30, command=lambda: validarObtenerLista(diccGlobal["numero"].get()))
    searchButton.pack(pady=(5, 10))
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
    diccGlobal["botones"]["boton3"] = tk.Button(root, text="3. Mostrar Inventario", width=20, command=mostrarInventario)
    diccGlobal["botones"]["boton3"].pack()
    diccGlobal["botones"]["boton4"] = tk.Button(root, text="4. Estadística por estado", width=20, command=obtenerEstadísticaPorEstado)
    diccGlobal["botones"]["boton4"].pack()
    diccGlobal["botones"]["boton5"] = tk.Button(root, text="5. Crear HTML", width=20, command=crearHTML)
    diccGlobal["botones"]["boton5"].pack()
    diccGlobal["botones"]["boton6"] = tk.Button(root, text="6. Generar PDF", width=20)
    diccGlobal["botones"]["boton6"].pack()
    diccGlobal["botones"]["boton7"] = tk.Button(root, text="7. Generar .csv", width=20)
    diccGlobal["botones"]["boton7"].pack()
    diccGlobal["botones"]["boton8"] = tk.Button(root, text="8. Búsqueda por orden", width=20, command=ventanaBusquedaPorOrden)
    diccGlobal["botones"]["boton8"].pack()
    root.mainloop()

diccGlobal = {
    "root": None,
    "botones": {}
}
main()