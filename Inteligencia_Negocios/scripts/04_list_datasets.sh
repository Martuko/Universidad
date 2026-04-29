#!/bin/bash
# Listar todos los datasets extraídos por país

DATA_DIR="data/extracted"
OUTPUT_DIR="data/checks"

# Países con sus códigos de directorio
declare -A COUNTRIES=(
    ["Chile"]="CP2017CHL"
    ["Argentina"]="CP2010ARG"
    ["Brasil"]="CP2010BRA|Cp1991BRA|Cp2000BRA"
    ["Peru"]="CP2017PER|CP2007PER"
)

echo "# Listado de datasets por país" > "$OUTPUT_DIR/list_datasets_by_country.txt"
echo "" >> "$OUTPUT_DIR/list_datasets_by_country.txt"

for country in "${!COUNTRIES[@]}"; do
    patterns="${COUNTRIES[$country]}"
    echo "## $country" >> "$OUTPUT_DIR/list_datasets_by_country.txt"
    echo "" >> "$OUTPUT_DIR/list_datasets_by_country.txt"

    # Obtener directorios que coinciden con el país
    if [[ "$patterns" == *"|"* ]]; then
        # Múltiples patrones
        patterns_list=$(echo "$patterns" | tr '|' '\n')
    else
        patterns_list="$patterns"
    fi

    for pattern in $patterns_list; do
        dir_path="$DATA_DIR/$pattern"
        if [[ -d "$dir_path" ]]; then
            # Tamaño
            size=$(du -sh "$dir_path" | cut -f1)
            echo "Dir: $dir_path" >> "$OUTPUT_DIR/list_datasets_by_country.txt"
            echo "Tamaño: $size" >> "$OUTPUT_DIR/list_datasets_by_country.txt"
            echo "" >> "$OUTPUT_DIR/list_datasets_by_country.txt"

            # Listar subdirectorios principales
            echo "Subdirectorios:" >> "$OUTPUT_DIR/list_datasets_by_country.txt"
            ls -1 "$dir_path" 2>/dev/null | while read -r subdir; do
                echo "  - $subdir" >> "$OUTPUT_DIR/list_datasets_by_country.txt"
            done
            echo "" >> "$OUTPUT_DIR/list_datasets_by_country.txt"
        fi
    done
done

echo "" >> "$OUTPUT_DIR/list_datasets_by_country.txt"
echo "---" >> "$OUTPUT_DIR/list_datasets_by_country.txt"
echo "" >> "$OUTPUT_DIR/list_datasets_by_country.txt"

# Mostrar diccionarios disponibles por país
echo "# Diccionarios por país" > "$OUTPUT_DIR/list_dictionaries.txt"
echo "" >> "$OUTPUT_DIR/list_dictionaries.txt"

for country in "${!COUNTRIES[@]}"; do
    patterns="${COUNTRIES[$country]}"
    echo "## $country" >> "$OUTPUT_DIR/list_dictionaries.txt"
    echo "" >> "$OUTPUT_DIR/list_dictionaries.txt"

    if [[ "$patterns" == *"|"* ]]; then
        patterns_list=$(echo "$patterns" | tr '|' '\n')
    else
        patterns_list="$patterns"
    fi

    for pattern in $patterns_list; do
        dir_path="$DATA_DIR/$pattern"
        if [[ -d "$dir_path" ]]; then
            # Buscar archivos .dic
            echo "$dir_path/**/*.dic" 2>/dev/null | xargs -I {} ls -la "{}" 2>/dev/null >> "$OUTPUT_DIR/list_dictionaries.txt" || true
            echo "" >> "$OUTPUT_DIR/list_dictionaries.txt"
        fi
    done
done

echo "Perfiles generados en $OUTPUT_DIR/"
