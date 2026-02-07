import streamlit as st

# 1. Configuración de página y Estética
st.set_page_config(page_title="Brújula Política Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #e3f2fd; }
    
    /* Botones centrados y con longitud uniforme */
    div.stButton > button {
        width: 100%;
        border-radius: 15px;
        height: 3.5em;
        font-weight: bold;
        font-size: 16px;
        background-color: white;
        border: 2px solid #1565c0;
        color: #1565c0;
        margin-bottom: 10px;
    }
    
    /* Texto de ideología en azul más oscuro que el fondo */
    .ideologia-box {
        background-color: #bbdefb;
        color: #0d47a1;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        border: 2px solid #90caf9;
        margin-bottom: 20px;
    }

    /* Contenedor del mapa con punto rojo */
    .map-container {
        position: relative;
        display: flex;
        justify-content: center;
        margin: auto;
        width: 100%;
        max-width: 400px;
    }
    .red-dot {
        position: absolute;
        width: 14px;
        height: 14px;
        background-color: #ff0000;
        border-radius: 50%;
        border: 2px solid white;
        transform: translate(-50%, -50%);
        z-index: 10;
        box-shadow: 0px 0px 5px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicializar estado
if 'idx' not in st.session_state:
    st.session_state.idx, st.session_state.x, st.session_state.y = 0, 0.0, 0.0
    st.session_state.history = []

# 3. Banco de 85 Preguntas
questions = [
    # (Preguntas 1-65 anteriores se mantienen...)
    {"t": "1. El mercado libre beneficia a todos a largo plazo.", "a": "x", "v": 1},
    {"t": "2. La sanidad debe ser 100% pública y gratuita.", "a": "x", "v": -1},
    {"t": "3. El estado debe regular los precios del alquiler.", "a": "x", "v": -1},
    {"t": "4. La privatización de empresas eléctricas es positiva.", "a": "x", "v": 1},
    {"t": "5. Los impuestos a las grandes fortunas deben subir.", "a": "x", "v": -1},
    {"t": "6. El proteccionismo protege el empleo local.", "a": "x", "v": -1},
    {"t": "7. El salario mínimo debería eliminarse.", "a": "x", "v": 1},
    {"t": "8. El medio ambiente es más importante que el PIB.", "a": "x", "v": -1},
    {"t": "9. Las subvenciones a empresas deben desaparecer.", "a": "x", "v": 1},
    {"t": "10. La herencia es un derecho familiar intocable.", "a": "x", "v": 1},
    {"t": "11. La educación universitaria debe ser gratuita.", "a": "x", "v": -1},
    {"t": "12. La competencia siempre mejora la calidad.", "a": "x", "v": 1},
    {"t": "13. El estado debe garantizar un trabajo a todos.", "a": "x", "v": -1},
    {"t": "14. La propiedad privada debe ser absoluta.", "a": "x", "v": 1},
    {"t": "15. Los bancos centrales no deberían existir.", "a": "x", "v": 1},
    {"t": "16. La infraestructura debe ser estatal.", "a": "x", "v": -1},
    {"t": "17. El comercio global reduce la pobreza.", "a": "x", "v": 1},
    {"t": "18. La especulación financiera debe prohibirse.", "a": "x", "v": -1},
    {"t": "19. El gasto público excesivo daña la economía.", "a": "x", "v": 1},
    {"t": "20. La caridad es mejor que el bienestar estatal.", "a": "x", "v": 1},
    {"t": "21. Los paraísos fiscales son legítimos.", "a": "x", "v": 1},
    {"t": "22. El estado debe rescatar sectores clave.", "a": "x", "v": -1},
    {"t": "23. La austeridad es necesaria en crisis.", "a": "x", "v": 1},
    {"t": "24. La desigualdad es natural en el progreso.", "a": "x", "v": 1},
    {"t": "25. El sindicato tiene demasiado poder.", "a": "x", "v": 1},
    {"t": "26. La moneda debe estar ligada al oro.", "a": "x", "v": 1},
    {"t": "27. La automatización requiere renta básica.", "a": "x", "v": -1},
    {"t": "28. Las patentes frenan el progreso humano.", "a": "x", "v": -1},
    {"t": "29. El consumo es el motor de la felicidad.", "a": "x", "v": 1},
    {"t": "30. La jornada laboral debe ser de 30 horas.", "a": "x", "v": -1},
    {"t": "31. La meritocracia es real en el capitalismo.", "a": "x", "v": 1},
    {"t": "32. Los monopolios naturales deben ser públicos.", "a": "x", "v": -1},
    {"t": "33. El FMI ayuda a las naciones pobres.", "a": "x", "v": 1},
    {"t": "34. La obediencia a la autoridad es una virtud.", "a": "y", "v": 1},
    {"t": "35. El aborto debe ser legal y seguro.", "a": "y", "v": -1},
    {"t": "36. La religión no debe influir en la política.", "a": "y", "v": -1},
    {"t": "37. Se necesita un líder fuerte para la nación.", "a": "y", "v": 1},
    {"t": "38. La marihuana debería ser legalizada.", "a": "y", "v": -1},
    {"t": "39. La cadena perpetua es necesaria.", "a": "y", "v": 1},
    {"t": "40. Las fronteras deben estar controladas.", "a": "y", "v": 1},
    {"t": "41. El feminismo actual es necesario.", "a": "y", "v": -1},
    {"t": "42. La vigilancia masiva evita el terrorismo.", "a": "y", "v": 1},
    {"t": "43. La libertad individual es absoluta.", "a": "y", "v": -1},
    {"t": "44. La eutanasia debe ser un derecho legal.", "a": "y", "v": -1},
    {"t": "45. El servicio militar debería ser obligatorio.", "a": "y", "v": 1},
    {"t": "46. La familia tradicional es el pilar social.", "a": "y", "v": 1},
    {"t": "47. La pornografía debería ser ilegal.", "a": "y", "v": 1},
    {"t": "48. El arte no debe ser censurado nunca.", "a": "y", "v": -1},
    {"t": "49. La pena de muerte es justa a veces.", "a": "y", "v": 1},
    {"t": "50. La inmigración descontrolada es un peligro.", "a": "y", "v": 1},
    {"t": "51. El matrimonio es solo hombre y mujer.", "a": "y", "v": 1},
    {"t": "52. La protesta callejera debe ser regulada.", "a": "y", "v": 1},
    {"t": "53. La identidad de género es una elección.", "a": "y", "v": -1},
    {"t": "54. La monarquía debe ser abolida.", "a": "y", "v": -1},
    {"t": "55. La policía necesita más poderes.", "a": "y", "v": 1},
    {"t": "56. La educación sexual debe ser obligatoria.", "a": "y", "v": -1},
    {"t": "57. La blasfemia no debería ser delito.", "a": "y", "v": -1},
    {"t": "58. Mi bandera es el símbolo más importante.", "a": "y", "v": 1},
    {"t": "59. La clonación humana debe permitirse.", "a": "y", "v": -1},
    {"t": "60. La corrección política limita la libertad.", "a": "y", "v": 1},
    {"t": "61. El multiculturalismo ha fallado.", "a": "y", "v": 1},
    {"t": "62. La experimentación con animales es necesaria.", "a": "y", "v": 1},
    {"t": "63. El estado debe promover la natalidad.", "a": "y", "v": 1},
    {"t": "64. La piratería digital no es un crimen real.", "a": "y", "v": -1},
    {"t": "65. La disciplina escolar debe ser estricta.", "a": "y", "v": 1},
    # --- NUEVAS PREGUNTAS (66-85) ---
    {"t": "66. La inteligencia artificial debe ser regulada por el estado.", "a": "y", "v": 1},
    {"t": "67. La energía nuclear es una solución necesaria.", "a": "x", "v": 1},
    {"t": "68. Los animales deben tener derechos legales similares a los humanos.", "a": "y", "v": -1},
    {"t": "69. El espacio debe ser colonizado por empresas privadas.", "a": "x", "v": 1},
    {"t": "70. La libertad de expresión incluye el derecho a ofender.", "a": "y", "v": -1},
    {"t": "71. El estado debería financiar las artes y la cultura.", "a": "x", "v": -1},
    {"t": "72. La globalización destruye las identidades nacionales.", "a": "y", "v": 1},
    {"t": "73. El capitalismo es incompatible con la sostenibilidad.", "a": "x", "v": -1},
    {"t": "74. Los ciudadanos deberían votar directamente todas las leyes.", "a": "y", "v": -1},
    {"t": "75. El sistema de prisiones debe enfocarse en la rehabilitación.", "a": "y", "v": -1},
    {"t": "76. La riqueza es un indicador de esfuerzo personal.", "a": "x", "v": 1},
    {"t": "77. Los servicios de internet deben ser un derecho público.", "a": "x", "v": -1},
    {"t": "78. La religión debe enseñarse en escuelas públicas.", "a": "y", "v": 1},
    {"t": "79. Es legítimo que un país intervenga militarmente en otro por derechos humanos.", "a": "y", "v": 1},
    {"t": "80. Las criptomonedas deberían sustituir al dinero estatal.", "a": "x", "v": 1},
    {"t": "81. La meritocracia justifica las diferencias de salario.", "a": "x", "v": 1},
    {"t": "82. El estado debe prohibir la comida basura.", "a": "y", "v": 1},
    {"t": "83. La diversidad es la mayor fuerza de una sociedad.", "a": "y", "v": -1},
    {"t": "84. Las huelgas perjudican a la economía más de lo que ayudan.", "a": "x", "v": 1},
    {"t": "85. La tecnología nos hace menos libres.", "a": "y", "v": 1}
]

def get_ideology(x, y):
    if x > 15 and y > 15: return "Autoritarismo de Derecha (Conservadurismo)"
    if x < -15 and y > 15: return "Autoritarismo de Izquierda (Comunismo/Socialismo)"
    if x > 15 and y < -15: return "Libertarismo de Derecha (Anarcocapitalismo)"
    if x < -15 and y < -15: return "Libertarismo de Izquierda (Anarquismo)"
    if abs(x) <= 15 and abs(y) <= 15: return "Centro / Socialdemocracia"
    return "Tendencia Moderada"

def responder(m):
    q = questions[st.session_state.idx]
    p = m * q["v"]
    st.session_state.history.append((p if q["a"]=="x" else 0, p if q["a"]=="y" else 0))
    if q["a"]=="x": st.session_state.x += p
    else: st.session_state.y += p
    st.session_state.idx += 1

# --- PANTALLA DE RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown("<h1 style='text-align: center; color: #0d47a1;'>Tu Resultado Final</h1>", unsafe_allow_html=True)
    
    ideologia = get_ideology(st.session_state.x, st.session_state.y)
    st.markdown(f"<div class='ideologia-box'><h3>Tu Ideología es: {ideologia}</h3></div>", unsafe_allow_html=True)

    # Punto Rojo Dinámico (Escalado para 85 preguntas)
    # Rango máximo aprox +/- 170. Mapeamos a % de la imagen
    left_p = 50 + (st.session_state.x * 0.28) 
    top_p = 50 - (st.session_state.y * 0.28)

    st.markdown(f"""
        <div class="map-container">
            <img src="https://raw.githubusercontent.com/testpolitico2/main/chart.png" style="width:100%; border-radius: 10px;">
            <div class="red-dot" style="left: {left_p}%; top: {top_p}%;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Imagen de respaldo por si falla el HTML
    st.image("chart.png", caption="Ubicación en el Mapa")

    st.info(f"Coordenadas: Eje X: {round(st.session_state.x, 2)} | Eje Y: {round(st.session_state.y, 2)}")
    
    if st.button("🔄 Reiniciar el Test"):
        st.session_state.idx, st.session_state.x, st.session_state.y = 0, 0.0, 0.0
        st.session_state.history = []
        st.rerun()

# --- PANTALLA DE PREGUNTAS ---
else:
    st.markdown(f"<p style='text-align: center; color: #546e7a;'>Progreso: {st.session_state.idx + 1} de {len(questions)}</p>", unsafe_allow_html=True)
    st.progress(st.session_state.idx / len(questions))
    st.markdown(f"<h2 style='text-align: center; color: #1565c0;'>{questions[st.session_state.idx]['t']}</h2>", unsafe_allow_html=True)
    
    # Botones en columna centralizada
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        if st.button("✨ Totalmente de acuerdo"): responder(2); st.rerun()
        if st.button("👍 De acuerdo"): responder(1); st.rerun()
        if st.button("😐 Neutral / No sé"): responder(0); st.rerun()
        if st.button("👎 En desacuerdo"): responder(-1); st.rerun()
        if st.button("🔥 Totalmente en desacuerdo"): responder(-2); st.rerun()
        
        if st.session_state.idx > 0:
            st.write("")
            if st.button("⬅️ Volver atrás"):
                st.session_state.idx -= 1
                px, py = st.session_state.history.pop()
                st.session_state.x -= px
                st.session_state.y -= py
                st.rerun()
