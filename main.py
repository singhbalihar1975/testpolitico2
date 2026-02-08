import streamlit as st
import streamlit.components.v1 as components
import math

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Compás Político", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .main .block-container { max-width: 850px; padding-top: 2rem; text-align: center; }
    .main-title { font-size: 60px; font-weight: 950; color: #1E3A8A; margin-bottom: 20px; text-align: center; width: 100%; }
    .welcome-box { background-color: #EFF6FF; border: 2px solid #3B82F6; border-radius: 15px; padding: 25px; margin-bottom: 30px; color: #1E40AF; text-align: center; font-size: 18px; }
    .q-counter { font-size: 18px; color: #64748B; font-weight: 700; margin-bottom: 10px; display: block; text-align: center; }
    .question-container { margin: 40px auto; min-height: 140px; display: flex; align-items: center; justify-content: center; max-width: 750px; }
    .question-text { font-size: 32px !important; font-weight: 800; color: #0F172A; line-height: 1.2; text-align: center; }

    /* Botones de Colores Semáforo */
    div.stButton > button { width: 100% !important; height: 58px !important; border-radius: 14px !important; font-size: 19px !important; font-weight: 700; margin-bottom: 10px !important; border: none !important; }
    .stButton:nth-of-type(1) button { background-color: #10B981 !important; color: white !important; } /* Totalmente acuerdo */
    .stButton:nth-of-type(2) button { background-color: #A7F3D0 !important; color: #064E3B !important; } /* Acuerdo */
    .stButton:nth-of-type(3) button { background-color: #F1F5F9 !important; color: #475569 !important; } /* Neutral */
    .stButton:nth-of-type(4) button { background-color: #FECACA !important; color: #991B1B !important; } /* Desacuerdo */
    .stButton:nth-of-type(5) button { background-color: #EF4444 !important; color: white !important; } /* Totalmente desacuerdo */
    
    .back-btn button { background-color: white !important; color: #64748B !important; border: 2px solid #E2E8F0 !important; height: 45px !important; margin-top: 25px !important; }

    .result-bubble { background-color: white; border-radius: 30px; padding: 40px; border: 6px solid #3B82F6; margin: 30px auto; text-align: center; }
    .ideology-title { font-size: 45px !important; font-weight: 950; color: #1D4ED8; text-transform: uppercase; display: block; text-align: center; }
    .ideology-desc { font-size: 20px; color: #334155; line-height: 1.5; margin-top: 15px; text-align: center; }
    .match-tag { font-size: 24px; font-weight: 800; color: #1E40AF; margin-top: 25px; background: #DBEAFE; padding: 15px 30px; border-radius: 20px; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# 2. LÍDERES POLÍTICOS (45 FIGURAS)
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

# 3. LAS 85 PREGUNTAS (Económicas x, Sociales y)
questions = [
    # ECONÓMICAS
    {"t": "El salario mínimo debería ser eliminado para fomentar la contratación.", "a": "x", "v": 1},
    {"t": "La sanidad debe ser 100% pública, gratuita y universal.", "a": "x", "v": -1},
    {"t": "El Estado debe gestionar sectores como la energía y el agua.", "a": "x", "v": -1},
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
    {"t": "La bolsa es una herramienta útil de inversión social.", "a": "x", "v": 1},
    {"t": "El dinero físico debe ser reemplazado por digital estatal.", "a": "x", "v": -1},
    {"t": "La caridad privada es mejor que la ayuda pública.", "a": "x", "v": 1},
    {"t": "Los paraísos fiscales son un robo a la sociedad.", "a": "x", "v": -1},
    {"t": "El Estado no debería endeudarse con bancos privados.", "a": "x", "v": 1},
    {"t": "Reducir la jornada laboral por ley es necesario.", "a": "x", "v": -1},
    {"t": "Expropiar tierras sin uso es legítimo.", "a": "x", "v": -1},
    {"t": "El éxito económico depende más de la suerte que del trabajo.", "a": "x", "v": -1},
    {"t": "Gravar los robots es necesario ante la automatización.", "a": "x", "v": -1},
    {"t": "El mercado de armas debería ser libre.", "a": "x", "v": 1},
    {"t": "La publicidad comercial no debe ser regulada.", "a": "x", "v": 1},
    {"t": "El Estado debe fijar los tipos de interés.", "a": "x", "v": -1},

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
    {"t": "Las fronteras abiertas son el futuro de la humanidad.", "a": "y", "v": -1},
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
    {"t": "La pornografía daña a la sociedad y debe prohibirse.", "a": "y", "v": 1},
    {"t": "El multiculturalismo debilita al país.", "a": "y", "v": 1},
    {"t": "Portar armas es un derecho de autodefensa.", "a": "y", "v": -1},
    {"t": "La globalización cultural es colonialismo.", "a": "y", "v": 1},
    {"t": "El Estado debe financiar museos y arte.", "a": "y", "v": -1},
    {"t": "Obedecer a los padres es la base social.", "a": "y", "v": 1},
    {"t": "Los sindicatos públicos deben prohibirse.", "a": "y", "v": 1},
    {"t": "La inmigración ilegal es una amenaza.", "a": "y", "v": 1},
    {"t": "El cambio climático es una herramienta de control.", "a": "y", "v": 1},
    {"t": "La familia tradicional es el núcleo nacional.", "a": "y", "v": 1},
    {"t": "Prohibir velos o cruces en público es correcto.", "a": "y", "v": 1},
    {"t": "La corrección política mata la libertad.", "a": "y", "v": 1},
    {"t": "La autoridad viene de la Tradición o Dios.", "a": "y", "v": 1},
    {"t": "Prohibir huelgas en servicios básicos es justo.", "a": "y", "v": 1},
    {"t": "La tecnología nos quita la humanidad.", "a": "y", "v": 1},
    {"t": "La libertad individual es superior al bien común.", "a": "y", "v": -1},
    {"t": "El honor es más importante que la vida.", "a": "y", "v": 1},
    {"t": "La jerarquía es natural en los humanos.", "a": "y", "v": 1},
    {"t": "Los presos deben trabajar forzosamente.", "a": "y", "v": 1},
    {"t": "La historia debe enseñarse para crear patriotas.", "a": "y", "v": 1}
]

# 4. LÓGICA DE IDEOLOGÍAS (25 CATEGORÍAS)
def get_full_ideology(x, y):
    if y > 6:
        if x < -6: return "Marxismo-Leninismo", "Buscas la abolición de clases mediante un Estado con control total de la economía.\nDefiendes la planificación central como método para eliminar la explotación capitalista."
        if x < -2: return "Nacionalbolchevismo", "Estado soviético en lo económico pero con un nacionalismo extremo y socialmente conservador.\nCrees en un Estado fuerte que proteja la soberanía nacional frente a influencias externas."
        if x < 2: return "Totalitarismo Central", "Consideras que el Estado debe regir de forma absoluta todos los aspectos de la vida ciudadana.\nEl orden y la disciplina colectiva son superiores a cualquier libertad individual o de mercado."
        if x < 6: return "Fascismo Clásico", "Unidad nacional y corporativismo bajo un mando único autoritario que rechaza la lucha de clases.\nPriorizas la voluntad de la nación y la jerarquía tradicional por encima de todo."
        return "Derecha Radical Autoritaria", "Apoyas un mercado libre para las élites nacionales protegido por un régimen policial implacable.\nBuscas preservar las jerarquías tradicionales mediante la fuerza estatal y la disciplina social."
    elif y < -6:
        if x < -6: return "Anarcocomunismo", "Deseas una sociedad sin Estado ni propiedad privada basada en la ayuda mutua voluntaria.\nCrees en la autogestión comunal absoluta y la eliminación de toda jerarquía coercitiva."
        if x < -2: return "Mutualismo", "Propugnas una economía de mercado basada en cooperativas e intercambio justo sin lucro capitalista.\nRechazas al Estado en favor de la asociación voluntaria de productores libres."
        if x < 2: return "Anarquismo Individualista", "Sostienes la soberanía absoluta del individuo sobre su vida y trabajo frente a cualquier colectividad.\nRechazas toda autoridad externa defendiendo la asociación voluntaria por puro interés mutuo."
        if x < 6: return "Voluntarismo", "Afirmas que toda interacción humana debe ser voluntaria y que el Estado es una agresión ilegítima.\nCrees que cualquier servicio debe ser provisto mediante acuerdos libres y contratos privados."
        return "Anarcocapitalismo", "Abogas por la eliminación del Estado en favor de la propiedad privada absoluta y mercados libres.\nTodos los servicios deben ser privatizados y la justicia administrada por agencias en competencia."
    else:
        if x < -6: return "Socialismo de Estado", "Crees que el gobierno debe ser gestor de los medios de producción para garantizar la igualdad.\nLa autoridad estatal es necesaria para redistribuir la riqueza y asegurar necesidades básicas."
        if x < -2: return "Socialdemocracia", "Defiendes un sistema capitalista corregido por un fuerte Estado de bienestar y sindicatos potentes.\nBuscas armonizar el crecimiento económico con una red de seguridad social universal."
        if x < 2: return "Centrismo Pragmático", "Rechazas dogmas extremos buscando soluciones basadas en la evidencia y el consenso social.\nBuscas equilibrio entre libertad individual, eficiencia de mercado y protección social."
        if x < 6: return "Liberalismo Moderno", "Priorizas el progreso social y la libertad individual junto con una economía de mercado regulada.\nCrees que el Estado debe proteger los derechos civiles y garantizar una competencia justa."
        return "Liberalismo Clásico", "Defiendes un Estado mínimo que proteja la vida, la libertad y la propiedad privada de los ciudadanos.\nEl mercado libre es el mecanismo más eficiente para organizar la sociedad civil."

# 5. MOTOR DE NAVEGACIÓN Y CÁLCULO
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'history_x': [], 'history_y': []})

def responder(p):
    q = questions[st.session_state.idx]
    # Normalización para 85 preguntas
    if q['a'] == 'x':
        st.session_state.history_x.append(p * q['v'])
        st.session_state.history_y.append(0)
    else:
        st.session_state.history_y.append(p * q['v'])
        st.session_state.history_x.append(0)
    st.session_state.idx += 1

def volver():
    if st.session_state.idx > 0:
        st.session_state.idx -= 1
        st.session_state.history_x.pop()
        st.session_state.history_y.pop()

# --- PANTALLA RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown('<h1 class="main-title">Compás Político</h1>', unsafe_allow_html=True)
    
    # Cálculo final escalado a 10
    total_qx = len([q for q in questions if q['a'] == 'x'])
    total_qy = len([q for q in questions if q['a'] == 'y'])
    ux = max(min((sum(st.session_state.history_x) / (total_qx * 2)) * 10, 10), -10)
    uy = max(min((sum(st.session_state.history_y) / (total_qy * 2)) * 10, 10), -10)
    
    name, desc = get_full_ideology(ux, uy)
    
    # Buscar Líder más cercano
    match = min(LEADERS, key=lambda l: math.sqrt((ux - l['x'])**2 + (uy - l['y'])**2))['n']
    
    st.markdown(f'<div class="result-bubble"><span class="ideology-title">{name}</span><p class="ideology-desc">{desc}</p><span class="match-tag">Más cercano a: {match}</span></div>', unsafe_allow_html=True)
    
    # SVG Chart (Tamaño 600px para balance)
    px, py = 300 + (ux * 27), 300 - (uy * 27)
    leaders_svg = "".join([f'<circle cx="{300+(l["x"]*27)}" cy="{300-(l["y"]*27)}" r="5" fill="{l["c"]}" stroke="black"/><text x="{300+(l["x"]*27)}" y="{300-(l["y"]*27)+15}" font-size="11" text-anchor="middle" font-family="Arial" font-weight="bold">{l["n"]}</text>' for l in LEADERS])
    
    svg = f"""
    <div style="display:flex; justify-content:center; padding:20px;">
        <svg width="600" height="600" viewBox="0 0 600 600" style="border:4px solid #333; background:white;">
            <rect width="300" height="300" fill="#FFB2B2" opacity="0.6"/><rect x="300" width="300" height="300" fill="#B2B2FF" opacity="0.6"/>
            <rect y="300" width="300" height="300" fill="#B2FFB2" opacity="0.6"/><rect x="300" y="300" width="300" height="300" fill="#FFFFB2" opacity="0.6"/>
            <line x1="300" y1="0" x2="300" y2="600" stroke="black" stroke-width="3"/><line x1="0" y1="300" x2="600" y2="300" stroke="black" stroke-width="3"/>
            <text x="520" y="325" font-weight="900" font-size="16">DERECHA</text><text x="10" y="325" font-weight="900" font-size="16">IZQUIERDA</text>
            <text x="310" y="30" font-weight="900" font-size="16">AUTORITARIO</text><text x="310" y="585" font-weight="900" font-size="16">LIBERTARIO</text>
            {leaders_svg}
            <circle cx="{px}" cy="{py}" r="12" fill="red" stroke="white" stroke-width="4"/><text x="{px}" y="{py-20}" fill="red" font-weight="950" font-size="22" text-anchor="middle">TÚ</text>
        </svg>
    </div>
    """
    components.html(svg, height=650)
    
    if st.button("🔄 REINICIAR TEST"):
        st.session_state.update({'idx': 0, 'history_x': [], 'history_y': []})
        st.rerun()

# --- PANTALLA PREGUNTAS ---
else:
    st.markdown('<h1 class="main-title">Compás Político</h1>', unsafe_allow_html=True)
    
    if st.session_state.idx == 0:
        st.markdown('<div class="welcome-box"><b>Bienvenido.</b> Este test de alta precisión evaluará tu posición en el espectro político a través de 85 variables socioeconómicas. Responde con honestidad.</div>', unsafe_allow_html=True)
    
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
        st.button("⬅️ Volver a la pregunta anterior", on_click=volver)
        st.markdown('</div>', unsafe_allow_html=True)
