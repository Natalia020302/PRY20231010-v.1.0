import os
import boto3
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO

# Configuración de S3
s3 = boto3.client('s3')
bucket_origen = '2-2-training-dataaugmentation'  # Reemplaza con el nombre de tu bucket de origen
bucket_destino = '2-3-training-nitidez'  # Reemplaza con el nombre de tu bucket de destino

# Función para procesar una imagen
def process_image(image_data):
    imagen = Image.open(BytesIO(image_data))
    
    ancho, alto = imagen.size

    if extension in ['.jpg', '.jpeg', '.png', '.gif']:
        # Definir las dimensiones límite
        alto_minimo = 1100
        alto_maximo = 1500

        # Calcular nuevo alto manteniendo la relación de aspecto
        nuevo_alto = min(max(alto, alto_minimo), alto_maximo)
        nuevo_ancho = int(ancho * nuevo_alto / alto)

        # Redimensionar la imagen original a las nuevas dimensiones
        imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto), resample=Image.LANCZOS)

        # Aplicar filtro de enfoque a los bordes
        imagen_enfocada = imagen_redimensionada.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

        # Aumentar el contraste de la imagen
        factor_contraste = 1.2  # Ajusta este valor para aumentar o disminuir el contraste
        realce_contraste = ImageEnhance.Contrast(imagen_enfocada)
        imagen_contraste = realce_contraste.enhance(factor_contraste)

        # Ajustar el brillo de la imagen
        factor_brillo = 0.7  # Ajusta este valor para hacer la imagen más oscura (0.0 - 1.0)
        realce_brillo = ImageEnhance.Brightness(imagen_contraste)
        imagen_oscurecida = realce_brillo.enhance(factor_brillo)

        # Aumentar la nitidez de la imagen
        factor_nitidez = 1  # Ajusta este valor para aumentar o disminuir la nitidez
        realce_nitidez = ImageEnhance.Sharpness(imagen_contraste)
        imagen_nitidez = realce_nitidez.enhance(factor_nitidez)

    return imagen_nitidez

# Obtener una lista de los objetos que ya han sido procesados en el bucket de destino
response = s3.list_objects_v2(Bucket=bucket_destino)
archivos_procesados = [obj['Key'] for obj in response.get('Contents', [])]

# Obtener el último número de imagen procesada
ultimo_numero = len(archivos_procesados)

paginator = s3.get_paginator('list_objects_v2')
operation_parameters = {'Bucket': bucket_origen}

for page in paginator.paginate(**operation_parameters):
    nuevos_archivos = [obj['Key'] for obj in page.get('Contents', []) if obj['Key'] != '.DS_Store']
    
    for objeto_key in nuevos_archivos:
        if objeto_key not in archivos_procesados:
            nombre_archivo = os.path.basename(objeto_key)
            nombre_sin_extension, extension = os.path.splitext(nombre_archivo)
    
            # Incrementar el contador de imágenes procesadas
            ultimo_numero += 1
    
            # Nombre de la imagen procesada (mismo nombre que el original)
            nombre_procesado = nombre_sin_extension
    
            # Descargar la imagen desde el bucket de origen
            objeto = s3.get_object(Bucket=bucket_origen, Key=objeto_key)
            imagen_data = objeto['Body'].read()
            
            # Procesar la imagen
            imagen_procesada = process_image(imagen_data)
            
            # Guardar la imagen procesada en el bucket de destino
            buffer = BytesIO()
            imagen_procesada.save(buffer, format='JPEG', quality=95)
            buffer.seek(0)
            ruta_destino_procesado = f"{nombre_procesado}{extension}"
            s3.upload_fileobj(buffer, bucket_destino, ruta_destino_procesado)
            
            print(f"Processed: {nombre_procesado}")
    
print("Reajuste nitidez completado.")