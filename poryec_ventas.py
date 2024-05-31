import tkinter as tk
from tkinter import messagebox
import datetime
import os

# Crear ventana principal
root = tk.Tk()
clientes = [] #GUARDAR LA INFORMACION DE LOS CLIENTES 
last_id_cliente = 0
last_id_factura = 0

# Clase cliente
class Cliente:
    def __init__(self, id_cliente, nombre, fechaNacimiento, documento):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.fechaNacimiento = fechaNacimiento
        self.documento = documento
    def __str__(self):
        return f"ID: {self.id_cliente} | Nombre: {self.nombre} | Documento: {self.documento}"


# Clase producto
class Producto:
    def __init__(self, id_producto, nombre, cantidad, costo_compra, precio_venta, fechaVencimiento):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.costo_compra = costo_compra
        self.precio_venta = precio_venta
        self.fechaVencimiento = fechaVencimiento

# Clase factura
class Factura:
    def __init__(self, id_factura, id_cliente, fecha_factura, total_factura, productos_vendidos):
        self.id_factura = id_factura
        self.id_cliente = id_cliente
        self.fecha_factura = fecha_factura
        self.total_factura = total_factura
        self.productos_vendidos = productos_vendidos

productos = [
    Producto("01", "Coca-Cola", 30, 1000, 1500, "21/05/2024"),
    Producto("02", "Pepsi   ", 30, 1000, 1500, "21/05/2024"),
    Producto("03", "Margaritas", 20, 4000, 5000, "04/08/2024"),
    Producto("04", "Choclito", 20, 4100, 5200, "01/11/2024"),
    Producto("05", "Doritos", 15, 3500, 4000, "11/10/2024")
]

facturas = []

# Función para guardar los clientes en archivo
def guardar_cliente(nombre, fecha_naci, documento):
    global last_id_cliente
    last_id_cliente += 1
    cliente = Cliente(last_id_cliente, nombre, fecha_naci, documento)
    clientes.append(cliente)
    with open("clientes.txt", "a") as f:
        f.write(f"{cliente.id_cliente},{cliente.nombre},{cliente.fechaNacimiento},{cliente.documento}\n")
    messagebox.showinfo("Guardado", "Cliente guardado correctamente.")

# Función para cargar los clientes desde archivo
def cargar_clientes():
    global last_id_cliente
    if os.path.exists("clientes.txt"):
        with open("clientes.txt", "r") as f:
            for line in f:
                id_cliente, nombre, fechaNacimiento, documento = line.strip().split(",")
                clientes.append(Cliente(int(id_cliente), nombre, fechaNacimiento, documento))
                last_id_cliente = max(last_id_cliente, int(id_cliente))

# Función para guardar productos en archivo
def guardar_productos():
    with open("productos.txt", "w") as f:
        for producto in productos:
            f.write(f"{producto.id_producto},{producto.nombre},{producto.cantidad},{producto.costo_compra},{producto.precio_venta},{producto.fechaVencimiento}\n")

# Función para cargar productos desde archivo
def cargar_productos():
    if os.path.exists("productos.txt"):
        with open("productos.txt", "r") as f:
            productos.clear()
            for line in f:
                id_producto, nombre, cantidad, costo_compra, precio_venta, fechaVencimiento = line.strip().split(",")
                productos.append(Producto(id_producto, nombre, int(cantidad), int(costo_compra), int(precio_venta), fechaVencimiento))

# Función para guardar facturas en archivo
def guardar_factura(factura, monto_pagado, cambio):
    with open("facturas.txt", "a") as f:
        productos_vendidos_str = ";".join([f"{pv['id_producto']}:{pv['cantidad']}:{pv['precio']}" for pv in factura.productos_vendidos])
        f.write(f"{factura.id_factura},{factura.id_cliente},{factura.fecha_factura},{factura.total_factura},{productos_vendidos_str},{monto_pagado},{cambio}\n")
    generar_factura_txt(factura, monto_pagado, cambio)


# Función para cargar facturas desde archivo
def cargar_facturas():
    global last_id_factura
    if os.path.exists("facturas.txt"):
        with open("facturas.txt", "r") as f:
            facturas.clear()
            for line in f:
                # Ajustamos la cantidad de valores a desempacar
                id_factura, id_cliente, fecha_factura, total_factura, productos_vendidos_str, monto_pagado, cambio = line.strip().split(",")
                productos_vendidos = []
                for pv_str in productos_vendidos_str.split(";"):
                    id_producto, cantidad, precio = pv_str.split(":")
                    productos_vendidos.append({"id_producto": id_producto, "cantidad": int(cantidad), "precio": int(precio)})
                facturas.append(Factura(int(id_factura), int(id_cliente), fecha_factura, float(total_factura), productos_vendidos))
                last_id_factura = max(last_id_factura, int(id_factura))

