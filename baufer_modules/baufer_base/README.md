# BAUFER Base

Módulo fundacional del ecosistema BAUFER para Odoo 18.0 Enterprise. Reúne los catálogos maestros y las extensiones core de
Contactos y Productos necesarias para operar el negocio de importación y venta de repuestos de maquinaria pesada.

> **Ámbito:** Datos maestros, enriquecimiento de modelos estándar y configuración inicial para todas las demás apps BAUFER.

---

## 1. Información rápida

| Ítem | Detalle |
|------|---------|
| **Nombre técnico** | `baufer_base` |
| **Versión** | 18.0.1.0.0 |
| **Dependencias** | `base`, `product`, `stock`, `sale`, `purchase`, `contacts` |
| **Datos cargados** | 10 marcas, 16 regiones, 10 categorías de producto |
| **Menú raíz** | `BAUFER` |
| **Usuarios objetivo** | Área comercial, logística y gerencia |
| **Estado** | En producción |

### Instalación exprés

```bash
# Copia el módulo a la ruta de addons y luego ejecuta
odoo-bin -d <database> -i baufer_base
```

> ¿Prefieres una guía paso a paso con chequeos intermedios? Revisa
> [`docs/INSTALACION_PASO_A_PASO.md`](../../docs/INSTALACION_PASO_A_PASO.md).

---

## 2. Estructura del módulo

```text
baufer_base/
├── __manifest__.py      # Metadatos, dependencias y assets a cargar
├── __init__.py          # Importa los modelos Python declarados
├── data/                # Catálogos maestros precargados
├── models/              # Clases Python (nuevos modelos + herencias)
├── security/            # Reglas de acceso (ir.model.access.csv)
└── views/               # Vistas, menús y acciones del módulo
```

| Carpeta / Archivo | Rol dentro del módulo |
|-------------------|-----------------------|
| `data/product_brands.xml` | Alta de las 10 marcas soportadas por BAUFER (Caterpillar, Komatsu, etc.). |
| `data/product_categories.xml` | Jerarquía base de categorías de repuestos para facilitar filtros y reportes. |
| `data/regions.xml` | Catálogo de regiones de Chile con flag de zonas mineras. |
| `models/product_brand.py` | Define el nuevo modelo `product.brand`. |
| `models/baufer_region.py` | Define el nuevo modelo `baufer.region`. |
| `models/res_partner.py` | Extiende `res.partner` con campos comerciales y SLA. |
| `models/product_template.py` | Extiende `product.template` con datos técnicos y logísticos. |
| `views/res_partner_views.xml` | Menú raíz, vistas de contactos y regiones. |
| `views/product_views.xml` | Vistas de productos y marcas. |

---

## 3. Modelos y campos

### 3.1 Nuevos modelos

#### `product.brand`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | Char (req.) | Nombre comercial de la marca. |
| `code` | Char (req., único) | Identificador corto (ej: `CAT`). |
| `description` | Text | Descripción extendida de la marca. |
| `logo` | Binary | Logotipo para vistas kanban/form. |
| `product_ids` | One2many (`product.template`) | Productos asociados. |
| `partner_ids` | Many2many (`res.partner`) | Clientes que trabajan con la marca. |
| `product_count` | Integer (compute) | Cantidad de productos vinculados. |
| `partner_count` | Integer (compute) | Cantidad de clientes vinculados. |

#### `baufer.region`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | Char (req.) | Nombre de la región. |
| `code` | Char (req., único) | Código abreviado (ej: `AN`). |
| `sequence` | Integer | Orden de despliegue en menús/listas. |
| `mining_area` | Boolean | Marca la región como zona minera prioritaria. |
| `service_coverage` | Selection | Estado de cobertura BAUFER (Completa / Parcial / Sin cobertura). |
| `partner_ids` | Many2many (`res.partner`) | Clientes presentes en la región. |
| `partner_count` | Integer (compute) | Número de clientes asociados. |

### 3.2 Extensiones de modelos existentes

#### `res.partner`
| Campo | Tipo | Categoría |
|-------|------|-----------|
| `customer_type` | Selection | Segmentación comercial (Arriendo, Minería, etc.). |
| `fleet_size` | Integer | Tamaño de flota declarada por el cliente. |
| `main_brands` | Many2many (`product.brand`) | Marcas principales que opera. |
| `equipment_types` | Many2many (`product.category`) | Tipos de equipo en operación. |
| `region_operations` | Many2many (`baufer.region`) | Regiones donde mantiene operaciones. |
| `credit_days` | Integer | Días de crédito otorgados. |
| `payment_terms` | Selection | Términos de pago acordados. |
| `is_mining_sector` | Boolean (compute) | Verdadero si opera en una región minera o su tipo es minería. |
| `sla_15min_compliance` | Float (compute) | % de oportunidades atendidas dentro del SLA de 15 minutos. |
| `average_response_time` | Float (compute) | Tiempo promedio de primera respuesta en minutos. |
| `lifetime_value` | Monetary (compute) | Monto acumulado de ventas al cliente. |
| `average_ticket` | Monetary (compute) | Ticket promedio de venta. |
| `purchase_frequency` | Float (compute) | Frecuencia de compra mensual. |
| `last_purchase_date` | Date (compute) | Fecha de la última orden confirmada. |
| `risk_level` | Selection | Nivel de riesgo crediticio (Bajo/Medio/Alto). |
| `nps_score` | Integer | Net Promoter Score reportado. |
| `total_orders` | Integer (compute) | Número total de órdenes confirmadas. |

