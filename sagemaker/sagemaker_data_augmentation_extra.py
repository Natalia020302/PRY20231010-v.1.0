import boto3
from PIL import Image
import io

# Nombre del bucket de S3 donde se encuentran las imágenes originales
bucket_origen = '2-training'
# Nombre del bucket de S3 donde se guardarán las imágenes rotadas
bucket_destino = '2-2-training-dataaugmentation'

# Inicializa el cliente de S3
s3_client = boto3.client('s3')

# Obtiene la lista de objetos en el bucket de origen con paginación
paginator = s3_client.get_paginator('list_objects_v2')
result = paginator.paginate(Bucket=bucket_origen)

# Inicializa una lista para almacenar los objetos en orden normal
objetos_en_orden_normal = []

# Itera a través de los objetos en el bucket de origen y los almacena en la lista
for page in result:
    for obj in page.get('Contents', []):
        archivo = obj['Key']
        if archivo.endswith(".jpg") or archivo.endswith(".png"):
            objetos_en_orden_normal.append(archivo)

# Procesa los objetos en orden normal
for archivo in objetos_en_orden_normal:
    # Descarga la imagen desde el bucket de origen
    imagen_bytes = s3_client.get_object(Bucket=bucket_origen, Key=archivo)['Body'].read()
    imagen = Image.open(io.BytesIO(imagen_bytes))
    
    # Guarda la imagen original con "0_"
    s3_client.put_object(Bucket=bucket_destino, Key=f"0_{archivo}", Body=imagen_bytes)
    
    # Rotación a 45 grados
    imagen_rotada_45 = imagen.rotate(45)
    imagen_rotada_45_bytes = io.BytesIO()
    imagen_rotada_45.save(imagen_rotada_45_bytes, format='JPEG')
    s3_client.put_object(Bucket=bucket_destino, Key=f"1_{archivo}", Body=imagen_rotada_45_bytes.getvalue())
    
    # Rotación a 135 grados
    imagen_rotada_135 = imagen.rotate(135)
    imagen_rotada_135_bytes = io.BytesIO()
    imagen_rotada_135.save(imagen_rotada_135_bytes, format='JPEG')
    s3_client.put_object(Bucket=bucket_destino, Key=f"2_{archivo}", Body=imagen_rotada_135_bytes.getvalue())
   
    print(f"Processed: {archivo}")

print("Proceso completado. Imágenes rotadas guardadas en el bucket de destino.")
