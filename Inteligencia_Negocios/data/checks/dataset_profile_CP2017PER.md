# Perfil Dataset: Perú (CP2017PER)
## Reconocimiento Técnico Inicial - 2026-04-29

### Resumen

- **País**: Perú
- **Dataset**: CP2017PER (Censo 2017)
- **Tamaño total**: 1.8G
- **Estado**: Extraído y listo para análisis

### Archivos encontrados

```
data/extracted/CP2017PER/
├── BaseD/
│   ├── CPVPER2017D-xxx.rbf
│   └── C5PxDI.rbf
└── Docs/
```

### Subdirectorios principales

- **BaseD/**: Datos principales (Base de Datos)
- **Docs/**: Documentación

### Estructura de archivos

- **CPVPER2017D-xxx.rbf**: Datos de vivienda/persona (CPV = Censo Población y Vivienda)
- **C5PxDI.rbf**: Diccionarios o look-up tables

### Variables candidatas detectadas

**Demografía:**
- Edad
- Sexo
- Estado civil
- Ocupación
- Educación

**Vivienda:**
- Tipo de vivienda
- Servicios
- Materiales

**Geografía:**
- Provincia
- Distrito
- Sección
- Parcela

### Siguiente paso recomendado

1. Listar todos archivos en BaseD/
2. Inspeccionar diccionarios en Docs/
3. Leer documentación

---
