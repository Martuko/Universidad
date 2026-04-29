# Reconocimiento inicial datasets Redatam

## 1. Resumen ejecutivo

- **datasets detectados**: 7 (Chile: 1, Brasil: 3, Perú: 2, Argentina: 1)
- **tamaño total aproximado**: 14.9 GB
- **cantidad de archivos**: 1,438 archivos
- **extensiones principales**: .rbf (1,104), .dic/.dicx (108), .bin (149), .pdf (29)
- **formatos Redatam detectados**: CPV (Censo Población y Vivienda), CD (diccionarios), PESSOA (persona - Brasil)
- **estado del reconocimiento**: Completado - inventario y clasificación terminada
- **riesgos técnicos principales**: archivos .rbf no legibles sin librería Redatam; no confirmados ponderadores; diferencias entre censos sin homologación

---

## 2. Estado por país principal

### Chile - CP2017CHL

- **tamaño del dataset**: 763 MB
- **estructura encontrada**: `BaseOrg16/` (71 archivos) + `Docs/` (17 archivos)
- **archivos principales detectados**:
  - `CPV2017-16.rbf` - Datos combinados (personas + viviendas)
  - `CPV2017-16*.ptr` - Pointer files
  - `CPV2017-16_LKP*.rbf` - Look-up tables
- **diccionarios encontrados**: `CPV2017-16.dic`, `.dicx`, `.~dicX`
- **documentación encontrada**: 17 archivos (.pdf, .docx, .txt) en `Docs/`
- **archivos de datos Redatam encontrados**: 71 archivos .rbf en `BaseOrg16/`

#### Variables candidatas para escolaridad
No lo sé (no se inspeccionó contenido de diccionarios)

#### Variables candidatas para vivienda
Inferido desde nombre de archivo (confianza baja):
- Tipo de vivienda (inferido desde glosarios .txt)
- Materiales de construcción (inferido desde LKP2)
- Servicios básicos (inferido desde LKP3)
- Características físicas (inferido desde LKP2)

#### Variables candidatas para sexo
Inferido desde nombre de archivo (confianza baja):
- Sexo (Hombre/Mujer) - inferido desde estructura poblacional estándar

#### Variables candidatas para edad
Inferido desde nombre de archivo (confianza baja):
- Edad - inferido desde rango 0-100+ típico en censos

#### Variables candidatas para geografía
Inferido desde nombres de archivos (confianza media):
- Región (16 regiones) - desde CPV2017-16_REGION_REDCODENOMBRE
- Comuna - desde glosarios Glosas_COMUNA*.txt
- Distrito - desde glosarios Glosas_DISTRITO*.txt
- Localidad - desde glosarios Glosas_LOCALIDAD*.txt
- Provincia - desde glosarios Glosas_PROVINCIA*.txt

#### Variables candidatas para ponderadores
No lo sé (no confirmados localmente)

#### nivel de confianza: **medio** (inferido desde estructura y nombres)
- **dudas pendientes**: Inspeccionar diccionario CPV2017-16.dic, confirmar ponderadores
- **siguiente paso recomendado**: `strings data/extracted/CP2017CHL/BaseOrg16/CPV2017-16.dic | grep -v "^$" | sort -u > /tmp/CPV2017CHL_vars.txt`

---

### Brasil - CP2010BRA

- **tamaño del dataset**: 4.8 GB
- **estructura encontrada**: `BaseR/` (335 archivos) + `Docs/`
- **archivos principales detectados**:
  - `CD2010_xxx.rbf` - Diccionarios de código (325 archivos)
  - `PESSOA_RENDSM.RBF` - Persona - Rendimiento socioeconómico
  - `PESSOA_RENDTOTTS.RBF` - Persona - Total hogares
  - `PESSOA_RENDTOTSM.RBF` - Persona - Total personas
  - `PESSOA_RENDOUTS.RBF` - Persona - Resultados
- **diccionarios encontrados**: `CD2010_xxx.rbf` (325 archivos)
- **documentación encontrada**: No listada en perfiles
- **archivos de datos Redatam encontrados**: Archivos PESSOA_*.RBF y otros .RBf

