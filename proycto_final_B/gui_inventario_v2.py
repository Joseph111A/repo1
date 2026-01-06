import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from datetime import date

"""
gui_inventario_v2.py
--------------------
Interfaz gráfica (Tkinter) para gestionar la base de datos `inventario_db`.

Esta aplicación proporciona CRUD para productos y clientes, y un
flujo maestro-detalle para crear pedidos (añadir líneas, crear pedido,
actualizar stock). El archivo contiene utilidades de conexión a MySQL
y varias ventanas/frames: `ProductosFrame`, `ClientesFrame`, `PedidosFrame`,
`NuevoPedidoWindow`, `DetallePedidoWindow`.

Instrucciones rápidas:
 - Asegúrate de que MySQL está en ejecución y `DB_CONFIG` es correcto.
 - Ejecuta `python gui_inventario_v2.py` para abrir la aplicación.

Notas de diseño:
 - Cada operación usa `get_connection()` para abrir/usar/cerrar una
     conexión. Las funciones `db_select` y `db_execute` simplifican
     operaciones comunes.
 - Las operaciones compuestas (crear pedido) hacen commit sólo al
     final de las series de queries para mantener consistencia.
"""

# -------------------------
# CONFIGURACIÓN DB
# -------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",     # cambia si tienes clave
    "database": "inventario_db"
}

# -------------------------
# UTILIDADES DB
# -------------------------
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def db_select(query, params=()):
    """Ejecuta una consulta SELECT y devuelve lista de diccionarios.

    Args:
        query (str): sentencia SQL (con placeholders %s).
        params (tuple): parámetros para la consulta.

    Returns:
        list[dict]: filas resultantes, cada una como diccionario (cursor dictionary=True).
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def db_execute(query, params=(), commit=True):
    """Ejecuta una sentencia de modificación (INSERT/UPDATE/DELETE).

    Si `commit` es True (por defecto), hace commit antes de cerrar la conexión.

    Devuelve `lastrowid` del cursor, útil para INSERTs.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    if commit:
        conn.commit()
    lastrow = cur.lastrowid
    cur.close()
    conn.close()
    return lastrow

# -----------------------------------
# GUI Principal
# -----------------------------------
class InventarioApp(tk.Tk):
    def __init__(self):
        """Ventana principal que agrupa los diferentes módulos (pestañas).

        Crea un `ttk.Notebook` con las pestañas de Productos, Clientes y Pedidos.
        Cada pestaña se implementa en su propia clase (frame) para mantener
        el código organizado.
        """
        super().__init__()
        self.title("Gestión de Inventario - Productos / Clientes / Pedidos")
        self.geometry("1100x650")
        self.resizable(True, True)

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True)

        self.productos_frame = ProductosFrame(nb)
        self.clientes_frame = ClientesFrame(nb)
        self.pedidos_frame = PedidosFrame(nb)

        nb.add(self.productos_frame, text="Productos")
        nb.add(self.clientes_frame, text="Clientes")
        nb.add(self.pedidos_frame, text="Pedidos")

