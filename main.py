import streamlit as st
import streamlit.components.v1 as components
import math

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Compás Político", layout="centered")

# 2. ESTILOS CSS
st.markdown("""
    <style>
    .stApp { background-color: #E0F2FE; }
    .main .block-container { max-width: 900px; display: flex; flex-direction: column; align-items: center; }
    
    .main-title { font-size: 55px; font-weight: 950; color: #1E3A8A; text-align: center; width: 100%; margin-bottom: 10px; }
    .welcome-text { font-size: 20px; color: #1E40AF; text-align: center; margin-bottom: 30px; font-weight: 500; }
    .warning-box { background-color: #FFFFFF; border: 2px solid #3B82F6; border-radius: 15px; padding: 20px; text-align: center; color: #1E40AF; font-weight: 700; font-size: 18px; margin-bottom: 25px; width: 100%; }
    
    .q-counter { font-size: 18px; color: #1E40AF; font-weight: 800; margin-bottom: -35px; text-transform: uppercase; }
    
    .question-container { margin: 45px auto; width: 100%; text-align: center; min-height: 130px; display: flex; align-items: center; justify-content: center; }
    .question-text { font-size: 32px !important; font-weight: 800; color: #1E3A8A; line-height: 1.2; }
    
    .result-bubble { background-color: white; border-radius: 35px; padding: 40px; box-shadow: 0 15px 30px rgba(0,0,0,0.1); border: 3px solid #60A5FA; text-align: center; margin: 20px auto; width: 100%; }
    .ideology-title { font-size: 38px !important; font-weight: 950; color: #2563EB; margin: 0; text-transform: uppercase; }
    .ideology-desc { font-size: 18px !important; color: #334155; margin-top: 20px; line-height: 1.6; text-align: justify; font-weight: 400; }

    div.stButton > button { width: 100% !important; max-width: 650px !important; height: 58px !important; border-radius: 15px !important; font-size: 20px !important; background-color: #FFFFFF !important; color: #1E40AF !important; border: 2px solid #BFDBFE !important; border-bottom: 5px solid #BFDBFE !important; margin: 10px auto !important; display: block !important; font-weight: 700; transition: 0.2s; }
    div.stButton > button:hover { background-color: #F0F9FF !important; border-color: #3B82F6 !important; }
    
    .leader-match { background: white; border: 1px solid #BFDBFE; border-radius: 12px; padding: 12px; margin: 6px 0; display: flex; justify-content: space-between; color: #1E293B; font-weight: 700; font-size: 17px; width: 100%; max-width: 600px; }
    </style>
    """, unsafe_allow_html=True)

# 3. BASE DE DATOS LÍDERES
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

