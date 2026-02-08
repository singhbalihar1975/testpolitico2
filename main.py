import streamlit as st
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Compás Político", layout="centered")

# 2. ESTILOS CSS (Centrado, Botones Suaves y Barras de Separación)
st.markdown("""
    <style>
    /* Fondo azul claro original */
    .stApp { background-color: #EBF8FF; }
    
    /* Centrado absoluto del bloque principal */
    .main .block-container {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        text-align: center; max-width: 800px;
    }

    .main-title { font-size: 45px; font-weight: 800; color: #1E3A8A; margin-bottom: 20px; width: 100%; }
    
    /* Caja de pregunta */
    .question-container { 
        margin: 20px auto; width: 100%; max-width: 650px;
        min-height: 100px; display: flex; align-items: center; justify-content: center;
    }
    .question-text { font-size: 26px !important; font-weight: 700; color: #1E3A8A; line-height: 1.3; }
    
    .warning-box { 
        background-color: #FFFBEB; border: 1px solid #F59E0B; border-radius: 15px;
        padding: 20px; margin: 10px auto 25px auto; max-width: 600px;
        color: #92400E; text-align: center; font-weight: 600; font-size: 16px;
    }

    /* BOTONES: Redondeados, azules y con la barra gris debajo de cada uno */
    div.stButton > button {
        width: 100% !important; 
        max-width: 600px !important; 
        height: 58px !important;
        border-radius: 15px !important; 
        font-size: 18px !important;
        background-color: #DBEAFE !important; 
        color: #1E40AF !important;
        border: 1px solid #BFDBFE !important;
        /* La barra gris ligera que pediste entre botones */
        border-bottom: 4px solid #CBD5E1 !important; 
        margin: 10px auto !important;
        display: block !important;
        font-weight: 600;
        transition: 0.2s;
    }
    div.stButton > button:hover { 
        background-color: #BFDBFE !important; 
        transform: scale(1.01); 
    }

    /* Separador gris específico para antes del botón "Volver" */
    .separator {
        width: 100%; max-width: 600px;
        border-top: 2px solid #CBD5E1;
        margin: 25px auto;
    }

    .result-bubble {
        background-color: white; border-radius: 25px; padding: 40px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 2px solid #BFDBFE;
        text-align: center; margin: 20px auto; width: 100%; max-width: 600px;
    }
    .ideology-title { font-size: 36px !important; font-weight: 900; color: #2563EB; text-transform: uppercase; margin: 0; }
    
    .stProgress { max-width: 600px; margin: 0 auto; }
    iframe { display: block; margin: 0 auto; border-radius: 15px; background: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. BASE DE DATOS: 45 LÍDERES
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
    total_eje = len([qu for qu in questions if qu["a"] == q["a"]])
    val = (puntos / 2) * (10 / (total_eje / 2)) * q["v"]
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    st.session_state.idx += 1

# --- PANTALLA DE RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown('<div class="main-title">Compás Político</div>', unsafe_allow_html=True)
    x, y = st.session_state.x, st.session_state.y

    # Lógica de Ideologías
    if y > 6:
        if x < -6: id_nom, desc = "Marxismo-Leninismo", "Abolición del capitalismo mediante un Estado centralizado y poderoso."
        elif x > 6: id_nom, desc = "Fascismo / Nacionalismo", "Estado totalitario con economía dirigida y enfoque nacionalista."
        elif x < -2: id_nom, desc = "Socialismo Autoritario", "Igualdad económica mediante control gubernamental estricto."
        elif x > 2: id_nom, desc = "Conservadurismo Autoritario", "Estado enfocado en la moral tradicional y el orden absoluto."
        else: id_nom, desc = "Totalitarismo", "Control total del Estado sobre todos los aspectos de la vida."
    elif y < -6:
        if x < -6: id_nom, desc = "Anarco-Comunismo", "Sociedad sin clases ni Estado, basada en la cooperación voluntaria."
        elif x > 6: id_nom, desc = "Anarco-Capitalismo", "Propiedad privada absoluta y eliminación total del gobierno."
        elif x < -2: id_nom, desc = "Mutualismo", "Economía de mercado basada en cooperativas sin jerarquías."
        elif x > 2: id_nom, desc = "Minarquismo", "El Estado solo existe para proteger la propiedad y la vida."
        else: id_nom, desc = "Libertarismo Radical", "Oposición frontal a cualquier regulación estatal."
    elif y > 2:
        if x < -5: id_nom, desc = "Socialismo de Estado", "Gestión pública de recursos con regulaciones sociales firmes."
        elif x > 5: id_nom, desc = "Derecha Conservadora", "Libre mercado y defensa de valores tradicionales."
        elif x < -1: id_nom, desc = "Estatismo de Izquierda", "Prioridad al gasto público y control social moderado."
        elif x > 1: id_nom, desc = "Democracia Cristiana", "Economía social de mercado con enfoque en familia y orden."
        else: id_nom, desc = "Populismo", "Liderazgo fuerte que apela al pueblo contra las élites."
    elif y < -2:
        if x < -5: id_nom, desc = "Socialismo Libertario", "Igualdad social rechazando estructuras de mando."
        elif x > 5: id_nom, desc = "Liberalismo Radical", "Libertad económica extrema y libertades civiles totales."
        elif x < -1: id_nom, desc = "Progresismo", "Derechos de minorías y justicia social redistributiva."
        elif x > 1: id_nom, desc = "Liberalismo Progresista", "Libertad individual con Estado que corrige desigualdades."
        else: id_nom, desc = "Individualismo", "La libertad personal es la máxima prioridad."
    else:
        if x < -5: id_nom, desc = "Socialismo Democrático", "Igualdad mediante el sistema parlamentario."
        elif x > 5: id_nom, desc = "Liberalismo Clásico", "Libre mercado, propiedad y libertades limitadas."
        elif x < -2: id_nom, desc = "Socialdemocracia", "Capitalismo con fuerte Estado del bienestar."
        elif x > 2: id_nom, desc = "Neoliberalismo", "Reducción del gasto público y privatización."
        elif abs(x) < 1.5: id_nom, desc = "Centrismo Pragmático", "Soluciones técnicas evitando extremos."
        else: id_nom, desc = "Centro-Moderado", "Postura equilibrada entre los distintos ejes."

    st.markdown(f'<div class="result-bubble"><p class="ideology-title">{id_nom}</p><p class="ideology-desc">{desc}</p></div>', unsafe_allow_html=True)

    # GRÁFICO
    leaders_html = "".join([f"""
        <div style="position:absolute; width:8px; height:8px; background:{l['c']}; border-radius:50%; left:{50 + (l['x']*4.5)}%; top:{50 - (l['y']*4.5)}%; transform:translate(-50%,-50%); border:1px solid #000; z-index:2;"></div>
        <div style="position:absolute; font-size:9px; font-weight:bold; left:{50 + (l['x']*4.5)}%; top:{50 - (l['y']*4.5)}%; transform:translate(-50%, 6px); color:#334155; z-index:2; white-space:nowrap;">{l['n']}</div>
    """ for l in LEADERS])

    user_x = max(2, min(98, 50 + (x * 4.5)))
    user_y = max(2, min(98, 50 - (y * 4.5)))

    compass_code = f"""
    <div style="position:relative; width:600px; height:600px; margin:auto; background:white; border:3px solid #1e293b; overflow:hidden; font-family:sans-serif; border-radius:10px;">
        <div style="position:absolute; width:50%; height:50%; top:0; left:0; background:rgba(239,68,68,0.15);"></div>
        <div style="position:absolute; width:50%; height:50%; top:0; right:0; background:rgba(59,130,246,0.15);"></div>
        <div style="position:absolute; width:50%; height:50%; bottom:0; left:0; background:rgba(34,197,94,0.15);"></div>
        <div style="position:absolute; width:50%; height:50%; bottom:0; right:0; background:rgba(234,179,8,0.15);"></div>
        <div style="position:absolute; width:100%; height:2px; background:#1e293b; top:50%;"></div>
        <div style="position:absolute; width:2px; height:100%; background:#1e293b; left:50%;"></div>
        <div style="position:absolute; top:8px; width:100%; text-align:center; font-weight:900; font-size:14px; color:#1e293b;">AUTORITARIO</div>
        <div style="position:absolute; bottom:8px; width:100%; text-align:center; font-weight:900; font-size:14px; color:#1e293b;">LIBERTARIO</div>
        <div style="position:absolute; top:48%; left:8px; font-weight:900; font-size:14px; color:#1e293b;">IZQUIERDA</div>
        <div style="position:absolute; top:48%; right:8px; font-weight:900; font-size:14px; color:#1e293b;">DERECHA</div>
        {leaders_html}
        <div style="position:absolute; width:16px; height:16px; background:red; border:3px solid white; border-radius:50%; left:{user_x}%; top:{user_y}%; transform:translate(-50%,-50%); z-index:10; box-shadow:0 0 10px red;"></div>
        <div style="position:absolute; color:red; font-weight:900; font-size:16px; left:{user_x}%; top:{user_y}%; transform:translate(-50%, 14px); z-index:11; font-family:sans-serif; text-shadow:1px 1px white;">TÚ</div>
    </div>
    """
    components.html(compass_code, height=640)

    st.markdown('<div class="action-area">', unsafe_allow_html=True)
    if st.button("🖨️ IMPRIMIR / GUARDAR PDF"):
        components.html("<script>window.print();</script>", height=0)
    
    if st.button("🔄 REPETIR EL TEST"):
        st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANTALLA DE PREGUNTAS ---
else:
    st.markdown('<div class="main-title">Compás Político</div>', unsafe_allow_html=True)
    
    if st.session_state.idx == 0:
        st.markdown('<div class="warning-box">⚠️ Si no sabes lo que significa la pregunta, pon <b>Neutral / No lo sé</b>.</div>', unsafe_allow_html=True)
    
    st.progress(st.session_state.idx / len(questions))
    st.write(f"<p style='text-align:center; color:#64748B; font-weight:bold;'>Pregunta {st.session_state.idx + 1} de {len(questions)}</p>", unsafe_allow_html=True)
    
    st.markdown(f'<div class="question-container"><span class="question-text">{questions[st.session_state.idx]["t"]}</span></div>', unsafe_allow_html=True)
    
    # Botones de respuesta con la barra gris (border-bottom) definida en el CSS
    st.button("✅ Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("👍 De acuerdo", on_click=responder, args=(1,))
    st.button("😐 Neutral / No lo sé", on_click=responder, args=(0,))
    st.button("👎 En desacuerdo", on_click=responder, args=(-1,))
    st.button("❌ Totalmente en desacuerdo", on_click=responder, args=(-2,))

    # Botón Volver con separador visual
    if st.session_state.idx > 0:
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.markdown('<div class="action-area">', unsafe_allow_html=True)
        if st.button("⬅️ VOLVER A LA PREGUNTA ANTERIOR"):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px
            st.session_state.y -= py
            st.session_state.idx -= 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
