#!/usr/bin/env Rscript

.libPaths(Sys.getenv("R_LIBS_USER"))

suppressPackageStartupMessages({
  library(redatamx)
})

out_dir <- "data/checks/redatamx"
report_dir <- "reports/phase2"

dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

datasets <- data.frame(
  country = c("argentina", "chile", "peru"),
  dataset = c("CP2010ARG", "CP2017CHL", "CP2017PER"),
  dictionary = c(
    "data/extracted/CP2010ARG/BASE_AMP_DPTO/CPV2010Ampliado.dicx",
    "data/extracted/CP2017CHL/BaseOrg16/CPV2017-16.dicx",
    "data/extracted/CP2017PER/BaseD/BaseR/CPVPER2017D.dicX"
  ),
  stringsAsFactors = FALSE
)

# Buscar posible diccionario .dicx de Brasil, si existe
brasil_dicx <- list.files(
  "data/extracted/CP2010BRA",
  pattern = "\\.dicx$|\\.dicX$",
  recursive = TRUE,
  full.names = TRUE,
  ignore.case = TRUE
)

if (length(brasil_dicx) > 0) {
  datasets <- rbind(
    datasets,
    data.frame(
      country = "brasil",
      dataset = "CP2010BRA",
      dictionary = brasil_dicx[1],
      stringsAsFactors = FALSE
    )
  )
}

all_entities <- data.frame()
all_variables <- data.frame()
errors <- data.frame()

safe_df <- function(x) {
  tryCatch(as.data.frame(x), error = function(e) data.frame(value = as.character(x)))
}

for (i in seq_len(nrow(datasets))) {
  country <- datasets$country[i]
  dataset <- datasets$dataset[i]
  dict_path <- datasets$dictionary[i]

  cat("============================================================\n")
  cat("País:", country, "\n")
  cat("Dataset:", dataset, "\n")
  cat("Diccionario:", dict_path, "\n")

  if (!file.exists(dict_path)) {
    errors <- rbind(errors, data.frame(
      country = country,
      dataset = dataset,
      step = "file_exists",
      entity = NA,
      error = "dictionary_not_found",
      stringsAsFactors = FALSE
    ))
    next
  }

  dic <- tryCatch(
    redatam_open(dict_path),
    error = function(e) e
  )

  if (inherits(dic, "error")) {
    errors <- rbind(errors, data.frame(
      country = country,
      dataset = dataset,
      step = "redatam_open",
      entity = NA,
      error = conditionMessage(dic),
      stringsAsFactors = FALSE
    ))
    next
  }

  entities <- tryCatch(
    safe_df(redatam_entities(dic)),
    error = function(e) e
  )

  if (inherits(entities, "error")) {
    errors <- rbind(errors, data.frame(
      country = country,
      dataset = dataset,
      step = "redatam_entities",
      entity = NA,
      error = conditionMessage(entities),
      stringsAsFactors = FALSE
    ))
    tryCatch(redatam_close(dic), error = function(e) NULL)
    next
  }

  entities$country <- country
  entities$dataset <- dataset
  entities$dictionary <- dict_path

  all_entities <- rbind(all_entities, entities)

  entity_names <- entities$name

  for (entity_name in entity_names) {
    cat("  Extrayendo variables entidad:", entity_name, "\n")

    vars <- tryCatch(
      safe_df(redatam_variables(dic, entity_name = entity_name)),
      error = function(e) e
    )

    if (inherits(vars, "error")) {
      errors <- rbind(errors, data.frame(
        country = country,
        dataset = dataset,
        step = "redatam_variables",
        entity = entity_name,
        error = conditionMessage(vars),
        stringsAsFactors = FALSE
      ))
      next
    }

    if (nrow(vars) == 0) {
      next
    }

    vars$country <- country
    vars$dataset <- dataset
    vars$dictionary <- dict_path
    vars$entity <- entity_name

    all_variables <- rbind(all_variables, vars)
  }

  tryCatch(redatam_close(dic), error = function(e) NULL)
}

