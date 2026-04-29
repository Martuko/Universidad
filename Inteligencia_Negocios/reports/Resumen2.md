# Resumen para decidir temas del proyecto BI Redatam

## Objetivo

Este documento resume el estado actual del proyecto para decidir, como equipo, qué 2 temas usar en el trabajo de Inteligencia de Negocios.

El encargo permite elegir 2 temas entre:

1. Escolaridad
2. Vivienda
3. Origen étnico
4. Actividad económica
5. Hijos / grupo familiar

## Países definidos

Se trabajará con 4 países:

- Chile
- Brasil
- Argentina
- Perú

## Datasets principales recomendados

Para comparación entre países se recomienda usar un solo censo por país:

- Chile: CP2017CHL
- Brasil: CP2010BRA
- Argentina: CP2010ARG
- Perú: CP2017PER

## Por qué no usar todos los años de Brasil y Perú

También existen:

- Brasil 1991
- Brasil 2000
- Perú 2007

Pero no se usan en el análisis principal porque el trabajo pide comparación entre países, no evolución histórica por país.

Usar varios años para Brasil y Perú agregaría complejidad temporal y haría más difícil comparar de forma limpia con Chile y Argentina.


## Archivos principales

### Variables completas

- data/checks/redatamx/redatam_variables_all.csv

Este archivo contiene todas las variables reales extraídas desde los diccionarios .dicx.

### Entidades

- data/checks/redatamx/redatam_entities_all.csv

Contiene las entidades disponibles por país.

### Catálogo general por temas

- data/checks/redatamx/catalogo_temas_trabajo.csv
- data/checks/redatamx/catalogo_temas_relevantes.csv
- data/checks/redatamx/resumen_catalogo_temas_trabajo.csv

Estos archivos sirven para decidir qué temas son más viables.

## Entidades principales por país

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

### Brasil

- REGIAO
- UF
- MUNIC
- APOND
- DOMICIL
- FAMILIA
- PESSOA

### Argentina

- PROV
- DPTO
- FRAC
- RADIO
- SEG
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

## Evaluación preliminar de temas

### Escolaridad

Ventajas:
- Aparece en los 4 países.
- Se cruza bien con sexo, edad y territorio.
- Es fácil de explicar en Power BI.
- Tiene valor social claro.

Riesgos:
- Hay que revisar categorías/códigos para homologar niveles educativos.

### Vivienda

Ventajas:
- Aparece en los 4 países.
- Tiene muchas variables en Argentina, Brasil y Perú.
- Sirve muy bien para análisis territorial.
- Es fuerte para GeoDa en Chile.

Riesgos:
- Las variables de vivienda no siempre son idénticas entre países.
- Hay que decidir si se usará agua, saneamiento, hacinamiento, materialidad o índice compuesto.

### Origen étnico

Ventajas:
- Tema social potente.
- Puede generar hallazgos relevantes.

Riesgos:
- Las categorías étnicas pueden variar mucho entre países.
- Comparabilidad más difícil.

### Actividad económica

Ventajas:
- Permite análisis por edad, sexo y territorio.
- Puede conectar con implicancias económicas.

Riesgos:
- Puede tener muchas categorías complejas.
- Puede exigir más limpieza y homologación.

### Hijos / grupo familiar

Ventajas:
- Puede cruzarse con edad, sexo y hogar.
- Tiene potencial demográfico.

Riesgos:
- Puede complicar el modelo persona-hogar.
- Puede ser menos directo para Power BI si no se homogeniza bien.

## Recomendación preliminar

La opción más viable sigue siendo:

1. Escolaridad
2. Vivienda

Motivo:
- Son los temas más defendibles para un dashboard BI.
- Aparecen en los 4 países.
- Permiten cruces con sexo, edad y geografía.
- Son fáciles de explicar en storytelling.
- Permiten un buen análisis espacial con GeoDa para Chile.

## Decisión pendiente

Antes de cerrar los temas, revisar:

- data/checks/redatamx/resumen_catalogo_temas_trabajo.csv
- data/checks/redatamx/catalogo_temas_relevantes.csv
- data/checks/redatamx/redatam_variables_all.csv

