import csv
import os
#Esta es para que las características del .csv se agreguen a cada txt (es ahí donde está el valor de si es benigno o no)
# Rutas de los archivos

ruta_txt = "/Users/natty/Desktop/PRUEBASHORT/extra_200"
ruta_csv = "/Users/natty/Desktop/PRUEBASHORT/extra_200/excel2.csv"

# Leer el archivo CSV y crear un diccionario con los nombres y características
diccionario_caracteristicas = {}
with open(ruta_csv, 'r') as archivo_csv:
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
for archivo in os.listdir(ruta_txt):
    if archivo.endswith('.txt'):
        ruta_archivo = os.path.join(ruta_txt, archivo)
        nombre_archivo = os.path.splitext(archivo)[0]
        caracteristicas = diccionario_caracteristicas.get(nombre_archivo)

        if caracteristicas:
            # Agregar las características al archivo .txt
            with open(ruta_archivo, 'a') as archivo_txt:
                archivo_txt.write(f"Edad: {caracteristicas['Edad'].rstrip()}\n")
                archivo_txt.write(f"Melanoma: {caracteristicas['Melanoma'].rstrip()}\n")
