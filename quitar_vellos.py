import os
import cv2

# Function to resize image while maintaining aspect ratio
# def resize_image(image, target_height):
#     original_height, original_width = image.shape[:2]
#     aspect_ratio = original_width / original_height
#     target_width = int(target_height * aspect_ratio)
#     resized_image = cv2.resize(image, (target_width, target_height))
#     return resized_image

# Specify input and output folders
input_folder = "/Users/natty/Desktop/3_reajustenitidez"
output_folder = "/Users/natty/Desktop/4_quitar_vellos"

# Iterate through all image files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Read image
        image = cv2.imread(input_path, cv2.IMREAD_COLOR)

        # Resize image if its height is greater than 1800
        # if image.shape[0] > 1800:
        #     image = resize_image(image, target_height=1800)


        # Gray scale
        grayScale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        # Black hat filter
        kernel = cv2.getStructuringElement(1, (17, 17))
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
