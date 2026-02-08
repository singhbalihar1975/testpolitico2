import streamlit as st
import streamlit.components.v1 as components
import math

# 1. CONFIGURACIÓN Y ESTILO (con fondo azul claro y tonos azules)
st.set_page_config(page_title="Compás Político", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #E0F2FE; } /* Fondo azul claro */
    .main .block-container { max-width: 850px; padding-top: 2rem; text-align: center; }
    
    .main-title { font-size: 60px; font-weight: 950; color: #1E3A8A; margin-bottom: 20px; text-align: center; width: 100%; } /* Azul oscuro para el título */
    .welcome-box { 
        background-color: #DBEAFE; /* Burbuja azul claro */
        border: 2px solid #3B82F6; 
        border-radius: 15px; 
        padding: 25px; 
        margin-bottom: 30px; 
        color: #1E40AF; /* Texto en azul más oscuro */
        text-align: center; 
        font-size: 18px; 
        font-weight: 500;
    }

    .q-counter { font-size: 18px; color: #1E40AF; font-weight: 700; margin-bottom: 10px; display: block; text-align: center; }
    
    .question-container { margin: 40px auto; min-height: 140px; display: flex; align-items: center; justify-content: center; max-width: 750px; }
    .question-text { font-size: 32px !important; font-weight: 800; color: #1E3A8A; line-height: 1.2; text-align: center; } /* Azul oscuro */

    /* Botones de Colores Semáforo con mismo tamaño */
    div.stButton > button { 
        width: 100% !important; 
        height: 58px !important; 
        border-radius: 14px !important; 
        font-size: 19px !important; 
        font-weight: 700; 
        margin-bottom: 10px !important; 
        border: none !important; 
        transition: transform 0.2s;
    }
    div.stButton > button:hover { transform: scale(1.02); }

    .stButton:nth-of-type(1) button { background-color: #059669 !important; color: white !important; } /* Totalmente acuerdo - Verde Fuerte */
    .stButton:nth-of-type(2) button { background-color: #A7F3D0 !important; color: #065F46 !important; } /* De acuerdo - Verde Pastel */
    .stButton:nth-of-type(3) button { background-color: #BFDBFE !important; color: #1E40AF !important; } /* Neutral - Azul Pastel más claro */
    .stButton:nth-of-type(4) button { background-color: #FECACA !important; color: #991B1B !important; } /* En desacuerdo - Rojo Pastel */
    .stButton:nth-of-type(5) button { background-color: #DC2626 !important; color: white !important; } /* Totalmente en desacuerdo - Rojo Fuerte */
    
    .back-btn button { 
        background-color: #93C5FD !important; /* Azul más oscuro para botón de atrás */
        color: white !important; 
        border: 2px solid #60A5FA !important; 
        height: 45px !important; 
        margin-top: 25px !important; 
        width: 100% !important; 
        border-radius: 14px !important;
    }

    .result-bubble { 
        background-color: #DBEAFE; /* Burbuja azul claro */
        border-radius: 30px; 
        padding: 40px; 
        border: 6px solid #3B82F6; 
        margin: 30px auto; 
        text-align: center; 
    }
    .ideology-title { font-size: 45px !important; font-weight: 950; color: #1D4ED8; text-transform: uppercase; display: block; text-align: center; margin-bottom: 10px; } /* Azul oscuro */
    .ideology-desc { font-size: 20px; color: #1E40AF; line-height: 1.5; margin-top: 15px; text-align: center; font-weight: 500;} /* Azul más oscuro */
    .match-tag { 
        font-size: 24px; 
        font-weight: 800; 
        color: #1E40AF; /* Azul oscuro */
        margin-top: 25px; 
        background: #BFDBFE; /* Azul pastel para la etiqueta */
        padding: 15px 30px; 
        border-radius: 20px; 
        display: inline-block; 
        border: 2px solid #60A5FA;
    }
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
    {"t": "El Estado debe gestionar sectores estratégicos como la energía y el agua.", "a": "x", "v": -1},
    {"t": "Privatizar empresas públicas mejora siempre la eficiencia del servicio.", "a": "x", "v": 1},
    {"t": "Los impuestos a las grandes fortunas deben subir drásticamente.", "a": "x", "v": -1},
    {"t": "El mercado libre sin regulaciones es el mejor motor de progreso.", "a": "x", "v": 1},
    {"t": "El Estado no debe rescatar bancos o empresas privadas con dinero público.", "a": "x", "v": 1},
    {"t": "Es necesario proteger la industria nacional con aranceles y subsidios.", "a": "x", "v": -1},
    {"t": "La propiedad privada es un derecho humano absoluto e intocable.", "a": "x", "v": 1},
    {"t": "El gobierno debería garantizar una Renta Básica Universal a cada ciudadano.", "a": "x", "v": -1},
    {"t": "Las herencias deberían tener un impuesto muy elevado para redistribuir la riqueza.", "a": "x", "v": -1},
    {"t": "Es injusto que los que más ganan paguen un porcentaje mayor de impuestos.", "a": "x", "v": 1},
    {"t": "El capitalismo explota intrínsecamente al trabajador asalariado.", "a": "x", "v": -1},
    {"t": "Los sindicatos son esenciales para equilibrar el poder empresarial y los derechos laborales.", "a": "x", "v": -1},
    {"t": "La competencia es siempre mejor que cualquier forma de planificación estatal.", "a": "x", "v": 1},
    {"t": "Controlar los precios de alquiler ayuda a los ciudadanos más vulnerables.", "a": "x", "v": -1},
    {"t": "El Banco Central debería desaparecer y el dinero ser libre.", "a": "x", "v": 1},
    {"t": "La desigualdad económica es necesaria para incentivar el esfuerzo y la innovación.", "a": "x", "v": 1},
    {"t": "El Estado debe financiar la investigación científica aunque no sea inmediatamente rentable.", "a": "x", "v": -1},
    {"t": "Las multinacionales tienen demasiado poder político y económico hoy en día.", "a": "x", "v": -1},
    {"t": "El gasto público excesivo es la raíz de los problemas económicos de un país.", "a": "x", "v": 1},
    {"t": "Las pensiones deberían ser gestionadas por sistemas de ahorro privado individual.", "a": "x", "v": 1},
    {"t": "La protección del medio ambiente es más importante que el crecimiento económico.", "a": "x", "v": -1},
    {"t": "Las criptomonedas no deben ser reguladas por ningún gobierno o entidad central.", "a": "x", "v": 1},
    {"t": "El Estado debe crear empleo directo en épocas de crisis económica.", "a": "x", "v": -1},
    {"t": "La especulación financiera debería estar prohibida o fuertemente limitada.", "a": "x", "v": -1},
    {"t": "Los servicios de correos, trenes y transporte deben ser exclusivamente públicos.", "a": "x", "v": -1},
    {"t": "Bajar impuestos a los ricos termina beneficiando a todos a largo plazo.", "a": "x", "v": 1},
    {"t": "La deuda externa de los países pobres debería ser condonada.", "a": "x", "v": -1},
    {"t": "El mercado libre no garantiza que todo el mundo tenga acceso a alimentación y vivienda.", "a": "x", "v": -1},
    {"t": "Las patentes farmacéuticas deberían ser de libre acceso en situaciones de pandemia.", "a": "x", "v": -1},
    {"t": "La bolsa de valores es una herramienta útil de inversión y desarrollo social.", "a": "x", "v": 1},
    {"t": "El dinero físico debería ser reemplazado por dinero digital emitido por el Estado.", "a": "x", "v": -1},
    {"t": "La caridad privada es más eficiente que la asistencia social del Estado.", "a": "x", "v": 1},
    {"t": "Los paraísos fiscales son un fraude a la sociedad y deben eliminarse globalmente.", "a": "x", "v": -1},
    {"t": "El Estado no debería pedir préstamos a bancos privados.", "a": "x", "v": 1},
    {"t": "Reducir la jornada laboral por ley sin bajar el sueldo es una medida justa y necesaria.", "a": "x", "v": -1},
    {"t": "Es justo que el Estado expropie tierras sin uso para fines agrícolas o sociales.", "a": "x", "v": -1},
    {"t": "El éxito económico depende más de la suerte o el origen que del trabajo duro.", "a": "x", "v": -1},
    {"t": "Gravar los robots o la automatización es necesario para proteger el empleo humano.", "a": "x", "v": -1},
    {"t": "El mercado libre de armas de fuego sería beneficioso para la autodefensa.", "a": "x", "v": 1},
    {"t": "La publicidad comercial no debería ser regulada en absoluto.", "a": "x", "v": 1},
    {"t": "El Estado debe tener control sobre los tipos de interés.", "a": "x", "v": -1},
    
    # SOCIALES
    {"t": "El aborto debe ser un derecho legal, seguro y gratuito para todas las mujeres.", "a": "y", "v": -1},
    {"t": "Se necesita un líder fuerte para imponer orden y disciplina en el país.", "a": "y", "v": 1},
    {"t": "La religión no debe influir en absoluto en la legislación o las políticas públicas.", "a": "y", "v": -1},
    {"t": "Todas las drogas deberían ser legales para consumo y venta regulada.", "a": "y", "v": -1},
    {"t": "La cadena perpetua es un castigo justo y necesario para delitos graves.", "a": "y", "v": 1},
    {"t": "La identidad nacional es más importante que los derechos individuales o globales.", "a": "y", "v": 1},
    {"t": "El matrimonio debe ser exclusivamente entre un hombre y una mujer.", "a": "y", "v": 1},
    {"t": "Las cámaras de vigilancia masiva son un precio aceptable por la seguridad.", "a": "y", "v": 1},
    {"t": "La libertad de expresión incluye el derecho a ofender a sensibilidades ajenas.", "a": "y", "v": -1},
    {"t": "La eutanasia es un derecho básico de la persona sobre su propio cuerpo.", "a": "y", "v": -1},
    {"t": "El servicio militar debería volver a ser obligatorio para los jóvenes.", "a": "y", "v": 1},
    {"t": "Las fronteras abiertas benefician a la humanidad y el desarrollo cultural.", "a": "y", "v": -1},
    {"t": "La patria es sagrada y merece cualquier sacrificio individual.", "a": "y", "v": 1},
    {"t": "La educación sexual en las escuelas corrompe la inocencia de los niños.", "a": "y", "v": 1},
    {"t": "La prostitución debe ser ilegal en todos los casos.", "a": "y", "v": 1},
    {"t": "Quemar la bandera nacional debería conllevar penas de cárcel.", "a": "y", "v": 1},
    {"t": "El feminismo actual ha ido demasiado lejos y es perjudicial.", "a": "y", "v": 1},
    {"t": "La experimentación con animales debería estar prohibida por ley.", "a": "y", "v": -1},
    {"t": "La pena de muerte es aceptable para crímenes atroces.", "a": "y", "v": 1},
    {"t": "El Estado debe proteger la lengua nacional por encima de otras.", "a": "y", "v": 1},
    {"t": "La meritocracia es un mito; el sistema es inherentemente injusto.", "a": "y", "v": -1},
    {"t": "La policía debería tener más autoridad para el uso de la fuerza.", "a": "y", "v": 1},
    {"t": "La pornografía es dañina para la sociedad y debería prohibirse por ley.", "a": "y", "v": 1},
    {"t": "El multiculturalismo debilita la cohesión social de un país.", "a": "y", "v": 1},
    {"t": "Un ciudadano tiene derecho a portar armas ocultas para su defensa.", "a": "y", "v": -1},
    {"t": "La globalización cultural es una forma de colonialismo moderno.", "a": "y", "v": 1},
    {"t": "El Estado debe financiar las artes y la cultura con dinero público.", "a": "y", "v": -1},
    {"t": "La obediencia a los padres es la base de una sociedad estable.", "a": "y", "v": 1},
    {"t": "Los sindicatos deberían estar prohibidos en sectores públicos esenciales.", "a": "y", "v": 1},
    {"t": "La inmigración ilegal es una invasión organizada de nuestro territorio.", "a": "y", "v": 1},
    {"t": "El cambio climático es una exageración usada para controlar a la población.", "a": "y", "v": 1},
    {"t": "La familia tradicional es el núcleo insustituible de la nación.", "a": "y", "v": 1},
    {"t": "Se debería prohibir el uso de símbolos religiosos ostentosos en público.", "a": "y", "v": -1}, # Cambiado para un enfoque más libertario/laicista
    {"t": "La corrección política limita nuestra libertad real de expresión.", "a": "y", "v": 1},
    {"t": "La autoridad del Estado emana de Dios o la Tradición, no del pueblo.", "a": "y", "v": 1},
    {"t": "Las huelgas deberían estar prohibidas en servicios básicos como la sanidad.", "a": "y", "v": 1},
    {"t": "El progreso tecnológico nos está deshumanizando.", "a": "y", "v": 1},
    {"t": "La libertad individual es siempre superior al bien común colectivo.", "a": "y", "v": -1},
    {"t": "El honor y la reputación son más importantes que la propia vida.", "a": "y", "v": 1},
    {"t": "La jerarquía social es natural y necesaria en la sociedad humana.", "a": "y", "v": 1},
    {"t": "Los presos deberían trabajar forzosamente para pagar su estancia en prisión.", "a": "y", "v": 1},
    {"t": "La historia debe enseñarse para fomentar el patriotismo y el orgullo nacional.", "a": "y", "v": 1}
]

# 4. LÓGICA DE IDEOLOGÍAS (25 CATEGORÍAS)
def get_full_ideology(x, y):
    if y > 6:
        if x < -6: return "Marxismo-Leninismo", "Buscas la abolición de las clases sociales mediante un Estado todopoderoso y una economía planificada centralmente.\nDefiendes la dictadura del proletariado como herramienta para eliminar la explotación capitalista y las jerarquías privadas."
        if x < -2: return "Nacionalbolchevismo", "Combinas la economía colectivista de estilo soviético con un nacionalismo extremo y una moral social conservadora.\nCrees en un Estado fuerte que proteja la soberanía nacional frente a influencias externas y mantenga el control económico."
        if x < 2: return "Totalitarismo Central", "Consideras que el Estado debe tener el control absoluto de todas las esferas de la vida ciudadana, sin excepciones.\nLa lealtad al gobierno y el orden social son los valores supremos por encima de cualquier derecho individual o de mercado."
        if x < 6: return "Fascismo Clásico", "Defiendes un Estado corporativo autoritario que unifique a la nación por encima de las divisiones de clase y partidos.\nRechazas tanto el liberalismo como el marxismo, priorizando la voluntad nacional, la jerarquía y el heroísmo colectivo."
        return "Derecha Radical Autoritaria", "Apoyas un sistema de mercado libre para las élites nacionales, protegido por un régimen policial y militar implacable.\nBuscas preservar las jerarquías tradicionales y los valores nacionales mediante la fuerza estatal y la disciplina social."
    elif y > 2:
        if x < -6: return "Socialismo de Estado", "Crees que el gobierno debe ser el dueño y gestor de los medios de producción para garantizar la igualdad social.\nLa autoridad estatal es necesaria para redistribuir la riqueza y asegurar que las necesidades básicas de todos sean cubiertas."
        if x < -2: return "Socialdemocracia", "Defiendes un sistema capitalista de mercado corregido por un fuerte Estado de bienestar y sindicatos potentes.\nEl objetivo es armonizar el crecimiento económico con una red de seguridad social que garantice salud, educación y pensiones."
        if x < 2: return "Centrismo Pragmático", "Rechazas los dogmas de izquierda y derecha, prefiriendo soluciones pragmáticas basadas en la evidencia y el consenso.\nBuscas un equilibrio entre la libertad individual, la eficiencia del mercado y una protección social moderada y sostenible."
        if x < 6: return "Conservadurismo", "Defiendes las instituciones tradicionales, el libre mercado moderado y el mantenimiento del orden social establecido.\nCrees en el cambio gradual y en la importancia de la religión, la familia y las leyes fuertes para preservar la civilización."
        return "Derecha Autoritaria", "Abogas por una economía de mercado muy abierta pero bajo un marco legal socialmente restrictivo y punitivo.\nEl Estado debe ser pequeño en lo económico pero extremadamente fuerte en la represión del crimen y el mantenimiento del orden."
    elif y > -2:
        if x < -6: return "Socialismo Democrático", "Buscas alcanzar la igualdad económica y social a través de métodos democráticos y la gestión pública de servicios clave.\nCrees que el capitalismo debe ser superado mediante reformas electorales que empoderen a la clase trabajadora de forma pacífica."
        if x < -2: return "Populismo de Izquierda", "Movilizas al pueblo contra las élites económicas mediante un liderazgo carismático y políticas de protección estatal directa.\nPriorizas la justicia social inmediata y el control soberano de los recursos nacionales frente a los mercados globales."
        if x < 2: return "Liberalismo Progresista", "Priorizas el progreso social y la libertad individual junto con una economía de mercado dinámica y regulada.\nCrees que el Estado debe proteger los derechos civiles de las minorías y garantizar una competencia justa en los negocios."
        if x < 6: return "Liberalismo Clásico", "Defiendes un Estado mínimo que se limite a proteger la vida, la libertad y la propiedad privada de los ciudadanos.\nEl mercado libre es el mecanismo más eficiente para organizar la sociedad y el individuo debe ser soberano en sus decisiones."
        return "Minarquismo", "Crees que el único papel legítimo del gobierno es la protección contra la agresión, el robo, el fraude y el cumplimiento de contratos.\nEl Estado solo debe gestionar la policía, los tribunales y la defensa nacional, dejando todo lo demás a la iniciativa privada."
    elif y > -6:
        if x < -6: return "Anarcosindicalismo", "Propones una sociedad organizada a través de sindicatos autogestionados de trabajadores, sin necesidad de un Estado central.\nLa acción directa y la propiedad colectiva de las fábricas son las bases para eliminar tanto al gobierno como al capital."
        if x < -2: return "Socialismo Libertario", "Buscas una organización social basada en la cooperación voluntaria y la eliminación de las jerarquías coercitivas y el lucro.\nDefiendes que la libertad individual solo es posible en una comunidad donde los recursos se gestionen de forma común y libre."
        if x < 2: return "Libertarismo de Izquierda", "Combinas una defensa radical de las libertades personales con una visión crítica de las grandes concentraciones de poder corporativo.\nApoyas la legalización total de conductas privadas y un mercado libre de privilegios estatales para fomentar la autonomía individual."
        if x < 6: return "Objetivismo", "Sostienes que la razón individual, el egoísmo racional y el capitalismo de laissez-faire son los pilares de la moralidad.\nEl Estado debe ser mínimo y solo proteger los derechos individuales, rechazando el altruismo y el colectivismo."
        return "Paleolibertarismo", "Unes el rechazo total al Estado económico con una defensa de los valores culturales tradicionales y las instituciones privadas.\nCrees que el mercado libre y la moralidad tradicional son los mejores pilares para una sociedad estable y próspera sin gobierno."
    else: # y <= -6
        if x < -6: return "Anarcocomunismo", "Sueñas con una sociedad sin Estado, sin clases y sin dinero, basada en el principio de 'a cada cual según su necesidad'.\nLa federación voluntaria de comunas libres es el modelo para alcanzar la verdadera igualdad y libertad humana total."
        if x < -2: return "Mutualismo", "Propones un mercado de cooperativas y artesanos basado en el intercambio justo y la ausencia de intereses o rentas capitalistas.\nLa banca mutua y la posesión basada en el uso reemplazan al Estado y a la propiedad privada acumulativa tradicional."
        if x < 2: return "Anarquismo Individualista", "Sostienes la soberanía absoluta del individuo sobre su propia vida y los frutos de su trabajo frente a cualquier colectividad.\nRechazas toda autoridad externa, sea estatal o social, defendiendo la asociación voluntaria basada únicamente en el interés mutuo."
        if x < 6: return "Voluntarismo", "Afirmas que todas las interacciones humanas deben ser totalmente voluntarias y que el Estado es una agresión intrínsecamente ilegítima.\nCrees que cualquier servicio, incluyendo la ley y la seguridad, debe ser provisto mediante acuerdos libres y contratos privados."
        return "Anarcocapitalismo", "Abogas por la eliminación total del Estado en favor de un sistema de propiedad privada absoluta y mercados libres competitivos.\nTodos los servicios públicos deben ser privatizados y la justicia debe ser administrada por agencias de protección en competencia."


# 5. MOTOR DE NAVEGACIÓN Y CÁLCULO
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'history_x': [], 'history_y': []})

def responder(p):
    q = questions[st.session_state.idx]
    
    # Añadir a la historia
    if q['a'] == 'x': 
        st.session_state.history_x.append(p * q['v'])
        st.session_state.history_y.append(0) # 0 para la otra coordenada si no se usa
    else: # q['a'] == 'y'
        st.session_state.history_y.append(p * q['v'])
        st.session_state.history_x.append(0) # 0 para la otra coordenada si no se usa
        
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
    total_score_x = sum(st.session_state.history_x)
    total_score_y = sum(st.session_state.history_y)
    
    # Máximo score posible por eje (cada pregunta contribuye con 2 o -2)
    max_score_x = len([q for q in questions if q['a'] == 'x']) * 2
    max_score_y = len([q for q in questions if q['a'] == 'y']) * 2
    
    ux = (total_score_x / max_score_x) * 10 if max_score_x > 0 else 0
    uy = (total_score_y / max_score_y) * 10 if max_score_y > 0 else 0
    
    # Asegurar que los valores estén dentro del rango [-10, 10]
    ux = max(min(ux, 10), -10)
    uy = max(min(uy, 10), -10)
    
    name, desc = get_full_ideology(ux, uy)
