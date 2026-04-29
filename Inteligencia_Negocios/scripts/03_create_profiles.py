#!/usr/bin/env python3
"""
Generador de perfiles de datasets por país.
Procesa todos los datasets extraídos y crea archivos .md con perfiles.
"""
import os
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path("data/extracted")
PROFILES_DIR = Path("data/checks")

# Países a procesar
COUNTRIES = ["Chile", "Argentina", "Brasil", "Peru"]


def get_dataset_name_from_path(path):
    """Extraer nombre del dataset desde el path."""
    parts = path.parts
    for p in parts:
        # Buscar prefijos conocidos
        if p.startswith("CP2017") and p.endswith("CHL"):
            return p.replace("CHL", "CHL")
        if p.startswith("CP2010") and p.endswith("ARG"):
            return p.replace("ARG", "ARG")
        if p.startswith("CP2010BRA") or p.startswith("Cp1991BRA") or p.startswith("Cp2000BRA"):
            return p.replace("BRA", "BRA")
        if p.startswith("CP2017PER") or p.startswith("CP2007PER"):
            return p.replace("PER", "PER")
    # Intentar obtener desde primera subcarpeta
    try:
        return parts[parts.index("data") + 2]
    except:
        return path.name


def get_extension_lower(path):
    """Obtener extensión en minúsculas."""
    stem = path.stem
    suffix = path.suffix.lower()
    if suffix == ".RB":
        return ".rbf"
    if suffix == ".MP":
        return ".mp"
    return suffix if suffix else ""


def count_extensions_by_file(path):
    """Contar extensiones en directorio."""
    ext_counts = defaultdict(int)
    for f in path.rglob("*"):
        ext = get_extension_lower(f)
        if ext:
            ext_counts[ext] += 1
    return ext_counts


def count_files_by_name_prefix(path):
    """Contar archivos por prefijo de nombre."""
    prefix_counts = defaultdict(int)
    for f in path.rglob("*"):
        name = f.name.upper()
        # Extraer prefijo
        if name.startswith("CD") and len(name) == 7:
            prefix_counts[name] += 1
        elif name.startswith("CPV"):
            # CPV + código país + año
            prefix = name.split("-")[0] if "-" in name else name[:15]
            prefix_counts[name[:15]] += 1
    return prefix_counts


def generate_country_profile(country_name):
    """Generar perfil para un país."""
    profile = {
        "country": country_name,
        "size_mb": 0,
        "total_files": 0,
        "extensions": {},
        "main_tables": [],
        "variables_detected": [],
    }

    # Buscar dataset para este país
    for root, dirs, files in os.walk(DATA_DIR):
        for d in dirs:
            # Normalizar nombre
            d_norm = d.replace("_", "").replace(".", "")
            if country_name in d.upper():
                dataset_path = Path(root) / d
                break
        else:
            continue
        break
    else:
        return None

    # Obtener tamaño
    total_size = sum(f.stat().st_size for f in dataset_path.rglob("*") if f.is_file())
    profile["size_mb"] = round(total_size / (1024 * 1024), 2)
    profile["total_files"] = len(list(dataset_path.rglob("*")))

    # Contar extensiones
    profile["extensions"] = dict(count_extensions_by_file(dataset_path))

    # Buscar archivos principales (rbf grandes)
    large_files = [(f.name, f.stat().st_size) for f in dataset_path.rglob("*.rbf")
                   if f.stat().st_size > 50 * 1024 * 1024]  # > 50MB
    profile["main_tables"] = large_files[:10]  # Top 10

    # Buscar diccionarios
    dicts = list(dataset_path.rglob("*.dic"))
    if dicts:
        profile["variables_detected"] = [str(d) for d in dicts[:5]]

    return profile


def main():
    print(f"Generando perfiles para: {', '.join(COUNTRIES)}")

    for country in COUNTRIES:
        print(f"\n--- {country} ---")
        profile = generate_country_profile(country)
        if profile:
            print(f"  Tamaño: {profile['size_mb']} MB")
            print(f"  Archivos: {profile['total_files']}")
            print(f"  Extensiones: {profile['extensions']}")


if __name__ == "__main__":
    main()
