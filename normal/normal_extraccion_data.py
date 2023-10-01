import os
import cv2
import numpy as np

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
    archivos = os.listdir(bucket_origen)
    for archivo in archivos:
        ruta_origen = os.path.join(bucket_origen, archivo)
        imagen = cv2.imread(ruta_origen)
        asimetria = calcular_asimetria(imagen)
        variacion_color = calcular_variacion_color(imagen)
        diametro = calcular_diametro(imagen)
        diametro, punto_izquierdo, punto_derecho = calcular_diametro(imagen)
        valor_bordes = calcular_borde_irisado(imagen) # Obtener el valor del borde irisado
        nombre_archivo = os.path.splitext(archivo)[0] + ".txt"
        ruta_destino = os.path.join(bucket_destino, nombre_archivo)
        with open(ruta_destino, "w") as archivo_txt:
            archivo_txt.write(f"Asimetria: {asimetria:.4f}\n")
            archivo_txt.write(f"Color: {variacion_color:.4f}\n")
            archivo_txt.write(f"Diametro: {diametro}\n")
            archivo_txt.write(f"Bordes: {valor_bordes:.4f}\n") # Agregar el valor del borde al archivo de texto

bucket_origen = "/Users/natty/Desktop/PRUEBASHORT/segmenfinalciclo"
bucket_destino = "/Users/natty/Desktop/PRUEBASHORT/extracfinal"
extraer_caracteristicas(bucket_origen, bucket_destino)