# Modelo Entidad-Relación y Modelo Relacional - Inventario de Tienda

## 1. MODELO ENTIDAD-RELACIÓN (ER)

### Entidades y Atributos

#### **ENTIDAD: PRODUCTO**
- **ID_Producto** (PK - Clave Primaria) ✓ ÚNICO
- Nombre
- Descripción
- Precio_Unitario
- Stock_Disponible
- Categoría
- Fecha_Ingreso
- **FK_Proveedor** (Clave Foránea hacia PROVEEDOR)

#### **ENTIDAD: PROVEEDOR**
- **ID_Proveedor** (PK) ✓ ÚNICO
- Nombre_Proveedor
- Email
- Teléfono
- Dirección
- Ciudad

#### **ENTIDAD: CLIENTE**
- **ID_Cliente** (PK) ✓ ÚNICO
- Nombre
- Apellido
- Email ✓ ÚNICO
- Teléfono
- Dirección
- Fecha_Registro

#### **ENTIDAD: PEDIDO**
- **ID_Pedido** (PK) ✓ ÚNICO
- Fecha_Pedido
- Total_Pedido
- Estado (Pendiente, Completado, Cancelado)
- **FK_Cliente** (Clave Foránea hacia CLIENTE)

#### **ENTIDAD: DETALLE_PEDIDO**
- **ID_Detalle** (PK) ✓ ÚNICO
- **FK_Pedido** (Clave Foránea hacia PEDIDO)
- **FK_Producto** (Clave Foránea hacia PRODUCTO)
- Cantidad
- Precio_Pedido
- Subtotal

#### **ENTIDAD: CATEGORÍA**
- **ID_Categoría** (PK) ✓ ÚNICO
- Nombre_Categoría ✓ ÚNICO
- Descripción

---

## 2. RELACIONES

- **PROVEEDOR** → **PRODUCTO**: (1:N) - Un proveedor puede suministrar muchos productos
- **CATEGORÍA** → **PRODUCTO**: (1:N) - Una categoría contiene muchos productos
- **CLIENTE** → **PEDIDO**: (1:N) - Un cliente puede hacer muchos pedidos
- **PEDIDO** → **DETALLE_PEDIDO**: (1:N) - Un pedido tiene muchos detalles
- **PRODUCTO** → **DETALLE_PEDIDO**: (1:N) - Un producto puede estar en muchos detalles de pedido

---

## 3. MODELO RELACIONAL (SQL)

### Definición en SQL:

```sql
-- Tabla CATEGORÍA
CREATE TABLE CATEGORIA (
    ID_Categoria INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    Nombre_Categoria VARCHAR(50) NOT NULL UNIQUE,
    Descripcion VARCHAR(200)
);

-- Tabla PROVEEDOR
CREATE TABLE PROVEEDOR (
    ID_Proveedor INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    Nombre_Proveedor VARCHAR(100) NOT NULL,
    Email VARCHAR(100),
    Telefono VARCHAR(15),
    Direccion VARCHAR(150),
    Ciudad VARCHAR(50)
);

-- Tabla PRODUCTO
CREATE TABLE PRODUCTO (
    ID_Producto INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion VARCHAR(300),
    Precio_Unitario DECIMAL(10, 2) NOT NULL,
    Stock_Disponible INT NOT NULL DEFAULT 0,
    Categoria INT NOT NULL,
    Fecha_Ingreso DATE,
    ID_Proveedor INT NOT NULL,
    FOREIGN KEY (Categoria) REFERENCES CATEGORIA(ID_Categoria),
    FOREIGN KEY (ID_Proveedor) REFERENCES PROVEEDOR(ID_Proveedor)
);

-- Tabla CLIENTE
CREATE TABLE CLIENTE (
    ID_Cliente INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Telefono VARCHAR(15),
    Direccion VARCHAR(150),
    Fecha_Registro DATE
);

-- Tabla PEDIDO
CREATE TABLE PEDIDO (
    ID_Pedido INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    Fecha_Pedido DATE NOT NULL,
    Total_Pedido DECIMAL(12, 2),
    Estado VARCHAR(20) DEFAULT 'Pendiente',
    ID_Cliente INT NOT NULL,
    FOREIGN KEY (ID_Cliente) REFERENCES CLIENTE(ID_Cliente)
);

-- Tabla DETALLE_PEDIDO
CREATE TABLE DETALLE_PEDIDO (
    ID_Detalle INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    ID_Pedido INT NOT NULL,
    ID_Producto INT NOT NULL,
    Cantidad INT NOT NULL,
    Precio_Pedido DECIMAL(10, 2),
    Subtotal DECIMAL(12, 2),
    FOREIGN KEY (ID_Pedido) REFERENCES PEDIDO(ID_Pedido),
    FOREIGN KEY (ID_Producto) REFERENCES PRODUCTO(ID_Producto)
);
```

---

## 4. RESUMEN ATRIBUTOS ÚNICOS

| Entidad | Atributos Únicos (UNIQUE) |
|---------|---------------------------|
| **PRODUCTO** | ID_Producto |
| **PROVEEDOR** | ID_Proveedor |
| **CLIENTE** | ID_Cliente, Email |
| **PEDIDO** | ID_Pedido |
| **DETALLE_PEDIDO** | ID_Detalle |
| **CATEGORÍA** | ID_Categoría, Nombre_Categoría |

**Nota:** PK = Clave Primaria (siempre única), FK = Clave Foránea (referencia a otra tabla)

---

## 5. EXPLICACIÓN RÁPIDA

**ER:** Define QUÉ entidades existen, SUS atributos y CÓMO se relacionan.

**RELACIONAL:** Convierte el ER en tablas concretas con filas y columnas, usando claves primarias y foráneas para mantener la integridad de los datos.
