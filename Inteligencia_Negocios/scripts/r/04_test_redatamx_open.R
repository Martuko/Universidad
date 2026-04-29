#!/usr/bin/env Rscript

.libPaths(Sys.getenv("R_LIBS_USER"))

suppressPackageStartupMessages({
  library(redatamx)
})

out_dir <- "data/checks/redatamx"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

report_file <- file.path(out_dir, "redatamx_open_test.txt")
csv_file <- file.path(out_dir, "redatamx_open_test.csv")

all_files <- list.files(
  "data/extracted",
  recursive = TRUE,
  full.names = TRUE,
  ignore.case = TRUE
)

wanted_names <- c(
  "CPV2017-16.dicx",
  "CPV2017-16.dic",
  "CPV2010Ampliado.dicx",
  "CPV2010Ampliado.dic",
  "CPVPER2017D.dicx",
  "CPVPER2017D.dic"
)

candidate_files <- all_files[
  tolower(basename(all_files)) %in% tolower(wanted_names)
]

# Brasil puede no tener .dic/.dicx claro. Agregamos candidatos .RBF principales,
# pero solo para probar apertura controlada. Si falla, se documenta.
brasil_candidates <- all_files[
  grepl("CP2010BRA", all_files, ignore.case = TRUE) &
    grepl("(PESSOA|CD2010).*\\.(rbf|RBF)$", basename(all_files), ignore.case = TRUE)
]

brasil_candidates <- head(brasil_candidates, 10)

candidate_files <- unique(c(candidate_files, brasil_candidates))

sink(report_file)

cat("== redatamx open test ==\n")
cat("Package version:", as.character(packageVersion("redatamx")), "\n")
cat("R_LIBS_USER:", Sys.getenv("R_LIBS_USER"), "\n")
cat("Working directory:", getwd(), "\n\n")

cat("Available redatamx functions:\n")
print(ls("package:redatamx"))
cat("\n")

cat("Candidate files found:", length(candidate_files), "\n\n")

