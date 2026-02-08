import streamlit as st
import streamlit.components.v1 as components
import math

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Compás Político", layout="centered")

# 2. ESTILOS CSS (Mejorados para impresión y espaciado)
st.markdown("""
    <style>
    /* Fondo y contenedores */
    .stApp { background-color: #E0F2FE; }
    .main .block-container { max-width: 900px; padding-top: 2rem; }
    
    /* Títulos y Bienvenida */
    .main-title { font-size: 50px; font-weight: 900; color: #1E3A8A; text-align: center; margin-bottom: 5px; }
    .welcome-text { font-size: 19px; color: #1E40AF; text-align: center; margin-bottom: 20px; font-weight: 500; }
    .warning-box { background-color: #FFFFFF; border: 2px solid #3B82F6; border-radius: 15px; padding: 20px; text-align: center; color: #1E40AF; font-weight: 700; margin-bottom: 30px; }
    
    /* Separación del contador y la barra */
    .q-counter { 
        font-size: 18px; 
        color: #1E40AF; 
        font-weight: 800; 
        margin-bottom: 15px; /* Espacio extra aquí */
        text-transform: uppercase; 
        display: block;
    }
    
    /* Pregunta */
    .question-container { margin: 40px 0; text-align: center; min-height: 120px; display: flex; align-items: center; justify-content: center; }
    .question-text { font-size: 30px !important; font-weight: 800; color: #1E3A8A; line-height: 1.2; }
    
    /* Botones de respuesta */
    div.stButton > button { 
        width: 100% !important; 
        height: 55px !important; 
        border-radius: 12px !important; 
        font-size: 18px !important; 
        background-color: #FFFFFF !important; 
        color: #1E40AF !important; 
        border: 2px solid #BFDBFE !important; 
        border-bottom: 4px solid #BFDBFE !important; 
        margin-bottom: 10px !important; 
        font-weight: 700; 
    }
    div.stButton > button:hover { background-color: #F0F9FF !important; border-color: #3B82F6 !important; }

    /* Resultados e Impresión */
    @media print {
        .stButton, .q-counter, .stProgress, .welcome-text { display: none !important; }
        .stApp { background-color: white !important; }
        .result-bubble { border: 2px solid black !important; box-shadow: none !important; }
    }
    
    .result-bubble { background-color: white; border-radius: 25px; padding: 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 3px solid #60A5FA; text-align: center; margin-bottom: 20px; }
    .ideology-title { font-size: 35px !important; font-weight: 900; color: #2563EB; text-transform: uppercase; margin: 0; }
    .ideology-desc { font-size: 17px !important; color: #334155; margin-top: 15px; text-align: justify; }
    
    .leader-match { background: white; border: 1px solid #BFDBFE; border-radius: 10px; padding: 10px 20px; margin: 5px 0; display: flex; justify-content: space-between; font-weight: 700; color: #1E293B; }
    </style>
    """, unsafe_allow_html=True)

# 3. DATOS (Líderes, Preguntas e Ideologías)
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

questions = [
    # ECONÓMICAS (Factor 10/43)
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
    # SOCIALES (Factor 10/42)
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

def get_long_desc(x, y):
    if y > 6:
        if x < -6: return "Marxismo-Leninismo", "Buscas una sociedad donde el Estado controle todo para eliminar las diferencias de dinero. Crees en la disciplina férrea."
        if -6 <= x < -2: return "Nacionalbolchevismo", "Estado fuerte en lo económico y nacionalismo extremo en lo social."
        if -2 <= x <= 2: return "Totalitarismo", "El Estado es todo, fuera del Estado nada."
        if 2 < x <= 6: return "Fascismo Clásico", "Unidad nacional, jerarquía y un Estado corporativo fuerte."
        return "Derecha Radical Autoritaria", "Tradición, orden y mercado libre pero servil a la nación."
    elif 2 < y <= 6:
        if x < -6: return "Socialismo de Estado", "Gestión pública total para la igualdad social con autoridad."
        if -6 <= x < -2: return "Populismo de Izquierda", "Lucha contra las élites con un Estado protector."
        if -2 <= x <= 2: return "Estatismo", "Capitalismo vigilado y regulado por un gobierno fuerte."
        if 2 < x <= 6: return "Conservadurismo", "Tradiciones, libre mercado y orden institucional."
        return "Derecha Autoritaria", "Leyes muy estrictas y economía de libre mercado absoluta."
    elif -2 <= y <= 2:
        if x < -6: return "Socialismo Democrático", "Igualdad económica lograda a través de la democracia."
        if -6 <= x < -2: return "Socialdemocracia", "El modelo de bienestar: mercado con muchos servicios públicos."
        if -2 <= x <= 2: return "Centrismo", "Equilibrio entre libertad y protección social."
        if 2 < x <= 6: return "Liberalismo Moderno", "Libertades individuales y economía dinámica."
        return "Liberalismo Clásico", "Estado mínimo centrado en proteger la propiedad y la libertad."
    elif -6 < y <= -2:
        if x < -6: return "Anarcosindicalismo", "Sociedad organizada por trabajadores sin políticos ni jefes."
        if -6 <= x < -2: return "Socialismo Libertario", "Comunidades libres y solidarias sin autoridad central."
        if -2 <= x <= 2: return "Libertarismo Progresista", "Libertad total en lo personal con justicia social básica."
        if 2 < x <= 6: return "Minarquismo", "El Estado solo para policía y justicia, nada más."
        return "Paleolibertarismo", "Anarcocapitalismo con valores culturales conservadores."
    else:
        if x < -6: return "Anarcocomunismo", "Sin Estado, sin dinero y sin clases sociales."
        if -6 <= x < -2: return "Mutualismo", "Mercado libre basado en la cooperación y el intercambio justo."
        if -2 <= x <= 2: return "Anarquismo Individualista", "Autonomía total del individuo frente a cualquier grupo."
        if 2 < x <= 6: return "Voluntarismo", "Todas las interacciones humanas deben ser voluntarias."
        return "Anarcocapitalismo", "Privatización total de la sociedad y soberanía individual."

# 4. LÓGICA DE NAVEGACIÓN
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})

