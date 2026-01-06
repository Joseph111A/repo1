# Sistema de Inventario - Tienda

## Descripción
Sistema completo de gestión de inventario para una tienda con interfaz gráfica en Tkinter. Permite gestionar productos, pedidos y clientes con una base de datos SQLite.

## Características

### 📦 Gestión de Productos
- **Búsqueda avanzada**: Por ID, nombre, precio, categoría
- **Agregar productos**: Con nombre, descripción, precio, stock, categoría y proveedor
- **Editar productos**: Modificar cualquier información del producto
- **Eliminar productos**: Remover productos del inventario
- **Vista completa**: Tabla con todos los detalles del producto

### 📋 Gestión de Pedidos
- **Búsqueda de pedidos**: Por ID, cliente, estado
- **Agregar pedidos**: Crear nuevos pedidos con cliente y total
- **Cambiar estado**: Pendiente → Completado → Cancelado
- **Ver detalles**: Visualizar items incluidos en cada pedido
- **Cancelar pedidos**: Marcar como cancelado
- **Eliminar pedidos**: Remover pedidos y sus detalles

### 👥 Gestión de Clientes
- **Búsqueda de clientes**: Por ID y nombre
- **Agregar clientes**: Con información personal y contacto
- **Editar clientes**: Actualizar datos de clientes existentes
- **Vista completa**: Tabla con todos los clientes

## Instalación

### 1. Crear la base de datos
```bash
python crear_bd.py
```

### 2. Inicializar con datos de prueba (opcional)
```bash
python inicializar_bd.py
```

### 3. Ejecutar la interfaz
```bash
python interfaz_inventario.py
```

## Archivos del Proyecto

- `crear_bd.py` - Crea la estructura de la base de datos SQLite
- `bd_funciones.py` - Todas las funciones CRUD para base de datos
- `interfaz_inventario.py` - Interfaz gráfica principal (Tkinter)
- `inicializar_bd.py` - Script para cargar datos de prueba
- `inventario.db` - Base de datos SQLite (se genera automáticamente)

## Estructura de Base de Datos

### Tablas
1. **CATEGORIA** - Categorías de productos
2. **PROVEEDOR** - Información de proveedores
3. **PRODUCTO** - Inventario de productos
4. **CLIENTE** - Base de clientes
5. **PEDIDO** - Pedidos realizados (Estados: Pendiente, Completado, Cancelado)
6. **DETALLE_PEDIDO** - Detalles de cada pedido

## Uso de la Interfaz

### Pestaña Productos
1. **Búsqueda**: Ingrese criterios y haga clic en el botón correspondiente
2. **Agregar**: Clic en "Agregar Producto" y llene el formulario
3. **Editar**: Seleccione un producto y clic en "Editar Producto"
4. **Eliminar**: Seleccione un producto y clic en "Eliminar Producto"

### Pestaña Pedidos
1. **Búsqueda**: Use los filtros por ID, cliente o estado
2. **Agregar**: Clic en "Agregar Pedido" y seleccione cliente
3. **Cambiar Estado**: Seleccione un pedido y clic en "Cambiar Estado"
4. **Ver Detalles**: Clic en "Ver Detalles" para productos en el pedido
5. **Cancelar/Eliminar**: Opciones para gestión de pedidos

### Pestaña Clientes
1. **Búsqueda**: Busque por ID o nombre
2. **Agregar**: Clic en "Agregar Cliente" con datos personales
3. **Editar**: Seleccione cliente y clic en "Editar Cliente"

## Funciones de Búsqueda

### Productos
- **Por ID**: Búsqueda exacta
- **Por Nombre**: Búsqueda parcial (LIKE)
- **Por Precio**: Rango de precios (min - max)
- **Por Categoría**: Seleccionar de lista

### Pedidos
- **Por ID**: Búsqueda exacta del pedido
- **Por Cliente**: Todos los pedidos de un cliente
- **Por Estado**: Filtrar por Pendiente/Completado/Cancelado

### Clientes
- **Por ID**: Búsqueda exacta
- **Por Nombre**: Búsqueda parcial en nombre o apellido

## Datos de Prueba Iniciales

Si ejecuta `inicializar_bd.py`, se cargarán:
- 4 Categorías: Electrónica, Ropa, Alimentos, Libros
- 3 Proveedores principales
- 10 Productos de ejemplo
- 5 Clientes de prueba
- 3 Pedidos de ejemplo

## Requisitos

- Python 3.7+
- Tkinter (incluido en Python por defecto)
- SQLite3 (incluido en Python por defecto)

## Notas Importantes

- La base de datos se crea automáticamente en la primera ejecución
- Los estados de pedido disponibles son: Pendiente, Completado, Cancelado
- Los cambios se guardan automáticamente en la base de datos
- Puede editar productos pero se recomienda usar la opción eliminar con cuidado

## Mejoras Futuras

- Exportar a PDF/Excel
- Gráficos de ventas
- Gestión de usuarios y permisos
- Backup automático de base de datos
- Reportes detallados
- Sistema de facturas

---

**Versión**: 1.0  
**Última actualización**: Diciembre 2025
