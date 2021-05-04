"""
Script utilizado para crear el modelo
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import metrics
import joblib

# Clase Clasificador
class Clasificador(object):
    #Abrimos el archivo de entrenamiento. La ruta se debe de cambiar por la ruta en donde se tengan los datos
    corpus = open("train_aggressiveness.csv", encoding="ISO-8859-1")
    corpusAgresivo = pd.read_csv(corpus, encoding="ISO-8859-1")
    #Se obtiene las etiquetas de clasificación (1 agresivo y 0 no agresivo)
    corpusEtiquetas = corpusAgresivo.Category
    #print(corpusEtiquetas)
    #Se obtiene los comentarios agresivos 
    corpusComentarios = corpusAgresivo.Text
    #print(corpusComentarios)
    #Mostramos los tipo de etiquetas
    tiposEtiquetas = set(corpusEtiquetas)
    #Creamos un objeto de tipo TfidVectoricer 
    vector = TfidfVectorizer(min_df=2)

    #Particionamos los datos del archivo de entrenamiento para poder obtener datos de entrenamiento y de prueba
    #Para hacer la partición se utiliza train_test_split(datos, etiquetas y estado ramdon)
    def particionarDatos(self):
        #Este método particiona los datos y retorna una lista con los datos particionados resultantes
        xEntrenamiento, xPrueba, yEntrenamiento, yPrueba = train_test_split(self.corpusComentarios, self.corpusEtiquetas)
        datos = [xEntrenamiento, xPrueba, yEntrenamiento, yPrueba]
        return datos
    
    #Con los datos particionados en entrenamiento y prueba se realiza un matriz de entrenamiento y una matriz de prueba 
    #utilizando TfidVectorizer. fit_transfrom para los datos de entrenamiento y transform para los datos de prueba.
    def creaMatrizEntrenamiento(self, dato): 
        #Este método crea una matriz de entrenamiento
        matrizEntrenamiento = self.vector.fit_transform(dato) #Se realiza la tokenización o bolsa de palabras
        return matrizEntrenamiento
    
    def creaMatrizPrueba(self, dato):
        #Este métodod crea una matriz de prueba 
        matrizPrueba = self.vector.transform(dato)  
        return matrizPrueba
    
    #Cuando la bolsa de palabras o la tokenización este lista se prodece a entrenar el modelo de predicción
    #El algortimo o modelo de clasificacion es Naibe Bayes
    def entrenarModelo(self, matrizE, datos):
        #Este método crea un objeto de MultinomialNB() el cual es entrenado y posteriormente retornado 
        nb = MultinomialNB()
        #Se entrena al algortimo con (matrix de entrenamiento, target)
        
        nb.fit(matrizE, datos[2])
        return nb
    
    def predecir(self,nb,matriz):
        yprediccion = nb.predict(matriz)
        return yprediccion

    def metricaConfusion(self, datos, yprediccion):
        return metrics.confusion_matrix(datos[3], yprediccion)


c2 = Clasificador() #Creamos una instancia de Clasificador()
datos = c2.particionarDatos()#Se particionan los datos


corpus = open("train_aggressiveness.csv", encoding="ISO-8859-1")
corpusAgresivo = pd.read_csv(corpus, encoding="ISO-8859-1") 
matrizEntrenamiento = c2.creaMatrizEntrenamiento(datos[0]) #Esta matriz es para el model0
atributosE = c2.vector.get_feature_names() #Obtenemos los atributos de la matriz
#pd.DataFrame(matrizEntrenamiento.toarray(), columns=atributosE).head(10)
matrizPrueba = c2.creaMatrizPrueba(datos[1]) #Esta matriz es para el modelo
atributosP = c2.vector.get_feature_names() #Obtenemos los atributos de la matriz
#pd.DataFrame(matrizPrueba.toarray(), columns= atributosP).head(10)

nb = c2.entrenarModelo(matrizEntrenamiento, datos)

"""
#Se guarda el modelo y el vector
import joblib
joblib.dump(nb,"modeloEntrenado.pkl")
joblib.dump(c2.vector, 'vector.pkl')

#Abrimos el modelo para testearlo
modelo = joblib.load('modeloEntrenado.pkl')


#testeamos
y_pred = modelo.predict(matrizPrueba)
from sklearn import metrics
exactitud = metrics.accuracy_score(datos[3],y_pred)
precision = metrics.precision_score(datos[3],y_pred,average='macro')
recall = metrics.recall_score(datos[3],y_pred,average='macro')
fScore = metrics.f1_score(datos[3],y_pred,average='macro')

print("EXACTITUD: ", exactitud)
print("PRECISION: ", precision)
print("RECALL: ", recall)
print("F-SCORE: ", fScore)
"""