# Función para generar factura en .txt
def generar_factura_txt(factura, monto_pagado=None, cambio=None):
    cliente = next((c for c in clientes if c.id_cliente == factura.id_cliente), None)
    if cliente:
        with open(f"factura_{factura.id_factura}.txt", "w") as f:
            f.write(f"Fecha: {factura.fecha_factura}\n")
            f.write(f"Factura N#: {factura.id_factura}\n\n")
            f.write("TULUA CENTER  T.C.\n")
            f.write(f"Cliente: {cliente.nombre}\n")
            f.write(f"Documento: {cliente.documento}\n\n")
            f.write("Productos:\n")
            
            
            for pv in factura.productos_vendidos:
                producto = next((p for p in productos if p.id_producto == pv["id_producto"]), None)
                if producto:
                    total_producto = pv["cantidad"] * pv["precio"]
                    f.write(f"{producto.id_producto}  \t{producto.nombre} \t{pv['cantidad']} unid/s  \t${pv['precio']} x Unid    total:\t${total_producto}\n")
                    
            f.write(f"\nTotal Factura: ${factura.total_factura}\n")
            if monto_pagado is not None and cambio is not None:
                f.write(f"Efectivo (COP): ${monto_pagado}\n")
                f.write(f"Cambio: ${cambio:.2f}\n")
#actualizar
def actualizar_archivo_facturas():
    with open("facturas.txt", "w") as f:
        for factura in facturas:
            productos_vendidos_str = ";".join([f"{pv['id_producto']}:{pv['cantidad']}:{pv['precio']}" for pv in factura.productos_vendidos])
            f.write(f"{factura.id_factura},{factura.id_cliente},{factura.fecha_factura},{factura.total_factura},{productos_vendidos_str}\n")

# Menú de productos
def menu_productos():
    for widget in root.winfo_children():
        widget.destroy()
    
    root.title("PRODUCTOS") #NOMBRE DE LA VENTANA 
    label_titulo_productos = tk.Label(root, text="PRODUCTOS REGISTRADOS")
    label_titulo_productos.grid(row=0, column=0, columnspan=10, padx=10)
    atributos = ["ID", "Nombre", "Cantidad", "Costo compra", "Precio venta", "Fecha de vencimiento"]
    for i, attr in enumerate(atributos):
        tk.Label(root, text=attr.upper()).grid(row=1, column=i, padx=10)
    for i, producto in enumerate(productos):
        valores = [producto.id_producto, producto.nombre, producto.cantidad, producto.costo_compra, producto.precio_venta, producto.fechaVencimiento]
        for j, value in enumerate(valores):
            tk.Label(root, text=value).grid(row=i+2, column=j, padx=10)
    boton_volver = tk.Button(root, text="Volver al menú principal", command=volver_menu_principal)
    boton_volver.grid(row=len(productos)+2, column=0, columnspan=10)

# Menú de clientes
def menu_clientes():
    for widget in root.winfo_children():
        widget.destroy()
        
    root.title("REGISTRAR CLIENTE") #NOMBRE DE LA VENTANA     
    label_titulo_clientes = tk.Label(root, text="CLIENTES")
    label_titulo_clientes.grid(row=0, column=0)
    label_id_cliente = tk.Label(root, text=f"Clientes registrados: {last_id_cliente}")
    label_id_cliente.grid(row=0, column=1)
    label_nombre = tk.Label(root, text="Nombre:")
    label_nombre.grid(row=1, column=0)
    label_fecha_naci = tk.Label(root, text="Fecha de nacimiento:")
    label_fecha_naci.grid(row=2, column=0)
    label_documento = tk.Label(root, text="Documento:")
    label_documento.grid(row=3, column=0)
    entry_nombre = tk.Entry(root, width=15)
    entry_nombre.grid(row=1, column=1)
    entry_fecha_naci = tk.Entry(root, width=15)
    entry_fecha_naci.grid(row=2, column=1)
    entry_documento = tk.Entry(root, width=15)
    entry_documento.grid(row=3, column=1)

    def save_cliente():
        documento = entry_documento.get()
        for cliente in clientes:
            if documento == cliente.documento:
                messagebox.showinfo("Error documento", "El número de Documento ya se encuentra registrado, introduzca un documento diferente")
                return 
        guardar_cliente(entry_nombre.get(), entry_fecha_naci.get(), entry_documento.get())
        return menu_factura()

    boton_save_cliente = tk.Button(root, text="GUARDAR CLIENTE", command=save_cliente)
    boton_save_cliente.grid(row=4, column=1)
    boton_volver = tk.Button(root, text="VOLVER", command=volver_menu_principal)
    boton_volver.grid(row=4, column=0)

