import streamlit as st
import base64

# 1. ESTÉTICA RADICAL Y BURBUJAS CENTRADAS
st.set_page_config(page_title="Brújula Política: Edición Extrema", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Burbujas de respuesta: Centradas y Alargadas */
    div.stButton > button {
        width: 100% !important;
        max-width: 650px; 
        margin: 10px auto !important;
        display: block;
        border-radius: 40px;
        height: 3.8em;
        font-weight: bold;
        font-size: 17px;
        background-color: #1f2937;
        border: 2px solid #3b82f6;
        color: white;
        transition: all 0.25s ease;
    }
    div.stButton > button:hover {
        background-color: #3b82f6;
        border-color: #ffffff;
        transform: scale(1.02);
        box-shadow: 0px 0px 20px rgba(59, 130, 246, 0.4);
    }

    /* Mapa y Marcadores */
    .map-container {
        position: relative; 
        width: 480px; height: 480px; 
        margin: 30px auto; 
        border: 4px solid #3b82f6; 
        background-color: white;
        border-radius: 8px;
        overflow: hidden;
    }
    .chart-img { width: 100%; height: 100%; display: block; }
    
    .marker {
        position: absolute; transform: translate(-50%, -50%);
        border-radius: 50%; border: 1px solid white;
    }
    .user-marker {
        width: 30px; height: 30px; background: #ff0000; z-index: 100;
        box-shadow: 0 0 15px #ff0000; color: white; 
        display: flex; align-items: center; justify-content: center;
        font-size: 10px; font-weight: bold;
    }
    .leader-marker { width: 12px; height: 12px; z-index: 50; }

    @media print {
        .stButton, .stProgress, header, footer, .stMetric { display: none !important; }
        .map-container { border: 2px solid black !important; margin: 0 auto; }
        .stApp { background-color: white !important; color: black !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE RADICALIZACIÓN
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'eco': 0.0, 'glob': 0.0, 'hist': []})

def get_radical_value(m):
    sign = 1 if m >= 0 else -1
    return (m**2) * sign * 3.5  # Multiplicador agresivo para lanzar el punto a los bordes

# 3. LÍDERES HISTÓRICOS (Coordenadas extremas)
LEADERS = [
    {"n": "Milei", "x": 85, "y": -75, "c": "#facc15"},
    {"n": "Stalin", "x": -95, "y": 95, "c": "#ef4444"},
    {"n": "Hitler", "x": 90, "y": 98, "c": "#4b5563"},
    {"n": "Mao", "x": -98, "y": 85, "c": "#dc2626"},
    {"n": "Pol Pot", "x": -99, "y": 70, "c": "#7f1d1d"},
    {"n": "Pinochet", "x": 95, "y": 90, "c": "#1d4ed8"},
    {"n": "Rothbard", "x": 99, "y": -99, "c": "#f97316"},
    {"n": "Gandhi", "x": -65, "y": -80, "c": "#22c55e"}
]

# 4. LAS 85 PREGUNTAS
# a: eje (x/y), v: dirección, s: sub-eje (e=eco/industria, g=global/soberano)
questions = [
    {"t": "1. El mercado libre es el único sistema moral de cooperación.", "a": "x", "v": 1, "s": "e"},
    {"t": "2. La sanidad debe ser 100% pública y gratuita.", "a": "x", "v": -1, "s": None},
    {"t": "3. El estado debe regular los precios del alquiler.", "a": "x", "v": -1, "s": None},
    {"t": "4. La privatización de eléctricas es positiva.", "a": "x", "v": 1, "s": "e"},
    {"t": "5. Los impuestos a las grandes fortunas deben subir.", "a": "x", "v": -1, "s": None},
    {"t": "6. El proteccionismo protege el empleo local.", "a": "x", "v": -1, "s": "g"},
    {"t": "7. El salario mínimo debería eliminarse.", "a": "x", "v": 1, "s": None},
    {"t": "8. El medio ambiente es más importante que el PIB.", "a": "x", "v": -1, "s": "e"},
    {"t": "9. Las subvenciones a empresas deben desaparecer.", "a": "x", "v": 1, "s": None},
    {"t": "10. La herencia es un derecho familiar intocable.", "a": "x", "v": 1, "s": None},
    {"t": "11. Educación universitaria gratuita para todos.", "a": "x", "v": -1, "s": None},
    {"t": "12. La competencia siempre mejora la calidad.", "a": "x", "v": 1, "s": "e"},
    {"t": "13. El estado debe garantizar trabajo a todos.", "a": "x", "v": -1, "s": None},
    {"t": "14. La propiedad privada debe ser absoluta.", "a": "x", "v": 1, "s": None},
    {"t": "15. Los bancos centrales no deberían existir.", "a": "x", "v": 1, "s": None},
    {"t": "16. Infraestructuras básicas deben ser estatales.", "a": "x", "v": -1, "s": None},
    {"t": "17. El comercio global reduce la pobreza.", "a": "x", "v": 1, "s": "g"},
    {"t": "18. La especulación financiera debe prohibirse.", "a": "x", "v": -1, "s": None},
    {"t": "19. El gasto público excesivo daña la nación.", "a": "x", "v": 1, "s": None},
    {"t": "20. La caridad privada supera al bienestar estatal.", "a": "x", "v": 1, "s": None},
    {"t": "21. Los paraísos fiscales son legítimos.", "a": "x", "v": 1, "s": None},
    {"t": "22. Rescate estatal a empresas en crisis.", "a": "x", "v": -1, "s": None},
    {"t": "23. Austeridad fiscal en tiempos de crisis.", "a": "x", "v": 1, "s": None},
    {"t": "24. La desigualdad es un motor natural.", "a": "x", "v": 1, "s": None},
    {"t": "25. Los sindicatos tienen demasiado poder.", "a": "x", "v": 1, "s": None},
    {"t": "26. Volver al patrón oro.", "a": "x", "v": 1, "s": None},
    {"t": "27. Renta básica por automatización.", "a": "x", "v": -1, "s": None},
    {"t": "28. Abolir patentes farmacéuticas.", "a": "x", "v": -1, "s": None},
    {"t": "29. El consumo masivo es progreso.", "a": "x", "v": 1, "s": "e"},
    {"t": "30. Jornada laboral de 30 horas por ley.", "a": "x", "v": -1, "s": None},
    {"t": "31. La meritocracia es real hoy día.", "a": "x", "v": 1, "s": None},
    {"t": "32. Monopolios naturales deben ser públicos.", "a": "x", "v": -1, "s": None},
    {"t": "33. El FMI es beneficioso.", "a": "x", "v": 1, "s": "g"},
    {"t": "34. Obedecer a la autoridad es una virtud.", "a": "y", "v": 1, "s": None},
    {"t": "35. Aborto legal, seguro y gratuito.", "a": "y", "v": -1, "s": None},
    {"t": "36. Separación absoluta Iglesia-Estado.", "a": "y", "v": -1, "s": None},
    {"t": "37. Un líder fuerte para poner orden.", "a": "y", "v": 1, "s": None},
    {"t": "38. Legalización total de la marihuana.", "a": "y", "v": -1, "s": None},
    {"t": "39. Cadena perpetua para crímenes graves.", "a": "y", "v": 1, "s": None},
    {"t": "40. Control fronterizo militarizado.", "a": "y", "v": 1, "s": "g"},
    {"t": "41. El feminismo actual es necesario.", "a": "y", "v": -1, "s": None},
    {"t": "42. Vigilancia masiva contra terrorismo.", "a": "y", "v": 1, "s": None},
    {"t": "43. Libertad de expresión total (ofensa incluida).", "a": "y", "v": -1, "s": None},
    {"t": "44. Eutanasia como derecho legal.", "a": "y", "v": -1, "s": None},
    {"t": "45. Servicio militar obligatorio.", "a": "y", "v": 1, "s": "g"},
    {"t": "46. Familia tradicional como base social.", "a": "y", "v": 1, "s": None},
    {"t": "47. Prohibición de la pornografía.", "a": "y", "v": 1, "s": None},
    {"t": "48. El arte nunca debe ser censurado.", "a": "y", "v": -1, "s": None},
    {"t": "49. Pena de muerte en casos extremos.", "a": "y", "v": 1, "s": None},
    {"t": "50. La inmigración diluye la identidad nacional.", "a": "y", "v": 1, "s": "g"},
    {"t": "51. Matrimonio solo hombre-mujer.", "a": "y", "v": 1, "s": None},
    {"t": "52. Prohibir protestas que corten calles.", "a": "y", "v": 1, "s": None},
    {"t": "53. Género como construcción social.", "a": "y", "v": -1, "s": None},
    {"t": "54. Abolición de la monarquía.", "a": "y", "v": -1, "s": None},
    {"t": "55. Más poderes para la policía.", "a": "y", "v": 1, "s": None},
    {"t": "56. Educación sexual obligatoria.", "a": "y", "v": -1, "s": None},
    {"t": "57. No debe existir el delito de blasfemia.", "a": "y", "v": -1, "s": None},
    {"t": "58. La bandera es el símbolo máximo.", "a": "y", "v": 1, "s": "g"},
    {"t": "59. Permitir clonación humana.", "a": "y", "v": -1, "s": "e"},
    {"t": "60. La corrección política es censura.", "a": "y", "v": 1, "s": None},
    {"t": "61. El multiculturalismo ha fallado.", "a": "y", "v": 1, "s": "g"},
    {"t": "62. Experimentación animal necesaria.", "a": "y", "v": 1, "s": "e"},
    {"t": "63. Fomentar natalidad desde el estado.", "a": "y", "v": 1, "s": None},
    {"t": "64. La piratería digital no es robo.", "a": "y", "v": -1, "s": None},
    {"t": "65. Disciplina escolar estricta.", "a": "y", "v": 1, "s": None},
    {"t": "66. Control gubernamental de la IA.", "a": "y", "v": 1, "s": "e"},
    {"t": "67. Energía nuclear como solución.", "a": "x", "v": 1, "s": "e"},
    {"t": "68. Derechos legales para animales.", "a": "y", "v": -1, "s": "e"},
    {"t": "69. Colonización espacial privada.", "a": "x", "v": 1, "s": "e"},
    {"t": "70. Derecho a portar armas.", "a": "y", "v": -1, "s": None},
    {"t": "71. Subvencionar cine y cultura.", "a": "x", "v": -1, "s": None},
    {"t": "72. La globalización mata culturas locales.", "a": "y", "v": 1, "s": "g"},
    {"t": "73. El capitalismo destruye el planeta.", "a": "x", "v": -1, "s": "e"},
    {"t": "74. Democracia directa por internet.", "a": "y", "v": -1, "s": None},
    {"t": "75. Cárceles para castigo, no reinserción.", "a": "y", "v": 1, "s": None},
    {"t": "76. La riqueza es mérito individual.", "a": "x", "v": 1, "s": None},
    {"t": "77. Internet como derecho humano básico.", "a": "x", "v": -1, "s": None},
    {"t": "78. Religión obligatoria en escuelas.", "a": "y", "v": 1, "s": None},
    {"t": "79. Intervención militar por DDHH.", "a": "y", "v": 1, "s": "g"},
    {"t": "80. Criptomonedas sobre moneda estatal.", "a": "x", "v": 1, "s": None},
    {"t": "81. CEO ganando 500x que empleado es justo.", "a": "x", "v": 1, "s": None},
    {"t": "82. Prohibir comida basura por salud.", "a": "y", "v": 1, "s": "e"},
    {"t": "83. La diversidad es nuestra fuerza.", "a": "y", "v": -1, "s": "g"},
    {"t": "84. Las huelgas dañan la nación.", "a": "x", "v": 1, "s": None},
    {"t": "85. La tecnología nos deshumaniza.", "a": "y", "v": 1, "s": "e"}
]

def responder(m):
    q = questions[st.session_state.idx]
    val = get_radical_value(m) * q["v"]
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    if q["s"] == "e": st.session_state.eco += val
    if q["s"] == "g": st.session_state.glob += val
    st.session_state.idx += 1

# --- PANTALLAS ---
if st.session_state.idx >= len(questions):
    st.markdown("## 🏁 RESULTADOS FINALES")
    x, y = st.session_state.x, st.session_state.y
    
    # Análisis Ideológico Extremo
    if x > 50 and y > 50: i, d = "AUTORITARISMO NACIONAL", "Orden supremo, mercado jerárquico y defensa de la soberanía nacional."
    elif x < -50 and y > 50: i, d = "TOTALITARISMO COLECTIVISTA", "Control estatal absoluto y abolición de la propiedad privada."
    elif x > 50 and y < -50: i, d = "ANARCOCAPITALISMO", "Soberanía individual absoluta. El Estado es un agresor ilegítimo."
    elif x < -50 and y < -50: i, d = "ANARCOCOMUNISMO", "Sociedad sin clases ni estado basada en la cooperación mutua."
    else: i, d = "CENTRISMO", "Tus visiones son equilibradas o pragmáticas."

    st.success(f"**Ideología:** {i}")
    st.info(d)

    # Sub-ejes
    c1, c2 = st.columns(2)
    with c1: st.metric("🏭 Desarrollo", "Industrialista" if st.session_state.eco > 0 else "Ecologista")
    with c2: st.metric("🌐 Exterior", "Soberanista" if st.session_state.glob > 0 else "Globalista")

    # Mapa
    def get_b64(p):
        try:
            with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
        except: return ""
    
    b64 = get_b64("chart.png")
    l_html = ""
    for l in LEADERS:
        left, top = 50 + (l["x"]/2), 50 - (l["y"]/2)
        l_html += f'<div class="marker leader-marker" style="left:{left}%; top:{top}%; background:{l["c"]};"></div>'

    ux, uy = max(min(x, 100), -100), max(min(y, 100), -100)
    st.markdown(f"""
        <div class="map-container">
            <img src="data:image/png;base64,{b64}" class="chart-img">
            {l_html}
            <div class="marker user-marker" style="left:{50+ux/2}%; top:{50-uy/2}%;">TÚ</div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🖨️ GUARDAR PDF"):
        st.components.v1.html("<script>window.print();</script>", height=0)

    if st.button("🔄 REINICIAR"):
        st.session_state.update({'idx':0, 'x':0, 'y':0, 'eco':0, 'glob':0, 'hist':[]})
        st.rerun()

else:
    st.progress(st.session_state.idx / len(questions))
    st.markdown(f"<h2 style='text-align:center;'>{questions[st.session_state.idx]['t']}</h2>", unsafe_allow_html=True)
    
    if st.button("✨ Totalmente de acuerdo"): responder(2); st.rerun()
    if st.button("👍 De acuerdo"): responder(1); st.rerun()
    if st.button("⚪ Neutral"): responder(0); st.rerun()
    if st.button("👎 En desacuerdo"): responder(-1); st.rerun()
    if st.button("🔥 Totalmente en desacuerdo"): responder(-2); st.rerun()
    
    if st.session_state.idx > 0:
        if st.button("⬅️ Atrás"):
            st.session_state.idx -= 1
            hx, hy = st.session_state.hist.pop()
            st.session_state.x -= hx; st.session_state.y -= hy
            st.rerun()
