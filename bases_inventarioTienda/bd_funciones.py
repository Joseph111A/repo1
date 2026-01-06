import sqlite3
from datetime import datetime

DB_NAME = 'inventario.db'

def conectar():
    """Conecta a la base de datos"""
    return sqlite3.connect(DB_NAME)

# ============= FUNCIONES CATEGORIA =============

def obtener_categorias():
    """Obtiene todas las categorías"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM CATEGORIA')
    categorias = cursor.fetchall()
    conexion.close()
    return categorias

# ============= FUNCIONES PROVEEDOR =============

def obtener_proveedores():
    """Obtiene todos los proveedores"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM PROVEEDOR')
    proveedores = cursor.fetchall()
    conexion.close()
    return proveedores

def agregar_proveedor(nombre, email, telefono, direccion, ciudad):
    """Agrega un nuevo proveedor"""
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO PROVEEDOR (Nombre_Proveedor, Email, Telefono, Direccion, Ciudad)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, email, telefono, direccion, ciudad))
        conexion.commit()
        conexion.close()
        return True, "Proveedor agregado exitosamente"
    except Exception as e:
        return False, f"Error al agregar proveedor: {str(e)}"

# ============= FUNCIONES PRODUCTO =============

def obtener_productos():
    """Obtiene todos los productos"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT p.ID_Producto, p.Nombre, p.Descripcion, p.Precio_Unitario, 
               p.Stock_Disponible, c.Nombre_Categoria, pr.Nombre_Proveedor
        FROM PRODUCTO p
        LEFT JOIN CATEGORIA c ON p.ID_Categoria = c.ID_Categoria
        LEFT JOIN PROVEEDOR pr ON p.ID_Proveedor = pr.ID_Proveedor
    ''')
    productos = cursor.fetchall()
    conexion.close()
    return productos

def buscar_producto_por_id(id_producto):
    """Busca un producto por ID"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT p.ID_Producto, p.Nombre, p.Descripcion, p.Precio_Unitario, 
               p.Stock_Disponible, c.Nombre_Categoria, pr.Nombre_Proveedor
        FROM PRODUCTO p
        LEFT JOIN CATEGORIA c ON p.ID_Categoria = c.ID_Categoria
        LEFT JOIN PROVEEDOR pr ON p.ID_Proveedor = pr.ID_Proveedor
        WHERE p.ID_Producto = ?
    ''', (id_producto,))
    producto = cursor.fetchall()
    conexion.close()
    return producto

def buscar_producto_por_nombre(nombre):
    """Busca productos por nombre (LIKE)"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT p.ID_Producto, p.Nombre, p.Descripcion, p.Precio_Unitario, 
               p.Stock_Disponible, c.Nombre_Categoria, pr.Nombre_Proveedor
        FROM PRODUCTO p
        LEFT JOIN CATEGORIA c ON p.ID_Categoria = c.ID_Categoria
        LEFT JOIN PROVEEDOR pr ON p.ID_Proveedor = pr.ID_Proveedor
        WHERE p.Nombre LIKE ?
    ''', (f'%{nombre}%',))
    productos = cursor.fetchall()
    conexion.close()
    return productos

def buscar_producto_por_precio(precio_min, precio_max):
    """Busca productos por rango de precio"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT p.ID_Producto, p.Nombre, p.Descripcion, p.Precio_Unitario, 
               p.Stock_Disponible, c.Nombre_Categoria, pr.Nombre_Proveedor
        FROM PRODUCTO p
        LEFT JOIN CATEGORIA c ON p.ID_Categoria = c.ID_Categoria
        LEFT JOIN PROVEEDOR pr ON p.ID_Proveedor = pr.ID_Proveedor
        WHERE p.Precio_Unitario BETWEEN ? AND ?
    ''', (precio_min, precio_max))
    productos = cursor.fetchall()
    conexion.close()
    return productos

def buscar_producto_por_categoria(id_categoria):
    """Busca productos por categoría"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT p.ID_Producto, p.Nombre, p.Descripcion, p.Precio_Unitario, 
               p.Stock_Disponible, c.Nombre_Categoria, pr.Nombre_Proveedor
        FROM PRODUCTO p
        LEFT JOIN CATEGORIA c ON p.ID_Categoria = c.ID_Categoria
        LEFT JOIN PROVEEDOR pr ON p.ID_Proveedor = pr.ID_Proveedor
        WHERE p.ID_Categoria = ?
    ''', (id_categoria,))
    productos = cursor.fetchall()
    conexion.close()
    return productos

def agregar_producto(nombre, descripcion, precio, stock, id_categoria, id_proveedor):
    """Agrega un nuevo producto"""
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        fecha_ingreso = datetime.now().date()
        cursor.execute('''
            INSERT INTO PRODUCTO (Nombre, Descripcion, Precio_Unitario, Stock_Disponible, 
                                  ID_Categoria, Fecha_Ingreso, ID_Proveedor)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, descripcion, precio, stock, id_categoria, fecha_ingreso, id_proveedor))
        conexion.commit()
        conexion.close()
        return True, "Producto agregado exitosamente"
    except Exception as e:
        return False, f"Error al agregar producto: {str(e)}"

