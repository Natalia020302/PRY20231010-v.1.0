import csv
import os

#es para que elimines las filas del excel de las imagenes que no están en tu carpetas
# es más para que veas que imagenes tienes y si son benigno o no

# Rutas de los archivos
ruta_txt = r'C:\Users\FLAVIA\Downloads\codigomodel\extraccion\destinocaract'
ruta_csv = r'C:\Users\FLAVIA\Downloads\codigomodel\extraccion\destinocaract\excel.csv'

# Obtener la lista de nombres de archivo de la carpeta de .txt
nombres_archivo_txt = []
for archivo in os.listdir(ruta_txt):
    if archivo.endswith('.txt'):
        nombre_archivo = os.path.splitext(archivo)[0]
        nombres_archivo_txt.append(nombre_archivo)

# Crear una copia del archivo CSV eliminando las filas correspondientes a nombres de archivo no encontrados en la carpeta de .txt
ruta_csv_temporal = r'C:\Users\FLAVIA\Downloads\codigomodel\extraccion\destinocaract\excel_temporal.csv'
with open(ruta_csv, 'r') as archivo_csv, open(ruta_csv_temporal, 'w', newline='') as archivo_temporal:
    lector_csv = csv.reader(archivo_csv)
    escritor_csv = csv.writer(archivo_temporal)

    # Escribir las filas del archivo CSV que corresponden a los nombres de archivo presentes en la carpeta de .txt
    for fila in lector_csv:
        if len(fila) > 0:
            nombre = fila[0]
            if nombre in nombres_archivo_txt:
                escritor_csv.writerow(fila)

# Reemplazar el archivo original con la copia actualizada
os.remove(ruta_csv)
os.rename(ruta_csv_temporal, ruta_csv)
