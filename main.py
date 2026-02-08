import streamlit as st
import base64

# 1. ESTÉTICA DEFINITIVA Y CONTROL DE COLORES
st.set_page_config(page_title="Brújula Política Estudiantil", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    
    .question-text {
        text-align: center;
        font-size: 38px !important; 
        font-weight: 800;
        color: #0D47A1;
        margin: 40px 0px 60px 0px;
        line-height: 1.1;
    }

    /* CONTENEDOR DE BOTONES: Centrado con ligero desplazamiento a la derecha */
    div.stButton {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-left: 20px; /* Desplazamiento ligero a la derecha */
    }

    div.stButton > button {
        width: 620px !important; 
        height: 70px !important;
        border-radius: 35px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border: none !important;
        margin: 8px 0px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        transition: 0.3s;
    }

    /* COLORES ESPECÍFICOS POR POSICIÓN (Basado en el orden de renderizado) */
    /* 1. Totalmente de acuerdo - Verde Oscuro */
    div[data-testid="stVerticalBlock"] > div:nth-child(3) div.stButton button { background-color: #1B5E20 !important; color: white !important; }
    /* 2. De acuerdo - Verde Claro */
    div[data-testid="stVerticalBlock"] > div:nth-child(4) div.stButton button { background-color: #81C784 !important; color: #052b08 !important; }
    /* 3. Neutral - Blanco */
    div[data-testid="stVerticalBlock"] > div:nth-child(5) div.stButton button { background-color: #FFFFFF !important; color: #1565C0 !important; border: 2px solid #BBDEFB !important; }
    /* 4. En desacuerdo - Rojo Claro */
    div[data-testid="stVerticalBlock"] > div:nth-child(6) div.stButton button { background-color: #EF9A9A !important; color: #7f0000 !important; }
    /* 5. Totalmente en desacuerdo - Rojo Oscuro */
    div[data-testid="stVerticalBlock"] > div:nth-child(7) div.stButton button { background-color: #B71C1C !important; color: white !important; }

    /* Botón Volver / Reiniciar / Imprimir */
    div[data-testid="stVerticalBlock"] > div:nth-child(8) div.stButton button,
    .print-btn button { 
        background-color: #546E7A !important; 
        color: white !important; 
        width: 300px !important;
        margin-top: 30px !important;
    }

    div.stButton > button:hover { transform: scale(1.02); filter: brightness(1.1); }

    .result-card {
        background-color: white; padding: 40px; border-radius: 30px;
        text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border: 6px solid #1976D2;
    }
    .map-container {
        position: relative; width: 450px; height: 450px; 
        margin: 30px auto; border: 10px solid white; border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2); overflow: hidden;
    }
    .dot { position: absolute; border-radius: 50%; border: 2px solid white; transform: translate(-50%, -50%); }
    .user-dot {
        width: 40px; height: 40px; background-color: #FF1744; z-index: 100;
        box-shadow: 0 0 20px #FF1744; border: 4px solid white; color: white;
        display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})

def responder(puntos):
    q = questions[st.session_state.idx]
    val = puntos * 18.0 * q["v"] 
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    st.session_state.idx += 1

LEADERS = [
    {"n": "Milei", "x": 175, "y": -165, "c": "#FFD600"},
    {"n": "Stalin", "x": -195, "y": 195, "c": "#D32F2F"},
    {"n": "Hitler", "x": 185, "y": 198, "c": "#37474F"},
    {"n": "Mao", "x": -198, "y": 180, "c": "#F44336"},
    {"n": "Gandhi", "x": -140, "y": -175, "c": "#4CAF50"},
    {"n": "Rothbard", "x": 195, "y": -198, "c": "#FF9800"},
    {"n": "Thatcher", "x": 155, "y": 120, "c": "#1976D2"},
    {"n": "Castro", "x": -170, "y": 150, "c": "#2E7D32"}
]

# 3. PREGUNTAS (85)
questions = [
    {"t": "Cualquier persona debería poder abrir un negocio sin que el gobierno le ponga muchas reglas.", "a": "x", "v": 1},
    {"t": "Los hospitales deberían ser siempre gratis y pagados con nuestros impuestos.", "a": "x", "v": -1},
    {"t": "El gobierno debería poner un límite al precio del alquiler de los pisos.", "a": "x", "v": -1},
    {"t": "Es mejor que la electricidad sea vendida por empresas privadas que por el gobierno.", "a": "x", "v": 1},
    {"t": "La gente que tiene mucho dinero debería pagar muchísimos más impuestos que el resto.", "a": "x", "v": -1},
    {"t": "Es mejor comprar productos fabricados aquí que traerlos de otros países.", "a": "x", "v": -1},
    {"t": "No debería existir un sueldo mínimo; cada uno debería pactar lo que cobra.", "a": "x", "v": 1},
    {"t": "Cuidar el planeta es más importante que ganar mucho dinero como país.", "a": "x", "v": -1},
    {"t": "El gobierno no debería dar dinero (ayudas) a ninguna empresa privada.", "a": "x", "v": 1},
    {"t": "Si mis padres mueren, todo su dinero debería ser mío sin pagar impuestos.", "a": "x", "v": 1},
    {"t": "Ir a la universidad debería ser totalmente gratis para todo el mundo.", "a": "x", "v": -1},
    {"t": "Si las empresas compiten entre ellas, los servicios serán mejores.", "a": "x", "v": 1},
    {"t": "El gobierno debe asegurar que todo el mundo tenga un trabajo.", "a": "x", "v": -1},
    {"t": "Nadie tiene derecho a quitarle nada a una persona si es su propiedad privada.", "a": "x", "v": 1},
    {"t": "Los bancos centrales (que fabrican el dinero) deberían desaparecer.", "a": "x", "v": 1},
    {"t": "El agua y la luz deberían estar siempre en manos del gobierno.", "a": "x", "v": -1},
    {"t": "Comprar y vender cosas con todo el mundo ayuda a que haya menos pobreza.", "a": "x", "v": 1},
    {"t": "Debería estar prohibido ganar dinero solo apostando en la bolsa.", "a": "x", "v": -1},
    {"t": "Que el gobierno gaste mucho dinero es lo que crea las crisis.", "a": "x", "v": 1},
    {"t": "Las personas ayudan mejor a los pobres que el gobierno.", "a": "x", "v": 1},
    {"t": "Los países que no cobran impuestos a las empresas son algo justo.", "a": "x", "v": 1},
    {"t": "El gobierno debe ayudar con dinero a las empresas grandes si van a cerrar.", "a": "x", "v": -1},
    {"t": "Para que un país vaya bien, hay que gastar menos de lo que se gana.", "a": "x", "v": 1},
    {"t": "Es normal que haya gente rica y pobre; eso hace que la gente se esfuerce.", "a": "x", "v": 1},
    {"t": "Los sindicatos de trabajadores tienen demasiado poder hoy en día.", "a": "x", "v": 1},
    {"t": "El dinero debería valer por el oro que tenga el país.", "a": "x", "v": 1},
    {"t": "Como las máquinas harán los trabajos, el gobierno debería darnos un sueldo a todos.", "a": "x", "v": -1},
    {"t": "Las medicinas no deberían tener dueño ni patentes privadas.", "a": "x", "v": -1},
    {"t": "Comprar muchas cosas es bueno para que la economía funcione.", "a": "x", "v": 1},
    {"t": "Por ley, nadie debería trabajar más de 30 horas a la semana.", "a": "x", "v": -1},
    {"t": "Obedecer a la autoridad es lo más importante que debe aprender un niño.", "a": "y", "v": 1},
    {"t": "Cualquier mujer debería poder decidir si quiere abortar gratis.", "a": "y", "v": -1},
    {"t": "La religión no debería influir en las leyes del país.", "a": "y", "v": -1},
    {"t": "Hace falta un líder fuerte que mande con mano dura para poner orden.", "a": "y", "v": 1},
    {"t": "Cada uno debería poder drogarse si quiere, es su propia vida.", "a": "y", "v": -1},
    {"t": "Los criminales peligrosos no deberían salir nunca de la cárcel.", "a": "y", "v": 1},
    {"t": "El ejército debería vigilar las fronteras para que nadie entre sin permiso.", "a": "y", "v": 1},
    {"t": "La lucha de las mujeres por la igualdad es totalmente justa.", "a": "y", "v": -1},
    {"t": "El gobierno puede espiarnos para evitar ataques terroristas.", "a": "y", "v": 1},
    {"t": "Cada uno puede decir lo que quiera, aunque alguien se sienta insultado.", "a": "y", "v": -1},
    {"t": "Si alguien muy enfermo quiere morir, el médico debería poder ayudarle.", "a": "y", "v": -1},
    {"t": "Todos los jóvenes deberían hacer el servicio militar obligatorio.", "a": "y", "v": 1},
    {"t": "La familia tradicional es la mejor base para la sociedad.", "a": "y", "v": 1},
    {"t": "Ver películas para adultos (porno) debería estar prohibido por ley.", "a": "y", "v": 1},
    {"t": "Nadie debería prohibir una obra de arte, aunque sea ofensiva.", "a": "y", "v": -1},
    {"t": "La pena de muerte está bien para los peores criminales.", "a": "y", "v": 1},
    {"t": "Que venga mucha gente de fuera hace que nuestra cultura se pierda.", "a": "y", "v": 1},
    {"t": "El matrimonio solo debería ser entre un hombre y una mujer.", "a": "y", "v": 1},
    {"t": "Debería estar prohibido cortar calles para hacer manifestaciones.", "a": "y", "v": 1},
    {"t": "Uno no nace hombre o mujer, sino que elige lo que quiere ser.", "a": "y", "v": -1},
    {"t": "La monarquía (reyes) es algo antiguo que ya no debería existir.", "a": "y", "v": -1},
    {"t": "La policía necesita mucho más poder del que tiene ahora.", "a": "y", "v": 1},
    {"t": "Aprender sobre sexo en el colegio es fundamental para los niños.", "a": "y", "v": -1},
    {"t": "Insultar a la religión no debería ser un delito.", "a": "y", "v": -1},
    {"t": "La bandera de nuestro país es algo sagrado.", "a": "y", "v": 1},
    {"t": "Los científicos deberían poder clonar humanos para curar enfermedades.", "a": "y", "v": -1},
    {"t": "Hoy en día hay demasiada piel fina; se puede decir muy poco sin ofender.", "a": "y", "v": 1},
    {"t": "Mezclar muchas culturas en el mismo barrio no funciona bien.", "a": "y", "v": 1},
    {"t": "Es necesario probar medicinas con animales para salvar humanos.", "a": "y", "v": 1},
    {"t": "El gobierno debería pagar dinero a las familias por tener hijos.", "a": "y", "v": 1},
    {"t": "Bajarse películas sin pagar no es un crimen de verdad.", "a": "y", "v": -1},
    {"t": "En el colegio debería haber mucha más disciplina y respeto.", "a": "y", "v": 1},
    {"t": "El gobierno debe controlar la IA antes de que sea tarde.", "a": "y", "v": 1},
    {"t": "La energía nuclear es la mejor solución para el clima.", "a": "x", "v": 1},
    {"t": "Los animales deberían tener los mismos derechos que las personas.", "a": "y", "v": -1},
    {"t": "Llegar al espacio deberían hacerlo empresas privadas.", "a": "x", "v": 1},
    {"t": "Dar dinero público para el cine o el teatro es malgastar impuestos.", "a": "x", "v": 1},
    {"t": "La globalización está destruyendo nuestras costumbres locales.", "a": "y", "v": 1},
    {"t": "El capitalismo está rompiendo el planeta.", "a": "x", "v": -1},
    {"t": "Deberíamos poder votar todas las leyes por internet.", "a": "y", "v": -1},
    {"t": "La cárcel debe ser un castigo duro, no un sitio para aprender.", "a": "y", "v": 1},
    {"t": "Si eres rico es porque te has esforzado más.", "a": "x", "v": 1},
    {"t": "Internet debería ser gratis para todo el mundo.", "a": "x", "v": -1},
    {"t": "Debería haber clases de religión obligatorias.", "a": "y", "v": 1},
    {"t": "Nuestro ejército debería ir a otros países a ayudar si hay guerras.", "a": "y", "v": 1},
    {"t": "Las criptomonedas son el futuro de la libertad.", "a": "x", "v": 1},
    {"t": "Es justo que un jefe gane muchísimo más que un empleado.", "a": "x", "v": 1},
    {"t": "El gobierno debería prohibir la comida basura.", "a": "y", "v": 1},
    {"t": "Tener vecinos de muchas razas distintas fortalece al país.", "a": "y", "v": -1},
    {"t": "Las huelgas generales solo sirven para perder tiempo.", "a": "x", "v": 1},
    {"t": "La tecnología nos está haciendo menos humanos.", "a": "y", "v": 1},
    {"t": "Los multimillonarios deberían dar casi todo su dinero al Estado.", "a": "x", "v": -1},
    {"t": "Hay que prohibir pronto los coches de gasolina.", "a": "x", "v": -1},
    {"t": "Sin una autoridad que ponga orden, la sociedad sería un caos.", "a": "y", "v": 1},
    {"t": "Cualquier tiempo pasado fue mucho mejor.", "a": "y", "v": 1}
]

# --- PANTALLAS ---
if st.session_state.idx >= len(questions):
    x, y = st.session_state.x, st.session_state.y
    
    if x > 100 and y > 100: n, d = "DERECHA AUTORITARIA", "Orden social fuerte y libertad económica."
    elif x < -100 and y > 100: n, d = "IZQUIERDA AUTORITARIA", "Estado fuerte que controla la economía."
    elif x > 100 and y < -100: n, d = "LIBERALISMO RADICAL", "Libertad individual y mercado por encima de todo."
    elif x < -100 and y < -100: n, d = "IZQUIERDA LIBERTARIA", "Comunidades libres sin jerarquías."
    else: n, d = "CENTRO POLÍTICO", "Moderación y sentido común."

    st.markdown(f'<div class="result-card"><div class="result-title" style="font-size:50px; color:#0D47A1;">{n}</div><div class="result-desc">{d}</div></div>', unsafe_allow_html=True)

    def get_b64(f):
        try:
            with open(f, "rb") as b: return base64.b64encode(b.read()).decode()
        except: return ""

    img_data = get_b64("chart.png")
    l_html = "".join([f'<div class="dot" style="left:{50+(l["x"]*0.23)}%; top:{50-(l["y"]*0.23)}%; width:16px; height:16px; background:{l["c"]}; z-index:50;"></div>' for l in LEADERS])
    ux, uy = max(8, min(92, 50 + (x * 0.23))), max(8, min(92, 50 - (y * 0.23)))
    
    st.markdown(f'<div class="map-container"><img src="data:image/png;base64,{img_data}" style="width:100%; height:100%;">{l_html}<div class="dot user-dot" style="left:{ux}%; top:{uy}%;">Tú</div></div>', unsafe_allow_html=True)

    # BOTONES FINALES
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 REINICIAR"):
            st.session_state.update({'idx':0, 'x':0, 'y':0, 'hist':[]})
            st.rerun()
    with col2:
        if st.button("🖨️ IMPRIMIR / PDF"):
            st.components.v1.html("<script>window.print();</script>", height=0)

else:
    st.progress(st.session_state.idx / len(questions))
    st.markdown(f'<div class="question-text">{questions[st.session_state.idx]["t"]}</div>', unsafe_allow_html=True)
    
    st.button("Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("De acuerdo", on_click=responder, args=(1,))
    st.button("No estoy seguro / Neutral", on_click=responder, args=(0,))
    st.button("En desacuerdo", on_click=responder, args=(-1,))
    st.button("Totalmente en desacuerdo", on_click=responder, args=(-2,))

    if st.session_state.idx > 0:
        if st.button("⬅️ VOLVER ATRÁS"):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px; st.session_state.y -= py
            st.session_state.idx -= 1
            st.rerun()
