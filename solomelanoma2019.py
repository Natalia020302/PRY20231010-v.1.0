import os
import pandas as pd
import shutil

# Ruta del archivo de Excel
excel_file = "/Users/natty/Desktop/IMAGENES_ISIC_2019/ISIC_2019_Training_Metadata_complete.xlsx"

# Ruta de la carpeta con las imágenes
carpeta_imagenes = "/Users/natty/Desktop/IMAGENES_ISIC_2019/ISIC_2019_Training_Input"

# Ruta de la carpeta de destino para las imágenes filtradas
carpeta_destino = "/Users/natty/Desktop/IMAGENES_ISIC_2019/solo_melanoma"

# Lee el archivo de Excel usando pandas
dataframe = pd.read_excel(excel_file)

# Filtra las filas del DataFrame donde Melanoma sea "malignant"
imagenes_malignas = dataframe[dataframe["Melanoma"] == "malignant"]["nombre"]

# Crea la carpeta de destino si no existe
if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

# Itera sobre los nombres de las imágenes y las transporta a la carpeta de destino
for imagen_base in imagenes_malignas:
    # Busca la imagen con la extensión .jpg en la carpeta y la transporta a la carpeta de destino
    for filename in os.listdir(carpeta_imagenes):
        if filename.startswith(imagen_base) and filename.lower().endswith(".jpg"):
            ruta_imagen = os.path.join(carpeta_imagenes, filename)
            ruta_destino = os.path.join(carpeta_destino, filename)
            shutil.move(ruta_imagen, ruta_destino)

print("Imágenes transportadas exitosamente.")