import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure
from copy import deepcopy
import plotly.io as pio

# === Tema Plotly oscuro elegante (solo estilos; no cambia lógica) ===
pio.templates["ai_dark"] = deepcopy(pio.templates["plotly_dark"])  # type: ignore
pio.templates["ai_dark"].layout.update(  # type: ignore
    font=dict(family="Inter, system-ui, Segoe UI, Roboto, Arial", size=13),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#0f172a",
    margin=dict(l=40, r=30, t=60, b=40),
    xaxis=dict(gridcolor="rgba(255,255,255,.08)", zerolinecolor="rgba(255,255,255,.15)"),
    yaxis=dict(gridcolor="rgba(255,255,255,.08)", zerolinecolor="rgba(255,255,255,.15)"),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
    colorway=["#00d8d6", "#8b5cf6", "#f59e0b", "#22c55e", "#ef4444", "#14b8a6"]
)
px.defaults.template = "ai_dark"  # type: ignore
px.defaults.color_discrete_sequence = pio.templates["ai_dark"].layout.colorway  # type: ignore

# Configuración de página
st.set_page_config(
    page_title="AI Development Assistant",
    page_icon="🤖",
    layout="wide"
)

def cargar_css(file_name): # type: ignore
    """Lee un archivo CSS y lo inyecta en la página de Streamlit."""
    with open(file_name) as f: # type: ignore
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Llama a la función para cargar tu CSS
cargar_css("styles/style.css")


API_URL = "http://127.0.0.1:8000/api/v1"

# === Función de manejo de API centralizada ===
def handle_api_request(endpoint, data, success_message, language=None): # type: ignore
    """
    Maneja las solicitudes a la API, muestra un spinner y gestiona los estados de éxito/error.
    
    Parámetros:
    - endpoint (str): El endpoint de la API (ejemplo: "/generate-code").
    - data (dict): Los datos que se envían en el cuerpo de la solicitud.
    - success_message (str): El mensaje que se muestra en caso de éxito.
    - language (str, opcional): El lenguaje para mostrar el código en st.code.
    """
    full_url = f"{API_URL}{endpoint}"
    with st.spinner("Procesando..."):
        try:
            api_response = requests.post(full_url, json=data) # type: ignore
            
            if api_response.status_code == 200:
                response = api_response.json()
                st.success(success_message) # type: ignore
                
                # Dynamic content based on endpoint
                if endpoint == "/generate-code":
                    st.code(response["generated_code"], language=language) # type: ignore
                    st.markdown("---")
                    col_m1, col_m2, col_m3 = st.columns(3)
                    with col_m1: st.metric("Proveedor", response["provider_used"].upper())
                    with col_m2: st.metric("Tiempo", f"{response['execution_time']:.1f}s")
                    with col_m3: st.metric("Tokens", str(response["tokens_used"]))
                elif endpoint == "/review-code":
                    st.markdown(response["review"])
                elif endpoint == "/generate-tests":
                    st.code(response["tests"], language=language) # type: ignore
                
            else:
                st.error(f"Error en API: {api_response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error conectando con la API: {str(e)}")

# Sidebar para configuración
with st.sidebar:
    st.title("🤖 AI Dev Assistant")
    st.markdown("---")

    provider = st.selectbox(
        "Proveedor de IA:",
        ["OPENIA", "ANTHROPIC", "GOOGLE"]
    )

    language = st.selectbox(
        "Lenguaje:",
        ["Python", "Javascript", "Java", "C++"]
    )

# Título principal
st.title("🚀 Asistente de Desarrollo con IA")
st.markdown("Acelera tu desarrollo con herramientas de inteligencia artificial")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["💻 Generar Código", "🔍 Code Review", "🧪 Generar Tests", "📊 Analytics"])

# ---------------------------
# TAB 1: Generar Código
# ---------------------------
with tab1:
    st.header("Generación de Código")
    prompt = st.text_area("Describe qué código necesitas:", 
                          placeholder="Ej: Crea una función que valide emails usando regex", 
                          height=100)
    if st.button("🚀 Generar", type="primary"):
        if prompt:
            handle_api_request(
                endpoint="/generate-code",
                data={"prompt": prompt, "language": language, "provider": provider},
                success_message=f"✅ Código generado usando {provider.upper()}",
                language=language
            )
        else:
            st.warning("Por favor, ingresa una descripción del código.")

# ---------------------------
# TAB 2: Code Review
# ---------------------------
with tab2:
    st.header("Code Review Automático")
    code_input = st.text_area("Pega tu código aquí:", 
                              placeholder="Ej: def mi_funcion():\n    pass", 
                              height=200)
    if st.button("🔍 Revisar Código"):
        if code_input:
            handle_api_request(
                endpoint="/review-code",
                data={"code": code_input, "language": language},
                success_message="✅ Revisión de código completada"
            )
        else:
            st.warning("Por favor, ingresa código para revisar.")

# ---------------------------
# TAB 3: Generación de Tests
# ---------------------------
with tab3:
    st.header("Generación de Tests")
    code_for_tests = st.text_area("Código para generar tests:", 
                                  placeholder="Ingresa tu función o clase", 
                                  height=150)
    test_framework = st.selectbox("Framework de testing:", 
                                  ["pytest", "unittest", "nose2"])
    if st.button("🧪 Generar Tests"):
        if code_for_tests:
            handle_api_request(
                endpoint="/generate-tests",
                data={"code": code_for_tests, "framework": test_framework},
                success_message=f"✅ Tests generados con {test_framework}",
                language="python"
            )
        else:
            st.warning("Por favor, ingresa código para generar tests.")

# ---------------------------
# TAB 4: Analytics (no modificado)
# ---------------------------
with tab4:
    st.header("📊 Analytics de Uso")
    usage_data = pd.DataFrame({
        'Fecha': pd.date_range('2025-01-01', periods=30, freq='D'),
        'Código Generado': range(1, 31),
        'Reviews': [x * 0.8 for x in range(1, 31)],
        'Tests': [x * 0.6 for x in range(1, 31)]
    })
    col1, col2 = st.columns(2)
    with col1:
        fig_usage: Figure = px.line(  # type: ignore
            usage_data, x='Fecha',
            y=['Código Generado', 'Reviews', 'Tests'],
            title="Uso de Herramientas IA por Día"
        )
        st.plotly_chart(fig_usage, use_container_width=True)  # type: ignore
    with col2:
        provider_data = pd.DataFrame({
            'Proveedor': ['OpenAI', 'Anthropic', 'Google'],
            'Uso': [45, 35, 20]
        })
        fig_providers: Figure = px.pie(  # type: ignore
            provider_data, values='Uso', names='Proveedor',
            title="Distribución de Proveedores"
        )
        st.plotly_chart(fig_providers, use_container_width=True)  # type: ignore
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Requests", "1,247", "↗️ 23%")
    with col2:
        st.metric("Tiempo Promedio", "1.8s", "↘️ 0.2s")
    with col3:
        st.metric("Tokens Usados", "45.2K", "↗️ 15%")
    with col4:
        st.metric("Satisfacción", "4.8/5", "↗️ 0.1")

# Footer
st.markdown("---")
st.markdown("🤖 **AI Development Assistant** - Potenciado por múltiples proveedores de IA")