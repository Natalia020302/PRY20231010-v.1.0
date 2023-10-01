import os
import cv2

# Specify input and output folders
input_bucket = "/Users/natty/Desktop/3_reajustenitidez"
output_bucket = "/Users/natty/Desktop/4_quitar_vellos"

# Iterate through all image files in the input folder
for filename in os.listdir(input_bucket):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        input_path = os.path.join(input_bucket, filename)
        output_path = os.path.join(output_bucket, filename)

        # Read image
        image = cv2.imread(input_path, cv2.IMREAD_COLOR)

        # Gray scale
        grayScale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        # Black hat filter
        kernel = cv2.getStructuringElement(1, (10, 10))
        #it was 17 i think, changed it to 30
        blackhat = cv2.morphologyEx(grayScale, cv2.MORPH_BLACKHAT, kernel)
        # Gaussian filter
        bhg = cv2.GaussianBlur(blackhat, (3, 3), cv2.BORDER_DEFAULT)
        # Binary thresholding (MASK)
        ret, mask = cv2.threshold(bhg, 10, 255, cv2.THRESH_BINARY)
        # Replace pixels of the mask
        dst = cv2.inpaint(image, mask, 6, cv2.INPAINT_TELEA)

        # Save the clean image to the output folder
        cv2.imwrite(output_path, dst, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

print("Processing complete.")