results <- data.frame(
  path = character(),
  file_name = character(),
  size_bytes = numeric(),
  status = character(),
  class = character(),
  entities_status = character(),
  variables_status = character(),
  error = character(),
  strings_preview = character(),
  strings_has_text = logical(),
  strings_hits = integer(),
  strings_path = character(),
  strings_unique_path = character(),
  strings_hits_path = character(),
  strings_full_path = character(),
  strings_full_unique_path = character(),
  strings_full_hits_path = character(),
  strings_error = character(),
  strings_exit = integer(),
  strings_lines = integer(),
  strings_unique_lines = integer(),
  strings_hits_lines = integer(),
  strings_full_lines = integer(),
  strings_full_unique_lines = integer(),
  strings_full_hits_lines = integer(),
  strings_full_error = character(),
  strings_full_exit = integer(),
  strings_full_status = character(),
  strings_full_command = character(),
  strings_command = character(),
  notes = character(),
  strings_category_hits = character(),
  strings_full_category_hits = character(),
  strings_full_terms_used = character(),
  strings_terms_used = character(),
  strings_full_terms_path = character(),
  strings_terms_path = character(),
  strings_full_category_hits_path = character(),
  strings_category_hits_path = character(),
  strings_full_terms_error = character(),
  strings_terms_error = character(),
  strings_full_category_hits_error = character(),
  strings_category_hits_error = character(),
  strings_full_terms_exit = integer(),
  strings_terms_exit = integer(),
  strings_full_category_hits_exit = integer(),
  strings_category_hits_exit = integer(),
  strings_full_terms_lines = integer(),
  strings_terms_lines = integer(),
  strings_full_category_hits_lines = integer(),
  strings_category_hits_lines = integer(),
  strings_full_terms_status = character(),
  strings_terms_status = character(),
  strings_full_category_hits_status = character(),
  strings_category_hits_status = character(),
  strings_full_terms_command = character(),
  strings_terms_command = character(),
  strings_full_category_hits_command = character(),
  strings_category_hits_command = character(),
  strings_full_terms_notes = character(),
  strings_terms_notes = character(),
  strings_full_category_hits_notes = character(),
  strings_category_hits_notes = character(),
  strings_full_terms_preview = character(),
  strings_terms_preview = character(),
  strings_full_category_hits_preview = character(),
  strings_category_hits_preview = character(),
  strings_full_terms_has_text = logical(),
  strings_terms_has_text = logical(),
  strings_full_category_hits_has_text = logical(),
  strings_category_hits_has_text = logical(),
  strings_full_terms_hits = integer(),
  strings_terms_hits = integer(),
  strings_full_category_hits_hits = integer(),
  strings_category_hits_hits = integer(),
  strings_full_terms_unique_path = character(),
  strings_terms_unique_path = character(),
  strings_full_category_hits_unique_path = character(),
  strings_category_hits_unique_path = character(),
  strings_full_terms_hits_path = character(),
  strings_terms_hits_path = character(),
  strings_full_category_hits_hits_path = character(),
  strings_category_hits_hits_path = character(),
  strings_full_terms_full_path = character(),
  strings_terms_full_path = character(),
  strings_full_category_hits_full_path = character(),
  strings_category_hits_full_path = character(),
  strings_full_terms_full_unique_path = character(),
  strings_terms_full_unique_path = character(),
  strings_full_category_hits_full_unique_path = character(),
  strings_category_hits_full_unique_path = character(),
  strings_full_terms_full_hits_path = character(),
  strings_terms_full_hits_path = character(),
  strings_full_category_hits_full_hits_path = character(),
  strings_category_hits_full_hits_path = character(),
  strings_full_terms_strings_error = character(),
  strings_terms_strings_error = character(),
  strings_full_category_hits_strings_error = character(),
  strings_category_hits_strings_error = character(),
  strings_full_terms_strings_exit = integer(),
  strings_terms_strings_exit = integer(),
  strings_full_category_hits_strings_exit = integer(),
  strings_category_hits_strings_exit = integer(),
  strings_full_terms_strings_lines = integer(),
  strings_terms_strings_lines = integer(),
  strings_full_category_hits_strings_lines = integer(),
  strings_category_hits_strings_lines = integer(),
  strings_full_terms_strings_unique_lines = integer(),
  strings_terms_strings_unique_lines = integer(),
  strings_full_category_hits_strings_unique_lines = integer(),
  strings_category_hits_strings_unique_lines = integer(),
  strings_full_terms_strings_hits_lines = integer(),
  strings_terms_strings_hits_lines = integer(),
  strings_full_category_hits_strings_hits_lines = integer(),
  strings_category_hits_strings_hits_lines = integer(),
  strings_full_terms_strings_full_lines = integer(),
  strings_terms_strings_full_lines = integer(),
  strings_full_category_hits_strings_full_lines = integer(),
  strings_category_hits_strings_full_lines = integer(),
  strings_full_terms_strings_full_unique_lines = integer(),
  strings_terms_strings_full_unique_lines = integer(),
  strings_full_category_hits_strings_full_unique_lines = integer(),
  strings_category_hits_strings_full_unique_lines = integer(),
  strings_full_terms_strings_full_hits_lines = integer(),
  strings_terms_strings_full_hits_lines = integer(),
  strings_full_category_hits_strings_full_hits_lines = integer(),
  strings_category_hits_strings_full_hits_lines = integer(),
  strings_full_terms_strings_full_error = character(),
  strings_terms_strings_full_error = character(),
  strings_full_category_hits_strings_full_error = character(),
  strings_category_hits_strings_full_error = character(),
  strings_full_terms_strings_full_exit = integer(),
  strings_terms_strings_full_exit = integer(),
  strings_full_category_hits_strings_full_exit = integer(),
  strings_category_hits_strings_full_exit = integer(),
  strings_full_terms_strings_full_status = character(),
  strings_terms_strings_full_status = character(),
  strings_full_category_hits_strings_full_status = character(),
  strings_category_hits_strings_full_status = character(),
  strings_full_terms_strings_full_command = character(),
  strings_terms_strings_full_command = character(),
  strings_full_category_hits_strings_full_command = character(),
  strings_category_hits_strings_full_command = character(),
  strings_full_terms_strings_command = character(),
  strings_terms_strings_command = character(),
  strings_full_category_hits_strings_command = character(),
  strings_category_hits_strings_command = character(),
  strings_full_terms_strings_category_hits = character(),
  strings_terms_strings_category_hits = character(),
  strings_full_category_hits_strings_category_hits = character(),
  strings_category_hits_strings_category_hits = character(),
  strings_full_terms_strings_full_category_hits = character(),
  strings_terms_strings_full_category_hits = character(),
  strings_full_category_hits_strings_full_category_hits = character(),
  strings_category_hits_strings_full_category_hits = character(),
  strings_full_terms_strings_full_terms_used = character(),
  strings_terms_strings_full_terms_used = character(),
  strings_full_category_hits_strings_full_terms_used = character(),
  strings_category_hits_strings_full_terms_used = character(),
  strings_full_terms_strings_terms_used = character(),
  strings_terms_strings_terms_used = character(),
  strings_full_category_hits_strings_terms_used = character(),
  strings_category_hits_strings_terms_used = character(),
  stringsAsFactors = FALSE
)

