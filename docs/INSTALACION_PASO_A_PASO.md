# Guía paso a paso para instalar los módulos BAUFER en Odoo 18

> **Objetivo:** llevar el código de este repositorio a tu instancia de Odoo (local u Odoo.sh) y dejar instalado el módulo `baufer_base` sin perderte en tecnicismos.
>
> **Formato:** instrucciones en español sencillo, con ejemplos reales y chequeos después de cada paso.

---

## 1. Antes de tocar nada

| Necesitas | Cómo comprobarlo |
|-----------|------------------|
| **Odoo 18.0 Enterprise** instalado | Entra a tu Odoo y abajo a la derecha debe decir `Odoo 18.0+e`. |
| **Acceso de administrador** | Debes poder ver el menú **Settings/Ajustes**. |
| **Módulos base ya instalados** (`base`, `contacts`, `sale`, `purchase`, `stock`, `product`) | En **Apps** busca cada uno y asegúrate de que diga **Installed**. |
| **Acceso al servidor o a Odoo.sh** | Debes poder hacer `git clone` / `git push` o subir archivos por SFTP. |
| **Python 3.10+ y PostgreSQL 14+** (solo instalaciones locales) | Ejecuta `python3 --version` y `psql --version` en tu terminal.

Si algo falta, detente y resuélvelo primero; Odoo no instalará el módulo correctamente sin esos requisitos.

---

## 2. Descarga o actualiza el código

### Opción A: primer clon
```bash
# clona el repositorio desde GitHub u Odoo.sh
cd /ruta/donde/guardas/proyectos

# reemplaza <> con la URL real
git clone <url-del-repositorio>
cd BFR
```

> **¿Hay submódulos?** Este repositorio principal no define submódulos de Git. Si en tu fork o rama aparecen submódulos adicionales,
> ejecuta inmediatamente después del clon:
> ```bash
> git submodule update --init --recursive
> ```
> Así te aseguras de que también se descarguen los módulos anidados antes de continuar con la instalación.

### Opción B: ya lo tenías
```bash
cd /ruta/donde/guardas/proyectos/BFR
git pull
```

> **Chequeo rápido:** `ls` debe mostrar las carpetas `baufer_base/`, `baufer_modules/`, `docs/`, etc.

---

## 3. Copia el módulo donde Odoo lo busca

### Si usas **Odoo.sh**
1. Agrega el remoto una sola vez: `git remote add odoo <url-odoo.sh>`
2. Sube tus cambios: `git push odoo <nombre-de-tu-rama>`
3. Odoo.sh creará un *build* automáticamente y copiará `baufer_modules/baufer_base` al directorio correcto.

### Si tienes **Odoo instalado en tu propio servidor**
1. Identifica la carpeta de addons de tu instancia (por ejemplo `/opt/odoo/odoo-server/addons` o `/opt/odoo/custom-addons`).
2. Copia el módulo:
   ```bash
   cd /ruta/donde/guardas/proyectos/BFR
   cp -r baufer_modules/baufer_base /opt/odoo/custom-addons/
   ```
3. Verifica que la carpeta quedó completa (`__manifest__.py`, `models/`, `views/`, `data/`, `security/`).

> **Nota para submódulos**: Si `baufer_modules/baufer_base` proviene de un submódulo Git, confirma que el comando anterior lo copie con
> su contenido (`ls baufer_modules/baufer_base`). Si ves la carpeta vacía, vuelve al paso 2 y ejecuta `git submodule update --init --recursive`.

> **Chequeo rápido:** abre el archivo `/opt/odoo/custom-addons/baufer_base/__manifest__.py` y confirma que existe. Si no, la copia falló.

---

## 4. Dile a Odoo que hay cosas nuevas

### Desde la terminal (recomendado para admins)
```bash
# sustituye <db> por el nombre real de tu base de datos
/opt/odoo/odoo-bin -d <db> -u base
```

