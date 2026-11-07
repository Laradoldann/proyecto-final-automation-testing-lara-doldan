# Proyecto final – Automation Testing

Framework de pruebas automatizadas en Python. Incluye pruebas de interfaz sobre [SauceDemo](https://www.saucedemo.com/) con Selenium WebDriver y pruebas de API sobre [JSONPlaceholder](https://jsonplaceholder.typicode.com/) con Requests. Genera un reporte HTML con capturas de pantalla de los fallos y un log de cada ejecución.

Autora: Lara Doldan

## Objetivo

- Automatizar flujos completos de UI (login, navegación, carrito y checkout) con el patrón Page Object Model, con escenarios positivos y negativos y datos de prueba en CSV y JSON.
- Automatizar pruebas de API con GET, POST y DELETE, validando códigos de estado y contenido JSON.
- Generar reportes HTML, capturas automáticas ante fallos y logging.
- Mantener los tests independientes entre sí.

## Tecnologías

Python 3.9 o superior, Pytest, Selenium WebDriver (Chrome), Requests, pytest-html, Git y GitHub Actions.

## Requisitos previos

- Python 3.9 o superior
- Google Chrome (Selenium descarga el driver automáticamente)
- Git
- Conexión a internet

## Estructura del proyecto

```
├── .github/workflows/tests.yml   # GitHub Actions
├── api/
│   └── jsonplaceholder_client.py # Cliente de la API (un método por endpoint)
├── config/
│   └── settings.py               # URLs, timeouts, rutas y usuario de demo
├── data/
│   ├── login.csv                 # Usuarios del login y resultado esperado
│   ├── checkout.json             # Datos de clientes para el checkout
│   └── posts_api.json            # Cuerpos de los POST de la API
├── pages/                        # Page Objects
│   ├── base_page.py              # Acciones comunes con esperas explícitas
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── product_detail_page.py
│   ├── cart_page.py
│   └── checkout_page.py          # Las tres pantallas del checkout
├── reports/                      # Reporte, log y capturas (se generan al ejecutar)
├── tests/
│   ├── ui/                       # test_login, test_inventory, test_cart, test_checkout
│   └── api/                      # test_posts_api, test_flujos_encadenados
├── utils/
│   ├── data_reader.py            # Lectura de CSV y JSON
│   └── screenshots.py            # Guardado de capturas
├── conftest.py                   # Navegador, capturas en fallos y registro de resultados
├── pytest.ini                    # Reporte, log y marcadores
└── requirements.txt
```

Los tests (`tests/`) dicen qué se prueba, los Page Objects (`pages/`) saben cómo interactuar con cada pantalla y los datos están separados en `data/`.

## Instalación

1. Abrir una terminal en la carpeta del proyecto.
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

   Si PowerShell no permite activarlo, ejecutar antes `Set-ExecutionPolicy -Scope Process RemoteSigned`.

3. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Configuración del entorno

No hace falta configurar nada. Los valores están en `config/settings.py` y se pueden cambiar con variables de entorno: `BASE_URL`, `UI_TIMEOUT`, `API_URL` y `API_TIMEOUT`.

## Cómo ejecutar las pruebas

Desde la raíz del proyecto, con el entorno virtual activado:

```bash
pytest                      # todas las pruebas (UI y API)
pytest -m ui                # solo UI
pytest -m api               # solo API
pytest -m ui --headless     # UI sin abrir la ventana de Chrome
pytest tests/ui/test_login.py                    # un archivo
pytest tests/ui/test_login.py::test_cerrar_sesion  # un test
```

Cada ejecución reemplaza `reports/reporte.html`. Para guardar reportes separados:

```bash
pytest -m ui --html=reports/reporte_ui.html
pytest -m api --html=reports/reporte_api.html
```

Para comprobar rápido que pytest encuentra los tests sin abrir el navegador:

```bash
pytest --collect-only -q -o addopts=""
```

Debe indicar 42 tests (27 de UI y 15 de API).

## Reportes HTML

`reports/reporte.html` es un único archivo que se abre con doble clic. Muestra el resumen (pasados, fallados y duración total), la lista de tests con su resultado y duración, y, al expandir un test fallado, el error, el log y la captura de pantalla.

## Capturas de pantalla

Cuando falla un test de UI, o su preparación (por ejemplo un login dentro de un fixture), se guarda una captura en `reports/screenshots/` y se adjunta al reporte. El nombre incluye fecha, hora, test y fase (`setup` es la preparación y `call` es el test en sí):

```
2026-11-07_15-30-45_test_login_con_datos_invalidos_usuario_vacio_call.png
```

## Logging

El log queda en `reports/ejecucion.log` y se reemplaza en cada ejecución:

```
2026-11-07 15:30:45 | INFO    | pages.login_page | Iniciando sesión con el usuario 'standard_user'
```

Registra el inicio y el resultado de cada test, los pasos de los Page Objects, cada petición de la API con su código de respuesta y tiempo, y los errores con la ruta de su captura. Para verlo también en la consola:

```bash
pytest -o log_cli=true -o log_cli_level=INFO
```

## Casos de prueba

**UI (SauceDemo) – 27 tests**

| Archivo | Tests |
|---|---|
| `test_login.py` | Login exitoso (2 usuarios del CSV), login inválido (5 casos del CSV), acceso directo al catálogo sin login, cerrar sesión |
| `test_inventory.py` | Catálogo con 6 productos, ordenar por nombre y precio (4 criterios), detalle de producto y volver |
| `test_cart.py` | Agregar un producto (2 productos), agregar varios, quitar desde el carrito, carrito vacío |
| `test_checkout.py` | Compra completa (2 clientes del JSON), datos incompletos (3 casos del JSON), subtotal y total del resumen, cancelar checkout |

**API (JSONPlaceholder) – 15 tests**

| Archivo | Tests |
|---|---|
| `test_posts_api.py` | GET de todos los posts, GET por id (1, 50, 100), GET de ids inexistentes (404), filtro por usuario, POST (3 casos del JSON) y DELETE |
| `test_flujos_encadenados.py` | Post → usuario → comentarios; POST y luego GET del id creado (404, porque la API no guarda) |

## Datos de prueba

Cada caso de `data/` tiene un campo `caso` que se usa como nombre del test en el reporte, por ejemplo `test_login_con_datos_invalidos[usuario_vacio]`. Agregar una fila al CSV o un caso al JSON crea un test nuevo sin tocar el código.

## GitHub Actions

`.github/workflows/tests.yml` ejecuta `pytest --headless` en cada push o pull request a `main` y guarda la carpeta `reports/` como artefacto de la ejecución.

## Limitaciones

- SauceDemo no tiene buscador, por eso el filtrado del catálogo se prueba con el selector de orden.
- JSONPlaceholder simula las escrituras: el POST devuelve 201 con id 101 y el DELETE devuelve 200, pero no se guarda ni se borra nada. Esos tests validan la respuesta y no el estado posterior.
- Las pruebas dependen de sitios públicos: si están caídos o lentos, los tests pueden fallar por eso.

## Problemas frecuentes

| Síntoma | Qué probar |
|---|---|
| `ModuleNotFoundError: selenium` o `pytest_html` | Activar el entorno virtual y repetir `pip install -r requirements.txt` |
| Chrome no abre o falla el driver | Actualizar Chrome; la primera vez Selenium necesita internet para descargar el driver |
| Los tests de API devuelven 403 | Probar desde otra conexión; JSONPlaceholder a veces bloquea ciertas redes |
