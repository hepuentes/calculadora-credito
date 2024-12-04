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

# Título principal
st.title("Simulador de Crédito Loansi")

# Selección de línea de crédito
st.header("Selecciona la Línea de Crédito")
tipo_credito = st.selectbox("", options=list(LINEAS_DE_CREDITO.keys()), index=0)
detalles = LINEAS_DE_CREDITO[tipo_credito]

st.markdown(f"**Descripción:** {detalles['descripcion']}")

# Entrada del monto con símbolo de peso
st.header("Escribe el valor del crédito")
st.markdown(f"Ingrese un monto entre $ {format_number(detalles['monto_min'])} y $ {format_number(detalles['monto_max'])} COP:")

monto = st.number_input(
    "Monto del crédito",
    min_value=detalles["monto_min"],
    max_value=detalles["monto_max"],
    step=1000,
    value=detalles["monto_min"],
)

# Slider de plazo
if tipo_credito == "LoansiFlex":
    st.header("Plazo en Meses")
    plazo = st.slider("Seleccione el plazo (en meses):", 
                     min_value=detalles["plazo_min"], 
                     max_value=detalles["plazo_max"], 
                     step=12,
                     value=detalles["plazo_min"])
    frecuencia_pago = "Mensual"
else:
    st.header("Plazo en Semanas")
    plazo = st.slider("Seleccione el plazo (en semanas):", 
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
### Resultado:
Pagarás {plazo} cuotas de aproximadamente:
- **Monto por cuota:** $ {format_number(cuota)} {frecuencia_pago}
""")

# Detalles del crédito
st.subheader("Detalles del Crédito")
st.write(f"**Monto solicitado:** $ {format_number(monto)} COP")
st.write(f"**Plazo:** {plazo} {'meses' if tipo_credito == 'LoansiFlex' else 'semanas'}")
st.write(f"**Frecuencia de Pago:** {frecuencia_pago}")
st.write(f"**Tasa Efectiva Anual (E.A.):** {detalles['tasa_anual_efectiva']:.2f}%")
st.write(f"**Valor total a financiar:** $ {format_number(total_financiar)} COP")

# Disclaimer
st.info("Estos valores son aproximados y pueden variar según las políticas de Loansi.")

