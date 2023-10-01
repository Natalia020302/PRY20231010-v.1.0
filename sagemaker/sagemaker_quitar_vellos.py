import os
import cv2
import boto3
import numpy as np
from io import BytesIO

# Specify S3 bucket names
input_bucket = '2-3-training-nitidez'  # Cambia esto al nombre de tu bucket de entrada en S3
output_bucket = '2-4-training-quitar-vellos'  # Cambia esto al nombre de tu bucket de salida en S3

# Crear cliente de S3
s3_client = boto3.client('s3')

# Función para procesar una imagen
def process_image(image_bytes):
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    
    grayScale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    kernel = cv2.getStructuringElement(1, (10, 10))
    blackhat = cv2.morphologyEx(grayScale, cv2.MORPH_BLACKHAT, kernel)
    bhg = cv2.GaussianBlur(blackhat, (3, 3), cv2.BORDER_DEFAULT)
    ret, mask = cv2.threshold(bhg, 10, 255, cv2.THRESH_BINARY)
    dst = cv2.inpaint(image, mask, 6, cv2.INPAINT_TELEA)
    
    return dst

# Listar objetos en el bucket de entrada usando paginator
paginator = s3_client.get_paginator('list_objects_v2')
operation_parameters = {'Bucket': input_bucket}

for page in paginator.paginate(**operation_parameters):
    input_objects = page.get('Contents', [])
    
    for obj in input_objects:
        if obj['Key'].endswith(('.jpg', '.jpeg', '.png')):
            # Descargar la imagen desde S3
            image_obj = s3_client.get_object(Bucket=input_bucket, Key=obj['Key'])
            image_bytes = image_obj['Body'].read()

            # Procesar la imagen
            processed_image = process_image(image_bytes)
            
            # Convertir la imagen procesada a bytes
            success, encoded_image = cv2.imencode('.jpg', processed_image)
            if not success:
                continue
            encoded_image_bytes = encoded_image.tobytes()

            # Subir la imagen procesada al bucket de salida
            s3_output_path = f"{obj['Key']}"  # Cambia "output_folder" según tu ruta deseada
            s3_client.upload_fileobj(BytesIO(encoded_image_bytes), output_bucket, s3_output_path)
            
            print(f"Processed: {obj['Key']}")

print("Processing complete.")
