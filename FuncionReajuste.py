from PIL import Image
import os
# Ruta de la imagen que deseas cargar
#ruta_imagen = "C:/Users/FLAVIA/Downloads/Python/prueba2.jpg"

# Abrir la imagen
#imagen = Image.open(ruta_imagen)
#imagen.show()
# Mostrar información de la imagen
#print("Formato de la imagen:", imagen.format)
#print("Dimensiones de la imagen:", imagen.size)
#print("Modo de la imagen:", imagen.mode)

ruta_original = 'C:/Users/FLAVIA/Downloads/Python/prueba2.jpg'
ruta_destino = 'C:/Users/FLAVIA/Downloads/Python/prueba332.jpg'

imagen = Image.open(ruta_original)
ancho, alto = imagen.size

nuevo_ancho = ancho // 2
nuevo_alto = alto // 2

imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto))
imagen_redimensionada.save(ruta_destino)
imagen_redimensionada.show()
os.startfile(ruta_destino)
# Imprime los tamaños originales y redimensionados
print(f"Tamaño original: {ancho}x{alto}")
print(f"Tamaño redimensionado: {nuevo_ancho}x{nuevo_alto}")