# Menú de facturas
def menu_factura():
    for widget in root.winfo_children():
        widget.destroy()
    
    root.title("PRODUCTOS") #NOMBRE DE LA VENTANA 
    label_titulo_productos = tk.Label(root, text="PRODUCTOS REGISTRADOS")
    label_titulo_productos.grid(row=0, column=0, columnspan=10, padx=10, pady=5)
    atributos = ["ID", "Nombre", "Disponible", "Costo de compra", "Precio venta", "Fecha de vencimiento", "Ingresar cantidad"]
    for i, attr in enumerate(atributos):
        tk.Label(root, text=attr.upper()).grid(row=1, column=i, padx=10)

    entries = []
    for i, producto in enumerate(productos):
        valores = [producto.id_producto, producto.nombre, producto.cantidad, producto.costo_compra, producto.precio_venta, producto.fechaVencimiento]
        for j, value in enumerate(valores):
            tk.Label(root, text=value).grid(row=i+2, column=j, padx=10)
        entry_cantidad = tk.Entry(root, width=10)
        entry_cantidad.grid(row=i+2, column=len(atributos)-1, padx=3)
        entries.append((producto.id_producto, entry_cantidad))

    def guardar_productos_factura():
        productos_vendidos = []
        for id_producto, entry in entries:
            cantidad_str = entry.get()
            if cantidad_str.isdigit():
                cantidad = int(cantidad_str)
                producto = next((p for p in productos if p.id_producto == id_producto), None)
                if producto and cantidad > 0 and producto.cantidad >= cantidad:
                    producto.cantidad -= cantidad
                    productos_vendidos.append({"id_producto": id_producto, "cantidad": cantidad, "precio": producto.precio_venta})
                else:
                    messagebox.showinfo("Error", f"No hay suficiente cantidad de {producto.nombre}" if producto else "Producto no encontrado")
                    return
            elif cantidad_str:
                messagebox.showinfo("Error", f"Cantidad inválida para {id_producto}")
                return
        if productos_vendidos:
            global last_id_factura
            last_id_factura += 1
            id_cliente = last_id_cliente
            fecha_factura = datetime.datetime.now().strftime("%d/%m/%Y")
            total_factura = sum(pv["cantidad"] * pv["precio"] for pv in productos_vendidos)
            factura = Factura(last_id_factura, id_cliente, fecha_factura, total_factura, productos_vendidos)
            facturas.append(factura)
            #Llamar a guardar_productos despues de ajustar las cantidades de los productos
            guardar_productos()
            
            abrir_pagar_factura(factura, total_factura)

    def abrir_pagar_factura(factura, total_factura):
        def confirmar_pago():
            try:
                monto_pagado = float(entry_monto_pagado.get())
                if monto_pagado >= total_factura:
                    cambio = monto_pagado - total_factura
                    guardar_factura(factura, monto_pagado, cambio)
                    messagebox.showinfo("Pago Exitoso", f"Factura ID: {factura.id_factura} pagada correctamente. Cambio: ${cambio:.2f}")
                    
                    
                    pago_window.destroy()  # Cierra la ventana de pago una vez el pago es exitoso
                    menu_principal()  # Vuelve al menú principal
                    
                else:
                    messagebox.showinfo("Advertencia", "El monto pagado es menor al total de la factura.")
                    # No cerrar la ventana para permitir al usuario ingresar nuevamente
            except ValueError:
                messagebox.showwaring("Error", "Monto pagado inválido. Por favor ingrese un valor válido")
                # No cerrar la ventana para permitir al usuario ingresar nuevamente
            
        pago_window = tk.Toplevel(root)
        pago_window.title("PAGAR FACTURA")
        tk.Label(pago_window, text=f"ID Factura: {factura.id_factura}").grid(row=0, column=0)
        tk.Label(pago_window, text=f"Total Factura: ${factura.total_factura}").grid(row=1, column=0)
        tk.Label(pago_window, text="Efectivo (COP):").grid(row=2, column=0)
        entry_monto_pagado = tk.Entry(pago_window)
        entry_monto_pagado.grid(row=2, column=1)
        boton_confirmar = tk.Button(pago_window, text="Confirmar Pago", command=confirmar_pago)
        boton_confirmar.grid(row=3, column=0, columnspan=2)

    boton_guardar_productos = tk.Button(root, text="Guardar productos", command=guardar_productos_factura)
    boton_guardar_productos.grid(row=len(productos) + 3, column=len(atributos) - 1)
    boton_volver = tk.Button(root, text="Volver al menú principal", command=volver_menu_principal)
    boton_volver.grid(row=len(productos) + 3, column=0)

