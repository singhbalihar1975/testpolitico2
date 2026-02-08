import streamlit as st

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Compás Político", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F0F8FF; }
    
    .question-text {
        text-align: center;
        font-size: 28px !important; 
        font-weight: 700;
        color: #1E3A8A;
        margin: 25px 0px;
        line-height: 1.2;
    }

    /* BOTONES AZUL CLARO ALINEADOS A LA IZQUIERDA */
    div.stButton {
        display: flex;
        justify-content: flex-start;
        padding-left: 5%;
    }

    div.stButton > button {
        width: 500px !important; 
        height: 55px !important;
        border-radius: 12px !important;
        font-size: 17px !important;
        background-color: #BEE3F8 !important; 
        color: #2C5282 !important;
        border: none !important;
        margin: 3px 0px !important;
        transition: 0.2s;
        text-align: left !important;
        padding-left: 20px !important;
    }

    div.stButton > button:hover { 
        background-color: #90CDF4 !important;
        transform: translateX(5px);
    }

    /* GRÁFICO */
    .map-container {
        position: relative; width: 500px; height: 500px; 
        margin: 20px auto; background: white;
        border: 2px solid #CBD5E0; border-radius: 8px;
    }
    .axis-h { position: absolute; width: 100%; height: 2px; background: #A0AEC0; top: 50%; }
    .axis-v { position: absolute; width: 2px; height: 100%; background: #A0AEC0; left: 50%; }
    
    .label-leader {
        position: absolute;
        font-size: 10px;
        font-weight: bold;
        color: #2D3748;
        text-align: center;
        width: 70px;
        transform: translateX(-50%);
        margin-top: 15px;
    }

    .dot { 
        position: absolute; border-radius: 50%; 
        width: 12px; height: 12px; 
        transform: translate(-50%, -50%);
    }
    
    .user-dot {
        width: 22px; height: 22px; background: red;
        border: 3px solid white; box-shadow: 0 0 10px red;
        z-index: 100;
    }

    .final-btn > div.stButton > button {
        background-color: #2B6CB0 !important;
        color: white !important;
        width: 100% !important;
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. LÍDERES
LEADERS = [
    {"n": "Milei", "x": 8.5, "y": -8.5, "c": "#F6AD55"},
    {"n": "Stalin", "x": -9, "y": 9, "c": "#F56565"},
    {"n": "Hitler", "x": 8, "y": 9.5, "c": "#4A5568"},
    {"n": "Mao", "x": -9.5, "y": 8.5, "c": "#E53E3E"},
    {"n": "Gandhi", "x": -6.5, "y": -7.5, "c": "#68D391"},
    {"n": "Thatcher", "x": 7.5, "y": 6.5, "c": "#4299E1"},
    {"n": "Castro", "x": -8.5, "y": 7, "c": "#38A169"},
    {"n": "Friedman", "x": 8, "y": -5, "c": "#ECC94B"},
    {"n": "Sanders", "x": -5, "y": -3, "c": "#63B3ED"}
]

# 3. 85 PREGUNTAS (Simplificadas para 4º ESO)
questions = [
    # ECONÓMICAS (X)
    {"t": "El gobierno no debería decir a las empresas cuánto tienen que pagar a sus trabajadores.", "a": "x", "v": 1},
    {"t": "La sanidad debería ser gratis y pagada con los impuestos de todos.", "a": "x", "v": -1},
    {"t": "El Estado debería ser el dueño de las empresas de luz y agua.", "a": "x", "v": -1},
    {"t": "Es mejor que los colegios sean privados para que haya competencia.", "a": "x", "v": 1},
    {"t": "Los que más dinero ganan deben pagar muchos más impuestos.", "a": "x", "v": -1},
    {"t": "El gobierno debería poner límites al precio de la comida básica.", "a": "x", "v": -1},
    {"t": "Si una empresa va a quebrar, el gobierno no debería ayudarla con dinero público.", "a": "x", "v": 1},
    {"t": "Es mejor comprar productos de nuestro país que traerlos de fuera.", "a": "x", "v": -1},
    {"t": "Cualquiera debería poder abrir un negocio sin pedir tantos permisos al gobierno.", "a": "x", "v": 1},
    {"t": "Las huelgas de trabajadores hacen más daño que bien a la economía.", "a": "x", "v": 1},
    {"t": "El gobierno debe asegurar que todo el mundo tenga una casa, aunque sea regalada.", "a": "x", "v": -1},
    {"t": "El libre mercado es la mejor forma de que un país sea rico.", "a": "x", "v": 1},
    {"t": "Hacerse rico es un mérito personal y el Estado no debería quitarte ese dinero.", "a": "x", "v": 1},
    {"t": "Los sindicatos tienen demasiado poder hoy en día.", "a": "x", "v": 1},
    {"t": "El transporte público debería ser totalmente gratuito.", "a": "x", "v": -1},
    {"t": "La competencia entre empresas hace que los productos sean más baratos.", "a": "x", "v": 1},
    {"t": "El Estado debería dar un sueldo básico a todos los ciudadanos solo por existir.", "a": "x", "v": -1},
    {"t": "Pedir préstamos al banco debería tener un interés controlado por el gobierno.", "a": "x", "v": -1},
    {"t": "Las herencias no deberían tener impuestos; el dinero es de la familia.", "a": "x", "v": 1},
    {"t": "La mayoría de servicios públicos funcionan peor que los privados.", "a": "x", "v": 1},
    {"t": "El gobierno debería prohibir que las empresas despidan a gente si tienen beneficios.", "a": "x", "v": -1},
    {"t": "Los paraísos fiscales deberían desaparecer para que todos paguen por igual.", "a": "x", "v": -1},
    {"t": "El capitalismo es el sistema más justo que existe.", "a": "x", "v": 1},
    {"t": "Las grandes fortunas deberían repartirse entre los más pobres.", "a": "x", "v": -1},
    {"t": "Si trabajas más, es justo que ganes mucho más que los demás.", "a": "x", "v": 1},
    {"t": "El Estado no debería cobrar impuestos por la gasolina o el diésel.", "a": "x", "v": 1},
    {"t": "Las medicinas deberían ser gratis para todo el mundo sin excepción.", "a": "x", "v": -1},
    {"t": "Es mejor que el dinero esté en el bolsillo de la gente que en el del gobierno.", "a": "x", "v": 1},
    {"t": "Debería estar prohibido que una sola empresa controle todo un mercado (monopolio).", "a": "x", "v": -1},
    {"t": "La publicidad engañosa debería estar castigada con multas muy altas.", "a": "x", "v": -1},
    {"t": "La propiedad privada es sagrada y nadie debería tocarla.", "a": "x", "v": 1},
    {"t": "El gobierno debería crear más empresas públicas para dar trabajo.", "a": "x", "v": -1},
    {"t": "Los bancos centrales no deberían existir.", "a": "x", "v": 1},
    {"t": "La desigualdad de dinero es natural y siempre existirá.", "a": "x", "v": 1},
    {"t": "La universidad pública es una pérdida de dinero si no hay trabajo para todos.", "a": "x", "v": 1},
    {"t": "El gobierno debería vigilar que las empresas no contaminen nada.", "a": "x", "v": -1},
    {"t": "Bajar los impuestos a las empresas hace que contraten a más gente.", "a": "x", "v": 1},
    {"t": "La tecnología y los robots deberían pertenecer a todos, no solo a los dueños.", "a": "x", "v": -1},
    {"t": "Si el gobierno gasta mucho, la moneda pierde valor (inflación).", "a": "x", "v": 1},
    {"t": "La luz y el gas deberían tener un precio fijo puesto por el Estado.", "a": "x", "v": -1},
    {"t": "No debería haber fronteras para el comercio entre países.", "a": "x", "v": 1},
    {"t": "El Estado gasta demasiado dinero en cosas que no sirven para nada.", "a": "x", "v": 1},
    {"t": "Es injusto que haya gente con mil millones de euros mientras otros pasan hambre.", "a": "x", "v": -1},

    # SOCIALES / AUTORIDAD (Y)
    {"t": "Obedecer a los padres y a los profesores es la base de una buena sociedad.", "a": "y", "v": 1},
    {"t": "Cada uno debería poder decir lo que quiera, aunque moleste a otros.", "a": "y", "v": -1},
    {"t": "El gobierno debería poner leyes más duras contra los delincuentes.", "a": "y", "v": 1},
    {"t": "El aborto debería ser legal y una decisión de la mujer.", "a": "y", "v": -1},
    {"t": "Hace falta un líder fuerte que ponga orden cuando las cosas van mal.", "a": "y", "v": 1},
    {"t": "La religión no debería influir en las leyes de un país.", "a": "y", "v": -1},
    {"t": "El ejército es necesario para mantener la seguridad de la nación.", "a": "y", "v": 1},
    {"t": "La eutanasia (ayudar a morir a alguien muy enfermo) debería ser legal.", "a": "y", "v": -1},
    {"t": "El Estado debería vigilar internet para evitar que se digan mentiras.", "a": "y", "v": 1},
    {"t": "Consumir drogas debería ser una elección libre de cada adulto.", "a": "y", "v": -1},
    {"t": "Nuestra bandera y nuestro país son lo más importante.", "a": "y", "v": 1},
    {"t": "El matrimonio entre personas del mismo sexo es un derecho justo.", "a": "y", "v": -1},
    {"t": "Debería haber más cámaras de vigilancia en las calles para evitar robos.", "a": "y", "v": 1},
    {"t": "La educación sexual en el instituto es fundamental.", "a": "y", "v": -1},
    {"t": "Es necesario controlar más quién entra en nuestro país (fronteras).", "a": "y", "v": 1},
    {"t": "La cultura de nuestro país debe ser protegida frente a culturas extranjeras.", "a": "y", "v": 1},
    {"t": "Protestar en la calle cortando el tráfico debería estar prohibido.", "a": "y", "v": 1},
    {"t": "Las tradiciones de toda la vida se están perdiendo y eso es malo.", "a": "y", "v": 1},
    {"t": "El Estado no tiene por qué saber lo que hago en mi vida privada.", "a": "y", "v": -1},
    {"t": "La pena de muerte debería existir para crímenes muy horribles.", "a": "y", "v": 1},
    {"t": "Es más importante el orden público que la libertad individual.", "a": "y", "v": 1},
    {"t": "Cualquier persona debería poder vestirse o ser como quiera sin juicios.", "a": "y", "v": -1},
    {"t": "La disciplina en los colegios debería ser mucho más estricta.", "a": "y", "v": 1},
    {"t": "Insultar a los símbolos nacionales (himno, bandera) debería ser delito.", "a": "y", "v": 1},
    {"t": "El gobierno debería prohibir los videojuegos violentos.", "a": "y", "v": 1},
    {"t": "Las minorías deben tener leyes especiales que las protejan.", "a": "y", "v": -1},
    {"t": "El servicio militar debería volver a ser obligatorio.", "a": "y", "v": 1},
    {"t": "La policía necesita más autoridad para hacer su trabajo.", "a": "y", "v": 1},
    {"t": "La pornografía debería estar prohibida o muy controlada.", "a": "y", "v": 1},
    {"t": "No se debe permitir que la gente falte al respeto a las religiones.", "a": "y", "v": 1},
    {"t": "La globalización está borrando lo que nos hace únicos como país.", "a": "y", "v": 1},
    {"t": "Los científicos deberían poder clonar humanos si sirve para curar enfermedades.", "a": "y", "v": -1},
    {"t": "La familia formada por padre y madre es el modelo ideal.", "a": "y", "v": 1},
    {"t": "El arte no debería ser censurado, aunque sea provocativo.", "a": "y", "v": -1},
    {"t": "La cárcel debe ser un lugar de castigo, no un hotel.", "a": "y", "v": 1},
    {"t": "Fumar tabaco debería estar prohibido en todos los lugares públicos.", "a": "y", "v": 1},
    {"t": "Cada pueblo tiene derecho a decidir si quiere ser independiente.", "a": "y", "v": -1},
    {"t": "El Estado debería fomentar que la gente tenga más hijos.", "a": "y", "v": 1},
    {"t": "La tecnología está haciendo que la gente sea menos respetuosa.", "a": "y", "v": 1},
    {"t": "Debería ser legal llevar armas para defenderse.", "a": "y", "v": -1},
    {"t": "La justicia debe ser rápida, aunque a veces se pierdan derechos del acusado.", "a": "y", "v": 1},
    {"t": "El pasado de nuestra nación es algo de lo que estar muy orgullosos.", "a": "y", "v": 1}
]

# 4. LÓGICA DE ESTADO
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})

def responder(puntos):
    q = questions[st.session_state.idx]
    # Normalizamos el impacto según el número de preguntas de cada eje
    total_x = len([qu for qu in questions if qu["a"] == "x"])
    total_y = len([qu for qu in questions if qu["a"] == "y"])
    
    if q["a"] == "x": 
        val = (puntos / 2) * (10 / (total_x / 2)) * q["v"]
        st.session_state.x += val
    else: 
        val = (puntos / 2) * (10 / (total_y / 2)) * q["v"]
        st.session_state.y += val
    
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    st.session_state.idx += 1

# --- PANTALLA FINAL ---
if st.session_state.idx >= len(questions):
    st.title("📍 Tu Resultado Final")
    x, y = st.session_state.x, st.session_state.y

    # Determinación simple de ideología
    if y > 2:
        res = "Autoritario"
        if x > 2: id_nom = "Derecha Conservadora"
        elif x < -2: id_nom = "Izquierda Autoritaria"
        else: id_nom = "Populismo de Orden"
    elif y < -2:
        res = "Libertario"
        if x > 2: id_nom = "Liberalismo / Libertarismo"
        elif x < -2: id_nom = "Anarquismo / Socialismo Libertario"
        else: id_nom = "Progresismo Radical"
    else:
        if x > 2: id_nom = "Liberalismo Clásico"
        elif x < -2: id_nom = "Socialdemocracia"
        else: id_nom = "Centro Político"

    st.success(f"Tu perfil es: **{id_nom}**")

    # Dibujar gráfico
    labels_html = ""
    for l in LEADERS:
        pos_x = 50 + (l["x"] * 4.5)
        pos_y = 50 - (l["y"] * 4.5)
        labels_html += f"""
            <div class="dot" style="left:{pos_x}%; top:{pos_y}%; background:{l['c']};"></div>
            <div class="label-leader" style="left:{pos_x}%; top:{pos_y}%;">{l['n']}</div>
        """
    
    # Limitar usuario al cuadro
    ux = max(2, min(98, 50 + (x * 4.5)))
    uy = max(2, min(98, 50 - (y * 4.5)))

    st.markdown(f"""
        <div class="map-container">
            <div class="axis-h"></div>
            <div class="axis-v"></div>
            <div style="position:absolute; top:2%; left:42%; font-weight:bold; color:#718096; font-size:12px;">AUTORITARIO</div>
            <div style="position:absolute; bottom:2%; left:43%; font-weight:bold; color:#718096; font-size:12px;">LIBERTARIO</div>
            <div style="position:absolute; top:48%; left:1%; font-weight:bold; color:#718096; font-size:12px;">IZQUIERDA</div>
            <div style="position:absolute; top:48%; right:1%; font-weight:bold; color:#718096; font-size:12px;">DERECHA</div>
            {labels_html}
            <div class="dot user-dot" style="left:{ux}%; top:{uy}%;"></div>
            <div class="label-leader" style="left:{ux}%; top:{uy}%; color:red; font-size:14px; font-weight:900;">TÚ</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="final-btn">', unsafe_allow_html=True)
    
    # Resumen para descarga
    resumen = f"""COMPÁS POLÍTICO - RESULTADOS
----------------------------------
Ideología estimada: {id_nom}
Puntuación Económica (X): {x:.2f} (Derecha si es positivo)
Puntuación Social (Y): {y:.2f} (Autoritario si es positivo)

Para guardar como PDF, selecciona 'Imprimir' en tu navegador y elige 'Guardar como PDF'."""
    
    st.download_button("📄 DESCARGAR RESULTADO (.txt)", resumen, file_name="mi_compas_politico.txt")
    
    if st.button("🔄 REPETIR EL TEST"):
        st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANTALLA DE PREGUNTAS ---
else:
    st.title("Compás Político")
    st.write(f"Pregunta {st.session_state.idx + 1} de {len(questions)}")
    st.progress((st.session_state.idx) / len(questions))
    
    st.markdown(f'<div class="question-text">{questions[st.session_state.idx]["t"]}</div>', unsafe_allow_html=True)
    
    st.button("✅ Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("👍 De acuerdo", on_click=responder, args=(1,))
    st.button("😐 Neutral / No lo sé", on_click=responder, args=(0,))
    st.button("👎 En desacuerdo", on_click=responder, args=(-1,))
    st.button("❌ Totalmente en desacuerdo", on_click=responder, args=(-2,))

    if st.session_state.idx > 0:
        st.write("---")
        if st.button("⬅️ Volver a la anterior"):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px
            st.session_state.y -= py
            st.session_state.idx -= 1
            st.rerun()
