# Resumen de variables reales Redatam

## Estado

Se logró extraer entidades y variables reales desde diccionarios `.dicx` usando `redatamx`.

## Archivos base

- `data/checks/redatamx/redatam_entities_all.csv`
- `data/checks/redatamx/redatam_variables_all.csv`
- `data/checks/redatamx/redatam_variables_theme_hits.csv`
- `data/checks/redatamx/summary_variables_by_entity.csv`
- `data/checks/redatamx/summary_hits_by_country_theme.csv`

## Países confirmados

- Argentina: `CPV2010Ampliado.dicx`
- Chile: `CPV2017-16.dicx`
- Perú: `CPVPER2017D.dicX`
- Brasil: `CD2010_Amostra.dicx`

## Próximo objetivo

Seleccionar variables comparables para:

1. Escolaridad
2. Vivienda
3. Sexo
4. Edad
5. Geografía
6. Ponderadores

## Regla metodológica

Solo se considerarán variables como confirmadas si aparecen en `redatam_variables_all.csv`.

Las variables detectadas solo por inferencia de nombre de archivo quedan descartadas como evidencia principal.