# 4. PREGUNTAS (85 EN TOTAL)
# Se asume que la lista completa de 85 preguntas está integrada aquí...
questions = [
    # ECONÓMICAS
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
    
    # SOCIALES
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

# 5. LÓGICA DE ESTADO
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

# 6. DESCRIPIÓN LARGA DE IDEOLOGÍAS
def get_long_desc(x, y):
    if y > 6:
        if x < -6: return "Marxismo-Leninismo", "Buscas una sociedad donde el Estado controle todo para eliminar las diferencias de dinero. Crees que la disciplina y el control de la economía son la única forma de conseguir justicia para los trabajadores."
        if -6 <= x < -2: return "Nacionalbolchevismo", "Una mezcla rara: quieres una economía donde el Estado mande mucho, pero a la vez eres super nacionalista. Valoras las tradiciones de tu país tanto como el reparto de la riqueza."
        if -2 <= x <= 2: return "Totalitarismo", "Para ti, el Estado es lo más importante que existe. Crees que las libertades personales no importan tanto como la seguridad, el orden y cumplir los objetivos del gobierno."
        if 2 < x <= 6: return "Fascismo Clásico", "Defiendes un Estado fuerte que una a toda la nación por encima de todo. Crees en la jerarquía, el orden militar y que todo el mundo debe trabajar unido por el orgullo nacional."
        return "Derecha Radical Autoritaria", "Tu visión se basa en mantener las tradiciones y el orden a toda costa, usando un Estado muy fuerte y un mercado que sirva sobre todo a los intereses del país."
    elif 2 < y <= 6:
        if x < -6: return "Socialismo de Estado", "Crees que el gobierno debe gestionar casi todo para que nadie sea pobre, aunque eso signifique perder algo de libertad individual. El bienestar de todos va antes que los negocios privados."
        if -6 <= x < -2: return "Populismo de Izquierda", "Te centras en luchar contra los de arriba (élites). Quieres un Estado que proteja a la gente común y reparta el dinero, usando el apoyo de la mayoría para cambiar las cosas."
        if -2 <= x <= 2: return "Estatismo", "Crees que el capitalismo solo va bien si el gobierno lo vigila de cerca. Defiendes que la gente tenga sus cosas, pero quieres que el Estado intervenga para que haya orden y equilibrio social."
        if 2 < x <= 6: return "Conservadurismo", "Valoras la estabilidad y las tradiciones. Crees en el libre mercado, pero piensas que el Estado debe estar ahí para proteger la moral y que las cosas no cambien de forma loca de un día para otro."
        return "Derecha Autoritaria", "Te gusta que el mercado sea muy libre y el Estado no se meta en economía, pero exiges mucha policía, fronteras fuertes y leyes estrictas para que la sociedad funcione como debe."
    elif -2 <= y <= 2:
        if x < -6: return "Socialismo Democrático", "Buscas que la economía sea de todos pero de forma democrática, sin dictaduras. Crees que el sistema debe servir a las personas y no solo para que unos pocos se forren."
        if -6 <= x < -2: return "Socialdemocracia", "Eres el defensor del 'Estado del Bienestar'. Te parece bien que haya empresas, pero quieres impuestos altos a los ricos para pagar sanidad, educación y ayudas para todo el mundo."
        if -2 <= x <= 2: return "Centrismo", "Pasas de los extremos. Buscas soluciones prácticas: un poco de libertad económica para que el país crezca, pero con ayudas sociales y leyes que protejan a los ciudadanos."
        if 2 < x <= 6: return "Liberalismo Moderno", "Tu prioridad es que cada uno haga lo que quiera. Defiendes un mercado con mucha chispa y libertades sociales a tope, dejando que el Estado solo se meta si algo va muy mal."
        return "Liberalismo Clásico", "Crees que el mercado se arregla solo y que el Estado debería ser mini. Lo más importante para ti es proteger la vida, la libertad y que nadie te toque lo que es tuyo."
    elif -6 < y <= -2:
        if x < -6: return "Anarcosindicalismo", "Te gustaría una sociedad organizada por los propios trabajadores en sindicatos. No quieres jefes ni políticos, solo gente cooperando de forma libre y colectiva."
        if -6 <= x < -2: return "Socialismo Libertario", "Quieres igualdad económica pero odias que alguien te mande. Crees en comunidades donde la gente comparta lo que tiene voluntariamente, sin necesidad de un gobierno central."
        if -2 <= x <= 2: return "Libertarismo Progresista", "Quieres libertad total en temas sociales (aborto, drogas, derechos) pero aceptas que el Estado mantenga algunas ayudas básicas para que todo el mundo tenga una oportunidad al empezar."
        if 2 < x <= 6: return "Minarquismo", "Crees que el Estado solo debe existir para la policía y la justicia. Cualquier otra cosa que haga el gobierno te parece que es meterse donde no le llaman y quitarte libertad."
        return "Paleolibertarismo", "Quieres un mercado libre a tope y sin Estado, pero en lo personal te gustan los valores tradicionales. Crees que la libertad económica es la clave, pero que la moral es importante para que la sociedad no se hunda."
    else:
        if x < -6: return "Anarcocomunismo", "Sueñas con un mundo sin Estado, sin dinero y sin propiedad privada. Crees que todo debería ser de todos y que cada uno aporte lo que pueda y reciba lo que necesite."
        if -6 <= x < -2: return "Mutualismo", "Propones un mercado libre de verdad, sin Estado ni bancos centrales. Crees en cooperativas donde la gente se ayude mutuamente y el intercambio sea justo para todos."
        if -2 <= x <= 2: return "Anarquismo Individualista", "Para ti lo más importante eres TÚ. Pasas de cualquier institución que te diga qué hacer. Defiendes una autonomía total donde nadie tenga poder sobre nadie más."
        if 2 < x <= 6: return "Voluntarismo", "Crees que todas las relaciones humanas deben ser porque ambas partes quieran. Odias al Estado porque te obliga a hacer cosas, y defiendes que la libertad de elegir es la base de todo."
        return "Anarcocapitalismo", "Crees que el Estado es un robo. Quieres que todo se privatice (carreteras, justicia, seguridad...) y confías en que el mercado libre sea el que organice el mundo de forma perfecta."

# --- PANTALLA RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown('<h1 class="main-title">Compás Político</h1>', unsafe_allow_html=True)
    x, y = max(min(st.session_state.x, 10), -10), max(min(st.session_state.y, 10), -10)
    id_nom, id_desc = get_long_desc(x, y)
    
    st.markdown(f'<div class="result-bubble"><p class="ideology-title">{id_nom}</p><p class="ideology-desc">{id_desc}</p></div>', unsafe_allow_html=True)

    # Gráfico del Compás
    leaders_html = "".join([f"""
        <div style="position:absolute; width:10px; height:10px; background:{l['c']}; border-radius:50%; left:{50 + (l['x']*4.6)}%; top:{50 - (l['y']*4.6)}%; transform:translate(-50%,-50%); border:1px solid black; z-index:5;"></div>
        <div style="position:absolute; font-size:11px; font-weight:900; left:{50 + (l['x']*4.6)}%; top:{50 - (l['y']*4.6)}%; transform:translate(-50%, 8px); color:#1E293B; z-index:6; white-space:nowrap; text-shadow: 1px 1px white;">{l['n']}</div>
    """ for l in LEADERS])

    compass_code = f"""
    <div style="position:relative; width:650px; height:650px; margin:20px auto; background:white; border:4px solid #1e293b; overflow:hidden; border-radius:15px; font-family: sans-serif;">
        <div style="position:absolute; width:50%; height:50%; top:0; left:0; background:rgba(239,68,68,0.2);"></div>
        <div style="position:absolute; width:50%; height:50%; top:0; right:0; background:rgba(59,130,246,0.2);"></div>
        <div style="position:absolute; width:50%; height:50%; bottom:0; left:0; background:rgba(34,197,94,0.2);"></div>
        <div style="position:absolute; width:50%; height:50%; bottom:0; right:0; background:rgba(234,179,8,0.2);"></div>
        <div style="position:absolute; width:100%; height:3px; background:#1e293b; top:50%;"></div>
        <div style="position:absolute; width:3px; height:100%; background:#1e293b; left:50%;"></div>
        {leaders_html}
        <div style="position:absolute; width:18px; height:18px; background:red; border:3px solid white; border-radius:50%; left:{50+(x*4.6)}%; top:{50-(y*4.6)}%; transform:translate(-50%,-50%); z-index:100; box-shadow:0 0 10px rgba(255,0,0,0.5);"></div>
        <div style="position:absolute; color:red; font-weight:1000; font-size:20px; left:{50+(x*4.6)}%; top:{50-(y*4.6)}%; transform:translate(-50%, {"-35px" if y < -8 else "18px"}); z-index:101; text-shadow:2px 2px white, -2px -2px white;">TÚ</div>
    </div>
    """
    components.html(compass_code, height=680)

    st.markdown("<h2 style='text-align:center; color:#1E3A8A;'>¿A quién te pareces más?</h2>", unsafe_allow_html=True)
    for l in LEADERS: l['match'] = max(0, 100 - (math.sqrt((x-l['x'])**2 + (y-l['y'])**2) * 5.5))
    for l in sorted(LEADERS, key=lambda k: k['match'], reverse=True)[:3]:
        st.markdown(f'<div class="leader-match"><span>{l["n"]}</span><span>{l["match"]:.1f}%</span></div>', unsafe_allow_html=True)

    # BOTONES FINALES
    if st.button("🖨️ GUARDAR / IMPRIMIR RESULTADOS"):
        components.html("<script>window.print();</script>", height=0)
    if st.button("🔄 VOLVER A EMPEZAR"):
        st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})
        st.rerun()

# --- PANTALLA PREGUNTAS ---
else:
    st.markdown('<h1 class="main-title">Compás Político</h1>', unsafe_allow_html=True)
    
    if st.session_state.idx == 0:
        st.markdown('<p class="welcome-text">¡Hola! Descubre cuál es tu verdadera ideología política con este test de 85 preguntas. No hay respuestas correctas o incorrectas, solo tu opinión.</p>', unsafe_allow_html=True)
        st.markdown('<div class="warning-box">Responde lo que pienses de verdad. Si no entiendes alguna pregunta, usa el botón "Neutral".</div>', unsafe_allow_html=True)
    
    st.markdown(f'<p class="q-counter">Pregunta {st.session_state.idx + 1} de 85</p>', unsafe_allow_html=True)
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
