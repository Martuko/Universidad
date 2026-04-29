#!/usr/bin/env python3
"""
Script para construir inventario maestro de archivos Redatam.
No carga todo en memoria - procesa por lotes.
"""
import os
import csv
import re
from pathlib import Path

# Configuración
DATA_DIR = Path("data/extracted")
OUTPUT_CSV = Path("data/checks/master_file_inventory.csv")

# Mapeo de prefijos a país (inferencia desde nombres de archivos/carpetas)
PATTERN_COUNTRY = {
    r"CP2017CHL": "Chile",
    r"CP2010ARG": "Argentina",
    r"CP2010BRA": "Brasil",
    r"CP2017PER": "Peru",
    r"CP2007PER": "Peru",
    r"Cp1991BRA": "Brasil",
    r"Cp2000BRA": "Brasil",
}

# Mapeo de extensiones a roles probables
EXTENSION_ROLES = {
    "rbf": "redatam_data",
    "bin": "redatam_binary",
    "ptr": "redatam_pointer",
    "dic": "redatam_dictionary",
    "dicx": "redatam_dictionary",
    "~dicx": "redatam_dictionary",
    "spc": "metadata",
    "pdf": "documentation",
    "doc": "documentation",
    "docx": "documentation",
    "txt": "metadata",
    "xls": "excel",
    "xlsx": "excel",
    "prjx": "project_file",
    "wxp": "project_file",
    "wpm": "project_file",
    "mpg": "media",
    "mp4": "media",
    "avi": "media",
    "mdb": "possible_database",
    "ldb": "possible_database",
}

# Diccionario de patrones nombre -> país
NAME_PATTERN_COUNTRY = {
    r"CP2017CHL": "Chile",
    r"CP2010ARG": "Argentina",
    r"CP2010BRA": "Brasil",
    r"CP2017PER": "Peru",
    r"CP2007PER": "Peru",
    r"Cp1991BRA": "Brasil",
    r"Cp2000BRA": "Brasil",
}


def infer_country_from_path(path):
    """Inferir país desde el path usando regex."""
    path_str = str(path)
    # Buscar coincidiendo patrones en el path completo
    for pattern, country in NAME_PATTERN_COUNTRY.items():
        if re.search(pattern, path_str):
            return country
    # Intentar inferir desde los componentes del path
    for p in path.parts:
        # Buscar prefijos que indican país
        if p.startswith("CP2017") and p.endswith("CHL"):
            return "Chile"
        if p.startswith("CP2010") and p.endswith("ARG"):
            return "Argentina"
        if p.startswith("CP2010BRA"):
            return "Brasil"
        if p.startswith("CP2017PER"):
            return "Peru"
        if p.startswith("CP2007PER"):
            return "Peru"
        if p.startswith("Cp1991BRA"):
            return "Brasil"
        if p.startswith("Cp2000BRA"):
            return "Brasil"
    return "unknown"


def get_extension_lower(path):
    """Obtener extensión en minúsculas."""
    stem = path.stem
    suffix = path.suffix.lower()
    # Caso especial: .RB con posible .F
    if suffix == ".RB":
        return ".rbf"
    # Caso especial: .MPG mal detectado como .MP
    if suffix == ".MP":
        return ".mp"
    return suffix if suffix else ""


def classify_file(path):
    """Clasificar rol probable de un archivo."""
    ext = get_extension_lower(path)
    stem = path.stem.upper()
    name = path.name.upper()

    if ext == ".MPG" or ext == ".MP4" or ext == ".AVI":
        return "media", ""
    if ext == ".ZIP":
        return "zip", ""
    if ext in [".DIC", ".DICX", "~DICX"]:
        return "redatam_dictionary", ""
    if ext == ".PTR":
        return "redatam_pointer", ""
    if ext == ".BIN":
        return "redatam_binary", ""
    if ext == ".RBF":
        # Verificar si es diccionario por nombre
        if "DICT" in name or "DIC" in stem:
            return "redatam_dictionary", "Posible diccionario por nombre de archivo"
        if len(stem) == 7 and stem.startswith("CD"):
            return "redatam_dictionary", "Código de diccionario Redatam (CDxxxxx)"
        if stem.startswith("CPV"):
            return "redatam_data", "Archivo de vivienda/persona (CPV)"
        if stem.startswith("PESSOA"):
            return "redatam_data", "Datos de persona (PESSOA)"
        if len(stem) == 7 and stem.startswith("C"):
            # CD + 5 dígitos = diccionario
            return "redatam_dictionary", "Código de diccionario Redatam"
        return "redatam_data", ""
    if ext in [".XLS", ".XLSX", ".XLSM"]:
        return "excel", ""
    if ext in [".PDF", ".DOC", ".DOCX", ".TXT", ".RTF"]:
        return "documentation", ""
    if ext in [".PRJX", ".WX", ".WPM"]:
        return "project_file", ""

    # Heurística adicional por nombre
    if stem.startswith("CD") and len(stem) == 7:  # CD + 5 dígitos
        return "redatam_dictionary", "Código de diccionario Redatam"

    if stem.startswith("BASE") or stem.startswith("CDATA"):
        return "redatam_data", ""

    return "unknown", f"Ext: {ext}, Name: {name}"


def main():
    print(f"Scanning: {DATA_DIR}")
    print(f"Expected countries: {list(NAME_PATTERN_COUNTRY.values())}")

    total_files = 0
    total_size = 0
    country_counts = {}

    rows = []

    for root, dirs, files in os.walk(DATA_DIR):
        for filename in files:
            path = Path(root) / filename
            size_bytes = path.stat().st_size

            country = infer_country_from_path(path)
            country_counts[country] = country_counts.get(country, 0) + 1
            ext = get_extension_lower(path)
            role, notes = classify_file(path)

            size_mb = round(size_bytes / (1024 * 1024), 2)
            readable = "no"
            if role in ["documentation", "metadata"]:
                readable = "quizas"
            elif role == "redatam_binary":
                readable = "no"
            elif ext in [".CSV", ".TXT"]:
                readable = "quizas"

            rows.append({
                "country_guess": country,
                "dataset_folder": root.split("/")[-1],
                "path": str(path),
                "file_name": filename,
                "extension": ext,
                "size_bytes": size_bytes,
                "size_mb": size_mb,
                "likely_role": role,
                "readable_by_duckdb": readable,
                "notes": notes
            })

            total_files += 1
            total_size += size_bytes

    # Ordenar por tamaño descendente
    rows.sort(key=lambda x: x["size_bytes"], reverse=True)

    # Imprimir resumen por país
    print("\n=== Counts by Country ===")
    for country in ["Chile", "Argentina", "Brasil", "Peru", "unknown"]:
        count = country_counts.get(country, 0)
        print(f"  {country}: {count}")

    # Escribir CSV
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "country_guess",
        "dataset_folder",
        "path",
        "file_name",
        "extension",
        "size_bytes",
        "size_mb",
        "likely_role",
        "readable_by_duckdb",
        "notes"
    ]

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nInventario escrito: {OUTPUT_CSV}")
    print(f"Total archivos: {total_files}")
    print(f"Tamaño total: {total_size / (1024**3):.2f} GB")


if __name__ == "__main__":
    main()
