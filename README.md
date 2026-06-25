# NeuroOnco RAG

**Asistente inteligente de consulta clínica sobre gliomas difusos con mutación IDH**

---

## Contexto del proyecto

Los gliomas difusos de bajo grado con mutación en el gen IDH1/IDH2 representan uno de los desafíos más complejos de la neurooncología moderna. A diferencia de otros tumores, estas patologías afectan principalmente a adultos jóvenes de entre 30 y 45 años, en plena etapa productiva, y tienen un carácter progresivo e incurable con una supervivencia media de aproximadamente 10 años desde el diagnóstico.

El problema concreto que motivó este proyecto es la **dispersión del conocimiento clínico**: las guías de práctica clínica provienen de múltiples sociedades científicas (SEOM-GEINO en España, grupos de consenso en Chile, México y Europa), están publicadas en documentos extensos y en su mayoría en inglés, y actualizarse con todas ellas requiere horas de lectura y síntesis por parte del clínico.

**NeuroOnco RAG** nace para resolver ese problema: un sistema que permite consultar en lenguaje natural sobre diagnóstico, clasificación molecular, estratificación de riesgo, esquemas de tratamiento y seguimiento de gliomas IDH-mutados, obteniendo respuestas precisas, fundamentadas y con trazabilidad directa a las guías originales.

---

## ¿Cómo funciona?

NeuroOnco RAG implementa una arquitectura **RAG (Retrieval-Augmented Generation)**:

1. **Carga de documentos.** Los PDFs de las guías clínicas se procesan y dividen en fragmentos de texto mediante `RecursiveCharacterTextSplitter`.
2. **Vectorización semántica.** Cada fragmento se convierte en un embedding usando el modelo `paraphrase-multilingual-MiniLM-L12-v2`, que soporta español e inglés.
3. **Base vectorial.** Los embeddings se almacenan en ChromaDB para búsqueda semántica eficiente.
4. **Retrieval con MMR.** Ante cada consulta, se recuperan los fragmentos más relevantes y diversos usando Maximal Marginal Relevance (k=6, fetch_k=12, λ=0.6).
5. **Generación de respuesta.** El modelo `Llama 3.3 70B` (vía Groq) sintetiza una respuesta fundamentada exclusivamente en los fragmentos recuperados, citando fuente y página.

```
Consulta del profesional
        ↓
  Retriever MMR
  (ChromaDB + embeddings multilingüe)
        ↓
  Fragmentos de guías clínicas
        ↓
  Prompt especializado en neurooncología
        ↓
  Llama 3.3 70B (Groq)
        ↓
  Respuesta con cita de fuente y página
```

---

## ¿Para qué sirve?

NeuroOnco RAG está diseñado para **profesionales de la salud** (oncólogos médicos, neurocirujanos, neurólogos, médicos residentes) que necesitan:

- Consultar criterios diagnósticos y biomarcadores moleculares según la clasificación OMS 2021.
- Identificar la estratificación de riesgo (bajo vs. alto riesgo) de un paciente con glioma IDH-mutado.
- Conocer los esquemas de tratamiento recomendados (RT-PCV, temozolomida, vorasidenib) y sus indicaciones.
- Comparar recomendaciones entre distintas guías internacionales.
- Acceder rápidamente a información sobre seguimiento y criterios RANO de respuesta.

Cada respuesta incluye trazabilidad: fuente (nombre del documento) y página de la guía citada.

---

## Documentos de trabajo

El sistema trabaja sobre un corpus de **8 guías clínicas y documentos de consenso** en español (o bilingüe), todos open access:

| # | Documento | Institución | Año |
|---|-----------|-------------|-----|
| 1 | Guía SEOM-GEINO para gliomas de grado 2 | Sociedad Española de Oncología Médica + GEINO | 2023 |
| 2 | Guía SEOM-GEINO para gliomas de alto grado | SEOM + GEINO | 2022 |
| 3 | Consenso Chileno para diagnóstico y tratamiento de gliomas del adulto | SONEPSYN + sociedades chilenas | 2022 |
| 4 | Primera guía de consenso mexicana para gliomas de bajo grado IDH-mutado | Academia Mexicana de Neurología | 2025 |
| 5 | Informe SEOM de evaluación del vorasidenib (inhibidor IDH) | SEOM | 2024 |
| 6 | Perspectivas para el abordaje integral del glioma de bajo grado con mutación IDH | GEINO + SEN + SENEC + SEOR + SEAP-IAP | 2025 |
| 7 | Guía de Tumores del Sistema Nervioso Central | AAOC (Asociación Argentina de Oncología Clínica) | 2026 |
| 8 | Vorasidenib in IDH1- or IDH2-Mutant Low-Grade Glioma (INDIGO trial) | Mellinghoff et al. — New England Journal of Medicine | 2023 |

