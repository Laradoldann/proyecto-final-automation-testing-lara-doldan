# Proyecto final – Automation Testing

Framework de pruebas automatizadas en Python que combina **pruebas de interfaz (UI)** sobre [SauceDemo](https://www.saucedemo.com/) con Selenium WebDriver y **pruebas de API** sobre [JSONPlaceholder](https://jsonplaceholder.typicode.com/) con Requests. Genera un reporte HTML con capturas de pantalla de los fallos y un log detallado de cada ejecución.

Autora: Lara Doldan

## Objetivo

Demostrar un framework de testing completo y mantenible:

- Pruebas de UI con el patrón **Page Object Model**, escenarios positivos y negativos, y datos de prueba externos (CSV y JSON).
- Pruebas de API con los métodos GET, POST y DELETE, validación de códigos de estado y del contenido JSON, y peticiones encadenadas.
- Reporte HTML, capturas automáticas ante fallos y logging para facilitar la depuración.
- Tests independientes entre sí: cada test de UI abre su propio navegador y cada test de API usa su propio cliente.

## Tecnologías

| Herramienta | Uso |
|---|---|
| Python 3.9 o superior | Lenguaje principal |
| Pytest | Ejecución de las pruebas, fixtures y parametrización |
| Selenium WebDriver | Automatización del navegador (Chrome) |
| Requests | Pruebas de API |
| pytest-html | Reporte HTML |
| Git y GitHub | Control de versiones |
| GitHub Actions | Ejecución automática en cada push (opcional) |

## Requisitos previos

- Python 3.9 o superior (`python --version`)
- Google Chrome instalado (Selenium descarga solo el driver que necesita)
- Git
- Conexión a internet (los tests usan sitios y APIs públicas)

## Estructura del proyecto

```
proyecto-final-automation-testing-lara-doldan/
├── .github/workflows/tests.yml   # GitHub Actions: corre las pruebas y guarda los reportes
├── api/
│   └── jsonplaceholder_client.py # Cliente de la API (una función por endpoint)
├── config/
│   └── settings.py               # URLs, timeouts, rutas y credenciales de demo
├── data/
│   ├── login.csv                 # Usuarios y resultados esperados del login
│   ├── checkout.json             # Datos de clientes para el checkout
│   └── posts_api.json            # Cuerpos de los POST de la API
├── docs/
│   └── checklist-consigna.md     # Cómo se cumple cada punto de la consigna
├── pages/                        # Page Objects (interacción con cada pantalla)
│   ├── base_page.py              # Acciones comunes con esperas explícitas
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── product_detail_page.py
│   ├── cart_page.py
│   └── checkout_page.py          # Las 3 pantallas del checkout
├── reports/                      # Reporte HTML, log y capturas (se generan al ejecutar)
├── tests/
│   ├── ui/                       # Pruebas de UI (solo usan Page Objects)
│   │   ├── conftest.py           # Fixtures: login_page, inventory_page, checkout_informacion
│   │   ├── test_login.py
│   │   ├── test_inventory.py
│   │   ├── test_cart.py
│   │   └── test_checkout.py
│   └── api/
│       ├── conftest.py           # Fixture cliente_api
│       ├── test_posts_api.py     # GET, POST y DELETE
│       └── test_flujos_encadenados.py
├── utils/
│   ├── data_reader.py            # Lectura de CSV/JSON y parámetros de pytest
│   └── screenshots.py            # Guardado de capturas con nombre descriptivo
├── conftest.py                   # Navegador, capturas automáticas y registro de resultados
├── pytest.ini                    # Reporte, logging y marcadores
└── requirements.txt              # Dependencias
```

**Cómo se reparte el trabajo:** los tests dicen *qué* se prueba (`tests/`), los Page Objects saben *cómo* interactuar con cada pantalla (`pages/`) y los datos viven aparte (`data/`). Si SauceDemo cambia un selector, se corrige en un solo lugar de `pages/`.

## Instalación

1. Abrir una terminal en la carpeta del proyecto (en VS Code: *Terminal → New Terminal*).
2. Crear y activar un entorno virtual:

   ```bash
   python -m venv venv

   # Windows (PowerShell)
   venv\Scripts\Activate.ps1
   # Windows (CMD)
   venv\Scripts\activate.bat
   # Mac / Linux
   source venv/bin/activate
   ```

   Si PowerShell no deja activar el entorno, ejecutar una vez `Set-ExecutionPolicy -Scope Process RemoteSigned` y volver a intentar.

3. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Configuración del entorno

No hace falta configurar nada: los valores por defecto están en `config/settings.py`. Si se necesita cambiar alguno, se puede hacer con variables de entorno:

| Variable | Por defecto | Para qué sirve |
|---|---|---|
| `BASE_URL` | `https://www.saucedemo.com/` | Sitio de las pruebas de UI |
| `UI_TIMEOUT` | `10` | Segundos máximos de las esperas explícitas |
| `API_URL` | `https://jsonplaceholder.typicode.com` | API de las pruebas de API |
| `API_TIMEOUT` | `10` | Segundos máximos de cada petición |

Las credenciales de `config/settings.py` son las de demo que SauceDemo publica en su propia página de login.

## Cómo ejecutar las pruebas

Todos los comandos se ejecutan desde la raíz del proyecto, con el entorno virtual activado.

```bash
# Todas las pruebas (UI + API)
pytest

# Solo UI
pytest -m ui

# Solo API
pytest -m api

# UI sin abrir la ventana de Chrome
pytest -m ui --headless

# Un archivo, un test o un grupo por nombre
pytest tests/ui/test_login.py
pytest tests/ui/test_login.py::test_cerrar_sesion
pytest -k "checkout"
```

Si se ejecuta una parte (por ejemplo solo la API), el reporte `reports/reporte.html` se reemplaza por el de esa ejecución. Para conservar varios reportes se puede indicar otro nombre:

```bash
pytest -m api --html=reports/reporte_api.html
pytest -m ui --html=reports/reporte_ui.html
```

## Cómo comprobar que todo funciona (paso a paso)

1. **Verificar que pytest encuentra los tests** (no abre el navegador ni usa internet):
   ```bash
   pytest --collect-only -q -o addopts=""
   ```
   Debe terminar con `42 tests collected` (27 de UI y 15 de API).
2. **Ejecutar la API:** `pytest -m api`. Son pruebas rápidas.
3. **Ejecutar la UI:** `pytest -m ui`. Se abre Chrome, así se puede ver el recorrido de cada test.
4. **Abrir el reporte** `reports/reporte.html` en el navegador y revisar los resultados.
5. **Comprobar las capturas de fallos** (opcional): en `tests/ui/test_inventory.py` cambiar `CANTIDAD_DE_PRODUCTOS = 6` por `7`, ejecutar `pytest tests/ui/test_inventory.py -k catalogo` y verificar que el test falla, que aparece una imagen en el reporte y que hay un archivo nuevo en `reports/screenshots/`. Después deshacer el cambio (`git checkout tests/ui/test_inventory.py`).

## Reportes HTML

Cada ejecución genera `reports/reporte.html` (un único archivo, se abre con doble clic). Muestra:

- Resumen: cantidad de tests pasados, fallados y errores, y duración total.
- Tabla con cada test, su resultado y su **duración**.
- Al expandir un test fallado: el error, el log capturado y la **captura de pantalla** del momento del fallo.

Se puede filtrar por resultado con las casillas de la parte superior.

## Capturas de pantalla

Cuando falla un test de UI, **o su preparación** (por ejemplo, si el login dentro de un fixture no funciona), se guarda una captura en `reports/screenshots/` y se adjunta al reporte HTML.

El nombre incluye fecha, hora, nombre del test y la fase en la que falló (`setup` = preparación, `call` = el test en sí):

```
2026-11-07_15-30-45_test_login_con_datos_invalidos_usuario_vacio_call.png
```

Esta carpeta no se sube a Git: las capturas se generan en cada ejecución.

## Logging

El log se guarda en `reports/ejecucion.log` y se reemplaza en cada ejecución. Formato:

```
2026-11-07 15:30:45 | INFO    | pages.login_page | Iniciando sesión con el usuario 'standard_user'
```

Registra el inicio y el resultado de cada test, los pasos de los Page Objects (abrir páginas, clics, productos agregados), cada petición de la API con su código de respuesta y tiempo, y los errores con su causa y la ruta de la captura. Las contraseñas escritas en los formularios no se registran.

Para ver el log también en la consola durante la ejecución:

```bash
pytest -o log_cli=true -o log_cli_level=INFO
```

## Casos de prueba

### UI (SauceDemo) – 27 tests

| Archivo | Test | Qué verifica |
|---|---|---|
| `test_login.py` | `test_login_exitoso` (2 usuarios del CSV) | Con credenciales válidas se llega al catálogo |
| | `test_login_con_datos_invalidos` (5 casos del CSV) | Usuario bloqueado, contraseña incorrecta, usuario inexistente y campos vacíos muestran el error correcto |
| | `test_acceso_directo_al_catalogo_sin_iniciar_sesion` | No se puede entrar al catálogo sin login |
| | `test_cerrar_sesion` | El menú cierra la sesión y vuelve al login |
| `test_inventory.py` | `test_catalogo_muestra_los_productos` | 6 productos con nombre y precio |
| | `test_ordenar_productos` (4 criterios) | Orden por nombre y por precio, ascendente y descendente |
| | `test_abrir_detalle_de_un_producto_y_volver` | Navegación al detalle y regreso al catálogo |
| `test_cart.py` | `test_agregar_un_producto_al_carrito` (2 productos) | Contador, botón "Remove" y contenido del carrito |
| | `test_agregar_varios_productos_al_carrito` | Tres productos agregados aparecen en el carrito |
| | `test_quitar_un_producto_desde_el_carrito` | Al quitar uno queda solo el otro |
| | `test_carrito_sin_productos_esta_vacio` | Carrito vacío sin contador |
| `test_checkout.py` | `test_compra_completa` (2 clientes del JSON) | Flujo completo hasta "Thank you for your order!" |
| | `test_checkout_con_datos_incompletos` (3 casos del JSON) | Mensajes de error por nombre, apellido o código postal vacíos |
| | `test_resumen_calcula_bien_subtotal_y_total` | Subtotal = suma de precios; total = subtotal + impuesto |
| | `test_cancelar_checkout_vuelve_al_carrito` | Cancelar conserva el producto en el carrito |

### API (JSONPlaceholder) – 15 tests

| Test | Método | Qué verifica |
|---|---|---|
| `test_listar_todos_los_posts` | GET | 200, 100 posts, estructura y tipos de cada campo |
| `test_obtener_un_post_existente` (ids 1, 50, 100) | GET | 200, `Content-Type` JSON y el id correcto |
| `test_obtener_un_post_inexistente_devuelve_404` (ids 0 y 9999) | GET | Escenario de error: 404 y cuerpo vacío |
| `test_filtrar_posts_por_usuario` (usuarios 1, 5 y 999) | GET | Filtro por `userId`; usuario inexistente devuelve lista vacía |
| `test_crear_un_post` (3 casos del JSON) | POST | 201 y el contenido enviado vuelve en la respuesta |
| `test_eliminar_un_post` | DELETE | 200 y cuerpo vacío |
| `test_post_usuario_y_comentarios_son_consistentes` | GET encadenado | Post → usuario del post → comentarios del post |
| `test_post_creado_no_se_puede_consultar_porque_la_api_no_lo_guarda` | POST + GET | Con el id devuelto por el POST, el GET responde 404 |

## Datos de prueba

- `data/login.csv`: un caso por fila (`caso`, `usuario`, `password`, `resultado`, `mensaje_error`). Agregar una fila crea un test nuevo automáticamente.
- `data/checkout.json`: clientes para la compra exitosa y casos de datos inválidos con su mensaje esperado.
- `data/posts_api.json`: cuerpos de los POST de la API.

Cada caso usa su campo `caso` como nombre del test en el reporte, por ejemplo `test_login_con_datos_invalidos[usuario_vacio]`.

## Cómo agregar una prueba nueva

1. Si la pantalla ya tiene Page Object, agregar el método que falte en `pages/`; si no, crear una clase nueva que herede de `BasePage`.
2. Escribir el test en `tests/ui/` (o `tests/api/`) con `pytestmark = pytest.mark.ui` o `api`, usando los fixtures existentes.
3. Si necesita varios juegos de datos, agregarlos a `data/` y leerlos con `leer_csv` o `leer_json`.

## GitHub Actions

El archivo `.github/workflows/tests.yml` ejecuta `pytest --headless` en cada push o pull request a `main` (y manualmente desde la pestaña *Actions*). Al terminar, guarda la carpeta `reports/` (reporte HTML, log y capturas) como artefacto descargable de la ejecución.

## Decisiones y limitaciones

- **SauceDemo no tiene buscador.** El filtrado del catálogo se prueba con el selector de orden.
- **JSONPlaceholder simula las escrituras:** un POST devuelve 201 con el id 101, pero no guarda nada, y un DELETE devuelve 200 sin borrar. Por eso esos tests validan la respuesta y no el estado posterior del servidor. Esto está documentado en el último test de la API.
- **Esperas:** solo explícitas (`WebDriverWait`); no se usan `time.sleep()` ni esperas implícitas.
- **Un navegador por test:** es un poco más lento, pero garantiza que ningún test dependa de otro.
- Las pruebas dependen de sitios públicos: si SauceDemo o JSONPlaceholder están caídos o lentos, los tests pueden fallar por eso y no por un error del código.

## Problemas frecuentes

| Síntoma | Qué probar |
|---|---|
| `ModuleNotFoundError: selenium` o `pytest_html` | Activar el entorno virtual y volver a ejecutar `pip install -r requirements.txt` |
| Chrome no abre o falla el driver | Actualizar Google Chrome; la primera vez Selenium necesita internet para descargar el driver |
| Los tests de API fallan con 403 | JSONPlaceholder a veces bloquea ciertas redes o VPN; probar desde otra conexión |
| `unrecognized arguments: --html` | Falta pytest-html: reinstalar las dependencias |
