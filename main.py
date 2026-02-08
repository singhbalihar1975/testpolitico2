import streamlit as st
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Compás Político Pro", layout="centered")

# 2. ESTILOS CSS (Centrado Total, Tamaño del Chart y Diseño)
st.markdown("""
    <style>
    /* Centrado global de la columna de Streamlit */
    .main .block-container {
        max-width: 800px;
        padding-top: 2rem;
        padding-bottom: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .stApp { background-color: #F0F8FF; }
    
    /* Títulos y textos */
    .main-title { text-align: center; font-size: 45px; font-weight: 800; color: #1E3A8A; width: 100%; }
    .question-text { text-align: center; font-size: 28px !important; font-weight: 700; color: #1E3A8A; margin: 30px auto; width: 100%; }
    .info-text { text-align: center; font-size: 15px; color: #718096; margin-top: -10px; margin-bottom: 25px; font-style: italic; width: 100%; }

    /* Burbuja de Ideología */
    .result-bubble {
        background-color: white;
        border-radius: 25px;
        padding: 40px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
        text-align: center;
        margin: 20px auto;
        border: 1px solid #E2E8F0;
        width: 100%;
        max-width: 700px;
    }
    .ideology-title { font-size: 55px !important; font-weight: 900; color: #2B6CB0; text-transform: uppercase; margin: 0; }
    .ideology-desc { font-size: 20px; color: #4A5568; line-height: 1.5; margin-top: 15px; }

    /* Estilo de botones (Forzar centrado) */
    div.stButton {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    
    div.stButton > button {
        width: 100% !important;
        max-width: 550px !important;
        height: 60px !important;
        border-radius: 15px !important;
        font-size: 19px !important;
        background-color: #BEE3F8 !important;
        color: #2C5282 !important;
        border: 1px solid #90CDF4 !important;
        margin: 8px auto !important;
        font-weight: 600;
    }

    /* Separadores */
    .separator { border-top: 2px solid #CBD5E0; margin: 30px auto; width: 550px; }
    .bubble-sep { border-top: 2px solid #CBD5E0; margin: 20px auto; width: 60%; }

    /* Botones finales */
    .final-btn-container div.stButton > button {
        background-color: #2B6CB0 !important;
        color: white !important;
        max-width: 450px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BASE DE DATOS
LEADERS = [
    {"n": "Stalin", "x": -9, "y": 8.5, "c": "#E53E3E"},
    {"n": "Mao", "x": -9.2, "y": 7.5, "c": "#E53E3E"},
    {"n": "Castro", "x": -8, "y": 6, "c": "#38A169"},
    {"n": "Hitler", "x": 8, "y": 9, "c": "#2D3748"},
    {"n": "Thatcher", "x": 7, "y": 6, "c": "#3182CE"},
    {"n": "Gandhi", "x": -6, "y": -7, "c": "#48BB78"},
    {"n": "Sanders", "x": -4, "y": -3, "c": "#4299E1"},
    {"n": "Friedman", "x": 7.5, "y": -5.5, "c": "#D69E2E"},
    {"n": "Milei", "x": 8.5, "y": -8.5, "c": "#ECC94B"},
    {"n": "Rothbard", "x": 9.5, "y": -9.5, "c": "#D69E2E"}
]

questions = [
    {"t": "El gobierno no debería decir a las empresas cuánto pagar a sus empleados.", "a": "x", "v": 1},
    {"t": "La sanidad debería ser gratis y pagada con los impuestos de todos.", "a": "x", "v": -1},
    {"t": "El Estado debería ser el dueño de las empresas de luz y agua.", "a": "x", "v": -1},
    {"t": "Es mejor que los colegios sean privados para que haya competencia.", "a": "x", "v": 1},
    {"t": "Los que más dinero ganan deben pagar muchos más impuestos.", "a": "x", "v": -1},
    {"t": "El gobierno debería poner límites al precio de la comida básica.", "a": "x", "v": -1},
    {"t": "Si una empresa va a quebrar, el gobierno no debería ayudarla.", "a": "x", "v": 1},
    {"t": "Es mejor comprar productos de nuestro país que traerlos de fuera.", "a": "x", "v": -1},
    {"t": "Cualquiera debería poder abrir un negocio sin tantos permisos.", "a": "x", "v": 1},
    {"t": "Las huelgas de trabajadores hacen más daño que bien a la economía.", "a": "x", "v": 1},
    {"t": "El gobierno debe asegurar que todo el mundo tenga una casa.", "a": "x", "v": -1},
    {"t": "El libre mercado es la mejor forma de que un país sea rico.", "a": "x", "v": 1},
    {"t": "Hacerse rico es un mérito y el Estado no debería quitarte ese dinero.", "a": "x", "v": 1},
    {"t": "Los sindicatos tienen demasiado poder hoy en día.", "a": "x", "v": 1},
    {"t": "El transporte público debería ser totalmente gratuito.", "a": "x", "v": -1},
    {"t": "La competencia entre empresas baja los precios para nosotros.", "a": "x", "v": 1},
    {"t": "El Estado debería dar un sueldo básico a todos por igual.", "a": "x", "v": -1},
    {"t": "Los bancos no deberían cobrar intereses tan altos.", "a": "x", "v": -1},
    {"t": "Las herencias familiares no deberían tener impuestos.", "a": "x", "v": 1},
    {"t": "Los servicios públicos funcionan peor que los privados.", "a": "x", "v": 1},
    {"t": "Debería estar prohibido despedir a gente si la empresa gana dinero.", "a": "x", "v": -1},
    {"t": "Los paraísos fiscales deberían estar prohibidos.", "a": "x", "v": -1},
    {"t": "El capitalismo es el sistema más justo para progresar.", "a": "x", "v": 1},
    {"t": "Las grandes fortunas deberían repartirse entre los pobres.", "a": "x", "v": -1},
    {"t": "Si te esfuerzas más, es justo que ganes mucho más dinero.", "a": "x", "v": 1},
    {"t": "No debería haber impuestos especiales para la gasolina.", "a": "x", "v": 1},
    {"t": "Cualquier medicina debería ser gratis para quien la necesite.", "a": "x", "v": -1},
    {"t": "Es mejor bajar impuestos para que la gente tenga más dinero.", "a": "x", "v": 1},
    {"t": "El gobierno debe evitar que una sola empresa controle todo.", "a": "x", "v": -1},
    {"t": "Las multas a empresas que engañan deberían ser altísimas.", "a": "x", "v": -1},
    {"t": "La propiedad privada es intocable.", "a": "x", "v": 1},
    {"t": "El gobierno debería crear fábricas para dar empleo.", "a": "x", "v": -1},
    {"t": "El Banco Central hace que el dinero pierda valor.", "a": "x", "v": 1},
    {"t": "Es normal y natural que unos tengan más dinero que otros.", "a": "x", "v": 1},
    {"t": "Gastar dinero público en cultura es un error.", "a": "x", "v": 1},
    {"t": "Las leyes ambientales frenan el crecimiento económico.", "a": "x", "v": 1},
    {"t": "Bajar impuestos a los ricos crea empleo para los demás.", "a": "x", "v": 1},
    {"t": "Las máquinas que sustituyen humanos deberían pagar impuestos.", "a": "x", "v": -1},
    {"t": "El Estado no debería pedir préstamos que pagaremos nosotros.", "a": "x", "v": 1},
    {"t": "El precio del alquiler debe estar regulado por ley.", "a": "x", "v": -1},
    {"t": "Vender órganos debería ser legal si hay acuerdo entre personas.", "a": "x", "v": 1},
    {"t": "El Estado gasta demasiado en políticos y burocracia.", "a": "x", "v": 1},
    {"t": "Tener mucha riqueza acumulada debería ser ilegal.", "a": "x", "v": -1},
    {"t": "La disciplina y la obediencia son lo más importante.", "a": "y", "v": 1},
    {"t": "La libertad de expresión debe ser total.", "a": "y", "v": -1},
    {"t": "Hace falta mucha más policía en las calles.", "a": "y", "v": 1},
    {"t": "El aborto debe ser una decisión libre de la mujer.", "a": "y", "v": -1},
    {"t": "Un país necesita un líder fuerte.", "a": "y", "v": 1},
    {"t": "La religión no tiene sitio en la política moderna.", "a": "y", "v": -1},
    {"t": "Gastar más dinero en el ejército es necesario.", "a": "y", "v": 1},
    {"t": "La eutanasia debe ser legal.", "a": "y", "v": -1},
    {"t": "El gobierno debería controlar internet.", "a": "y", "v": 1},
    {"t": "Lo que haga un adulto en su casa no es asunto del Estado.", "a": "y", "v": -1},
    {"t": "Nuestra cultura nacional es superior a otras.", "a": "y", "v": 1},
    {"t": "La familia tradicional es la mejor base.", "a": "y", "v": 1},
    {"t": "Las cámaras de vigilancia nos hacen más libres.", "a": "y", "v": 1},
    {"t": "Se debe legalizar el consumo de marihuana.", "a": "y", "v": -1},
    {"t": "Hay que endurecer las fronteras.", "a": "y", "v": 1},
    {"t": "La bandera es el símbolo más sagrado.", "a": "y", "v": 1},
    {"t": "Cortar carreteras en protestas debe ser cárcel.", "a": "y", "v": 1},
    {"t": "Las tradiciones religiosas son la base moral.", "a": "y", "v": 1},
    {"t": "El Estado no debería pedir el DNI para todo.", "a": "y", "v": -1},
    {"t": "La cadena perpetua es necesaria.", "a": "y", "v": 1},
    {"t": "El orden es más importante que los derechos individuales.", "a": "y", "v": 1},
    {"t": "La justicia protege demasiado a los delincuentes.", "a": "y", "v": 1},
    {"t": "Los hijos pertenecen a los padres, no al Estado.", "a": "y", "v": 1},
    {"t": "Quemar la bandera debería ser delito.", "a": "y", "v": 1},
    {"t": "El porno debe controlarse.", "a": "y", "v": 1},
    {"t": "Las cuotas de género son injustas.", "a": "y", "v": 1},
    {"t": "El servicio militar debería ser obligatorio.", "a": "y", "v": 1},
    {"t": "Registros policiales sin orden deben ser legales.", "a": "y", "v": 1},
    {"t": "No debe haber educación sexual en colegios.", "a": "y", "v": 1},
    {"t": "Blasfemar debe estar castigado.", "a": "y", "v": 1},
    {"t": "La globalización destruye nuestra identidad.", "a": "y", "v": 1},
    {"t": "Experimentar con células madre debe ser libre.", "a": "y", "v": -1},
    {"t": "La autoridad del profesor es absoluta.", "a": "y", "v": 1},
    {"t": "El arte moderno es una falta de respeto.", "a": "y", "v": 1},
    {"t": "Las cárceles deben ser lugares de castigo duro.", "a": "y", "v": 1},
    {"t": "Prohibiría el tabaco si pudiera.", "a": "y", "v": 1},
    {"t": "La unidad del país es sagrada.", "a": "y", "v": 1},
    {"t": "Premiar a quienes tengan muchos hijos.", "a": "y", "v": 1},
    {"t": "Las redes sociales nos vuelven maleducados.", "a": "y", "v": 1},
    {"t": "Derecho a tener armas en casa.", "a": "y", "v": -1},
    {"t": "Nuestros antepasados son sagrados.", "a": "y", "v": 1},
    {"t": "Un buen ciudadano obedece siempre la ley.", "a": "y", "v": 1}
]

if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})

def responder(puntos):
    q = questions[st.session_state.idx]
    total_x = len([qu for qu in questions if qu["a"] == "x"])
    total_y = len([qu for qu in questions if qu["a"] == "y"])
    val = (puntos / 2) * (10 / ((total_x if q["a"]=="x" else total_y) / 2)) * q["v"]
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    st.session_state.idx += 1

# --- PANTALLA RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown('<div class="main-title">📍 Tu Resultado</div>', unsafe_allow_html=True)
    x, y = st.session_state.x, st.session_state.y

    # Lógica de Ideologías
    if y > 2:
        if x > 2: id_nom, desc = "Derecha Conservadora", "Buscas mantener las tradiciones y el orden social con un sistema económico de mercado libre."
        elif x < -2: id_nom, desc = "Izquierda Autoritaria", "Crees en la igualdad económica impuesta por un Estado fuerte que dirija la sociedad."
        else: id_nom, desc = "Populismo de Orden", "Priorizas el control social y la autoridad del Estado por encima de la economía o la libertad."
    elif y < -2:
        if x > 2: id_nom, desc = "Libertarismo", "Defiendes la libertad individual absoluta y un mercado sin ninguna intervención del gobierno."
        elif x < -2: id_nom, desc = "Socialismo Libertario", "Buscas la igualdad social y económica pero rechazando la autoridad de los gobiernos."
        else: id_nom, desc = "Progresismo Radical", "Te enfocas en los derechos civiles y la libertad personal con un sistema económico mixto."
    else:
        if x > 2: id_nom, desc = "Liberalismo", "Defiendes las libertades individuales y una economía de mercado con poca intervención estatal."
        elif x < -2: id_nom, desc = "Socialdemocracia", "Crees en la democracia parlamentaria combinada con ayudas sociales y regulación económica."
        else: id_nom, desc = "Centro Político", "Mantienes una postura equilibrada entre la autoridad, la libertad, el mercado y el Estado."

    st.markdown(f"""
        <div class="result-bubble">
            <div class="ideology-title">{id_nom}</div>
            <div class="bubble-sep"></div>
            <div class="ideology-desc">{desc}</div>
        </div>
    """, unsafe_allow_html=True)

    # CHART MÁS GRANDE (600px)
    leaders_js = "".join([f"""
        <div class="dot" style="left:{50 + (l['x']*4.5)}%; top:{50 - (l['y']*4.5)}%; background:{l['c']};"></div>
        <div class="label" style="left:{50 + (l['x']*4.5)}%; top:{50 - (l['y']*4.5)}%;">{l['n']}</div>
    """ for l in LEADERS])
    
    user_x = max(2, min(98, 50 + (x * 4.5)))
    user_y = max(2, min(98, 50 - (y * 4.5)))

    compass_html = f"""
    <style>
        .map {{ position: relative; width: 600px; height: 600px; margin: 40px auto; background: white; border: 3px solid #000; font-family: sans-serif; overflow: visible; }}
        .quadrant {{ position: absolute; width: 50%; height: 50%; opacity: 0.2; }}
        .axis-h {{ position: absolute; width: 100%; height: 3px; background: #000; top: 50%; z-index: 2; }}
        .axis-v {{ position: absolute; width: 3px; height: 100%; background: #000; left: 50%; z-index: 2; }}
        .q-label {{ position: absolute; font-size: 14px; font-weight: 800; color: #000; z-index: 3; }}
        .dot {{ position: absolute; width: 12px; height: 12px; border-radius: 50%; transform: translate(-50%, -50%); border: 1px solid #000; z-index: 4; }}
        .label {{ position: absolute; font-size: 11px; font-weight: bold; transform: translate(-50%, 8px); width: 70px; text-align: center; z-index: 4; }}
        .user-dot {{ position: absolute; width: 28px; height: 28px; background: red; border-radius: 50%; transform: translate(-50%, -50%); border: 4px solid white; box-shadow: 0 0 15px red; z-index: 10; }}
        .user-txt {{ position: absolute; font-size: 18px; font-weight: 900; color: red; transform: translate(-50%, 15px); z-index: 11; text-shadow: 1px 1px 2px white; }}
    </style>
    <div class="map">
        <div class="quadrant" style="top:0; left:0; background: #FFB3B3;"></div>
        <div class="quadrant" style="top:0; right:0; background: #B3C1FF;"></div>
        <div class="quadrant" style="bottom:0; left:0; background: #B3FFCC;"></div>
        <div class="quadrant" style="bottom:0; right:0; background: #FFF9B3;"></div>
        <div class="axis-h"></div><div class="axis-v"></div>
        <div class="q-label" style="top:-30px; left:41%;">AUTORITARIO</div>
        <div class="q-label" style="bottom:-30px; left:42%;">LIBERTARIO</div>
        <div class="q-label" style="top:48%; left:-90px;">IZQUIERDA</div>
        <div class="q-label" style="top:48%; right:-80px;">DERECHA</div>
        {leaders_js}
        <div class="user-dot" style="left:{user_x}%; top:{user_y}%;"></div>
        <div class="user-txt" style="left:{user_x}%; top:{user_y}%;">TÚ</div>
    </div>
    """
    components.html(compass_html, height=700)

    st.markdown('<div class="final-btn-container">', unsafe_allow_html=True)
    st.button("🖨️ IMPRIMIR / GUARDAR PDF", on_click=lambda: components.html("<script>window.print();</script>"))
    if st.button("🔄 REPETIR TEST"):
        st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANTALLA PREGUNTAS ---
else:
    st.markdown('<div class="main-title">Compás Político</div>', unsafe_allow_html=True)
    st.progress(st.session_state.idx / len(questions))
    st.write(f"<p style='text-align:center;'>Pregunta {st.session_state.idx + 1} de {len(questions)}</p>", unsafe_allow_html=True)
    
    if st.session_state.idx == 0:
        st.markdown('<div class="info-text">Si no sabes lo que significa la pregunta o no tienes una opinión clara, responde "Neutral / No lo sé".</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="question-text">{questions[st.session_state.idx]["t"]}</div>', unsafe_allow_html=True)
    
    st.button("✅ Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("👍 De acuerdo", on_click=responder, args=(1,))
    st.button("😐 Neutral / No lo sé", on_click=responder, args=(0,))
    st.button("👎 En desacuerdo", on_click=responder, args=(-1,))
    st.button("❌ Totalmente en desacuerdo", on_click=responder, args=(-2,))

    if st.session_state.idx > 0:
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        if st.button("⬅️ VOLVER A LA ANTERIOR"):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px
            st.session_state.y -= py
            st.session_state.idx -= 1
            st.rerun()
