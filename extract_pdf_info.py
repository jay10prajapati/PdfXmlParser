import os
from PyPDF2 import PdfReader
import re
import json
import csv
from datetime import datetime
from typing import Dict, Optional, Tuple, Any, List


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


def detect_form_type(form_fields: Dict[str, str]) -> str:
    """
    Detect whether the PDF is MGT7 or AOC4 form based on form fields.
    Args:
        form_fields: Dictionary of form fields
    Returns:
        Form type: 'MGT7', 'AOC4', or 'UNKNOWN'
    """
    # Check for MGT7 form fields
    for field_name in form_fields.keys():
        if 'FormMGT7' in field_name:
            return 'MGT7'
        elif 'FormAOC4' in field_name:
            return 'AOC4'
    return 'UNKNOWN'


def decode_form_values(value: str, field_type: str) -> str:
    """
    Decode abbreviated form values to readable text.
    Args:
        value: The abbreviated value from form
        field_type: Type of field to determine decoding rules
    Returns:
        Decoded readable value
    """
    if not value:
        return value
    
    # Company type mappings
    type_mappings = {
        'PRIV': 'Private Company',
        'PUBL': 'Public Company',
        'GOVT': 'Government Company',
        'FORE': 'Foreign Company'
    }
    
    # Category mappings
    category_mappings = {
        'CLSH': 'Company limited by shares',
        'CLGU': 'Company limited by guarantee',
        'ULCL': 'Unlimited company',
        'NIDC': 'Nidhi Company'
    }
    
    # Sub-category mappings
    subcategory_mappings = {
        'NGOV': 'Indian Non-Government company',
        'GOVT': 'Government company',
        'FORE': 'Foreign company'
    }
    
    # Yes/No mappings
    yes_no_mappings = {
        '/YES': 'Yes',
        '/NO': 'No',
        'YES': 'Yes',
        'NO': 'No'
    }
    
    if field_type == 'type':
        return type_mappings.get(value, value)
    elif field_type == 'category':
        return category_mappings.get(value, value)
    elif field_type == 'subcategory':
        return subcategory_mappings.get(value, value)
    elif field_type == 'yes_no':
        return yes_no_mappings.get(value, value)
    
    return value


def extract_business_activities(form_fields: Dict[str, str]) -> Dict[str, Any]:
    """
    Extract business activities information from MGT7 form fields.
    Args:
        form_fields: Dictionary of form fields
    Returns:
        Dictionary with business activities information
    """
    business_info = {}
    
    # Number of business activities
    business_info['Number_Of_Activities'] = form_fields.get('data[0].FormMGT7_Dtls[0].MainPage[0].SectionII[0].NoBusinessActivity[0]', '')
    
    # Extract business activities table
    activities = []
    
    # Check for multiple rows (Row1, Row2, etc.)
    for i in range(1, 11):  # Check up to 10 rows
        row_key = f'Row{i}'
        
        # Check if this row exists
        s_no_key = f'data[0].FormMGT7_Dtls[0].MainPage[0].SectionIITable[0].PrincipalBusinessActivity[0].{row_key}[0].Cell1[0]'
        if s_no_key in form_fields and form_fields[s_no_key]:
            activity = {
                'S_No': form_fields.get(f'data[0].FormMGT7_Dtls[0].MainPage[0].SectionIITable[0].PrincipalBusinessActivity[0].{row_key}[0].Cell1[0]', ''),
                'Main_Activity_Group_Code': form_fields.get(f'data[0].FormMGT7_Dtls[0].MainPage[0].SectionIITable[0].PrincipalBusinessActivity[0].{row_key}[0].Cell2[0]', ''),
                'Description_Main_Activity_Group': form_fields.get(f'data[0].FormMGT7_Dtls[0].MainPage[0].SectionIITable[0].PrincipalBusinessActivity[0].{row_key}[0].Cell3[0]', ''),
                'Business_Activity_Code': form_fields.get(f'data[0].FormMGT7_Dtls[0].MainPage[0].SectionIITable[0].PrincipalBusinessActivity[0].{row_key}[0].Cell4[0]', ''),
                'Description_Business_Activity': form_fields.get(f'data[0].FormMGT7_Dtls[0].MainPage[0].SectionIITable[0].PrincipalBusinessActivity[0].{row_key}[0].Cell5[0]', ''),
                'Percentage_Turnover': form_fields.get(f'data[0].FormMGT7_Dtls[0].MainPage[0].SectionIITable[0].PrincipalBusinessActivity[0].{row_key}[0].Cell6[0]', '')
            }
            activities.append(activity)
        else:
            break  # No more rows found
    
    business_info['Activities'] = activities
    return business_info


