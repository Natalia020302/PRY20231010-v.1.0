import csv
import os

bucket_txt = "/Users/natty/Desktop/car"
bucket_csv = "/Users/natty/Desktop/7_entrenamiento/excel.csv"

# Leer el archivo CSV y crear un diccionario con los nombres y características
diccionario_caracteristicas = {}
with open(bucket_csv, 'r') as archivo_csv:
    lector_csv = csv.reader(archivo_csv)
    for fila in lector_csv:
        if len(fila) >= 4:
            nombre = fila[0]
            sexo = fila[1]
            edad = fila[2]
            melanoma = fila[3]
            diccionario_caracteristicas[nombre] = {
                'Edad': edad,
                'Melanoma': melanoma
            }

# Recorrer los archivos .txt y agregar las características correspondientes
for archivo in os.listdir(bucket_txt):
    if archivo.endswith('.txt'):
        ruta_archivo = os.path.join(bucket_txt, archivo)
        nombre_archivo = os.path.splitext(archivo)[0][2:]  # Ignorar los primeros 2 caracteres
        caracteristicas = diccionario_caracteristicas.get(nombre_archivo)

        if caracteristicas:
            # Agregar las características al archivo .txt
            with open(ruta_archivo, 'a') as archivo_txt:
                archivo_txt.write(f"Edad: {caracteristicas['Edad'].rstrip()}\n")
                archivo_txt.write(f"Melanoma: {caracteristicas['Melanoma'].rstrip()}\n")