write.csv(
  all_entities,
  file.path(out_dir, "redatam_entities_all.csv"),
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

write.csv(
  all_variables,
  file.path(out_dir, "redatam_variables_all.csv"),
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

write.csv(
  errors,
  file.path(out_dir, "redatam_variables_errors.csv"),
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

# Crear búsqueda temática simple sobre todas las columnas textuales
if (nrow(all_variables) > 0) {
  text_blob <- apply(all_variables, 1, function(row) {
    paste(row, collapse = " | ")
  })

  classify_theme <- function(txt) {
    txt_low <- tolower(txt)

    hits <- c()

    if (grepl("educ|escola|escolar|instru|nivel|curso|alfabet|ensino|grado|secundaria|superior|primaria|basica|básica|media", txt_low)) {
      hits <- c(hits, "escolaridad")
    }

    if (grepl("viv|vivienda|domicilio|domicílio|hogar|casa|parede|piso|techo|material|agua|saneamiento|baño|bano|desague|desagüe|alcantarillado|electricidad|dormitorio|hacinamiento", txt_low)) {
      hits <- c(hits, "vivienda")
    }

    if (grepl("sexo|sex|hombre|mujer|masculino|femenino|homem|mulher", txt_low)) {
      hits <- c(hits, "sexo")
    }

    if (grepl("edad|idade|age|tramo|grupo|años|anos", txt_low)) {
      hits <- c(hits, "edad")
    }

    if (grepl("region|región|provincia|comuna|municipio|distrito|departamento|uf|estado|localidad|area|área|urbano|rural|cod|código|codigo", txt_low)) {
      hits <- c(hits, "geografia")
    }

    if (grepl("peso|pondera|factor|expan|expansion|expansión|weight|fexp", txt_low)) {
      hits <- c(hits, "ponderador")
    }

    if (grepl("persona|pessoa|pessoas|morador|familia|família|hogar|vivienda", txt_low)) {
      hits <- c(hits, "entidad")
    }

    if (length(hits) == 0) {
      return(NA_character_)
    }

    paste(unique(hits), collapse = ";")
  }

  all_variables$theme_hits <- vapply(text_blob, classify_theme, character(1))

  hits <- all_variables[!is.na(all_variables$theme_hits), ]

  write.csv(
    hits,
    file.path(out_dir, "redatam_variables_theme_hits.csv"),
    row.names = FALSE,
    fileEncoding = "UTF-8"
  )
} else {
  hits <- data.frame()
  write.csv(
    hits,
    file.path(out_dir, "redatam_variables_theme_hits.csv"),
    row.names = FALSE,
    fileEncoding = "UTF-8"
  )
}

# Reporte Markdown
report_file <- file.path(report_dir, "redatam_variables_extraccion.md")

sink(report_file)

cat("# Extracción de entidades y variables Redatam\n\n")
cat("Fecha: ", as.character(Sys.time()), "\n\n", sep = "")

cat("## 1. Diccionarios procesados\n\n")
print(datasets)
cat("\n\n")

cat("## 2. Entidades encontradas\n\n")
if (nrow(all_entities) > 0) {
  print(all_entities)
} else {
  cat("No se extrajeron entidades.\n")
}
cat("\n\n")

cat("## 3. Resumen de variables por país y entidad\n\n")
if (nrow(all_variables) > 0) {
  summary_table <- as.data.frame(table(all_variables$country, all_variables$entity))
  names(summary_table) <- c("country", "entity", "n_variables")
  summary_table <- summary_table[summary_table$n_variables > 0, ]
  print(summary_table)
} else {
  cat("No se extrajeron variables.\n")
}
cat("\n\n")

cat("## 4. Variables candidatas por términos clave\n\n")
if (exists("hits") && nrow(hits) > 0) {
  cat("Total hits: ", nrow(hits), "\n\n", sep = "")
  print(head(hits, 100))
} else {
  cat("No se detectaron hits temáticos.\n")
}
cat("\n\n")

cat("## 5. Errores\n\n")
if (nrow(errors) > 0) {
  print(errors)
} else {
  cat("Sin errores críticos.\n")
}
cat("\n\n")

cat("## 6. Siguiente paso recomendado\n\n")
cat("- Revisar `data/checks/redatamx/redatam_variables_theme_hits.csv`.\n")
cat("- Confirmar variables de escolaridad, vivienda, sexo, edad, geografía y ponderadores.\n")
cat("- Resolver Brasil buscando su diccionario principal `.dicx` o documentación equivalente.\n")
cat("- Luego preparar consultas Redatam o exportaciones agregadas.\n")

sink()

cat("OK: entidades -> ", file.path(out_dir, "redatam_entities_all.csv"), "\n", sep = "")
cat("OK: variables -> ", file.path(out_dir, "redatam_variables_all.csv"), "\n", sep = "")
cat("OK: hits -> ", file.path(out_dir, "redatam_variables_theme_hits.csv"), "\n", sep = "")
cat("OK: errores -> ", file.path(out_dir, "redatam_variables_errors.csv"), "\n", sep = "")
cat("OK: reporte -> ", report_file, "\n", sep = "")