def extract_mgt7_info(form_fields: Dict[str, str]) -> Dict[str, str]:
    """
    Extract information from MGT7 form fields.
    Args:
        form_fields: Dictionary of form fields
    Returns:
        Dictionary with extracted information
    """
    mgt7_info = {}
    
    # Company basic information
    mgt7_info['CIN'] = form_fields.get('data[0].FormMGT7_Dtls[0].MainPage[0].Page1[0].CIN[0]', '')
    mgt7_info['GLN'] = form_fields.get('data[0].FormMGT7_Dtls[0].MainPage[0].Page1[0].GLN[0]', '')
    mgt7_info['Company_Name'] = form_fields.get('data[0].FormMGT7_Dtls[0].MainPage[0].Page1[0].Name[0]', '')
    mgt7_info['Address'] = form_fields.get('data[0].FormMGT7_Dtls[0].MainPage[0].Page1[0].Address[0]', '')
    mgt7_info['Email'] = form_fields.get('data[0].FormMGT7_Dtls[0].MainPage[0].Page1[0].Email[0]', '')
    mgt7_info['Telephone'] = form_fields.get('data[0].FormMGT7_Dtls[0].MainPage[0].Page1[0].Telephone[0]', '')
    mgt7_info['Website'] = form_fields.get('data[0].FormMGT7_Dtls[0].MainPage[0].Page1[0].Website[0]', '')
    mgt7_info['Date_Of_Incorporation'] = form_fields.get('data[0].FormMGT7_Dtls[0].MainPage[0].Page1[0].DateOfIncorporation[0]', '')
    
    # Company type and category (decode abbreviations)
    type_code = form_fields.get('data[0].FormMGT7_Dtls[0].MainPage[0].Page1[0].CompanyDetailsTable[0].Row1[0].TypeOfCompany[0]', '')
    category_code = form_fields.get('data[0].FormMGT7_Dtls[0].MainPage[0].Page1[0].CompanyDetailsTable[0].Row1[0].Category[0]', '')
    subcategory_code = form_fields.get('data[0].FormMGT7_Dtls[0].MainPage[0].Page1[0].CompanyDetailsTable[0].Row1[0].SubCategory[0]', '')
    
    mgt7_info['Type_Of_Company'] = decode_form_values(type_code, 'type')
    mgt7_info['Category'] = decode_form_values(category_code, 'category')
    mgt7_info['Sub_Category'] = decode_form_values(subcategory_code, 'subcategory')
    
    # Share capital and stock exchange (decode yes/no values)
    share_capital_code = form_fields.get('data[0].FormMGT7_Dtls[0].MainPage[0].Page1[0].SharedCapital_R[0]', '')
    stock_exchange_code = form_fields.get('data[0].FormMGT7_Dtls[0].MainPage[0].Page1[0].StockExchange[0]', '')
    
    mgt7_info['Share_Capital'] = decode_form_values(share_capital_code, 'yes_no')
    mgt7_info['Stock_Exchange'] = decode_form_values(stock_exchange_code, 'yes_no')
    
    # Extract business activities
    mgt7_info['Business_Activities'] = extract_business_activities(form_fields)
    
    return mgt7_info


