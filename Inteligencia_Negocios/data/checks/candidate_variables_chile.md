# Variables candidatas - Chile (CP2017CHL)

## Escolaridad

| término detectado | posible variable o evidencia | archivo fuente | tipo de evidencia | confianza | comentario |
|---|---|---|---|---|---|
| Educación | Inferido desde estructura censo | CPV2017-16.dic | inferido desde nombre | baja | No se inspeccionó diccionario |

## Vivienda

| término detectado | posible variable o evidencia | archivo fuente | tipo de evidencia | confianza | comentario |
|---|---|---|---|---|---|
| Tipo de vivienda | Inferido desde glosarios | Glosas_*.txt | inferido desde nombres | media | Glosas_COMUNA, PROVINCIA, etc. |
| Materiales | Inferido desde LKP2 | CPV2017-16_LKP2*.rbf | inferido desde nombre | media | Look-up 2 características vivienda |
| Servicios básicos | Inferido desde LKP3 | CPV2017-16_LKP3*.rbf | inferido desde nombre | media | Look-up 3 ubicación vivienda |
| Características físicas | Inferido desde LKP2 | CPV2017-16_LKP2*.rbf | inferido desde nombre | media | Look-up 2 |

## Sexo

| término detectado | posible variable o evidencia | archivo fuente | tipo de evidencia | confianza | comentario |
|---|---|---|---|---|---|
| Sexo | Inferido desde estructura poblacional | CPV2017-16.rbf | inferido desde nombre | baja | Estructura estándar censo |

## Edad

| término detectado | posible variable o evidencia | archivo fuente | tipo de evidencia | confianza | comentario |
|---|---|---|---|---|---|
| Edad | Inferido desde rango 0-100+ | CPV2017-16.rbf | inferido desde nombre | baja | Estructura censo estándar |

## Geografía

| término detectado | posible variable o evidencia | archivo fuente | tipo de evidencia | confianza | comentario |
|---|---|---|---|---|---|
| Región | Inferido desde CPV2017-16_REGION | CPV2017-16_REGION*.rbf | inferido desde nombre | media | 16 regiones de Chile |
| Comuna | Inferido desde glosarios | Glosas_COMUNA*.txt | inferido desde nombre | media | 150+ comunas |
| Distrito | Inferido desde glosarios | Glosas_DISTRITO*.txt | inferido desde nombre | media | Distritos comunales |
| Localidad | Inferido desde glosarios | Glosas_LOCALIDAD*.txt | inferido desde nombre | media | Barrios/localidades |
| Provincia | Inferido desde glosarios | Glosas_PROVINCIA*.txt | inferido desde nombre | media | Provinciones de cada región |

## Ponderadores

| término detectado | posible variable o evidencia | archivo fuente | tipo de evidencia | confianza | comentario |
|---|---|---|---|---|---|
| Ponderador diseño | No confirmado | - | no encontrado | bajo | No se inspeccionó diccionario |
| Ponderador supresión | No confirmado | - | no encontrado | bajo | No se inspeccionó diccionario |

## Entidades persona/hogar/vivienda

| término detectado | posible variable o evidencia | archivo fuente | tipo de evidencia | confianza | comentario |
|---|---|---|---|---|---|
| Persona | Inferido desde estructura poblacional | CPV2017-16.rbf | inferido desde nombre | media | Entidad principal censo |
| Hogar | Inferido desde estructura vivienda | CPV2017-16.rbf | inferido desde nombre | media | Entidad vivienda-persona |
| Vivienda | Inferido desde estructura vivienda | CPV2017-16.rbf | inferido desde nombre | media | Entidad física vivienda |

## Qué sigue siendo No lo sé

- Nombres reales de variables (sin inspección de `CPV2017-16.dic`)
- Ponderadores exactos
- Variables de muestra vs universo
- Variables confirmadas entre países

---

**Fecha**: 2026-04-29  
**Confianza promedio**: media (inferido desde nombres sin inspección de diccionarios)
