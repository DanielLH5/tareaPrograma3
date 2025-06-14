import tkinter as tk

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

    diccGlobal["botones"]["boton1"] = tk.Button(root, text="1. Obtener lista", width=20)
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