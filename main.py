import streamlit as st
import streamlit.components.v1 as components
import math

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Compás Político Profesional", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #E0F2FE; }
    .main-title { font-size: 55px; font-weight: 950; color: #1E3A8A; text-align: center; margin-bottom: 5px; }
    .welcome-text { font-size: 19px; color: #1E40AF; text-align: center; margin-bottom: 20px; font-weight: 500; }
    .warning-box { background-color: #FFFFFF; border: 2px solid #3B82F6; border-radius: 15px; padding: 25px; text-align: center; color: #1E40AF; font-weight: 700; margin-bottom: 30px; }
    
    .q-counter { font-size: 20px; color: #1E40AF; font-weight: 800; margin-bottom: 20px; display: block; text-transform: uppercase; }
    .stProgress { margin-bottom: 40px !important; }
    
    .question-container { margin: 40px 0; text-align: center; min-height: 120px; display: flex; align-items: center; justify-content: center; }
    .question-text { font-size: 32px !important; font-weight: 800; color: #1E3A8A; line-height: 1.2; }
    
    div.stButton > button { width: 100% !important; height: 55px !important; border-radius: 12px !important; font-size: 19px !important; font-weight: 700; margin-bottom: 12px !important; }

    @media print {
        .stButton, .q-counter, .stProgress, .welcome-text, .warning-box, header, [data-testid="stSidebar"] { display: none !important; }
        .stApp { background-color: white !important; }
        .result-bubble { border: 2px solid black !important; padding: 20px; margin-bottom: 30px; page-break-inside: avoid; }
        .chart-container { width: 100% !important; display: block !important; }
    }
    
    .result-bubble { background-color: white; border-radius: 25px; padding: 35px; border: 4px solid #60A5FA; margin-bottom: 25px; text-align: center; }
    .ideology-title { font-size: 42px !important; font-weight: 900; color: #2563EB; text-transform: uppercase; margin-bottom: 10px; }
    .ideology-desc { font-size: 18px; color: #334155; line-height: 1.5; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS DE LÍDERES (45 Figuras)
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

# 3. LAS 85 PREGUNTAS
questions = [
    # ECONÓMICAS
    {"t": "El salario mínimo debería ser eliminado para que las empresas contraten más.", "a": "x", "v": 1},
    {"t": "La sanidad debe ser 100% pública y gratuita para todos los ciudadanos.", "a": "x", "v": -1},
    {"t": "El Estado debe poseer sectores estratégicos como la energía y el agua.", "a": "x", "v": -1},
    {"t": "Privatizar aeropuertos y trenes mejora la eficiencia del servicio.", "a": "x", "v": 1},
    {"t": "Los impuestos a las grandes fortunas deben subir drásticamente.", "a": "x", "v": -1},
    {"t": "El libre mercado sin regulaciones es el mejor motor de progreso.", "a": "x", "v": 1},
    {"t": "El Estado no debe rescatar empresas privadas con dinero público.", "a": "x", "v": 1},
    {"t": "Es necesario proteger la industria nacional con aranceles.", "a": "x", "v": -1},
    {"t": "La propiedad privada es un derecho humano absoluto e intocable.", "a": "x", "v": 1},
    {"t": "El gobierno debe garantizar un ingreso básico a cada ciudadano.", "a": "x", "v": -1},
    {"t": "Las herencias deberían tener un impuesto muy alto.", "a": "x", "v": -1},
    {"t": "Es injusto que quienes más ganan paguen un porcentaje mayor.", "a": "x", "v": 1},
    {"t": "El capitalismo explota intrínsecamente al trabajador.", "a": "x", "v": -1},
    {"t": "Los sindicatos son necesarios para equilibrar el poder empresarial.", "a": "x", "v": -1},
    {"t": "La competencia es siempre mejor que la planificación estatal.", "a": "x", "v": 1},
    {"t": "El control de precios de alquiler ayuda a los más pobres.", "a": "x", "v": -1},
    {"t": "Los bancos centrales causan inflación y deberían ser cerrados.", "a": "x", "v": 1},
    {"t": "La desigualdad económica es necesaria para incentivar el esfuerzo.", "a": "x", "v": 1},
    {"t": "El Estado debe invertir en ciencia y tecnología aunque no sea rentable.", "a": "x", "v": -1},
    {"t": "Las multinacionales tienen demasiado poder político hoy en día.", "a": "x", "v": -1},
    {"t": "El gasto público es el principal problema de la economía.", "a": "x", "v": 1},
    {"t": "La jubilación debería ser un sistema privado de ahorro personal.", "a": "x", "v": 1},
    {"t": "El medio ambiente es más importante que el crecimiento económico.", "a": "x", "v": -1},
    {"t": "Las criptomonedas no deberían tener ningún control estatal.", "a": "x", "v": 1},
    {"t": "El Estado debería crear empleo directo en tiempos de crisis.", "a": "x", "v": -1},
    {"t": "La especulación financiera debería estar prohibida.", "a": "x", "v": -1},
    {"t": "Los servicios de mensajería deberían ser exclusivamente públicos.", "a": "x", "v": -1},
    {"t": "Bajar impuestos a los ricos termina beneficiando a los pobres.", "a": "x", "v": 1},
    {"t": "La deuda externa de los países pobres debería ser condonada.", "a": "x", "v": -1},
    {"t": "El mercado libre no garantiza que todo el mundo coma.", "a": "x", "v": -1},
    {"t": "Las patentes farmacéuticas deberían ser libres en pandemias.", "a": "x", "v": -1},
    {"t": "La bolsa de valores es una herramienta útil de inversión social.", "a": "x", "v": 1},
    {"t": "El dinero físico debería ser sustituido por dinero digital estatal.", "a": "x", "v": -1},
    {"t": "La caridad privada es mejor que la asistencia del Estado.", "a": "x", "v": 1},
    {"t": "Los paraísos fiscales deberían ser eliminados por ley global.", "a": "x", "v": -1},
    {"t": "El Estado no debería pedir préstamos a bancos privados.", "a": "x", "v": 1},
    {"t": "La jornada laboral debería reducirse por ley sin bajar el sueldo.", "a": "x", "v": -1},
    {"t": "Es justo que el Estado expropie tierras sin uso para cultivos.", "a": "x", "v": -1},
    {"t": "El éxito económico depende más de la suerte que del trabajo.", "a": "x", "v": -1},
    {"t": "La automatización debe ser gravada con impuestos especiales.", "a": "x", "v": -1},
    {"t": "El libre mercado de armas de fuego sería beneficioso.", "a": "x", "v": 1},
    {"t": "La publicidad engañosa no debería ser regulada.", "a": "x", "v": 1},
    {"t": "El Estado debería controlar los tipos de interés.", "a": "x", "v": -1},
    
    # SOCIALES
    {"t": "El aborto debe ser legal y gratuito en cualquier circunstancia.", "a": "y", "v": -1},
    {"t": "Se necesita un líder fuerte para imponer orden en el país.", "a": "y", "v": 1},
    {"t": "La religión no debería influir en absoluto en las leyes.", "a": "y", "v": -1},
    {"t": "El consumo de todas las drogas debería ser legalizado.", "a": "y", "v": -1},
    {"t": "La cadena perpetua es necesaria para delitos graves.", "a": "y", "v": 1},
    {"t": "La identidad nacional es más importante que los derechos globales.", "a": "y", "v": 1},
    {"t": "El matrimonio debe ser exclusivamente entre un hombre y una mujer.", "a": "y", "v": 1},
    {"t": "La vigilancia masiva por cámaras es aceptable para evitar el crimen.", "a": "y", "v": 1},
    {"t": "La libertad de expresión incluye el derecho a ofender.", "a": "y", "v": -1},
    {"t": "La eutanasia es un derecho básico de la persona.", "a": "y", "v": -1},
    {"t": "El servicio militar debería volver a ser obligatorio.", "a": "y", "v": 1},
    {"t": "Las fronteras abiertas benefician a la humanidad.", "a": "y", "v": -1},
    {"t": "La patria es sagrada y merece cualquier sacrificio.", "a": "y", "v": 1},
    {"t": "La educación sexual en las escuelas corrompe a los niños.", "a": "y", "v": 1},
    {"t": "La prostitución debería ser ilegal en todos los casos.", "a": "y", "v": 1},
    {"t": "Quemar la bandera nacional debería conllevar cárcel.", "a": "y", "v": 1},
    {"t": "El feminismo actual ha ido demasiado lejos.", "a": "y", "v": 1},
    {"t": "La experimentación con animales debería estar prohibida.", "a": "y", "v": -1},
    {"t": "La pena de muerte es aceptable para crímenes atroces.", "a": "y", "v": 1},
    {"t": "El Estado debe proteger la lengua nacional sobre las demás.", "a": "y", "v": 1},
    {"t": "La meritocracia es un mito; el sistema es injusto.", "a": "y", "v": -1},
    {"t": "La policía debería tener más autoridad para disparar.", "a": "y", "v": 1},
    {"t": "La pornografía debería estar prohibida por ley.", "a": "y", "v": 1},
    {"t": "El multiculturalismo debilita la cohesión social.", "a": "y", "v": 1},
    {"t": "Un ciudadano tiene derecho a portar armas ocultas.", "a": "y", "v": -1},
    {"t": "La globalización cultural es una forma de colonialismo.", "a": "y", "v": 1},
    {"t": "El Estado debe financiar las artes con dinero público.", "a": "y", "v": -1},
    {"t": "La obediencia a los padres es la base de la sociedad.", "a": "y", "v": 1},
    {"t": "Los sindicatos deberían estar prohibidos en sectores públicos.", "a": "y", "v": 1},
    {"t": "La inmigración ilegal es una invasión organizada.", "a": "y", "v": 1},
    {"t": "El cambio climático es una exageración para controlarnos.", "a": "y", "v": 1},
    {"t": "La familia tradicional es el núcleo de la nación.", "a": "y", "v": 1},
    {"t": "Se debería prohibir el uso de símbolos religiosos en público.", "a": "y", "v": 1},
    {"t": "La corrección política limita nuestra libertad real.", "a": "y", "v": 1},
    {"t": "La autoridad del Estado emana de Dios o la Tradición.", "a": "y", "v": 1},
    {"t": "Las huelgas deberían estar prohibidas en servicios básicos.", "a": "y", "v": 1},
    {"t": "El progreso tecnológico nos está deshumanizando.", "a": "y", "v": 1},
    {"t": "La libertad individual es superior al bien común.", "a": "y", "v": -1},
    {"t": "El honor es más importante que la propia vida.", "a": "y", "v": 1},
    {"t": "La jerarquía es natural en la sociedad humana.", "a": "y", "v": 1},
    {"t": "Los presos deberían trabajar para pagar su estancia.", "a": "y", "v": 1},
    {"t": "La historia debe enseñarse para fomentar el patriotismo.", "a": "y", "v": 1}
]

# 4. LÓGICA DE IDEOLOGÍAS (25 CATEGORÍAS - 2 LÍNEAS CADA UNA)
def get_detailed_ideology(x, y):
    if y > 6:
        if x < -6: return "Marxismo-Leninismo", "Buscas la abolición de las clases sociales mediante un Estado todopoderoso y una economía planificada centralmente.\nDefiendes la dictadura del proletariado como herramienta para eliminar la explotación capitalista y las jerarquías privadas."
        if x < -2: return "Nacionalbolchevismo", "Combinas la economía colectivista de estilo soviético con un nacionalismo extremo y una moral social conservadora.\nCrees en un Estado fuerte que proteja la soberanía nacional frente a influencias externas y mantenga el control económico."
        if x < 2: return "Totalitarismo Central", "Consideras que el Estado debe tener el control absoluto de todas las esferas de la vida ciudadana, sin excepciones.\nLa lealtad al gobierno y el orden social son los valores supremos por encima de cualquier derecho individual o de mercado."
        if x < 6: return "Fascismo Clásico", "Defiendes un Estado corporativo autoritario que unifique a la nación por encima de las divisiones de clase y partidos.\nRechazas tanto el liberalismo como el marxismo, priorizando la voluntad nacional, la jerarquía y el heroísmo colectivo."
        return "Derecha Radical Autoritaria", "Apoyas un sistema de mercado libre para las élites nacionales, protegido por un régimen policial y militar implacable.\nBuscas preservar las jerarquías tradicionales y los valores nacionales mediante la fuerza estatal y la disciplina social."
    elif y > 2:
        if x < -6: return "Socialismo de Estado", "Crees que el gobierno debe ser el dueño y gestor de los medios de producción para garantizar la igualdad social.\nLa autoridad estatal es necesaria para redistribuir la riqueza y asegurar que las necesidades básicas de todos sean cubiertas."
        if x < -2: return "Populismo de Izquierda", "Movilizas al pueblo contra las élites económicas mediante un liderazgo carismático y políticas de protección estatal directa.\nPriorizas la justicia social inmediata y el control soberano de los recursos nacionales frente a los mercados globales."
        if x < 2: return "Estatismo", "Consideras que el Estado debe intervenir activamente para corregir los fallos del mercado y regular la moralidad pública.\nBuscas un equilibrio donde la autoridad gubernamental garantice la estabilidad nacional y el bienestar ciudadano dirigido."
        if x < 6: return "Conservadurismo", "Defiendes las instituciones tradicionales, el libre mercado moderado y el mantenimiento del orden social establecido.\nCrees en el cambio gradual y en la importancia de la religión, la familia y las leyes fuertes para preservar la civilización."
        return "Derecha Autoritaria", "Abogas por una economía de mercado muy abierta pero bajo un marco legal socialmente restrictivo y punitivo.\nEl Estado debe ser pequeño en lo económico pero extremadamente fuerte en la represión del crimen y el mantenimiento del orden."
    elif y > -2:
        if x < -6: return "Socialismo Democrático", "Buscas alcanzar la igualdad económica y social a través de métodos democráticos y la gestión pública de servicios clave.\nCrees que el capitalismo debe ser superado mediante reformas electorales que empoderen a la clase trabajadora de forma pacífica."
        if x < -2: return "Socialdemocracia", "Defiendes un sistema capitalista de mercado corregido por un fuerte Estado de bienestar y sindicatos potentes.\nEl objetivo es armonizar el crecimiento económico con una red de seguridad social que garantice salud, educación y pensiones."
        if x < 2: return "Centrismo", "Rechazas los dogmas de izquierda y derecha, prefiriendo soluciones pragmáticas basadas en la evidencia y el consenso.\nBuscas un equilibrio entre la libertad individual, la eficiencia del mercado y una protección social moderada y sostenible."
        if x < 6: return "Liberalismo Moderno", "Priorizas el progreso social y la libertad individual junto con una economía de mercado dinámica y regulada.\nCrees que el Estado debe proteger los derechos civiles de las minorías y garantizar una competencia justa en los negocios."
        return "Liberalismo Clásico", "Defiendes un Estado mínimo que se limite a proteger la vida, la libertad y la propiedad privada de los ciudadanos.\nEl mercado libre es el mecanismo más eficiente para organizar la sociedad y el individuo debe ser soberano en sus decisiones."
    elif y > -6:
        if x < -6: return "Anarcosindicalismo", "Propones una sociedad organizada a través de sindicatos autogestionados de trabajadores, sin necesidad de un Estado central.\nLa acción directa y la propiedad colectiva de las fábricas son las bases para eliminar tanto al gobierno como al capital."
        if x < -2: return "Socialismo Libertario", "Buscas una organización social basada en la cooperación voluntaria y la eliminación de las jerarquías coercitivas y el lucro.\nDefiendes que la libertad individual solo es posible en una comunidad donde los recursos se gestionen de forma común y libre."
        if x < 2: return "Libertarismo Progresista", "Combinas una defensa radical de las libertades personales con una visión crítica de las grandes concentraciones de poder corporativo.\nApoyas la legalización total de conductas privadas y un mercado libre de privilegios estatales para fomentar la autonomía individual."
        if x < 6: return "Minarquismo", "Crees que el único papel legítimo del gobierno es la protección contra la agresión, el robo, el fraude y el cumplimiento de contratos.\nEl Estado solo debe gestionar la policía, los tribunales y la defensa nacional, dejando todo lo demás a la iniciativa privada."
        return "Paleolibertarismo", "Unes el rechazo total al Estado económico con una defensa de los valores culturales tradicionales y las instituciones privadas.\nCrees que el mercado libre y la moralidad tradicional son los mejores pilares para una sociedad estable y próspera sin gobierno."
    else:
        if x < -6: return "Anarcocomunismo", "Sueñas con una sociedad sin Estado, sin clases y sin dinero, basada en el principio de 'a cada cual según su necesidad'.\nLa federación voluntaria de comunas libres es el modelo para alcanzar la verdadera igualdad y libertad humana total."
        if x < -2: return "Mutualismo", "Propones un mercado de cooperativas y artesanos basado en el intercambio justo y la ausencia de intereses o rentas capitalistas.\nLa banca mutua y la posesión basada en el uso reemplazan al Estado y a la propiedad privada acumulativa tradicional."
        if x < 2: return "Anarquismo Individualista", "Sostienes la soberanía absoluta del individuo sobre su propia vida y los frutos de su trabajo frente a cualquier colectividad.\nRechazas toda autoridad externa, sea estatal o social, defendiendo la asociación voluntaria basada únicamente en el interés mutuo."
        if x < 6: return "Voluntarismo", "Afirmas que todas las interacciones humanas deben ser totalmente voluntarias y que el Estado es una agresión intrínsecamente ilegítima.\nCrees que cualquier servicio, incluyendo la ley y la seguridad, debe ser provisto mediante acuerdos libres y contratos privados."
        return "Anarcocapitalismo", "Abogas por la eliminación total del Estado en favor de un sistema de propiedad privada absoluta y mercados libres competitivos.\nTodos los servicios públicos deben ser privatizados y la justicia debe ser administrada por agencias de protección en competencia."

# 5. LÓGICA DE NAVEGACIÓN
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0})

def responder(p):
    q = questions[st.session_state.idx]
    # Normalización para 85 preguntas
    num_x = len([qu for qu in questions if qu['a'] == 'x'])
    num_y = len([qu for qu in questions if qu['a'] == 'y'])
    
    if q['a'] == 'x': st.session_state.x += (p * q['v']) / (num_x / 5)
    else: st.session_state.y += (p * q['v']) / (num_y / 5)
    st.session_state.idx += 1

# --- UI: RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown('<h1 class="main-title">Análisis Final</h1>', unsafe_allow_html=True)
    ux, uy = max(min(st.session_state.x, 10), -10), max(min(st.session_state.y, 10), -10)
    name, desc = get_detailed_ideology(ux, uy)
    
    st.markdown(f'<div class="result-bubble"><p class="ideology-title">{name}</p><p class="ideology-desc">{desc}</p></div>', unsafe_allow_html=True)
    
    # SVG GRÁFICO GRANDE (600x600)
    px, py = 300 + (ux * 27), 300 - (uy * 27)
    leaders_svg = "".join([f'<circle cx="{300+(l["x"]*27)}" cy="{300-(l["y"]*27)}" r="5" fill="{l["c"]}" stroke="black"/><text x="{300+(l["x"]*27)}" y="{300-(l["y"]*27)+15}" font-size="11" text-anchor="middle" font-family="Arial" font-weight="bold">{l["n"]}</text>' for l in LEADERS])
    
    svg_code = f"""
    <div class="chart-container" style="text-align:center; background:white; padding:10px; border-radius:15px; display:flex; justify-content:center;">
        <svg width="600" height="600" viewBox="0 0 600 600" style="border:4px solid #333; font-family:Arial; width:100%; max-width:600px;">
            <rect width="300" height="300" fill="#FFB2B2" opacity="0.6"/>
            <rect x="300" width="300" height="300" fill="#B2B2FF" opacity="0.6"/>
            <rect y="300" width="300" height="300" fill="#B2FFB2" opacity="0.6"/>
            <rect x="300" y="300" width="300" height="300" fill="#FFFFB2" opacity="0.6"/>
            <line x1="300" y1="0" x2="300" y2="600" stroke="black" stroke-width="3"/>
            <line x1="0" y1="300" x2="600" y2="300" stroke="black" stroke-width="3"/>
            <text x="510" y="320" font-weight="bold" font-size="16">DERECHA</text>
            <text x="10" y="320" font-weight="bold" font-size="16">IZQUIERDA</text>
            <text x="310" y="25" font-weight="bold" font-size="16">AUTORITARIO</text>
            <text x="310" y="590" font-weight="bold" font-size="16">LIBERTARIO</text>
            {leaders_svg}
            <circle cx="{px}" cy="{py}" r="12" fill="red" stroke="white" stroke-width="4"/>
            <text x="{px}" y="{py-18}" fill="red" font-weight="900" font-size="20" text-anchor="middle">TÚ</text>
        </svg>
    </div>
    """
    components.html(svg_code, height=620)

    if st.button("🖨️ GUARDAR RESULTADOS (PDF / IMPRIMIR)"):
        components.html("<script>window.print();</script>", height=0)
    if st.button("🔄 VOLVER A EMPEZAR"):
        st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0})
        st.rerun()

# --- UI: PREGUNTAS ---
else:
    st.markdown('<h1 class="main-title">Compás Político</h1>', unsafe_allow_html=True)
    
    if st.session_state.idx == 0:
        st.markdown('<p class="welcome-text">Analiza tu posición ideológica con este test de 85 preguntas diseñado para alta precisión.</p>', unsafe_allow_html=True)
        st.markdown('<div class="warning-box">⚠️ Sé honesto contigo mismo. Si no entiendes un concepto económico o social, utiliza el botón "Neutral".</div>', unsafe_allow_html=True)
    
    st.markdown(f'<span class="q-counter">Pregunta {st.session_state.idx + 1} de {len(questions)}</span>', unsafe_allow_html=True)
    st.progress(st.session_state.idx / len(questions))
    
    st.markdown(f'<div class="question-container"><p class="question-text">{questions[st.session_state.idx]["t"]}</p></div>', unsafe_allow_html=True)
    
    st.button("✅ Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("👍 De acuerdo", on_click=responder, args=(1,))
    st.button("😐 Neutral / No lo sé", on_click=responder, args=(0,))
    st.button("👎 En desacuerdo", on_click=responder, args=(-1,))
    st.button("❌ Totalmente en desacuerdo", on_click=responder, args=(-2,))
