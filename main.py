import streamlit as st
import streamlit.components.v1 as components
import math

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Compás Político", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .main .block-container { max-width: 800px; padding-top: 2rem; text-align: center; }
    
    .centered-text { text-align: center; }
    .main-title { font-size: 50px; font-weight: 900; color: #1E3A8A; margin-bottom: 20px; text-align: center; width: 100%; }
    
    .welcome-box { background-color: #EFF6FF; border: 2px solid #3B82F6; border-radius: 15px; padding: 20px; margin-bottom: 30px; color: #1E40AF; }

    .q-counter { font-size: 18px; color: #64748B; font-weight: 700; margin-bottom: 10px; display: block; }
    
    .question-container { margin: 40px auto; min-height: 120px; display: flex; align-items: center; justify-content: center; }
    .question-text { font-size: 30px !important; font-weight: 800; color: #0F172A; line-height: 1.2; text-align: center; }

    /* Estilo de Botones con Colores Específicos */
    div.stButton > button { width: 100% !important; height: 55px !important; border-radius: 12px !important; font-size: 18px !important; font-weight: 700; margin-bottom: 8px !important; border: none !important; }
    
    /* Colores de respuestas */
    .stButton:nth-of-type(1) button { background-color: #059669 !important; color: white !important; } /* Verde Fuerte */
    .stButton:nth-of-type(2) button { background-color: #A7F3D0 !important; color: #065F46 !important; } /* Verde Pastel */
    .stButton:nth-of-type(3) button { background-color: #E2E8F0 !important; color: #475569 !important; } /* Gris */
    .stButton:nth-of-type(4) button { background-color: #FECACA !important; color: #991B1B !important; } /* Rojo Pastel */
    .stButton:nth-of-type(5) button { background-color: #DC2626 !important; color: white !important; } /* Rojo Fuerte */
    
    /* Botón Atrás */
    .back-btn button { background-color: transparent !important; color: #64748B !important; border: 1px solid #CBD5E1 !important; height: 40px !important; margin-top: 20px !important; }

    .result-bubble { background-color: white; border-radius: 25px; padding: 30px; border: 4px solid #3B82F6; margin-bottom: 20px; text-align: center; }
    .ideology-title { font-size: 40px !important; font-weight: 900; color: #1D4ED8; text-transform: uppercase; text-align: center; display: block; width: 100%; }
    .match-text { font-size: 22px; font-weight: 700; color: #1E40AF; margin-top: 15px; background: #DBEAFE; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS DE LÍDERES
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
    {"n": "Kim Jong-un", "x": -9.5, "y": 10, "c": "#E53E3E"}, {"n": "Mujica", "x": -7, "y": -4, "c": "#48BB78"}
]

# 3. PREGUNTAS (85)
questions = [
    # ECONÓMICAS
    {"t": "El salario mínimo debería ser eliminado para que las empresas contraten más.", "a": "x", "v": 1},
    {"t": "La sanidad debe ser 100% pública y gratuita para todos.", "a": "x", "v": -1},
    {"t": "El Estado debe poseer sectores estratégicos como energía y agua.", "a": "x", "v": -1},
    {"t": "Privatizar aeropuertos y trenes mejora la eficiencia.", "a": "x", "v": 1},
    {"t": "Los impuestos a las grandes fortunas deben subir drásticamente.", "a": "x", "v": -1},
    {"t": "El libre mercado sin regulaciones es el mejor motor de progreso.", "a": "x", "v": 1},
    {"t": "El Estado no debe rescatar empresas privadas con dinero público.", "a": "x", "v": 1},
    {"t": "Es necesario proteger la industria nacional con aranceles.", "a": "x", "v": -1},
    {"t": "La propiedad privada es un derecho humano absoluto.", "a": "x", "v": 1},
    {"t": "El gobierno debe garantizar un ingreso básico a cada ciudadano.", "a": "x", "v": -1},
    {"t": "Las herencias deberían tener un impuesto muy alto.", "a": "x", "v": -1},
    {"t": "Es injusto que quienes más ganan paguen un porcentaje mayor.", "a": "x", "v": 1},
    {"t": "El capitalismo explota intrínsecamente al trabajador.", "a": "x", "v": -1},
    {"t": "Los sindicatos son necesarios para equilibrar el poder empresarial.", "a": "x", "v": -1},
    {"t": "La competencia es siempre mejor que la planificación estatal.", "a": "x", "v": 1},
    # (Añadir el resto hasta 85 siguiendo el patrón)
]

# 4. LÓGICA DE IDEOLOGÍAS (25 categorías)
def get_ideology_details(x, y):
    if y > 6:
        if x < -6: return "Marxismo-Leninismo", "Estado totalitario con economía planificada. Buscas la abolición de clases mediante el control central absoluto."
        if x < -2: return "Nacionalbolchevismo", "Estado soviético en economía, pero nacionalista extremo y tradicionalista en cultura."
        if x < 2: return "Totalitarismo", "Control absoluto del Estado en todas las facetas de la vida, social y económica."
        if x < 6: return "Fascismo Clásico", "Corporativismo económico y ultranacionalismo autoritario para la unidad nacional."
        return "Derecha Radical", "Estado policial fuerte con capitalismo nacionalista y leyes sociales restrictivas."
    elif y < -6:
        if x < -6: return "Anarcocomunismo", "Sociedad sin dinero, sin clases y sin Estado basada en la ayuda mutua voluntaria."
        if x > 6: return "Anarcocapitalismo", "Privatización total de la ley y la seguridad. El mercado absoluto sin Estado."
        return "Libertarismo", "Máxima soberanía individual y mínima intervención estatal en cualquier área."
    else:
        if x < -4: return "Socialismo Democrático", "Justicia social mediante democracia y servicios públicos potentes."
        if x > 4: return "Liberalismo Clásico", "Estado mínimo que solo protege la vida, la libertad y la propiedad."
        return "Centrismo", "Moderación y pragmatismo sin dogmas extremos de izquierda o derecha."

def find_match(ux, uy):
    best_leader = None
    min_dist = float('inf')
    for l in LEADERS:
        dist = math.sqrt((ux - l['x'])**2 + (uy - l['y'])**2)
        if dist < min_dist:
            min_dist = dist
            best_leader = l['n']
    return best_leader

# 5. ESTADO
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x_pts': [], 'y_pts': []})

def handle_click(p):
    q = questions[st.session_state.idx]
    # Guardamos los puntos para poder retroceder
    if q['a'] == 'x': 
        st.session_state.x_pts.append(p * q['v'])
        st.session_state.y_pts.append(0)
    else:
        st.session_state.y_pts.append(p * q['v'])
        st.session_state.x_pts.append(0)
    st.session_state.idx += 1

def handle_back():
    if st.session_state.idx > 0:
        st.session_state.idx -= 1
        st.session_state.x_pts.pop()
        st.session_state.y_pts.pop()

# --- UI: RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown('<h1 class="main-title">Compás Político</h1>', unsafe_allow_html=True)
    
    # Cálculo final
    scale_factor = 10 / (len(questions) / 2)
    ux = max(min(sum(st.session_state.x_pts) * scale_factor, 10), -10)
    uy = max(min(sum(st.session_state.y_pts) * scale_factor, 10), -10)
    
    name, desc = get_ideology_details(ux, uy)
    match = find_match(ux, uy)
    
    st.markdown(f'<div class="result-bubble"><span class="ideology-title">{name}</span><p class="ideology-desc">{desc}</p><p class="match-text">Tu perfil es más cercano a: <b>{match}</b></p></div>', unsafe_allow_html=True)
    
    # SVG Chart (Tamaño medio para balance)
    px, py = 250 + (ux * 22), 250 - (uy * 22)
    leaders_svg = "".join([f'<circle cx="{250+(l["x"]*22)}" cy="{250-(l["y"]*22)}" r="5" fill="{l["c"]}" stroke="black"/><text x="{250+(l["x"]*22)}" y="{250-(l["y"]*22)+14}" font-size="10" text-anchor="middle" font-family="Arial" font-weight="bold">{l["n"]}</text>' for l in LEADERS])
    
    svg = f"""
    <div style="display:flex; justify-content:center; padding:20px;">
        <svg width="500" height="500" viewBox="0 0 500 500" style="border:3px solid #333; background:white;">
            <rect width="250" height="250" fill="#FFB2B2" opacity="0.6"/><rect x="250" width="250" height="250" fill="#B2B2FF" opacity="0.6"/>
            <rect y="250" width="250" height="250" fill="#B2FFB2" opacity="0.6"/><rect x="250" y="250" width="250" height="250" fill="#FFFFB2" opacity="0.6"/>
            <line x1="250" y1="0" x2="250" y2="500" stroke="black" stroke-width="2"/><line x1="0" y1="250" x2="500" y2="250" stroke="black" stroke-width="2"/>
            {leaders_svg}
            <circle cx="{px}" cy="{py}" r="10" fill="red" stroke="white" stroke-width="3"/>
            <text x="{px}" y="{py-15}" fill="red" font-weight="900" font-size="18" text-anchor="middle">TÚ</text>
        </svg>
    </div>
    """
    components.html(svg, height=550)
    
    if st.button("🔄 Reiniciar Test"):
        st.session_state.update({'idx': 0, 'x_pts': [], 'y_pts': []})
        st.rerun()

# --- UI: PREGUNTAS ---
else:
    st.markdown('<h1 class="main-title">Compás Político</h1>', unsafe_allow_html=True)
    
    if st.session_state.idx == 0:
        st.markdown('<div class="welcome-box"><b>¡Bienvenido!</b> Descubre tu posición exacta en el espectro político. Responde con sinceridad para obtener el resultado más preciso.</div>', unsafe_allow_html=True)
    
    st.markdown(f'<span class="q-counter">Pregunta {st.session_state.idx + 1} de {len(questions)}</span>', unsafe_allow_html=True)
    st.progress(st.session_state.idx / len(questions))
    
    st.markdown(f'<div class="question-container"><p class="question-text">{questions[st.session_state.idx]["t"]}</p></div>', unsafe_allow_html=True)
    
    st.button("✅ Totalmente de acuerdo", on_click=handle_click, args=(2,))
    st.button("👍 De acuerdo", on_click=handle_click, args=(1,))
    st.button("😐 Neutral", on_click=handle_click, args=(0,))
    st.button("👎 En desacuerdo", on_click=handle_click, args=(-1,))
    st.button("❌ Totalmente en desacuerdo", on_click=handle_click, args=(-2,))
    
    if st.session_state.idx > 0:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        st.button("⬅️ Volver a la pregunta anterior", on_click=handle_back)
        st.markdown('</div>', unsafe_allow_html=True)
