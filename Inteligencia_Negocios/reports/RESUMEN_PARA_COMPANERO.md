# Resumen para continuar proyecto BI Redatam

## Estado actual

Ya se hizo el reconocimiento técnico inicial de los datos Redatam y se logró abrir los diccionarios con `redatamx`.

## Países definidos

- Chile: CP2017CHL
- Brasil: CP2010BRA
- Argentina: CP2010ARG
- Perú: CP2017PER

## Temas recomendados preliminares

- Escolaridad
- Vivienda

Todavía debemos confirmarlo como equipo, pero son los temas más viables porque aparecen variables reales en los 4 países.

## Tamaño e inventario de datos

Se inventariaron 7 datasets:

- Chile 2017: 763 MB
- Argentina 2010: 1.5 GB
- Perú 2017: 1.8 GB
- Brasil 2010: 4.8 GB
- Además quedaron inventariados datasets no prioritarios de Brasil 1991, Brasil 2000 y Perú 2007.

Total aproximado extraído: 14.9 GB  
Archivos inventariados: 1.438  
Archivos `.rbf`: 1.104  
Diccionarios detectados: 108  

## Herramientas probadas

- R instalado
- `redatamx` instalado correctamente
- RedEngine funcionando en Linux
- DuckDB instalado
- Se logró abrir diccionarios `.dicx` de los 4 países

## Entidades reales encontradas

### Argentina

- PROV
- DPTO
- FRAC
- RADIO
- SEG
- VIVIENDA
- HOGAR
- PERSONA

### Chile

- REGION
- PROVINCI
- COMUNA
- DISTRITO
- AREA
- ZONALOC
- VIVIENDA
- HOGAR
- PERSONA

### Perú

- DEPARTAM
- PROVINCI
- DISTRITO
- VIVIENDA
- HOGAR
- PERSONA

### Brasil

- REGIAO
- UF
- MUNIC
- APOND
- DOMICIL
- FAMILIA
- PESSOA

## Cantidad de variables por entidad

### Argentina

- PERSONA: 71
- HOGAR: 47
- VIVIENDA: 35

### Brasil

- PESSOA: 142
- DOMICIL: 41
- FAMILIA: 4

### Chile

- PERSONA: 33
- VIVIENDA: 10
- HOGAR: 2

### Perú

- PERSONA: 71
- HOGAR: 31
- VIVIENDA: 19

## Variables y temas detectados

Ya existen hits reales para:

- Escolaridad
- Vivienda
- Sexo
- Edad
- Geografía
- Ponderadores en algunos países

Importante: todavía falta revisar categorías/códigos antes de crear indicadores finales.

## Archivos más importantes para revisar

### Reportes generales

- `reports/dataset_reconocimiento_inicial.md`
- `reports/handoff_reconocimiento.md`
- `reports/phase2/redatam_variables_extraccion.md`

### Variables reales extraídas

- `data/checks/redatamx/redatam_entities_all.csv`
- `data/checks/redatamx/redatam_variables_all.csv`
- `data/checks/redatamx/redatam_variables_theme_hits.csv`
- `data/checks/redatamx/summary_variables_by_entity.csv`
- `data/checks/redatamx/summary_hits_by_country_theme.csv`

### Variables separadas por país

- `data/checks/redatamx/by_country/chile_hits.csv`
- `data/checks/redatamx/by_country/brasil_hits.csv`
- `data/checks/redatamx/by_country/argentina_hits.csv`
- `data/checks/redatamx/by_country/peru_hits.csv`

## Decisión pendiente con el equipo

Debemos decidir definitivamente los 2 temas.

Recomendación principal:

1. Escolaridad
2. Vivienda

Motivo:

- Son temas presentes en los 4 países.
- Permiten análisis por sexo, edad y territorio.
- Sirven bien para Power BI.
- Vivienda y escolaridad permiten buen análisis espacial para Chile en GeoDa.
- Son fáciles de explicar en storytelling final.

## Lo que falta hacer

1. Revisar variables candidatas de escolaridad.
2. Revisar variables candidatas de vivienda.
3. Revisar categorías/códigos de esas variables.
4. Elegir variables equivalentes entre países.
5. Probar una consulta agregada simple en Chile.
6. Repetir para Brasil, Argentina y Perú.
7. Exportar tablas agregadas para Power BI.
8. Preparar análisis GeoDa solo para Chile.

## Advertencias

- No subir ZIP ni carpetas extraídas al repositorio.
- No usar pandas para abrir `.rbf`.
- No asumir que todos los países son perfectamente comparables.
- No comparar conteos absolutos sin revisar ponderadores.
- Trabajar con porcentajes y tasas.
- Las variables deben salir de `redatam_variables_all.csv`, no de intuición.

