import tkinter as tk
from tkinter import messagebox
# Crear ventana principal
root = tk.Tk()
clientes = []
last_id_cliente = 0
#Variable del producto(nombre) con su respetivo valor para que el valor cambie cuando sea necesario
coca_cola = 30
pepsi = 30
papas_margaritas = 20
choclito = 20
doritos = 15

# Clase cliente
class Cliente:
    def __init__(self, id_cliente, nombre, fechaNacimiento, documento):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.fechaNacimiento = fechaNacimiento
        self.documento = documento


# Clase producto
class Producto:
    def __init__(self, id_producto, nombre, cantidad, costo_compra, precio_compra, fechaVencimiento):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.costo_compra = costo_compra
        self.precio_compra = precio_compra
        self.fechaVencimiento = fechaVencimiento

# Crear varios productos
# Instanciar productos
productos = [
    Producto("01", "Coca-Cola", coca_cola, 1000, 1500, "21/05/2024"),
    Producto("02", "Pepsi", pepsi, 1000, 1500, "21/05/2024"),
    Producto("03", "Papas Margaritas", papas_margaritas, 4000, 5000, "04/08/2024"),
    Producto("04", "Choclito", choclito, 4100, 5200, "01/11/2024"),
    Producto("05", "Doritos", doritos, 3500, 4000, "11/10/2024")
]

class Factura:
    def __init__(self,id_factura, id_cliente, fecha_factura,total_factura,productos_vendidos):
        self.id_factura = id_factura
        self.id_cliente = id_cliente
        self. fecha_factura =  fecha_factura
        self. fecha_factura =  fecha_factura
        self.productos_vendidos = productos_vendidos
        
# Función para guardar la información del cliente en la matriz 3xN
def guardar_cliente(nombre, fecha_naci, documento):
    global last_id_cliente
    last_id_cliente += 1
    clientes.append([last_id_cliente, nombre, fecha_naci, documento])
    messagebox.showinfo("Guardado", "Cliente guardado correctamente.")
    print(clientes)
    
# Función para crear el menú de productos
def menu_productos():
    

    # Etiqueta de título para el menú de productos
    label_titulo_productos = tk.Label(root, text="PRODUCTOS REGISTRADOS")
    label_titulo_productos.grid(row=0, column=1, columnspan=10, padx=10)
   

def ver_productos():
    # Elimina todos los widgets de la ventana principal
    for widget in root.winfo_children():
        widget.destroy()
    # Etiqueta de título para el menú de productos
    label_titulo_productos = tk.Label(root, text="PRODUCTOS REGISTRADOS")
    label_titulo_productos.grid(row=0, column=0, columnspan=10, padx=10)

    # Mostrar información de los productos en etiquetas
    atributos = ["ID", "Nombre", "Cantidad", "Costo compra", "Precio compra", "Fecha de vencimiento"]
    for i, attr in enumerate(atributos):
        tk.Label(root, text=attr.upper()).grid(row=1, column=i, padx=10)

    # Mostrar los valores de los productos en etiquetas
    for i, producto in enumerate(productos):
        valores = [producto.id_producto, producto.nombre, producto.cantidad, producto.costo_compra, producto.precio_compra, producto.fechaVencimiento]
        for j, value in enumerate(valores):
            tk.Label(root, text=value).grid(row=i+2, column=j, padx=10)

    # Botón para volver al menú principal
    boton_volver = tk.Button(root, text="Volver al menú principal", command=volver_menu_principal)
    boton_volver.grid(row=len(productos)+2, column=0, columnspan=10)

def menu_clientes():
  # Elimina todos los widgets de la ventana principal
  for widget in root.winfo_children():
      widget.destroy()

  # Etiqueta de título para el menú de clientes
  label_titulo_clientes = tk.Label(root, text="CLIENTES")
  label_titulo_clientes.grid(row=0, column=0)

  # ETIQUETAS PARA LOS DATOS DEL CLIENTE
  label_id_cliente = tk.Label(root, text=f"Clientes registrados: {last_id_cliente}")
  label_id_cliente.grid(row=0, column=1)
  label_nombre = tk.Label(root, text="Nombre:")
  label_nombre.grid(row=1, column=0)
  label_fecha_naci = tk.Label(root, text="Fecha de nacimiento:")
  label_fecha_naci.grid(row=2, column=0)
  label_documento = tk.Label(root, text="Documento:")
  label_documento.grid(row=3, column=0)

  # ENTRADAS PARA LOS DATOS DEL CLIENTE
  entry_nombre = tk.Entry(root, width=15)
  entry_nombre.grid(row=1, column=1)
  entry_fecha_naci = tk.Entry(root, width=15)
  entry_fecha_naci.grid(row=2, column=1)
  entry_documento = tk.Entry(root, width=15)
  entry_documento.grid(row=3, column=1)
  


  def save_cliente():
    documento = entry_documento.get()
    for cliente in clientes:
        if documento == cliente[3]:
            messagebox.showinfo("Error documento", "El número de Documento ya se encuentra registrado, introduzca un documento diferente")
            return 
    guardar_cliente(entry_nombre.get(), entry_fecha_naci.get(), entry_documento.get())
    return menu_factura()



        
  # BOTÓN PARA GUARDAR CLIENTE
  boton_save_cliente = tk.Button(root, text="GUARDAR CLIENTE", command=save_cliente)
  boton_save_cliente.grid(row=4, column=1)
  

  # BOTÓN DE VOLVER A LA PANTALLA PRINCIPAL
  boton_volver = tk.Button(root, text="VOLVER", command=volver_menu_principal)
  boton_volver.grid(row=4, column=0)

