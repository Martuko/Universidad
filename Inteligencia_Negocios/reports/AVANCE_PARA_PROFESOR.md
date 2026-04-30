# Avance proyecto BI Redatam

## 1. Decisión del estudio

Países seleccionados:

- Chile
- Brasil
- Argentina
- Perú

Temas seleccionados:

- Escolaridad
- Vivienda

Justificación:

Se eligieron estos temas porque están presentes en los cuatro países, permiten análisis comparativo, se pueden cruzar con sexo, edad y ubicación geográfica, y tienen valor social para identificar brechas educativas y condiciones materiales de vida.

## 2. Fuente de datos

La fuente utilizada corresponde a microdatos censales disponibles en Redatam.

Datasets principales:

| País | Dataset | Año | Entidad persona | Entidad hogar | Entidad vivienda | Geografía recomendada |
|---|---|---:|---|---|---|---|
| Chile | CP2017CHL | 2017 | PERSONA | HOGAR | VIVIENDA | COMUNA |
| Brasil | CP2010BRA | 2010 | PESSOA | FAMILIA | DOMICIL | MUNIC |
| Argentina | CP2010ARG | 2010 | PERSONA | HOGAR | VIVIENDA | DPTO |
| Perú | CP2017PER | 2017 | PERSONA | HOGAR | VIVIENDA | DISTRITO |

Se logró abrir los diccionarios `.dicx` con `redatamx` y extraer variables reales de cada país.

## 3. Dataset normalizado propuesto

El dataset final para Power BI no será el microdato crudo. Será una tabla agregada y normalizada.

Campos propuestos:

| Campo | Descripción |
|---|---|
| country_id | Código del país |
| country_name | Nombre del país |
| census_year | Año censal |
| geo_id | Código territorial |
| geo_name | Nombre territorial |
| geo_level | Nivel territorial comparable |
| sexo_homologado | Sexo normalizado |
| edad_tramo | Edad agrupada |
| tamano_poblacion_segmento | Segmento de tamaño poblacional |
| tema | Escolaridad o vivienda |
| indicador | Indicador calculado |
| category | Categoría del indicador |
| numerator | Casos que cumplen condición |
| denominator | Base del indicador |
| pct | Porcentaje |
| weight_used | Si se usó ponderador |
| source_variable | Variable original Redatam |
| quality_flag | Estado metodológico |

## 4. Dimensiones mínimas

### Sexo

Se normalizará como:

- hombre
- mujer
- no_informado

### Edad

Se agrupará en:

- 0_14
- 15_24
- 25_44
- 45_64
- 65_mas
- no_informado

### Ubicación geográfica

Nivel propuesto:

| País | Nivel territorial |
|---|---|
| Chile | Comuna |
| Brasil | Municipio |
| Argentina | Departamento / Partido |
| Perú | Distrito |

### Tamaño poblacional

Se construirá por agregación territorial:

- muy_pequeno: menos de 10.000 habitantes
- pequeno: 10.000 a 49.999
- mediano: 50.000 a 199.999
- grande: 200.000 a 999.999
- metropolitano: 1.000.000 o más

## 5. Temas e indicadores propuestos

### Escolaridad

Unidad base: persona.

Indicadores propuestos:

- % población 25+ con secundaria/media completa o más
- % población 25+ con educación superior completa o más
- % población 15+ con baja escolaridad

### Vivienda

Unidad base: hogar/vivienda.

Indicadores propuestos:

- % hogares/viviendas con agua adecuada
- % hogares/viviendas con saneamiento adecuado
- % hogares con hacinamiento

## 6. Estado actual

Ya se realizó:

- Descarga y organización de datasets Redatam.
- Inventario técnico de archivos.
- Instalación y prueba de `redatamx`.
- Apertura de diccionarios `.dicx`.
- Extracción de entidades reales.
- Extracción de variables reales.
- Creación de Excel de avance:
  - `reports/avances_dataset_normalizado_redatam.xlsx`

## 7. Pendientes

- Revisar códigos/categorías de las variables seleccionadas.
- Confirmar variables finales por país.
- Crear tabla agregada final para Power BI.
- Definir medidas DAX.
- Preparar GeoDa solo para Chile.
- Construir dashboard final.