def ver_factura():
    # Eliminar todos los widgets de la ventana
    for widget in root.winfo_children():
        widget.destroy()
    root.title("MOSTRAR FACTURAS REGISTRADAS")
    label_titulo_facturas = tk.Label(root, text="FACTURAS")
    label_titulo_facturas.grid(row=0, column=0, columnspan=10)
    lista_facturas = tk.Listbox(root, width=75)
    lista_facturas.grid(row=1, column=0, columnspan=2)
    for factura in facturas:
        cliente = next((c for c in clientes if c.id_cliente == factura.id_cliente), None)
        cliente_info = f"{cliente.nombre} ({cliente.documento})" if cliente else "Cliente no encontrado"
        lista_facturas.insert(tk.END, f"ID: {factura.id_factura} | Cliente: {cliente_info} | Total: ${factura.total_factura} | Fecha: {factura.fecha_factura}")

    
    def ver_detalles_factura():
        selected_indices = lista_facturas.curselection()
        if not selected_indices:
            messagebox.showwarning("Advertencia", "Seleccione una factura para ver los detalles.")
            return
        selected_index = selected_indices[0]
        selected_factura = facturas[selected_index]
        factura_filename = f"factura_{selected_factura.id_factura}.txt"

        if os.path.exists(factura_filename):
            with open(factura_filename, "r") as f:
                factura_contenido = f.read()
             # Eliminar todos los widgets de la ventana
            for widget in root.winfo_children():
                widget.destroy()
            
            root.title(f"RECIBO DE LA FACTURA {selected_factura.id_factura}")
            tk.Label(root, text=factura_contenido, justify=tk.LEFT).grid(row=0, column=0, padx=10, pady=10)
            tk.Button(root, text="Descargar archivo").grid(row=1, column=0, columnspan=10)
            tk.Button(root, text="Regresar", command=ver_factura).grid(row=2, column=0, columnspan=10)
            tk.Button(root, text="volver menu principal", command=menu_principal).grid(row=3, column=0, columnspan=10)
            
        else:
            messagebox.showwarning("Advertencia", "El archivo de la factura no existe.")

    boton_pagar_factura = tk.Button(root, text="Mostrar Factura Seleccionada", command=ver_detalles_factura)
    boton_pagar_factura.grid(row=2, column=0, columnspan=2)
    boton_nuevo_cliente = tk.Button(root, text="Añadir nuevo cliente", command=menu_clientes)
    boton_nuevo_cliente.grid(row=3, column=0, columnspan=2)
    boton_volver = tk.Button(root, text="Volver al menú principal", command=volver_menu_principal)
    boton_volver.grid(row=4, column=0, columnspan=2)

# Menú principal
def volver_menu_principal():
    for widget in root.winfo_children():
        widget.destroy()
    menu_principal()

def salir():
    root.quit()

# Función para generar informe de productos agotados
def informe_productos_agotados():
    for widget in root.winfo_children():
        widget.destroy()
    root.title("INFORME")
    label_titulo = tk.Label(root, text="PRODUCTOS AGOTADOS")
    label_titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
    productos_agotados = [p for p in productos if p.cantidad == 0]
    if productos_agotados:
        for i, producto in enumerate(productos_agotados):
            tk.Label(root, text=producto.id_producto).grid(row=i+1, column=0, padx=10)
            tk.Label(root, text=producto.nombre).grid(row=i+1, column=1, padx=10)
    else:
        tk.Label(root, text="No hay productos agotados.").grid(row=1, column=0, columnspan=2)
    boton_volver = tk.Button(root, text="Volver al menú principal", command=volver_menu_principal)
    boton_volver.grid(row=len(productos_agotados)+2, column=0, columnspan=2)
#funcion
def ventas_ultimo_dia():
    hoy = datetime.datetime.now()
    hace_una_semana = hoy - datetime.timedelta(days=7)
    ventas = {producto.id_producto: 0 for producto in productos}
    
    for factura in facturas:
        fecha_factura = datetime.datetime.strptime(factura.fecha_factura, "%d/%m/%Y")
        if fecha_factura >= hace_una_semana:
            for pv in factura.productos_vendidos:
                ventas[pv["id_producto"]] += pv["cantidad"]
    
    return ventas

