import streamlit as st
import base64

# 1. CONFIGURACIÓN Y ESTILO AGRESIVO
st.set_page_config(page_title="Brújula Política Estudiantil", layout="centered")

st.markdown("""
    <style>
    /* Fondo Azul Claro */
    .stApp { background-color: #E3F2FD !important; }

    /* Centrado de texto de preguntas */
    h1, h2, h3, .stMarkdown p {
        text-align: center !important;
    }
    
    .question-style {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #0D47A1 !important;
        padding: 20px;
        line-height: 1.2;
    }

    /* BOTONES DE RESPUESTA: Colores y Tamaño */
    div.stButton > button {
        width: 100% !important;
        height: 65px !important;
        border-radius: 35px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        margin-bottom: 10px !important;
        border: none !important;
        transition: 0.3s;
    }

    /* Asignación de colores por posición (Selector de hijos) */
    div[data-testid="stVerticalBlock"] > div:nth-child(2) button { background-color: #1B5E20 !important; color: white !important; }
    div[data-testid="stVerticalBlock"] > div:nth-child(3) button { background-color: #4CAF50 !important; color: white !important; }
    div[data-testid="stVerticalBlock"] > div:nth-child(4) button { background-color: #FFFFFF !important; color: #1565C0 !important; border: 2px solid #BBDEFB !important; }
    div[data-testid="stVerticalBlock"] > div:nth-child(5) button { background-color: #EF5350 !important; color: white !important; }
    div[data-testid="stVerticalBlock"] > div:nth-child(6) button { background-color: #B71C1C !important; color: white !important; }

    /* BOTONES FINALES: Negros y Grandes */
    .black-btn button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        height: 75px !important;
        font-size: 22px !important;
        border-radius: 15px !important;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE ESTADO
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})

def responder(pts):
    q = questions[st.session_state.idx]
    val = pts * 14.5 * q["v"]
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    st.session_state.idx += 1

# 3. BASE DE DATOS: 85 PREGUNTAS
questions = [
    {"t": "Cualquier persona debería poder abrir un negocio sin que el gobierno le ponga muchas reglas.", "a": "x", "v": 1},
    {"t": "Los hospitales deberían ser siempre gratis y pagados con nuestros impuestos.", "a": "x", "v": -1},
    {"t": "El gobierno debería poner un límite al precio del alquiler de los pisos.", "a": "x", "v": -1},
    {"t": "Es mejor que la electricidad sea vendida por empresas privadas que por el gobierno.", "a": "x", "v": 1},
    {"t": "La gente que tiene mucho dinero debería pagar muchísimos más impuestos que el resto.", "a": "x", "v": -1},
    {"t": "Es mejor comprar productos fabricados aquí que traerlos de otros países.", "a": "x", "v": -1},
    {"t": "No debería existir un sueldo mínimo; cada uno debería pactar lo que cobra.", "a": "x", "v": 1},
    {"t": "Cuidar el planeta es más importante que ganar mucho dinero como país.", "a": "x", "v": -1},
    {"t": "El gobierno no debería dar dinero a ninguna empresa privada.", "a": "x", "v": 1},
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
    {"t": "Los animales deberían tener los mismos derechos que los humanos.", "a": "y", "v": -1},
    {"t": "Llegar al espacio deberían hacerlo empresas privadas.", "a": "x", "v": 1},
    {"t": "Dar dinero para el cine es malgastar impuestos.", "a": "x", "v": 1},
    {"t": "La globalización destruye nuestras costumbres.", "a": "y", "v": 1},
    {"t": "El capitalismo está rompiendo el planeta.", "a": "x", "v": -1},
    {"t": "Votar todas las leyes por internet es buena idea.", "a": "y", "v": -1},
    {"t": "La cárcel debe ser un castigo duro, no un lugar de descanso.", "a": "y", "v": 1},
    {"t": "Si eres rico es porque te has esforzado.", "a": "x", "v": 1},
    {"t": "Internet debería ser gratis para todos.", "a": "x", "v": -1},
    {"t": "Debería haber clases de religión obligatorias.", "a": "y", "v": 1},
    {"t": "El ejército debería intervenir en conflictos de otros países.", "a": "y", "v": 1},
    {"t": "Las criptomonedas son el futuro de la libertad.", "a": "x", "v": 1},
    {"t": "Es justo que un jefe gane 100 veces más que un empleado.", "a": "x", "v": 1},
    {"t": "Prohibir la comida basura por el bien de la salud pública.", "a": "y", "v": 1},
    {"t": "La diversidad de razas y culturas fortalece al país.", "a": "y", "v": -1},
    {"t": "Las huelgas solo sirven para perjudicar a los ciudadanos.", "a": "x", "v": 1},
    {"t": "La tecnología nos está quitando la humanidad.", "a": "y", "v": 1},
    {"t": "Los multimillonarios deberían entregar su fortuna al Estado.", "a": "x", "v": -1},
    {"t": "Hay que prohibir pronto los coches de gasolina.", "a": "x", "v": -1},
    {"t": "Sin una autoridad fuerte, la sociedad sería un caos.", "a": "y", "v": 1},
    {"t": "Cualquier tiempo pasado fue mejor que el presente.", "a": "y", "v": 1}
]

# 4. LÍDERES (15)
LEADERS = [
    {"n": "Milei", "x": 185, "y": -180, "c": "#FFD600"},
    {"n": "Stalin", "x": -190, "y": 190, "c": "#D32F2F"},
    {"n": "Hitler", "x": 160, "y": 180, "c": "#212121"},
    {"n": "Mao", "x": -195, "y": 170, "c": "#B71C1C"},
    {"n": "Gandhi", "x": -140, "y": -150, "c": "#4CAF50"},
    {"n": "Rothbard", "x": 195, "y": -195, "c": "#FF9800"},
    {"n": "Thatcher", "x": 150, "y": 130, "c": "#1976D2"},
    {"n": "Castro", "x": -170, "y": 150, "c": "#2E7D32"},
    {"n": "Pinochet", "x": 175, "y": 170, "c": "#455A64"},
    {"n": "Che Guevara", "x": -185, "y": -90, "c": "#000000"},
    {"n": "Friedman", "x": 170, "y": -120, "c": "#00C853"},
    {"n": "Mussolini", "x": 140, "y": 195, "c": "#000000"},
    {"n": "Sanders", "x": -130, "y": -100, "c": "#03A9F4"},
    {"n": "John Locke", "x": 120, "y": -140, "c": "#795548"},
    {"n": "Kropotkin", "x": -195, "y": -195, "c": "#E91E63"}
]

# --- PANTALLA RESULTADOS (15 IDEOLOGÍAS) ---
if st.session_state.idx >= len(questions):
    x, y = st.session_state.x, st.session_state.y
    
    # Lógica de Ideologías
    if y > 65:
        if x > 65: n, d = "FASCISMO", "Crees en un Estado totalitario con economía nacional-corporativa."
        elif x < -65: n, d = "ESTALINISMO", "Economía planificada y autoridad estatal absoluta."
        else: n, d = "AUTORITARISMO SOCIAL", "El orden estatal es la prioridad sobre cualquier libertad."
    elif y > 25:
        if x > 50: n, d = "CONSERVADURISMO", "Valores tradicionales y libre mercado regulado."
        elif x < -50: n, d = "SOCIALISMO DE ESTADO", "Control público de la economía y leyes sociales fuertes."
        else: n, d = "NACIONALISMO", "Prioridad a la soberanía del país y cohesión social."
    elif y < -65:
        if x > 65: n, d = "ANARCOCAPITALISMO", "Propiedad privada absoluta y desaparición del Estado."
        elif x < -65: n, d = "ANARCOCOMUNISMO", "Sociedad sin clases ni gobierno basada en el apoyo mutuo."
        else: n, d = "ANARQUISMO", "Rechazo a toda autoridad jerárquica y estatal."
    elif y < -25:
        if x > 50: n, d = "LIBERTARISMO", "Mínima intervención estatal en economía y vida privada."
        elif x < -50: n, d = "SOCIALISMO LIBERTARIO", "Justicia social sin autoritarismo estatal."
        else: n, d = "PROGRESISMO LIBERAL", "Libertades civiles individuales y economía mixta."
    else:
        if x > 50: n, d = "NEOLIBERALISMO", "Prioridad absoluta al libre mercado y crecimiento."
        elif x < -50: n, d = "SOCIALDEMOCRACIA", "Capitalismo con fuertes impuestos para bienestar social."
        else: n, d = "CENTRISMO", "Equilibrio pragmático entre todos los ejes."

    st.markdown(f'<div style="text-align:center; background:white; padding:40px; border-radius:30px; border:5px solid #0D47A1;">'
                f'<h1 style="color:#0D47A1; margin:0;">{n}</h1>'
                f'<p style="font-size:20px; color:#444;">{d}</p></div>', unsafe_allow_html=True)

    # Métricas
    col1, col2 = st.columns(2)
    with col1: st.metric("Economía (Eje X)", f"{'Derecha' if x>0 else 'Izquierda'}", f"{int(abs(x))}%")
    with col2: st.metric("Social (Eje Y)", f"{'Autoritario' if y>0 else 'Libertario'}", f"{int(abs(y))}%")

    # Mapa Político Personalizado
    l_html = "".join([f'<div style="position:absolute; left:{50+(l["x"]*0.24)}%; top:{50-(l["y"]*0.24)}%; transform:translate(-50%,-50%);">'
                      f'<div style="width:10px; height:10px; background:{l["c"]}; border-radius:50%; border:1px solid white;"></div>'
                      f'<div style="font-size:10px; font-weight:bold; color:black; text-shadow: 1px 1px white;">{l["n"]}</div></div>' for l in LEADERS])
    
    ux, uy = 50 + (x * 0.24), 50 - (y * 0.24)
    st.markdown(f"""
        <div style="position:relative; width:100%; max-width:550px; height:550px; margin:20px auto; background:white; border:3px solid #000; border-radius:15px; overflow:hidden;">
            <div style="position:absolute; width:100%; height:2px; background:black; top:50%;"></div>
            <div style="position:absolute; width:2px; height:100%; background:black; left:50%;"></div>
            {l_html}
            <div style="position:absolute; left:{ux}%; top:{uy}%; transform:translate(-50%,-50%); z-index:99;">
                <div style="width:30px; height:30px; background:red; border-radius:50%; border:4px solid white; box-shadow:0 0 15px red;"></div>
                <div style="background:red; color:white; font-size:14px; font-weight:900; padding:2px 8px; border-radius:6px; margin-top:5px; text-align:center;">TÚ</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # BOTONES FINALES
    st.write("---")
    cola, colb = st.columns(2)
    with cola:
        st.markdown('<div class="black-btn">', unsafe_allow_html=True)
        if st.button("🔄 REINICIAR TEST", use_container_width=True):
            st.session_state.update({'idx':0, 'x':0, 'y':0, 'hist':[]})
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with colb:
        st.markdown('<div class="black-btn">', unsafe_allow_html=True)
        if st.button("🖨️ GUARDAR / PDF", use_container_width=True):
            st.components.v1.html("<script>window.print();</script>", height=0)
        st.markdown('</div>', unsafe_allow_html=True)

# --- PANTALLA PREGUNTAS ---
else:
    st.progress(st.session_state.idx / len(questions))
    st.markdown(f'<div class="question-style">{questions[st.session_state.idx]["t"]}</div>', unsafe_allow_html=True)
    
    st.button("Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("De acuerdo", on_click=responder, args=(1,))
    st.button("No estoy seguro / Neutral", on_click=responder, args=(0,))
    st.button("En desacuerdo", on_click=responder, args=(-1,))
    st.button("Totalmente en desacuerdo", on_click=responder, args=(-2,))

    if st.session_state.idx > 0:
        st.write("")
        if st.button("⬅️ VOLVER A LA ANTERIOR", use_container_width=True):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px; st.session_state.y -= py
            st.session_state.idx -= 1
            st.rerun()