#### Variables candidatas para escolaridad
No lo sé (no se inspeccionó diccionario)

#### Variables candidatas para vivienda
Inferido desde estructura (confianza baja):
- Tipo de vivienda (inferido desde diccionarios CD2010)
- Servicios (inferido desde estructura estándar Brasil)
- Materiales de construcción (inferido desde estructura)

#### Variables candidatas para sexo
Inferido desde estructura (confianza baja):
- Sexo (Hombre/Mujer) - inferido desde PESSOA_RENDSM

#### Variables candidatas para edad
Inferido desde estructura (confianza baja):
- Edad - inferido desde estructura estándar censo Brasil

#### Variables candidatas para geografía
Inferido desde estructura (confianza media):
- Municipio (inferido desde diccionarios CD2010)
- Estado (UF) (inferido desde estructura censo Brasil)

#### Variables candidatas para ponderadores
No lo sé (no confirmados)

#### nivel de confianza: **bajo** (inferido desde nombres de archivo sin inspección de diccionarios)
- **dudas pendientes**: Inspeccionar diccionarios CD2010, confirmar estructura de variables
- **siguiente paso recomendado**: `ls data/extracted/CP2010BRA/BaseR/ | head -20`

---

### Argentina - CP2010ARG

- **tamaño del dataset**: 1.5 GB
- **estructura encontrada**: `BASE_AMP_DPTO/` (190 archivos) + `Docs/`
- **archivos principales detectados**:
  - `CPV2000xx.rbf` - Datos ampliados
  - `CPV2001xx.rbf` - Datos ampliados
- **diccionarios encontrados**: `CPV2010Ampliado.dic`, `.dicx`
- **documentación encontrada**: No listada en perfiles
- **archivos de datos Redatam encontrados**: Archivos CPV2000xx.rbf y CPV2001xx.rbf

#### Variables candidatas para escolaridad
No lo sabe (no se inspeccionó diccionario)

#### Variables candidatas para vivienda
Inferido desde nombre (confianza baja):
- Tipo de vivienda (inferido desde CPV)
- Servicios (inferido desde estructura)

#### Variables candidatas para sexo
Inferido desde estructura (confianza baja):
- Sexo (inferido desde estructura CPV estándar)

#### Variables candidatas para edad
Inferido desde estructura (confianza baja):
- Edad (inferido desde estructura CPV estándar)

#### Variables candidatas para geografía
Inferido desde estructura (confianza media):
- Departamento (inferido desde nombre BASE_AMP_DPTO)
- Provincia (inferido desde estructura Argentina)

#### Variables candidatas para ponderadores
No lo sabe (no confirmados)

#### nivel de confianza: **bajo** (inferido desde estructura sin inspección de diccionarios)
- **dudas pendientes**: Inspeccionar diccionario CPV2010Ampliado
- **siguiente paso recomendado**: `strings data/extracted/CP2010ARG/BASE_AMP_DPTO/CPV2010Ampliado.dic | head -100`

---

### Perú - CP2017PER

- **tamaño del dataset**: 1.8 GB
- **estructura encontrada**: `BaseD/` (archivos .rbf) + `Docs/`
- **archivos principales detectados**:
  - `CPVPER2017D-xxx.rbf` - Datos de censo Perú
  - `C5PxDI.rbf` - Diccionarios
- **diccionarios encontrados**: `CPVPER2017D.dic`
- **documentación encontrada**: No listada en perfiles
- **archivos de datos Redatam encontrados**: Archivos CPVPER2017D-xxx.rbf

#### Variables candidatas para escolaridad
No lo sabe (no se inspeccionó diccionario)

#### Variables candidatas para vivienda
Inferido desde nombre (confianza baja):
- Tipo de vivienda (inferido desde CPVPER2017D)
- Servicios (inferido desde estructura Perú)
- Materiales (inferido desde estructura)

#### Variables candidatas para sexo
Inferido desde estructura (confianza baja):
- Sexo (inferido desde estructura censo Perú)

#### Variables candidatas para edad
Inferido desde estructura (confianza baja):
- Edad (inferido desde estructura censo Perú)

