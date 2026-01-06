import mysql.connector

# ------------------------------
# 1. Conexión inicial al servidor
# ------------------------------
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""   # cambia si tienes clave
)

cursor = conexion.cursor()

# ------------------------------
# 2. Crear base de datos
# ------------------------------
cursor.execute("CREATE DATABASE IF NOT EXISTS inventario_db")
print("Base de datos 'inventario_db' creada o ya existente.")

cursor.close()
conexion.close()

# ------------------------------
# 3. Conectar a la nueva base
# ------------------------------
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="inventario_db"
)
cursor = conexion.cursor()

# ------------------------------
# 4. Crear tablas
# ------------------------------

# Tabla CATEGORIA
cursor.execute("""
CREATE TABLE IF NOT EXISTS categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255)
)
""")
print("Tabla categoria creada.")

# Tabla PROVEEDOR
cursor.execute("""
CREATE TABLE IF NOT EXISTS proveedor (
    nit INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    pais VARCHAR(50),
    ciudad VARCHAR(50)
)
""")
print("Tabla proveedor creada.")

# Tabla PRODUCTO
cursor.execute("""
CREATE TABLE IF NOT EXISTS producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    stock INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    id_categoria INT,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
)
""")
print("Tabla producto creada.")

# Tabla PROVEEDOR_PRODUCTO 
cursor.execute("""
CREATE TABLE IF NOT EXISTS proveedor_producto (
    nit INT,
    id_producto INT,
    FOREIGN KEY (nit) REFERENCES proveedor(nit),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
)
""")
print("Tabla proveedor_producto creada.")

# Tabla CLIENTE
cursor.execute("""
CREATE TABLE IF NOT EXISTS cliente (
    cedula INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    direccion VARCHAR(255)
)
""")
print("Tabla cliente creada.")

# Tabla PEDIDO
cursor.execute("""
CREATE TABLE IF NOT EXISTS pedido (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    estado VARCHAR(50),
    fecha DATE,
    total DECIMAL(10,2),
    cedula INT,
    FOREIGN KEY (cedula) REFERENCES cliente(cedula)
)
""")
print("Tabla pedido creada.")

# Tabla DETALLE_PEDIDO
cursor.execute("""
CREATE TABLE IF NOT EXISTS detalle_pedido (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT,
    id_pedido INT,
    cantidad INT NOT NULL,
    subtotal DECIMAL(10,2),
    precio DECIMAL(10,2),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido)
)
""")
print("Tabla detalle_pedido creada.")

# -----------------------------------
# 5. INSETAR DATOS DE PRUEBA
# -----------------------------------

print("Tablas creadas correctamente.")


# ---------- Categorías ----------
cursor.execute("""
INSERT INTO categoria (nombre, descripcion)
VALUES 
('Tecnología', 'Productos electrónicos'),
('Alimentos', 'Comestibles y bebidas'),
('Ropa', 'Vestimenta y accesorios')
""")

# ---------- Proveedores ----------
cursor.execute("""
INSERT INTO proveedor (nit, nombre, telefono, pais, ciudad)
VALUES
(1010, 'ProveedorTech', '3001234567', 'Colombia', 'Bogotá'),
(2020, 'Alimentos S.A', '3109876543', 'Colombia', 'Medellín')
""")

# ---------- Productos ----------
cursor.execute("""
INSERT INTO producto (nombre, stock, precio, id_categoria)
VALUES
('Laptop Lenovo', 10, 2500000, 1),
('Teclado Gamer', 25, 150000, 1),
('Manzana Roja', 100, 1200, 2),
('Camiseta Negra', 50, 35000, 3)
""")

# ---------- proveedor_producto ----------
cursor.execute("""
INSERT INTO proveedor_producto (nit, id_producto)
VALUES
(1010, 1),
(1010, 2),
(2020, 3),
(2020, 3)
""")

# ---------- Clientes ----------
cursor.execute("""
INSERT INTO cliente (cedula, nombre, apellido, telefono, direccion)
VALUES
(123456, 'Juan', 'Perez', '3001112233', 'Calle 10 #5-20'),
(789123, 'Maria', 'Gomez', '3025558899', 'Carrera 8 #12-30')
""")

# ---------- Pedidos ----------
cursor.execute("""
INSERT INTO pedido (estado, fecha, total, cedula)
VALUES
('Pendiente', '2025-02-01', 50000, 123456),
('Completado', '2025-02-05', 350000, 789123)
""")

# ---------- Detalle Pedido ----------
cursor.execute("""
INSERT INTO detalle_pedido (id_producto, id_pedido, cantidad, subtotal, precio)
VALUES
(3, 1, 10, 12000, 1200),   -- Pedido 1: Manzana Roja
(2, 2, 1, 150000, 150000), -- Pedido 2: Teclado Gamer
(1, 2, 1, 2500000, 2500000)
""")

conexion.commit()

print("Datos de prueba insertados correctamente.")

cursor.close()
conexion.close()
print("\n✔ BASE DE DATOS COMPLETA CON DATOS DE PRUEBA LISTA.")