### Desde la interfaz de Odoo
1. Activa el modo desarrollador (**Settings → Activate the developer mode**).
2. Ve a **Apps → Update Apps List** y confirma.

> **Chequeo rápido:** al terminar, busca "BAUFER" en Apps; ya debería aparecer listado (aunque aún sin instalar).

---

## 5. Instala el módulo `baufer_base`

### Por consola
```bash
/opt/odoo/odoo-bin -d <db> -i baufer_base
```

### Por interfaz
1. Entra a **Apps** y asegúrate de tener activado "Show Apps from Uninstalled".
2. Busca "BAUFER Base".
3. Pulsa **Install**.

> **Chequeo rápido:** Odoo mostrará una barra de progreso y regresará al listado de Apps sin errores.

---

## 6. Comprueba que todo quedó bien

| Dónde mirar | Qué deberías ver |
|-------------|------------------|
| **Menú principal** | Un nuevo menú "BAUFER". |
| **Contactos → Clientes → pestaña Información BAUFER** | Campos como "Tipo de cliente", "Marcas principales", "Regiones donde opera". |
| **Productos → pestaña Información Repuesto** | Campos adicionales (marcas compatibles, número de parte, SLA, etc.). |
| **Catálogo → Marcas** | 10 marcas ya cargadas. |
| **Configuración → Regiones BAUFER** | 16 regiones con indicador de zona prioritaria. |

Si algo falta, revisa los logs (`/var/log/odoo/odoo-server.log`) buscando errores durante la instalación.

---

## 7. Actualizar el módulo cuando cambies el código

Cada vez que modifiques los archivos del módulo:

```bash
# después de copiar el nuevo código
/opt/odoo/odoo-bin -d <db> -u baufer_base
```

Eso recarga modelos, vistas y datos sin desinstalar el módulo.

---

## 8. Problemas frecuentes y soluciones

| Problema | Causa típica | Solución |
|----------|--------------|----------|
| `ModuleNotFoundError: No module named 'baufer_base'` | No copiaste la carpeta en el directorio de addons o faltó reiniciar el servicio. | Copia de nuevo la carpeta y reinicia `sudo service odoo restart`. |
| `psycopg2.errors.UndefinedTable` | Olvidaste actualizar la base antes de instalar. | Ejecuta `-u base` o `-u baufer_base` según corresponda. |
| Odoo no muestra "BAUFER Base" en Apps | No activaste "Show Apps from Uninstalled" o no actualizaste la lista. | Activa la casilla y repite **Update Apps List**. |
| Error de permisos al copiar archivos | Usuario `odoo` no puede leer la carpeta. | Ajusta permisos: `sudo chown -R odoo:odoo /opt/odoo/custom-addons/baufer_base`. |

---

## 9. ¿Necesitas reinstalar desde cero?

1. **Haz respaldo** de la base de datos desde Odoo (**Settings → Database Structure → Backups**).
2. Desinstala el módulo desde **Apps** o por consola con `-u base -i baufer_base` (si necesitas cargar datos limpios).
3. Vuelve a seguir los pasos 3 a 6.

> Consejo de viejo: siempre revisa los logs. Si Odoo muestra un error rojo, copia el mensaje completo y búscalo en `odoo-server.log`; normalmente indica qué archivo dio problemas.

---

## 10. Glosario rápido

- **Addons**: carpetas donde Odoo busca los módulos.
- **Manifest (`__manifest__.py`)**: archivo que describe el módulo.
- **Build (Odoo.sh)**: ambiente temporal donde Odoo instala todo para probar.
- **Modo desarrollador**: opción que desbloquea menús técnicos en la interfaz.
- **Actualizar (`-u`)**: volver a cargar un módulo ya instalado.

Con esta guía deberías poder instalar y reinstalar las "weás" sin necesidad de ayuda externa. Si algo no funciona, vuelve a leer el paso correspondiente y valida cada chequeo rápido antes de continuar.
