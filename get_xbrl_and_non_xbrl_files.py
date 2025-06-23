"""
check_xbrl.py

This script scans all ZIP files in the 'Input_data' directory, extracts their PDF files, and checks if each PDF filename contains 'XBRL'.
- PDFs with 'XBRL' in the name are reported.
- PDFs without 'XBRL' in the name are moved to the 'No_XBRL' directory, with duplicate names handled by appending a suffix.
- Temporary extraction directories are cleaned up after each ZIP is processed.

This helps segregate and identify PDFs that do not follow the XBRL naming convention for further review.
"""

import os
import zipfile
import shutil
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)


def check_pdf_xbrl(zip_path, temp_dir):
    """
    Check each PDF in the zip file for XBRL designation in filename.
    Move No-XBRL PDFs to No_XBRL folder.
    """
    try:
        # Clean up temp directory if it exists
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        # Extract zip file to temp directory
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Get zip filename for reporting
        zip_name = os.path.splitext(os.path.basename(zip_path))[0]
        logging.info(f"Checking PDFs in: {zip_name}")
        
        # Find all PDF files in the extracted directory
        pdf_files = []
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        
        if not pdf_files:
            logging.warning(f"No PDF files found in {zip_name}")
            return
        
        # Ensure No_XBRL and XBRL directories exist
        no_xbrl_dir = "No_XBRL"
        xbrl_dir = "XBRL"
        if not os.path.exists(no_xbrl_dir):
            os.makedirs(no_xbrl_dir)
        if not os.path.exists(xbrl_dir):
            os.makedirs(xbrl_dir)
        
        # Check each PDF filename
        for pdf_file in pdf_files:
            pdf_name = os.path.basename(pdf_file)
            if "XBRL" in pdf_name:
                logging.info(f"File: {pdf_name} - (XBRL) -> Moving to {xbrl_dir}")
                # Move the file to XBRL folder
                dest_path = os.path.join(xbrl_dir, pdf_name)
                # If file with same name exists, add a suffix
                base, ext = os.path.splitext(pdf_name)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(xbrl_dir, f"{base}_{counter}{ext}")
                    counter += 1
                shutil.move(pdf_file, dest_path)
            else:
                logging.info(f"File: {pdf_name} - (No-XBRL) -> Moving to {no_xbrl_dir}")
                # Move the file to No_XBRL folder
                dest_path = os.path.join(no_xbrl_dir, pdf_name)
                # If file with same name exists, add a suffix
                base, ext = os.path.splitext(pdf_name)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(no_xbrl_dir, f"{base}_{counter}{ext}")
                    counter += 1
                shutil.move(pdf_file, dest_path)
        
    except Exception as e:
        logging.error(f"Error processing zip file {zip_path}: {e}")
    finally:
        # Clean up temp directory after processing this zip
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def main():
    # Process all zip files in Input_data directory
    input_dir = "Input_data"
    if not os.path.exists(input_dir):
        logging.error(f"Error: Input directory '{input_dir}' does not exist")
        return
    
    zip_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.zip')]
    
    if not zip_files:
        logging.warning(f"No zip files found in {input_dir}")
        return
    
    logging.info(f"Found {len(zip_files)} zip files to process")
    
    # Process each zip file
    for zip_file in zip_files:
        zip_path = os.path.join(input_dir, zip_file)
        check_pdf_xbrl(zip_path, "temp_extract")


if __name__ == "__main__":
    main() 