def informe_baja_rotacion():
    for widget in root.winfo_children():
        widget.destroy()
    root.title("INFORME")
    label_titulo = tk.Label(root, text="PRODUCTOS DE BAJA ROTACIÓN")
    label_titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

    ventas = ventas_ultimo_dia()
    umbral = 5  # Puedes ajustar este umbral según tus necesidades
    productos_baja_rotacion = [p for p in productos if ventas[p.id_producto] < umbral]

    if productos_baja_rotacion:
        for i, producto in enumerate(productos_baja_rotacion):
            tk.Label(root, text=producto.id_producto).grid(row=i+1, column=0, padx=10)
            tk.Label(root, text=producto.nombre).grid(row=i+1, column=1, padx=10)
            tk.Label(root, text=f"Ventas: {ventas[producto.id_producto]}").grid(row=i+1, column=2, padx=10)
    else:
        tk.Label(root, text="No hay productos de baja rotación.").grid(row=1, column=0, columnspan=2)
    
    boton_volver = tk.Button(root, text="Volver al menú principal", command=volver_menu_principal)
    boton_volver.grid(row=len(productos_baja_rotacion)+2, column=0, columnspan=2)
    
# Función para generar informe de ventas
def informe_ventas():
    for widget in root.winfo_children():
        widget.destroy()
    root.title("INFORME")
    label_titulo = tk.Label(root, text="INFORME DE VENTAS")
    label_titulo.grid(row=0, column=0, columnspan=5, padx=10, pady=5)
    atributos = ["Factura ID", "Cliente ID", "Fecha", "Total", "Productos Vendidos"]
    for i, attr in enumerate(atributos):
        tk.Label(root, text=attr.upper()).grid(row=1, column=i, padx=10)
    total_ventas = 0
    for i, factura in enumerate(facturas):
        total_ventas += factura.total_factura
        productos_vendidos_str = ", ".join([f"{pv['cantidad']}x{pv['id_producto']}" for pv in factura.productos_vendidos])
        valores = [factura.id_factura, factura.id_cliente, factura.fecha_factura, factura.total_factura, productos_vendidos_str]
        for j, value in enumerate(valores):
            tk.Label(root, text=value).grid(row=i+2, column=j, padx=10)
    tk.Label(root, text=f"Total de ventas: ${total_ventas}").grid(row=len(facturas)+2, column=0, columnspan=5)
    boton_volver = tk.Button(root, text="Volver al menú principal", command=volver_menu_principal)
    boton_volver.grid(row=len(facturas)+3, column=0, columnspan=5)

# Añadir botones al menú principal para los informes
def menu_principal():
    for wiget in root.winfo_children():
        wiget.destroy()
    
    label_titulo_interfaz = tk.Label(root, text="MENÚ PRINCIPAL")
    label_titulo_interfaz.grid(row=0, column=0)
    root.title("SISTEMA DE VENTAS")
    cliente_boton = tk.Button(root, text="Registrar Cliente", command=menu_clientes)
    cliente_boton.grid(row=1, column=0, padx=10, pady=5)
    producto_boton = tk.Button(root, text="Ver Productos", command=menu_productos)
    producto_boton.grid(row=2, column=0, padx=10, pady=5)
    factura_boton = tk.Button(root, text="Ver Facturas", command=ver_factura)
    factura_boton.grid(row=3, column=0, padx=10, pady=5)
    agotados_boton = tk.Button(root, text="Productos Agotados", command=informe_productos_agotados)
    agotados_boton.grid(row=4, column=0, padx=10, pady=5)
    tk.Button(root, text="Productos de baja rotación", command=informe_baja_rotacion).grid(row=5, column=0, padx=10, pady=5)
    ventas_boton = tk.Button(root, text="Informe de Ventas", command=informe_ventas)
    ventas_boton.grid(row=6, column=0, padx=10, pady=5)
    salir_boton = tk.Button(root, text="Salir del programa", command=salir)
    salir_boton.grid(row=7, column=0, padx=10, pady=5)


# Cargar datos al iniciar
cargar_clientes()
cargar_productos()
cargar_facturas()

informe_productos_agotados()
informe_ventas()
informe_baja_rotacion()
#mostrar menu al iniciar
menu_principal()
#Iniciar el bucle de la ventana
root.mainloop()
