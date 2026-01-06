"""
Script para inicializar la base de datos con datos de prueba
Ejecutar solo una vez
"""

import sqlite3
import crear_bd
import bd_funciones as bd

def cargar_datos_iniciales():
    """Carga datos iniciales para pruebas"""
    
    # Crear base de datos
    crear_bd.crear_base_datos()
    
    # Agregar categorías
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    
    categorias = [
        ("Electrónica", "Productos electrónicos"),
        ("Ropa", "Prendas de vestir"),
        ("Alimentos", "Productos alimenticios"),
        ("Libros", "Libros y literatura")
    ]
    
    for cat in categorias:
        try:
            cursor.execute('''
                INSERT INTO CATEGORIA (Nombre_Categoria, Descripcion)
                VALUES (?, ?)
            ''', cat)
        except:
            pass
    
    # Agregar proveedores
    proveedores = [
        ("Tech Store", "tech@store.com", "555-0001", "Calle Principal 123", "Ciudad"),
        ("Distribuidora Nacional", "dist@nacional.com", "555-0002", "Av. Central 456", "Metrópolis"),
        ("Mayoristas SA", "mayoristas@sa.com", "555-0003", "Zona Industrial 789", "Puerto")
    ]
    
    for prov in proveedores:
        try:
            cursor.execute('''
                INSERT INTO PROVEEDOR (Nombre_Proveedor, Email, Telefono, Direccion, Ciudad)
                VALUES (?, ?, ?, ?, ?)
            ''', prov)
        except:
            pass
    
    # Agregar productos
    productos = [
        ("Laptop", "Laptop HP Intel i7", 1200.00, 5, 1, 1),
        ("Monitor", "Monitor LG 24 pulgadas", 350.00, 10, 1, 1),
        ("Mouse", "Mouse inalámbrico Logitech", 45.00, 25, 1, 1),
        ("Teclado", "Teclado mecánico RGB", 120.00, 8, 1, 1),
        ("Camiseta", "Camiseta 100% algodón", 25.00, 50, 2, 2),
        ("Pantalón", "Pantalón jean azul", 60.00, 30, 2, 2),
        ("Arroz", "Arroz integral 1kg", 5.00, 100, 3, 3),
        ("Pasta", "Pasta integral 500g", 3.00, 80, 3, 3),
        ("Novela", "Novela de ficción", 35.00, 15, 4, 2),
        ("Técnico", "Libro de programación", 55.00, 12, 4, 2)
    ]
    
    for prod in productos:
        try:
            cursor.execute('''
                INSERT INTO PRODUCTO (Nombre, Descripcion, Precio_Unitario, Stock_Disponible, ID_Categoria, ID_Proveedor)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', prod)
        except:
            pass
    
    # Agregar clientes
    clientes = [
        ("Juan", "Pérez", "juan@email.com", "555-1001", "Calle 1 #100"),
        ("María", "González", "maria@email.com", "555-1002", "Calle 2 #200"),
        ("Carlos", "López", "carlos@email.com", "555-1003", "Calle 3 #300"),
        ("Ana", "Martínez", "ana@email.com", "555-1004", "Calle 4 #400"),
        ("Roberto", "Sánchez", "roberto@email.com", "555-1005", "Calle 5 #500")
    ]
    
    for cli in clientes:
        try:
            cursor.execute('''
                INSERT INTO CLIENTE (Nombre, Apellido, Email, Telefono, Direccion)
                VALUES (?, ?, ?, ?, ?)
            ''', cli)
        except:
            pass
    
    # Agregar algunos pedidos
    pedidos = [
        (1, 1500.00, "Completado", 1),
        (2, 800.00, "Pendiente", 2),
        (3, 200.00, "Completado", 1),
    ]
    
    for ped in pedidos:
        try:
            cursor.execute('''
                INSERT INTO PEDIDO (Fecha_Pedido, Total_Pedido, Estado, ID_Cliente)
                VALUES (DATE('now'), ?, ?, ?)
            ''', ped[1:])
        except:
            pass
    
    conexion.commit()
    conexion.close()
    
    print("✓ Base de datos inicializada con datos de prueba")

if __name__ == "__main__":
    cargar_datos_iniciales()
