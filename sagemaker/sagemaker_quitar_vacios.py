import boto3
import cv2
import numpy as np

def is_image_mostly_dark(image, threshold=0.98):
    # Verificar si la mayoría de los píxeles en la imagen son oscuros
    imagen_gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    total_pixels = imagen_gris.size
    dark_pixels = np.count_nonzero(imagen_gris < 10)  # Ajusta el umbral según tus necesidades
    
    return (dark_pixels / total_pixels) >= threshold

def move_dark_images(bucket_origen, bucket_destino):
    s3_client = boto3.client('s3')
    
    paginator = s3_client.get_paginator('list_objects_v2')
    operation_parameters = {'Bucket': bucket_origen}
    
    moved_count = 0  # Contador de imágenes trasladadas
    
    for page in paginator.paginate(**operation_parameters):
        input_objects = page.get('Contents', [])
        
        for obj in input_objects:
            archivo = obj['Key']
            
            response = s3_client.get_object(Bucket=bucket_origen, Key=archivo)
            imagen_bytes = response['Body'].read()
            imagen = cv2.imdecode(np.frombuffer(imagen_bytes, np.uint8), cv2.IMREAD_COLOR)

            if imagen is not None and is_image_mostly_dark(imagen, threshold=0.98):
                # Trasladar la imagen al bucket de destino
                s3_client.copy_object(
                    Bucket=bucket_destino,
                    CopySource={'Bucket': bucket_origen, 'Key': archivo},
                    Key=archivo
                )
                s3_client.delete_object(Bucket=bucket_origen, Key=archivo)  # Eliminar la imagen del bucket de origen
                moved_count += 1
                print(f"Traslada la imagen: {archivo}")
    
    print(f"Traslado completo. Se trasladaron {moved_count} imágenes.")

# Cambiar estos valores con los nombres reales de tus buckets en S3
bucket_origen = '2-5-training-segmentacion'
bucket_destino = 'inner-train-5-extraccion2'

# Llamar a la función para trasladar las imágenes mayormente negras
move_dark_images(bucket_origen, bucket_destino)
