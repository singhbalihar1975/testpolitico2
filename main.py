import streamlit as st
import streamlit.components.v1 as components
import math

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Compás Político Profesional", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #E0F2FE; } 
    .main .block-container { max-width: 850px; padding-top: 2rem; text-align: center; }
    .main-title { font-size: 60px; font-weight: 950; color: #1E3A8A; margin-bottom: 20px; text-align: center; }
    
    .welcome-box { 
        background-color: #DBEAFE; border: 2px solid #3B82F6; 
        border-radius: 15px; padding: 25px; margin-bottom: 30px; 
        color: #1E40AF; text-align: center; font-size: 18px; font-weight: 500;
    }

    .q-counter { font-size: 18px; color: #1E40AF; font-weight: 700; margin-bottom: 10px; display: block; }
    .question-container { margin: 40px auto; min-height: 140px; display: flex; align-items: center; justify-content: center; }
    .question-text { font-size: 32px !important; font-weight: 800; color: #1E3A8A; line-height: 1.2; text-align: center; }

    div.stButton > button { 
        width: 100% !important; height: 58px !important; border-radius: 14px !important; 
        font-size: 19px !important; font-weight: 700; margin-bottom: 10px !important; 
        border: 2px solid #3B82F6 !important; background-color: #DBEAFE !important; 
        color: #1E40AF !important; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #BFDBFE !important; border-color: #1E3A8A !important; }

    .back-btn button { 
        background-color: #93C5FD !important; color: white !important; 
        border: 2px solid #60A5FA !important; height: 45px !important; margin-top: 15px !important; 
    }

    .result-bubble { 
        background-color: #DBEAFE; border-radius: 30px; padding: 40px; 
        border: 6px solid #3B82F6; margin: 30px auto; text-align: center; 
    }
    .ideology-title { font-size: 42px !important; font-weight: 950; color: #1D4ED8; text-transform: uppercase; display: block; margin-bottom: 10px; }
    .ideology-desc { font-size: 19px; color: #1E40AF; line-height: 1.4; font-weight: 500; display: block; }
    .match-tag { 
        font-size: 22px; font-weight: 800; color: #1E40AF; margin-top: 25px; 
        background: #BFDBFE; padding: 12px 25px; border-radius: 20px; display: inline-block; border: 2px solid #60A5FA;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS DE LÍDERES (45)
LEADERS = [
    {"n": "Stalin", "x": -9, "y": 9, "c": "#C53030"}, {"n": "Hitler", "x": 8, "y": 9.5, "c": "#2D3748"},
    {"n": "Mao", "x": -9.5, "y": 8.5, "c": "#E53E3E"}, {"n": "Gandhi", "x": -6.5, "y": -7.5, "c": "#48BB78"},
    {"n": "Thatcher", "x": 7.5, "y": 6.5, "c": "#3182CE"}, {"n": "Milei", "x": 9.2, "y": -8.8, "c": "#D69E2E"},
    {"n": "Castro", "x": -8.5, "y": 7, "c": "#2F855A"}, {"n": "Friedman", "x": 8.5, "y": -6, "c": "#ECC94B"},
    {"n": "Sanders", "x": -5.5, "y": -2, "c": "#4299E1"}, {"n": "Pinochet", "x": 8.8, "y": 8, "c": "#1A202C"},
    {"n": "Chomsky", "x": -8.5, "y": -8.5, "c": "#38A169"}, {"n": "Rothbard", "x": 10, "y": -10, "c": "#F6E05E"},
    {"n": "Obama", "x": 2.5, "y": 1.5, "c": "#2B6CB0"}, {"n": "Mandela", "x": -3, "y": -3, "c": "#48BB78"},
    {"n": "Churchill", "x": 6, "y": 5, "c": "#2C5282"}, {"n": "Trump", "x": 6.5, "y": 5.5, "c": "#E53E3E"},
    {"n": "Putin", "x": 7, "y": 8.5, "c": "#2B6CB0"}, {"n": "Sánchez", "x": -2.5, "y": 1, "c": "#F56565"},
    {"n": "Bukele", "x": 5, "y": 7, "c": "#2D3748"}, {"n": "Lula", "x": -4.5, "y": 1.5, "c": "#E53E3E"},
    {"n": "Kim Jong-un", "x": -9.5, "y": 10, "c": "#E53E3E"}, {"n": "Macron", "x": 4, "y": 3, "c": "#3182CE"},
    {"n": "Mujica", "x": -7, "y": -4, "c": "#48BB78"}, {"n": "Hayek", "x": 9, "y": -7, "c": "#F6E05E"},
    {"n": "Kropotkin", "x": -10, "y": -10, "c": "#000000"}, {"n": "Mussolini", "x": 7.5, "y": 9.5, "c": "#1A202C"},
    {"n": "Keynes", "x": -3, "y": 2, "c": "#63B3ED"}, {"n": "Lenin", "x": -8.5, "y": 8, "c": "#C53030"},
    {"n": "Abascal", "x": 7.5, "y": 7.5, "c": "#38A169"}, {"n": "Díaz", "x": -6, "y": -2, "c": "#ED64A6"},
    {"n": "Merkel", "x": 2.5, "y": 3, "c": "#4A5568"}, {"n": "Biden", "x": 3, "y": 2, "c": "#3182CE"},
    {"n": "Rand", "x": 9.5, "y": -8, "c": "#718096"}, {"n": "Bolsonaro", "x": 8, "y": 6.5, "c": "#48BB78"},
    {"n": "Trudeau", "x": -1.5, "y": -1.5, "c": "#ED64A6"}, {"n": "Meloni", "x": 7, "y": 6, "c": "#2C5282"},
    {"n": "Locke", "x": 6, "y": -5, "c": "#3182CE"}, {"n": "Jefferson", "x": 4, "y": -7.5, "c": "#D69E2E"},
    {"n": "Che Guevara", "x": -9, "y": 6, "c": "#2F855A"}, {"n": "Franco", "x": 7, "y": 9, "c": "#2D3748"},
    {"n": "Robespierre", "x": -4, "y": 9, "c": "#C53030"}, {"n": "Malatesta", "x": -9, "y": -9.5, "c": "#4A5568"},
    {"n": "Voltaire", "x": 5, "y": -3, "c": "#ECC94B"}, {"n": "Gaddafi", "x": -2, "y": 8, "c": "#38A169"},
    {"n": "Rousseau", "x": -5, "y": 4, "c": "#4299E1"}
]

# 3. LAS 85 PREGUNTAS
questions = [
    # ECONÓMICAS
    {"t": "El salario mínimo debería ser eliminado para fomentar la contratación.", "a": "x", "v": 1},
    {"t": "La sanidad debe ser 100% pública, gratuita y universal.", "a": "x", "v": -1},
    {"t": "El Estado debe gestionar sectores estratégicos como la energía.", "a": "x", "v": -1},
    {"t": "Privatizar empresas públicas mejora siempre la eficiencia.", "a": "x", "v": 1},
    {"t": "Los impuestos a las grandes fortunas deben subir drásticamente.", "a": "x", "v": -1},
    {"t": "El mercado libre sin regulaciones es el mejor motor de progreso.", "a": "x", "v": 1},
    {"t": "El Estado no debe rescatar bancos o empresas privadas.", "a": "x", "v": 1},
    {"t": "Es necesario proteger la industria nacional con aranceles.", "a": "x", "v": -1},
    {"t": "La propiedad privada es un derecho humano intocable.", "a": "x", "v": 1},
    {"t": "El gobierno debería garantizar una Renta Básica Universal.", "a": "x", "v": -1},
    {"t": "Las herencias deberían tener un impuesto muy elevado.", "a": "x", "v": -1},
    {"t": "Es injusto que los que más ganan paguen más porcentaje.", "a": "x", "v": 1},
    {"t": "El capitalismo explota intrínsecamente al trabajador.", "a": "x", "v": -1},
    {"t": "Los sindicatos son esenciales para el equilibrio económico.", "a": "x", "v": -1},
    {"t": "La competencia es superior a cualquier planificación estatal.", "a": "x", "v": 1},
    {"t": "Controlar los precios de alquiler ayuda a los ciudadanos.", "a": "x", "v": -1},
    {"t": "El Banco Central debería desaparecer.", "a": "x", "v": 1},
    {"t": "La desigualdad económica motiva el esfuerzo personal.", "a": "x", "v": 1},
    {"t": "El Estado debe financiar ciencia aunque no sea rentable.", "a": "x", "v": -1},
    {"t": "Las multinacionales tienen demasiado poder político.", "a": "x", "v": -1},
    {"t": "El gasto público es la raíz de los problemas económicos.", "a": "x", "v": 1},
    {"t": "Las pensiones deberían ser ahorros privados individuales.", "a": "x", "v": 1},
    {"t": "El planeta es más importante que el PIB.", "a": "x", "v": -1},
    {"t": "Las criptomonedas no deben ser reguladas.", "a": "x", "v": 1},
    {"t": "El Estado debe crear empleo en épocas de crisis.", "a": "x", "v": -1},
    {"t": "La especulación financiera es perjudicial.", "a": "x", "v": -1},
    {"t": "Correos y transporte deben ser solo públicos.", "a": "x", "v": -1},
    {"t": "Bajar impuestos a ricos beneficia a todos al final.", "a": "x", "v": 1},
    {"t": "La deuda externa de países pobres debe condonarse.", "a": "x", "v": -1},
    {"t": "El mercado no garantiza las necesidades básicas.", "a": "x", "v": -1},
    {"t": "Las patentes farmacéuticas no deben existir en crisis.", "a": "x", "v": -1},
    {"t": "La bolsa es una herramienta útil de desarrollo.", "a": "x", "v": 1},
    {"t": "El dinero físico debe ser reemplazado por digital estatal.", "a": "x", "v": -1},
    {"t": "La caridad privada es mejor que la ayuda pública.", "a": "x", "v": 1},
    {"t": "Los paraísos fiscales son un robo a la sociedad.", "a": "x", "v": -1},
    {"t": "El Estado no debería endeudarse con bancos privados.", "a": "x", "v": 1},
    {"t": "Reducir la jornada laboral por ley es necesario.", "a": "x", "v": -1},
    {"t": "Expropiar tierras sin uso es legítimo.", "a": "x", "v": -1},
    {"t": "El éxito depende más de la suerte que del trabajo.", "a": "x", "v": -1},
    {"t": "Gravar los robots es necesario ante la IA.", "a": "x", "v": -1},
    {"t": "El mercado de armas debería ser libre.", "a": "x", "v": 1},
    {"t": "El Estado debe fijar los tipos de interés.", "a": "x", "v": -1},
    {"t": "El libre comercio perjudica a los trabajadores locales.", "a": "x", "v": -1},
    # SOCIALES
    {"t": "El aborto debe ser un derecho legal y gratuito.", "a": "y", "v": -1},
    {"t": "Se necesita un líder fuerte para imponer orden.", "a": "y", "v": 1},
    {"t": "La religión no debe influir en la legislación.", "a": "y", "v": -1},
    {"t": "Todas las drogas deberían ser legales para consumo.", "a": "y", "v": -1},
    {"t": "La cadena perpetua es un castigo justo.", "a": "y", "v": 1},
    {"t": "La nación es más importante que el individuo.", "a": "y", "v": 1},
    {"t": "El matrimonio solo es entre hombre y mujer.", "a": "y", "v": 1},
    {"t": "Cámaras de vigilancia en cada esquina son seguridad.", "a": "y", "v": 1},
    {"t": "La libertad de expresión incluye el derecho a ofender.", "a": "y", "v": -1},
    {"t": "La eutanasia es un derecho básico.", "a": "y", "v": -1},
    {"t": "El servicio militar debe ser obligatorio.", "a": "y", "v": 1},
    {"t": "Las fronteras abiertas son el futuro.", "a": "y", "v": -1},
    {"t": "La bandera es sagrada y merece respeto por ley.", "a": "y", "v": 1},
    {"t": "La educación sexual escolar corrompe a los niños.", "a": "y", "v": 1},
    {"t": "La prostitución debe ser ilegal.", "a": "y", "v": 1},
    {"t": "Quemar la bandera debería ser delito.", "a": "y", "v": 1},
    {"t": "El feminismo actual es excesivo.", "a": "y", "v": 1},
    {"t": "Prohibir experimentos con animales es urgente.", "a": "y", "v": -1},
    {"t": "La pena de muerte es aceptable.", "a": "y", "v": 1},
    {"t": "Proteger la lengua nacional es deber del Estado.", "a": "y", "v": 1},
    {"t": "La meritocracia es un engaño social.", "a": "y", "v": -1},
    {"t": "La policía debe tener más libertad de acción.", "a": "y", "v": 1},
    {"t": "La pornografía daña a la sociedad.", "a": "y", "v": 1},
    {"t": "El multiculturalismo debilita al país.", "a": "y", "v": 1},
    {"t": "Portar armas es un derecho de autodefensa.", "a": "y", "v": -1},
    {"t": "La globalización cultural es colonialismo.", "a": "y", "v": 1},
    {"t": "El Estado debe financiar museos y arte.", "a": "y", "v": -1},
    {"t": "Obedecer a los padres es la base social.", "a": "y", "v": 1},
    {"t": "La inmigración ilegal es una amenaza.", "a": "y", "v": 1},
    {"t": "El cambio climático es una herramienta de control.", "a": "y", "v": 1},
    {"t": "La familia tradicional es el núcleo nacional.", "a": "y", "v": 1},
    {"t": "La corrección política mata la libertad.", "a": "y", "v": 1},
    {"t": "La autoridad viene de la Tradición o Dios.", "a": "y", "v": 1},
    {"t": "La tecnología nos quita la humanidad.", "a": "y", "v": 1},
    {"t": "Los presos deben trabajar forzosamente.", "a": "y", "v": 1},
    {"t": "La historia debe enseñarse para crear patriotas.", "a": "y", "v": 1},
    {"t": "Se debe prohibir el velo islámico en público.", "a": "y", "v": 1},
    {"t": "La libertad individual es superior al bien común.", "a": "y", "v": -1},
    {"t": "El Estado debe censurar noticias falsas.", "a": "y", "v": 1},
    {"t": "La monarquía es una institución útil.", "a": "y", "v": 1},
    {"t": "Las huelgas deben ser limitadas en sectores clave.", "a": "y", "v": 1},
    {"t": "El castigo físico moderado a niños es educativo.", "a": "y", "v": 1}
]

# 4. LÓGICA DE LAS 25 IDEOLOGÍAS
def get_full_ideology(x, y):
    if y > 6:
        if x < -6: return "Marxismo-Leninismo", "Defiende la abolición de la propiedad privada mediante el control total del Estado.\nBusca la dictadura del proletariado para eliminar las clases sociales por la fuerza."
        if x < -2: return "Nacionalbolchevismo", "Combina una economía de planificación centralizada de estilo soviético con valores ultranacionalistas.\nRechaza el globalismo y defiende una identidad nacional rígida bajo mando estatal."
        if x < 2: return "Totalitarismo Central", "Establece el predominio absoluto del Estado sobre todos los aspectos de la vida pública y privada.\nSuprime toda disidencia y centraliza el poder en una figura o partido único e infalible."
        if x < 6: return "Fascismo Clásico", "Promueve la unidad nacional a través de un Estado corporativista y autoritario de carácter militar.\nSubordina los intereses individuales al destino de la nación bajo una jerarquía estricta."
        return "Derecha Radical Autoritaria", "Fusiona un capitalismo de mercado para las élites con un control policial y social implacable.\nDefiende la jerarquía natural y el castigo severo a cualquier desviación de la norma establecida."
    elif y > 2:
        if x < -6: return "Socialismo de Estado", "Aboga por la propiedad pública de los medios de producción dentro de un marco autoritario suave.\nGarantiza la igualdad mediante la burocracia estatal y la planificación económica dirigida."
        if x < -2: return "Socialdemocracia", "Busca humanizar el capitalismo mediante un fuerte Estado del bienestar y redistribución de riqueza.\nDefiende servicios públicos universales financiados con impuestos progresivos y justicia social."
        if x < 2: return "Centrismo Pragmático", "Evita los extremismos ideológicos buscando soluciones técnicas basadas en la eficiencia y el equilibrio.\nCombina la libertad de mercado con protecciones sociales moderadas según la necesidad del momento."
        if x < 6: return "Conservadurismo", "Prioriza el mantenimiento del orden social, la tradición religiosa y la estabilidad de las instituciones.\nDefiende la propiedad privada y la moral tradicional como pilares de una sociedad funcional."
        return "Derecha Autoritaria", "Sostiene que la libertad económica requiere un marco social rígido y una autoridad fuerte.\nPromueve el patriotismo y el respeto a la ley como métodos para preservar la civilización."
    elif y > -2:
        if x < -6: return "Socialismo Democrático", "Propone la transición hacia una economía socializada mediante mecanismos democráticos y pluralismo.\nBusca empoderar a los trabajadores y eliminar la explotación sin suprimir las libertades civiles."
        if x < -2: return "Populismo de Izquierda", "Moviliza a las clases populares contra las élites económicas y globales mediante el liderazgo fuerte.\nDefiende la soberanía nacional y la protección del mercado interno para el beneficio del pueblo."
        if x < 2: return "Liberalismo Progresista", "Defiende las libertades civiles individuales y los derechos de las minorías dentro de un mercado regulado.\nCree en el progreso social y la intervención estatal limitada para corregir desigualdades de origen."
        if x < 6: return "Liberalismo Clásico", "Sostiene que el papel del Estado debe limitarse estrictamente a proteger la vida y la propiedad.\nConsidera que el libre intercambio es la fuente principal de prosperidad y libertad humana."
        return "Minarquismo", "Propugna que el Estado solo debe encargarse de la seguridad, la justicia y la defensa nacional.\nCualquier otra función estatal es vista como una interferencia ilegítima en la libertad individual."
    elif y > -6:
        if x < -6: return "Anarcosindicalismo", "Propone la gestión de la sociedad a través de sindicatos autogestionados y la acción directa obrera.\nRechaza tanto el Estado como el sistema salarial en favor de la federación de trabajadores."
        if x < -2: return "Socialismo Libertario", "Defiende la propiedad colectiva y la cooperación voluntaria sin necesidad de un gobierno central.\nBusca la máxima autonomía individual en una sociedad organizada horizontalmente y sin jerarquías."
        if x < 2: return "Libertarismo Progresista", "Combina una libertad personal radical en temas sociales con un mercado libre de privilegios corporativos.\nRechaza las leyes de moralidad estatal y aboga por la soberanía del individuo sobre su cuerpo."
        if x < 6: return "Objetivismo", "Filosofía basada en el egoísmo racional, el capitalismo de laissez-faire y la realidad objetiva.\nConsidera que el individuo debe vivir para sí mismo, sin sacrificarse por otros ni pedir sacrificios."
        return "Paleolibertarismo", "Une la oposición radical al Estado con valores culturales tradicionales y conservadores en lo social.\nCree que la libertad económica es más estable dentro de comunidades con moralidad clásica."
    else:
        if x < -6: return "Anarcocomunismo", "Sociedad organizada en comunas libres donde se produce según la capacidad y se consume según necesidad.\nAbolición total del dinero, el Estado y la propiedad privada en favor de la ayuda mutua absoluta."
        if x < -2: return "Mutualismo", "Sistema económico basado en el intercambio recíproco y cooperativas que operan sin beneficio de lucro.\nPropone que cada trabajador reciba el producto íntegro de su labor mediante contratos voluntarios."
        if x < 2: return "Anarquismo Individualista", "Sostiene que la voluntad del individuo es la única ley y no debe estar sujeta a grupos o Estados.\nDefiende la autonomía personal absoluta y la asociación libre basada en el beneficio mutuo."
        if x < 6: return "Voluntarismo", "Toda forma de asociación humana debe ser estrictamente voluntaria y carecer de cualquier coacción.\nRechaza la existencia del Estado por considerarlo una institución basada necesariamente en la violencia."
        return "Anarcocapitalismo", "Defiende la privatización total de todos los servicios, incluyendo la ley, la policía y los tribunales.\nConsidera la propiedad privada como el derecho absoluto y el Estado como una organización criminal.Eres autista."

# 5. MOTOR DE LÓGICA
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'hx': [], 'hy': []})

def responder(p):
    q = questions[st.session_state.idx]
    if q['a'] == 'x': 
        st.session_state.hx.append(p * q['v'])
        st.session_state.hy.append(0)
    else: 
        st.session_state.hy.append(p * q['v'])
        st.session_state.hx.append(0)
    st.session_state.idx += 1

def volver():
    if st.session_state.idx > 0:
        st.session_state.idx -= 1
        st.session_state.hx.pop()
        st.session_state.hy.pop()

# --- RESULTADOS FINALES ---
if st.session_state.idx >= len(questions):
    st.markdown('<h1 class="main-title">Tu Compás Político</h1>', unsafe_allow_html=True)
    total_x = len([q for q in questions if q['a'] == 'x'])
    total_y = len([q for q in questions if q['a'] == 'y'])
    
    # Normalización a escala -10 a 10
    ux = max(min((sum(st.session_state.hx) / (total_x * 2)) * 10, 10), -10)
    uy = max(min((sum(st.session_state.hy) / (total_y * 2)) * 10, 10), -10)
    
    name, desc = get_full_ideology(ux, uy)
    match = min(LEADERS, key=lambda l: math.sqrt((ux-l['x'])**2 + (uy-l['y'])**2))['n']
    
    st.markdown(f'<div class="result-bubble"><span class="ideology-title">{name}</span><span class="ideology-desc">{desc}</span><span class="match-tag">Más cercano a: {match}</span></div>', unsafe_allow_html=True)
    
    # Dibujo del Gráfico con Brillo en el círculo "TÚ"
    px, py = 250 + (ux * 23), 250 - (uy * 23)
    leaders_svg = "".join([f'<circle cx="{250+(l["x"]*23)}" cy="{250-(l["y"]*23)}" r="5" fill="{l["c"]}" stroke="black"/><text x="{250+(l["x"]*23)}" y="{250-(l["y"]*23)+14}" font-size="10" text-anchor="middle" font-weight="bold" font-family="sans-serif">{l["n"]}</text>' for l in LEADERS])
    
    svg = f"""<div style="display:flex; justify-content:center;">
    <svg width="500" height="500" viewBox="0 0 500 500" style="border:3px solid #333; background:white; font-family: sans-serif;">
        <defs>
            <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="4.5" result="coloredBlur"/>
                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
        </defs>
        
        <rect width="250" height="250" fill="#FFB2B2" opacity="0.5"/><rect x="250" width="250" height="250" fill="#B2B2FF" opacity="0.5"/><rect y="250" width="250" height="250" fill="#B2FFB2" opacity="0.5"/><rect x="250" y="250" width="250" height="250" fill="#FFFFB2" opacity="0.5"/>
        <line x1="250" y1="0" x2="250" y2="500" stroke="black" stroke-width="1"/><line x1="0" y1="250" x2="500" y2="250" stroke="black" stroke-width="1"/>
        
        {leaders_svg}
        
        <circle cx="{px}" cy="{py}" r="11" fill="red" stroke="white" stroke-width="3" filter="url(#glow)"/>
        <text x="{px}" y="{py-20}" fill="red" font-weight="950" font-size="24" text-anchor="middle">TÚ</text>
    </svg></div>"""
    
    components.html(svg, height=520)
    if st.button("REINICIAR TEST"): 
        st.session_state.update({'idx': 0, 'hx': [], 'hy': []})
        st.rerun()

# --- INTERFAZ DE PREGUNTAS ---
else:
    st.markdown('<h1 class="main-title">Compás Político</h1>', unsafe_allow_html=True)
    if st.session_state.idx == 0: 
        st.markdown('<div class="welcome-box">Test de 85 variables. Responde honestamente, si no sabes lo que significa la pregunta, responde neutral.</div>', unsafe_allow_html=True)
    
    st.markdown(f'<span class="q-counter">Pregunta {st.session_state.idx + 1} de {len(questions)}</span>', unsafe_allow_html=True)
    st.progress(st.session_state.idx / len(questions))
    
    st.markdown(f'<div class="question-container"><p class="question-text">{questions[st.session_state.idx]["t"]}</p></div>', unsafe_allow_html=True)
    
    st.button("✅ Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("👍 De acuerdo", on_click=responder, args=(1,))
    st.button("😐 Neutral / No lo sé", on_click=responder, args=(0,))
    st.button("👎 En desacuerdo", on_click=responder, args=(-1,))
    st.button("❌ Totalmente en desacuerdo", on_click=responder, args=(-2,))
    
    if st.session_state.idx > 0: 
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        st.button("⬅️ Pregunta Anterior", on_click=volver)
        st.markdown('</div>', unsafe_allow_html=True)