def menu_factura():
    # Eliminar todos los widgets de la ventana
    for widget in root.winfo_children():
        widget.destroy()
    
    # Etiqueta de título para el menú de productos
    label_titulo_productos = tk.Label(root, text="PRODUCTOS REGISTRADOS")
    label_titulo_productos.grid(row=4, column=0, columnspan=10, padx=10, pady=5)
    
    # Mostrar información de los productos en etiquetas
    atributos = ["ID", "Nombre", "Disponible","Costo de compra", "Precio compra", "Fecha de vencimiento", "ingresar cantidad"]
    
    for i, attr in enumerate(atributos):
        tk.Label(root, text=attr.upper()).grid(row=5, column=i, padx=10)
        i +=1
     # Mostrar los valores de los productos en etiquetas
    
    for i, producto in enumerate(productos):
        
        valores = [producto.id_producto, producto.nombre, producto.cantidad,producto.costo_compra, producto.precio_compra, producto.fechaVencimiento]
        
        for j, value in enumerate(valores):
            tk.Label(root, text=value).grid(row=i+6, column=j, padx=10)
            j +=1
                
    #entras para guardar los productos
    entry_prod1 = tk.Entry(root, width=10)
    entry_prod1.grid(row=6, column=6, padx=3)
    
    entry_prod2 = tk.Entry(root, width=10)
    entry_prod2.grid(row=7, column=6, padx=3)
    
    entry_prod3 = tk.Entry(root, width=10)
    entry_prod3.grid(row=8, column=6, padx=3)
    
    entry_prod4 = tk.Entry(root, width=10)
    entry_prod4.grid(row=9, column=6, padx=3)
    
    entry_prod5 = tk.Entry(root, width=10)
    entry_prod5.grid(row=10, column=6, padx=3)
    
    def save_produt_factura():
        productos_vendidos = []
        
    
    # botón para guardar los productos del cliente
    boton_guardar_productos = tk.Button(root, text="Guardar productos", command=volver_menu_principal)
    boton_guardar_productos.grid(row=11, column=6)
    
    # Botón para volver al menú principal
    boton_volver = tk.Button(root, text="Volver al menú principal", command=volver_menu_principal)
    boton_volver.grid(row= 11,column=0, columnspan=10 )
    
def ver_factura():
    # Eliminar todos los widgets de la ventana
    for widget in root.winfo_children():
        widget.destroy()

    root.columnconfigure(1, weight=1)  # Ajuste de la columna 1

    label_titulo = tk.Label(root, text="FACTURA")
    label_titulo.grid(row=0, column=0, pady=10, columnspan=10)
    
    

    # Crear Listbox para mostrar clientes registrados
    listbox = tk.Listbox(root, height=5, width=30, activestyle='dotbox', fg="BLUE")

    label_lista = tk.Label(root, text="CLIENTES REGISTRADOS")

    # Insert each cliente from the list into the Listbox
    for cliente in clientes:
        listbox.insert(tk.END, f"{cliente}")

    label_lista.grid(row=1, column=0, columnspan=10,)
    listbox.grid(row=2, column=0, columnspan=10, pady=5)
    # Botón para volver al menú principal
    boton_volver = tk.Button(root, text="Volver al menú principal", command=volver_menu_principal)
    boton_volver.grid(row= 4,column=0, columnspan=10 )
    
    #botón para añadir un nuevo cliente
    boton_anadir = tk.Button(root, text="Añadir nuevo cliente", command=menu_clientes)
    boton_anadir.grid(row= 3,column=0, columnspan=10)

def prod_agotado():
    for widget in root.winfo_children():
        widget.destroy()
    #etiqueta de productos agotados(titulo)
    titulo= tk.Label(root, text="PRODUCTOS AGOTADOS")
    titulo.grid(row=0, column=0, columnspan=10, padx=5)

#funcion para mostrar un informe de las ventas
def informe_ventas():
    for widget in root.winfo_children():
        widget.destroy()
    #etiqueta del informe de ventas(titulo)
    titulo= tk.Label(root, text="INFORME DE VENTAS")
    titulo.grid(row=0, column=0, columnspan=10, padx=5)

def volver_menu_principal():
  # Elimina todos los widgets de la ventana principal
  for widget in root.winfo_children():
      widget.destroy()

  return menu_principal()
    
def salir():
    root.quit()
      
def menu_principal():
  # Título de la interfaz
  label_titulo_interfaz = tk.Label(root, text="MENÚ PRINCIPAL")
  label_titulo_interfaz.grid(row=0, column=0)
  root.title("SISTEMA DE VENTAS")
  # Botón para clientes
  cliente_boton = tk.Button(root, text="Registrar Cliente", command=menu_clientes)
  cliente_boton.grid(row=1, column=0, padx=10, pady=5)

  # Botón para productos
  producto_boton = tk.Button(root, text="Ver Productos", command=ver_productos)
  producto_boton.grid(row=2, column=0, padx=10, pady=5)
  
  #Botón para factura
  factura_boton = tk.Button(root, text="Ver Facturas", command=ver_factura)
  factura_boton.grid( row=3, column=0, padx=10, pady=5)
  
  #boton para productos agotados
  prod_agotados = tk.Button(root, text="Productos Agotados", command=prod_agotado)
  prod_agotados.grid(row=4, column=0, padx = 10, pady=5)
  
  #boton informe de ventas
  infor_ventas = tk.Button(root, text="Informe de Ventas", command=informe_ventas)
  infor_ventas.grid(row = 5, column=0, padx = 10, pady=5)
  #Boton para salir del programa
  salir_boton = tk.Button(root, text="Salir del progrma", command=salir)
  salir_boton.grid(row = 6, column=0, padx = 10, pady=5)
  
menu_principal()
root.mainloop()
