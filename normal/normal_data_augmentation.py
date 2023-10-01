from PIL import Image
import os

ruta_carpeta = '/Users/natty/Desktop/1_data_augmentation'
ruta_destino = '/Users/natty/Desktop/2_data_augmentation' 

def rotate_image(image_path, angle):
    with Image.open(image_path) as img:
        rotated_img = img.rotate(angle, expand=True)
        return rotated_img

def augment_images_in_folder(src_folder, dest_folder, rotations=4):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for filename in os.listdir(src_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            src_path = os.path.join(src_folder, filename)
            
            # Rename the original image
            orig_dest_path = os.path.join(dest_folder, f"0_{filename}")
            os.rename(src_path, orig_dest_path)
            
            for i in range(rotations):
                if i >= 3:
                    break

                dest_path = os.path.join(dest_folder, f"{i + 1}_{filename}")
                angle = 90 * (i + 1)
                rotated_img = rotate_image(orig_dest_path, angle)
                rotated_img.save(dest_path)

if __name__ == "__main__":
    augment_images_in_folder(ruta_carpeta, ruta_destino, rotations=3)
    print("Data augmentation completado.")
