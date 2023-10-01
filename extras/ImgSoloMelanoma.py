import os
import pandas as pd
import shutil

# Define the paths to the folders and Excel file
#image_folder = "/Users/natty/Desktop/IMAGENES_ISIC/ISIC_2020_IMG_TRAIN"
#filtered_folder = "/Users/natty/Desktop/IMAGENES_ISIC/solo_img_melanoma"
#excel_file = "/Users/natty/Desktop/IMAGENES_ISIC/ISIC_2020_Training_GroundTruthl.xlsx"

# Define the paths to the folders and Excel file
image_folder = "/Users/natty/Desktop/IMAGENES_ISIC_2019/ISIC_2019_Training_Input"
filtered_folder = "/Users/natty/Desktop/IMAGENES_ISIC_2019/solo_melanoma"
excel_file = "/Users/natty/Desktop/IMAGENES_ISIC_2019/ISIC_2019_Training_Metadata_complete.xlsx"

# Load the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file)

# Filter the DataFrame to only include rows with "melanoma" diagnosis
filtered_df = df[df['diagnosis'] == 'melanoma']

# Iterate through the filtered DataFrame and move corresponding images to the filtered folder
for _, row in filtered_df.iterrows():
    image_name = row['image_name']
    image_name_with_extension = image_name + '.jpg'  # Append the '.jpg' extension
    image_path = os.path.join(image_folder, image_name_with_extension)
    if os.path.exists(image_path):
        shutil.move(image_path, filtered_folder)
        print(f"Moved image: {image_name_with_extension}")
    else:
        print(f"Image not found: {image_name_with_extension}")


print("Images moved successfully!")



