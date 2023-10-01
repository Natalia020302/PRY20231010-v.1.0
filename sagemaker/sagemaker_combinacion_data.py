import csv
import os
import boto3

def procesar_documentos(bucket_txt, bucket_csv):
    s3_client = boto3.client('s3')
    
    # Leer el archivo CSV y crear un diccionario con los nombres y características
    diccionario_caracteristicas = {}
    response = s3_client.get_object(Bucket=bucket_csv, Key='excel.csv')
    contenido_csv = response['Body'].read().decode('utf-8').splitlines()
    lector_csv = csv.reader(contenido_csv)
    
    for fila in lector_csv:
        if len(fila) >= 4:
            nombre = fila[0]
            sexo = fila[1]
            edad = fila[2]
            melanoma = fila[3]
            diccionario_caracteristicas[nombre] = {
                'Edad': edad,
                'Melanoma': melanoma
            }

    # Obtener la lista de archivos .txt en el bucket
    paginator = s3_client.get_paginator('list_objects_v2')
    operation_parameters = {'Bucket': bucket_txt}

    for page in paginator.paginate(**operation_parameters):
        input_objects = page.get('Contents', [])
        
        for obj in input_objects:
            archivo = obj['Key']
            
            if archivo.endswith('.txt'):
                # Descargar el archivo .txt desde S3
                response = s3_client.get_object(Bucket=bucket_txt, Key=archivo)
                contenido_txt = response['Body'].read().decode('utf-8')
                nombre_archivo = os.path.splitext(archivo)[0][4:]  # Ignorar los primeros 2 caracteres
               # nombre_archivo = os.path.splitext(archivo)[0] # no ignorar los primeros 2 caracteres

                caracteristicas = diccionario_caracteristicas.get(nombre_archivo)

                if caracteristicas:
                    # Agregar las características al archivo .txt
                    contenido_nuevo = f"Edad: {caracteristicas['Edad'].rstrip()}\n"
                    contenido_nuevo += f"Melanoma: {caracteristicas['Melanoma'].rstrip()}\n"
                    contenido_actualizado = contenido_txt + contenido_nuevo

                    # Subir el archivo .txt actualizado a S3
                    s3_client.put_object(Bucket=bucket_txt, Key=archivo, Body=contenido_actualizado.encode('utf-8'))

                    print(f"Processed: {archivo}")
                else:
                    print(f"Características no encontradas para: {nombre_archivo}")

    print("Processing complete.")

# Cambiar estos valores con los nombres reales de tus buckets en S3
bucket_txt = '2-6-training-extraccion'
bucket_csv = 'excel-imagenescompletas'

# Llamar a la función para procesar los documentos y agregar las características
procesar_documentos(bucket_txt, bucket_csv)