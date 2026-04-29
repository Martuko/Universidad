# Variables candidatas - Brasil (CP2010BRA)

## Escolaridad

| término detectado | posible variable o evidencia | archivo fuente | tipo de evidencia | confianza | comentario |
|---|---|---|---|---|---|
| Escolaridad | No confirmado | CD2010_xxx.rbf | no inspeccionado | bajo | No se inspeccionó diccionario |

## Vivienda

| término detectado | posible variable o evidencia | archivo fuente | tipo de evidencia | confianza | comentario |
|---|---|---|---|---|---|
| Tipo de vivienda | Inferido desde estructura | PESSOA_*.RBF | inferido desde nombre | baja | Estructura censo Brasil |
| Servicios | Inferido desde diccionarios | CD2010_xxx.rbf | inferido desde nombre | baja | Diccionarios no inspeccionados |
| Materiales de construcción | Inferido desde estructura | CD2010_xxx.rbf | inferido desde nombre | baja | Diccionarios no inspeccionados |

## Sexo

| término detectado | posible variable o evidencia | archivo fuente | tipo de evidencia | confianza | comentario |
|---|---|---|---|---|---|
| Sexo | Inferido desde PESSOA_RENDSM | PESSOA_RENDSM.RBF | inferido desde nombre | baja | PESSOA indica persona |

## Edad

| término detectado | posible variable o evidencia | archivo fuente | tipo de evidencia | confianza | comentario |
|---|---|---|---|---|---|
| Edad | Inferido desde estructura censo | PESSOA_*.RBF | inferido desde nombre | baja | Estructura censo Brasil |

## Geografía

| término detectado | posible variable o evidencia | archivo fuente | tipo de evidencia | confianza | comentario |
|---|---|---|---|---|---|
| Municipio | Inferido desde diccionarios CD2010 | CD2010_xxx.rbf | inferido desde nombre | media | Diccionarios de código |
| Estado (UF) | Inferido desde estructura | CD2010_xxx.rbf | inferido desde nombre | media | Unidades federativas |

## Ponderadores

| término detectado | posible variable o evidencia | archivo fuente | tipo de evidencia | confianza | comentario |
|---|---|---|---|---|---|
| Peso de diseño | Inferido desde estructura | PESSOA_*.RBF | inferido desde nombre | baja | No confirmado |
| Supresión por motivo | Inferido desde estructura | CD2010_xxx.rbf | inferido desde nombre | baja | No confirmado |

## Entidades persona/hogar/vivienda

| término detectado | posible variable o evidencia | archivo fuente | tipo de evidencia | confianza | comentario |
|---|---|---|---|---|---|
| Persona | Confirmado desde nombre | PESSOA_*.RBF | inferido desde nombre | media | PESSOA = Persona |
| Hogar | Inferido desde estructura | PESSOA_RENDTOTTS.RBF | inferido desde nombre | baja | Total hogares |
| Vivienda | Inferido desde estructura | CD2010_xxx.rbf | inferido desde nombre | baja | Diccionarios de código |

## Qué sigue siendo No lo só

- Nombres reales de variables (sin inspección de CD2010_xxx.rbf)
- Ponderadores exactos
- Variables de muestra vs universo
- Estructura exacta de diccionarios

---

**Fecha**: 2026-04-29  
**Confianza promedio**: baja (inferido desde nombres de archivo sin inspección de diccionarios)
