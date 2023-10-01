import cv2
import os  # Agregar la importación de os
import numpy as np
import boto3
from io import BytesIO

def calcular_asimetria(imagen):
    # Código para calcular la asimetría
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    asimetria = np.sum(np.abs(imagen_gris - np.flip(imagen_gris))) / (2 * imagen_gris.size)
    return asimetria

def calcular_variacion_color(imagen):
    # Código para calcular la variación de color
    imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    canal_saturacion = imagen_hsv[:, :, 1]
    desviacion_estandar = np.std(canal_saturacion)
    return desviacion_estandar

def calcular_borde_irisado(imagen):
    # Código para calcular el borde irisado
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    bordes = cv2.Canny(imagen_gris, 100, 200)
    valor_promedio = cv2.mean(imagen_gris, mask=bordes)[0]
    return valor_promedio

def calcular_diametro(imagen):
    # Código para calcular el diámetro
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    _, imagen_binaria = cv2.threshold(imagen_gris, 0, 255, cv2.THRESH_BINARY)
    contornos, _ = cv2.findContours(imagen_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contorno_principal = max(contornos, key=cv2.contourArea)
    puntos_extremos = contorno_principal[:, 0, :]
    punto_izquierdo = puntos_extremos[np.argmin(puntos_extremos[:, 0])]
    punto_derecho = puntos_extremos[np.argmax(puntos_extremos[:, 0])]
    diametro = np.linalg.norm(punto_derecho - punto_izquierdo)
    return diametro, punto_izquierdo, punto_derecho

def extraer_caracteristicas(bucket_origen, bucket_destino):
    s3_client = boto3.client('s3')
    
    paginator = s3_client.get_paginator('list_objects_v2')
    operation_parameters = {'Bucket': bucket_origen}

    for page in paginator.paginate(**operation_parameters):
        input_objects = page.get('Contents', [])
        
        for obj in input_objects:
            archivo = obj['Key']
            ruta_origen = f"s3://{bucket_origen}/{archivo}"

            # Descargar la imagen desde S3
            response = s3_client.get_object(Bucket=bucket_origen, Key=archivo)
            imagen_bytes = response['Body'].read()
            imagen = cv2.imdecode(np.frombuffer(imagen_bytes, np.uint8), cv2.IMREAD_COLOR)

            if imagen is not None:
                asimetria = calcular_asimetria(imagen)
                variacion_color = calcular_variacion_color(imagen)
                diametro, _, _ = calcular_diametro(imagen)
                valor_bordes = calcular_borde_irisado(imagen)
                nombre_archivo = os.path.splitext(archivo)[0] + ".txt"
                ruta_destino = f"s3://{bucket_destino}/{nombre_archivo}"
                
                # Crear el contenido del archivo de texto
                contenido_txt = f"Asimetria: {asimetria:.4f}\n"
                contenido_txt += f"Color: {variacion_color:.4f}\n"
                contenido_txt += f"Diametro: {diametro}\n"
                contenido_txt += f"Bordes: {valor_bordes:.4f}\n"

                # Subir el archivo de texto al bucket de destino
                s3_client.put_object(Bucket=bucket_destino, Key=nombre_archivo, Body=contenido_txt.encode('utf-8'))

                print(f"Processed: {archivo}")
            else:
                print(f"Error al procesar la imagen: {ruta_origen}")

    print("Processing complete.")

# Cambiar estos valores con los nombres reales de tus buckets en S3
bucket_origen = '2-5-training-segmentacion'
bucket_destino = '2-6-training-extraccion'

# Llamar a la función para extraer las características y guardar los resultados
extraer_caracteristicas(bucket_origen, bucket_destino)
