# Checklist Requisitos para el Profesor

**Fecha:** 2026-04-30  
**Proyecto:** BI Redatam - Análisis comparativo multinacional

---

## Tabla de Requisitos y Estado

| Requisito del trabajo | Estado actual | Evidencia/archivo | Pendiente |
|---|---|---|---|
| **4 países incluyendo Chile** | ✅ Completado | - Chile (CP2017CHL) 2017<br>- Brasil (CP2010BRA) 2010<br>- Argentina (CP2010ARG) 2010<br>- Perú (CP2017PER) 2017<br>*Ver Excel y diccionarios .dicx abiertos* | No |
| **2 temas seleccionados** | ✅ Completado | Escolaridad y Vivienda<br>*Decision tomada y documentada* | No |
| **Sexo normalizado** | ✅ Diseñado | Valores: hombre, mujer, no_informado<br>*Ver sección 7 del AVANCE_PARA_PROFESOR* | No |
| **Edad agrupada** | ✅ Diseñado | 0_14, 15_24, 25_44, 45_64, 65_mas, no_informado<br>*Ver sección 7 del AVANCE_PARA_PROFESOR* | No |
| **Ubicación geográfica** | ✅ Diseñado | Chile: Comuna<br>Brasil: Municipio<br>Argentina: Departamento/Partido<br>Perú: Distrito<br>*Ver sección 7 del AVANCE_PARA_PROFESOR* | No |
| **Tamaño poblacional** | ✅ Diseñado | Categorías: muy_pequeno (<10k), pequeno (10k-50k), mediano (50k-200k), grande (200k-1M), metropolitano (>1M)<br>*Ver sección 7 del AVANCE_PARA_PROFESOR* | No |
| **Dataset normalizado propuesto** | ✅ Diseñado | Estructura de tabla agregada con 20 campos definidos<br>*Ver sección 3 del AVANCE_PARA_PROFESOR* | No |
| **Variables y categorizaciones** | 🟡 En revisión | Diccionarios .dicx extraídos<br>Entidades identificadas<br>Variables candidatas en CSVs de selección<br>*Falta revisión de códigos/categorías por país* | Sí - Revisión de códigos |
| **Power BI futuro** | 🟡 Planificado | Diseño de esquema de datos listo<br>Medidas DAX por definir<br>*Pendiente definir medidas* | Sí - Definir medidas |
| **GeoDa Chile futuro** | 🟡 Planificado | Preparar archivo único para Chile<br>Usar comuna como unidad<br>*Pendiente preparación* | Sí - Preparar archivo |
| **Dashboard mínimo 3 páginas futuro** | 🟡 Planificado | Estructura sugerida:<br>1. Resumen por país<br>2. Escolaridad comparada<br>3. Vivienda comparada<br>*Pendiente construir* | Sí - Construir dashboard |
| **Storytelling futuro** | 🟡 Planificado | Narrativa: Brechas educativas y condiciones de vivienda entre países<br>*Pendiente desarrollar* | Sí - Desarrollar narrativa |

---

## Resumen de Estado

| Categoría | Total | Completado | Pendiente |
|---|---|---|---|
| Requisitos | 11 | 6 | 5 |

---

## Evidencia Principal

- **Excel de avance:** `reports/avances_dataset_normalizado_redatam.xlsx`
- **Diccionarios:** Archivos .dicx de los 4 países en `data/checks/redatamx/`
- **Entidades:** `data/checks/redatamx/redatam_entities_all.csv`
- **Variables:** `data/checks/redatamx/redatam_variables_all.csv`
- **Selección escolaridad:** `data/checks/redatamx/selection/escolaridad_candidatas.csv`
- **Selección vivienda:** `data/checks/redatamx/selection/vivienda_candidatas.csv`
- **Selección dimensiones:** `data/checks/redatamx/selection/dimensiones_candidatas.csv`

---

## Próximos Pasos Críticos

1. Revisar códigos de categorización por país para variables seleccionadas
2. Definir medidas DAX para Power BI
3. Preparar dataset de Chile para GeoDa
4. Construir primera tabla agregada de prueba
5. Desarrollar narrativa de storytelling inicial
