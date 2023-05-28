from PIL import Image, ImageEnhance
import os
import shutil

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
        nuevo_ancho = 500
        nuevo_alto = 500
        
        # Ajustar las nuevas dimensiones para mantener la relación de aspecto
        relacion_aspecto = ancho / alto
        if relacion_aspecto > 1:
            nuevo_alto = int(nuevo_ancho / relacion_aspecto)
        else:
            nuevo_ancho = int(nuevo_alto * relacion_aspecto)
        
        # Redimensionar la imagen original a las nuevas dimensiones
        imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto), resample=Image.LANCZOS)
        
        # Aumentar el contraste de la imagen
        factor_contraste = 2  # Ajusta este valor para aumentar o disminuir el contraste
        realce_contraste = ImageEnhance.Contrast(imagen_redimensionada)
        imagen_contraste = realce_contraste.enhance(factor_contraste)
        
        nombre_procesado = archivos_procesados[-1]
        ruta_destino_archivo = os.path.join(ruta_destino, nombre_procesado)
        
        # Guardar la imagen redimensionada y con mayor contraste en formato JPEG
        imagen_contraste.save(ruta_destino_archivo, format='JPEG', quality=95)
        imagen_contraste.show()
        os.startfile(ruta_destino_archivo)
        
        # Imprime los tamaños originales y redimensionados
        print(f"Tamaño original: {ancho}x{alto}")
        print(f"Tamaño redimensionado: {nuevo_ancho}")