Los documentos cubren: clasificación OMS 2021, diagnóstico molecular (IDH1/2, 1p/19q, ATRX, CDKN2A/B, MGMT), cirugía (resección máxima segura), radioterapia (RT), quimioterapia (PCV, temozolomida), inhibidores IDH (vorasidenib), criterios RANO, seguimiento por imágenes y cuidados de soporte.

---

## ¿Quién lo desarrolló?

**Gabriel Marquez**  
Estudiante de Tecnicatura Superior en Ciencias de Datos e Inteligencia Artificial  
Instituto de Formación Técnico Superior N°24 (IFTS N°24)  
Buenos Aires, Argentina  
Año: 2026

---

## Contexto académico

Proyecto final desarrollado para la materia **Procesamiento de Lenguaje Natural** de la Tecnicatura Superior en Ciencias de Datos e Inteligencia Artificial del IFTS N°24.

El proyecto surge de una necesidad real identificada en el campo de la neurooncología: la falta de herramientas accesibles que permitan a los profesionales de la salud consultar en lenguaje natural sobre guías clínicas actualizadas de gliomas IDH-mutados, integrando recomendaciones de múltiples sociedades científicas de habla hispana.

---

## Stack tecnológico

| Componente | Tecnología |
|---|---|
| Framework RAG | LangChain |
| LLM | Llama 3.3 70B vía Groq |
| Embeddings | paraphrase-multilingual-MiniLM-L12-v2 |
| Base vectorial | ChromaDB |
| Retriever | MMR (k=6, fetch_k=12, λ=0.6) |
| Interfaz | Streamlit |
| Deploy | Hugging Face Spaces |

---

## Demo

La aplicación está disponible públicamente en Hugging Face Spaces:

🔗 **[https://huggingface.co/spaces/GaboRTX/neurooncolog-rag](https://huggingface.co/spaces/GaboRTX/neurooncolog-rag)**

---

## Estructura del proyecto

```
proyecto_final_rag_GM/
├── app.py                    # Interfaz Streamlit
├── rag_system.py             # Pipeline RAG principal
├── conf.py                   # Configuración de modelos y retriever
├── prompts.py                # Prompt especializado en neurooncología
├── create_vectorstore.py     # Script para crear la base vectorial
├── requirements.txt          # Dependencias del proyecto
├── .gitignore
├── README.md
└── guias_neurooncologia/     # PDFs de las guías clínicas
    ├── 01_consenso_chileno_gliomas_adulto_2022.pdf
    ├── 02_seom_geino_gliomas_grado2_2023.pdf
    ├── 03_seom_geino_gliomas_alto_grado_2022.pdf
    ├── 04_guia_mexicana_gliomas_idh_mutado_2025.pdf
    ├── 05_seom_informe_vorasidenib_idh_2024.pdf
    ├── 06_consenso_multidisciplinar_idh_espana_2025.pdf
    ├── 07_Tumores SNC, 2026; publicada AAOC.pdf
    └── 08_Vorasidenib in IDH1- or IDH2-Mutant Low-Grade Glioma 2023.pdf
```

La carpeta `chroma_db/` (base vectorial generada) y el archivo `.env` (variables de entorno con la API key de Groq) **no se incluyen en el repositorio**. Se generan localmente o se configuran como secrets en Hugging Face.

---

## Instalacion local

```bash
# 1. Clonar el repositorio
git clone https://github.com/GaboRTX/proyecto_final_rag_GM.git
cd proyecto_final_rag_GM

# 2. Crear entorno virtual e instalar dependencias
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt

# 3. Configurar variables de entorno
# Crear archivo .env con:
# GROQ_API_KEY=tu_api_key_de_groq

# 4. Crear la base vectorial a partir de los PDFs
python create_vectorstore.py

# 5. Correr la aplicación
streamlit run app.py
```

### Obtener la API key de Groq
1. Registrarse gratis en [console.groq.com](https://console.groq.com)
2. Crear una API key en el panel
3. Pegarla en el archivo `.env`

---

## Deploy en Hugging Face Spaces

1. Crear una cuenta en [huggingface.co](https://huggingface.co)
2. Crear un nuevo Space → tipo **Streamlit**
3. Subir todos los archivos del proyecto (incluyendo la carpeta `guias_neurooncologia/`)
4. En **Settings → Variables and secrets**, agregar:
   - `GROQ_API_KEY` = tu api key de Groq
5. El Space ejecutará automáticamente `create_vectorstore.py` si está configurado, o podés incluir la `chroma_db/` pre-generada

---

*NeuroOnco RAG · Porque el conocimiento clínico sobre gliomas IDH-mutados no debería estar atrapado en PDFs dispersos.*
