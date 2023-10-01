import os

# Directorio donde se encuentran los archivos JPEG
directorio = '/Users/natty/Desktop/s3_no_melanoma70'

# Itera sobre todos los archivos en el directorio
for filename in os.listdir(directorio):
    if filename.endswith('.jpg'):
        # Genera el nuevo nombre de archivo con "0_" al inicio
        nuevo_nombre = "0_" + filename
        # Crea la ruta completa al archivo original y al nuevo archivo
        ruta_original = os.path.join(directorio, filename)
        ruta_nuevo = os.path.join(directorio, nuevo_nombre)
        # Renombra el archivo
        os.rename(ruta_original, ruta_nuevo)

print("Archivos renombrados exitosamente.")
