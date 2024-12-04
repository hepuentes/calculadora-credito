import streamlit as st
import math

# Función para formatear números con separadores de miles
def format_number(number):
    return "{:,.0f}".format(number).replace(",", ".")

# Datos para cada línea de crédito
LINEAS_DE_CREDITO = {
    "LoansiFlex": {
        "descripcion": "Crédito de libre inversión para empleados, independientes, personas naturales y pensionados.",
        "monto_min": 1000000,
        "monto_max": 20000000,
        "plazo_min": 12,
        "plazo_max": 60,
        "tasa_anual_efectiva": 25.89,
        "aval_porcentaje": 0.10,
        "seguro_vida_base": 150000
    },
    "Microflex": {
        "descripcion": "Crédito rotativo para personas en sectores informales, orientado a cubrir necesidades de liquidez rápida con pagos semanales.",
        "monto_min": 50000,
        "monto_max": 500000,
        "plazo_min": 4,
        "plazo_max": 8,
        "tasa_anual_efectiva": 25.89,
        "aval_porcentaje": 0.12,
    }
}

COSTOS_ASOCIADOS = {
    "Pagaré Digital": 2800,
    "Carta de Instrucción": 2800,
    "Custodia TVE": 5600,
    "Consulta Datacrédito": 11000
}

total_costos_asociados = sum(COSTOS_ASOCIADOS.values())

def calcular_seguro_vida(plazo, seguro_vida_base):
    años = plazo // 12
    return seguro_vida_base * años if años >= 1 else 0

# Configuración de la página
st.set_page_config(page_title="Simulador de Crédito Loansi", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
        .stSelectbox {
            margin-top: 0.2rem !important;
        }
        
        .stSelectbox > div > div {
            pointer-events: auto;
            background-color: transparent !important;
            border: 1px solid #404040 !important;
            color: inherit !important;
            cursor: pointer;
        }

        .description-text {
            font-size: 1.1rem !important;
            margin: 0.8rem 0 !important;
            line-height: 1.4 !important;
        }

        .value-description {
            font-size: 1.1rem !important;
            margin: 0.5rem 0 !important;
        }

        .plazo-text {
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important;
        }

        .stSlider > div > div > div {
            font-size: 1.2rem !important;
        }

        .currency-symbol {
            font-size: 1.3rem;
            margin-top: 0.7rem;
            margin-left: 0.2rem;
        }

        .result-box {
            background-color: rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            text-align: center;
        }
        
        .result-text {
            font-size: 1.2rem;
            margin-bottom: 0.8rem;
        }
        
        .result-amount {
            font-size: 2.2rem;
            font-weight: 700;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }

        .detail-item {
            display: flex;
            justify-content: space-between;
            padding: 0.75rem 0;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            color: inherit;
        }
        
        .disclaimer {
            background-color: rgba(0, 0, 0, 0.03);
            border-radius: 10px;
            padding: 1.5rem;
            margin-top: 2rem;
            border: 1px solid rgba(0, 0, 0, 0.1);
            color: inherit;
        }

        .disclaimer p {
            font-size: 0.9rem;
            line-height: 1.6;
            margin: 0;
            text-align: justify;
            color: inherit;
        }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.title("Simulador de Crédito Loansi")

# Selección de línea de crédito
st.header("Selecciona la Línea de Crédito")
tipo_credito = st.selectbox("", options=list(LINEAS_DE_CREDITO.keys()), index=0)
detalles = LINEAS_DE_CREDITO[tipo_credito]

st.markdown(f"<p class='description-text'>{detalles['descripcion']}</p>", unsafe_allow_html=True)

# Entrada del monto con símbolo de peso
st.header("Escribe el valor del crédito")
st.markdown(f"<p class='value-description'>Ingresa un valor entre $ {format_number(detalles['monto_min'])} y $ {format_number(detalles['monto_max'])} COP</p>", unsafe_allow_html=True)

col1, col2 = st.columns([0.5,20])
with col1:
    st.markdown('<div class="currency-symbol">$</div>', unsafe_allow_html=True)
with col2:
    monto = st.number_input("", 
                           min_value=detalles["monto_min"],
                           max_value=detalles["monto_max"],
                           step=1000,
                           value=detalles["monto_min"],
                           format="%d")

# Slider de plazo
if tipo_credito == "LoansiFlex":
    st.header("Plazo en Meses")
    plazo = st.slider("", 
                     min_value=detalles["plazo_min"], 
                     max_value=detalles["plazo_max"], 
                     step=12,
                     value=detalles["plazo_min"])
    frecuencia_pago = "Mensual"
else:
    st.header("Plazo en Semanas")
    plazo = st.slider("", 
                     min_value=detalles["plazo_min"], 
                     max_value=detalles["plazo_max"], 
                     step=1,
                     value=detalles["plazo_min"])
    frecuencia_pago = "Semanal"

# Cálculos
aval = monto * detalles["aval_porcentaje"]
seguro_vida = calcular_seguro_vida(plazo, detalles.get("seguro_vida_base", 0)) if tipo_credito == "LoansiFlex" else 0
total_financiar = monto + aval + total_costos_asociados + seguro_vida

# Cálculo de cuota
tasa_mensual = detalles["tasa_anual_efectiva"] / 12 / 100

if tipo_credito == "LoansiFlex":
    cuota = (total_financiar * tasa_mensual) / (1 - (1 + tasa_mensual) ** -plazo)
else:
    tasa_semanal = ((1 + detalles["tasa_anual_efectiva"]/100) ** (1/52)) - 1
    cuota = (total_financiar * tasa_semanal) / (1 - (1 + tasa_semanal) ** -plazo)

# Mostrar resultado
st.markdown(f"""
<div class="result-box">
    <p class="result-text">Pagarás {plazo} cuotas por un valor aproximado de:</p>
    <div class="result-amount">$ {format_number(cuota)} {frecuencia_pago}</div>
</div>
""", unsafe_allow_html=True)

# Detalles del crédito simplificados
with st.expander("Ver Detalles del Crédito"):
    detalles_orden = [
        ("Dinero total desembolsado", f"$ {format_number(monto)} COP"),
        ("Plazo", f"{plazo} {'meses' if tipo_credito == 'LoansiFlex' else 'semanas'}"),
        ("Frecuencia de Pago", frecuencia_pago),
        ("Tasa Efectiva Anual (E.A.)", f"{detalles['tasa_anual_efectiva']:.2f}%"),
        ("Valor Cuota a Pagar", f"$ {format_number(cuota)} COP"),
    ]
    
    for titulo, valor in detalles_orden:
        st.markdown(f"""
        <div class="detail-item">
            <span class="detail-label">{titulo}</span>
            <span class="detail-value">{valor}</span>
        </div>
        """, unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class="disclaimer">
    <p>Estos valores son aproximados, los cuales fueron calculados teniendo en cuenta una tasa de interés variable, así como los demás conceptos asociados al crédito, y representan una referencia para el usuario, por lo tanto, podrán variar de conformidad con el perfil crediticio del cliente y las políticas de aprobación del crédito establecidas por LOANSI.</p>
</div>
""", unsafe_allow_html=True)
