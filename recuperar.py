import os
import shutil

carpeta_a = "/Users/natty/Desktop/PRUEBASHORT/2000_originales"
carpeta_b = "/Users/natty/Desktop/PRUEBASHORT/segmentadas/melanoma_seg"
carpeta_c = "/Users/natty/Desktop/IMAGENES_ISIC/solo_img_melanoma"

# Obtener la lista de nombres de archivos en la carpeta B
archivos_b = [os.path.splitext(archivo)[0] for archivo in os.listdir(carpeta_b)]

# Recorrer la carpeta A
for archivo in os.listdir(carpeta_a):
    nombre_archivo, extension = os.path.splitext(archivo)
    ruta_archivo = os.path.join(carpeta_a, archivo)
    # Verificar si el nombre del archivo (sin extensión) existe en la carpeta B
    if nombre_archivo in archivos_b:
        # Copiar el archivo a la carpeta C
        ruta_destino = os.path.join(carpeta_c, archivo)
        shutil.copyfile(ruta_archivo, ruta_destino)
        print(f"Archivo {archivo} copiado a la carpeta C.")

print("Proceso finalizado.")
