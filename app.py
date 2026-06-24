import streamlit as st
from rag_system import query_rag


def main():
    st.set_page_config(
        page_title="NeuroOnco RAG",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # ── Estilos globales ─────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0a0f1e;
        color: #e2e8f0;
    }

    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; }

    .app-header {
        text-align: center;
        padding: 2rem 0 1.4rem 0;
        border-bottom: 1px solid #1e2d4a;
        margin-bottom: 1.5rem;
    }
    .app-header h1 {
        font-size: 2rem;
        color: #e2e8f0;
        letter-spacing: -0.5px;
        margin-bottom: 0.3rem;
    }
    .app-header .subtitle {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 300;
    }
    .app-header .badge {
        display: inline-block;
        background: #0f2a4a;
        border: 1px solid #1e4a7a;
        color: #38bdf8;
        font-size: 0.72rem;
        font-weight: 500;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        margin-top: 0.5rem;
    }
    [data-testid="collapsedControl"] { display: none; }

    /* Mensajes del chat */
    .msg-user {
        background: #111827;
        border: 1px solid #1e2d4a;
        border-radius: 10px 10px 2px 10px;
        padding: 0.9rem 1.2rem;
        margin: 0.6rem 0;
        margin-left: 15%;
        color: #e2e8f0;
        line-height: 1.6;
    }
    .msg-assistant {
        background: #0d1829;
        border: 1px solid #1e2d4a;
        border-left: 3px solid #38bdf8;
        border-radius: 2px 10px 10px 10px;
        padding: 0.9rem 1.2rem;
        margin: 0.6rem 0;
        margin-right: 5%;
        color: #e2e8f0;
        line-height: 1.7;
    }
    .msg-label {
        font-size: 0.68rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
        font-weight: 500;
    }
    .msg-label-user      { color: #64748b; text-align: right; }
    .msg-label-assistant { color: #38bdf8; }

    /* Fragmentos de guías */
    .fragmento-card {
        background: #080e1c;
        border: 1px solid #1e2d4a;
        border-radius: 8px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.8rem;
        font-size: 0.82rem;
    }
    .fragmento-header {
        font-size: 0.68rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #38bdf8;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    .fragmento-meta {
        color: #64748b;
        font-size: 0.75rem;
        margin-bottom: 0.5rem;
    }
    .fragmento-content {
        color: #94a3b8;
        line-height: 1.6;
    }

    /* Estado vacío */
    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        color: #64748b;
    }
    .empty-state-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1rem; }
    </style>
    """, unsafe_allow_html=True)

    # ── Header ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="app-header">
        <h1>🧠 NeuroOnco RAG</h1>
        <div class="subtitle">Consulta inteligente sobre guías clínicas de gliomas IDH-mutados</div>
        <div class="badge">6 guías clínicas · SEOM · GEINO · Consenso Chile · México · España</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Inicializar historial ─────────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ── Layout principal ──────────────────────────────────────────────
    col_chat, col_docs = st.columns([2, 1], gap="large")

    with col_chat:
        st.markdown("#### Consulta clínica")

        # Estado vacío con ejemplos
        if not st.session_state.messages:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🧠</div>
                <div>Realizá tu primera consulta sobre las guías clínicas cargadas.</div>
                <div style="font-size:0.82rem; margin-top:0.8rem; color:#475569;">
                    Ejemplos de consultas:
                </div>
                <div style="font-size:0.8rem; margin-top:0.5rem; color:#334155; text-align:left; max-width:400px; margin-left:auto; margin-right:auto;">
                    • ¿Cuál es el tratamiento de primera línea para gliomas grado 2 IDH-mutado de alto riesgo?<br><br>
                    • ¿Qué biomarcadores moleculares son clave para clasificar un glioma difuso según la OMS 2021?<br><br>
                    • ¿Cuál es el rol del vorasidenib en gliomas con mutación IDH?<br><br>
                    • ¿Cómo se define un paciente de bajo riesgo según la SEOM-GEINO 2023?
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Historial de mensajes
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="msg-label msg-label-user">Consulta</div>
                <div class="msg-user">{message["content"]}</div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="msg-label msg-label-assistant">Asistente neurooncológico</div>
                <div class="msg-assistant">{message["content"]}</div>
                """, unsafe_allow_html=True)

        # Input del usuario
        if prompt := st.chat_input("Consultá sobre diagnóstico, clasificación OMS 2021, tratamiento o seguimiento..."):
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.spinner("Consultando guías clínicas..."):
                response, docs = query_rag(prompt)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "docs": docs
                })

            st.rerun()

    with col_docs:
        st.markdown("#### Fuentes recuperadas")

        # Mostrar fragmentos del último mensaje del asistente
        last_assistant = next(
            (m for m in reversed(st.session_state.messages) if m["role"] == "assistant"),
            None
        )

        if last_assistant and "docs" in last_assistant and last_assistant["docs"]:
            for doc in last_assistant["docs"]:
                st.markdown(f"""
                <div class="fragmento-card">
                    <div class="fragmento-header">Fragmento {doc['fragmento']}</div>
                    <div class="fragmento-meta">
                        📄 {doc['fuente']} &nbsp;|&nbsp; Pág. {doc['pagina']}
                    </div>
                    <div class="fragmento-content">{doc['contenido']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="padding:2rem 0; color:#64748b; font-size:0.85rem;">
                Los fragmentos de las guías clínicas aparecen aquí después de cada consulta.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#1e2d4a; font-size:0.75rem;'>NeuroOnco RAG · Proyecto Final PLN · IFTS N°24 · 2026 · Gabriel Marquez</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
