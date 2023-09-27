import streamlit as st
from PIL import Image


st.title("Cálculo financiero")
st.subheader("¡Bienvenido!")
st.write("Uno de los aspectos más importantes y en el que se percibe desconocimiento en las personas, es el relacionado con la parte financiera.Esta situación se puede estar presentando debido  a que en las escuelas se aborda de una manera superficial este tema lo que lleva a que no se tenga claridad de algunos aspectos y variables que la entidades financieras valoran al momento de estudiar  o analizar una solicitud de crédito, lo que lleva a que en algunas oportunidades sean rechazada.  Por tal motivo, con esta herramienta se pretende que el usuario pueda evaluar las características de las  solicitudes de crédito y que se solicitan afectan positiva o negativamente el puntaje para tener en cuenta en  la solicitud que se está o se quiere realizar.")
st.subheader("¿Cómo funciona?")
st.write("Después de esta explicación encontrarás una serie de criterios, los cuales te pediremos que analices y los ajustes de acuerdo a tus valores. Estos filtros son:")
mark = """
* Tipo de propiedad de la vivienda. 
* El propósito de tu crédito que puede ser desde educación hasta remodalaciones para el hogar. 
* Si ha tenido algún incumplimiento histórico en sus pagos.
* El montó del crédito que desea solicitar.
"""
st.markdown(mark)
st.write("Luego de ajustar los filtros a tus parámetros, oprimes el botón 'Calcula tu puntaje crediticio' y automáticamente te aparecerá tu puntaje de puntaje crediticio, se te comenta qué tan probable es que tu crédito sea aprobado y una serie de imágenes en donde te ilustramos cómo está tu puntaje con respecto al resto de la población.")
# Tipo de propiedad de la vivienda
tipoPropiedad = ('Alquiler', 'Propietario', 'Hipoteca', 'Otro')
tipoPropiedadOptions = st.selectbox(
    "Elige el tipo de propiedad de la vivienda", tipoPropiedad)
# Propositos
purposes = ('Personal', 'Educación', 'Medicina', 'Empresa', 'Mejora de hogar','Consolidación de deuda')
purposeOption = st.selectbox("Elige tu propósito del crédito", purposes)
# Incumplimiento historico
historicalDefault = ("Si", "No")
historicalDefaultOption = st.selectbox(
    "¿Ha tenido incumplimiento histórico?", historicalDefault)
# Loan amount: Monto del crédito
amountRateSlider = st.slider(
    "¿De cuánto es el monto el préstamo?", min_value=500, max_value=35000, step=500)
# Variables para ir calculando el scorecard
intercepto = 586.7390265
# Tipo de propiedad de la vivienda
tipoPropiedadCoeficients = [98.48833297,
                           -97.61532867,
                           -51.12233204,
                           50.90444366]
tipoPropiedadScore = {tipoPropiedad[i]: tipoPropiedadCoeficients[i]
                 for i in range(len(tipoPropiedad))}
# Para la suma del scorecard
tipoPropiedadScoreSumar = tipoPropiedadScore[tipoPropiedadOptions]
# Proposito
purposeCoeficients = [-13.26120991,
                      -36.46796862,
                      28.72147217,
                      -54.34337143,
                      37.50081583,
                      38.50537786]
purposeScore = {purposes[i]: purposeCoeficients[i]
                for i in range(len(purposeCoeficients))}
# Para la suma del scorecard
purposeScoreSumar = purposeScore[purposeOption]
# Incumplimiento historico
historicalDefaultCoeficient = [56.27710989, -55.62199397]
historicalDefaultScore = {historicalDefault[i]: historicalDefaultCoeficient[i]
             for i in range(len(historicalDefaultCoeficient))}
# Para la suma del scorecard
historicalDefaultScoreSumar = historicalDefaultScore[historicalDefaultOption]
# Monto del crédito
amountDiccionario = {'465.5, 3950.0': -54.22147633,
                  '3950.0, 7400.0': -79.15833246,
                  '7400.0, 10850.0': -60.54640156,
                  '14300.0, 17750.0': -0.3632122271,
                  '10850.0, 14300.0': -44.58188284,
                  '24650.0, 28100.0': 69.99015274,
                  '17750.0, 21200.0': 11.80417282,
                  '31550.0, 35000.0': 62.79296439,
                  '28100.0, 31550.0': 41.6612782,
                  '21200.0, 24650.0': 53.27785318}
# Se itera para saber en qué limite está
for intervalo in amountDiccionario:
    limites = list(map(float, intervalo.split(',')))
    if amountRateSlider > limites[0] and amountRateSlider <= limites[1]:
        amountRateScoreSumar = amountDiccionario[intervalo]
        break
scoreCard = round(intercepto+tipoPropiedadScoreSumar+purposeScoreSumar+historicalDefaultScoreSumar+amountRateScoreSumar)
# Por si llega a ser mayor (aunque es imposible, pero por si llega a suceder)
if scoreCard > 850:
    scoreCard = 850
elif scoreCard < 300:
    scoreCard = 300
# Encima de x porcentaje
posiciones = [538.0, 559.0, 578.0, 597.0,
              614.0, 628.0, 644.0, 667.0, 711.0]


def retornarPorcentaje():
    for i in range(8, -1, -1):
        if scoreCard > posiciones[i]:
            return (i*10)+10
    return 0

# Se importan la imagen, numero es el numero para diferenciar la imagen
def buscarImagen(numero):
    path = 'Sinfondos/'+str(numero)+'.png'
    image = Image.open(path)
    return image


if st.button("Calcula tu puntaje crediticio"):
    st.write("Tu puntaje crediticio es de:", scoreCard)
    if scoreCard >= 584:
        st.write("Tu solicitud de crédito probablemente será aprobada.")
    else:
        st.write("Lastimosamente es improbable de que tu crédito sea aprobado.")
    
    porcentaje = retornarPorcentaje()
    st.write("Tu puntaje crediticio está encima del",
             porcentaje, "% de los puntajes crediticios de la población.")
    if porcentaje >= 10:
        imagen = buscarImagen(porcentaje)
        st.image(imagen, caption='Ilustración de comparativa del usuario con el resto de la población')
