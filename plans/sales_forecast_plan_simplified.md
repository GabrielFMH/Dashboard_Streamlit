# Plan Simplificado: Forecast de Ventas con Clean Architecture

## 📋 Resumen del Proyecto
Crear una aplicación de forecast de ventas con datos ficticios usando Python y Streamlit, siguiendo principios de Clean Architecture simplificados.

## 🎯 Requisitos Funcionales
- **Múltiples métricas**: Ingresos, unidades vendidas, categorías de productos
- **Visualizaciones interactivas**: Gráficos dinámicos con Plotly
- **Datos ficticios**: Generación automática de datos históricos de ventas
- **Forecast**: Proyecciones basadas en tendencias históricas
- **Dashboard interactivo**: Filtros por período, categoría, producto

## 🏗️ Arquitectura Simplificada

### Estructura de Capas (3 capas principales)

```
src/
├── models/                    # 🔵 Modelos de datos
│   ├── __init__.py
│   ├── sale.py               # Modelo Sale
│   ├── product.py            # Modelo Product
│   └── forecast.py           # Modelo Forecast
│
├── services/                  # 🟢 Lógica de negocio
│   ├── __init__.py
│   ├── data_service.py       # Servicio de datos
│   ├── forecast_service.py   # Servicio de forecast
│   └── metrics_service.py    # Servicio de métricas
│
├── data/                      # 🟡 Generación de datos
│   ├── __init__.py
│   └── generator.py          # Generador de datos ficticios
│
├── ui/                        # 🔴 Interfaz de usuario
│   ├── __init__.py
│   ├── dashboard.py          # Dashboard principal
│   ├── components.py         # Componentes reutilizables
│   └── charts.py             # Gráficos
│
└── main.py                    # 🚀 Punto de entrada
```

## 📦 Dependencias del Proyecto

### requirements.txt
```
streamlit==1.31.0
pandas==2.2.0
numpy==1.26.3
plotly==5.18.0
```

## 🔧 Implementación por Capa

### 1. Models Layer (Modelos)
**Responsabilidad**: Definir estructuras de datos

**Modelos**:
- `Sale`: Representa una venta individual
- `Product`: Representa un producto
- `Forecast`: Representa una proyección de ventas

### 2. Services Layer (Servicios)
**Responsabilidad**: Lógica de negocio y orquestación

**Servicios**:
- `DataService`: Obtiene y filtra datos de ventas
- `ForecastService`: Genera proyecciones de ventas
- `MetricsService`: Calcula KPIs y métricas

### 3. Data Layer (Datos)
**Responsabilidad**: Generación y gestión de datos

**Componentes**:
- `DataGenerator`: Genera datos históricos realistas

### 4. UI Layer (Interfaz)
**Responsabilidad**: Renderizar UI y manejar interacción

**Componentes**:
- `Dashboard`: Vista principal del dashboard
- `Components`: Componentes reutilizables (filtros, tarjetas)
- `Charts`: Componentes gráficos

## 📊 Generación de Datos Ficticios

### Criterios de Generación
- **Período**: 24 meses de datos históricos
- **Productos**: 10 productos diferentes
- **Categorías**: 3 categorías (Electrónica, Ropa, Alimentos)
- **Estacionalidad**: Patrones estacionales realistas
- **Tendencia**: Crecimiento gradual del 5-10% anual
- **Variabilidad**: Ruido aleatorio del 10-15%

### Métricas Calculadas
1. **Ingresos Totales**: Suma de ventas en moneda
2. **Unidades Vendidas**: Cantidad de productos vendidos
3. **Ticket Promedio**: Ingresos / Unidades
4. **Crecimiento MoM**: Crecimiento mes a mes
5. **Crecimiento YoY**: Crecimiento año a año

## 🎨 Visualizaciones Interactivas

### Gráficos Implementados
1. **Línea de Tendencia**: Evolución de ventas en el tiempo
2. **Barras por Categoría**: Ventas por categoría de producto
3. **Forecast Chart**: Proyecciones con intervalos de confianza
4. **KPI Cards**: Tarjetas con métricas clave
5. **Tabla de Datos**: Datos detallados con filtros

### Filtros Disponibles
- Selector de período (últimos 3, 6, 12, 24 meses)
- Selector de categoría
- Selector de producto
- Selector de métrica (ingresos, unidades, ticket)

## 🔄 Flujo de Datos

```
Usuario → Streamlit UI → Services → Data Generator
                ↓              ↓           ↓
            Presentación    Lógica      Datos
```

## ✅ Criterios de Aceptación

1. ✅ La aplicación se ejecuta sin errores
2. ✅ Se muestran datos ficticios realistas
3. ✅ Los filtros funcionan correctamente
4. ✅ Las visualizaciones son interactivas
5. ✅ El forecast muestra proyecciones coherentes
6. ✅ La arquitectura sigue principios de Clean Architecture
7. ✅ El código está bien organizado y documentado

## 📝 Próximos Pasos

1. Crear estructura de directorios
2. Implementar Models
3. Implementar Data Generator
4. Implementar Services
5. Implementar UI (Dashboard, Components, Charts)
6. Crear punto de entrada (main.py)
7. Crear requirements.txt
8. Actualizar README.md
9. Probar aplicación completa

## 🎓 Beneficios de esta Arquitectura

1. **Simplicidad**: Menos capas, más fácil de entender
2. **Mantenibilidad**: Código organizado y modular
3. **Testeabilidad**: Cada componente puede probarse
4. **Escalabilidad**: Fácil agregar nuevas funcionalidades
5. **Claridad**: Flujo de datos claro y directo
