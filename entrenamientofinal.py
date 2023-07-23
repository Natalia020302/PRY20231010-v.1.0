import os
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Directorio de las imágenes
directorio_imagenes = "/Users/natty/Desktop/PRUEBASHORT/combinado_segmentadas"

# Rutas de los archivos de características para entrenamiento y pruebas
ruta_entrenamiento = "/Users/natty/Desktop/PRUEBASHORT/combinado_carac_entre"
ruta_pruebas = "/Users/natty/Desktop/PRUEBASHORT/combinado_carac_test"

# Lista para almacenar las características y las etiquetas
caracteristicas = []
etiquetas = []

# Recorrer los archivos de características para entrenamiento
for archivo in os.listdir(ruta_entrenamiento):
    if archivo.endswith(".txt"):
        # Leer el archivo de características
        ruta_archivo = os.path.join(ruta_entrenamiento, archivo)
        with open(ruta_archivo, "r") as f:
            lineas = f.readlines()

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

# Recorrer los archivos de características para pruebas
for archivo in os.listdir(ruta_pruebas):
    if archivo.endswith(".txt"):
        # Leer el archivo de características
        ruta_archivo = os.path.join(ruta_pruebas, archivo)
        with open(ruta_archivo, "r") as f:
            lineas = f.readlines()

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
reporte = classification_report(y_test, y_pred, labels=[1], target_names=['maligno'])
reporte_lines = reporte.split('\n')
precision = float(reporte_lines[2].split()[3])
recall = float(reporte_lines[2].split()[4])
f1_score = float(reporte_lines[2].split()[5])
accuracy = float(reporte_lines[5].split()[1])

print(f"Precisión de maligno (1): {precision}")
print(f"Recall de maligno (1): {recall}")
print(f"F1-score de maligno (1): {f1_score}")
print(f"Accuracy del modelo: {accuracy}")
