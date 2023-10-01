from PIL import Image, ImageEnhance, ImageFilter
import os

carpeta_origen = '/Users/natty/Desktop/2_data_augmentation'
carpeta_destino = '/Users/natty/Desktop/3_reajustenitidez'

# Obtener una lista de los archivos que ya han sido procesados
archivos_procesados = [nombre_archivo for nombre_archivo in os.listdir(carpeta_destino) if nombre_archivo.startswith('imagenprocesada')]

# Obtener una lista de las nuevas imágenes que no han sido procesadas
nuevos_archivos = [nombre_archivo for nombre_archivo in os.listdir(carpeta_origen) if not nombre_archivo.startswith('imagenoriginal') and nombre_archivo != '.DS_Store']

# Obtener el último número de imagen procesada
ultimo_numero = len(archivos_procesados)

for nombre_archivo in nuevos_archivos:
    ruta_original = os.path.join(carpeta_origen, nombre_archivo)
    nombre_sin_extension, extension = os.path.splitext(nombre_archivo)

    # Incrementar el contador de imágenes procesadas
    ultimo_numero += 1

    # Nombre de la imagen procesada (utilizar el nombre original sin extensión)
    nombre_procesado = nombre_sin_extension

    # Procesar la imagen
    imagen = Image.open(ruta_original)
    ancho, alto = imagen.size

    if extension in ['.jpg', '.jpeg', '.png', '.gif']:
        # Definir las dimensiones límite
        alto_minimo = 1100
        alto_maximo = 1500

        # Calcular nuevo alto manteniendo la relación de aspecto
        nuevo_alto = min(max(alto, alto_minimo), alto_maximo)
        nuevo_ancho = int(ancho * nuevo_alto / alto)

        # Redimensionar la imagen original a las nuevas dimensiones
        imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto), resample=Image.LANCZOS)

        # Aplicar filtro de enfoque a los bordes
        imagen_enfocada = imagen_redimensionada.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

        # Aumentar el contraste de la imagen
        factor_contraste = 1.2  # Ajusta este valor para aumentar o disminuir el contraste
        realce_contraste = ImageEnhance.Contrast(imagen_enfocada)
        imagen_contraste = realce_contraste.enhance(factor_contraste)

        # Ajustar el brillo de la imagen
        factor_brillo = 0.7  # Ajusta este valor para hacer la imagen más oscura (0.0 - 1.0)
        realce_brillo = ImageEnhance.Brightness(imagen_contraste)
        imagen_oscurecida = realce_brillo.enhance(factor_brillo)

        # Aumentar la nitidez de la imagen
        factor_nitidez = 1  # Ajusta este valor para aumentar o disminuir la nitidez
        realce_nitidez = ImageEnhance.Sharpness(imagen_contraste)
        imagen_nitidez = realce_nitidez.enhance(factor_nitidez)

        # Guardar la imagen procesada en el destino con el nombre correspondiente
        ruta_destino_procesado = os.path.join(carpeta_destino, f"{nombre_procesado}{extension}")
        imagen_nitidez.save(ruta_destino_procesado, format='JPEG', quality=95)