def actualizar_producto(id_producto, nombre, descripcion, precio, stock, id_categoria, id_proveedor):
    """Actualiza un producto existente"""
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE PRODUCTO
            SET Nombre = ?, Descripcion = ?, Precio_Unitario = ?, Stock_Disponible = ?,
                ID_Categoria = ?, ID_Proveedor = ?
            WHERE ID_Producto = ?
        ''', (nombre, descripcion, precio, stock, id_categoria, id_proveedor, id_producto))
        conexion.commit()
        conexion.close()
        return True, "Producto actualizado exitosamente"
    except Exception as e:
        return False, f"Error al actualizar producto: {str(e)}"

def eliminar_producto(id_producto):
    """Elimina un producto"""
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM PRODUCTO WHERE ID_Producto = ?', (id_producto,))
        conexion.commit()
        conexion.close()
        return True, "Producto eliminado exitosamente"
    except Exception as e:
        return False, f"Error al eliminar producto: {str(e)}"

# ============= FUNCIONES CLIENTE =============

def obtener_clientes():
    """Obtiene todos los clientes"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM CLIENTE')
    clientes = cursor.fetchall()
    conexion.close()
    return clientes

def buscar_cliente_por_id(id_cliente):
    """Busca un cliente por ID"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM CLIENTE WHERE ID_Cliente = ?', (id_cliente,))
    cliente = cursor.fetchall()
    conexion.close()
    return cliente

def buscar_cliente_por_nombre(nombre):
    """Busca clientes por nombre"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT * FROM CLIENTE 
        WHERE Nombre LIKE ? OR Apellido LIKE ?
    ''', (f'%{nombre}%', f'%{nombre}%'))
    clientes = cursor.fetchall()
    conexion.close()
    return clientes

def agregar_cliente(nombre, apellido, email, telefono, direccion):
    """Agrega un nuevo cliente"""
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        fecha_registro = datetime.now().date()
        cursor.execute('''
            INSERT INTO CLIENTE (Nombre, Apellido, Email, Telefono, Direccion, Fecha_Registro)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, apellido, email, telefono, direccion, fecha_registro))
        conexion.commit()
        conexion.close()
        return True, "Cliente agregado exitosamente"
    except Exception as e:
        return False, f"Error al agregar cliente: {str(e)}"

def actualizar_cliente(id_cliente, nombre, apellido, email, telefono, direccion):
    """Actualiza un cliente"""
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE CLIENTE
            SET Nombre = ?, Apellido = ?, Email = ?, Telefono = ?, Direccion = ?
            WHERE ID_Cliente = ?
        ''', (nombre, apellido, email, telefono, direccion, id_cliente))
        conexion.commit()
        conexion.close()
        return True, "Cliente actualizado exitosamente"
    except Exception as e:
        return False, f"Error al actualizar cliente: {str(e)}"

# ============= FUNCIONES PEDIDO =============

def obtener_pedidos():
    """Obtiene todos los pedidos"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT p.ID_Pedido, p.Fecha_Pedido, p.Total_Pedido, p.Estado, 
               c.ID_Cliente, c.Nombre, c.Apellido
        FROM PEDIDO p
        LEFT JOIN CLIENTE c ON p.ID_Cliente = c.ID_Cliente
    ''')
    pedidos = cursor.fetchall()
    conexion.close()
    return pedidos

def buscar_pedido_por_id(id_pedido):
    """Busca un pedido por ID"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT p.ID_Pedido, p.Fecha_Pedido, p.Total_Pedido, p.Estado, 
               c.ID_Cliente, c.Nombre, c.Apellido
        FROM PEDIDO p
        LEFT JOIN CLIENTE c ON p.ID_Cliente = c.ID_Cliente
        WHERE p.ID_Pedido = ?
    ''', (id_pedido,))
    pedido = cursor.fetchall()
    conexion.close()
    return pedido

def buscar_pedido_por_cliente(id_cliente):
    """Busca pedidos de un cliente"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT p.ID_Pedido, p.Fecha_Pedido, p.Total_Pedido, p.Estado, 
               c.ID_Cliente, c.Nombre, c.Apellido
        FROM PEDIDO p
        LEFT JOIN CLIENTE c ON p.ID_Cliente = c.ID_Cliente
        WHERE p.ID_Cliente = ?
    ''', (id_cliente,))
    pedidos = cursor.fetchall()
    conexion.close()
    return pedidos

