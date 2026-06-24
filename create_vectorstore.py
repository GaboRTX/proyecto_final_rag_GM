from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from conf import CARPETA_DOCUMENTOS, CARPETA_CHROMA, EMBEDDING_MODEL

print("Cargando guías clínicas desde la carpeta...")
loader = PyPDFDirectoryLoader(CARPETA_DOCUMENTOS)
documentos = loader.load()
print(f"Se cargaron {len(documentos)} páginas de guías clínicas.")

# DIVIDIR EN CHUNKS
# Guías clínicas de 10 a 15 páginas — chunks medianos para no perder contexto clínico
# chunk_overlap=300 para mantener continuidad entre fragmentos de criterios y recomendaciones
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=300
)

docs_split = text_splitter.split_documents(documentos)
print(f"Se crearon {len(docs_split)} chunks de texto.")

# CREAR EMBEDDINGS
print("Cargando modelo de embeddings multilingüe...")
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)
print("Modelo de embeddings listo.")

# CREAR Y PERSISTIR EL VECTOR STORE
print("Creando base de datos vectorial Chroma...")
vectorstore = Chroma.from_documents(
    docs_split,
    embedding=embeddings,
    persist_directory=CARPETA_CHROMA
)
print(f"Base de datos creada y guardada en: {CARPETA_CHROMA}")
print("Sistema listo para consultas.")