def responder(puntos):
    q = questions[st.session_state.idx]
    factor = 10 / (43 if q["a"] == "x" else 42)
    val = puntos * factor * q["v"]
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    st.session_state.idx += 1

# --- PANTALLA RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown('<h1 class="main-title">Tus Resultados</h1>', unsafe_allow_html=True)
    x, y = max(min(st.session_state.x, 10), -10), max(min(st.session_state.y, 10), -10)
    id_nom, id_desc = get_long_desc(x, y)
    
    st.markdown(f'<div class="result-bubble"><p class="ideology-title">{id_nom}</p><p class="ideology-desc">{id_desc}</p></div>', unsafe_allow_html=True)

    # Gráfico
    leaders_js = "".join([f"""
        <div style="position:absolute; width:10px; height:10px; background:{l['c']}; border-radius:50%; left:{50 + (l['x']*4.6)}%; top:{50 - (l['y']*4.6)}%; transform:translate(-50%,-50%); border:1px solid black;"></div>
        <div style="position:absolute; font-size:10px; font-weight:bold; left:{50 + (l['x']*4.6)}%; top:{50 - (l['y']*4.6)}%; transform:translate(-50%, 8px); color:black; white-space:nowrap;">{l['n']}</div>
    """ for l in LEADERS])

    compass_html = f"""
    <div id="capture" style="position:relative; width:600px; height:600px; margin:auto; background:white; border:3px solid black; font-family:Arial;">
        <div style="position:absolute; width:50%; height:50%; top:0; left:0; background:rgba(239,68,68,0.15); border-right:1px solid #ccc; border-bottom:1px solid #ccc;"></div>
        <div style="position:absolute; width:50%; height:50%; top:0; right:0; background:rgba(59,130,246,0.15); border-bottom:1px solid #ccc;"></div>
        <div style="position:absolute; width:50%; height:50%; bottom:0; left:0; background:rgba(34,197,94,0.15); border-right:1px solid #ccc;"></div>
        <div style="position:absolute; width:50%; height:50%; bottom:0; right:0; background:rgba(234,179,8,0.15);"></div>
        <div style="position:absolute; width:100%; height:2px; background:black; top:50%;"></div>
        <div style="position:absolute; width:2px; height:100%; background:black; left:50%;"></div>
        {leaders_js}
        <div style="position:absolute; width:16px; height:16px; background:red; border:2px solid white; border-radius:50%; left:{50+(x*4.6)}%; top:{50-(y*4.6)}%; transform:translate(-50%,-50%); z-index:100;"></div>
        <div style="position:absolute; color:red; font-weight:900; left:{50+(x*4.6)}%; top:{50-(y*4.6)}%; transform:translate(-50%, 15px); z-index:101;">TÚ</div>
    </div>
    """
    components.html(compass_html, height=620)

    st.markdown("### Afinidad con líderes")
    for l in LEADERS: l['match'] = max(0, 100 - (math.sqrt((x-l['x'])**2 + (y-l['y'])**2) * 5.5))
    for l in sorted(LEADERS, key=lambda k: k['match'], reverse=True)[:3]:
        st.markdown(f'<div class="leader-match"><span>{l["n"]}</span><span>{l["match"]:.1f}%</span></div>', unsafe_allow_html=True)

    if st.button("🖨️ GUARDAR COMO PDF / IMPRIMIR"):
        # Script mejorado para imprimir
        components.html("<script>setTimeout(function(){ window.print(); }, 500);</script>", height=0)
    
    if st.button("🔄 REPETIR TEST"):
        st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})
        st.rerun()

# --- PANTALLA PREGUNTAS ---
else:
    st.markdown('<h1 class="main-title">Compás Político</h1>', unsafe_allow_html=True)
    
    if st.session_state.idx == 0:
        st.markdown('<p class="welcome-text">Descubre dónde encajas en el mapa político con este test diseñado para jóvenes.</p>', unsafe_allow_html=True)
        st.markdown('<div class="warning-box">Responde con sinceridad. Si no entiendes algo, dale a "Neutral".</div>', unsafe_allow_html=True)
    
    # El contador ahora tiene margen inferior para no pegarse a la barra
    st.markdown(f'<span class="q-counter">Pregunta {st.session_state.idx + 1} de 85</span>', unsafe_allow_html=True)
    st.progress(st.session_state.idx / 85)
    
    st.markdown(f'<div class="question-container"><span class="question-text">{questions[st.session_state.idx]["t"]}</span></div>', unsafe_allow_html=True)
    
    st.button("✅ Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("👍 De acuerdo", on_click=responder, args=(1,))
    st.button("😐 Neutral / No lo sé", on_click=responder, args=(0,))
    st.button("👎 En desacuerdo", on_click=responder, args=(-1,))
    st.button("❌ Totalmente en desacuerdo", on_click=responder, args=(-2,))

    if st.session_state.idx > 0:
        if st.button("⬅️ VOLVER A LA ANTERIOR"):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px; st.session_state.y -= py
            st.session_state.idx -= 1; st.rerun()
