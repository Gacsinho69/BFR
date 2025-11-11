# Sistema ERP BAUFER - Odoo 18.0 Enterprise

Sistema ERP personalizado para **BAUFER (Inversiones Séneca SpA)**, empresa especializada en la importación y venta de repuestos para motores diesel, gasolina y gas orientada al sector de maquinaria pesada en Chile, con foco principal en el sector minero.

## 📋 Información de la Empresa

- **Razón Social**: Inversiones Séneca SpA (BAUFER)
- **RUT**: 76.XXX.XXX-X
- **Sector**: Importación y venta de repuestos para motores
- **Mercado Objetivo**: Empresas de arriendo de maquinaria pesada (foco en minería)
- **Modelo de Negocio**: 100% Customer-Oriented
- **SLA Crítico**: 15 minutos máximo para primer contacto

## 🎯 Principios Operacionales

- **"Sin datos, no hay acción"**: Todas las validaciones son obligatorias (validaciones hard)
- **Customer-Oriented**: El cliente es el centro de todas las operaciones
- **SLA 15 minutos**: Tiempo máximo de primer contacto con el cliente
- **Cobertura Nacional**: Foco en regiones mineras del norte de Chile

## 🏗️ Arquitectura del Sistema

### Stack Tecnológico

- **Plataforma**: Odoo 18.0 Enterprise
- **Deployment**: Odoo.sh (Cloud)
- **Python**: 3.10+
- **Base de datos**: PostgreSQL 14+
- **VCS**: GitHub
- **Branch Strategy**: development → staging → production

### Estructura de Módulos

```
baufer_base/              ✅ IMPLEMENTADO - Fase 1
├── models/
│   ├── res_partner.py
│   ├── product_template.py
│   ├── product_brand.py
│   └── baufer_region.py
├── data/
│   ├── product_brands.xml
│   ├── product_categories.xml
│   └── regions.xml
├── views/
│   ├── res_partner_views.xml
│   └── product_views.xml
└── security/
    └── ir.model.access.csv

├── baufer_crm/           📋 PENDIENTE - Fase 2
├── baufer_sale/          📋 PENDIENTE - Fase 3
├── baufer_inventory/     📋 PENDIENTE - Fase 4
└── baufer_automation/    📋 PENDIENTE - Fase 5
```

## ✅ Fase 1: baufer_base (COMPLETADA)

### Modelos Implementados

#### 1. **product.brand** (Nuevo Modelo)
Gestión de marcas de maquinaria pesada.

**Marcas Pre-cargadas**:
- Caterpillar (CAT)
- Komatsu (KOM)
- John Deere (JD)
- Volvo (VOL)
- JCB
- Case (CASE)
- Hyundai (HYU)
- Doosan (DOO)
- Hyster (HYS)
- Yale (YALE)

**Campos Principales**:
- `name`: Nombre de la marca
- `code`: Código corto (único, mayúsculas)
- `description`: Descripción de la marca
- `logo`: Logo de la marca
- `product_count`: Cantidad de productos (computed)
- `partner_count`: Cantidad de clientes (computed)

#### 2. **baufer.region** (Nuevo Modelo)
Gestión de regiones de Chile con énfasis en zonas mineras.

**Regiones Pre-cargadas**: Las 16 regiones de Chile

**Regiones Mineras** 🔶:
- Arica y Parinacota (AP)
- Tarapacá (TA)
- Antofagasta (AN) - Principal región minera
- Atacama (AT)

**Campos Principales**:
- `name`: Nombre de la región
- `code`: Código corto (único)
- `sequence`: Orden de visualización
- `mining_area`: Indica si es zona minera
- `service_coverage`: Indica cobertura BAUFER
- `partner_count`: Cantidad de clientes en región (computed)

#### 3. **res.partner** (Extensión)
Extensión del modelo de contactos/clientes con información específica BAUFER.

**Campos Nuevos - Datos Comerciales**:
- `customer_type`: Tipo de cliente (Arriendo, Transporte, Construcción, Minería, Otro)
- `fleet_size`: Tamaño de flota del cliente
- `main_brands`: Marcas principales que opera (Many2many)
- `equipment_types`: Tipos de equipos (Many2many)
- `region_operations`: Regiones donde opera (Many2many)
- `credit_days`: Días de crédito otorgados
- `payment_terms`: Términos de pago

