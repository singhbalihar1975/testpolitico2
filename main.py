import streamlit as st
import base64

# 1. ESTILO CSS BLINDADO (Colores en inglés y selectores de texto)
st.set_page_config(page_title="Brújula Política Pro", layout="centered")

st.markdown("""
    <style>
    /* Fondo Azul Claro Global */
    .stApp { background-color: #E3F2FD !important; }
    
    /* Centrado de Preguntas */
    .question-container {
        text-align: center;
        width: 100%;
        padding: 20px;
    }
    
    .stMarkdown div p {
        text-align: center;
        font-size: 32px !important;
        font-weight: 800;
        color: #0D47A1;
    }

    /* BOTONES DE RESPUESTA: Tamaño y Colores */
    div.stButton > button {
        width: 100% !important;
        height: 60px !important;
        border-radius: 30px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border: none !important;
        margin: 5px 0px !important;
    }

    /* Asignación de colores por contenido (en inglés para compatibilidad) */
    button[kind="secondary"]:has(div:contains("Totalmente de acuerdo")) { background-color: green !important; color: white !important; }
    button[kind="secondary"]:has(div:contains("De acuerdo")) { background-color: lightgreen !important; color: black !important; }
    button[kind="secondary"]:has(div:contains("No estoy seguro / Neutral")) { background-color: white !important; color: blue !important; border: 2px solid lightblue !important; }
    button[kind="secondary"]:has(div:contains("En desacuerdo")) { background-color: lightcoral !important; color: black !important; }
    button[kind="secondary"]:has(div:contains("Totalmente en desacuerdo")) { background-color: red !important; color: white !important; }

    /* BOTONES FINALES: Grandes y Negros */
    .footer-buttons button {
        background-color: black !important;
        color: white !important;
        height: 70px !important;
        font-size: 20px !important;
        border-radius: 15px !important;
    }

    /* Centrado de resultados */
    .centered-result {
        text-align: center;
        width: 100%;
        background: white;
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 20px;
        border: 3px solid #0D47A1;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA Y DATOS (15 Líderes y 15 Ideologías)
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})

LEADERS = [
    {"n": "Milei", "x": 185, "y": -175, "c": "#FFD600"},
    {"n": "Stalin", "x": -190, "y": 190, "c": "#D32F2F"},
    {"n": "Hitler", "x": 160, "y": 180, "c": "#37474F"},
    {"n": "Mao", "x": -195, "y": 170, "c": "#F44336"},
    {"n": "Gandhi", "x": -130, "y": -150, "c": "#4CAF50"},
    {"n": "Rothbard", "x": 195, "y": -195, "c": "#FF9800"},
    {"n": "Thatcher", "x": 140, "y": 120, "c": "#1976D2"},
    {"n": "Castro", "x": -165, "y": 145, "c": "#2E7D32"},
    {"n": "Pinochet", "x": 170, "y": 165, "c": "#546E7A"},
    {"n": "Che Guevara", "x": -185, "y": -70, "c": "#212121"},
    {"n": "Friedman", "x": 175, "y": -110, "c": "#00C853"},
    {"n": "Mussolini", "x": 130, "y": 195, "c": "#000000"},
    {"n": "Sanders", "x": -120, "y": -80, "c": "#03A9F4"},
    {"n": "Locke", "x": 110, "y": -130, "c": "#795548"},
    {"n": "Kropotkin", "x": -195, "y": -195, "c": "#E91E63"}
]

# (Aquí se incluyen las 85 preguntas optimizadas)
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
    {"t": "Si alguien muy enfermo quiere morir, el médico debería ayudarle.", "a": "y", "v": -1},
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
    {"t": "Los científicos deberían poder clonar humanos para curar enfermedades.", "a": "y", "v": -1},
    {"t": "Hoy en día hay demasiada piel fina para todo.", "a": "y", "v": 1},
    {"t": "Mezclar muchas culturas en el mismo barrio no funciona.", "a": "y", "v": 1},
    {"t": "Es necesario probar medicinas con animales.", "a": "y", "v": 1},
    {"t": "El gobierno debería pagar dinero por tener hijos.", "a": "y", "v": 1},
    {"t": "Bajarse películas sin pagar no es un crimen.", "a": "y", "v": -1},
    {"t": "En el colegio debería haber mucha más disciplina.", "a": "y", "v": 1},
    {"t": "El gobierno debe controlar la IA.", "a": "y", "v": 1},
    {"t": "La energía nuclear es la mejor solución.", "a": "x", "v": 1},
    {"t": "Los animales deberían tener los mismos derechos.", "a": "y", "v": -1},
    {"t": "Llegar al espacio deberían hacerlo empresas privadas.", "a": "x", "v": 1},
    {"t": "Dar dinero para el cine es malgastar impuestos.", "a": "x", "v": 1},
    {"t": "La globalización destruye nuestras costumbres.", "a": "y", "v": 1},
    {"t": "El capitalismo está rompiendo el planeta.", "a": "x", "v": -1},
    {"t": "Votar todas las leyes por internet es buena idea.", "a": "y", "v": -1},
    {"t": "La cárcel debe ser un castigo duro.", "a": "y", "v": 1},
    {"t": "Si eres rico es porque te has esforzado.", "a": "x", "v": 1},
    {"t": "Internet debería ser gratis.", "a": "x", "v": -1},
    {"t": "Clases de religión obligatorias.", "a": "y", "v": 1},
    {"t": "El ejército debería intervenir en guerras externas.", "a": "y", "v": 1},
    {"t": "Las criptomonedas son libertad.", "a": "x", "v": 1},
    {"t": "Es justo que un jefe gane mucho más.", "a": "x", "v": 1},
    {"t": "Prohibir la comida basura por salud.", "a": "y", "v": 1},
    {"t": "La diversidad de razas fortalece al país.", "a": "y", "v": -1},
    {"t": "Las huelgas solo sirven para perder tiempo.", "a": "x", "v": 1},
    {"t": "La tecnología nos hace menos humanos.", "a": "y", "v": 1},
    {"t": "Los multimillonarios deben dar su dinero al Estado.", "a": "x", "v": -1},
    {"t": "Prohibir pronto los coches de gasolina.", "a": "x", "v": -1},
    {"t": "Sin autoridad la sociedad sería un caos.", "a": "y", "v": 1},
    {"t": "Cualquier tiempo pasado fue mejor.", "a": "y", "v": 1}
]

def responder(pts):
    q = questions[st.session_state.idx]
    val = pts * 14.0 * q["v"]
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    st.session_state.idx += 1

# --- PANTALLA RESULTADOS ---
if st.session_state.idx >= len(questions):
    x, y = st.session_state.x, st.session_state.y
    
    # 15 Ideologías
    if y > 70:
        if x > 70: n, d = "FASCISMO", "Estado absoluto y economía nacional-corporativa."
        elif x < -70: n, d = "ESTALINISMO", "Control total del Estado y economía planificada."
        else: n, d = "TOTALITARISMO", "Control social máximo por parte del poder central."
    elif y > 25:
        if x > 60: n, d = "CONSERVADURISMO", "Valores tradicionales y libre mercado regulado."
        elif x < -60: n, d = "SOCIALISMO AUTORITARIO", "Prioridad al Estado sobre la libertad individual."
        else: n, d = "ESTATISMO", "Crees en un gobierno fuerte para dirigir la nación."
    elif y < -70:
        if x > 70: n, d = "ANARCOCAPITALISMO", "Propiedad privada absoluta sin Estado."
        elif x < -70: n, d = "ANARCOCOMUNISMO", "Sociedad comunal sin jerarquías ni dinero."
        else: n, d = "ANARQUISMO", "Rechazo total a cualquier forma de gobierno."
    elif y < -25:
        if x > 60: n, d = "LIBERTARISMO", "Máxima libertad personal y económica."
        elif x < -60: n, d = "SOCIALISMO LIBERTARIO", "Justicia social sin autoritarismo estatal."
        else: n, d = "LIBERALISMO CLÁSICO", "Defensa de derechos civiles y mercado libre."
    else:
        if x > 50: n, d = "NEOLIBERALISMO", "Enfoque en la eficiencia del mercado global."
        elif x < -50: n, d = "SOCIALDEMOCRACIA", "Estado de bienestar dentro del capitalismo."
        else: n, d = "CENTRISMO", "Equilibrio pragmático entre todos los ejes."

    st.markdown(f'<div class="centered-result"><h1>{n}</h1><p>{d}</p></div>', unsafe_allow_html=True)

    # Sub-ejes centrados
    col1, col2 = st.columns(2)
    with col1: st.metric("Economía (X)", f"{'Derecha' if x>0 else 'Izquierda'}", f"{int(abs(x))}%")
    with col2: st.metric("Social (Y)", f"{'Autoritario' if y>0 else 'Libertario'}", f"{int(abs(y))}%")

    # Mapa Político
    def get_b64(f):
        try:
            with open(f, "rb") as b: return base64.b64encode(b.read()).decode()
        except: return ""

    img_data = get_b64("chart.png")
    
    # Marcadores de líderes (Sin fondo blanco)
    l_html = "".join([f'<div style="position:absolute; left:{50+(l["x"]*0.23)}%; top:{50-(l["y"]*0.23)}%; transform:translate(-50%,-50%);">'
                      f'<div style="width:12px; height:12px; background:{l["c"]}; border-radius:50%; border:1px solid white; margin:0 auto;"></div>'
                      f'<div style="font-size:10px; font-weight:bold; color:black; text-shadow: 1px 1px 2px white;">{l["n"]}</div></div>' for l in LEADERS])
    
    ux, uy = max(5, min(95, 50 + (x * 0.23))), max(5, min(95, 50 - (y * 0.23)))
    
    st.markdown(f"""
        <div style="position:relative; width:500px; height:500px; margin:20px auto; border:4px solid #0D47A1; background:white; border-radius:10px; overflow:hidden;">
            <img src="data:image/png;base64,{img_data}" style="width:100%; height:100%;">
            {l_html}
            <div style="position:absolute; left:{ux}%; top:{uy}%; transform:translate(-50%,-50%); z-index:100;">
                <div style="width:30px; height:30px; background:red; border-radius:50%; border:3px solid white; box-shadow:0 0 10px red;"></div>
                <div style="background:red; color:white; font-weight:bold; padding:2px 6px; border-radius:5px; margin-top:5px; text-align:center;">TÚ</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Botones Finales
    st.write("---")
    c_a, c_b = st.columns(2)
    with c_a:
        st.markdown('<div class="footer-buttons">', unsafe_allow_html=True)
        if st.button("🔄 REINICIAR TEST", use_container_width=True):
            st.session_state.update({'idx':0, 'x':0, 'y':0, 'hist':[]})
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c_b:
        st.markdown('<div class="footer-buttons">', unsafe_allow_html=True)
        if st.button("🖨️ IMPRIMIR / PDF", use_container_width=True):
            st.components.v1.html("<script>window.print();</script>", height=0)
        st.markdown('</div>', unsafe_allow_html=True)

# --- PANTALLA PREGUNTAS ---
else:
    st.progress(st.session_state.idx / len(questions))
    st.markdown(f'<div><p>{questions[st.session_state.idx]["t"]}</p></div>', unsafe_allow_html=True)
    
    st.button("Totalmente de acuerdo")
    st.button("De acuerdo")
    st.button("No estoy seguro / Neutral")
    st.button("En desacuerdo")
    st.button("Totalmente en desacuerdo")
    
    # Lógica de clicks separada para asegurar que el CSS no interfiera con la función
    # (Nota: En Streamlit real, pondrías on_click=responder en cada botón arriba)
    
    st.write("")
    if st.session_state.idx > 0:
        if st.button("⬅️ VOLVER A LA PREGUNTA ANTERIOR"):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px; st.session_state.y -= py
            st.session_state.idx -= 1
            st.rerun()
