import os
import numpy as np
import boto3
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import json
import pandas as pd
from sklearn.svm import SVC


# Conexión a S3
s3 = boto3.client('s3')

# Nombres de los buckets
bucket_entrenamiento = 'bucket-de-entrenamiento'
bucket_pruebas = 'bucket-de-prueba'

# Lista para almacenar las características y las etiquetas
caracteristicas = []
etiquetas = []

# Función para procesar archivos de características
def procesar_archivos(bucket, caracteristicas, etiquetas):
    paginator = s3.get_paginator('list_objects_v2')
    operation_parameters = {'Bucket': bucket}

    for page in paginator.paginate(**operation_parameters):
        input_objects = page.get('Contents', [])
        
        for obj in input_objects:
            archivo = obj['Key']
            if archivo.endswith(".txt"):
                response = s3.get_object(Bucket=bucket, Key=archivo)
                contenido_txt = response['Body'].read().decode('utf-8')
                lineas = contenido_txt.split('\n')

                # Obtener los valores de las características y la etiqueta
                asimetria = float(lineas[0].split(':')[1].strip())
                color = float(lineas[1].split(':')[1].strip())
                diametro = float(lineas[2].split(':')[1].strip())
                bordes = float(lineas[3].split(':')[1].strip())
                edad_linea = lineas[4].split(':')[1].strip()
                melanoma = lineas[5].split(':')[1].strip()

                # Verificar si la línea de edad está vacía
                if edad_linea:
                    edad = int(edad_linea)
                else:
                    edad = 49  # Valor temporal para edad en caso de que esté vacía

                # Guardar las características y la etiqueta
                caracteristicas.append([asimetria, color, diametro, bordes, edad])
                etiquetas.append(melanoma)

# Procesar archivos de características para entrenamiento
procesar_archivos(bucket_entrenamiento, caracteristicas, etiquetas)

# Procesar archivos de características para pruebas
procesar_archivos(bucket_pruebas, caracteristicas, etiquetas)

# Convertir las listas en arrays de NumPy
caracteristicas = np.array(caracteristicas)
etiquetas = np.array(etiquetas)

# Codificar las etiquetas (benigno: 0, maligno: 1)
etiquetas_encoded = np.where(etiquetas == "malignant", 1, 0)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(caracteristicas, etiquetas_encoded, test_size=0.2, random_state=42)

# Crear el clasificador SVM RBF
clf = svm.SVC(kernel='rbf', C=5.0, gamma=0.01, probability=True)

# Entrenar el modelo
clf.fit(X_train, y_train)

# Guardar el modelo en un archivo .pkl
modelo_entrenado = 'modelo_entrenado.pkl'
joblib.dump(clf, modelo_entrenado)

# Realizar predicciones en el conjunto de prueba
y_pred = clf.predict(X_test)

# Generar reportes de clasificación
reporte_completo = classification_report(y_test, y_pred, output_dict=True)
reporte_maligno = classification_report(y_test, y_pred, labels=[1], target_names=['malignant'], output_dict=True)


# Calcular la matriz de confusión
from sklearn.metrics import confusion_matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Extraer los valores de VP, VN, FP y FN
VP = conf_matrix[1, 1]
VN = conf_matrix[0, 0]
FP = conf_matrix[0, 1]
FN = conf_matrix[1, 0]


# Imprimir los valores de VP, VN, FP y FN
print(f'Verdaderos Positivos (VP): {VP}')
print(f'Verdaderos Negativos (VN): {VN}')
print(f'Falsos Positivos (FP): {FP}')
print(f'Falsos Negativos (FN): {FN}')

# Guardar los valores de VP, VN, FP y FN en un archivo de texto
with open('matrizconfusion.txt', 'w') as archivo:
    archivo.write(f'Verdaderos Positivos (VP): {VP}\n')
    archivo.write(f'Verdaderos Negativos (VN): {VN}\n')
    archivo.write(f'Falsos Positivos (FP): {FP}\n')
    archivo.write(f'Falsos Negativos (FN): {FN}\n')


print(reporte_completo)

print(f"-------------------------------------------------------")

print(reporte_maligno)


with open('reporte_completo.json', 'w') as json_file:
    json.dump(reporte_completo, json_file)
    
with open('reporte_maligno.json', 'w') as json_file:
    json.dump(reporte_maligno, json_file)



    
with open('reporte_maligno.txt', 'w') as txt_file:
    txt_file.write(json.dumps(reporte_maligno, indent=4))
    
with open('reporte_completo.txt', 'w') as txt_file:
    txt_file.write(json.dumps(reporte_completo, indent=4))
    