def extract_aoc4_info(form_fields: Dict[str, str]) -> Dict[str, str]:
    """
    Extract information from AOC4 form fields.
    Args:
        form_fields: Dictionary of form fields
    Returns:
        Dictionary with extracted information
    """
    aoc4_info = {}
    
    # Company basic information
    aoc4_info['CIN'] = form_fields.get('data[0].FormAOC4_Dtls[0].Segment1_PartA[0].CIN_C[0]', '')
    aoc4_info['From_Date'] = form_fields.get('data[0].FormAOC4_Dtls[0].Segment1_PartA[0].FromDate[0]', '')
    aoc4_info['To_Date'] = form_fields.get('data[0].FormAOC4_Dtls[0].Segment1_PartA[0].ToDate[0]', '')
    
    # Financial year
    if aoc4_info['From_Date'] and aoc4_info['To_Date']:
        aoc4_info['Financial_Year'] = f"{aoc4_info['From_Date']} to {aoc4_info['To_Date']}"
    else:
        aoc4_info['Financial_Year'] = ''
    
    return aoc4_info


def process_pdf(pdf_path: str) -> Tuple[Optional[str], Optional[str], Dict[str, str], str]:
    """
    Process a single PDF file and extract required information using PyPDF2.
    Args:
        pdf_path: Path to PDF file
    Returns:
        Tuple of (CIN, financial year, extracted info, form type)
    """
    try:
        # Get form fields
        form_fields = get_form_fields(pdf_path)
        
        # Detect form type
        form_type = detect_form_type(form_fields)
        
        cin = None
        financial_year = None
        extracted_info = {}
        
        if form_type == 'MGT7':
            extracted_info = extract_mgt7_info(form_fields)
            cin = extracted_info.get('CIN')
            # MGT7 doesn't have financial year in the same format, use date of incorporation
            financial_year = extracted_info.get('Date_Of_Incorporation')
            
        elif form_type == 'AOC4':
            extracted_info = extract_aoc4_info(form_fields)
            cin = extracted_info.get('CIN')
            financial_year = extracted_info.get('Financial_Year')
        
        # If not found in form fields, fall back to text extraction
        if not cin or not financial_year:
            text = extract_text_from_pdf(pdf_path)
            if not cin:
                cin = extract_cin(text)
            if not financial_year:
                financial_year = extract_financial_year(text)
        
        return cin, financial_year, extracted_info, form_type
        
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None, None, {}, 'UNKNOWN'