# -----------------------------------------------------------------
#                      FRAME  PRODUCTOS
# -----------------------------------------------------------------
class ProductosFrame(ttk.Frame):
    def __init__(self, container):
        """Frame para gestionar productos.

        Contiene:
        - Búsqueda y filtros.
        - Formulario para crear/editar productos.
        - Tabla (Treeview) con la lista de productos.
        """
        super().__init__(container)

        # --------------- BÚSQUEDA ---------------
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=8, pady=6)

        ttk.Label(search_frame, text="Buscar:").grid(row=0, column=0)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=4)

        ttk.Label(search_frame, text="Por:").grid(row=0, column=2)
        self.search_cb = ttk.Combobox(search_frame, state="readonly", width=20,
             values=["ID", "Nombre", "Stock", "Precio", "Categoría", "Proveedor"])
        self.search_cb.grid(row=0, column=3, padx=4)

        ttk.Button(search_frame, text="Buscar", command=self.buscar_producto)\
            .grid(row=0, column=4, padx=4)

        ttk.Button(search_frame, text="Mostrar Todo", command=self.cargar_productos)\
            .grid(row=0, column=5, padx=4)

        # --------------- FORMULARIO ---------------
        form = ttk.Frame(self)
        form.pack(fill="x", padx=8, pady=6)

        ttk.Label(form, text="Nombre:").grid(row=0, column=0, sticky="w")
        self.nombre_entry = ttk.Entry(form, width=25)
        self.nombre_entry.grid(row=0, column=1, padx=4)

        ttk.Label(form, text="Stock:").grid(row=0, column=2, sticky="w")
        self.stock_entry = ttk.Entry(form, width=10)
        self.stock_entry.grid(row=0, column=3, padx=4)

        ttk.Label(form, text="Precio:").grid(row=0, column=4, sticky="w")
        self.precio_entry = ttk.Entry(form, width=12)
        self.precio_entry.grid(row=0, column=5, padx=4)

        ttk.Label(form, text="Categoría:").grid(row=1, column=0, sticky="w", pady=6)
        self.categoria_cb = ttk.Combobox(form, state="readonly", width=25)
        self.categoria_cb.grid(row=1, column=1, padx=4, sticky="w")

        ttk.Button(form, text="Agregar", command=self.agregar_producto)\
            .grid(row=1, column=3, padx=4)
        ttk.Button(form, text="Editar", command=self.editar_producto)\
            .grid(row=1, column=4, padx=4)
        ttk.Button(form, text="Eliminar", command=self.eliminar_producto)\
            .grid(row=1, column=5, padx=4)

        # --------------- TABLA PRODUCTOS ---------------
        cols = ("id_producto","nombre","stock","precio","categoria")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=8, pady=6)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        ttk.Button(self, text="Refrescar", command=self.cargar_productos)\
            .pack(side="right", padx=8, pady=6)

        self.cargar_categorias()
        self.cargar_productos()

    # ------------------------- BÚSQUEDA -------------------------
    def buscar_producto(self):
        """Buscar productos según campo seleccionado.

        El campo se selecciona en el combobox `self.search_cb` y
        el texto a buscar en `self.search_entry`.
        """
        texto = self.search_entry.get().strip()
        campo = self.search_cb.get()

        if not texto or not campo:
            messagebox.showwarning("Atención", "Ingresa un valor y un campo.")
            return

        query = """
            SELECT p.id_producto, p.nombre, p.stock, p.precio,
                   c.nombre AS categoria
            FROM producto p
            LEFT JOIN categoria c ON c.id_categoria = p.id_categoria
            LEFT JOIN proveedor_producto pp ON pp.id_producto = p.id_producto
            LEFT JOIN proveedor pr ON pr.id_proveedor = pp.id_proveedor
            WHERE 
        """

        if campo == "ID":
            query += "p.id_producto = %s"
        elif campo == "Nombre":
            query += "p.nombre LIKE %s"
            texto = f"%{texto}%"
        elif campo == "Stock":
            query += "p.stock = %s"
        elif campo == "Precio":
            query += "p.precio = %s"
        elif campo == "Categoría":
            query += "c.nombre LIKE %s"
            texto = f"%{texto}%"
        elif campo == "Proveedor":
            query += "pr.nombre LIKE %s"
            texto = f"%{texto}%"

        rows = db_select(query, (texto,))

        for r in self.tree.get_children():
            self.tree.delete(r)

        for r in rows:
            self.tree.insert("", "end",
                values=(r["id_producto"], r["nombre"], r["stock"],
                        float(r["precio"]), r["categoria"] or "")
            )

    # ------------------------- CRUD PRODUCTOS -------------------------
    def cargar_categorias(self):
        """Carga todas las categorías desde la BD y actualiza el Combobox.

        Guarda un diccionario `self.categorias` que mapea nombre -> id.
        """
        rows = db_select("SELECT * FROM categoria")
        self.categorias = {r["nombre"]: r["id_categoria"] for r in rows}
        self.categoria_cb["values"] = list(self.categorias.keys())

    def cargar_productos(self):
        """Carga todos los productos y los muestra en el Treeview.

        Convierte `precio` a float para mostrarlo correctamente.
        """
        for r in self.tree.get_children():
            self.tree.delete(r)
        rows = db_select("""
            SELECT p.id_producto,p.nombre,p.stock,p.precio,c.nombre as categoria
            FROM producto p 
            LEFT JOIN categoria c ON c.id_categoria=p.id_categoria
        """)
        for r in rows:
            self.tree.insert("", "end",
                values=(r["id_producto"], r["nombre"], r["stock"],
                        float(r["precio"]), r["categoria"] or "")
            )

    def agregar_producto(self):
        try:
            nombre = self.nombre_entry.get().strip()
            stock = int(self.stock_entry.get().strip())
            precio = float(self.precio_entry.get().strip())
            categoria = self.categoria_cb.get()
            cat_id = self.categorias.get(categoria)

            db_execute(
                "INSERT INTO producto (nombre,stock,precio,id_categoria) VALUES (%s,%s,%s,%s)",
                (nombre, stock, precio, cat_id)
            )
            messagebox.showinfo("OK", "Producto agregado.")
            self.cargar_productos()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def editar_producto(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un producto.")
            return
        item = self.tree.item(sel[0])["values"]
        id_prod = item[0]

        try:
            nombre = self.nombre_entry.get().strip()
            stock = int(self.stock_entry.get().strip())
            precio = float(self.precio_entry.get().strip())
            categoria = self.categoria_cb.get()
            cat_id = self.categorias.get(categoria)

            db_execute("""
                UPDATE producto SET nombre=%s, stock=%s, precio=%s,
                id_categoria=%s WHERE id_producto=%s
            """, (nombre, stock, precio, cat_id, id_prod))

            messagebox.showinfo("OK", "Producto actualizado.")
            self.cargar_productos()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_producto(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un producto.")
            return

        idp = self.tree.item(sel[0])["values"][0]

        if messagebox.askyesno("Confirmar", "¿Eliminar producto?"):
            try:
                db_execute("DELETE FROM proveedor_producto WHERE id_producto=%s", (idp,))
                db_execute("DELETE FROM detalle_pedido WHERE id_producto=%s", (idp,))
                db_execute("DELETE FROM producto WHERE id_producto=%s", (idp,))
                messagebox.showinfo("OK", "Producto eliminado.")
                self.cargar_productos()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])["values"]
        self.nombre_entry.delete(0, tk.END); self.nombre_entry.insert(0, item[1])
        self.stock_entry.delete(0, tk.END); self.stock_entry.insert(0, item[2])
        self.precio_entry.delete(0, tk.END); self.precio_entry.insert(0, item[3])
        self.categoria_cb.set(item[4] if item[4] else "")


