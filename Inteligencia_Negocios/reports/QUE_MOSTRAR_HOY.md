# Guía Práctica: Qué Mostrar al Profesor Hoy

**Fecha:** 2026-04-30  
**Objetivo:** Presentar avance del proyecto BI Redatam

---

## 1. PRIMERO: Abrir el Excel

**Archivo principal:**
```
reports/avances_dataset_normalizado_redatam.xlsx
```

### Hojas importantes en orden de presentación:

1. **Resumen** (si existe) - Para dar contexto rápido
2. **Países** - Mostrar los 4 países seleccionados
3. **Variables candidatas** - Mostrar escolaridad y vivienda por país
4. **Dimensiones** - Mostrar sexo, edad, ubicación, tamaño poblacional
5. **Indicadores propuestos** - Mostrar qué analizaremos

---

## 2. EXPLICAR AL PROFESOR

### 2.1 Qué NO es esto:

> **NO son microdatos crudos directamente del censo.**

Es importante dejar claro desde el principio:

- No es el archivo completo del censo
- No es crudo sin procesar
- Es un **dataset de trabajo normalizado**

### 2.2 Qué ES esto:

> **Sí es un dataset normalizado de trabajo**

Este archivo representa:

- ✅ Estructura definida para análisis comparativo
- ✅ Datos de 4 países con 2 temas
- ✅ Dimensiones estandarizadas (sexo, edad, ubicación, tamaño)
- ✅ Lista de variables candidatas revisadas
- ✅ Indicadores propuestos para cálculo
- ✅ Preparado para agregación en Power BI

### 2.3 Qué falta para la tabla final:

> **No es la tabla final para producción**

Lo que falta:

1. **Revisión de códigos/categorías** de las variables seleccionadas por país
2. **Homologación de categorías** - mapear códigos diferentes entre países a valores comparables
3. **Definición de ponderadores** - decidir si usar pesos por país
4. **Cálculo de indicadores** - aplicar fórmulas y verificar resultados
5. **Generación de tabla agregada** - crear tabla final para Power BI

---

## 3. LO QUE YA LOGRAMOS

### Checklist rápido para explicar:

- [x] Seleccionados: Chile, Brasil, Argentina, Perú
- [x] Temáticas: Escolaridad + Vivienda
- [x] Datasets descargados de Redatam
- [x] Diccionarios `.dicx` abiertos con `redatamx`
- [x] Entidades extraídas (persona, hogar, vivienda)
- [x] Variables identificadas por país
- [x] Dimensiones estandarizadas definidas
- [x] Indicadores propuestos listados
- [x] Estructura normalizada diseñada

### Qué falta confirmar:

- [ ] Revisión detallada de códigos de categorización
- [ ] Definición de ponderadores
- [ ] Cálculo de primeros indicadores
- [ ] Generación de tabla agregada

---

## 4. PREGUNTAS PARA EL PROFESOR

Tener estas preguntas listas:

1. **Comparación entre censos:**
   - ¿Acepta comparar censos de años distintos (2010 Chile vs 2017 Perú)?
   - ¿Prefiere análisis solo dentro de una misma referencia temporal?

2. **Formato de resultados:**
   - ¿Prefiere ver conteos absolutos o porcentajes?
   - ¿O ambas, con preferencia clara?

3. **Unidad geográfica:**
   - ¿El tamaño poblacional debe agregarse por comuna/municipio/departamento/distrito?
   - ¿O prefiere un nivel territorial único para todo?

4. **Herramienta GeoDa:**
   - ¿Para GeoDa en Chile, prefiere usar comuna o región como unidad espacial?
   - ¿Hay preferencia sobre el nivel territorial?

5. **Homologación de variables:**
   - ¿Acepta indicadores aproximados (no variables idénticas) para comparar países?
   - ¿O exige exactamente la misma variable en todos los países?

---

## 5. FOLIOS ADICIONALES A TENER LISTOS

Estos están disponibles para profundizar:

- `reports/AVANCE_PARA_PROFESOR.md` - Documento técnico completo
- `reports/HANDOFF_COMPANERO_AVANCE.md` - Contexto y estado
- `reports/TEXTO_CORTO_PRESENTACION_AVANCE.md` - Versión resumida
- `data/checks/redatamx/redatam_variables_all.csv` - Variables extraídas
- `data/checks/redatamx/selection/*.csv` - Variables candidatas por tema

---

## 6. ESTRUCTURA DE LA PRESENTACIÓN

**Minuto 0-3:** Saludo + contexto del proyecto  
**Minuto 3-8:** Mostrar Excel + explicar hojas clave  
**Minuto 8-12:** Explicar qué es y qué falta  
**Minuto 12-15:** Preguntar dudas + feedback

**Total:** ~15 minutos

---

## 7. SEÑALES VERDES / ROJAS

### Verdes (listo):
- ✅ Datos descargados
- ✅ Diccionarios abiertos
- ✅ Variables identificadas
- ✅ Estructura diseñada

### Rojas (pendiente):
- ❓ Códigos no revisados aún
- ❓ Homologación por hacer
- ❓ Primer cálculo pendiente
- ❓ Tabla agregada no generada

**Mensaje clave al profesor:**  
*"Tenemos todo lo técnico listo. Ahora necesitamos su retroalimentación para validar el enfoque metodológico y definir los siguientes pasos."*
