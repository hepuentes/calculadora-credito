import streamlit as st

# Variables modificables
INTERES_BANCARIO_CORRIENTE = 18.6  # Puedes actualizar este valor cada mes
PUNTAJE_CLIENTE_NUEVO = 20  # Puntaje inicial bajo para clientes sin historial

# Diccionario de líneas de crédito y sus características
LINEAS_DE_CREDITO = {
    "LoansiMoto": {"descripcion": "Compra de moto nueva", "interes_mv": 1.7, "monto_max": 16100000},
    "LoansiFlex": {"descripcion": "Libre inversión", "interes_mv": 1.8, "monto_max": 20000000},
    "LoansiMicroFlex": {"descripcion": "Crédito para clientes informales", "interes_mv": 3.0, "monto_max": 300000}  # Línea para competir con gota a gota
}

# Título de la aplicación
st.title("Calculadora de Scoring y Tipo de Crédito - Loansi")

# Función para calcular el puntaje de crédito
def calcular_scoring(ingresos, frecuencia_ingresos, ocupacion, referencias, calidad_referencia, historial_pago, puntaje_datacredito, linea_credito):
    # Ajuste de ingresos según frecuencia
    if frecuencia_ingresos == "Semanal":
        ingresos_mensuales = ingresos * 4
    elif frecuencia_ingresos == "Quincenal":
        ingresos_mensuales = ingresos * 2
    else:  # Mensual
        ingresos_mensuales = ingresos

    # Puntaje por Ingresos y Estabilidad
    if ingresos_mensuales > 250000:
        puntaje_ingresos = 20
    elif 150000 <= ingresos_mensuales <= 250000:
        puntaje_ingresos = 15
    else:
        puntaje_ingresos = 10

    if ocupacion in ["Empleado", "Comerciante fijo", "Independiente", "Vendedor ambulante"]:
        puntaje_ocupacion = 20
    else:
        puntaje_ocupacion = 10

    # Puntaje total de ingresos y estabilidad
    puntaje_ingresos_total = puntaje_ingresos + puntaje_ocupacion

    # Puntaje por Referencias Personales
    if referencias == 2:
        puntaje_referencias = 10
    elif referencias == 1:
        puntaje_referencias = 5
    else:
        puntaje_referencias = 0

    if calidad_referencia in ["Familiar directo", "Amigo confiable"]:
        puntaje_calidad = 10
    else:
        puntaje_calidad = 5

    # Puntaje total de referencias
    puntaje_referencias_total = puntaje_referencias + puntaje_calidad

    # Puntaje por Historial de Pagos
    if historial_pago == "Buen historial completo":
        puntaje_historial = 40
    elif historial_pago == "Retrasos menores":
        puntaje_historial = 25
    elif historial_pago == "Historial único":
        puntaje_historial = 20
    else:
        puntaje_historial = PUNTAJE_CLIENTE_NUEVO  # Aplicar el puntaje definido para nuevos clientes sin historial

    # Puntaje por Datacrédito
    if puntaje_datacredito > 600:
        puntaje_datacredito_final = 30
    elif 500 <= puntaje_datacredito <= 600:
        puntaje_datacredito_final = 20
    elif 400 <= puntaje_datacredito < 500:
        puntaje_datacredito_final = 10
    else:
        puntaje_datacredito_final = 0  # Rechazo potencial

    # Puntaje total
    puntaje_total = puntaje_ingresos_total + puntaje_referencias_total + puntaje_historial + puntaje_datacredito_final

    # Calificación de Riesgo basada en el puntaje total ajustado
    if puntaje_total <= 45:
        calificacion_riesgo = "Alto Riesgo - Rechazo Potencial"
    elif 46 <= puntaje_total <= 70:
        calificacion_riesgo = "Riesgo Medio - Aprobación con Condiciones"
    else:
        calificacion_riesgo = "Bajo Riesgo - Aprobación Estándar"

    # Detalles de la línea de crédito seleccionada
    detalles_credito = LINEAS_DE_CREDITO.get(linea_credito, {})
    interes_mensual = detalles_credito.get("interes_mv", INTERES_BANCARIO_CORRIENTE)
    monto_maximo = detalles_credito.get("monto_max", 0)

    return puntaje_total, calificacion_riesgo, interes_mensual, monto_maximo

# Selección de línea de crédito
linea_credito = st.selectbox("Selecciona la Línea de Crédito", options=list(LINEAS_DE_CREDITO.keys()))

# Entrada de datos del usuario
ingresos = st.number_input("Ingresos (COP):", min_value=0, step=10000)
frecuencia_ingresos = st.selectbox("Frecuencia de Ingresos", ["Semanal", "Quincenal", "Mensual"])
ocupacion = st.selectbox("Ocupación", ["Empleado", "Comerciante fijo", "Independiente", "Vendedor ambulante", "Otro"])
referencias = st.selectbox("Número de referencias personales", [0, 1, 2])
calidad_referencia = st.selectbox("Calidad de la referencia", ["Familiar directo", "Amigo confiable", "Otro"])
historial_pago = st.selectbox("Historial de pagos con Loansi", ["Buen historial completo", "Retrasos menores", "Historial único", "Nuevo cliente"])
puntaje_datacredito = st.number_input("Puntaje en Datacrédito (Si no tiene historial, ingrese 400 o 500 según perfil):", min_value=0, step=50)

# Botón para calcular el puntaje
if st.button("Calcular Puntaje"):
    puntaje, riesgo, interes_mensual, monto_maximo = calcular_scoring(
        ingresos, frecuencia_ingresos, ocupacion, referencias, calidad_referencia, historial_pago, puntaje_datacredito, linea_credito
    )
    st.write("### Resultado de Scoring")
    st.write(f"**Puntaje Total**: {puntaje}")
    st.write(f"**Calificación de Riesgo**: {riesgo}")
    st.write(f"**Interés Mensual (M.V.) para {linea_credito}:** {interes_mensual}%")
    st.write(f"**Monto Máximo Disponible para {linea_credito}:** {monto_maximo} COP")