def print_mgt7_info(extracted_info: Dict[str, str]):
    """Print MGT7 form information in a formatted way."""
    print("\n=== MGT7 FORM - REGISTRATION AND OTHER DETAILS ===")
    
    # Company identification
    print(f"(i) Corporate Identification Number (CIN): {extracted_info.get('CIN', 'Not found')}")
    print(f"    Global Location Number (GLN): {extracted_info.get('GLN', 'Not found')}")
    
    # Company details
    print(f"(ii) (a) Name of the company: {extracted_info.get('Company_Name', 'Not found')}")
    print(f"     (b) Registered office address:")
    address = extracted_info.get('Address', 'Not found')
    if address != 'Not found':
        # Format address for better readability
        formatted_address = address.replace('\r', '\n        ')
        print(f"        {formatted_address}")
    else:
        print(f"        {address}")
    
    # Contact information
    print(f"     (c) e-mail ID of the company: {extracted_info.get('Email', 'Not found')}")
    print(f"     (d) Telephone number with STD code: {extracted_info.get('Telephone', 'Not found')}")
    print(f"     (e) Website: {extracted_info.get('Website', 'Not found')}")
    
    # Incorporation date
    print(f"(iii) Date of Incorporation: {extracted_info.get('Date_Of_Incorporation', 'Not found')}")
    
    # Company classification
    print(f"(iv) Type of the Company: {extracted_info.get('Type_Of_Company', 'Not found')}")
    print(f"     Category of the Company: {extracted_info.get('Category', 'Not found')}")
    print(f"     Sub-category of the Company: {extracted_info.get('Sub_Category', 'Not found')}")
    
    # Share capital and listing
    share_capital = extracted_info.get('Share_Capital', 'Not found')
    stock_exchange = extracted_info.get('Stock_Exchange', 'Not found')
    print(f"(v) Whether company is having share capital: {share_capital}")
    print(f"(vi) Whether shares listed on recognized Stock Exchange(s): {stock_exchange}")
    
    # Principal Business Activities
    business_activities = extracted_info.get('Business_Activities', {})
    if business_activities:
        print("\n=== II. PRINCIPAL BUSINESS ACTIVITIES OF THE COMPANY ===")
        
        num_activities = business_activities.get('Number_Of_Activities', 'Not found')
        print(f"Number of business activities: {num_activities}")
        
        activities = business_activities.get('Activities', [])
        if activities:
            print("\n{:<5} {:<10} {:<35} {:<15} {:<45} {:<12}".format(
                "S.No", "Main", "Description of Main Activity", "Business", "Description of Business Activity", "% of"
            ))
            print("{:<5} {:<10} {:<35} {:<15} {:<45} {:<12}".format(
                "", "Activity", "group", "Activity", "", "turnover"
            ))
            print("{:<5} {:<10} {:<35} {:<15} {:<45} {:<12}".format(
                "", "group code", "", "Code", "", "of the"
            ))
            print("{:<5} {:<10} {:<35} {:<15} {:<45} {:<12}".format(
                "", "", "", "", "", "company"
            ))
            print("-" * 132)
            
            for activity in activities:
                s_no = activity.get('S_No', '')
                main_code = activity.get('Main_Activity_Group_Code', '')
                main_desc = activity.get('Description_Main_Activity_Group', '')
                business_code = activity.get('Business_Activity_Code', '')
                business_desc = activity.get('Description_Business_Activity', '')
                turnover = activity.get('Percentage_Turnover', '')
                
                # Truncate long descriptions for better formatting
                main_desc_short = main_desc[:33] + ".." if len(main_desc) > 35 else main_desc
                business_desc_short = business_desc[:43] + ".." if len(business_desc) > 45 else business_desc
                
                print("{:<5} {:<10} {:<35} {:<15} {:<45} {:<12}".format(
                    s_no, main_code, main_desc_short, business_code, business_desc_short, turnover
                ))
        else:
            print("No business activities found in form fields.")
    else:
        print("\n=== II. PRINCIPAL BUSINESS ACTIVITIES OF THE COMPANY ===")
        print("Business activities information not found.")


