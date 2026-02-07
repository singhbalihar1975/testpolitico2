import streamlit as st
import base64

# 1. Configuración de página y Estética Radical
st.set_page_config(page_title="Brújula Política: Edición Radical", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    
    /* Botones idénticos y grandes */
    div.stButton > button {
        width: 100% !important; max-width: 550px; margin: 10px auto !important;
        border-radius: 12px; height: 3.8em; font-weight: bold; font-size: 16px;
        background-color: white; border: 2px solid #0d47a1; color: #0d47a1;
        transition: 0.2s;
    }
    div.stButton > button:hover { background-color: #0d47a1; color: white; transform: scale(1.02); }

    /* Caja de Resultados */
    .result-header {
        background-color: #0d47a1; color: white; padding: 20px;
        border-radius: 15px 15px 0 0; text-align: center; margin-top: 20px;
    }
    .result-body {
        background-color: #e3f2fd; color: #0d47a1; padding: 20px;
        border-radius: 0 0 15px 15px; text-align: center; border: 2px solid #0d47a1;
        margin-bottom: 25px; font-weight: 500; line-height: 1.5;
    }

    /* MAPA Y POSICIONAMIENTO */
    .map-container {
        position: relative; width: 450px; height: 450px; 
        margin: 30px auto; border: 5px solid #0d47a1; border-radius: 10px;
        background-color: white; overflow: hidden;
    }
    .chart-img { width: 100%; height: 100%; display: block; }
    
    .dot {
        position: absolute; border-radius: 50%; border: 2px solid white;
        transform: translate(-50%, -50%); z-index: 10;
        display: flex; align-items: center; justify-content: center;
    }
    
    .user-dot {
        width: 28px; height: 28px; background-color: #ff0000;
        z-index: 100; box-shadow: 0 0 15px rgba(255,0,0,0.8);
        border: 3px solid white; color: white; font-size: 10px; font-weight: bold;
    }

    .leader-dot { width: 14px; height: 14px; }

    @media print {
        .stButton, .stProgress, header, footer { display: none !important; }
        .map-container { border: 2px solid black !important; margin: 0 auto; }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Motor de Radicalización y Estado
if 'idx' not in st.session_state:
    st.session_state.idx, st.session_state.x, st.session_state.y = 0, 0.0, 0.0
    st.session_state.eco, st.session_state.glob = 0.0, 0.0
    st.session_state.history = []

def get_radical_points(val):
    # Multiplica por 3 si es "Totalmente" para forzar los extremos
    if abs(val) == 2: return val * 3.0
    return val * 1.0

# 3. Líderes Mundiales (Coordenadas extremas para contraste)
LEADERS = [
    {"n": "Milei", "x": 165, "y": -150, "c": "#ffeb3b"},
    {"n": "Stalin", "x": -180, "y": 180, "c": "#b71c1c"},
    {"n": "Hitler", "x": 170, "y": 190, "c": "#424242"},
    {"n": "Mao", "x": -190, "y": 160, "c": "#f44336"},
    {"n": "Pol Pot", "x": -195, "y": 140, "c": "#880e4f"},
    {"n": "Gandhi", "x": -120, "y": -160, "c": "#4caf50"},
    {"n": "Pinochet", "x": 175, "y": 170, "c": "#0d47a1"},
    {"n": "Rothbard", "x": 190, "y": -195, "c": "#ff9800"}
]

# 4. Banco de 85 Preguntas
questions = [
    {"t": "El mercado libre beneficia a todos a largo plazo.", "a": "x", "v": 1, "s": "ind"},
    {"t": "La sanidad debe ser 100% pública y gratuita.", "a": "x", "v": -1, "s": None},
    {"t": "El estado debe regular los precios del alquiler.", "a": "x", "v": -1, "s": None},
    {"t": "La privatización de empresas eléctricas es positiva.", "a": "x", "v": 1, "s": "ind"},
    {"t": "Los impuestos a las grandes fortunas deben subir.", "a": "x", "v": -1, "s": None},
    {"t": "El proteccionismo nacional protege el empleo.", "a": "x", "v": -1, "s": "sob"},
    {"t": "El salario mínimo debería eliminarse.", "a": "x", "v": 1, "s": None},
    {"t": "El medio ambiente es más importante que el crecimiento económico.", "a": "x", "v": -1, "s": "eco"},
    {"t": "Las subvenciones a empresas privadas deben desaparecer.", "a": "x", "v": 1, "s": None},
    {"t": "La herencia es un derecho familiar intocable.", "a": "x", "v": 1, "s": None},
    {"t": "La educación universitaria debe ser gratuita para todos.", "a": "x", "v": -1, "s": None},
    {"t": "La competencia siempre mejora la calidad de los servicios.", "a": "x", "v": 1, "s": "ind"},
    {"t": "El estado debe garantizar un puesto de trabajo a cada ciudadano.", "a": "x", "v": -1, "s": None},
    {"t": "La propiedad privada debe ser absoluta y sin límites.", "a": "x", "v": 1, "s": None},
    {"t": "Los bancos centrales no deberían existir.", "a": "x", "v": 1, "s": None},
    {"t": "Las infraestructuras básicas (agua, luz) deben ser estatales.", "a": "x", "v": -1, "s": None},
    {"t": "El comercio global es la principal vía para reducir la pobreza.", "a": "x", "v": 1, "s": "glob"},
    {"t": "La especulación financiera debería estar prohibida.", "a": "x", "v": -1, "s": None},
    {"t": "El gasto público excesivo es la causa de todos los males económicos.", "a": "x", "v": 1, "s": None},
    {"t": "La caridad privada es más eficiente que la asistencia estatal.", "a": "x", "v": 1, "s": None},
    {"t": "Los paraísos fiscales son una respuesta legítima a la presión fiscal.", "a": "x", "v": 1, "s": None},
    {"t": "El estado debe rescatar a las empresas estratégicas en crisis.", "a": "x", "v": -1, "s": None},
    {"t": "La austeridad fiscal es necesaria para el crecimiento sano.", "a": "x", "v": 1, "s": None},
    {"t": "La desigualdad económica es un motor natural de progreso.", "a": "x", "v": 1, "s": None},
    {"t": "Los sindicatos tienen actualmente demasiado poder.", "a": "x", "v": 1, "s": None},
    {"t": "La moneda debería volver a estar respaldada por oro.", "a": "x", "v": 1, "s": None},
    {"t": "La automatización requiere la implantación de una Renta Básica.", "a": "x", "v": -1, "s": None},
    {"t": "Las patentes farmacéuticas frenan el progreso humano.", "a": "x", "v": -1, "s": None},
    {"t": "El consumo masivo es fundamental para la felicidad social.", "a": "x", "v": 1, "s": "ind"},
    {"t": "La jornada laboral debería reducirse por ley a 30 horas.", "a": "x", "v": -1, "s": None},
    {"t": "La obediencia a la autoridad es una virtud que debe enseñarse.", "a": "y", "v": 1, "s": None},
    {"t": "El aborto debe ser legal, seguro y gratuito.", "a": "y", "v": -1, "s": None},
    {"t": "La religión no debe tener ninguna influencia en las leyes.", "a": "y", "v": -1, "s": None},
    {"t": "Se necesita un líder fuerte para poner orden en el país.", "a": "y", "v": 1, "s": None},
    {"t": "El consumo de drogas debería ser una decisión privada legal.", "a": "y", "v": -1, "s": None},
    {"t": "La cadena perpetua es necesaria para crímenes atroces.", "a": "y", "v": 1, "s": None},
    {"t": "El control de fronteras debe ser estricto y militarizado.", "a": "y", "v": 1, "s": "sob"},
    {"t": "El feminismo actual es una lucha necesaria y justa.", "a": "y", "v": -1, "s": None},
    {"t": "La vigilancia estatal masiva es aceptable para evitar el terrorismo.", "a": "y", "v": 1, "s": None},
    {"t": "La libertad de expresión debe ser absoluta, incluso si ofende.", "a": "y", "v": -1, "s": None},
    {"t": "La eutanasia debe ser un derecho legal garantizado.", "a": "y", "v": -1, "s": None},
    {"t": "El servicio militar debería volver a ser obligatorio.", "a": "y", "v": 1, "s": "sob"},
    {"t": "La familia tradicional es la base de una sociedad estable.", "a": "y", "v": 1, "s": None},
    {"t": "La pornografía debería ser ilegal por su daño social.", "a": "y", "v": 1, "s": None},
    {"t": "El arte nunca debe ser censurado por motivos morales.", "a": "y", "v": -1, "s": None},
    {"t": "La pena de muerte es una medida justa en casos extremos.", "a": "y", "v": 1, "s": None},
    {"t": "La inmigración masiva pone en peligro la identidad nacional.", "a": "y", "v": 1, "s": "sob"},
    {"t": "El matrimonio solo debería ser entre un hombre y una mujer.", "a": "y", "v": 1, "s": None},
    {"t": "Las manifestaciones que bloquean calles deben ser prohibidas.", "a": "y", "v": 1, "s": None},
    {"t": "La identidad de género es una construcción social, no biológica.", "a": "y", "v": -1, "s": None},
    {"t": "La monarquía es una institución obsoleta que debe desaparecer.", "a": "y", "v": -1, "s": None},
    {"t": "La policía necesita más autoridad y menos restricciones.", "a": "y", "v": 1, "s": None},
    {"t": "La educación sexual en escuelas es esencial.", "a": "y", "v": -1, "s": None},
    {"t": "Blasfemar contra figuras religiosas no debería ser delito.", "a": "y", "v": -1, "s": None},
    {"t": "La bandera nacional es el símbolo más sagrado.", "a": "y", "v": 1, "s": "sob"},
    {"t": "La clonación humana debería permitirse para el progreso médico.", "a": "y", "v": -1, "s": "ind"},
    {"t": "La corrección política está destruyendo la libertad de expresión.", "a": "y", "v": 1, "s": None},
    {"t": "El multiculturalismo ha sido un fracaso en Occidente.", "a": "y", "v": 1, "s": "sob"},
    {"t": "La experimentación con animales es un mal necesario.", "a": "y", "v": 1, "s": "ind"},
    {"t": "El estado debe fomentar activamente la natalidad.", "a": "y", "v": 1, "s": None},
    {"t": "La piratería digital no es un crimen real contra la propiedad.", "a": "y", "v": -1, "s": None},
    {"t": "La disciplina en las escuelas debe volver a ser estricta.", "a": "y", "v": 1, "s": None},
    {"t": "La IA debe ser controlada por el gobierno para evitar riesgos.", "a": "y", "v": 1, "s": "ind"},
    {"t": "La energía nuclear es la mejor solución al cambio climático.", "a": "x", "v": 1, "s": "ind"},
    {"t": "Los animales deberían tener derechos legales similares a los humanos.", "a": "y", "v": -1, "s": "eco"},
    {"t": "La colonización del espacio debe ser liderada por empresas privadas.", "a": "x", "v": 1, "s": "ind"},
    {"t": "El estado debe financiar el cine y el teatro con dinero público.", "a": "x", "v": -1, "s": None},
    {"t": "La globalización destruye las culturas locales.", "a": "y", "v": 1, "s": "sob"},
    {"t": "El capitalismo es inherentemente destructivo para el planeta.", "a": "x", "v": -1, "s": "eco"},
    {"t": "Los ciudadanos deberían votar directamente todas las leyes por internet.", "a": "y", "v": -1, "s": None},
    {"t": "Las cárceles deben servir para castigar, no para reinsertar.", "a": "y", "v": 1, "s": None},
    {"t": "Tener éxito económico es prueba de esfuerzo y mérito personal.", "a": "x", "v": 1, "s": None},
    {"t": "Internet debería ser un servicio público gratuito e inalienable.", "a": "x", "v": -1, "s": None},
    {"t": "Debería haber clases de religión obligatorias en la escuela.", "a": "y", "v": 1, "s": None},
    {"t": "La intervención militar exterior es justa si protege los DDHH.", "a": "y", "v": 1, "s": "glob"},
    {"t": "Las criptomonedas son el futuro de la libertad económica.", "a": "x", "v": 1, "s": None},
    {"t": "Es justo que un CEO gane 500 veces más que un empleado.", "a": "x", "v": 1, "s": None},
    {"t": "El estado debería prohibir la comida basura por salud pública.", "a": "y", "v": 1, "s": "eco"},
    {"t": "La diversidad étnica es la mayor fortaleza de una nación.", "a": "y", "v": -1, "s": "glob"},
    {"t": "Las huelgas generales suelen hacer más daño que bien.", "a": "x", "v": 1, "s": None},
    {"t": "La tecnología nos está alejando de nuestra verdadera esencia.", "a": "y", "v": 1, "s": "eco"},
    {"t": "Los ricos deberían pagar un 90% de impuestos.", "a": "x", "v": -1, "s": None},
    {"t": "El estado debe prohibir los coches de combustión pronto.", "a": "x", "v": -1, "s": "eco"},
    {"t": "Sin una jerarquía clara, la sociedad colapsa.", "a": "y", "v": 1, "s": None},
    {"t": "El pasado siempre fue mejor que el presente.", "a": "y", "v": 1, "s": None}
]

def responder(m):
    q = questions[st.session_state.idx]
    p = get_radical_points(m) * q["v"]
    st.session_state.history.append((p if q["a"]=="x" else 0, p if q["a"]=="y" else 0))
    if q["a"] == "x": st.session_state.x += p
    else: st.session_state.y += p
    if q["s"] == "ind": st.session_state.eco += p
    if q["s"] == "glob": st.session_state.glob += p
    st.session_state.idx += 1

# --- LÓGICA DE PANTALLAS ---
if st.session_state.idx >= len(questions):
    st.markdown("<h1>📊 Informe de Ideología Radical</h1>", unsafe_allow_html=True)
    
    x, y = st.session_state.x, st.session_state.y
    if x > 50 and y > 50: 
        n, d = "AUTORITARISMO NACIONAL", "Defiendes un Estado implacable que preserve la tradición y el orden bajo una economía de mercado jerárquica."
    elif x < -50 and y > 50: 
        n, d = "COMUNISMO DE ESTADO", "Abogas por la colectivización forzosa y la eliminación de la propiedad privada bajo un mando central absoluto."
    elif x > 50 and y < -50: 
        n, d = "ANARCOCAPITALISMO", "Crees en la soberanía absoluta del individuo y la propiedad. El Estado es, para ti, un agresor que debe desaparecer."
    elif x < -50 and y < -50: 
        n, d = "ANARCOCOMUNISMO", "Buscas la disolución de toda jerarquía y la creación de comunidades voluntarias basadas en la ayuda mutua radical."
    else:
        n, d = "CENTRISMO PRAGMÁTICO", "Tus visiones evitan los extremos, buscando un equilibrio funcional entre libertad, igualdad y orden."

    st.markdown(f"<div class='result-header'><h2>{n}</h2></div><div class='result-body'><p>{d}</p></div>", unsafe_allow_html=True)

    # Sub-ejes
    c1, c2 = st.columns(2)
    with c1: st.info(f"⚙️ **Eje Industrial:** {'Productivista' if st.session_state.eco > 0 else 'Ecologista'}")
    with c2: st.info(f"🌐 **Eje Global:** {'Globalista' if st.session_state.glob > 0 else 'Soberanista'}")

    # Mapa con puntos (Cálculo preciso para chart de 450px)
    def get_b64(file):
        try:
            with open(file, "rb") as f: return base64.b64encode(f.read()).decode()
        except: return ""

    img_data = get_b64("chart.png")
    leader_html = ""
    for l in LEADERS:
        lx = 50 + (l["x"] * 0.22); ly = 50 - (l["y"] * 0.22)
        leader_html += f'<div class="dot leader-dot" style="left:{lx}%; top:{ly}%; background:{l["c"]};" title="{l["n"]}"></div>'

    ux = 50 + (x * 0.22); uy = 50 - (y * 0.22)
    
    st.markdown(f"""
        <div class="map-container">
            <img src="data:image/png;base64,{img_data}" class="chart-img">
            {leader_html}
            <div class="dot user-dot" style="left:{ux}%; top:{uy}%;">TÚ</div>
        </div>
        <p style='text-align:center; font-size:11px;'>🔴 Tú | 🟡 Milei | 🔴 Stalin | ⚫ Hitler | 🔴 Mao | 🟣 Pol Pot | 🔵 Pinochet</p>
    """, unsafe_allow_html=True)

    # Botón PDF / Imprimir
    if st.button("📄 GENERAR PDF / IMPRIMIR"):
        st.components.v1.html("<script>window.print();</script>", height=0)

    if st.button("🔄 REPETIR TEST"):
        st.session_state.idx, st.session_state.x, st.session_state.y = 0, 0, 0
        st.session_state.history = []
        st.rerun()

else:
    st.progress(st.session_state.idx / len(questions))
    st.markdown(f"<h3 style='text-align:center; color:#0d47a1; min-height:100px;'>{questions[st.session_state.idx]['t']}</h3>", unsafe_allow_html=True)
    
    if st.button("✨ Totalmente de acuerdo"): responder(2); st.rerun()
    if st.button("👍 De acuerdo"): responder(1); st.rerun()
    if st.button("⚪ Neutral / No sé"): responder(0); st.rerun()
    if st.button("👎 En desacuerdo"): responder(-1); st.rerun()
    if st.button("🔥 Totalmente en desacuerdo"): responder(-2); st.rerun()
    
    if st.session_state.idx > 0:
        if st.button("⬅️ VOLVER ATRÁS"):
            st.session_state.idx -= 1
            px, py = st.session_state.history.pop()
            st.session_state.x -= px; st.session_state.y -= py
            st.rerun()