# -----------------------------------------------------------------
#                      FRAME  CLIENTES
# -----------------------------------------------------------------
class ClientesFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # --------------- BÚSQUEDA ---------------
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=8, pady=6)

        ttk.Label(search_frame, text="Buscar:").grid(row=0, column=0)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=4)

        ttk.Label(search_frame, text="Por:").grid(row=0, column=2)
        self.search_cb = ttk.Combobox(
            search_frame, state="readonly", width=20,
            values=["Cédula", "Nombre", "Apellido", "Teléfono", "Dirección"]
        )
        self.search_cb.grid(row=0, column=3, padx=4)

        ttk.Button(search_frame, text="Buscar", command=self.buscar_cliente)\
            .grid(row=0, column=4, padx=4)

        ttk.Button(search_frame, text="Mostrar Todo", command=self.cargar_clientes)\
            .grid(row=0, column=5, padx=4)

        # ---------------------------------------------------
        # FORMULARIO CLIENTE
        # ---------------------------------------------------
        form = ttk.Frame(self)
        form.pack(fill="x", padx=8, pady=6)

        ttk.Label(form, text="Cédula:").grid(row=0, column=0, sticky="w")
        self.cedula_entry = ttk.Entry(form, width=20)
        self.cedula_entry.grid(row=0, column=1, padx=4)

        ttk.Label(form, text="Nombre:").grid(row=0, column=2, sticky="w")
        self.nombre_entry = ttk.Entry(form, width=20)
        self.nombre_entry.grid(row=0, column=3, padx=4)

        ttk.Label(form, text="Apellido:").grid(row=0, column=4, sticky="w")
        self.apellido_entry = ttk.Entry(form, width=20)
        self.apellido_entry.grid(row=0, column=5, padx=4)

        ttk.Label(form, text="Teléfono:").grid(row=1, column=0, sticky="w", pady=6)
        self.telefono_entry = ttk.Entry(form, width=20)
        self.telefono_entry.grid(row=1, column=1, padx=4)

        ttk.Label(form, text="Dirección:").grid(row=1, column=2, sticky="w")
        self.direccion_entry = ttk.Entry(form, width=40)
        self.direccion_entry.grid(row=1, column=3, columnspan=3, padx=4, sticky="w")

        # BOTONES CRUD
        ttk.Button(form, text="Agregar", command=self.agregar_cliente)\
            .grid(row=2, column=3, padx=4, pady=6)
        ttk.Button(form, text="Editar", command=self.editar_cliente)\
            .grid(row=2, column=4, padx=4, pady=6)
        ttk.Button(form, text="Eliminar", command=self.eliminar_cliente)\
            .grid(row=2, column=5, padx=4, pady=6)

        # ---------------------------------------------------
        # TABLA CLIENTES
        # ---------------------------------------------------
        cols = ("cedula","nombre","apellido","telefono","direccion")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=8, pady=6)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        ttk.Button(self, text="Refrescar", command=self.cargar_clientes)\
            .pack(side="right", padx=8, pady=6)

        self.cargar_clientes()

    # ---------------------------------------------------
    # BÚSQUEDA CLIENTES
    # ---------------------------------------------------
    def buscar_cliente(self):
        texto = self.search_entry.get().strip()
        campo = self.search_cb.get()

        if not texto or not campo:
            messagebox.showwarning("Atención", "Completa los datos de búsqueda.")
            return

        campos_sql = {
            "Cédula": "cedula",
            "Nombre": "nombre",
            "Apellido": "apellido",
            "Teléfono": "telefono",
            "Dirección": "direccion",
        }

        col = campos_sql[campo]

        query = f"SELECT * FROM cliente WHERE {col} LIKE %s"
        texto = f"%{texto}%"

        rows = db_select(query, (texto,))

        for r in self.tree.get_children():
            self.tree.delete(r)

        for r in rows:
            self.tree.insert("", "end",
                values=(r["cedula"], r["nombre"], r["apellido"], r["telefono"], r["direccion"])
            )

    # ---------------------------------------------------
    # CRUD CLIENTES
    # ---------------------------------------------------
    def cargar_clientes(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        rows = db_select("SELECT * FROM cliente")
        for r in rows:
            self.tree.insert("", "end",
                values=(r["cedula"], r["nombre"], r["apellido"], r["telefono"], r["direccion"])
            )

    def agregar_cliente(self):
        try:
            cedula = int(self.cedula_entry.get().strip())
            nombre = self.nombre_entry.get().strip()
            apellido = self.apellido_entry.get().strip()
            telefono = self.telefono_entry.get().strip()
            direccion = self.direccion_entry.get().strip()

            if not nombre or not apellido:
                messagebox.showwarning("Atención", "Nombre y apellido son obligatorios.")
                return

            db_execute("""
                INSERT INTO cliente (cedula,nombre,apellido,telefono,direccion)
                VALUES (%s,%s,%s,%s,%s)
            """, (cedula, nombre, apellido, telefono, direccion))

            messagebox.showinfo("OK", "Cliente agregado.")
            self.cargar_clientes()

        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Error", "La cédula ya existe.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def editar_cliente(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un cliente.")
            return

        cedula_original = self.tree.item(sel[0])["values"][0]

        try:
            cedula = int(self.cedula_entry.get().strip())
            nombre = self.nombre_entry.get().strip()
            apellido = self.apellido_entry.get().strip()
            telefono = self.telefono_entry.get().strip()
            direccion = self.direccion_entry.get().strip()

            if not nombre or not apellido:
                messagebox.showwarning("Atención", "Nombre y apellido obligatorios.")
                return

            db_execute("""
                UPDATE cliente 
                SET cedula=%s, nombre=%s, apellido=%s, telefono=%s, direccion=%s
                WHERE cedula=%s
            """, (cedula, nombre, apellido, telefono, direccion, cedula_original))

            messagebox.showinfo("OK", "Cliente actualizado.")
            self.cargar_clientes()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_cliente(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un cliente.")
            return

        cedula = self.tree.item(sel[0])["values"][0]

        if not messagebox.askyesno("Confirmar", "¿Eliminar cliente y todos sus pedidos?"):
            return

        try:
            pedidos = db_select("SELECT id_pedido FROM pedido WHERE cedula=%s", (cedula,))
            for p in pedidos:
                db_execute("DELETE FROM detalle_pedido WHERE id_pedido=%s", (p["id_pedido"],))
            db_execute("DELETE FROM pedido WHERE cedula=%s", (cedula,))
            db_execute("DELETE FROM cliente WHERE cedula=%s", (cedula,))

            messagebox.showinfo("OK", "Cliente y pedidos eliminados.")
            self.cargar_clientes()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return

        item = self.tree.item(sel[0])["values"]
        self.cedula_entry.delete(0, tk.END); self.cedula_entry.insert(0, item[0])
        self.nombre_entry.delete(0, tk.END); self.nombre_entry.insert(0, item[1])
        self.apellido_entry.delete(0, tk.END); self.apellido_entry.insert(0, item[2])
        self.telefono_entry.delete(0, tk.END); self.telefono_entry.insert(0, item[3])
        self.direccion_entry.delete(0, tk.END); self.direccion_entry.insert(0, item[4])

# -----------------------------------------------------------------
#                      FRAME  PEDIDOS
# -----------------------------------------------------------------
class PedidosFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # --------------- BÚSQUEDA ---------------
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=8, pady=6)

        ttk.Label(search_frame, text="Buscar:").grid(row=0, column=0)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=4)

        ttk.Label(search_frame, text="Por:").grid(row=0, column=2)
        self.search_cb = ttk.Combobox(
            search_frame, state="readonly", width=24,
            values=["ID Pedido", "Estado", "Fecha", "Cédula Cliente", "Total", "Producto"]
        )
        self.search_cb.grid(row=0, column=3, padx=4)

        ttk.Button(search_frame, text="Buscar", command=self.buscar_pedido)\
            .grid(row=0, column=4, padx=4)

        ttk.Button(search_frame, text="Mostrar Todo", command=self.cargar_pedidos)\
            .grid(row=0, column=5, padx=4)

        # --------------- BOTONES ACCIÓN ---------------
        top = ttk.Frame(self)
        top.pack(fill="x", padx=8, pady=4)

        ttk.Button(top, text="Nuevo Pedido", command=self.nuevo_pedido).grid(row=0, column=0, padx=4)
        ttk.Button(top, text="Ver Detalle", command=self.ver_detalle).grid(row=0, column=1, padx=4)
        ttk.Button(top, text="Eliminar Pedido", command=self.eliminar_pedido).grid(row=0, column=2, padx=4)
        ttk.Button(top, text="Cambiar Estado", command=self.cambiar_estado).grid(row=0, column=3, padx=4)
        ttk.Button(top, text="Refrescar", command=self.cargar_pedidos).grid(row=0, column=4, padx=4)

        # --------------- TABLA PEDIDOS ---------------
        cols = ("id_pedido","estado","fecha","total","cedula")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=8, pady=6)

        self.cargar_pedidos()

    def cargar_pedidos(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        rows = db_select("SELECT * FROM pedido ORDER BY id_pedido DESC")
        for r in rows:
            fecha = r.get("fecha")
            if hasattr(fecha, "strftime"):
                fecha_s = fecha.strftime("%Y-%m-%d")
            else:
                fecha_s = str(fecha) if fecha is not None else ""
            total_v = float(r["total"]) if r.get("total") is not None else 0.0
            self.tree.insert("", "end",
                values=(r["id_pedido"], r["estado"], fecha_s, total_v, r["cedula"])
            )

    def buscar_pedido(self):
        texto = self.search_entry.get().strip()
        campo = self.search_cb.get()

        if not texto or not campo:
            messagebox.showwarning("Atención", "Completa los campos de búsqueda.")
            return

        if campo == "Producto":
            query = """SELECT DISTINCT p.id_pedido, p.estado, p.fecha, p.total, p.cedula
                       FROM pedido p
                       JOIN detalle_pedido d ON p.id_pedido = d.id_pedido
                       JOIN producto pr ON d.id_producto = pr.id_producto
                       WHERE pr.nombre LIKE %s
                       ORDER BY p.id_pedido DESC"""
            texto_param = f"%{texto}%"
            rows = db_select(query, (texto_param,))
        else:
            col_map = {
                "ID Pedido": "id_pedido",
                "Estado": "estado",
                "Fecha": "fecha",
                "Cédula Cliente": "cedula",
                "Total": "total"
            }
            col = col_map[campo]
            # Para id exacto si es numérico, permitir búsqueda exacta; otherwise LIKE
            if campo == "ID Pedido":
                query = f"SELECT * FROM pedido WHERE {col} = %s ORDER BY id_pedido DESC"
                rows = db_select(query, (texto,))
            else:
                query = f"SELECT * FROM pedido WHERE {col} LIKE %s ORDER BY id_pedido DESC"
                rows = db_select(query, (f"%{texto}%",))

        for r in self.tree.get_children():
            self.tree.delete(r)

        for r in rows:
            fecha = r.get("fecha")
            if hasattr(fecha, "strftime"):
                fecha_s = fecha.strftime("%Y-%m-%d")
            else:
                fecha_s = str(fecha) if fecha is not None else ""
            total_v = float(r["total"]) if r.get("total") is not None else 0.0
            self.tree.insert("", "end",
                values=(r["id_pedido"], r["estado"], fecha_s, total_v, r["cedula"])
            )

    def nuevo_pedido(self):
        NuevoPedidoWindow(self, on_created=self.cargar_pedidos)

    def ver_detalle(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un pedido.")
            return
        id_pedido = self.tree.item(sel[0])["values"][0]
        DetallePedidoWindow(self, id_pedido)

    def eliminar_pedido(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un pedido.")
            return
        id_pedido = self.tree.item(sel[0])["values"][0]
        if not messagebox.askyesno("Confirmar", "¿Eliminar pedido y restaurar stock?"):
            return
        try:
            detalles = db_select("SELECT id_producto, cantidad FROM detalle_pedido WHERE id_pedido=%s", (id_pedido,))
            for d in detalles:
                db_execute("UPDATE producto SET stock = stock + %s WHERE id_producto=%s", (d["cantidad"], d["id_producto"]))
            db_execute("DELETE FROM detalle_pedido WHERE id_pedido=%s", (id_pedido,))
            db_execute("DELETE FROM pedido WHERE id_pedido=%s", (id_pedido,))
            messagebox.showinfo("OK", "Pedido eliminado y stock restaurado.")
            self.cargar_pedidos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cambiar_estado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un pedido.")
            return
        id_pedido = self.tree.item(sel[0])["values"][0]
        estados = ["Pendiente","Procesando","Completado","Cancelado"]
        nuevo = simpledialog.askstring("Estado", f"Nuevo estado {estados}:")
        if nuevo and nuevo in estados:
            db_execute("UPDATE pedido SET estado=%s WHERE id_pedido=%s", (nuevo, id_pedido))
            messagebox.showinfo("OK", "Estado actualizado.")
            self.cargar_pedidos()
        else:
            messagebox.showwarning("Estado inválido", "Estado no reconocido o cancelado.")

# -----------------------------------------------------------------
#                    VENTANA: NUEVO PEDIDO
# -----------------------------------------------------------------
class NuevoPedidoWindow(tk.Toplevel):
    def __init__(self, parent, on_created=None):
        super().__init__(parent)
        self.title("Nuevo Pedido")
        self.geometry("750x520")
        self.on_created = on_created

        # Cliente
        ttk.Label(self, text="Cliente (selecciona):").pack(anchor="w", padx=8, pady=4)
        self.cliente_cb = ttk.Combobox(self, state="readonly", width=60)
        self.cliente_cb.pack(fill="x", padx=8)
        self.cargar_clientes()

        # Tabla detalle
        cols = ("id_producto","nombre","cantidad","precio","subtotal")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        # Añadir producto
        frame_add = ttk.Frame(self)
        frame_add.pack(fill="x", padx=8, pady=4)
        ttk.Label(frame_add, text="Producto:").grid(row=0, column=0)
        self.prod_cb = ttk.Combobox(frame_add, state="readonly", width=60)
        self.prod_cb.grid(row=0, column=1, padx=4)
        ttk.Label(frame_add, text="Cantidad:").grid(row=0, column=2)
        self.cant_entry = ttk.Entry(frame_add, width=8)
        self.cant_entry.grid(row=0, column=3, padx=4)
        ttk.Button(frame_add, text="Agregar línea", command=self.agregar_linea).grid(row=0, column=4, padx=4)
        ttk.Button(frame_add, text="Eliminar línea", command=self.eliminar_linea).grid(row=0, column=5, padx=4)

        # Total y acciones
        bottom = ttk.Frame(self)
        bottom.pack(fill="x", padx=8, pady=6)
        self.total_var = tk.DoubleVar(value=0.0)
        ttk.Label(bottom, text="Total:").pack(side="left")
        ttk.Label(bottom, textvariable=self.total_var).pack(side="left", padx=6)
        ttk.Button(bottom, text="Crear Pedido", command=self.crear_pedido).pack(side="right")
        ttk.Button(bottom, text="Cancelar", command=self.destroy).pack(side="right", padx=6)

        self.cargar_productos()

    def cargar_clientes(self):
        rows = db_select("SELECT cedula, nombre, apellido FROM cliente")
        self.clientes = {f'{r["cedula"]} - {r["nombre"]} {r["apellido"]}': r["cedula"] for r in rows}
        self.cliente_cb["values"] = list(self.clientes.keys())

    def cargar_productos(self):
        rows = db_select("SELECT id_producto, nombre, stock, precio FROM producto WHERE stock>0")
        self.productos = {f'{r["id_producto"]} - {r["nombre"]} (stock:{r["stock"]}) - {float(r["precio"])}': (r["id_producto"], r["stock"], float(r["precio"])) for r in rows}
        self.prod_cb["values"] = list(self.productos.keys())

    def agregar_linea(self):
        prod_desc = self.prod_cb.get()
        if not prod_desc:
            messagebox.showwarning("Selecciona", "Selecciona un producto.")
            return
        try:
            cantidad = int(self.cant_entry.get().strip())
            if cantidad <= 0:
                raise ValueError("Cantidad debe ser positiva.")
            idp, stock, precio = self.productos[prod_desc]
            if cantidad > stock:
                messagebox.showwarning("Stock insuficiente", f"Stock disponible: {stock}")
                return
            subtotal = round(cantidad * precio, 2)
            # acumular si ya existe
            found = None
            for it in self.tree.get_children():
                vals = self.tree.item(it)["values"]
                if vals[0] == idp:
                    found = it
                    break
            if found:
                vals = self.tree.item(found)["values"]
                nueva_cant = int(vals[2]) + cantidad
                nuevo_sub = round(nueva_cant * precio, 2)
                nombre = vals[1]
                self.tree.item(found, values=(idp, nombre, nueva_cant, precio, nuevo_sub))
            else:
                nombre = prod_desc.split(" - ")[1].split(" (")[0]
                self.tree.insert("", "end", values=(idp, nombre, cantidad, precio, subtotal))
            self.recalcular_total()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def eliminar_linea(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona una línea para eliminar.")
            return
        self.tree.delete(sel[0])
        self.recalcular_total()

    def recalcular_total(self):
        total = 0.0
        for it in self.tree.get_children():
            total += float(self.tree.item(it)["values"][4])
        self.total_var.set(round(total, 2))

    def crear_pedido(self):
        cliente_desc = self.cliente_cb.get()
        if not cliente_desc:
            messagebox.showwarning("Cliente", "Selecciona un cliente.")
            return
        if not self.tree.get_children():
            messagebox.showwarning("Detalle vacío", "Agrega al menos una línea de pedido.")
            return
        try:
            cedula = self.clientes[cliente_desc]
            total = float(self.total_var.get())
            hoy = date.today().isoformat()
            id_pedido = db_execute("INSERT INTO pedido (estado, fecha, total, cedula) VALUES (%s,%s,%s,%s)",
                                   ("Pendiente", hoy, total, cedula))
            for it in self.tree.get_children():
                id_producto, nombre, cantidad, precio, subtotal = self.tree.item(it)["values"]
                db_execute("INSERT INTO detalle_pedido (id_producto, id_pedido, cantidad, subtotal, precio) VALUES (%s,%s,%s,%s,%s)",
                           (id_producto, id_pedido, cantidad, subtotal, precio))
                db_execute("UPDATE producto SET stock = stock - %s WHERE id_producto=%s", (cantidad, id_producto))
            messagebox.showinfo("OK", f"Pedido creado (id={id_pedido}).")
            if self.on_created:
                self.on_created()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

# -----------------------------------------------------------------
#                 VENTANA: DETALLE PEDIDO
# -----------------------------------------------------------------
class DetallePedidoWindow(tk.Toplevel):
    def __init__(self, parent, id_pedido):
        super().__init__(parent)
        self.title(f"Detalle Pedido #{id_pedido}")
        self.geometry("600x420")
        cols = ("id_detalle","id_producto","nombre","cantidad","precio","subtotal")
        tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c.capitalize())
            tree.column(c, anchor="center")
        tree.pack(fill="both", expand=True, padx=8, pady=8)

        rows = db_select("""
            SELECT d.id_detalle, d.id_producto, p.nombre, d.cantidad, d.precio, d.subtotal
            FROM detalle_pedido d
            LEFT JOIN producto p ON d.id_producto = p.id_producto
            WHERE d.id_pedido=%s
        """, (id_pedido,))

        total = 0.0
        for r in rows:
            tree.insert("", "end",
                values=(r["id_detalle"], r["id_producto"], r["nombre"], r["cantidad"], float(r["precio"]), float(r["subtotal"]))
            )
            total += float(r["subtotal"])
        ttk.Label(self, text=f"Total calculado: {round(total,2)}").pack(anchor="e", padx=12, pady=6)

# -----------------------------------------------------------------
#                         Ejecutar app
# -----------------------------------------------------------------
if __name__ == "__main__":
    app = InventarioApp()
    app.mainloop()
# ===========================================================