def transform_mgt7_to_json(extracted_info: Dict[str, str], pdf_filename: str = "") -> Dict[str, Any]:
    """
    Transform MGT7 extracted information into a structured JSON format 
    that's easy to identify and convert to CSV/table format.
    
    Args:
        extracted_info: Dictionary containing extracted MGT7 information
        pdf_filename: Name of the source PDF file (optional)
        
    Returns:
        Dictionary in JSON-ready format with flattened structure for easy CSV conversion
    """
    
    # Create the main JSON structure
    mgt7_json = {
        # File metadata
        "source_file": pdf_filename,
        "form_type": "MGT7",
        "extraction_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        
        # Basic company information
        "company_cin": extracted_info.get('CIN', ''),
        "company_gln": extracted_info.get('GLN', ''),
        "company_name": extracted_info.get('Company_Name', ''),
        "company_email": extracted_info.get('Email', ''),
        "company_telephone": extracted_info.get('Telephone', ''),
        "company_website": extracted_info.get('Website', ''),
        "date_of_incorporation": extracted_info.get('Date_Of_Incorporation', ''),
        
        # Company address (cleaned and formatted)
        "registered_office_address": _clean_address(extracted_info.get('Address', '')),
        
        # Company classification
        "company_type": extracted_info.get('Type_Of_Company', ''),
        "company_category": extracted_info.get('Category', ''),
        "company_subcategory": extracted_info.get('Sub_Category', ''),
        
        # Share capital and listing information
        "has_share_capital": extracted_info.get('Share_Capital', ''),
        "listed_on_stock_exchange": extracted_info.get('Stock_Exchange', ''),
        
        # Business activities summary
        "total_business_activities": 0,
        "business_activities": []
    }
    
    # Process business activities
    business_activities = extracted_info.get('Business_Activities', {})
    if business_activities:
        # Extract number of activities
        num_activities_str = business_activities.get('Number_Of_Activities', '0')
        try:
            mgt7_json["total_business_activities"] = int(num_activities_str) if num_activities_str.isdigit() else 0
        except:
            mgt7_json["total_business_activities"] = 0
        
        # Process individual activities
        activities = business_activities.get('Activities', [])
        for activity in activities:
            activity_data = {
                "serial_number": activity.get('S_No', ''),
                "main_activity_group_code": activity.get('Main_Activity_Group_Code', ''),
                "main_activity_description": activity.get('Description_Main_Activity_Group', ''),
                "business_activity_code": activity.get('Business_Activity_Code', ''),
                "business_activity_description": activity.get('Description_Business_Activity', ''),
                "percentage_turnover": _clean_percentage(activity.get('Percentage_Turnover', ''))
            }
            mgt7_json["business_activities"].append(activity_data)
    
    return mgt7_json


def _clean_address(address: str) -> str:
    """Clean and format address for JSON storage."""
    if not address:
        return ""
    # Remove carriage returns and normalize whitespace
    cleaned = address.replace('\r', ' ').replace('\n', ' ')
    # Remove multiple spaces
    cleaned = ' '.join(cleaned.split())
    return cleaned


def _clean_percentage(percentage: str) -> str:
    """Clean and validate percentage values."""
    if not percentage:
        return ""
    # Remove any extra spaces and ensure it's a valid percentage format
    cleaned = percentage.strip()
    # You could add more validation here if needed
    return cleaned


def save_mgt7_json(mgt7_json: Dict[str, Any], output_file: str) -> bool:
    """
    Save MGT7 JSON data to a file.
    
    Args:
        mgt7_json: MGT7 data in JSON format
        output_file: Path to output JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(mgt7_json, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON file {output_file}: {e}")
        return False


def mgt7_json_to_csv_rows(mgt7_json: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Convert MGT7 JSON to a list of flat dictionaries suitable for CSV export.
    Each business activity becomes a separate row.
    
    Args:
        mgt7_json: MGT7 data in JSON format
        
    Returns:
        List of dictionaries, each representing a CSV row
    """
    csv_rows = []
    
    # Base company information that will be repeated for each activity
    base_info = {
        "source_file": mgt7_json.get("source_file", ""),
        "form_type": mgt7_json.get("form_type", ""),
        "company_cin": mgt7_json.get("company_cin", ""),
        "company_gln": mgt7_json.get("company_gln", ""),
        "company_name": mgt7_json.get("company_name", ""),
        "company_email": mgt7_json.get("company_email", ""),
        "company_telephone": mgt7_json.get("company_telephone", ""),
        "company_website": mgt7_json.get("company_website", ""),
        "date_of_incorporation": mgt7_json.get("date_of_incorporation", ""),
        "registered_office_address": mgt7_json.get("registered_office_address", ""),
        "company_type": mgt7_json.get("company_type", ""),
        "company_category": mgt7_json.get("company_category", ""),
        "company_subcategory": mgt7_json.get("company_subcategory", ""),
        "has_share_capital": mgt7_json.get("has_share_capital", ""),
        "listed_on_stock_exchange": mgt7_json.get("listed_on_stock_exchange", ""),
        "total_business_activities": str(mgt7_json.get("total_business_activities", 0))
    }
    
    # If there are business activities, create one row per activity
    activities = mgt7_json.get("business_activities", [])
    if activities:
        for activity in activities:
            row = base_info.copy()
            row.update({
                "activity_serial_number": activity.get("serial_number", ""),
                "main_activity_group_code": activity.get("main_activity_group_code", ""),
                "main_activity_description": activity.get("main_activity_description", ""),
                "business_activity_code": activity.get("business_activity_code", ""),
                "business_activity_description": activity.get("business_activity_description", ""),
                "percentage_turnover": activity.get("percentage_turnover", "")
            })
            csv_rows.append(row)
    else:
        # If no activities, create a single row with company info only
        row = base_info.copy()
        row.update({
            "activity_serial_number": "",
            "main_activity_group_code": "",
            "main_activity_description": "",
            "business_activity_code": "",
            "business_activity_description": "",
            "percentage_turnover": ""
        })
        csv_rows.append(row)
    
    return csv_rows


