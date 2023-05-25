import cv2
import numpy as np
import os

def segment_images(source_folder, destination_folder):
    # Crea el directorio de destino si no existe
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Obtén la lista de archivos de imagen en el directorio de origen
    image_files = [f for f in os.listdir(source_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    for image_file in image_files:
        # Verifica si la imagen ya ha sido procesada anteriormente
        if image_file.startswith('listo'):
            print(f"La imagen {image_file} ya ha sido procesada. Se omite.")
            continue
        
        # Lee la imagen
        image_path = os.path.join(source_folder, image_file)
        img = cv2.imread(image_path)

        # Realiza la segmentación aquí
        # Puedes utilizar técnicas como umbralización, segmentación basada en color, etc.
        # Asegúrate de obtener una máscara que destaque la parte del lunar o herida

        # Aplica un filtro de mediana para reducir el ruido
        filtered_img = cv2.medianBlur(img, 5)

        # Ejemplo de segmentación mediante umbralización simple
        gray = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Aplica operaciones morfológicas para mejorar la segmentación
        kernel = np.ones((3, 3), np.uint8)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations=6)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel, iterations=6)

        # Encuentra los contornos de la segmentación
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Encuentra el contorno más grande
        largest_contour = max(contours, key=cv2.contourArea)

        # Crea una máscara en blanco del tamaño de la imagen original
        mask = np.zeros_like(img)

        # Dibuja el contorno en la máscara
        cv2.drawContours(mask, [largest_contour], 0, (255, 255, 255), thickness=cv2.FILLED)




        # Aplica la máscara a la imagen original para obtener la parte segmentada en color
        #segmented_img = cv2.bitwise_and(img, img, mask=threshold)
        segmented_img = cv2.bitwise_and(img, mask)

        # Cambia el nombre de la imagen origen procesada agregando el prefijo "listo"
        processed_image_name = 'listo_' + image_file
        processed_image_path = os.path.join(source_folder, processed_image_name)
        os.rename(image_path, processed_image_path)
        print(f"Imagen procesada renombrada: {processed_image_path}")

        # Guarda la imagen segmentada en el directorio de destino
        #segmented_image_name = 'segmentada_' + image_file
        segmented_image_name = 'segmentada_' + image_file.split('.')[0] + '.png'
        segmented_image_path = os.path.join(destination_folder, segmented_image_name)
        #destination_path = os.path.join(destination_folder, segmented_image_name)
        #cv2.imwrite(destination_path, segmented_img)

        #print(f"Imagen segmentada guardada: {destination_path}")
        cv2.imwrite(segmented_image_path, segmented_img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        print(f"Parte segmentada guardada: {segmented_image_path}")

    print("Segmentación de imágenes completada.")


# Ejemplo de uso
source_folder = "/Users/natty/Desktop/prueba_origen"
destination_folder = "/Users/natty/Desktop/prueba_destino"

segment_images(source_folder, destination_folder)
