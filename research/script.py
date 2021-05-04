"""


"""

import joblib

def predecir(texto):
  """
  Esta función carga el modelo entrenado y el vector, el modelo tiene una exactitud del 79%
  Recibe un String
  Retorna 0 si el texto lo clasifica como no ofensivo y 1 si lo clasifica como ofensivo
  """
  modelo = joblib.load('modeloEntrenado.pkl')
  vector = joblib.load('vector.pkl')

  matriz = vector.transform([texto])
  return modelo.predict(matriz)  


#Ejemplo de prediccion
mensaje = "Hola, buen dia"
prediccion = predecir(mensaje)
print("Mensaje: ", mensaje)

if prediccion == 0:
  print("El mensaje fue clasificado como: no ofensivo")
else:
  print("El mensaje fue clasificado como: ofensivo")


