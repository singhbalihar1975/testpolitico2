import streamlit as st
import base64

# 1. CONFIGURACIÓN Y CSS REVISADO
st.set_page_config(page_title="Brújula Política Estudiantil", layout="centered")

st.markdown("""
    <style>
    /* Fondo Azul Muy Claro */
    .stApp { background-color: #E3F2FD; }
    
    /* PREGUNTAS GIGANTES */
    .question-text {
        text-align: center;
        font-size: 38px !important; 
        font-weight: 800;
        color: #0D47A1;
        margin: 40px 0px 60px 0px;
        line-height: 1.1;
    }

    /* ALINEACIÓN LIGERAMENTE A LA IZQUIERDA */
    div.stButton {
        display: flex;
        justify-content: flex-start; /* Movidos a la izquierda */
        padding-left: 10%; /* Ajuste fino de posición */
        width: 100%;
    }

    div.stButton > button {
        width: 550px !important; 
        height: 65px !important;
        border-radius: 15px !important;
        font-size: 19px !important;
        font-weight: bold !important;
        border: none !important;
        margin: 5px 0px !important;
        /* COLOR AZUL CLARO SOLICITADO */
        background-color: #BBDEFB !important;
        color: #0D47A1 !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        transition: 0.3s;
    }

    /* EFECTO HOVER PARA LOS BOTONES AZULES */
    div.stButton > button:hover { 
        background-color: #90CAF9 !important;
        transform: translateX(5px); /* Pequeño desplazamiento al pasar el ratón */
    }

    /* BOTONES FINALES (NEGROS Y GRANDES) */
    .final-section div.stButton {
        justify-content: center !important;
        padding-left: 0 !important;
    }
    
    .final-section div.stButton > button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        width: 100% !important;
        height: 75px !important;
        font-size: 22px !important;
        border-radius: 10px !important;
    }

    /* TARJETA DE RESULTADOS */
    .result-card {
        background-color: white; padding: 40px; border-radius: 30px;
        text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border: 6px solid #1976D2;
    }
    .result-title { font-size: 50px; font-weight: 900; color: #0D47A1; }
    .result-desc { font-size: 24px; color: #37474F; }

    /* MAPA */
    .map-container {
        position: relative; width: 450px; height: 450px; 
        margin: 30px auto; border: 10px solid white; border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2); overflow: hidden;
        background-color: white;
    }
    .dot { position: absolute; border-radius: 50%; border: 2px solid white; transform: translate(-50%, -50%); }
    .user-dot {
        width: 40px; height: 40px; background-color: #FF1744; z-index: 100;
        box-shadow: 0 0 20px #FF1744; border: 4px solid white; color: white;
        display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE DATOS
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
    {"t": "Los bancos centrales deberían desaparecer.", "a": "x", "v": 1},
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
    {"t": "Ver películas para adultos debería estar prohibido por ley.", "a": "y", "v": 1},
    {"t": "Nadie debería prohibir una obra de arte, aunque sea ofensiva.", "a": "y", "v": -1},
    {"t": "La pena de muerte está bien para los peores criminales.", "a": "y", "v": 1},
    {"t": "Que venga mucha gente de fuera hace que nuestra cultura se pierda.", "a": "y", "v": 1},
    {"t": "El matrimonio solo debería ser entre un hombre y una mujer.", "a": "y", "v": 1},
    {"t": "Debería estar prohibido cortar calles para hacer manifestaciones.", "a": "y", "v": 1},
    {"t": "Uno elige lo que quiere ser, no nace con ello.", "a": "y", "v": -1},
    {"t": "La monarquía ya no debería existir.", "a": "y", "v": -1},
    {"t": "La policía necesita mucho más poder.", "a": "y", "v": 1},
    {"t": "Aprender sobre sexo en el colegio es fundamental.", "a": "y", "v": -1},
    {"t": "Insultar a la religión no debería ser un delito.", "a": "y", "v": -1},
    {"t": "La bandera de nuestro país es algo sagrado.", "a": "y", "v": 1},
    {"t": "Los científicos deberían poder clonar humanos.", "a": "y", "v": -1},
    {"t": "Hay demasiada piel fina hoy en día.", "a": "y", "v": 1},
    {"t": "Mezclar muchas culturas en el mismo barrio no funciona.", "a": "y", "v": 1},
    {"t": "Es necesario probar medicinas con animales.", "a": "y", "v": 1},
    {"t": "El gobierno debería pagar por tener hijos.", "a": "y", "v": 1},
    {"t": "Bajarse películas no es un crimen.", "a": "y", "v": -1},
    {"t": "Más disciplina en el colegio.", "a": "y", "v": 1},
    {"t": "Controlar la IA es necesario.", "a": "y", "v": 1},
    {"t": "Energía nuclear es la solución.", "a": "x", "v": 1},
    {"t": "Animales con los mismos derechos.", "a": "y", "v": -1},
    {"t": "El espacio debe ser privado.", "a": "x", "v": 1},
    {"t": "El cine público es malgastar impuestos.", "a": "x", "v": 1},
    {"t": "Globalización destruye costumbres.", "a": "y", "v": 1},
    {"t": "El capitalismo rompe el planeta.", "a": "x", "v": -1},
    {"t": "Votar por internet leyes.", "a": "y", "v": -1},
    {"t": "Cárcel como castigo duro.", "a": "y", "v": 1},
    {"t": "Ricos esforzados.", "a": "x", "v": 1},
    {"t": "Internet gratis.", "a": "x", "v": -1},
    {"t": "Religión obligatoria.", "a": "y", "v": 1},
    {"t": "Ejército en guerras externas.", "a": "y", "v": 1},
    {"t": "Criptos son libertad.", "a": "x", "v": 1},
    {"t": "Jefes que ganan mucho es justo.", "a": "x", "v": 1},
    {"t": "Prohibir comida basura.", "a": "y", "v": 1},
    {"t": "Diversidad fortalece.", "a": "y", "v": -1},
    {"t": "Huelgas pierden tiempo.", "a": "x", "v": 1},
    {"t": "Tecnología nos hace menos humanos.", "a": "y", "v": 1},
    {"t": "Multimillonarios deben pagar todo.", "a": "x", "v": -1},
    {"t": "Prohibir gasolina.", "a": "x", "v": -1},
    {"t": "Autoridad evita el caos.", "a": "y", "v": 1},
    {"t": "Pasado mejor.", "a": "y", "v": 1}
]

# --- FLUJO DE LA APP ---
if st.session_state.idx >= len(questions):
    x, y = st.session_state.x, st.session_state.y
    
    # 15 Ideologías detalladas
    if y > 120:
        if x > 120: n, d = "FASCISMO", "Estado totalitario, nacionalismo extremo y economía dirigida."
        elif x < -120: n, d = "ESTALINISMO", "Centralización absoluta, colectivismo y control estatal."
        else: n, d = "AUTORITARISMO", "Prioridad total al orden y la autoridad del Estado."
    elif y < -120:
        if x > 120: n, d = "ANARCOCAPITALISMO", "Soberanía individual total y mercado sin Estado."
        elif x < -120: n, d = "ANARCOCOMUNISMO", "Sociedad sin clases ni Estado basada en la ayuda mutua."
        else: n, d = "ANARQUISMO", "Rechazo a toda autoridad jerárquica."
    else:
        if x > 100: n, d = "NEOLIBERALISMO", "Libre mercado, privatización y Estado mínimo."
        elif x < -100: n, d = "SOCIALDEMOCRACIA", "Justicia social mediante impuestos en un sistema capitalista."
        else: n, d = "CENTRO", "Equilibrio moderado entre libertad y orden."

    st.markdown(f'<div class="result-card"><div class="result-title">{n}</div><div class="result-desc">{d}</div></div>', unsafe_allow_html=True)

    # Mapa Político
    l_html = "".join([f'<div class="dot" style="left:{50+(l["x"]*0.23)}%; top:{50-(l["y"]*0.23)}%; width:16px; height:16px; background:{l["c"]}; z-index:50;"></div>' for l in LEADERS])
    ux, uy = 50 + (x * 0.23), 50 - (y * 0.23)
    ux, uy = max(8, min(92, ux)), max(8, min(92, uy))
    
    st.markdown(f"""
        <div class="map-container">
            <div style="position:absolute; width:100%; height:2px; background:#ddd; top:50%;"></div>
            <div style="position:absolute; width:2px; height:100%; background:#ddd; left:50%;"></div>
            {l_html}
            <div class="dot user-dot" style="left:{ux}%; top:{uy}%;">Tú</div>
        </div>
    """, unsafe_allow_html=True)

    # Sección Final
    st.markdown('<div class="final-section">', unsafe_allow_html=True)
    
    # Botón Descargar (Lógica de texto)
    resultado_texto = f"Resultado Brújula Política: {n}\nEje X (Econ): {x}\nEje Y (Soc): {y}"
    st.download_button("💾 DESCARGAR RESULTADOS (.txt)", resultado_texto, file_name="mi_brujula.txt")
    
    if st.button("🔄 REINICIAR TEST"):
        st.session_state.update({'idx':0, 'x':0, 'y':0, 'hist':[]})
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.progress(st.session_state.idx / len(questions))
    st.markdown(f'<div class="question-text">{questions[st.session_state.idx]["t"]}</div>', unsafe_allow_html=True)
    
    # Botones con la nueva alineación y color azul claro
    st.button("Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("De acuerdo", on_click=responder, args=(1,))
    st.button("No estoy seguro / Neutral", on_click=responder, args=(0,))
    st.button("En desacuerdo", on_click=responder, args=(-1,))
    st.button("Totalmente en desacuerdo", on_click=responder, args=(-2,))

    if st.session_state.idx > 0:
        if st.button("⬅️ VOLVER A LA ANTERIOR"):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px; st.session_state.y -= py
            st.session_state.idx -= 1
            st.rerun()
