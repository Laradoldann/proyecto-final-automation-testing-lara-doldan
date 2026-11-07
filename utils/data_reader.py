"""Lectura de los datos de prueba de la carpeta data/ (CSV y JSON)."""
import csv
import json

import pytest

from config.settings import CARPETA_DATOS


def _ruta_de_datos(nombre_archivo):
    ruta = CARPETA_DATOS / nombre_archivo
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de datos: {ruta}")
    return ruta


def leer_csv(nombre_archivo):
    """Devuelve el CSV como lista de diccionarios (la primera fila son los nombres de columna)."""
    with open(_ruta_de_datos(nombre_archivo), newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def leer_json(nombre_archivo):
    ruta = _ruta_de_datos(nombre_archivo)
    try:
        with open(ruta, encoding="utf-8") as archivo:
            return json.load(archivo)
    except json.JSONDecodeError as error:
        raise ValueError(f"El archivo {ruta.name} no es un JSON válido: {error}") from error


def como_parametros(casos):
    """Convierte cada caso en un parámetro de pytest que se llama como su campo 'caso'."""
    return [pytest.param(caso, id=caso["caso"]) for caso in casos]
