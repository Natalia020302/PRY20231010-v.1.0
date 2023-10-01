import os
import cv2
import numpy as np
import boto3
from io import BytesIO

def recortar_lunares(bucket_origen, bucket_destino, margen_superior, margen_inferior, margen_izquierdo, margen_derecho):
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
                # Recortar y procesar la imagen según los márgenes especificados
                # (código de procesamiento aquí)
                # Recortar la imagen según los márgenes especificados
                alto, ancho, _ = imagen.shape
                imagen_recortada = imagen[margen_superior:alto - margen_inferior, margen_izquierdo:ancho - margen_derecho]

                # Aplicar umbralización para segmentar los lunares o lesiones cutáneas
                gris = cv2.cvtColor(imagen_recortada, cv2.COLOR_BGR2GRAY)
                _, umbral = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

                # Encontrar los contornos de los objetos en la imagen umbralizada
                contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Encontrar el contorno de área máxima
                max_area = 0
                max_contorno = None
                for contorno in contornos:
                    area = cv2.contourArea(contorno)
                    if area > max_area:
                        max_area = area
                        max_contorno = contorno

                # Crear una máscara en blanco con el mismo tamaño que la imagen original recortada
                mascara = np.zeros_like(imagen_recortada, dtype=np.uint8)

                # Dibujar el contorno de área máxima en la máscara
                cv2.drawContours(mascara, [max_contorno], -1, (255, 255, 255), thickness=cv2.FILLED)

                # Ajustar el tamaño del kernel y el número de iteraciones para suavizar los bordes
                kernel_size = (6, 6)  # Ajusta el tamaño del kernel, por ejemplo, (3, 3) o (7, 7)
                dilate_iterations = 15  # Ajusta el número de iteraciones de dilatación, por ejemplo, 1 o 3
                erode_iterations = 12  # Ajusta el número de iteraciones de erosión, por ejemplo, 1 o 2

                # Aplicar operaciones de dilatación y erosión para suavizar los bordes
                kernel = np.ones(kernel_size, np.uint8)
                mascara = cv2.dilate(mascara, kernel, iterations=dilate_iterations)
                mascara = cv2.erode(mascara, kernel, iterations=erode_iterations)

                # Aplicar la máscara a la imagen recortada
                imagen_recortada = cv2.bitwise_and(imagen_recortada, mascara)

                # Guardar la imagen recortada en formato PNG con fondo transparente en la carpeta de destino
                #cv2.imwrite(ruta_destino.replace('.jpg', '.png'), imagen_recortada)
                
                s3_client.put_object(Bucket=bucket_destino, Key=archivo.replace('.jpg', '.png'), Body=cv2.imencode('.png', imagen_recortada)[1].tobytes())

                
                print(f"Processed: {archivo}")
                
            else:
                print(f"Error al procesar la imagen: {ruta_origen}")

    print("Processing complete.")
    
# Cambiar estos valores con los nombres reales de tus buckets en S3
bucket_origen = '2-4-training-quitar-vellos'
bucket_destino = '2-5-training-segmentacion'

# Establecer los márgenes de recorte
margen_superior = 100  
margen_inferior = 100 
margen_izquierdo = 170  
margen_derecho = 170 

# Llamar a la función para recortar los lunares o lesiones cutáneas
recortar_lunares(bucket_origen, bucket_destino, margen_superior, margen_inferior, margen_izquierdo, margen_derecho)