#### `product.template`
| Campo | Tipo | Categoría |
|-------|------|-----------|
| `part_number` | Char | Número de parte del fabricante. |
| `oem_number` | Char | Código OEM alternativo. |
| `brand_id` | Many2one (`product.brand`) | Marca principal del repuesto. |
| `compatible_brands` | Many2many (`product.brand`) | Marcas de maquinaria compatibles adicionales. |
| `engine_type` | Selection | Tipo de motor compatible (Diesel, Gasolina, Gas, Eléctrico, Híbrido, N/A). |
| `equipment_model` | Char | Modelos específicos de maquinaria. |
| `critical_part` | Boolean | Marca si es un componente crítico. |
| `minimum_stock` | Float | Stock mínimo operativo requerido. |
| `current_stock` | Float (compute) | Stock disponible en tiempo real (suma de variantes). |
| `stock_status` | Selection (compute) | Estado operacional (En stock / Bajo / Sin stock / Por pedir). |
| `lead_time_days` | Integer | Lead time promedio de importación. |
| `supplier_id` | Many2one (`res.partner`) | Proveedor principal. |
| `last_import_date` | Date | Fecha de la última importación. |
| `import_frequency` | Integer | Frecuencia de importación en días. |
| `next_import_date` | Date (compute) | Próxima importación estimada según frecuencia. |
| `sales_count` | Integer (compute) | Cantidad total vendida. |
| `last_sale_date` | Date (compute) | Fecha de la última venta. |
| `rotation_category` | Selection | Clasificación de rotación (Alta/Media/Baja/Obsoleto). |

---

## 4. Vistas y experiencia de usuario

| Vista | Archivo | Descripción |
|-------|---------|-------------|
| Menú principal BAUFER + submenús | `views/res_partner_views.xml` | Crea el menú raíz y accesos a Clientes, Catálogo y Configuración. |
| `res.partner` Form | `views/res_partner_views.xml` | Añade pestaña "Información BAUFER" con campos comerciales, métricas y SLA. |
| `res.partner` Tree | `views/res_partner_views.xml` | Muestra etiquetas de riesgo, LTV y sector minero en la lista. |
| `res.partner` Kanban | `views/res_partner_views.xml` | Badges para sector minero y nivel de riesgo. |
| `product.template` Form | `views/product_views.xml` | Nueva pestaña "Información de Repuesto" con bloques técnicos, stock e importación. |
| `product.template` Kanban | `views/product_views.xml` | Badges para criticidad, stock status y marca. |
| `product.brand` Tree/Form | `views/product_views.xml` | Gestión de catálogos con contadores y logotipos. |
| `baufer.region` Tree/Form | `views/res_partner_views.xml` | Visualización de regiones resaltando zonas mineras. |

> Las vistas se apoyan únicamente en componentes estándar de Odoo, por lo que son compatibles con los temas por defecto y futuras
> actualizaciones menores.

---

## 5. Seguridad y permisos

| Grupo | Permisos | Nota |
|-------|----------|------|
| Usuarios Internos | Lectura de marcas, regiones y campos BAUFER en contactos/productos. |
| Vendedores | Lectura y escritura sobre contactos BAUFER, productos y marcas. |
| Gerentes de Ventas | Control total (create/write/unlink) sobre los modelos agregados. |

- Los permisos se controlan mediante `security/ir.model.access.csv`.
- No se definen record rules adicionales en este módulo; se delega al estándar de Odoo para simplificar la administración.

---

## 6. Datos maestros precargados

| Archivo | Contenido |
|---------|-----------|
| `product_brands.xml` | 10 marcas con código único, descripción y logo referenciado. |
| `product_categories.xml` | Categorías jerárquicas (Motor, Transmisión, Hidráulico, etc.). |
| `regions.xml` | 16 regiones de Chile con bandera `mining_area` y secuencia de despliegue. |

Cada archivo está marcado como `noupdate="1"` para evitar sobrescribir modificaciones manuales en producción.

---

## 7. Ciclo de vida y mantenimiento

1. **Instalación inicial**: ejecutar `odoo-bin -d <db> -i baufer_base` sobre una base con dependencias instaladas.
2. **Actualizaciones**: tras modificar código o datos, ejecutar `odoo-bin -d <db> -u baufer_base`.
3. **Pruebas manuales sugeridas**:
   - Crear un cliente nuevo en sector minero y verificar cálculo de `is_mining_sector`.
   - Registrar un producto con `critical_part=True` y revisar el badge en la vista kanban.
   - Asignar ventas a un cliente para validar los indicadores de `lifetime_value` y `average_ticket`.
4. **Migraciones**: si se agregan campos requeridos, incluir valores por defecto en los datos XML o scripts de post-init.

---

## 8. Integraciones futuras

| Módulo futuro | Dependencia esperada |
|---------------|----------------------|
| `baufer_crm` | Utilizará campos de SLA y segmentación de `res.partner`. |
| `baufer_sale` | Reutilizará `product.brand` y campos logísticos de `product.template`. |
| `baufer_inventory` | Profundizará en los indicadores de stock introducidos aquí. |
| `baufer_automation` | Tomará métricas de respuesta y criticidad para disparar alertas. |

---

## 9. Soporte

Para dudas operativas o incidencias abrir ticket en el service desk interno de BAUFER. Adjuntar siempre los logs de Odoo
(`odoo-server.log`) y capturas de pantalla de los formularios afectados.

