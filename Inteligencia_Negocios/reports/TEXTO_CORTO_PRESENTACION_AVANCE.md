# Texto corto para presentar avance

Nuestro proyecto usará datos censales Redatam de Chile, Brasil, Argentina y Perú. Ya decidimos trabajar con dos temas: escolaridad y vivienda.

Hasta ahora descargamos y organizamos los datasets, hicimos un inventario técnico, instalamos `redatamx` y logramos abrir los diccionarios `.dicx` de los cuatro países. Desde esos diccionarios extrajimos entidades y variables reales, por ejemplo entidades de persona, hogar/vivienda y geografía.

También construimos un Excel de avance con la estructura del dataset normalizado que usaremos para Power BI. El dataset final no será microdato crudo, sino una tabla agregada por país, ubicación geográfica, sexo, edad agrupada, tamaño poblacional, tema e indicador.

Las dimensiones mínimas ya están consideradas: sexo, edad agrupada, ubicación geográfica y tamaño poblacional. El siguiente paso es revisar las categorías/códigos de las variables seleccionadas para construir indicadores comparables de escolaridad y vivienda.
