from pypdf import PdfReader
# from pypdf.annotations import FileAttachmentAnnotation
import os
import zipfile
from pathlib import Path


def extract_attachments(pdf_path, output_dir):
    """
    Extracts all attachments from a PDF document using pypdf's attachments property.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Create PdfReader object
        reader = PdfReader(pdf_path)
        
        # Get the attachments dictionary
        attachments = reader.attachments
        
        if not attachments:
            print(f"No attachments found in: {pdf_path}")
            return
            
        print(f"\nFound {len(attachments)} attachment(s) in the PDF.")
        
        # Extract each attachment
        for attachment_id, filename in attachments.items():
            try:
                # Skip if attachment_id is just a numeric string
                if attachment_id.isdigit():
                    print(f"  - Skipping numeric attachment ID: {attachment_id}")
                    continue
                
                # Get the attachment data from the attachments dictionary
                attachment_data_list = attachments[attachment_id]
                
                if not attachment_data_list:
                    print(f"  - Warning: No data found for attachment '{filename}' (ID: {attachment_id})")
                    continue
                
                # Get the first item from the list (usually there's only one)
                attachment_data = attachment_data_list[0]
                
                # Sanitize filename
                safe_filename = "".join([c for c in filename if c.isalnum() or c in ('.', '_', '-')]).strip()
                if not safe_filename:
                    safe_filename = f"attachment_{attachment_id}"
                
                # Create output file path
                output_filepath = os.path.join(output_dir, safe_filename)
                
                # Save the attachment
                with open(output_filepath, "wb") as f:
                    f.write(attachment_data)
                
                print(f"  - Extracted attachment: '{safe_filename}' to '{output_filepath}'")
                
            except Exception as e:
                print(f"  - Error extracting attachment '{safe_filename}' (ID: {attachment_id}): {e}")
        
        print(f"\nSuccessfully extracted attachments to '{output_dir}'")
        
    except Exception as e:
        print(f"Error processing PDF '{pdf_path}': {e}")


def process_zip_file(zip_path, main_output_dir):
    """
    Process a zip file containing PDFs and extract attachments maintaining hierarchy.
    """
    try:
        # Create a temporary directory to extract PDFs
        temp_dir = os.path.join(main_output_dir, "temp_extract")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Get zip filename without extension for creating output directory
        zip_name = os.path.splitext(os.path.basename(zip_path))[0]
        
        print(f"\nProcessing zip file: {zip_path}")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extract all files to temp directory
            zip_ref.extractall(temp_dir)
            
            # Find all PDF files in the extracted directory
            pdf_files = []
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        pdf_files.append(os.path.join(root, file))
            
            if not pdf_files:
                print(f"No PDF files found in {zip_path}")
                return
            
            print(f"Found {len(pdf_files)} PDF files in the zip")
            
            # Process each PDF file
            for pdf_file in pdf_files:
                # Get relative path from temp directory
                rel_path = os.path.relpath(pdf_file, temp_dir)
                # Create corresponding output directory structure
                pdf_dir = os.path.splitext(rel_path)[0]  # Remove .pdf extension
                output_dir = os.path.join(main_output_dir, zip_name, pdf_dir)
                
                print(f"\nProcessing PDF: {rel_path}")
                extract_attachments(pdf_file, output_dir)
        
        # Clean up temporary directory
        import shutil
        shutil.rmtree(temp_dir)
        
    except Exception as e:
        print(f"Error processing zip file {zip_path}: {e}")


def main():
    # Create main Extracted_data directory
    main_output_dir = "Extracted_data"
    if not os.path.exists(main_output_dir):
        os.makedirs(main_output_dir)
    
    # Process all zip files in Input_data directory
    input_dir = "Input_data"
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist")
        return
    
    zip_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.zip')]
    
    if not zip_files:
        print(f"No zip files found in {input_dir}")
        return
    
    print(f"Found {len(zip_files)} zip files to process")
    
    for zip_file in zip_files:
        zip_path = os.path.join(input_dir, zip_file)
        process_zip_file(zip_path, main_output_dir)


if __name__ == "__main__":
    main()