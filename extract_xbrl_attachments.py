import os
import logging
from pypdf import PdfReader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        # logging.FileHandler('extract_xbrl_attachments.log'),
        logging.StreamHandler()
    ]
)

XBRL_DIR = "XBRL"
OUTPUT_DIR = "XBRL_XML"


def extract_attachments(pdf_path, output_dir):
    """
    Extracts all attachments from a PDF document using pypdf's attachments property.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        reader = PdfReader(pdf_path)
        attachments = reader.attachments

        if not attachments:
            logging.info(f"No attachments found in: {pdf_path}")
            return

        logging.info(f"Found {len(attachments)} attachment(s) in '{os.path.basename(pdf_path)}'.")

        for attachment_id, filename in attachments.items():
            try:
                if attachment_id.isdigit():
                    logging.info(f"  - Skipping numeric attachment ID: {attachment_id}")
                    continue

                attachment_data_list = attachments[attachment_id]
                if not attachment_data_list:
                    logging.warning(f"  - No data found for attachment '{filename}' (ID: {attachment_id})")
                    continue

                attachment_data = attachment_data_list[0]
                safe_filename = "".join([c for c in filename if c.isalnum() or c in ('.', '_', '-')]).strip()
                if not safe_filename:
                    safe_filename = f"attachment_{attachment_id}"

                output_filepath = os.path.join(output_dir, safe_filename)
                with open(output_filepath, "wb") as f:
                    f.write(attachment_data)

                logging.info(f"  - Extracted attachment: '{safe_filename}' to '{output_filepath}'")
            except Exception as e:
                logging.error(f"  - Error extracting attachment '{filename}' (ID: {attachment_id}): {e}")

        logging.info(f"Successfully extracted attachments from '{os.path.basename(pdf_path)}' to '{output_dir}'")
    except Exception as e:
        logging.error(f"Error processing PDF '{pdf_path}': {e}")

def main():
    if not os.path.exists(XBRL_DIR):
        logging.error(f"XBRL directory '{XBRL_DIR}' does not exist.")
        return
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    pdf_files = [f for f in os.listdir(XBRL_DIR) if f.lower().endswith('.pdf')]
    if not pdf_files:
        logging.warning(f"No PDF files found in '{XBRL_DIR}'.")
        return

    logging.info(f"Found {len(pdf_files)} PDF files to process in '{XBRL_DIR}'.")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(XBRL_DIR, pdf_file)
        logging.info(f"Processing PDF: {pdf_file}")
        extract_attachments(pdf_path, OUTPUT_DIR)

    logging.info("All PDFs processed.")

if __name__ == "__main__":
    main() 