def buscar_pedido_por_estado(estado):
    """Busca pedidos por estado"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT p.ID_Pedido, p.Fecha_Pedido, p.Total_Pedido, p.Estado, 
               c.ID_Cliente, c.Nombre, c.Apellido
        FROM PEDIDO p
        LEFT JOIN CLIENTE c ON p.ID_Cliente = c.ID_Cliente
        WHERE p.Estado = ?
    ''', (estado,))
    pedidos = cursor.fetchall()
    conexion.close()
    return pedidos

def agregar_pedido(id_cliente, total):
    """Agrega un nuevo pedido"""
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        fecha_pedido = datetime.now().date()
        cursor.execute('''
            INSERT INTO PEDIDO (Fecha_Pedido, Total_Pedido, Estado, ID_Cliente)
            VALUES (?, ?, 'Pendiente', ?)
        ''', (fecha_pedido, total, id_cliente))
        conexion.commit()
        id_pedido = cursor.lastrowid
        conexion.close()
        return True, f"Pedido agregado exitosamente (ID: {id_pedido})", id_pedido
    except Exception as e:
        return False, f"Error al agregar pedido: {str(e)}", None

def actualizar_estado_pedido(id_pedido, estado):
    """Actualiza el estado de un pedido"""
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE PEDIDO
            SET Estado = ?
            WHERE ID_Pedido = ?
        ''', (estado, id_pedido))
        conexion.commit()
        conexion.close()
        return True, f"Estado del pedido actualizado a: {estado}"
    except Exception as e:
        return False, f"Error al actualizar estado: {str(e)}"

def eliminar_pedido(id_pedido):
    """Elimina un pedido y sus detalles"""
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        # Primero eliminar los detalles del pedido
        cursor.execute('DELETE FROM DETALLE_PEDIDO WHERE ID_Pedido = ?', (id_pedido,))
        # Luego eliminar el pedido
        cursor.execute('DELETE FROM PEDIDO WHERE ID_Pedido = ?', (id_pedido,))
        conexion.commit()
        conexion.close()
        return True, "Pedido eliminado exitosamente"
    except Exception as e:
        return False, f"Error al eliminar pedido: {str(e)}"

# ============= FUNCIONES DETALLE_PEDIDO =============

def obtener_detalles_pedido(id_pedido):
    """Obtiene los detalles de un pedido"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT dp.ID_Detalle, dp.ID_Pedido, dp.ID_Producto, dp.Cantidad, 
               dp.Precio_Pedido, dp.Subtotal, pr.Nombre
        FROM DETALLE_PEDIDO dp
        LEFT JOIN PRODUCTO pr ON dp.ID_Producto = pr.ID_Producto
        WHERE dp.ID_Pedido = ?
    ''', (id_pedido,))
    detalles = cursor.fetchall()
    conexion.close()
    return detalles

def agregar_detalle_pedido(id_pedido, id_producto, cantidad, precio_pedido):
    """Agrega un detalle a un pedido"""
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        subtotal = cantidad * precio_pedido
        cursor.execute('''
            INSERT INTO DETALLE_PEDIDO (ID_Pedido, ID_Producto, Cantidad, Precio_Pedido, Subtotal)
            VALUES (?, ?, ?, ?, ?)
        ''', (id_pedido, id_producto, cantidad, precio_pedido, subtotal))
        conexion.commit()
        conexion.close()
        return True, "Detalle agregado exitosamente"
    except Exception as e:
        return False, f"Error al agregar detalle: {str(e)}"

def eliminar_detalle_pedido(id_detalle):
    """Elimina un detalle del pedido"""
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM DETALLE_PEDIDO WHERE ID_Detalle = ?', (id_detalle,))
        conexion.commit()
        conexion.close()
        return True, "Detalle eliminado exitosamente"
    except Exception as e:
        return False, f"Error al eliminar detalle: {str(e)}"
