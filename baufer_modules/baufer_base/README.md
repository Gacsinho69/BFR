# Módulo `baufer_base`

Este módulo agrupa las funcionalidades base del proyecto BAUFER sobre Odoo 18.0 Enterprise. Si recién te estás familiarizando con la estructura de Odoo, este archivo resume qué contiene cada subcarpeta para que puedas ubicarte con rapidez.

## ¿Qué hay dentro de la carpeta?

| Carpeta / Archivo            | ¿Para qué sirve? |
|------------------------------|------------------|
| `__manifest__.py`            | La "cédula de identidad" del módulo: nombre, versión, dependencias y archivos que Odoo debe cargar al instalarlo. |
| `__init__.py`                | Indica a Python qué modelos debe importar para que estén disponibles al arrancar Odoo. |
| `models/`                    | Clases Python que crean modelos nuevos (`product.brand`, `baufer.region`) y amplían los existentes (`res.partner`, `product.template`). |
| `views/`                     | Archivos XML que definen menús y formularios. Al instalar el módulo verás nuevas pestañas y campos en Contactos y Productos. |
| `data/`                      | Registros iniciales que se cargan automáticamente: marcas, categorías y regiones. Así no comienzas con catálogos vacíos. |
| `security/`                  | Reglas de seguridad (`ir.model.access.csv`) que otorgan permisos para ver y editar los modelos recién creados. |

## Flujo de carga simplificado

1. **Odoo lee `__manifest__.py`** y verifica dependencias.
2. **`__init__.py` importa los archivos de `models/`**, por lo que las clases quedan listas cuando Odoo arranca.
3. **Durante la instalación** se cargan los datos (`data/`) y las vistas (`views/`).
4. **Las reglas de `security/`** determinan quién puede interactuar con la información.

Con esto tienes una vista rápida del módulo; si abres cualquiera de las carpetas ahora ya sabes qué esperar dentro.
