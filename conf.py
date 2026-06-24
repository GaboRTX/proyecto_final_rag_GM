import os

# -------------------------------------------------------------------
# MODELOS
# -------------------------------------------------------------------
GENERATION_MODEL = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# -------------------------------------------------------------------
# RUTAS (relativas a la raíz del proyecto)
# -------------------------------------------------------------------
CARPETA_CHROMA = "chroma_db"
CARPETA_DOCUMENTOS = "guias_neurooncologia"

# -------------------------------------------------------------------
# CONFIGURACIÓN DEL RETRIEVER
# -------------------------------------------------------------------

# Tipo de búsqueda: mmr = Maximal Marginal Relevance
SEARCH_TYPE = "mmr"

# Cantidad de chunks que se pasan al LLM para generar la respuesta
SEARCH_K = 6

# Controla el balance entre relevancia y diversidad en MMR
# 1.0 = máxima relevancia, 0.0 = máxima diversidad
MMR_DIVERSITY_LAMBDA = 0.6

# Cantidad de candidatos que MMR evalúa antes de seleccionar los SEARCH_K finales
MMR_FETCH_K = 12
