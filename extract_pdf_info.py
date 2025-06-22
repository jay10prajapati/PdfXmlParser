import os
from PyPDF2 import PdfReader
import re
from typing import Dict, Optional, Tuple


def extract_cin(text: str) -> Optional[str]:
    """
    Extract Corporate Identity Number (CIN) from text.
    CIN format: L[0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}
    
    Args:
        text: Text content from PDF
        
    Returns:
        CIN if found, None otherwise
    """
    # Pattern for CIN: L followed by 5 digits, 2 letters, 4 digits, 3 letters, 6 digits
    cin_pattern = r'L[0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}'
    match = re.search(cin_pattern, text)
    return match.group(0) if match else None


def extract_financial_year(text: str) -> Optional[str]:
    """
    Extract financial year from text using multiple patterns.
    
    Args:
        text: Text content from PDF
        
    Returns:
        Financial year if found, None otherwise
    """
    # Multiple patterns to match different financial year formats
    patterns = [
        (r'Financial Year\s*(\d{4}[-–]\d{2,4})', 'Financial Year'),
        (r'FY\s*(\d{4}[-–]\d{2,4})', 'FY'),
        (r'Year ended\s*(\d{1,2}(?:st|nd|rd|th)?\s*(?:March|April)\s*\d{4})', 'Year ended'),
        (r'Year\s*(\d{4}[-–]\d{2,4})', 'Year'),
        (r'(\d{4}[-–]\d{2,4})\s*Financial Year', 'Financial Year')
    ]
    
    for pattern, year_type in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return f"{year_type}: {match.group(1)}"
    
    return None


def get_fields(obj, tree=None, retval=None, fileobj=None):
    """
    Extracts field data if this PDF contains interactive form fields.
    The *tree* and *retval* parameters are for recursive use.
    """
    from collections import OrderedDict
    fieldAttributes = {'/FT': 'Field Type', '/Parent': 'Parent', '/T': 'Field Name', '/TU': 'Alternate Field Name',
                    '/TM': 'Mapping Name', '/Ff': 'Field Flags', '/V': 'Value', '/DV': 'Default Value'}
    if retval is None:
        retval = OrderedDict()
        catalog = obj.trailer["/Root"]
        # get the AcroForm tree
        if "/AcroForm" in catalog:
            tree = catalog["/AcroForm"]
        else:
            return None
    if tree is None:
        return retval

    obj._check_kids(tree, retval, fileobj)
    for attr in fieldAttributes:
        if attr in tree:
            # Tree is a field
            obj._build_field(tree, retval, fileobj, fieldAttributes)
            break

    if "/Fields" in tree:
        fields = tree["/Fields"]
        for f in fields:
            field = f.get_object()
            obj._build_field(field, retval, fileobj, fieldAttributes)

    return retval


def get_form_fields(infile):
    infile = PdfReader(open(infile, 'rb'))
    fields = get_fields(infile)
    if fields is None:
        return {}
    from collections import OrderedDict
    return OrderedDict((k, v.get('/V', '')) for k, v in fields.items())


def extract_text_from_pdf(pdf_path: str, max_pages: int = 5) -> str:
    """
    Extract text from PDF pages using PyPDF2.
    Args:
        pdf_path: Path to PDF file
        max_pages: Maximum number of pages to process
    Returns:
        Combined text from all processed pages
    """
    text = ""
    try:
        reader = PdfReader(open(pdf_path, 'rb'))
        for page_num in range(min(max_pages, len(reader.pages))):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                text += page_text
    except Exception as e:
        print(f"Warning: Error extracting text from page {page_num + 1}: {e}")
    return text


def process_pdf(pdf_path: str) -> Tuple[Optional[str], Optional[str], Dict[str, str]]:
    """
    Process a single PDF file and extract required information using PyPDF2.
    Args:
        pdf_path: Path to PDF file
    Returns:
        Tuple of (CIN, financial year, form fields)
    """
    try:
        # Get form fields
        form_fields = get_form_fields(pdf_path)
        # Try to extract CIN and financial year from form fields first
        cin = form_fields.get('data[0].FormAOC4_Dtls[0].Segment1_PartA[0].CIN_C[0]')
        from_date = form_fields.get('data[0].FormAOC4_Dtls[0].Segment1_PartA[0].FromDate[0]')
        to_date = form_fields.get('data[0].FormAOC4_Dtls[0].Segment1_PartA[0].ToDate[0]')
        if from_date and to_date:
            financial_year = f"{from_date} to {to_date}"
        else:
            financial_year = None
        # If not found in form fields, fall back to text extraction
        if not cin or not financial_year:
            text = extract_text_from_pdf(pdf_path)
            if not cin:
                cin = extract_cin(text)
            if not financial_year:
                financial_year = extract_financial_year(text)
        return cin, financial_year, form_fields
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None, None, {}


def main():
    # Directory containing No-XBRL PDFs
    input_dir = "No_XBRL"
    if not os.path.exists(input_dir):
        print(f"Error: Directory '{input_dir}' does not exist")
        return
    # Get all PDF files
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return
    print(f"Found {len(pdf_files)} PDF files to process")
    # Process each PDF file
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        cin, financial_year, form_fields = process_pdf(pdf_path)
        print(f"\nFile: {pdf_file}")
        print(f"CIN: {cin if cin else 'Not found'}")
        print(f"Financial Year: {financial_year if financial_year else 'Not found'}")
        # if form_fields:
        #     print("\nForm Fields Found:")
        #     for field_name, field_value in form_fields.items():
        #         print(f"{field_name}: {field_value}")


if __name__ == "__main__":
    main()