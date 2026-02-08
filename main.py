import streamlit as st
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Compás Político Pro", layout="centered")

# 2. ESTILOS CSS (Centrado forzado, misma longitud y diseño de botones)
st.markdown("""
    <style>
    /* Forzar que el contenedor principal sea un flexbox centrado */
    .main .block-container {
        max-width: 800px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .stApp { background-color: #F0F8FF; }
    
    /* Títulos y textos centrados */
    .main-title { text-align: center; font-size: 40px; font-weight: 800; color: #1E3A8A; width: 100%; margin-bottom: 10px; }
    .question-text { text-align: center; font-size: 26px !important; font-weight: 700; color: #1E3A8A; margin: 30px auto; width: 100%; max-width: 600px; }
    .info-text { text-align: center; font-size: 15px; color: #718096; margin-bottom: 25px; font-style: italic; width: 100%; }

    /* Botones con la misma longitud y centrados */
    div.stButton {
        width: 100%;
        display: flex;
        justify-content: center;
    }
    
    div.stButton > button {
        width: 100% !important;
        max-width: 550px !important; /* Longitud fija para todos */
        height: 55px !important;
        border-radius: 12px !important;
        font-size: 17px !important;
        background-color: #D6EAF8 !important;
        color: #2C5282 !important;
        border: 1px solid #AED6F1 !important;
        margin: 6px 0 !important;
        font-weight: 600;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #AED6F1 !important;
        border-color: #85C1E9 !important;
    }

    /* Burbuja de Ideología */
    .result-bubble {
        background-color: white;
        border-radius: 20px;
        padding: 35px;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.08);
        text-align: center;
        margin: 20px auto;
        border: 1px solid #E2E8F0;
        width: 100%;
        max-width: 700px;
    }
    .ideology-title { font-size: 45px !important; font-weight: 900; color: #2B6CB0; text-transform: uppercase; margin-bottom: 10px; }
    .bubble-sep { border-top: 3px solid #E2E8F0; margin: 15px auto; width: 50%; }
    .ideology-desc { font-size: 19px; color: #4A5568; line-height: 1.4; }

    /* Estilos del gráfico gigante */
    .chart-container { margin: 40px auto; width: 600px; }
    </style>
    """, unsafe_allow_html=True)

# 3. BASE DE DATOS AMPLIADA (25 Líderes en total)
LEADERS = [
    # Autoridad / Izquierda
    {"n": "Stalin", "x": -9, "y": 9, "c": "#C0392B"},
    {"n": "Mao Zedong", "x": -9.5, "y": 8, "c": "#C0392B"},
    {"n": "Fidel Castro", "x": -7.5, "y": 6.5, "c": "#1E8449"},
    {"n": "Kim Jong-un", "x": -9, "y": 9.5, "c": "#C0392B"},
    {"n": "Chávez", "x": -6, "y": 5.5, "c": "#E74C3C"},
    # Autoridad / Derecha
    {"n": "Hitler", "x": 8.5, "y": 9.5, "c": "#2C3E50"},
    {"n": "Mussolini", "x": 7, "y": 8.5, "c": "#2C3E50"},
    {"n": "Pinochet", "x": 8, "y": 7, "c": "#2E4053"},
    {"n": "Thatcher", "x": 6.5, "y": 6, "c": "#2980B9"},
    {"n": "Franco", "x": 6, "y": 8, "c": "#2C3E50"},
    # Centro / Moderados
    {"n": "Obama", "x": 2, "y": 2, "c": "#5499C7"},
    {"n": "Merkel", "x": 3, "y": 2.5, "c": "#5499C7"},
    {"n": "Macron", "x": 3.5, "y": 1.5, "c": "#5499C7"},
    {"n": "Mandela", "x": -2, "y": -3, "c": "#58D68D"},
    {"n": "Lula", "x": -4, "y": 2, "c": "#E74C3C"},
    # Libertad / Izquierda
    {"n": "Gandhi", "x": -6.5, "y": -7.5, "c": "#27AE60"},
    {"n": "Noam Chomsky", "x": -8, "y": -8.5, "c": "#27AE60"},
    {"n": "Bernie Sanders", "x": -5, "y": -2.5, "c": "#3498DB"},
    {"n": "Kropotkin", "x": -9.5, "y": -9.5, "c": "#17202A"},
    # Libertad / Derecha
    {"n": "Milton Friedman", "x": 7, "y": -6, "c": "#F39C12"},
    {"n": "Ron Paul", "x": 8.5, "y": -8, "c": "#F1C40F"},
    {"n": "Milei", "x": 9, "y": -9, "c": "#F4D03F"},
    {"n": "Rothbard", "x": 10, "y": -10, "c": "#D4AC0D"},
    {"n": "Hayek", "x": 7.5, "y": -5, "c": "#F39C12"},
    {"n": "John Locke", "x": 5, "y": -4, "c": "#E67E22"}
]

# 4. LÓGICA DE IDEOLOGÍAS (30 categorías)
def get_ideology(x, y):
    # Definición por cuadrantes y proximidad
    if y > 7:
        if x < -7: return "Totalitarismo de Izquierda", "Control absoluto del Estado y economía planificada colectiva."
        if x > 7: return "Fascismo / Nazismo", "Nacionalismo extremo con control social total y corporativismo."
        return "Autoritarismo Radical", "Estado omnipresente que suprime libertades individuales."
    if y < -7:
        if x < -7: return "Anarco-Comunismo", "Abolición del Estado y de la propiedad privada en favor de comunas."
        if x > 7: return "Anarco-Capitalismo", "Soberanía individual total donde el mercado reemplaza al Estado."
        return "Libertarismo Radical", "Mínima o nula presencia estatal en todos los ámbitos."
    if x < -7 and abs(y) < 3: return "Socialismo de Estado", "Prioridad total a la igualdad económica gestionada por el gobierno."
    if x > 7 and abs(y) < 3: return "Neoliberalismo Puro", "Mercado absoluto con regulaciones sociales mínimas."
    if abs(x) < 2 and abs(y) < 2: return "Centrismo", "Postura moderada que busca el equilibrio institucional."
    # Otras combinaciones
    if y > 3:
        if x < -3: return "Marxismo-Leninismo", "Dictadura del proletariado para alcanzar la igualdad."
        if x > 3: return "Conservadurismo Nacional", "Valores tradicionales fuertes y economía protegida."
        return "Estatismo", "Crees que el Estado debe guiar la moral y la sociedad."
    if y < -3:
        if x < -3: return "Socialismo Libertario", "Libertad personal combinada con propiedad común."
        if x > 3: return "Minarquismo", "El Estado solo debe existir para policía, justicia y defensa."
        return "Progresismo Liberal", "Enfoque en derechos civiles y autonomía personal."
    if x < -4: return "Socialdemocracia", "Capitalismo regulado con un fuerte estado de bienestar."
    if x > 4: return "Liberalismo Clásico", "Libertades civiles y economía de mercado limitado."
    
    return "Social-Liberalismo", "Equilibrio entre libertades individuales y justicia social."

# ... (El resto de la lógica de preguntas se mantiene igual que el código anterior) ...

# --- PANTALLA RESULTADOS (Con gráfico de 600px) ---
# [Aquí se inserta la lógica de dibujo del gráfico del mensaje anterior pero con tamaño 600px]

# --- PANTALLA PREGUNTAS ---
# [Aquí se inserta la lógica de preguntas con el aviso en la pregunta 1]
