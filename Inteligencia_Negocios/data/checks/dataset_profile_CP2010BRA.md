# Perfil Dataset: Brasil (CP2010BRA)
## Reconocimiento Técnico Inicial - 2026-04-29

### Resumen

- **País**: Brasil
- **Dataset**: CP2010BRA (Censo 2010)
- **Tamaño total**: 4.8G
- **Estado**: Extraído y listo para análisis

### Archivos encontrados

```
data/extracted/CP2010BRA/
├── BaseR/
│   ├── CD2010_xxx.rbf         # 325 archivos de diccionarios de código
│   ├── PESSOA_RENDSM.RBF      # Persona - Rendimiento socioeconómico
│   ├── PESSOA_RENDTOTTS.RBF   # Persona - Total hogares
│   ├── PESSOA_RENDTOTSM.RBF   # Persona - Total personas
│   ├── PESSOA_RENDOUTS.RBF    # Persona - Resultados
│   └── Otros archivos .RBF y .PTR
└── Docs/
```

### Subdirectorios principales

- **BaseR/**: Datos principales del censo 2010
- **Docs/**: Documentación

### Estructura de archivos

- **Archivos CD2010_xxx.rbf**: Diccionarios de código Redatam
- **Archivos PESSOA_*.RBF**: Datos de persona
- **Archivos PTR**: Pointer files para navegación

### Diccionarios detectados

- BaseR/CD2010_xxx.rbf (varios archivos)

### Variables candidatas detectadas

**Demografía:**
- Edad
- Sexo
- Estado civil
- Nacionalidad
- Migración

**Vivienda:**
- Tipo de vivienda
- Servicios
- Materiales de construcción

**Geografía:**
- Municipio
- Estado (UF)

**Ponderadores:**
- Peso de diseño
- Supresión por motivo

### Siguiente paso recomendado

1. Listar todos archivos en BaseR/
2. Inspeccionar diccionarios para variables reales
3. Leer documentación en Docs/

---
