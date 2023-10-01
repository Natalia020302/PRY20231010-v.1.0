from PIL import Image
import os

# Ruta de la carpeta con las imágenes originales
bucket_original = "bucket1"
# Ruta de la carpeta donde se guardarán las imágenes rotadas
bucket_destino = "bucket2"

# Crea la carpeta de destino si no existe
if not os.path.exists(bucket_destino):
    os.makedirs(bucket_destino)

# Lista los archivos en la carpeta original
archivos = os.listdir(bucket_original)

# Inicializa un contador
contador = 0

# Itera a través de los archivos
for archivo in archivos:
    if archivo.endswith(".jpg") or archivo.endswith(".png"):
        # Abre la imagen original
        imagen = Image.open(os.path.join(bucket_original, archivo))
        
        # Guarda la imagen original con "0_"
        imagen.save(os.path.join(bucket_destino, f"0_{archivo}"))
        
        # Rotación a 45 grados
        imagen_rotada_45 = imagen.rotate(45)
        imagen_rotada_45.save(os.path.join(bucket_destino, f"1_{archivo}"))
        
        # Rotación a 135 grados
        imagen_rotada_135 = imagen.rotate(135)
        imagen_rotada_135.save(os.path.join(bucket_destino, f"2_{archivo}"))
        
        # Incrementa el contador
        contador += 1

print("Proceso completado. Imágenes rotadas y guardadas en la carpeta de destino.")