#### Variables candidatas para geografía
Inferido desde nombres de archivos (confianza media):
- Provincia (inferido desde estructura Perú)
- Distrito (inferido desde estructura Perú)
- Sección (inferido desde estructura Perú)
- Parcela (inferido desde estructura Perú)

#### Variables candidatas para ponderadores
No lo sabe (no confirmados)

#### nivel de confianza: **bajo** (inferido desde estructura sin inspección de diccionarios)
- **dudas pendientes**: Inspeccionar diccionario CPVPER2017D
- **siguiente paso recomendado**: `strings data/extracted/CP2017PER/BaseD/BaseR/CPVPER2017D.dic | head -100`

---

## 3. Datasets no prioritarios

Estos datasets fueron inventariados pero **no serán usados** en el análisis principal salvo cambio del proyecto:

- **CP2007PER** (Perú 2007): 1.6 GB - inventariado, no inspeccionado
- **Cp1991BRA** (Brasil 1991): 1.8 GB - inventariado, no inspeccionado
- **Cp2000BRA** (Brasil 2000): 3.0 GB - inventariado, no inspeccionado

---

## 4. Evaluación de viabilidad

### Chile - CP2017CHL
**Estado**: **Requiere revisar metadata**
- Estructura clara desde nombres de archivos
- Diccionarios disponibles pero no inspeccionados
- Documentación completa en Docs/
- **No listo para conversión sin inspeccionar diccionarios**

### Brasil - CP2010BRA
**Estado**: **Requiere revisar metadata**
- Estructura desde nombres PESSOA_*
- Diccionarios existentes (CD2010_xxx.rbf)
- **No listo para conversión sin inspeccionar diccionarios**

### Argentina - CP2010ARG
**Estado**: **Requiere revisar metadata**
- Estructura desde nombre BASE_AMP_DPTO
- Diccionario CPV2010Ampliado
- **No listo para conversión sin inspeccionar diccionarios**

### Perú - CP2017PER
**Estado**: **Requiere revisar metadata**
- Estructura desde nombre CPVPER2017D
- Diccionario CPVPER2017D
- **No listo para conversión sin inspeccionar diccionarios**

---

## 5. Riesgos técnicos

- ⚠️ **archivos .rbf no legibles directamente con DuckDB** - Confirmado en todos los archivos
- ⚠️ **necesidad de Redatam/redatamx u otra herramienta** - Requiere instalación o librería específica
- ⚠️ **riesgo de no encontrar ponderadores** - No se han confirmado localmente
- ⚠️ **diferencias entre años censales** - 2017CHL vs 2010ARG vs 2010BRA vs 2017PER pueden tener estructuras diferentes
- ⚠️ **diferencias entre muestra/universo** - No confirmadas localmente
- ⚠️ **riesgo de variables no homologables** - Sin inspección de diccionarios no se puede confirmar homogeneidad
- ⚠️ **riesgo de comparar conteos absolutos** - Sin confirmar ponderadores y métodos de muestreo es riesgoso

---

## 6. Recomendación para siguiente fase

1. Inspeccionar diccionarios principales (`CPV2017-16.dic`, `CD2010_xxx.rbf`, etc.)
2. Extraer nombres reales de variables con `strings`
3. Crear diccionario de homologación por país
4. Definir variables finales de escolaridad y vivienda
5. Convertir solo variables necesarias a CSV/Parquet
6. Crear capa staging (limpio por país)
7. Crear capa BI agregada (unificada por indicador)

---

## 7. Limitaciones

- **No lo sé**: Nombres reales de variables (sin inspección de diccionarios)
- **No lo sé**: Ponderadores existentes
- **No lo sé**: Variables confirmadas entre países
- **No lo sé**: Variables de muestra vs universo
- **No lo sé**: Exactitud de conteos sin confirmar ponderadores
- **No lo só**: Estructura exacta de diccionarios sin inspeccionar

---

**Fecha**: 2026-04-29  
**Estado**: Reconocimiento inicial completado, inspección de diccionarios pendiente  
**Próximo paso**: Inspeccionar 4 diccionarios principales (1 por país prioritario)
