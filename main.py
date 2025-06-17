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
# 4. Estadística por estado
##################################################

def obtenerEstadísticaPorEstado():
    #('id', ('nombreColoquial', 'nombreCientifico'), 'url', [5, 1, 'c', 31.39])
    documento = cargarPickle(inventarioPkl)
    estados = []
    for animal in documento:
        info = animal.mostrarInformacion()
        estados.append(info)
    estadisticas = contarEstadosAnimales(estados)
    porcentajes = obtenerPorcentajes(estadisticas)
    return ventanaEstadisticaPorEstado(estadisticas, porcentajes)
    
def ventanaEstadisticaPorEstado(estadisticas, porcentajes):
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
# 2. Crear inventario
##################################################

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
    guardarPickle(inventarioPkl, listaObjetos)
    ventanaConfirmacion("Inventario creado y guardado con éxito en 'inventario.pkl'.") #Guarda en pickle
    return listaObjetos

##################################################
# 1. Obtener lista
##################################################

def obtenerLista(numeroTotales):
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
    diccGlobal["botones"]["boton3"] = tk.Button(root, text="3. Mostrar Inventario", width=20)
    diccGlobal["botones"]["boton3"].pack()
    diccGlobal["botones"]["boton4"] = tk.Button(root, text="4. Estadística por estado", width=20, command=obtenerEstadísticaPorEstado)
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