# Handoff para compañero - Avance BI Redatam

## Qué está listo

Ya está creado el Excel de avance:

- `reports/avances_dataset_normalizado_redatam.xlsx`

Este archivo resume:

- países seleccionados;
- datasets usados;
- entidades detectadas;
- variables candidatas de escolaridad;
- variables candidatas de vivienda;
- dimensiones mínimas;
- formato normalizado del dataset final;
- indicadores propuestos;
- pendientes.

## Países

- Chile: CP2017CHL
- Brasil: CP2010BRA
- Argentina: CP2010ARG
- Perú: CP2017PER

## Temas

- Escolaridad
- Vivienda

## Archivos importantes

### Excel principal

- `reports/avances_dataset_normalizado_redatam.xlsx`

### Reportes

- `reports/AVANCE_PARA_PROFESOR.md`
- `reports/TEXTO_CORTO_PRESENTACION_AVANCE.md`

### Variables reales extraídas

- `data/checks/redatamx/redatam_variables_all.csv`
- `data/checks/redatamx/redatam_entities_all.csv`

### Variables candidatas

- `data/checks/redatamx/selection/escolaridad_candidatas.csv`
- `data/checks/redatamx/selection/vivienda_candidatas.csv`
- `data/checks/redatamx/selection/dimensiones_candidatas.csv`

## Qué falta decidir

- Variables finales de escolaridad por país.
- Variables finales de vivienda por país.
- Códigos/categorías para homologar.
- Indicadores finales.
- Si usaremos ponderadores por país.

## Siguiente paso

Revisar categorías/códigos de las variables seleccionadas y generar una primera tabla agregada para Chile como prueba.
