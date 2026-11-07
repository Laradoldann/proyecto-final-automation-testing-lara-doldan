# Checklist de la consigna

Dónde se cumple cada punto del proyecto final.

## Pruebas de UI (Selenium WebDriver)

| Requisito | Dónde se cumple |
|---|---|
| Al menos 5 casos de prueba en un sitio demo | 27 tests sobre SauceDemo en `tests/ui/` (15 funciones de test, varias parametrizadas) |
| Flujos completos: login, navegación, carrito, checkout | `test_login.py`, `test_inventory.py` (ordenar y detalle), `test_cart.py`, `test_checkout.py::test_compra_completa` |
| Al menos un escenario negativo | `test_login_con_datos_invalidos` (5 casos), `test_acceso_directo_al_catalogo_sin_iniciar_sesion`, `test_checkout_con_datos_incompletos` (3 casos) |
| Parametrización con datos de prueba | `@pytest.mark.parametrize` en login, checkout, orden y carrito |
| Fuentes externas CSV/JSON | `data/login.csv`, `data/checkout.json`, leídos con `utils/data_reader.py` |
| Page Object Model: una clase por página | `pages/` (login, inventario, detalle, carrito y las 3 pantallas del checkout) |
| Métodos que representan acciones de cada página | Por ejemplo `iniciar_sesion()`, `agregar_producto()`, `completar_formulario()` |
| Lógica de tests separada de la interacción con la página | Los tests no contienen selectores ni llamadas directas a Selenium (salvo `driver.get` y `driver.current_url` en validaciones de navegación) |
| Captura automática al fallar | Hook `pytest_runtest_makereport` en `conftest.py` (fases `setup` y `call`) |
| Nombre con fecha/hora y nombre del test | `utils/screenshots.py::armar_nombre_captura` |

## Pruebas de API (Requests)

| Requisito | Dónde se cumple |
|---|---|
| Al menos 3 casos en una API pública | 15 tests sobre JSONPlaceholder en `tests/api/` |
| GET, POST y DELETE | `test_obtener_un_post_existente`, `test_crear_un_post`, `test_eliminar_un_post` |
| Códigos de estado | 200, 201 y 404 verificados en cada test |
| Estructura y contenido del JSON | `validar_estructura_de_post()` (campos y tipos) y comparación de valores |
| Escenarios de éxito y de error | `test_obtener_un_post_inexistente_devuelve_404`, filtro por usuario inexistente |
| Encadenamiento de peticiones (opcional) | `tests/api/test_flujos_encadenados.py` |

## Reportes y logging

| Requisito | Dónde se cumple |
|---|---|
| Reporte HTML con pytest | `pytest.ini` (`--html=reports/reporte.html --self-contained-html`) |
| Tests, estado y duración | Tabla de resultados de pytest-html |
| Capturas de pantalla en el reporte | `pytest_html.extras.image(...)` en `conftest.py` |
| Logging de pasos clave | `reports/ejecucion.log` (configurado en `pytest.ini`) con el registro de los Page Objects, el cliente de API y los hooks |

## Control de versiones y documentación

| Requisito | Dónde se cumple |
|---|---|
| Proyecto preparado para Git | Repositorio con `.gitignore` |
| Commits que documentan el progreso y ramas por funcionalidad | `git log --graph --oneline` |
| Nombre del repositorio | `proyecto-final-automation-testing-lara-doldan` |
| GitHub Actions (opcional) | `.github/workflows/tests.yml` |
| README con propósito, tecnologías, estructura, instalación, ejecución e interpretación de reportes | `README.md` |

## Criterios de calidad

| Criterio | Dónde se cumple |
|---|---|
| Tests independientes | Un navegador nuevo por test (`driver`) y un cliente de API nuevo por test (`cliente_api`) |
| Fácil de ampliar | Sección "Cómo agregar una prueba nueva" del README |
| Esperas explícitas | `BasePage` (`WebDriverWait`); no hay `sleep` ni esperas implícitas |
| Configuración centralizada | `config/settings.py` |
