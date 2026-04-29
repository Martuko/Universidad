# Perfil Dataset: Chile (CP2017CHL)
## Reconocimiento Técnico Inicial - 2026-04-29

### Resumen

- **País**: Chile
- **Dataset**: CP2017CHL (Censo 2017)
- **Tamaño total**: 763MB
- **Fecha en disco**: Sep 12 2018 - Mar 7 2019
- **Estado**: Extraído y listo para análisis

### Archivos encontrados

```
data/extracted/CP2017CHL/
├── BaseOrg16/                      # Base Orgánica 16° Región
│   ├── CPV2017-16.rbf             # Datos principales (personas + viviendas)
│   ├── CPV2017-16.dic             # Diccionario principal
│   ├── CPV2017-16.dicx            # Diccionario comprimido
│   ├── CPV2017-16.~dicX           # Diccionario de respaldo
│   ├── CPV2017-16_LKP*.rbf        # Look-up keys (geocódigos)
│   ├── CPV2017-16_COMUNA*.rbf      # Código comunas
│   ├── CPV2017-16_REGION*.rbf      # Código regiones
│   ├── CPV2017-16*.ptr            # Pointer files (1601-1657)
│   ├── CPV2017-16_CENSO.rbf       # Censo total
│   └── regiones.prjX              # Archivo de proyecto
└── Docs/
    ├── Censo2017_Nombres_Id_Geogrаfica/  # Glosarios geográficos
    │   ├── Glosas_COMUNA*.txt
    │   ├── Glosas_DISTRITO*.txt
    │   ├── Glosas_LOCALIDAD*.txt
    │   ├── Glosas_PROVINCIA*.txt
    │   └── Glosas_REGION*.txt
    ├── CUESTIONARIO-CENSO-2017-OF.pdf
    ├── CUESTIONARIO-CENSO-2017-TRANSITO.pdf
    ├── CUESTIONARIO-CENSO-2017-VIVIENDAS-COLECTIVAS.pdf
    ├── LEAME.docx
    ├── Manual_de_usuario_Censo_2017_(16R).pdf
    ├── Manual_para-Censistas.pdf
    ├── presentacion_de_la_segunda_entrega_de_resultados_censo2017.pdf
    └── Presentacion_Resultados_Definitivos_Censo2017.pdf
```

### Estructura de archivos Redatam

#### Archivos principales (CPV2017-16*.rbf)

| Nombre | Rol |
|--------|-----|
| CPV2017-16.rbf | Datos combinados (viviendas + personas) |
| CPV2017-16*.ptr | Pointer files para navegación |

#### Look-up tables (LKP)

| Nombre | Rol |
|--------|-----|
| CPV2017-16_LKP.rbf | Look-up genérico |
| CPV2017-16_LKP1*.rbf | Look-up 1 (tipo de vivienda) |
| CPV2017-16_LKP2*.rbf | Look-up 2 (características vivienda) |
| CPV2017-16_LKP3*.rbf | Look-up 3 (ubicación vivienda) |
| CPV2017-16_LKP4*.rbf | Look-up 4 (población) |

#### Diccionarios

| Nombre | Rol |
|--------|-----|
| CPV2017-16.dic | Diccionario principal |
| CPV2017-16.dicx | Diccionario comprimido |
| CPV2017-16.~dicX | Diccionario de respaldo |

#### Variables candidatas detectadas

Desde los nombres de archivos:

**Vivienda:**
- Tipo de vivienda
- Materiales de construcción
- Servicios básicos
- Características físicas

**Geografía:**
- Región (16 regiones de Chile)
- Provincia
- Comuna
- Distrito
- Localidad

**Población:**
- Edad
- Sexo
- Estado civil
- Ocupación
- Educación (escolaridad)
- Migración

**Variables demográficas:**
- Censo poblacional
- Pobres por región
- Pobres por comuna

**Ponderadores:**
- Posibles ponderadores de diseño
- Ponderadores de supresión

### Problemas detectados

1. **No se pudo leer contenido de .rbf directamente** - Requiere librería Redatam o convertir a CSV
2. **Diccionarios (.dic) sin leer** - Necesitan inspección para entender códigos
3. **Pointer files (.ptr)** - No se comprendió su propósito sin librería Redatam
4. **Look-up tables** - Propósito no verificado

### Lectura de diccionarios

Los diccionarios contienen los nombres reales de las variables Redatam. Para inspeccionar:
```bash
strings data/extracted/CP2017CHL/BaseOrg16/CPV2017-16.dic | grep -v "^$" | sort -u
```

### Siguiente paso recomendado

1. Inspeccionar diccionario CPV2017-16.dic para listar variables reales
2. Listar y catalogar todos los archivos .txt en Docs/
3. Leer LEAME.docx para entender estructura
4. Evaluar si es necesario instalar librería Redatam o usar duckdb con extensión

---

**Total archivos BaseOrg16**: 71 archivos
**Total archivos Docs**: 17 archivos
