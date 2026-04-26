import tkinter as tk
from tkinter import messagebox

def agregar_item():
    item = entrada_producto.get()
    if item != "":
        lista_compras.insert(tk.END, item)
        entrada_producto.delete(0, tk.END)
    else:
        messagebox.showwarning("Atención", "Por favor, escribe un producto.")

def eliminar_item():
    try:
        seleccion = lista_compras.curselection()
        lista_compras.delete(seleccion)
    except:
        messagebox.showwarning("Atención", "Selecciona un producto para eliminar.")

def limpiar_lista():
    confirmacion = messagebox.askyesno("Confirmar", "¿Deseas borrar toda la lista?")
    if confirmacion:
        lista_compras.delete(0, tk.END)

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Lista para Mercar")
ventana.geometry("400x500")

# Elementos de la interfaz
etiqueta = tk.Label(ventana, text="Producto:", font=("Arial", 12))
etiqueta.pack(pady=10)

entrada_producto = tk.Entry(ventana, font=("Arial", 14), width=25)
entrada_producto.pack(pady=5)

boton_agregar = tk.Button(ventana, text="Añadir a la lista", command=agregar_item, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
boton_agregar.pack(pady=10)

# Lista visual
lista_compras = tk.Listbox(ventana, font=("Arial", 12), width=35, height=10)
lista_compras.pack(pady=10)

# Botones de acción
marco_botones = tk.Frame(ventana)
marco_botones.pack(pady=10)

boton_eliminar = tk.Button(marco_botones, text="Eliminar seleccionado", command=eliminar_item, bg="#f44336", fg="white")
boton_eliminar.grid(row=0, column=0, padx=5)

boton_limpiar = tk.Button(marco_botones, text="Vaciar lista", command=limpiar_lista, bg="#555555", fg="white")
boton_limpiar.grid(row=0, column=1, padx=5)

# Ejecutar la aplicación
ventana.mainloop()