**Campos Nuevos - Scoring y Métricas**:
- `lifetime_value`: Valor total de compras históricas (computed)
- `average_ticket`: Ticket promedio (computed)
- `purchase_frequency`: Frecuencia de compra mensual (computed)
- `last_purchase_date`: Fecha última compra (computed)
- `risk_level`: Nivel de riesgo crediticio

**Campos Nuevos - SLA y Atención**:
- `sla_15min_compliance`: % cumplimiento SLA 15 min (computed)
- `average_response_time`: Tiempo promedio respuesta (computed)
- `nps_score`: Net Promoter Score
- `is_mining_sector`: Indicador sector minero (computed)

#### 4. **product.template** (Extensión)
Extensión del modelo de productos para repuestos de maquinaria pesada.

**Campos Nuevos - Identificación**:
- `part_number`: Número de parte del fabricante
- `oem_number`: Número OEM
- `brand_id`: Marca del repuesto
- `engine_type`: Tipo de motor (Diesel, Gasolina, Gas, Eléctrico, Híbrido)
- `equipment_model`: Modelo(s) de equipo compatible
- `compatible_brands`: Marcas compatibles (Many2many)

**Campos Nuevos - Criticidad y Stock**:
- `critical_part`: Indica si es parte crítica
- `minimum_stock`: Stock mínimo requerido
- `current_stock`: Stock disponible actual (computed)
- `stock_status`: Estado del stock (computed)

**Campos Nuevos - Importación**:
- `lead_time_days`: Lead time de importación en días
- `supplier_id`: Proveedor principal
- `last_import_date`: Fecha última importación
- `import_frequency`: Frecuencia de importación en días
- `next_import_date`: Próxima importación estimada (computed)

**Campos Nuevos - Comercial**:
- `sales_count`: Cantidad vendida (computed)
- `last_sale_date`: Fecha última venta (computed)
- `rotation_category`: Categoría de rotación (Alta/Media/Baja/Obsoleto)

### Categorías de Productos Pre-cargadas

1. **Motor** - Componentes del motor
2. **Transmisión** - Sistema de transmisión
3. **Sistema Hidráulico** - Componentes hidráulicos
4. **Sistema Eléctrico** - Componentes eléctricos
5. **Filtros** - Filtros de aceite, aire, combustible
6. **Rodamiento** - Rodamientos y cojinetes
7. **Tren de Rodaje** - Componentes de desplazamiento
8. **Sistema Enfriamiento** - Radiadores, ventiladores
9. **Frenos** - Sistema de frenado
10. **Dirección** - Sistema de dirección

### Vistas Implementadas

#### Vistas de Clientes (res.partner)
- ✅ Form View extendida con pestaña "Información BAUFER"
- ✅ Tree View con indicadores visuales (colores según riesgo)
- ✅ Kanban View con badges de sector minero y riesgo
- ✅ Filtros de búsqueda avanzados
- ✅ Agrupaciones por tipo, riesgo, etc.

#### Vistas de Productos (product.template)
- ✅ Form View extendida con pestaña "Información Repuesto"
- ✅ Tree View con indicadores de stock (colores según estado)
- ✅ Kanban View con información de stock y rotación
- ✅ Filtros por criticidad, stock, rotación, tipo motor
- ✅ Agrupaciones por marca, tipo motor, estado stock

#### Vistas de Marcas (product.brand)
- ✅ Tree View con contador de productos y clientes
- ✅ Form View con logo y descripción

#### Vistas de Regiones (baufer.region)
- ✅ Tree View con indicador de zona minera
- ✅ Form View con información detallada

### Menús Implementados

```
BAUFER (menú raíz)
├── Clientes
├── Catálogo
│   ├── Productos
│   └── Marcas
└── Configuración
    └── Regiones
```

### Seguridad

Permisos configurados para:
- **Usuarios base**: Solo lectura
- **Vendedores**: Lectura y escritura
- **Gerentes**: Control total

## 🚀 Instalación

### Requisitos Previos