def process_all_mgt7_to_json_csv(input_dir: str = "No_XBRL", output_json_dir: str = "No_XBRL_JSON", output_csv_file: str = "mgt7_combined_data.csv") -> Dict[str, int]:
    """
    Process all MGT7 PDFs and export to JSON and CSV formats.
    
    Args:
        input_dir: Directory containing PDF files
        output_json_dir: Directory to save individual JSON files
        output_csv_file: Path for combined CSV file
        
    Returns:
        Dictionary with processing statistics
    """
    
    stats = {
        "total_files": 0,
        "mgt7_files": 0,
        "json_saved": 0,
        "csv_rows": 0,
        "errors": 0
    }
    
    # Create output directories
    os.makedirs(output_json_dir, exist_ok=True)
    
    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Directory '{input_dir}' does not exist")
        return stats
    
    # Get all PDF files
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    stats["total_files"] = len(pdf_files)
    
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return stats
    
    print(f"Processing {len(pdf_files)} PDF files for MGT7 JSON/CSV export...")
    
    # Collect all CSV rows for combined CSV
    all_csv_rows = []
    
    # Process each PDF file
    for pdf_file in pdf_files:
        try:
            pdf_path = os.path.join(input_dir, pdf_file)
            cin, financial_year, extracted_info, form_type = process_pdf(pdf_path)
            
            if form_type == 'MGT7' and extracted_info:
                stats["mgt7_files"] += 1
                
                # Transform to JSON
                mgt7_json = transform_mgt7_to_json(extracted_info, pdf_file)
                
                # Save individual JSON file
                json_filename = pdf_file.replace('.pdf', '_mgt7.json')
                json_path = os.path.join(output_json_dir, json_filename)
                
                if save_mgt7_json(mgt7_json, json_path):
                    stats["json_saved"] += 1
                    print(f"✓ JSON saved: {json_filename}")
                else:
                    stats["errors"] += 1
                    print(f"✗ Failed to save JSON: {json_filename}")
                
                # Convert to CSV rows
                csv_rows = mgt7_json_to_csv_rows(mgt7_json)
                all_csv_rows.extend(csv_rows)
                stats["csv_rows"] += len(csv_rows)
                
        except Exception as e:
            stats["errors"] += 1
            print(f"✗ Error processing {pdf_file}: {e}")
    
    # Save combined CSV file
    if all_csv_rows:
        try:
            with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = all_csv_rows[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_csv_rows)
            print(f"✓ Combined CSV saved: {output_csv_file} ({len(all_csv_rows)} rows)")
        except Exception as e:
            stats["errors"] += 1
            print(f"✗ Failed to save CSV: {e}")
    
    # Print summary
    print("\n=== PROCESSING SUMMARY ===")
    print(f"Total PDF files processed: {stats['total_files']}")
    print(f"MGT7 forms found: {stats['mgt7_files']}")
    print(f"JSON files saved: {stats['json_saved']}")
    print(f"CSV rows generated: {stats['csv_rows']}")
    print(f"Errors encountered: {stats['errors']}")
    
    return stats


