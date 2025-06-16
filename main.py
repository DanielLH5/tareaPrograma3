import tkinter as tk
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
    root.geometry("300x100")
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
        f"Genérame una lista de {numeroTotales} animales diferentes a partir de {contenido}" +
        "únicamente con este formato: animal Sin ningún tipo de texto más ni negritas ni enumeración." +
        "Por ejemplo: Leon"
        )
        resultado = response.text
        resultado = limpiarTexto(resultado)
        resultado = resultado[:-1] #Para quitar el enter del final.
        print(resultado)
        grabaTxt("Animales", resultado)
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
    diccGlobal["botones"]["boton2"] = tk.Button(root, text="2. Crear Inventario", width=20)
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