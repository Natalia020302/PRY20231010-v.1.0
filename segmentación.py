import os
import cv2
import imghdr
import numpy as np

def recortar_lunares(origen, destino, margen_superior, margen_inferior, margen_izquierdo, margen_derecho):
    # Obtener la lista de archivos en la carpeta de origen
    archivos = os.listdir(origen)

    for archivo in archivos:
        if archivo == '.DS_Store':  # Ignorar el archivo .DS_Store
            continue
        ruta_origen = os.path.join(origen, archivo)
        ruta_destino = os.path.join(destino, archivo)

        # Verificar si el archivo es una imagen (JPEG, JPG, PNG)
        if imghdr.what(ruta_origen) in ['jpeg', 'jpg', 'png']:
            # Leer la imagen de la carpeta de origen
            imagen = cv2.imread(ruta_origen)

            if imagen is not None:
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
                cv2.imwrite(ruta_destino.replace('.jpg', '.png'), imagen_recortada)
            else:
                print(f"Error al leer la imagen: {ruta_origen}")
        else:
            print(f"Formato de archivo no admitido: {ruta_origen}")

# Solicitar la carpeta de origen y la carpeta de destino al usuario
carpeta_origen = "C:/Users/FLAVIA/Downloads/codigomodel/mejoramiento/destinomejor"
carpeta_destino = "C:/Users/FLAVIA/Downloads/codigomodel/segmentacion/destinosegm"

# Solicitar los márgenes de recorte al usuario
margen_superior = 200  # 100 para las de tamaño pequeño
margen_inferior = 200  # 100 para las de tamaño pequeño
margen_izquierdo = 370  # 100 para las de tamaño pequeño
margen_derecho = 370  # 100 para las de tamaño pequeño

# Llamar a la función para recortar los lunares o lesiones cutáneas
recortar_lunares(carpeta_origen, carpeta_destino, margen_superior, margen_inferior, margen_izquierdo, margen_derecho)
