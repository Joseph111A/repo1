import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import bd_funciones as bd
from datetime import datetime

class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario - Tienda")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear pestañas
        self.crear_pestana_productos()
        self.crear_pestana_pedidos()
        self.crear_pestana_clientes()
        
    # ==================== PESTAÑA PRODUCTOS ====================
    
    def crear_pestana_productos(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Productos")
        
        # Frame de búsqueda
        frame_busqueda = ttk.LabelFrame(frame, text="Búsqueda de Productos", padding=10)
        frame_busqueda.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_busqueda, text="Buscar por:").grid(row=0, column=0, sticky=tk.W, padx=5)
        
        # Opciones de búsqueda
        busqueda_frame = ttk.Frame(frame_busqueda)
        busqueda_frame.grid(row=1, column=0, columnspan=3, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(busqueda_frame, text="ID:").pack(side=tk.LEFT, padx=5)
        self.entry_id = ttk.Entry(busqueda_frame, width=10)
        self.entry_id.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(busqueda_frame, text="Nombre:").pack(side=tk.LEFT, padx=5)
        self.entry_nombre = ttk.Entry(busqueda_frame, width=20)
        self.entry_nombre.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(busqueda_frame, text="Precio Min:").pack(side=tk.LEFT, padx=5)
        self.entry_precio_min = ttk.Entry(busqueda_frame, width=10)
        self.entry_precio_min.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(busqueda_frame, text="Precio Max:").pack(side=tk.LEFT, padx=5)
        self.entry_precio_max = ttk.Entry(busqueda_frame, width=10)
        self.entry_precio_max.pack(side=tk.LEFT, padx=5)
        
        # Botones de búsqueda
        botones_busqueda = ttk.Frame(frame_busqueda)
        botones_busqueda.grid(row=2, column=0, columnspan=3, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Button(botones_busqueda, text="Buscar por ID", 
                   command=self.buscar_producto_id).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_busqueda, text="Buscar por Nombre", 
                   command=self.buscar_producto_nombre).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_busqueda, text="Buscar por Precio", 
                   command=self.buscar_producto_precio).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_busqueda, text="Ver Todos", 
                   command=self.ver_todos_productos).pack(side=tk.LEFT, padx=5)
        
        # Frame de acción
        frame_accion = ttk.LabelFrame(frame, text="Acciones", padding=10)
        frame_accion.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(frame_accion, text="Agregar Producto", 
                   command=self.ventana_agregar_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_accion, text="Eliminar Producto", 
                   command=self.eliminar_producto_seleccionado).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_accion, text="Editar Producto", 
                   command=self.ventana_editar_producto).pack(side=tk.LEFT, padx=5)
        
        # Frame de tabla
        frame_tabla = ttk.LabelFrame(frame, text="Lista de Productos", padding=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree_productos = ttk.Treeview(frame_tabla, 
                                           columns=('ID', 'Nombre', 'Precio', 'Stock', 'Categoría', 'Proveedor'),
                                           height=15, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree_productos.yview)
        
        self.tree_productos.column('#0', width=0, stretch=tk.NO)
        self.tree_productos.column('ID', anchor=tk.W, width=50)
        self.tree_productos.column('Nombre', anchor=tk.W, width=150)
        self.tree_productos.column('Precio', anchor=tk.CENTER, width=80)
        self.tree_productos.column('Stock', anchor=tk.CENTER, width=60)
        self.tree_productos.column('Categoría', anchor=tk.W, width=100)
        self.tree_productos.column('Proveedor', anchor=tk.W, width=150)
        
        self.tree_productos.heading('#0', text='', anchor=tk.W)
        self.tree_productos.heading('ID', text='ID', anchor=tk.W)
        self.tree_productos.heading('Nombre', text='Nombre', anchor=tk.W)
        self.tree_productos.heading('Precio', text='Precio', anchor=tk.CENTER)
        self.tree_productos.heading('Stock', text='Stock', anchor=tk.CENTER)
        self.tree_productos.heading('Categoría', text='Categoría', anchor=tk.W)
        self.tree_productos.heading('Proveedor', text='Proveedor', anchor=tk.W)
        
        self.tree_productos.pack(fill=tk.BOTH, expand=True)
        
        self.ver_todos_productos()
    
    def buscar_producto_id(self):
        id_prod = self.entry_id.get()
        if not id_prod:
            messagebox.showwarning("Validación", "Ingrese un ID de producto")
            return
        
        try:
            productos = bd.buscar_producto_por_id(int(id_prod))
            self.mostrar_productos(productos)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número")
    
    def buscar_producto_nombre(self):
        nombre = self.entry_nombre.get()
        if not nombre:
            messagebox.showwarning("Validación", "Ingrese un nombre de producto")
            return
        
        productos = bd.buscar_producto_por_nombre(nombre)
        self.mostrar_productos(productos)
    
    def buscar_producto_precio(self):
        try:
            precio_min = float(self.entry_precio_min.get() or 0)
            precio_max = float(self.entry_precio_max.get() or 99999)
            
            productos = bd.buscar_producto_por_precio(precio_min, precio_max)
            self.mostrar_productos(productos)
        except ValueError:
            messagebox.showerror("Error", "Los precios deben ser números")
    
    def ver_todos_productos(self):
        productos = bd.obtener_productos()
        self.mostrar_productos(productos)
    
    def mostrar_productos(self, productos):
        # Limpiar tabla
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        
        # Agregar productos
        if not productos:
            messagebox.showinfo("Búsqueda", "No se encontraron productos")
            return
        
        for prod in productos:
            self.tree_productos.insert('', 'end', values=(
                prod[0], prod[1], f"${prod[3]:.2f}", prod[4], prod[5], prod[6]
            ))
    
    def ventana_agregar_producto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Producto")
        ventana.geometry("400x500")
        
        ttk.Label(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = ttk.Entry(ventana, width=40)
        entry_nombre.pack(pady=5)
        
        ttk.Label(ventana, text="Descripción:").pack(pady=5)
        entry_desc = ttk.Entry(ventana, width=40)
        entry_desc.pack(pady=5)
        
        ttk.Label(ventana, text="Precio Unitario:").pack(pady=5)
        entry_precio = ttk.Entry(ventana, width=40)
        entry_precio.pack(pady=5)
        
        ttk.Label(ventana, text="Stock Disponible:").pack(pady=5)
        entry_stock = ttk.Entry(ventana, width=40)
        entry_stock.pack(pady=5)
        
        ttk.Label(ventana, text="Categoría:").pack(pady=5)
        combo_categoria = ttk.Combobox(ventana, width=37)
        categorias = bd.obtener_categorias()
        combo_categoria['values'] = [f"{cat[0]} - {cat[1]}" for cat in categorias]
        combo_categoria.pack(pady=5)
        
        ttk.Label(ventana, text="Proveedor:").pack(pady=5)
        combo_proveedor = ttk.Combobox(ventana, width=37)
        proveedores = bd.obtener_proveedores()
        combo_proveedor['values'] = [f"{prov[0]} - {prov[1]}" for prov in proveedores]
        combo_proveedor.pack(pady=5)
        
        def guardar():
            try:
                nombre = entry_nombre.get()
                desc = entry_desc.get()
                precio = float(entry_precio.get())
                stock = int(entry_stock.get())
                cat_idx = combo_categoria.current()
                prov_idx = combo_proveedor.current()
                
                if not nombre:
                    messagebox.showwarning("Validación", "El nombre es requerido")
                    return
                
                if cat_idx == -1 or prov_idx == -1:
                    messagebox.showwarning("Validación", "Seleccione categoría y proveedor")
                    return
                
                id_categoria = categorias[cat_idx][0]
                id_proveedor = proveedores[prov_idx][0]
                
                exito, mensaje = bd.agregar_producto(nombre, desc, precio, stock, id_categoria, id_proveedor)
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    self.ver_todos_productos()
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", mensaje)
            except ValueError:
                messagebox.showerror("Error", "Precio y stock deben ser números")
        
        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=20)
    
    def ventana_editar_producto(self):
        seleccion = self.tree_productos.selection()
        if not seleccion:
            messagebox.showwarning("Validación", "Seleccione un producto")
            return
        
        item = self.tree_productos.item(seleccion[0])
        id_prod = item['values'][0]
        
        productos = bd.buscar_producto_por_id(id_prod)
        if not productos:
            return
        
        prod = productos[0]
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Editar Producto")
        ventana.geometry("400x500")
        
        ttk.Label(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = ttk.Entry(ventana, width=40)
        entry_nombre.insert(0, prod[1])
        entry_nombre.pack(pady=5)
        
        ttk.Label(ventana, text="Descripción:").pack(pady=5)
        entry_desc = ttk.Entry(ventana, width=40)
        entry_desc.insert(0, prod[2] or "")
        entry_desc.pack(pady=5)
        
        ttk.Label(ventana, text="Precio Unitario:").pack(pady=5)
        entry_precio = ttk.Entry(ventana, width=40)
        entry_precio.insert(0, str(prod[3]))
        entry_precio.pack(pady=5)
        
        ttk.Label(ventana, text="Stock Disponible:").pack(pady=5)
        entry_stock = ttk.Entry(ventana, width=40)
        entry_stock.insert(0, str(prod[4]))
        entry_stock.pack(pady=5)
        
        ttk.Label(ventana, text="Categoría:").pack(pady=5)
        combo_categoria = ttk.Combobox(ventana, width=37)
        categorias = bd.obtener_categorias()
        combo_categoria['values'] = [f"{cat[0]} - {cat[1]}" for cat in categorias]
        combo_categoria.pack(pady=5)
        
        ttk.Label(ventana, text="Proveedor:").pack(pady=5)
        combo_proveedor = ttk.Combobox(ventana, width=37)
        proveedores = bd.obtener_proveedores()
        combo_proveedor['values'] = [f"{prov[0]} - {prov[1]}" for prov in proveedores]
        combo_proveedor.pack(pady=5)
        
        def actualizar():
            try:
                nombre = entry_nombre.get()
                desc = entry_desc.get()
                precio = float(entry_precio.get())
                stock = int(entry_stock.get())
                cat_idx = combo_categoria.current()
                prov_idx = combo_proveedor.current()
                
                if not nombre:
                    messagebox.showwarning("Validación", "El nombre es requerido")
                    return
                
                if cat_idx == -1 or prov_idx == -1:
                    messagebox.showwarning("Validación", "Seleccione categoría y proveedor")
                    return
                
                id_categoria = categorias[cat_idx][0]
                id_proveedor = proveedores[prov_idx][0]
                
                exito, mensaje = bd.actualizar_producto(id_prod, nombre, desc, precio, stock, id_categoria, id_proveedor)
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    self.ver_todos_productos()
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", mensaje)
            except ValueError:
                messagebox.showerror("Error", "Precio y stock deben ser números")
        
        ttk.Button(ventana, text="Actualizar", command=actualizar).pack(pady=20)
    
    def eliminar_producto_seleccionado(self):
        seleccion = self.tree_productos.selection()
        if not seleccion:
            messagebox.showwarning("Validación", "Seleccione un producto")
            return
        
        item = self.tree_productos.item(seleccion[0])
        id_prod = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar producto {id_prod}?"):
            exito, mensaje = bd.eliminar_producto(id_prod)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.ver_todos_productos()
            else:
                messagebox.showerror("Error", mensaje)
    
    # ==================== PESTAÑA PEDIDOS ====================
    
    def crear_pestana_pedidos(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Pedidos")
        
        # Frame de búsqueda
        frame_busqueda = ttk.LabelFrame(frame, text="Búsqueda de Pedidos", padding=10)
        frame_busqueda.pack(fill=tk.X, padx=10, pady=10)
        
        busqueda_frame = ttk.Frame(frame_busqueda)
        busqueda_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(busqueda_frame, text="ID Pedido:").pack(side=tk.LEFT, padx=5)
        self.entry_id_pedido = ttk.Entry(busqueda_frame, width=15)
        self.entry_id_pedido.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(busqueda_frame, text="ID Cliente:").pack(side=tk.LEFT, padx=5)
        self.entry_id_cliente = ttk.Entry(busqueda_frame, width=15)
        self.entry_id_cliente.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(busqueda_frame, text="Estado:").pack(side=tk.LEFT, padx=5)
        self.combo_estado = ttk.Combobox(busqueda_frame, width=15, 
                                         values=["Pendiente", "Completado", "Cancelado"])
        self.combo_estado.pack(side=tk.LEFT, padx=5)
        
        # Botones búsqueda
        botones_busqueda = ttk.Frame(frame_busqueda)
        botones_busqueda.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(botones_busqueda, text="Buscar por ID", 
                   command=self.buscar_pedido_id).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_busqueda, text="Buscar por Cliente", 
                   command=self.buscar_pedido_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_busqueda, text="Buscar por Estado", 
                   command=self.buscar_pedido_estado).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_busqueda, text="Ver Todos", 
                   command=self.ver_todos_pedidos).pack(side=tk.LEFT, padx=5)
        
        # Frame de acción
        frame_accion = ttk.LabelFrame(frame, text="Acciones", padding=10)
        frame_accion.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(frame_accion, text="Agregar Pedido", 
                   command=self.ventana_agregar_pedido).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_accion, text="Cambiar Estado", 
                   command=self.cambiar_estado_pedido).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_accion, text="Ver Detalles", 
                   command=self.ver_detalles_pedido).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_accion, text="Cancelar Pedido", 
                   command=self.cancelar_pedido).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_accion, text="Eliminar Pedido", 
                   command=self.eliminar_pedido_seleccionado).pack(side=tk.LEFT, padx=5)
        
        # Frame de tabla
        frame_tabla = ttk.LabelFrame(frame, text="Lista de Pedidos", padding=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree_pedidos = ttk.Treeview(frame_tabla, 
                                         columns=('ID', 'Fecha', 'Total', 'Estado', 'Cliente'),
                                         height=15, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree_pedidos.yview)
        
        self.tree_pedidos.column('#0', width=0, stretch=tk.NO)
        self.tree_pedidos.column('ID', anchor=tk.W, width=50)
        self.tree_pedidos.column('Fecha', anchor=tk.W, width=100)
        self.tree_pedidos.column('Total', anchor=tk.CENTER, width=80)
        self.tree_pedidos.column('Estado', anchor=tk.CENTER, width=100)
        self.tree_pedidos.column('Cliente', anchor=tk.W, width=300)
        
        self.tree_pedidos.heading('#0', text='', anchor=tk.W)
        self.tree_pedidos.heading('ID', text='ID', anchor=tk.W)
        self.tree_pedidos.heading('Fecha', text='Fecha', anchor=tk.W)
        self.tree_pedidos.heading('Total', text='Total', anchor=tk.CENTER)
        self.tree_pedidos.heading('Estado', text='Estado', anchor=tk.CENTER)
        self.tree_pedidos.heading('Cliente', text='Cliente', anchor=tk.W)
        
        self.tree_pedidos.pack(fill=tk.BOTH, expand=True)
        
        self.ver_todos_pedidos()
    
    def buscar_pedido_id(self):
        id_pedido = self.entry_id_pedido.get()
        if not id_pedido:
            messagebox.showwarning("Validación", "Ingrese un ID de pedido")
            return
        
        try:
            pedidos = bd.buscar_pedido_por_id(int(id_pedido))
            self.mostrar_pedidos(pedidos)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número")
    
    def buscar_pedido_cliente(self):
        id_cliente = self.entry_id_cliente.get()
        if not id_cliente:
            messagebox.showwarning("Validación", "Ingrese un ID de cliente")
            return
        
        try:
            pedidos = bd.buscar_pedido_por_cliente(int(id_cliente))
            self.mostrar_pedidos(pedidos)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número")
    
    def buscar_pedido_estado(self):
        estado = self.combo_estado.get()
        if not estado:
            messagebox.showwarning("Validación", "Seleccione un estado")
            return
        
        pedidos = bd.buscar_pedido_por_estado(estado)
        self.mostrar_pedidos(pedidos)
    
    def ver_todos_pedidos(self):
        pedidos = bd.obtener_pedidos()
        self.mostrar_pedidos(pedidos)
    
    def mostrar_pedidos(self, pedidos):
        # Limpiar tabla
        for item in self.tree_pedidos.get_children():
            self.tree_pedidos.delete(item)
        
        if not pedidos:
            messagebox.showinfo("Búsqueda", "No se encontraron pedidos")
            return
        
        for ped in pedidos:
            self.tree_pedidos.insert('', 'end', values=(
                ped[0], ped[1], f"${ped[2]:.2f}" if ped[2] else "$0.00", ped[3], 
                f"{ped[5]} {ped[6]}" if ped[5] else "N/A"
            ))
    
    def ventana_agregar_pedido(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Pedido")
        ventana.geometry("400x300")
        
        ttk.Label(ventana, text="Cliente:").pack(pady=5)
        combo_cliente = ttk.Combobox(ventana, width=40)
        clientes = bd.obtener_clientes()
        combo_cliente['values'] = [f"{cli[0]} - {cli[1]} {cli[2]}" for cli in clientes]
        combo_cliente.pack(pady=5)
        
        ttk.Label(ventana, text="Total:").pack(pady=5)
        entry_total = ttk.Entry(ventana, width=40)
        entry_total.pack(pady=5)
        
        def guardar():
            try:
                cli_idx = combo_cliente.current()
                total = float(entry_total.get() or 0)
                
                if cli_idx == -1:
                    messagebox.showwarning("Validación", "Seleccione un cliente")
                    return
                
                id_cliente = clientes[cli_idx][0]
                
                exito, mensaje, id_pedido = bd.agregar_pedido(id_cliente, total)
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    self.ver_todos_pedidos()
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", mensaje)
            except ValueError:
                messagebox.showerror("Error", "El total debe ser un número")
        
        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=20)
    
    def cambiar_estado_pedido(self):
        seleccion = self.tree_pedidos.selection()
        if not seleccion:
            messagebox.showwarning("Validación", "Seleccione un pedido")
            return
        
        item = self.tree_pedidos.item(seleccion[0])
        id_pedido = item['values'][0]
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Cambiar Estado")
        ventana.geometry("300x150")
        
        ttk.Label(ventana, text="Nuevo Estado:").pack(pady=10)
        combo_estado = ttk.Combobox(ventana, width=30, 
                                    values=["Pendiente", "Completado", "Cancelado"])
        combo_estado.pack(pady=10)
        
        def actualizar():
            estado = combo_estado.get()
            if not estado:
                messagebox.showwarning("Validación", "Seleccione un estado")
                return
            
            exito, mensaje = bd.actualizar_estado_pedido(id_pedido, estado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.ver_todos_pedidos()
                ventana.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        
        ttk.Button(ventana, text="Actualizar", command=actualizar).pack(pady=10)
    
    def ver_detalles_pedido(self):
        seleccion = self.tree_pedidos.selection()
        if not seleccion:
            messagebox.showwarning("Validación", "Seleccione un pedido")
            return
        
        item = self.tree_pedidos.item(seleccion[0])
        id_pedido = item['values'][0]
        
        detalles = bd.obtener_detalles_pedido(id_pedido)
        
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Detalles del Pedido {id_pedido}")
        ventana.geometry("600x400")
        
        # Treeview
        tree = ttk.Treeview(ventana, 
                           columns=('ID', 'Producto', 'Cantidad', 'Precio', 'Subtotal'),
                           height=15)
        
        tree.column('#0', width=0, stretch=tk.NO)
        tree.column('ID', anchor=tk.W, width=50)
        tree.column('Producto', anchor=tk.W, width=150)
        tree.column('Cantidad', anchor=tk.CENTER, width=80)
        tree.column('Precio', anchor=tk.CENTER, width=80)
        tree.column('Subtotal', anchor=tk.CENTER, width=80)
        
        tree.heading('#0', text='', anchor=tk.W)
        tree.heading('ID', text='ID', anchor=tk.W)
        tree.heading('Producto', text='Producto', anchor=tk.W)
        tree.heading('Cantidad', text='Cantidad', anchor=tk.CENTER)
        tree.heading('Precio', text='Precio', anchor=tk.CENTER)
        tree.heading('Subtotal', text='Subtotal', anchor=tk.CENTER)
        
        for det in detalles:
            tree.insert('', 'end', values=(
                det[0], det[6], det[3], f"${det[4]:.2f}", f"${det[5]:.2f}"
            ))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def cancelar_pedido(self):
        seleccion = self.tree_pedidos.selection()
        if not seleccion:
            messagebox.showwarning("Validación", "Seleccione un pedido")
            return
        
        item = self.tree_pedidos.item(seleccion[0])
        id_pedido = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"¿Cancelar pedido {id_pedido}?"):
            exito, mensaje = bd.actualizar_estado_pedido(id_pedido, "Cancelado")
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.ver_todos_pedidos()
            else:
                messagebox.showerror("Error", mensaje)
    
    def eliminar_pedido_seleccionado(self):
        seleccion = self.tree_pedidos.selection()
        if not seleccion:
            messagebox.showwarning("Validación", "Seleccione un pedido")
            return
        
        item = self.tree_pedidos.item(seleccion[0])
        id_pedido = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar pedido {id_pedido}?"):
            exito, mensaje = bd.eliminar_pedido(id_pedido)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.ver_todos_pedidos()
            else:
                messagebox.showerror("Error", mensaje)
    
    # ==================== PESTAÑA CLIENTES ====================
    
    def crear_pestana_clientes(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Clientes")
        
        # Frame de búsqueda
        frame_busqueda = ttk.LabelFrame(frame, text="Búsqueda de Clientes", padding=10)
        frame_busqueda.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_busqueda, text="ID:").pack(side=tk.LEFT, padx=5)
        self.entry_id_cliente_bus = ttk.Entry(frame_busqueda, width=15)
        self.entry_id_cliente_bus.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame_busqueda, text="Nombre:").pack(side=tk.LEFT, padx=5)
        self.entry_nombre_cliente_bus = ttk.Entry(frame_busqueda, width=20)
        self.entry_nombre_cliente_bus.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_busqueda, text="Buscar por ID", 
                   command=self.buscar_cliente_id).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_busqueda, text="Buscar por Nombre", 
                   command=self.buscar_cliente_nombre).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_busqueda, text="Ver Todos", 
                   command=self.ver_todos_clientes).pack(side=tk.LEFT, padx=5)
        
        # Frame de acción
        frame_accion = ttk.LabelFrame(frame, text="Acciones", padding=10)
        frame_accion.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(frame_accion, text="Agregar Cliente", 
                   command=self.ventana_agregar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_accion, text="Editar Cliente", 
                   command=self.ventana_editar_cliente).pack(side=tk.LEFT, padx=5)
        
        # Frame de tabla
        frame_tabla = ttk.LabelFrame(frame, text="Lista de Clientes", padding=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree_clientes = ttk.Treeview(frame_tabla, 
                                          columns=('ID', 'Nombre', 'Apellido', 'Email', 'Teléfono', 'Dirección'),
                                          height=15, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree_clientes.yview)
        
        self.tree_clientes.column('#0', width=0, stretch=tk.NO)
        self.tree_clientes.column('ID', anchor=tk.W, width=50)
        self.tree_clientes.column('Nombre', anchor=tk.W, width=100)
        self.tree_clientes.column('Apellido', anchor=tk.W, width=100)
        self.tree_clientes.column('Email', anchor=tk.W, width=150)
        self.tree_clientes.column('Teléfono', anchor=tk.CENTER, width=100)
        self.tree_clientes.column('Dirección', anchor=tk.W, width=200)
        
        self.tree_clientes.heading('#0', text='', anchor=tk.W)
        self.tree_clientes.heading('ID', text='ID', anchor=tk.W)
        self.tree_clientes.heading('Nombre', text='Nombre', anchor=tk.W)
        self.tree_clientes.heading('Apellido', text='Apellido', anchor=tk.W)
        self.tree_clientes.heading('Email', text='Email', anchor=tk.W)
        self.tree_clientes.heading('Teléfono', text='Teléfono', anchor=tk.CENTER)
        self.tree_clientes.heading('Dirección', text='Dirección', anchor=tk.W)
        
        self.tree_clientes.pack(fill=tk.BOTH, expand=True)
        
        self.ver_todos_clientes()
    
    def buscar_cliente_id(self):
        id_cliente = self.entry_id_cliente_bus.get()
        if not id_cliente:
            messagebox.showwarning("Validación", "Ingrese un ID de cliente")
            return
        
        try:
            clientes = bd.buscar_cliente_por_id(int(id_cliente))
            self.mostrar_clientes(clientes)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número")
    
    def buscar_cliente_nombre(self):
        nombre = self.entry_nombre_cliente_bus.get()
        if not nombre:
            messagebox.showwarning("Validación", "Ingrese un nombre")
            return
        
        clientes = bd.buscar_cliente_por_nombre(nombre)
        self.mostrar_clientes(clientes)
    
    def ver_todos_clientes(self):
        clientes = bd.obtener_clientes()
        self.mostrar_clientes(clientes)
    
    def mostrar_clientes(self, clientes):
        # Limpiar tabla
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        if not clientes:
            messagebox.showinfo("Búsqueda", "No se encontraron clientes")
            return
        
        for cli in clientes:
            self.tree_clientes.insert('', 'end', values=(
                cli[0], cli[1], cli[2], cli[3] or "N/A", cli[4] or "N/A", cli[5] or "N/A"
            ))
    
    def ventana_agregar_cliente(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Cliente")
        ventana.geometry("400x400")
        
        ttk.Label(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = ttk.Entry(ventana, width=40)
        entry_nombre.pack(pady=5)
        
        ttk.Label(ventana, text="Apellido:").pack(pady=5)
        entry_apellido = ttk.Entry(ventana, width=40)
        entry_apellido.pack(pady=5)
        
        ttk.Label(ventana, text="Email:").pack(pady=5)
        entry_email = ttk.Entry(ventana, width=40)
        entry_email.pack(pady=5)
        
        ttk.Label(ventana, text="Teléfono:").pack(pady=5)
        entry_telefono = ttk.Entry(ventana, width=40)
        entry_telefono.pack(pady=5)
        
        ttk.Label(ventana, text="Dirección:").pack(pady=5)
        entry_direccion = ttk.Entry(ventana, width=40)
        entry_direccion.pack(pady=5)
        
        def guardar():
            nombre = entry_nombre.get()
            apellido = entry_apellido.get()
            email = entry_email.get()
            telefono = entry_telefono.get()
            direccion = entry_direccion.get()
            
            if not nombre or not apellido:
                messagebox.showwarning("Validación", "Nombre y apellido son requeridos")
                return
            
            exito, mensaje = bd.agregar_cliente(nombre, apellido, email, telefono, direccion)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.ver_todos_clientes()
                ventana.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        
        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=20)
    
    def ventana_editar_cliente(self):
        seleccion = self.tree_clientes.selection()
        if not seleccion:
            messagebox.showwarning("Validación", "Seleccione un cliente")
            return
        
        item = self.tree_clientes.item(seleccion[0])
        id_cliente = item['values'][0]
        
        clientes = bd.buscar_cliente_por_id(id_cliente)
        if not clientes:
            return
        
        cli = clientes[0]
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Editar Cliente")
        ventana.geometry("400x400")
        
        ttk.Label(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = ttk.Entry(ventana, width=40)
        entry_nombre.insert(0, cli[1])
        entry_nombre.pack(pady=5)
        
        ttk.Label(ventana, text="Apellido:").pack(pady=5)
        entry_apellido = ttk.Entry(ventana, width=40)
        entry_apellido.insert(0, cli[2])
        entry_apellido.pack(pady=5)
        
        ttk.Label(ventana, text="Email:").pack(pady=5)
        entry_email = ttk.Entry(ventana, width=40)
        entry_email.insert(0, cli[3] or "")
        entry_email.pack(pady=5)
        
        ttk.Label(ventana, text="Teléfono:").pack(pady=5)
        entry_telefono = ttk.Entry(ventana, width=40)
        entry_telefono.insert(0, cli[4] or "")
        entry_telefono.pack(pady=5)
        
        ttk.Label(ventana, text="Dirección:").pack(pady=5)
        entry_direccion = ttk.Entry(ventana, width=40)
        entry_direccion.insert(0, cli[5] or "")
        entry_direccion.pack(pady=5)
        
        def actualizar():
            nombre = entry_nombre.get()
            apellido = entry_apellido.get()
            email = entry_email.get()
            telefono = entry_telefono.get()
            direccion = entry_direccion.get()
            
            if not nombre or not apellido:
                messagebox.showwarning("Validación", "Nombre y apellido son requeridos")
                return
            
            exito, mensaje = bd.actualizar_cliente(id_cliente, nombre, apellido, email, telefono, direccion)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.ver_todos_clientes()
                ventana.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        
        ttk.Button(ventana, text="Actualizar", command=actualizar).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()