# Reducimos resultados a columnas útiles al final para no depender de estructura rara.
simple_results <- data.frame(
  path = character(),
  file_name = character(),
  size_bytes = numeric(),
  status = character(),
  object_class = character(),
  entities_n = integer(),
  variables_n = integer(),
  error = character(),
  notes = character(),
  strings_preview = character(),
  strings_has_text = logical(),
  strings_hits = integer(),
  stringsAsFactors = FALSE
)

terms_regex <- paste(c(
  "educ", "escola", "escolar", "instru", "nivel", "curso", "alfabet",
  "ensino", "grado", "secundaria", "superior", "primaria", "basica", "básica", "media",
  "viv", "vivienda", "domicilio", "domicílio", "hogar", "casa", "parede", "piso",
  "techo", "material", "agua", "saneamiento", "baño", "bano", "desague", "desagüe",
  "alcantarillado", "electricidad", "dormitorio", "hacinamiento",
  "sexo", "sex", "hombre", "mujer", "masculino", "femenino", "homem", "mulher",
  "edad", "idade", "age", "tramo", "grupo", "años", "anos",
  "region", "región", "provincia", "comuna", "municipio", "distrito", "departamento",
  "uf", "estado", "localidad", "area", "área", "urbano", "rural", "cod", "código", "codigo",
  "peso", "pondera", "factor", "expan", "expansion", "expansión", "weight", "fexp",
  "persona", "pessoa", "pessoas", "morador", "familia", "família"
), collapse = "|")

for (p in candidate_files) {
  cat("------------------------------------------------------------\n")
  cat("Testing:", p, "\n")
  cat("Size bytes:", file.info(p)$size, "\n")

  object_class <- ""
  entities_n <- NA_integer_
  variables_n <- NA_integer_
  status <- "unknown"
  err <- ""
  notes <- ""

  # Preview controlado con strings
  str_preview <- tryCatch({
    x <- system2("strings", args = c("-n", "4", p), stdout = TRUE, stderr = TRUE)
    x <- x[nzchar(trimws(x))]
    paste(head(x, 20), collapse = " | ")
  }, error = function(e) {
    paste("strings_failed:", conditionMessage(e))
  })

  str_hits <- tryCatch({
    x <- system2("strings", args = c("-n", "4", p), stdout = TRUE, stderr = TRUE)
    x <- x[grepl(terms_regex, x, ignore.case = TRUE)]
    length(x)
  }, error = function(e) {
    0L
  })

  has_text <- !grepl("^strings_failed:", str_preview) && nchar(str_preview) > 0

  result <- tryCatch({
    dic <- redatam_open(p)
    status <<- "opened_ok"
    object_class <<- paste(class(dic), collapse = "|")

    ent <- tryCatch(redatam_entities(dic), error = function(e) e)
    if (inherits(ent, "error")) {
      notes <<- paste(notes, "entities_failed:", conditionMessage(ent))
    } else {
      entities_n <<- tryCatch(nrow(as.data.frame(ent)), error = function(e) length(ent))
      cat("Entities:\n")
      print(ent)
    }

    vars <- tryCatch(redatam_variables(dic), error = function(e) e)
    if (inherits(vars, "error")) {
      notes <<- paste(notes, "variables_failed:", conditionMessage(vars))
    } else {
      variables_n <<- tryCatch(nrow(as.data.frame(vars)), error = function(e) length(vars))
      cat("Variables preview:\n")
      print(head(as.data.frame(vars), 30))
    }

    tryCatch(redatam_close(dic), error = function(e) NULL)
    TRUE
  }, error = function(e) {
    status <<- "open_failed"
    err <<- conditionMessage(e)
    FALSE
  })

  cat("STATUS:", status, "\n")
  if (nzchar(err)) cat("ERROR:", err, "\n")
  if (nzchar(notes)) cat("NOTES:", notes, "\n")
  cat("strings_has_text:", has_text, "\n")
  cat("strings_hits:", str_hits, "\n\n")

  simple_results <- rbind(
    simple_results,
    data.frame(
      path = p,
      file_name = basename(p),
      size_bytes = file.info(p)$size,
      status = status,
      object_class = object_class,
      entities_n = ifelse(is.na(entities_n), NA_integer_, entities_n),
      variables_n = ifelse(is.na(variables_n), NA_integer_, variables_n),
      error = err,
      notes = notes,
      strings_preview = substr(str_preview, 1, 500),
      strings_has_text = has_text,
      strings_hits = str_hits,
      stringsAsFactors = FALSE
    )
  )
}

sink()

write.csv(simple_results, csv_file, row.names = FALSE, fileEncoding = "UTF-8")

cat("Reporte creado:", report_file, "\n")
cat("CSV creado:", csv_file, "\n")
