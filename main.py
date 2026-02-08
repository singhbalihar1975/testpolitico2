import streamlit as st
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN Y ESTILOS
st.set_page_config(page_title="Compás Político Pro", layout="centered")

st.markdown("""
    <style>
    /* Estética General */
    .stApp { background-color: #F0F4F8; }
    .main-title { text-align: center; color: #1E3A8A; font-size: 32px; font-weight: 800; margin-bottom: 10px; }
    
    /* Advertencia inicial */
    .warning-box { 
        background-color: #FEF3C7; border-left: 5px solid #F59E0B; 
        padding: 15px; margin: 20px auto; border-radius: 8px; 
        color: #92400E; font-size: 15px; text-align: center; max-width: 600px;
    }

    /* Pregunta */
    .question-box {
        text-align: center; font-size: 24px !important; font-weight: 700; 
        color: #1E40AF; margin: 30px 0; min-height: 70px;
    }

    /* BOTONES: Centrados, misma longitud y estilo */
    div.stButton > button {
        width: 100% !important;
        max-width: 550px !important;
        display: block;
        margin: 10px auto !important;
        height: 50px !important;
        border-radius: 12px !important;
        font-size: 17px !important;
        font-weight: 600 !important;
        background-color: #FFFFFF !important;
        color: #1E40AF !important;
        border: 2px solid #BFDBFE !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #DBEAFE !important;
        border-color: #3B82F6 !important;
    }

    /* Separador Horizontal */
    .custom-hr { border: 0; height: 1px; background-image: linear-gradient(to right, transparent, #94A3B8, transparent); margin: 40px auto; width: 90%; }

    /* Estilos del Gráfico */
    .label-leader { position: absolute; font-size: 10px; font-weight: bold; color: #333; transform: translate(-50%, 8px); white-space: nowrap; }
    .dot { position: absolute; width: 10px; height: 10px; border-radius: 50%; border: 1px solid white; transform: translate(-50%, -50%); }
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS: PREGUNTAS (85)
questions = [
    # ECONÓMICAS (Eje X)
    {"t": "El gobierno no debería decir a las empresas cuánto pagar.", "a": "x", "v": 1},
    {"t": "La sanidad debería ser gratis y pagada con impuestos.", "a": "x", "v": -1},
    {"t": "El Estado debería ser el dueño de empresas de luz y agua.", "a": "x", "v": -1},
    {"t": "Es mejor que los colegios sean privados para que compitan.", "a": "x", "v": 1},
    {"t": "Los que más ganan deben pagar muchos más impuestos.", "a": "x", "v": -1},
    {"t": "El gobierno debería poner límites al precio de la comida.", "a": "x", "v": -1},
    {"t": "Si una empresa va a quebrar, el gobierno no debe ayudarla.", "a": "x", "v": 1},
    {"t": "Es mejor comprar productos nacionales que importados.", "a": "x", "v": -1},
    {"t": "Abrir un negocio debería ser posible sin tantos permisos.", "a": "x", "v": 1},
    {"t": "Las huelgas hacen más daño que bien a la economía.", "a": "x", "v": 1},
    {"t": "El gobierno debe asegurar que todo el mundo tenga casa.", "a": "x", "v": -1},
    {"t": "El libre mercado es la mejor forma de que un país progrese.", "a": "x", "v": 1},
    {"t": "Hacerse rico es un mérito; el Estado no debe quitarte dinero.", "a": "x", "v": 1},
    {"t": "Los sindicatos tienen demasiado poder hoy en día.", "a": "x", "v": 1},
    {"t": "El transporte público debería ser totalmente gratuito.", "a": "x", "v": -1},
    {"t": "La competencia entre empresas baja los precios siempre.", "a": "x", "v": 1},
    {"t": "El Estado debería dar un sueldo básico a todos por igual.", "a": "x", "v": -1},
    {"t": "Los bancos centrales deberían desaparecer.", "a": "x", "v": 1},
    {"t": "Las herencias familiares no deberían tener impuestos.", "a": "x", "v": 1},
    {"t": "Los servicios públicos funcionan peor que los privados.", "a": "x", "v": 1},
    {"t": "Prohibiría despedir a gente si la empresa gana dinero.", "a": "x", "v": -1},
    {"t": "Los paraísos fiscales deberían estar prohibidos.", "a": "x", "v": -1},
    {"t": "El capitalismo es el sistema más justo para prosperar.", "a": "x", "v": 1},
    {"t": "Las grandes fortunas deberían repartirse entre los pobres.", "a": "x", "v": -1},
    {"t": "Si te esfuerzas más, es justo que ganes mucho más dinero.", "a": "x", "v": 1},
    {"t": "No debería haber impuestos especiales para la gasolina.", "a": "x", "v": 1},
    {"t": "Cualquier medicina debería ser gratis para quien la use.", "a": "x", "v": -1},
    {"t": "Bajar impuestos es mejor que dar ayudas públicas.", "a": "x", "v": 1},
    {"t": "El gobierno debe evitar que una empresa controle todo.", "a": "x", "v": -1},
    {"t": "Las multas a empresas que engañan deben ser altísimas.", "a": "x", "v": -1},
    {"t": "La propiedad privada es sagrada e intocable.", "a": "x", "v": 1},
    {"t": "El gobierno debería crear fábricas para dar empleo.", "a": "x", "v": -1},
    {"t": "Es natural que unos tengan mucho más dinero que otros.", "a": "x", "v": 1},
    {"t": "Gastar dinero público en cultura es un error.", "a": "x", "v": 1},
    {"t": "Leyes ambientales frenan el crecimiento económico.", "a": "x", "v": 1},
    {"t": "Bajar impuestos a los ricos crea empleo para todos.", "a": "x", "v": 1},
    {"t": "Las máquinas que sustituyen humanos deben pagar tasas.", "a": "x", "v": -1},
    {"t": "El Estado no debería pedir préstamos a futuro.", "a": "x", "v": 1},
    {"t": "El precio del alquiler debe estar regulado por ley.", "a": "x", "v": -1},
    {"t": "Vender órganos debería ser legal si hay acuerdo mutuo.", "a": "x", "v": 1},
    {"t": "El Estado gasta demasiado en políticos y burocracia.", "a": "x", "v": 1},
    {"t": "Tener riqueza acumulada excesiva debería ser ilegal.", "a": "x", "v": -1},
    {"t": "El proteccionismo económico ayuda a los trabajadores.", "a": "x", "v": -1},
    
    # SOCIALES / AUTORIDAD (Eje Y)
    {"t": "La disciplina y obediencia son lo más importante.", "a": "y", "v": 1},
    {"t": "La libertad de expresión debe ser total y absoluta.", "a": "y", "v": -1},
    {"t": "Hace falta mucha más presencia policial en las calles.", "a": "y", "v": 1},
    {"t": "El aborto debe ser una decisión libre de la mujer.", "a": "y", "v": -1},
    {"t": "Un país necesita un líder fuerte para funcionar bien.", "a": "y", "v": 1},
    {"t": "La religión no tiene sitio en la política moderna.", "a": "y", "v": -1},
    {"t": "Gastar más dinero en el ejército es una prioridad.", "a": "y", "v": 1},
    {"t": "La eutanasia (muerte digna) debe ser legal.", "a": "y", "v": -1},
    {"t": "El gobierno debería poder controlar internet.", "a": "y", "v": 1},
    {"t": "Lo que haga un adulto en su casa no es asunto del Estado.", "a": "y", "v": -1},
    {"t": "Nuestra cultura nacional es superior a otras.", "a": "y", "v": 1},
    {"t": "La familia tradicional es la base de una buena sociedad.", "a": "y", "v": 1},
    {"t": "Se debe legalizar el consumo de marihuana.", "a": "y", "v": -1},
    {"t": "Hay que cerrar o endurecer mucho las fronteras.", "a": "y", "v": 1},
    {"t": "La bandera es el símbolo más sagrado de un país.", "a": "y", "v": 1},
    {"t": "Cortar carreteras en protestas debe ser cárcel.", "a": "y", "v": 1},
    {"t": "Las tradiciones religiosas deben ser la base moral.", "a": "y", "v": 1},
    {"t": "La cadena perpetua es necesaria para delitos graves.", "a": "y", "v": 1},
    {"t": "El orden es más importante que los derechos individuales.", "a": "y", "v": 1},
    {"t": "La justicia protege demasiado a los delincuentes.", "a": "y", "v": 1},
    {"t": "Quemar la bandera debería ser un delito grave.", "a": "y", "v": 1},
    {"t": "El acceso a la pornografía debe estar controlado.", "a": "y", "v": 1},
    {"t": "El servicio militar debería ser obligatorio.", "a": "y", "v": 1},
    {"t": "No debe haber educación sexual en los colegios.", "a": "y", "v": 1},
    {"t": "La globalización destruye nuestra identidad.", "a": "y", "v": 1},
    {"t": "Experimentar con células madre debe ser libre.", "a": "y", "v": -1},
    {"t": "La autoridad del profesor debe ser absoluta.", "a": "y", "v": 1},
    {"t": "Las cárceles deben ser lugares de castigo duro.", "a": "y", "v": 1},
    {"t": "La unidad del país es lo más sagrado.", "a": "y", "v": 1},
    {"t": "Debería ser legal tener armas para defensa.", "a": "y", "v": -1},
    {"t": "Un buen ciudadano obedece sin cuestionar.", "a": "y", "v": 1},
    {"t": "El Estado debe vigilar a personas sospechosas sin orden.", "a": "y", "v": 1},
    {"t": "La pena de muerte debería existir para violadores.", "a": "y", "v": 1},
    {"t": "Los inmigrantes deben adaptarse 100% a nuestras costumbres.", "a": "y", "v": 1},
    {"t": "Es aceptable censurar libros que dañen la moral.", "a": "y", "v": 1},
    {"t": "La prostitución debería estar totalmente prohibida.", "a": "y", "v": 1},
    {"t": "El Estado debe promover los valores patrióticos.", "a": "y", "v": 1},
    {"t": "Las huelgas de funcionarios deberían estar prohibidas.", "a": "y", "v": 1},
    {"t": "La rebeldía juvenil es un problema de falta de castigo.", "a": "y", "v": 1},
    {"t": "El matrimonio solo debe ser entre hombre y mujer.", "a": "y", "v": 1}
]

# 3. BASE DE DATOS: LÍDERES
LEADERS = [
    {"n": "Stalin", "x": -9, "y": 9, "c": "#C0392B"}, {"n": "Hitler", "x": 8, "y": 9, "c": "#1A202C"},
    {"n": "Mao", "x": -9.5, "y": 8.5, "c": "#C0392B"}, {"n": "Mussolini", "x": 7, "y": 8, "c": "#1A202C"},
    {"n": "Castro", "x": -7, "y": 6, "c": "#1E8449"}, {"n": "Thatcher", "x": 7.5, "y": 6, "c": "#2980B9"},
    {"n": "Gandhi", "x": -6.5, "y": -7, "c": "#48BB78"}, {"n": "Milei", "x": 9, "y": -8.5, "c": "#ECC94B"},
    {"n": "Sanders", "x": -5.5, "y": -2, "c": "#4299E1"}, {"n": "Friedman", "x": 8, "y": -6, "c": "#D69E2E"},
    {"n": "Locke", "x": 5, "y": -4, "c": "#8B4513"}, {"n": "Kropotkin", "x": -9.5, "y": -9.5, "c": "#1A202C"},
    {"n": "Rothbard", "x": 10, "y": -10, "c": "#ECC94B"}, {"n": "Pinochet", "x": 8.5, "y": 7.5, "c": "#2D3748"}
]

# 4. LÓGICA DE CONTROL
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})

def responder(pts):
    q = questions[st.session_state.idx]
    # Factor de escala (10 puntos max / num_preguntas * peso_max)
    val = pts * q["v"] * 0.12 
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    st.session_state.idx += 1

# 5. LÓGICA DE IDEOLOGÍAS
def get_ideology_name(x, y):
    if y > 5:
        if x < -5: return "Socialismo Autoritario"
        if x > 5: return "Fascismo / Nacionalismo"
        return "Autoritarismo Estructural"
    if y < -5:
        if x < -5: return "Anarco-Comunismo"
        if x > 5: return "Anarco-Capitalismo"
        return "Libertarismo Radical"
    if x < -5: return "Socialdemocracia Radical"
    if x > 5: return "Liberalismo Clásico"
    if abs(x) < 2 and abs(y) < 2: return "Centrismo Pragmático"
    return "Populismo Moderado"

# --- PANTALLA DE RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown('<div class="main-title">📍 Resultado: '+get_ideology_name(st.session_state.x, st.session_state.y)+'</div>', unsafe_allow_html=True)
    
    xf = max(-10, min(10, st.session_state.x))
    yf = max(-10, min(10, st.session_state.y))

    # Generar HTML de líderes
    l_html = ""
    for l in LEADERS:
        # Coordenadas 5% a 95% para evitar bordes
        pos_x = 50 + (l["x"] * 4.5)
        pos_y = 50 - (l["y"] * 4.5)
        l_html += f'''
            <div class="dot" style="left:{pos_x}%; top:{pos_y}%; background:{l["c"]};"></div>
            <div class="label-leader" style="left:{pos_x}%; top:{pos_y}%;">{l["n"]}</div>
        '''

    chart_html = f'''
    <div style="display:flex; justify-content:center; margin:20px 0;">
        <div style="position:relative; width:580px; height:580px; background:white; border:3px solid #333; overflow:visible;">
            <div style="position:absolute; width:50%; height:50%; top:0; left:0; background:rgba(255,0,0,0.12);"></div>
            <div style="position:absolute; width:50%; height:50%; top:0; right:0; background:rgba(0,0,255,0.12);"></div>
            <div style="position:absolute; width:50%; height:50%; bottom:0; left:0; background:rgba(0,255,0,0.12);"></div>
            <div style="position:absolute; width:50%; height:50%; bottom:0; right:0; background:rgba(255,255,0,0.12);"></div>
            <div style="position:absolute; width:100%; height:2px; top:50%; background:#444;"></div>
            <div style="position:absolute; width:2px; height:100%; left:50%; background:#444;"></div>
            {l_html}
            <div style="position:absolute; left:{50+(xf*4.5)}%; top:{50-(yf*4.5)}%; width:22px; height:22px; background:red; border:4px solid white; border-radius:50%; transform:translate(-50%,-50%); z-index:100; box-shadow:0 0 15px red;"></div>
            <div style="position:absolute; left:{50+(xf*4.5)}%; top:{50-(yf*4.5)-5}%; color:red; font-weight:900; transform:translate(-50%, -100%); z-index:101; font-size:16px;">TÚ</div>
            <div style="position:absolute; top:5px; left:43%; font-weight:bold; font-size:12px;">AUTORITARIO</div>
            <div style="position:absolute; bottom:5px; left:43%; font-weight:bold; font-size:12px;">LIBERTARIO</div>
        </div>
    </div>
    '''
    components.html(chart_html, height=620)

    # Botones de Acción Final
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🖨️ IMPRIMIR / PDF"):
            components.html("<script>window.print();</script>", height=0)
    with c2:
        if st.button("🔄 REPETIR TEST"):
            st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})
            st.rerun()

# --- PANTALLA DE PREGUNTAS ---
else:
    st.markdown('<div class="main-title">Compás Político Estudiantil</div>', unsafe_allow_html=True)
    
    # Advertencia en la primera pregunta
    if st.session_state.idx == 0:
        st.markdown('<div class="warning-box"><b>⚠️ ATENCIÓN:</b> Responde según tu opinión personal. No pienses en lo que es "correcto", sino en lo que realmente crees.</div>', unsafe_allow_html=True)
    
    st.progress(st.session_state.idx / len(questions))
    st.markdown(f'<div class="question-box">{questions[st.session_state.idx]["t"]}</div>', unsafe_allow_html=True)
    
    # Bloque de respuestas
    st.button("✅ Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("👍 De acuerdo", on_click=responder, args=(1,))
    st.button("😐 Neutral / No lo sé", on_click=responder, args=(0,))
    st.button("👎 En desacuerdo", on_click=responder, args=(-1,))
    st.button("❌ Totalmente en desacuerdo", on_click=responder, args=(-2,))

    # Barra separadora y botón volver
    if st.session_state.idx > 0:
        st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
        if st.button("⬅️ VOLVER A LA ANTERIOR"):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px
            st.session_state.y -= py
            st.session_state.idx -= 1
            st.rerun()
