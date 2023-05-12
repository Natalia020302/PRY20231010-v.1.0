from PIL import Image
import os
import shutil
# Ruta de la imagen que deseas cargar
#ruta_imagen = "C:/Users/FLAVIA/Downloads/Python/prueba2.jpg"

# Abrir la imagen
#imagen = Image.open(ruta_imagen)
#imagen.show()
# Mostrar información de la imagen
#print("Formato de la imagen:", imagen.format)
#print("Dimensiones de la imagen:", imagen.size)
#print("Modo de la imagen:", imagen.mode)

ruta_carpeta = 'C:/Users/FLAVIA/Downloads/Python/misimagenes'
ruta_destino = 'C:/Users/FLAVIA/Downloads/redimensionado'

# Obtener una lista de los archivos que ya han sido procesados
archivos_procesados = [nombre_archivo for nombre_archivo in os.listdir(ruta_destino) if nombre_archivo.startswith('imagenprocesada')]

# Obtener una lista de las nuevas imágenes que no han sido procesadas
nuevos_archivos = [nombre_archivo for nombre_archivo in os.listdir(ruta_carpeta) if not nombre_archivo.startswith('imagenoriginal')]

for nombre_archivo in nuevos_archivos:
    ruta_original = os.path.join(ruta_carpeta, nombre_archivo)
    _, extension = os.path.splitext(nombre_archivo)
    
    # Renombrar la nueva imagen como "imagenoriginal{numero}.extension"
    nuevo_nombre = f"imagenoriginal{len(archivos_procesados) + 1}{extension}"
    os.rename(ruta_original, os.path.join(ruta_carpeta, nuevo_nombre))
    ruta_original = os.path.join(ruta_carpeta, nuevo_nombre)
    
    # Agregar el nuevo archivo a la lista de archivos procesados
    archivos_procesados.append(f"imagenprocesada{len(archivos_procesados) + 1}{extension}")
    
    # Procesar la imagen
    imagen = Image.open(ruta_original)
    ancho, alto = imagen.size
    
    if extension in ['.jpg', '.jpeg', '.png', '.gif']:
        if ancho < 1000 and alto < 1000:
            nuevo_ancho = ancho * 2
            nuevo_alto = alto * 2
            nombre_procesado = archivos_procesados[-1]
            ruta_destino_archivo = os.path.join(ruta_destino, nombre_procesado)
            
            imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto), resample=Image.LANCZOS)
            imagen_redimensionada.save(ruta_destino_archivo)
            imagen_redimensionada.show()
            os.startfile(ruta_destino_archivo)

            # Imprime los tamaños originales y redimensionados
            print(f"Tamaño original: {ancho}x{alto}")
            print(f"Tamaño redimensionado: {nuevo_ancho}x{nuevo_alto}")
        else:
            nombre_procesado = archivos_procesados[-1]
            ruta_destino_archivo = os.path.join(ruta_destino, nombre_procesado)
            
            shutil.copyfile(ruta_original, ruta_destino_archivo)
            imagen.show()
            os.startfile(ruta_original)
            print(f"Tamaño de la imagen: {ancho}x{alto}")
    else:
        print(f"{nombre_archivo} no es una imagen")