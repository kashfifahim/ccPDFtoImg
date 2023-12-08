import os
import shutil
from os import getenv
from pathlib import Path
from pdf_to_images import pdf_to_images, zip_folder


if __name__ == '__main__':
    print("Script started")
    # Section 1: Setting up the environment variables
    # Setting up input and output folders
    input_folder = Path(getenv('CROSSCOMPUTE_INPUT_FOLDER', 'batches/standard/input'))
    output_folder = Path(getenv('CROSSCOMPUTE_OUTPUT_FOLDER', 'batches/standard/output'))
    print(f"Input folder: {input_folder}, Output folder: {output_folder}")
    output_folder.mkdir(parents=True, exist_ok=True)
    
    # Creating temporary folders for processing
    temp_folder = output_folder / 'temp'
    print(f"Temporary folder: {temp_folder}")
    temp_folder.mkdir(exist_ok=True)
    temp_zip_file = temp_folder / 'temp.zip'
    
    extract_to_folder = temp_folder / 'extracted_images'
    print(f"Extracted folder: {extract_to_folder}")
    extract_to_folder.mkdir(exist_ok=True)

    # PDF Processing
    pdf_files = list(input_folder.glob('*.pdf'))
    if not pdf_files:
        print("No PDF file found in the input folder")
        raise ValueError("No PDF file found in the input folder")
    pdf_file = pdf_files[0]
    print(f"PDF file found: {pdf_file}")
    pdf_to_images(pdf_file, extract_to_folder)

    output_zip_file = Path(output_folder / 'output.zip')
    print(f"Output zip file will be saved as: {output_zip_file}")
    
    zip_folder(extract_to_folder, temp_zip_file)
    
    # Verifying the video creation and performing cleanup
    if os.path.exists(temp_zip_file) and os.path.getsize(temp_zip_file) > 0:
        print(f"Zip file created successfully: {temp_zip_file}")
        # Move the completed video to the output folder
        shutil.move(str(temp_zip_file), str(output_zip_file))
        print(f"Zip moved to output folder: {output_zip_file}")
        
        # Cleanup: delete the folder with extracted images
        try:
            shutil.rmtree(temp_zip_file.parent)
            print(f"Deleted temp images folder: {extract_to_folder}")
        except OSError as e:
            print(f"Error deleting folder {extract_to_folder}: {e.strerror}")
    else:
        print(f"Zip creation failed or video file is empty: {output_zip_file}")

    print("Script ended")
    
    

