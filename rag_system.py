from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from dotenv import load_dotenv

from conf import *
from prompts import *

load_dotenv()

# -------------------------------------------------------------------
# INICIALIZACIÓN DEL SISTEMA RAG
# -------------------------------------------------------------------

@st.cache_resource
def initialize_rag_system():
    """
    Arma y devuelve la cadena RAG completa lista para usar.
    El decorador @st.cache_resource hace que Streamlit la inicialice
    una sola vez y la reutilice en cada consulta — sin esto,
    el sistema recargaría el modelo de embeddings en cada pregunta.
    """

    # Cargamos el mismo modelo de embeddings que usamos al crear el vector store
    # Es CRÍTICO usar el mismo modelo, de lo contrario las búsquedas no funcionarán
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    # Conectamos con la base de datos Chroma ya creada
    # No creamos nada nuevo, solo abrimos lo que ya existe en disco
    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory=CARPETA_CHROMA
    )

    # LLM para generar la respuesta final al usuario
    llm_generation = ChatGroq(
        model=GENERATION_MODEL,
        temperature=0
    )

    # Retriever con MMR (Maximal Marginal Relevance)
    # MMR busca documentos relevantes pero diversos entre sí
    # Evita traer chunks que dicen exactamente lo mismo de la misma guía
    retriever = vectorstore.as_retriever(
        search_type=SEARCH_TYPE,
        search_kwargs={
            "k": SEARCH_K,
            "lambda_mult": MMR_DIVERSITY_LAMBDA,
            "fetch_k": MMR_FETCH_K
        }
    )

    # Función que formatea los chunks recuperados antes de mandárselos al LLM
    # Le agrega encabezados con fuente y página para que el modelo sepa
    # de qué guía clínica proviene cada fragmento
    def format_docs(docs):
        formatted = []
        for doc in docs:
            fuente = doc.metadata.get("source", "No especificada")
            fuente = fuente.split("\\")[-1].split("/")[-1]
            pagina = doc.metadata.get("page", "No especificada")
            header = f"Fuente: {fuente} - Página: {pagina}"
            content = doc.page_content.strip()
            formatted.append(f"{header}\n{content}")
        return "\n\n".join(formatted)

    # Armamos el prompt de respuesta
    prompt = PromptTemplate.from_template(RAG_TEMPLATE)

    # Cadena RAG completa
    # 1. La pregunta entra al retriever que busca los chunks relevantes
    # 2. Los chunks se formatean con format_docs
    # 3. El prompt combina contexto + pregunta
    # 4. El LLM genera la respuesta
    # 5. StrOutputParser convierte la respuesta a texto plano
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm_generation
        | StrOutputParser()
    )

    return rag_chain, retriever


# -------------------------------------------------------------------
# FUNCIÓN PRINCIPAL DE CONSULTA
# -------------------------------------------------------------------

def query_rag(question: str) -> tuple[str, list]:
    """
    Recibe una pregunta clínica, la procesa con la cadena RAG
    y devuelve la respuesta + los fragmentos de guías usados.
    """
    try:
        rag_chain, retriever = initialize_rag_system()

        # Generamos la respuesta
        response = rag_chain.invoke(question)

        # Recuperamos los documentos para mostrarlos en la UI
        docs = retriever.invoke(question)

        docs_info = []
        for i, doc in enumerate(docs[:SEARCH_K], 1):
            fuente = doc.metadata.get("source", "No especificada")
            fuente = fuente.split("\\")[-1].split("/")[-1]
            docs_info.append({
                "fragmento": i,
                "contenido": doc.page_content[:800] + "..." if len(doc.page_content) > 800 else doc.page_content,
                "fuente": fuente,
                "pagina": doc.metadata.get("page", "No especificada")
            })

        return response, docs_info

    except Exception as e:
        return f"Error al procesar la consulta: {str(e)}", []
