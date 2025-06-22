import os
import subprocess
import camelot
from PyPDF2 import PdfReader
import pikepdf
import pandas as pd

# Get the absolute path to the current script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SIGNED_PDF_PATH = os.path.join(BASE_DIR, "No_XBRL", "2__Form_AOC-4-13122024_signed.pdf")
UNSIGNED_PDF_PATH = os.path.join(BASE_DIR, "No_XBRL", "2__Form_AOC-4-13122024_unsigned.pdf")
OCR_PDF_PATH = os.path.join(BASE_DIR, "No_XBRL", "2__Form_AOC-4-13122024_ocr.pdf")

def run_qpdf(input_path, output_path):
    print(f"Removing signature using qpdf: {input_path} -> {output_path}")
    try:
        subprocess.run(["qpdf", "--decrypt", input_path, output_path], check=True)
    except Exception as e:
        print(f"qpdf failed: {e}")
        return False
    return True

def run_ocrmypdf(input_path, output_path):
    print(f"Running OCR with ocrmypdf: {input_path} -> {output_path}")
    try:
        subprocess.run(["ocrmypdf", "--force-ocr", input_path, output_path], check=True)
    except Exception as e:
        print(f"ocrmypdf failed: {e}")
        return False
    return True

def extract_tables_with_camelot(pdf_path):
    found_any = False
    try:
        tables = camelot.read_pdf(pdf_path, pages="all", strip_text='\n')
    except Exception as e:
        print(f"Error extracting tables: {e}")
        return

    print(f"Total tables extracted: {tables.n}")
    if tables.n == 0:
        print("No tables found.")
        return

    found_any = True
    output_dir = os.path.join(BASE_DIR, "Extracted_Tables")
    os.makedirs(output_dir, exist_ok=True)
    excel_path = os.path.join(output_dir, "all_tables.xlsx")
    csv_path = os.path.join(output_dir, "all_tables.csv")
    json_path = os.path.join(output_dir, "all_tables.json")

    # Save all tables in a single Excel file (each as a sheet)
    with pd.ExcelWriter(excel_path) as writer:
        for i, table in enumerate(tables, 1):
            print(f"\n--- Table {i} ---\n")
            # print(table.df.to_string(index=False, header=True))
            print('==================================================')
            sheet_name = f"Table_{i}"
            table.df.to_excel(writer, sheet_name=sheet_name, index=False)
    tables.export(csv_path, f='csv', compress=True)
    print(f"All tables saved to {csv_path}") 
    tables.export(json_path, f='json', compress=True)
    print(f"All tables saved to {json_path}")
    print(f"All tables saved to {excel_path}")

def extract_text_with_pypdf2(pdf_path):
    print("\nExtracting all text from each page using PyPDF2:\n")
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        for i, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            print(f"\n--- Page {i} ---\n")
            if text:
                print(text)
            else:
                print("[No extractable text found on this page]")
            print('==================================================')

def remove_pdf_signatures(input_path, output_path):
    print(f"Removing digital signatures using pikepdf: {input_path} -> {output_path}")
    try:
        with pikepdf.open(input_path, allow_overwriting_input=True) as pdf:
            root = pdf.trailer["/Root"]

            # Remove /Perms and /DocMDP if present
            for key in ["/Perms", "/DocMDP"]:
                if key in root:
                    del root[key]

            # Remove signature fields from AcroForm
            if "/AcroForm" in root:
                acroform = root["/AcroForm"]
                if "/Fields" in acroform:
                    fields = acroform["/Fields"]
                    new_fields = [f for f in fields if "/FT" not in f or f["/FT"] != "/Sig"]
                    acroform["/Fields"] = pikepdf.Array(new_fields)
                # Remove SigFlags if present
                if "/SigFlags" in acroform:
                    del acroform["/SigFlags"]

            # Remove signature widgets from page annotations
            for page in pdf.pages:
                if "/Annots" in page:
                    annots = page["/Annots"]
                    new_annots = []
                    for annot in annots:
                        subtype = annot.get("/Subtype", None)
                        if subtype == "/Widget" and annot.get("/FT", None) == "/Sig":
                            continue  # Skip signature widget
                        new_annots.append(annot)
                    page["/Annots"] = pikepdf.Array(new_annots)

            pdf.save(output_path)
        return True
    except Exception as e:
        print(f"pikepdf failed: {e}")
        return False

def main():
    # Step 1: Remove signature if unsigned file doesn't exist
    if not os.path.exists(UNSIGNED_PDF_PATH):
        if not remove_pdf_signatures(SIGNED_PDF_PATH, UNSIGNED_PDF_PATH):
            print("Failed to remove signature. Exiting.")
            return
    else:
        print("Unsigned PDF already exists.")

    # Step 2: OCR the unsigned PDF if OCR'd file doesn't exist
    if not os.path.exists(OCR_PDF_PATH):
        if not run_ocrmypdf(UNSIGNED_PDF_PATH, OCR_PDF_PATH):
            print("Failed to OCR PDF. Exiting.")
            return
    else:
        print("OCR'd PDF already exists.")

    # Step 3: Extract tables from the OCR'd PDF
    extract_tables_with_camelot(OCR_PDF_PATH)
    # extract_text_with_pypdf2(OCR_PDF_PATH)

if __name__ == "__main__":
    main() 