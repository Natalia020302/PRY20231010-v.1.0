import os
import shutil

#carpeta_a = "/Users/natty/Desktop/IMAGENES_ISIC/solo_img_melanoma"
#carpeta_b = "/Users/natty/Desktop/PRUEBASHORT/extraccion"
#carpeta_c = "/Users/natty/Desktop/PRUEBASHORT/ext_melanoma"

carpeta_a = "/Users/natty/Desktop/PRUEBASHORT/segmentadas"
carpeta_b = "/Users/natty/Desktop/PRUEBASHORT/carac_test"
carpeta_c = "/Users/natty/Desktop/PRUEBASHORT/seg_tes"

# Obtener la lista de nombres de archivos en la carpeta B sin extensión
archivos_b = [os.path.splitext(nombre)[0] for nombre in os.listdir(carpeta_b)]

# Iterar sobre los archivos de la carpeta A
for archivo_a in os.listdir(carpeta_a):
    nombre_a, _ = os.path.splitext(archivo_a)
    if nombre_a in archivos_b:
        ruta_archivo_a = os.path.join(carpeta_a, archivo_a)
        ruta_destino = os.path.join(carpeta_c, archivo_a)
        shutil.move(ruta_archivo_a, ruta_destino)
        print(f"Archivo {archivo_a} movido a la carpeta C.")