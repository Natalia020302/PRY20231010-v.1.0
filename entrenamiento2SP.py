import os
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Directorio de las imágenes
directorio_imagenes = "C:/Users/FLAVIA/Downloads/codigomodel/segmentacion/destinosegm"

# Directorio de los archivos de características
directorio_caracteristicas = "C:/Users/FLAVIA/Downloads/codigomodel/extraccion/destinocaract"

# Lista para almacenar las características y las etiquetas
caracteristicas = []
etiquetas = []

# Recorrer los archivos de características
for archivo in os.listdir(directorio_caracteristicas):
    if archivo.endswith(".txt"):
        # Leer el archivo de características
        ruta_archivo = os.path.join(directorio_caracteristicas, archivo)
        with open(ruta_archivo, "r") as f:
            lineas = f.readlines()
        
        # Obtener los valores de las características y la etiqueta
        asimetria = float(lineas[0].split(':')[1].strip())
        color = float(lineas[1].split(':')[1].strip())
        diametro = float(lineas[2].split(':')[1].strip())
        bordes = float(lineas[3].split(':')[1].strip())
        #edad = int(lineas[4].split(':')[1].strip())
        melanoma = lineas[4].split(':')[1].strip()
        
        # Guardar las características y la etiqueta
        caracteristicas.append([asimetria, color, diametro, bordes])
        etiquetas.append(melanoma)

# Convertir las listas en arrays de NumPy
caracteristicas = np.array(caracteristicas)
etiquetas = np.array(etiquetas)

# Codificar las etiquetas (benigno: 0, maligno: 1)
etiquetas_encoded = np.where(etiquetas == "malignant", 1, 0)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(caracteristicas, etiquetas_encoded, test_size=0.2, random_state=42)

# Crear el clasificador SVM
clf = svm.SVC(kernel='linear')

# Entrenar el modelo
clf.fit(X_train, y_train)

# Realizar predicciones en el conjunto de prueba
y_pred = clf.predict(X_test)

# Generar reporte de clasificación
reporte = classification_report(y_test, y_pred)
print(reporte)