def print_aoc4_info(extracted_info: Dict[str, str]):
    """Print AOC4 form information in a formatted way."""
    print("\n=== AOC4 FORM - FINANCIAL INFORMATION ===")
    print(f"CIN: {extracted_info.get('CIN', 'Not found')}")
    print(f"Financial Year: {extracted_info.get('Financial_Year', 'Not found')}")
    print(f"From Date: {extracted_info.get('From_Date', 'Not found')}")
    print(f"To Date: {extracted_info.get('To_Date', 'Not found')}")


def main():
    """
    Main function with options for different processing modes.
    """
    print("=== PDF Information Extractor ===")
    print("1. Display mode: Show detailed information for each PDF")
    print("2. Export mode: Export all MGT7 data to JSON and CSV")
    print("3. Both modes: Display and export")
    
    while True:
        choice = input("\nSelect mode (1, 2, 3, or 'q' to quit): ").strip()
        
        if choice.lower() == 'q':
            return
        elif choice in ['1', '2', '3']:
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 'q'.")
    
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
    
    print(f"\nFound {len(pdf_files)} PDF files to process")
    
    # Export mode (options 2 or 3)
    if choice in ['2', '3']:
        print("\n" + "="*60)
        print("EXPORT MODE: Processing all MGT7 files for JSON/CSV export")
        print("="*60)
        stats = process_all_mgt7_to_json_csv()
        
        if choice == '2':  # Export only mode
            return
    
    # Display mode (options 1 or 3)
    if choice in ['1', '3']:
        print("\n" + "="*60)
        print("DISPLAY MODE: Showing detailed information for each PDF")
        print("="*60)
        
        # Process each PDF file for display
        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_dir, pdf_file)
            cin, financial_year, extracted_info, form_type = process_pdf(pdf_path)
            
            print(f"\n{'='*60}")
            print(f"File: {pdf_file}")
            print(f"Form Type: {form_type}")
            print(f"CIN: {cin if cin else 'Not found'}")
            print(f"Financial Year/Date: {financial_year if financial_year else 'Not found'}")
            
            # Display detailed information based on form type
            if form_type == 'MGT7' and extracted_info:
                print_mgt7_info(extracted_info)
                
                # Show a sample of the JSON structure
                mgt7_json = transform_mgt7_to_json(extracted_info, pdf_file)
                print("\n=== JSON TRANSFORMATION SAMPLE ===")
                print("Company Information:")
                print(f"  CIN: {mgt7_json['company_cin']}")
                print(f"  Name: {mgt7_json['company_name']}")
                print(f"  Type: {mgt7_json['company_type']}")
                print(f"  Total Activities: {mgt7_json['total_business_activities']}")
                
                if mgt7_json['business_activities']:
                    print("  Business Activities:")
                    for i, activity in enumerate(mgt7_json['business_activities'][:2], 1):  # Show first 2 activities
                        print(f"    {i}. {activity['main_activity_description']} ({activity['percentage_turnover']}% turnover)")
                    if len(mgt7_json['business_activities']) > 2:
                        print(f"    ... and {len(mgt7_json['business_activities']) - 2} more activities")
                
                # Demonstrate CSV-ready format
                csv_rows = mgt7_json_to_csv_rows(mgt7_json)
                print(f"\nCSV Format: Ready for export with {len(csv_rows)} rows")
                
            elif form_type == 'AOC4' and extracted_info:
                print_aoc4_info(extracted_info)
            elif form_type == 'UNKNOWN':
                print("\nForm type could not be determined. No structured data extracted.")
            
            print(f"{'='*60}")


if __name__ == "__main__":
    main()