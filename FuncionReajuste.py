from PIL import Image

# Ruta de la imagen que deseas cargar
ruta_imagen = "C:/Users/FLAVIA/Downloads/Python/prueba2.jpg"

# Abrir la imagen
imagen = Image.open(ruta_imagen)
imagen.show()
# Mostrar información de la imagen
print("Formato de la imagen:", imagen.format)
print("Dimensiones de la imagen:", imagen.size)
print("Modo de la imagen:", imagen.mode)
