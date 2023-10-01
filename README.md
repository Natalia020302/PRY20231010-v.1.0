# PRY20231010-v.1.0
 Repositorio para el proyecto de tesis PRY20231010 UPC.

## Tecnologías 🛠️

* [Python] - Lenguaje de programación
* [SVM] - Algoritmo de ML

## Orden de los archivos
 * Data augmentation - el archivo con dicho nombre y el archivo extra (opcional).
 * Mejorar imagen - el archivo con dicho nombre para mejorar la calidad de las imágenes.
 * Quitar vellos - el archivo con dicho nombre para eliminar los vellos que podrían tapar la lesión a analizar.
 * Segmentación - el archivo con dicho nombre para reducir el alcance del análisis a la lesion cutánea.
 * Quitar vacios (opcional) - es posible que, luego de la segmentación, algunos archivos queden casi completamente vacíos, por ello es recomendable transportarlos a otro bucket en s3 o eliminarlos.
 * Extraccion de data - para poder obtener un txt con los valores de asimetría, bordes, color y diámetro de la lesión.
 * Combinación de data - para añadir la data de Edad y Diagnóstico al txt generado en el paso anterior.
 * Entrenamiento - para entrenar el modelo, obtenerlo y también obtener los valores de matriz de confusión y métricas de efectividad.

## Consideraciones

* El código más completo está en los files destinados a utilizarse en SageMaker notebooks
* El tipo de archivo de SageMaker notebooks debería ser .ipynb, pero GitHub no lo identifica.
* Existen algunas dependencias, como el descargar CV2. SageMaker dará la sugerencia de instalación cuando indentifique que lo necesita.