- Odoo 18.0 Enterprise instalado
- Acceso a Odoo.sh o instalación local
- Módulos base de Odoo: `base`, `product`, `stock`, `sale`, `purchase`, `contacts`

### Pasos de Instalación

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd BFR
```

2. **Copiar módulos a Odoo**:
```bash
# En Odoo.sh (la ruta del módulo ya es detectada automáticamente)
git push odoo <branch-name>

# En instalación local
cp -r baufer_base /path/to/odoo/addons/
```

3. **Actualizar lista de aplicaciones**:
```bash
# Desde CLI
odoo-bin -u all -d <database>

# Desde UI
Apps → Update Apps List
```

> 📚 **¿Necesitas instrucciones más guiadas?** Revisa [`docs/INSTALACION_PASO_A_PASO.md`](docs/INSTALACION_PASO_A_PASO.md) para seguir el proceso con verificaciones después de cada paso y soluciones a errores frecuentes.

4. **Instalar baufer_base**:
```bash
# Desde CLI
odoo-bin -i baufer_base -d <database>

# Desde UI
Apps → Buscar "BAUFER Base" → Install
```

### Verificación de Instalación

Después de la instalación, verificar que:

- ✅ El menú "BAUFER" aparece en la barra principal
- ✅ Se crearon 10 marcas en "Catálogo → Marcas"
- ✅ Se crearon 16 regiones en "Configuración → Regiones"
- ✅ Se crearon 10 categorías de productos (verificar en Productos)
- ✅ Los formularios de clientes muestran la pestaña "Información BAUFER"
- ✅ Los formularios de productos muestran la pestaña "Información Repuesto"

## 📊 Datos Maestros

### Marcas (10)
✅ Caterpillar, Komatsu, John Deere, Volvo, JCB, Case, Hyundai, Doosan, Hyster, Yale

### Regiones (16)
✅ Las 16 regiones de Chile, con 4 marcadas como zonas mineras

### Categorías de Productos (10)
✅ Motor, Transmisión, Sistema Hidráulico, Sistema Eléctrico, Filtros, Rodamiento, Tren de Rodaje, Sistema Enfriamiento, Frenos, Dirección

## 🔜 Próximas Fases

### Fase 2: baufer_crm
- Gestión de leads con BANT scoring
- Case ID único por oportunidad
- Tracking de SLA 15 minutos
- Seguimiento automatizado

### Fase 3: baufer_sale
- Proceso de ventas completo
- Cotizaciones con validación de stock
- Workflow de aprobaciones
- Términos comerciales

### Fase 4: baufer_inventory
- Gestión de stock
- Recepciones de importación
- Entregas a clientes
- Trazabilidad completa

### Fase 5: baufer_automation
- Cron jobs para SLA monitoring
- Seguimientos automáticos
- Alertas de stock
- Notificaciones de cotizaciones

## 📝 Convenciones de Código

### Nomenclatura
- Modelos: `baufer.nombre_modelo` (snake_case)
- Campos: `snake_case` en español descriptivo
- Métodos: `_verbo_accion` (prefijo _ para privados)
- Vistas: `baufer_modelo_vista_tipo`
- XML IDs: `baufer_module.descriptive_id`

### Validaciones
- Todos los campos críticos: `required=True`
- Validaciones hard con `@api.constrains`
- Mensajes de error en español
- Logging de acciones críticas

### Seguridad
- Grupos de acceso por módulo
- Reglas de registro según vendedor/región
- Audit trail en operaciones críticas

## 🤝 Contribución

Este es un proyecto interno de BAUFER. Para contribuir:

1. Crear una rama desde `development`
2. Seguir las convenciones de código establecidas
3. Probar en ambiente de staging
4. Crear Pull Request a `development`
5. Revisión y aprobación de gerencia
6. Merge a `production` tras validación

## 📄 Licencia

LGPL-3 - Ver archivo LICENSE para más detalles.

## 📧 Contacto

Para consultas sobre el sistema:
- **Empresa**: BAUFER - Inversiones Séneca SpA
- **Website**: https://www.baufer.cl

---

**Versión**: 18.0.1.0.0
**Última actualización**: 2025
**Estado**: Fase 1 Completada ✅
