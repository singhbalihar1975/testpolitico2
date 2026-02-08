import streamlit as st
import streamlit.components.v1 as components
import math

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Compás Político Pro", layout="centered")

# 2. ESTILOS CSS (Centrado y Diseño de Carnet)
st.markdown("""
    <style>
    .stApp { background-color: #F0F4F8; }
    
    /* Centrado Global */
    .main .block-container {
        max-width: 800px;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }

    .main-title { font-size: 50px; font-weight: 900; color: #1E3A8A; text-align: center; margin-bottom: 10px; }
    
    .question-container { margin: 40px auto; text-align: center; width: 100%; }
    .question-text { font-size: 28px !important; font-weight: 700; color: #1E40AF; }

    /* Botones Azules */
    div.stButton > button {
        width: 100% !important; max-width: 550px !important; height: 55px !important;
        border-radius: 15px !important; font-size: 19px !important;
        background-color: #DBEAFE !important; color: #1E40AF !important;
        border: 1px solid #BFDBFE !important; border-bottom: 4px solid #A5C9F8 !important;
        margin: 8px auto !important; display: block !important; font-weight: 700;
    }

    /* BURBUJA RESULTADO */
    .result-bubble {
        background: white; border-radius: 25px; padding: 40px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 2px solid #BFDBFE;
        text-align: center; margin: 20px auto; width: 100%;
    }
    .ideology-title { font-size: 45px !important; font-weight: 900; color: #2563EB; margin: 0; }

    /* CARNET POLÍTICO */
    .id-card {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white; border-radius: 20px; padding: 25px; width: 100%; max-width: 500px;
        margin: 20px auto; text-align: left; box-shadow: 0 15px 35px rgba(30,58,138,0.3);
        position: relative; overflow: hidden;
    }
    .id-card::after { content: "CERTIFIED"; position: absolute; right: -20px; bottom: 10px; opacity: 0.1; font-size: 40px; font-weight: 900; transform: rotate(-15deg); }
    .id-header { font-size: 12px; letter-spacing: 2px; opacity: 0.8; }
    .id-name { font-size: 24px; font-weight: 800; margin: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 5px; }
    .id-stat { font-size: 14px; margin: 5px 0; }
    
    .leader-match { background: #F1F5F9; border-radius: 12px; padding: 10px; margin: 5px 0; display: flex; justify-content: space-between; align-items: center; color: #1E293B; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# 3. BASE DE DATOS: LÍDERES
LEADERS = [
    {"n": "Stalin", "x": -9, "y": 9, "c": "#C53030"}, {"n": "Hitler", "x": 8, "y": 9.5, "c": "#2D3748"},
    {"n": "Mao", "x": -9.5, "y": 8.5, "c": "#E53E3E"}, {"n": "Gandhi", "x": -6.5, "y": -7.5, "c": "#48BB78"},
    {"n": "Thatcher", "x": 7.5, "y": 6.5, "c": "#3182CE"}, {"n": "Milei", "x": 9.2, "y": -8.8, "c": "#D69E2E"},
    {"n": "Castro", "x": -8.5, "y": 7, "c": "#2F855A"}, {"n": "Friedman", "x": 8.5, "y": -6, "c": "#ECC94B"},
    {"n": "Sanders", "x": -5.5, "y": -2, "c": "#4299E1"}, {"n": "Pinochet", "x": 8.8, "y": 8, "c": "#1A202C"},
    {"n": "Chomsky", "x": -8.5, "y": -8.5, "c": "#38A169"}, {"n": "Rothbard", "x": 10, "y": -10, "c": "#F6E05E"},
    {"n": "Obama", "x": 2.5, "y": 1.5, "c": "#2B6CB0"}, {"n": "Mandela", "x": -3, "y": -3, "c": "#48BB78"},
    {"n": "Churchill", "x": 6, "y": 5, "c": "#2C5282"}, {"n": "Lenin", "x": -8.5, "y": 8, "c": "#C53030"}, 
    {"n": "Trump", "x": 6.5, "y": 5.5, "c": "#E53E3E"}, {"n": "Biden", "x": 3, "y": 2, "c": "#3182CE"}, 
    {"n": "Merkel", "x": 2.5, "y": 3, "c": "#4A5568"}, {"n": "Bukele", "x": 5, "y": 7, "c": "#2D3748"}, 
    {"n": "Putin", "x": 7, "y": 8.5, "c": "#2B6CB0"}, {"n": "Sánchez", "x": -2.5, "y": 1, "c": "#F56565"}, 
    {"n": "Abascal", "x": 7.5, "y": 7.5, "c": "#38A169"}, {"n": "Díaz", "x": -6, "y": -2, "c": "#ED64A6"}, 
    {"n": "Bolsonaro", "x": 8, "y": 6.5, "c": "#48BB78"}, {"n": "Lula", "x": -4.5, "y": 1.5, "c": "#E53E3E"}, 
    {"n": "Jefferson", "x": 4, "y": -7.5, "c": "#D69E2E"}, {"n": "Robespierre", "x": -4, "y": 9, "c": "#C53030"}, 
    {"n": "Mussolini", "x": 7.5, "y": 9.5, "c": "#1A202C"}, {"n": "Keynes", "x": -3, "y": 2, "c": "#63B3ED"}, 
    {"n": "Hayek", "x": 9, "y": -7, "c": "#F6E05E"}, {"n": "Che Guevara", "x": -9, "y": 6, "c": "#2F855A"}, 
    {"n": "Franco", "x": 7, "y": 9, "c": "#2D3748"}, {"n": "Kropotkin", "x": -10, "y": -10, "c": "#000000"}, 
    {"n": "Malatesta", "x": -9, "y": -9.5, "c": "#4A5568"}, {"n": "Rousseau", "x": -5, "y": 4, "c": "#4299E1"}, 
    {"n": "Voltaire", "x": 5, "y": -3, "c": "#ECC94B"}, {"n": "Locke", "x": 6, "y": -5, "c": "#3182CE"}, 
    {"n": "Rand", "x": 9.5, "y": -8, "c": "#718096"}, {"n": "Gaddafi", "x": -2, "y": 8, "c": "#38A169"}, 
    {"n": "Kim Jong-un", "x": -9.5, "y": 10, "c": "#E53E3E"}, {"n": "Macron", "x": 4, "y": 3, "c": "#3182CE"}, 
    {"n": "Trudeau", "x": -1.5, "y": -1.5, "c": "#ED64A6"}, {"n": "Meloni", "x": 7, "y": 6, "c": "#2C5282"}, 
    {"n": "Mujica", "x": -7, "y": -4, "c": "#48BB78"}
]

# 4. PREGUNTAS (85)
questions = [
    # Económicas (x)
    {"t": "El gobierno no debería decir a las empresas cuánto pagar a sus empleados.", "a": "x", "v": 1},
    {"t": "La sanidad debería ser gratis y pagada con los impuestos de todos.", "a": "x", "v": -1},
    {"t": "El Estado debería ser el dueño de las empresas de luz y agua.", "a": "x", "v": -1},
    {"t": "Es mejor que los colegios sean privados para que haya competencia.", "a": "x", "v": 1},
    {"t": "Los que más dinero ganan deben pagar muchos más impuestos.", "a": "x", "v": -1},
    {"t": "El gobierno debería poner límites al precio de la comida básica.", "a": "x", "v": -1},
    {"t": "Si una empresa va a quebrar, el gobierno no debería ayudarla.", "a": "x", "v": 1},
    {"t": "Es mejor comprar productos de nuestro país que traerlos de fuera.", "a": "x", "v": -1},
    {"t": "Abrir un negocio debería ser fácil y sin tantos permisos del gobierno.", "a": "x", "v": 1},
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
    # Sociales (y)
    {"t": "La disciplina y la obediencia son lo más importante en la educación.", "a": "y", "v": 1},
    {"t": "La libertad de expresión debe ser total, aunque alguien se ofenda.", "a": "y", "v": -1},
    {"t": "Hace falta mucha más policía en las calles.", "a": "y", "v": 1},
    {"t": "El aborto debe ser una decisión libre de la mujer.", "a": "y", "v": -1},
    {"t": "Un país necesita un líder fuerte que tome decisiones rápidas.", "a": "y", "v": 1},
    {"t": "La religión no tiene sitio en la política moderna.", "a": "y", "v": -1},
    {"t": "Gastar más dinero en el ejército es necesario.", "a": "y", "v": 1},
    {"t": "Ayudar a morir a un enfermo terminal debe ser legal.", "a": "y", "v": -1},
    {"t": "El gobierno debería controlar lo que se publica en internet.", "a": "y", "v": 1},
    {"t": "Lo que haga un adulto en su casa no es asunto del Estado.", "a": "y", "v": -1},
    {"t": "Nuestra cultura nacional es superior a otras.", "a": "y", "v": 1},
    {"t": "El matrimonio debe ser solo entre hombre y mujer.", "a": "y", "v": 1},
    {"t": "Las cámaras de vigilancia en la calle nos hacen más libres.", "a": "y", "v": 1},
    {"t": "Se debe legalizar el consumo de marihuana.", "a": "y", "v": -1},
    {"t": "Hay que endurecer las fronteras para frenar la inmigración.", "a": "y", "v": 1},
    {"t": "La bandera es el símbolo más sagrado de un ciudadano.", "a": "y", "v": 1},
    {"t": "Cortar una carretera en una protesta debería ser cárcel.", "a": "y", "v": 1},
    {"t": "Las tradiciones religiosas son la base de nuestra moral.", "a": "y", "v": 1},
    {"t": "El Estado no debería pedirnos el DNI para todo.", "a": "y", "v": -1},
    {"t": "La cadena perpetua es necesaria para asesinos.", "a": "y", "v": 1},
    {"t": "El orden público es más importante que los derechos individuales.", "a": "y", "v": 1},
    {"t": "La justicia protege demasiado a los delincuentes.", "a": "y", "v": 1},
    {"t": "Los hijos pertenecen a los padres, no al Estado.", "a": "y", "v": 1},
    {"t": "Quemar la bandera nacional debería ser delito.", "a": "y", "v": 1},
    {"t": "El porno hace mucho daño a la sociedad y debe controlarse.", "a": "y", "v": 1},
    {"t": "Las cuotas de género son injustas.", "a": "y", "v": 1},
    {"t": "El servicio militar debería volver a ser obligatorio.", "a": "y", "v": 1},
    {"t": "La policía debería poder registrar a sospechosos sin orden judicial.", "a": "y", "v": 1},
    {"t": "La educación sexual no debe darse en los colegios.", "a": "y", "v": 1},
    {"t": "Blasfemar debe estar castigado.", "a": "y", "v": 1},
    {"t": "La globalización destruye la identidad de nuestro país.", "a": "y", "v": 1},
    {"t": "La experimentación con células madre debe ser libre.", "a": "y", "v": -1},
    {"t": "La autoridad de un profesor nunca debe cuestionarse.", "a": "y", "v": 1},
    {"t": "El arte moderno es a veces una falta de respeto.", "a": "y", "v": 1},
    {"t": "Las cárceles deben ser lugares de castigo duro.", "a": "y", "v": 1},
    {"t": "Prohibiría el tabaco si pudiera.", "a": "y", "v": 1},
    {"t": "La unidad del país es más importante que el derecho a decidir.", "a": "y", "v": 1},
    {"t": "El gobierno debe premiar a quienes tengan muchos hijos.", "a": "y", "v": 1},
    {"t": "Las redes sociales nos están volviendo maleducados.", "a": "y", "v": 1},
    {"t": "Tener un arma en casa para defensa debería ser un derecho.", "a": "y", "v": -1},
    {"t": "Los antepasados y la patria son sagrados.", "a": "y", "v": 1},
    {"t": "Un buen ciudadano siempre obedece la ley sin preguntar.", "a": "y", "v": 1}
]

# 5. LÓGICA DE CALCULO
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})

def responder(puntos):
    q = questions[st.session_state.idx]
    total_eje = len([qu for qu in questions if qu["a"] == q["a"]])
    val = (puntos / 2) * (10 / (total_eje / 2)) * q["v"]
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    st.session_state.idx += 1

# --- PANTALLA RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown('<h1 class="main-title">Análisis Final</h1>', unsafe_allow_html=True)
    x, y = max(min(st.session_state.x, 10), -10), max(min(st.session_state.y, 10), -10)

    # Lógica de Ideologías (Recortada para el script)
    id_nom, desc = "Centro", "Postura equilibrada."
    if y > 4:
        if x < -4: id_nom, desc = "Socialismo Autoritario", "Control estatal de la economía con orden social estricto."
        elif x > 4: id_nom, desc = "Derecha Nacionalista", "Libre mercado combinado con autoridad nacional fuerte."
        else: id_nom, desc = "Estatismo", "El Estado como guía principal de la sociedad."
    elif y < -4:
        if x < -4: id_nom, desc = "Anarco-Socialismo", "Libertad total y propiedad comunal."
        elif x > 4: id_nom, desc = "Libertarismo de Derecha", "Mínimo Estado y máxima propiedad privada."
        else: id_nom, desc = "Libertarismo Progresista", "Autonomía individual máxima."
    else:
        if x < -4: id_nom, desc = "Socialdemocracia", "Bienestar social dentro de un sistema democrático."
        elif x > 4: id_nom, desc = "Liberalismo Clásico", "Libertad económica con gobierno limitado."
        else: id_nom, desc = "Centrismo", "Moderación y pragmatismo."

    # 1. CÁLCULO DE AFINIDAD (Opción 1)
    for l in LEADERS:
        dist = math.sqrt((x - l['x'])**2 + (y - l['y'])**2)
        l['match'] = max(0, 100 - (dist * 5))
    top_matches = sorted(LEADERS, key=lambda k: k['match'], reverse=True)[:3]

    # 3. CARNET POLÍTICO (Opción 3)
    st.markdown(f"""
    <div class="id-card">
        <div class="id-header">POLITICAL IDENTITY CARD</div>
        <div class="id-name">{id_nom}</div>
        <div class="id-stat"><b>Eje Económico:</b> {"Derecha" if x>0 else "Izquierda"} ({abs(x):.1f})</div>
        <div class="id-stat"><b>Eje Social:</b> {"Autoritario" if y>0 else "Libertario"} ({abs(y):.1f})</div>
        <div class="id-stat" style="margin-top:10px; font-size:11px; opacity:0.8;">Esta tarjeta certifica tu posición en el espectro político actual.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="result-bubble"><p class="ideology-desc">{desc}</p></div>', unsafe_allow_html=True)

    # GRÁFICO
    leaders_html = "".join([f"""<div style="position:absolute; width:6px; height:6px; background:{l['c']}; border-radius:50%; left:{50 + (l['x']*4.6)}%; top:{50 - (l['y']*4.6)}%; transform:translate(-50%,-50%); border:0.5px solid black; z-index:2;"></div>""" for l in LEADERS])
    label_y = "-28px" if y < -8 else "15px"
    compass_code = f"""
    <div style="position:relative; width:580px; height:580px; margin:20px auto; background:white; border:3px solid #1e293b; overflow:hidden; border-radius:15px;">
        <div style="position:absolute; width:50%; height:50%; top:0; left:0; background:rgba(239,68,68,0.1);"></div>
        <div style="position:absolute; width:50%; height:50%; top:0; right:0; background:rgba(59,130,246,0.1);"></div>
        <div style="position:absolute; width:50%; height:50%; bottom:0; left:0; background:rgba(34,197,94,0.1);"></div>
        <div style="position:absolute; width:50%; height:50%; bottom:0; right:0; background:rgba(234,179,8,0.1);"></div>
        <div style="position:absolute; width:100%; height:2px; background:#1e293b; top:50%;"></div>
        <div style="position:absolute; width:2px; height:100%; background:#1e293b; left:50%;"></div>
        {leaders_html}
        <div style="position:absolute; width:18px; height:18px; background:red; border:3px solid white; border-radius:50%; left:{50+(x*4.6)}%; top:{50-(y*4.6)}%; transform:translate(-50%,-50%); z-index:100; box-shadow:0 0 10px rgba(255,0,0,0.5);"></div>
        <div style="position:absolute; color:red; font-weight:900; font-size:18px; left:{50+(x*4.6)}%; top:{50-(y*4.6)}%; transform:translate(-50%, {label_y}); z-index:101; text-shadow:2px 2px white, -2px -2px white;">TÚ</div>
    </div>
    """
    components.html(compass_code, height=620)

    # MOSTRAR AFINIDADES
    st.markdown("<h3 style='text-align:center;'>Afinidad con Líderes</h3>", unsafe_allow_html=True)
    for l in top_matches:
        st.markdown(f"""<div class="leader-match"><span>{l['n']}</span><span>{l['match']:.1f}%</span></div>""", unsafe_allow_html=True)

    if st.button("🔄 REPETIR TEST"):
        st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})
        st.rerun()

# --- PANTALLA PREGUNTAS ---
else:
    st.markdown(f'<h1 class="main-title">Compás Político</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; font-weight:bold; color:#64748B;">Pregunta {st.session_state.idx+1} de {len(questions)}</p>', unsafe_allow_html=True)
    st.progress(st.session_state.idx / len(questions))
    
    st.markdown(f'<div class="question-container"><span class="question-text">{questions[st.session_state.idx]["t"]}</span></div>', unsafe_allow_html=True)
    
    st.button("✅ Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("👍 De acuerdo", on_click=responder, args=(1,))
    st.button("😐 Neutral / No lo sé", on_click=responder, args=(0,))
    st.button("👎 En desacuerdo", on_click=responder, args=(-1,))
    st.button("❌ Totalmente en desacuerdo", on_click=responder, args=(-2,))

    if st.session_state.idx > 0:
        if st.button("⬅️ ANTERIOR"):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px; st.session_state.y -= py
            st.session_state.idx -= 1; st.rerun()
