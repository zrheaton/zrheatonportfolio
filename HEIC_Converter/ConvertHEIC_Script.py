import os
from PIL import Image
import pillow_heif

def convert_heic_to_jpeg(input_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.heic'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.jpeg')

            # Read and convert the HEIC file
            heif_file = pillow_heif.read_heif(input_path)
            image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data)

            # Save the image as JPEG
            image.save(output_path, 'JPEG')

            print(f'Converted {filename} to {output_path}')

if __name__ == '__main__':
    input_folder = input("Please enter the path to the folder containing HEIC images: ")
    output_folder = input("Please enter the path to the output folder: ")

    convert_heic_to_jpeg(input_folder, output_folder)
