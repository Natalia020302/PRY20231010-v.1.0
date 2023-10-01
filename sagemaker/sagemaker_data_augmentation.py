from PIL import Image
import boto3
from io import BytesIO

ruta_carpeta = '1-training'  # Nombre del bucket S3 de origen
ruta_destino = '2-training'  # Nombre del bucket S3 de destino

s3 = boto3.client('s3')

def rotate_image(image, angle):
    rotated_img = image.rotate(angle, expand=True)
    return rotated_img

def augment_images_in_folder(src_folder, dest_folder, rotations=4):
    paginator = s3.get_paginator('list_objects_v2')
    operation_parameters = {'Bucket': src_folder}
    
    for page in paginator.paginate(**operation_parameters):
        objects = page.get('Contents', [])
        
        for obj in objects:
            filename = obj['Key'].split('/')[-1]
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                src_path = f"{src_folder}/{filename}"
                
                # Download the original image
                response = s3.get_object(Bucket=src_folder, Key=obj['Key'])
                original_image = Image.open(BytesIO(response['Body'].read()))
                
                # Save the original image with prefix 0_
                dest_path_original = f"0_{filename}"
                with BytesIO() as output_original:
                    original_image.save(output_original, format='PNG')
                    output_original.seek(0)
                    s3.upload_fileobj(output_original, dest_folder, dest_path_original)
                    
                for i in range(rotations):
                    if i >= 3:
                        break
    
                    dest_path = f"{i + 1}_{filename}"
                    angle = 90 * (i + 1)
                    rotated_img = rotate_image(original_image, angle)
                    
                    with BytesIO() as output:
                        rotated_img.save(output, format='PNG')
                        output.seek(0)
                        s3.upload_fileobj(output, dest_folder, dest_path)
                    
                    print(f"Processed: {filename}, Rotation: {i + 1}")
    
    print("Data augmentation completado.")

if __name__ == "__main__":
    augment_images_in_folder(ruta_carpeta, ruta_destino, rotations=3)