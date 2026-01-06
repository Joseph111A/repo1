import sqlite3
from datetime import datetime

def crear_base_datos():
    """Crea la base de datos SQLite con todas las tablas"""
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    
    # Tabla CATEGORIA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CATEGORIA (
            ID_Categoria INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            Nombre_Categoria TEXT NOT NULL UNIQUE,
            Descripcion TEXT
        )
    ''')
    
    # Tabla PROVEEDOR
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PROVEEDOR (
            ID_Proveedor INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            Nombre_Proveedor TEXT NOT NULL,
            Email TEXT,
            Telefono TEXT,
            Direccion TEXT,
            Ciudad TEXT
        )
    ''')
    
    # Tabla PRODUCTO
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PRODUCTO (
            ID_Producto INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            Nombre TEXT NOT NULL,
            Descripcion TEXT,
            Precio_Unitario REAL NOT NULL,
            Stock_Disponible INTEGER NOT NULL DEFAULT 0,
            ID_Categoria INTEGER NOT NULL,
            Fecha_Ingreso DATE,
            ID_Proveedor INTEGER NOT NULL,
            FOREIGN KEY (ID_Categoria) REFERENCES CATEGORIA(ID_Categoria),
            FOREIGN KEY (ID_Proveedor) REFERENCES PROVEEDOR(ID_Proveedor)
        )
    ''')
    
    # Tabla CLIENTE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CLIENTE (
            ID_Cliente INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            Nombre TEXT NOT NULL,
            Apellido TEXT NOT NULL,
            Email TEXT UNIQUE,
            Telefono TEXT,
            Direccion TEXT,
            Fecha_Registro DATE
        )
    ''')
    
    # Tabla PEDIDO
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PEDIDO (
            ID_Pedido INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            Fecha_Pedido DATE NOT NULL,
            Total_Pedido REAL,
            Estado TEXT DEFAULT 'Pendiente',
            ID_Cliente INTEGER NOT NULL,
            FOREIGN KEY (ID_Cliente) REFERENCES CLIENTE(ID_Cliente)
        )
    ''')
    
    # Tabla DETALLE_PEDIDO
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DETALLE_PEDIDO (
            ID_Detalle INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            ID_Pedido INTEGER NOT NULL,
            ID_Producto INTEGER NOT NULL,
            Cantidad INTEGER NOT NULL,
            Precio_Pedido REAL,
            Subtotal REAL,
            FOREIGN KEY (ID_Pedido) REFERENCES PEDIDO(ID_Pedido),
            FOREIGN KEY (ID_Producto) REFERENCES PRODUCTO(ID_Producto)
        )
    ''')
    
    conexion.commit()
    print("✓ Base de datos creada exitosamente")
    conexion.close()

if __name__ == "__main__":
    crear_base_datos()
