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
    Detect whether the PDF is MGT7, AOC4, or PAC form based on form fields.
    Args:
        form_fields: Dictionary of form fields
    Returns:
        Form type: 'MGT7', 'AOC4', 'PAC', or 'UNKNOWN'
    """
    # Check for form type based on field patterns
    for field_name in form_fields.keys():
        if 'FormMGT7' in field_name:
            return 'MGT7'
        elif 'FormAOC4' in field_name:
            return 'AOC4'
        elif 'Form2_Dtls' in field_name:
            return 'PAC'
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


def extract_pac_info(form_fields: Dict[str, str]) -> Dict[str, str]:
    """
    Extract information from PAC (Private Allotment Certificate) form fields.
    Args:
        form_fields: Dictionary of form fields
    Returns:
        Dictionary with extracted information
    """
    pac_info = {}
    
    # Company basic information
    pac_info['CIN'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].Page1[0].CIN_C[0]', '')
    pac_info['GLN'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].Page1[0].GLN_C[0]', '')
    pac_info['Company_Name'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].Page1[0].CompanyName_C[0]', '')
    pac_info['Company_Address'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].Page1[0].CompanyAdd_C[0]', '')
    pac_info['Email'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].Page1[0].Email_C[0]', '')
    
    # Form language
    form_language = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].Page1[0].FormLanguage[0]', '')
    pac_info['Form_Language'] = 'English' if form_language == '/ENGL' else form_language
    
    # Company classification
    pac_info['Company_Class'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].Page1[0].hiddencompanyclass[0]', '')
    
    # Allotment information
    pac_info['Number_Of_Allotments'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].Heading1[0].NumOfAllotmnt_N[0]', '')
    
    # First allotment details
    allotment_info = {}
    allotment_info['Date_Of_Allotment'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DateAllotment_D[0]', '')
    allotment_info['Date_Of_Passing_Resolution'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].Date_D[0]', '')
    allotment_info['SRN'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].SRN_C[0]', '')
    
    # Preference shares details
    preference_shares = {}
    preference_shares['Number_Of_Shares'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefNumShares_N[0]', '')
    preference_shares['Nominal_Amount_Per_Share'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefPerNom_N[0]', '')
    preference_shares['Total_Nominal_Amount'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefTotNom_N[0]', '')
    preference_shares['Amount_Paid_Per_Share'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefPerShare_N[0]', '')
    preference_shares['Total_Amount_Paid'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefTotApp_N[0]', '')
    preference_shares['Amount_Due_Per_Share'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefPerAllot_N[0]', '')
    preference_shares['Total_Amount_Due'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefTotAllot_N[0]', '')
    preference_shares['Premium_Per_Share'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefPerPremiumDue_N[0]', '')
    preference_shares['Total_Premium_Amount'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefTotPremDue_N[0]', '')
    preference_shares['Premium_Paid_Per_Share'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefPerPremium_N[0]', '')
    preference_shares['Total_Premium_Paid'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefTotPremium_N[0]', '')
    preference_shares['Discount_Per_Share'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefPerDisc_N[0]', '')
    preference_shares['Total_Discount'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefTotDisc_N[0]', '')
    preference_shares['Amount_To_Be_Paid_Per_Share'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefAmtToBePaid_N[0]', '')
    preference_shares['Total_Amount_To_Be_Paid'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefTotalAmtToBePaid_N[0]', '')
    preference_shares['Particulars'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefParticulars[0]', '')
    
    # Equity shares details
    equity_shares = {}
    equity_shares['Number_Of_Shares'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqNumShares_N[0]', '')
    equity_shares['Nominal_Amount_Per_Share'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerNom_N[0]', '')
    equity_shares['Total_Nominal_Amount'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotNom_N[0]', '')
    equity_shares['Amount_Paid_Per_Share'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerShare_N[0]', '')
    equity_shares['Total_Amount_Paid'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotApp_N[0]', '')
    equity_shares['Amount_Due_Per_Share'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerAllot_N[0]', '')
    equity_shares['Total_Amount_Due'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotAllot_N[0]', '')
    equity_shares['Premium_Per_Share'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerPremiumDue_N[0]', '')
    equity_shares['Total_Premium_Amount'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotPremDue_N[0]', '')
    equity_shares['Premium_Paid_Per_Share'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerPremium_N[0]', '')
    equity_shares['Total_Premium_Paid'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotPremium_N[0]', '')
    equity_shares['Discount_Per_Share'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerDisc_N[0]', '')
    equity_shares['Total_Discount'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotDisc_N[0]', '')
    equity_shares['Amount_To_Be_Paid_Per_Share'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqAmtToBePaid_N[0]', '')
    equity_shares['Total_Amount_To_Be_Paid'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotalAmtToBePaid_N[0]', '')
    equity_shares['Particulars'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqParticulars[0]', '')
    
    # Capital structure information
    capital_structure = {}
    
    # Authorized capital
    capital_structure['Authorized_Capital_Total'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].Cap_Authrsd[0]', '')
    capital_structure['Authorized_Equity_Shares_Number'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumAuthSharesEq_N[0]', '')
    capital_structure['Authorized_Equity_Shares_Value'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValAuthEq_N[0]', '')
    capital_structure['Authorized_Equity_Nominal_Amount'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalAmtAuthPEqS[0]', '')
    capital_structure['Authorized_Preference_Shares_Number'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumSharesAuthPref_N[0]', '')
    capital_structure['Authorized_Preference_Shares_Value'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValAuthPref_N[0]', '')
    capital_structure['Authorized_Preference_Nominal_Amount'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalAmtAuthPPrfS[0]', '')
    capital_structure['Authorized_Unclassified_Shares_Number'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumSharesUnclassiedf_N[0]', '')
    capital_structure['Authorized_Unclassified_Shares_Value'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValUnclassifiedf_N[0]', '')
    
    # Issued capital
    capital_structure['Issued_Capital_Total'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CapIssuOfCompany[0]', '')
    capital_structure['Issued_Equity_Shares_Number'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumIssSharesEq_N[0]', '')
    capital_structure['Issued_Equity_Shares_Value'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValIssueEq_N[0]', '')
    capital_structure['Issued_Equity_Nominal_Amount'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalIssuAmtPEqS[0]', '')
    capital_structure['Issued_Preference_Shares_Number'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumSharesIssPref_N[0]', '')
    capital_structure['Issued_Preference_Shares_Value'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValIssPref_N[0]', '')
    capital_structure['Issued_Preference_Nominal_Amount'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalAmtIssPPrfS[0]', '')
    
    # Subscribed capital
    capital_structure['Subscribed_Capital_Total'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CapSubscrbCapOfCompany[0]', '')
    capital_structure['Subscribed_Equity_Shares_Number'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumSharesSubEq1_N[0]', '')
    capital_structure['Subscribed_Equity_Shares_Value'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValSubEq1_N[0]', '')
    capital_structure['Subscribed_Equity_Nominal_Amount'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalAmtSubPEqS[0]', '')
    capital_structure['Subscribed_Preference_Shares_Number'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumSharesSubPref1_N[0]', '')
    capital_structure['Subscribed_Preference_Shares_Value'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValSubPref1_N[0]', '')
    capital_structure['Subscribed_Preference_Nominal_Amount'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalAmtSubPPrfS[0]', '')
    
    # Paid-up capital
    capital_structure['Paid_Up_Capital_Total'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CapPaidUpOfCompany[0]', '')
    capital_structure['Paid_Up_Equity_Shares_Number'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumSharesPaidEq_N[0]', '')
    capital_structure['Paid_Up_Equity_Shares_Value'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValPaidEq_N[0]', '')
    capital_structure['Paid_Up_Equity_Nominal_Amount'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalAmtPaidPEqS[0]', '')
    capital_structure['Paid_Up_Preference_Shares_Number'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumSharesPaidPref_N[0]', '')
    capital_structure['Paid_Up_Preference_Shares_Value'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValPaidPref_N[0]', '')
    capital_structure['Paid_Up_Preference_Nominal_Amount'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalAmtPaidPPrfS[0]', '')
    
    # Bonus shares information
    capital_structure['Date_Of_Allotment_Bonus'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].DateAllotment_D[0]', '')
    capital_structure['Date_Of_Passing_Resolution_Bonus'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].Date_D[0]', '')
    capital_structure['SRN_Bonus'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].SRN_C[0]', '')
    capital_structure['Number_Of_Bonus_Shares'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumBonus_N[0]', '')
    capital_structure['Nominal_Amount_Bonus_Shares'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalBonus_N[0]', '')
    capital_structure['Paid_Up_Amount_Bonus_Shares'] = form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].PaidUpBonus_N[0]', '')
    
    # Allotment categories (checkboxes)
    capital_structure['Allotment_To_Employees'] = 'Yes' if form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CBEmp[0]', '') else 'No'
    capital_structure['Allotment_To_Existing_Shareholders'] = 'Yes' if form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CBExistShrHldr[0]', '') == '/ESHR' else 'No'
    capital_structure['Allotment_To_Directors'] = 'Yes' if form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CBDir[0]', '') else 'No'
    capital_structure['Allotment_To_Buyers'] = 'Yes' if form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CBBuyer[0]', '') else 'No'
    capital_structure['Allotment_To_Others'] = 'Yes' if form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CBOthers[0]', '') == '/OTHR' else 'No'
    
    # Compliance checkboxes
    capital_structure['All_Securities_Allotted'] = 'Yes' if form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CB11b1[0]', '') == '/ALLSEC' else 'No'
    capital_structure['Offer_Securities_To_Public'] = 'Yes' if form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CB11b3[0]', '') == '/OFFSEC' else 'No'
    capital_structure['Compliance_With_Allotment'] = 'Yes' if form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CB11b4[0]', '') == '/COMALL' else 'No'
    capital_structure['Money_Received_Against_Allotment'] = 'Yes' if form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CB11b5[0]', '') == '/RECMON' else 'No'
    capital_structure['Offer_In_Company_Name'] = 'Yes' if form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CB11b6[0]', '') == '/OFFNAME' else 'No'
    capital_structure['Offer_Account_Opened'] = 'Yes' if form_fields.get('data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CB11b7[0]', '') == '/OFFACC' else 'No'
    
    # Add structured data to main info
    pac_info['Allotment_Details'] = allotment_info
    pac_info['Preference_Shares'] = preference_shares
    pac_info['Equity_Shares'] = equity_shares
    pac_info['Capital_Structure'] = capital_structure
    
    return pac_info


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
            
        elif form_type == 'PAC':
            extracted_info = extract_pac_info(form_fields)
            cin = extracted_info.get('CIN')
            # PAC forms use allotment date as the reference date
            allotment_details = extracted_info.get('Allotment_Details', {})
            financial_year = allotment_details.get('Date_Of_Allotment', '')
        
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


def transform_pac_to_json(extracted_info: Dict[str, str], pdf_filename: str = "") -> Dict[str, Any]:
    """
    Transform PAC extracted information into a structured JSON format.
    
    Args:
        extracted_info: Dictionary containing extracted PAC information
        pdf_filename: Name of the source PDF file (optional)
        
    Returns:
        Dictionary in JSON-ready format
    """
    
    # Create the main JSON structure
    pac_json = {
        # File metadata
        "source_file": pdf_filename,
        "form_type": "PAC",
        "extraction_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        
        # Basic company information
        "company_cin": extracted_info.get('CIN', ''),
        "company_gln": extracted_info.get('GLN', ''),
        "company_name": extracted_info.get('Company_Name', ''),
        "company_email": extracted_info.get('Email', ''),
        "company_address": _clean_address(extracted_info.get('Company_Address', '')),
        "company_class": extracted_info.get('Company_Class', ''),
        "form_language": extracted_info.get('Form_Language', ''),
        
        # Allotment information
        "number_of_allotments": _safe_int_convert(extracted_info.get('Number_Of_Allotments', '')),
        
        # Allotment details
        "allotment_details": {},
        
        # Securities information
        "preference_shares": {},
        "equity_shares": {},
        "debentures": {},
        "warrants_or_other_securities": {},
        
        # Capital structure information
        "capital_structure": {}
    }
    
    # Process allotment details
    allotment_details = extracted_info.get('Allotment_Details', {})
    if allotment_details:
        pac_json["allotment_details"] = {
            "date_of_allotment": allotment_details.get('Date_Of_Allotment', ''),
            "date_of_passing_resolution": allotment_details.get('Date_Of_Passing_Resolution', ''),
            "srn_mgt14": allotment_details.get('SRN', '')
        }
    
    # Process preference shares
    preference_shares = extracted_info.get('Preference_Shares', {})
    if preference_shares and any(preference_shares.values()):
        pac_json["preference_shares"] = {
            "number_of_shares": _safe_int_convert(preference_shares.get('Number_Of_Shares', '')),
            "nominal_amount_per_share": _safe_float_convert(preference_shares.get('Nominal_Amount_Per_Share', '')),
            "total_nominal_amount": _safe_float_convert(preference_shares.get('Total_Nominal_Amount', '')),
            "amount_paid_per_share": _safe_float_convert(preference_shares.get('Amount_Paid_Per_Share', '')),
            "total_amount_paid": _safe_float_convert(preference_shares.get('Total_Amount_Paid', '')),
            "amount_due_per_share": _safe_float_convert(preference_shares.get('Amount_Due_Per_Share', '')),
            "total_amount_due": _safe_float_convert(preference_shares.get('Total_Amount_Due', '')),
            "premium_per_share": _safe_float_convert(preference_shares.get('Premium_Per_Share', '')),
            "total_premium_amount": _safe_float_convert(preference_shares.get('Total_Premium_Amount', '')),
            "premium_paid_per_share": _safe_float_convert(preference_shares.get('Premium_Paid_Per_Share', '')),
            "total_premium_paid": _safe_float_convert(preference_shares.get('Total_Premium_Paid', '')),
            "discount_per_share": _safe_float_convert(preference_shares.get('Discount_Per_Share', '')),
            "total_discount": _safe_float_convert(preference_shares.get('Total_Discount', '')),
            "amount_to_be_paid_per_share": _safe_float_convert(preference_shares.get('Amount_To_Be_Paid_Per_Share', '')),
            "total_amount_to_be_paid": _safe_float_convert(preference_shares.get('Total_Amount_To_Be_Paid', '')),
            "particulars": preference_shares.get('Particulars', '')
        }
    
    # Process equity shares
    equity_shares = extracted_info.get('Equity_Shares', {})
    if equity_shares and any(equity_shares.values()):
        pac_json["equity_shares"] = {
            "number_of_shares": _safe_int_convert(equity_shares.get('Number_Of_Shares', '')),
            "nominal_amount_per_share": _safe_float_convert(equity_shares.get('Nominal_Amount_Per_Share', '')),
            "total_nominal_amount": _safe_float_convert(equity_shares.get('Total_Nominal_Amount', '')),
            "amount_paid_per_share": _safe_float_convert(equity_shares.get('Amount_Paid_Per_Share', '')),
            "total_amount_paid": _safe_float_convert(equity_shares.get('Total_Amount_Paid', '')),
            "amount_due_per_share": _safe_float_convert(equity_shares.get('Amount_Due_Per_Share', '')),
            "total_amount_due": _safe_float_convert(equity_shares.get('Total_Amount_Due', '')),
            "premium_per_share": _safe_float_convert(equity_shares.get('Premium_Per_Share', '')),
            "total_premium_amount": _safe_float_convert(equity_shares.get('Total_Premium_Amount', '')),
            "premium_paid_per_share": _safe_float_convert(equity_shares.get('Premium_Paid_Per_Share', '')),
            "total_premium_paid": _safe_float_convert(equity_shares.get('Total_Premium_Paid', '')),
            "discount_per_share": _safe_float_convert(equity_shares.get('Discount_Per_Share', '')),
            "total_discount": _safe_float_convert(equity_shares.get('Total_Discount', '')),
            "amount_to_be_paid_per_share": _safe_float_convert(equity_shares.get('Amount_To_Be_Paid_Per_Share', '')),
            "total_amount_to_be_paid": _safe_float_convert(equity_shares.get('Total_Amount_To_Be_Paid', '')),
            "particulars": equity_shares.get('Particulars', '')
        }
    
    # Process capital structure
    capital_structure = extracted_info.get('Capital_Structure', {})
    if capital_structure and any(capital_structure.values()):
        pac_json["capital_structure"] = {
            # Authorized capital
            "authorized_capital_total": _safe_float_convert(capital_structure.get('Authorized_Capital_Total', '')),
            "authorized_equity_shares_number": _safe_int_convert(capital_structure.get('Authorized_Equity_Shares_Number', '')),
            "authorized_equity_shares_value": _safe_float_convert(capital_structure.get('Authorized_Equity_Shares_Value', '')),
            "authorized_equity_nominal_amount": capital_structure.get('Authorized_Equity_Nominal_Amount', ''),
            "authorized_preference_shares_number": _safe_int_convert(capital_structure.get('Authorized_Preference_Shares_Number', '')),
            "authorized_preference_shares_value": _safe_float_convert(capital_structure.get('Authorized_Preference_Shares_Value', '')),
            "authorized_preference_nominal_amount": capital_structure.get('Authorized_Preference_Nominal_Amount', ''),
            "authorized_unclassified_shares_number": _safe_int_convert(capital_structure.get('Authorized_Unclassified_Shares_Number', '')),
            "authorized_unclassified_shares_value": _safe_float_convert(capital_structure.get('Authorized_Unclassified_Shares_Value', '')),
            
            # Issued capital
            "issued_capital_total": _safe_float_convert(capital_structure.get('Issued_Capital_Total', '')),
            "issued_equity_shares_number": _safe_int_convert(capital_structure.get('Issued_Equity_Shares_Number', '')),
            "issued_equity_shares_value": _safe_float_convert(capital_structure.get('Issued_Equity_Shares_Value', '')),
            "issued_equity_nominal_amount": capital_structure.get('Issued_Equity_Nominal_Amount', ''),
            "issued_preference_shares_number": _safe_int_convert(capital_structure.get('Issued_Preference_Shares_Number', '')),
            "issued_preference_shares_value": _safe_float_convert(capital_structure.get('Issued_Preference_Shares_Value', '')),
            "issued_preference_nominal_amount": capital_structure.get('Issued_Preference_Nominal_Amount', ''),
            
            # Subscribed capital
            "subscribed_capital_total": _safe_float_convert(capital_structure.get('Subscribed_Capital_Total', '')),
            "subscribed_equity_shares_number": _safe_int_convert(capital_structure.get('Subscribed_Equity_Shares_Number', '')),
            "subscribed_equity_shares_value": _safe_float_convert(capital_structure.get('Subscribed_Equity_Shares_Value', '')),
            "subscribed_equity_nominal_amount": capital_structure.get('Subscribed_Equity_Nominal_Amount', ''),
            "subscribed_preference_shares_number": _safe_int_convert(capital_structure.get('Subscribed_Preference_Shares_Number', '')),
            "subscribed_preference_shares_value": _safe_float_convert(capital_structure.get('Subscribed_Preference_Shares_Value', '')),
            "subscribed_preference_nominal_amount": capital_structure.get('Subscribed_Preference_Nominal_Amount', ''),
            
            # Paid-up capital
            "paid_up_capital_total": _safe_float_convert(capital_structure.get('Paid_Up_Capital_Total', '')),
            "paid_up_equity_shares_number": _safe_int_convert(capital_structure.get('Paid_Up_Equity_Shares_Number', '')),
            "paid_up_equity_shares_value": _safe_float_convert(capital_structure.get('Paid_Up_Equity_Shares_Value', '')),
            "paid_up_equity_nominal_amount": capital_structure.get('Paid_Up_Equity_Nominal_Amount', ''),
            "paid_up_preference_shares_number": _safe_int_convert(capital_structure.get('Paid_Up_Preference_Shares_Number', '')),
            "paid_up_preference_shares_value": _safe_float_convert(capital_structure.get('Paid_Up_Preference_Shares_Value', '')),
            "paid_up_preference_nominal_amount": capital_structure.get('Paid_Up_Preference_Nominal_Amount', ''),
            
            # Bonus shares
            "date_of_allotment_bonus": capital_structure.get('Date_Of_Allotment_Bonus', ''),
            "date_of_passing_resolution_bonus": capital_structure.get('Date_Of_Passing_Resolution_Bonus', ''),
            "srn_bonus": capital_structure.get('SRN_Bonus', ''),
            "number_of_bonus_shares": _safe_int_convert(capital_structure.get('Number_Of_Bonus_Shares', '')),
            "nominal_amount_bonus_shares": _safe_float_convert(capital_structure.get('Nominal_Amount_Bonus_Shares', '')),
            "paid_up_amount_bonus_shares": _safe_float_convert(capital_structure.get('Paid_Up_Amount_Bonus_Shares', '')),
            
            # Allotment categories
            "allotment_to_employees": capital_structure.get('Allotment_To_Employees', 'No') == 'Yes',
            "allotment_to_existing_shareholders": capital_structure.get('Allotment_To_Existing_Shareholders', 'No') == 'Yes',
            "allotment_to_directors": capital_structure.get('Allotment_To_Directors', 'No') == 'Yes',
            "allotment_to_buyers": capital_structure.get('Allotment_To_Buyers', 'No') == 'Yes',
            "allotment_to_others": capital_structure.get('Allotment_To_Others', 'No') == 'Yes',
            
            # Compliance checkboxes
            "all_securities_allotted": capital_structure.get('All_Securities_Allotted', 'No') == 'Yes',
            "offer_securities_to_public": capital_structure.get('Offer_Securities_To_Public', 'No') == 'Yes',
            "compliance_with_allotment": capital_structure.get('Compliance_With_Allotment', 'No') == 'Yes',
            "money_received_against_allotment": capital_structure.get('Money_Received_Against_Allotment', 'No') == 'Yes',
            "offer_in_company_name": capital_structure.get('Offer_In_Company_Name', 'No') == 'Yes',
            "offer_account_opened": capital_structure.get('Offer_Account_Opened', 'No') == 'Yes'
        }
    
    return pac_json


def _safe_int_convert(value: str) -> int:
    """Safely convert string to integer, return 0 if conversion fails."""
    if not value or not value.strip():
        return 0
    try:
        return int(float(value.strip()))
    except (ValueError, TypeError):
        return 0


def _safe_float_convert(value: str) -> float:
    """Safely convert string to float, return 0.0 if conversion fails."""
    if not value or not value.strip():
        return 0.0
    try:
        return float(value.strip())
    except (ValueError, TypeError):
        return 0.0


def save_pac_json(pac_json: Dict[str, Any], output_file: str) -> bool:
    """
    Save PAC JSON data to a file.
    
    Args:
        pac_json: PAC data in JSON format
        output_file: Path to output JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(pac_json, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON file {output_file}: {e}")
        return False


def pac_json_to_csv_rows(pac_json: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Convert PAC JSON to a list of flat dictionaries suitable for CSV export.
    
    Args:
        pac_json: PAC data in JSON format
        
    Returns:
        List of dictionaries, each representing a CSV row
    """
    csv_rows = []
    
    # Base company information
    base_info = {
        "source_file": pac_json.get("source_file", ""),
        "form_type": pac_json.get("form_type", ""),
        "extraction_timestamp": pac_json.get("extraction_timestamp", ""),
        "company_cin": pac_json.get("company_cin", ""),
        "company_gln": pac_json.get("company_gln", ""),
        "company_name": pac_json.get("company_name", ""),
        "company_email": pac_json.get("company_email", ""),
        "company_address": pac_json.get("company_address", ""),
        "company_class": pac_json.get("company_class", ""),
        "form_language": pac_json.get("form_language", ""),
        "number_of_allotments": str(pac_json.get("number_of_allotments", 0))
    }
    
    # Allotment details
    allotment_details = pac_json.get("allotment_details", {})
    base_info.update({
        "date_of_allotment": allotment_details.get("date_of_allotment", ""),
        "date_of_passing_resolution": allotment_details.get("date_of_passing_resolution", ""),
        "srn_mgt14": allotment_details.get("srn_mgt14", "")
    })
    
    # Capital structure details
    capital_structure = pac_json.get("capital_structure", {})
    base_info.update({
        "authorized_capital_total": str(capital_structure.get("authorized_capital_total", 0.0)),
        "authorized_equity_shares_number": str(capital_structure.get("authorized_equity_shares_number", 0)),
        "authorized_preference_shares_number": str(capital_structure.get("authorized_preference_shares_number", 0)),
        "issued_capital_total": str(capital_structure.get("issued_capital_total", 0.0)),
        "issued_equity_shares_number": str(capital_structure.get("issued_equity_shares_number", 0)),
        "issued_preference_shares_number": str(capital_structure.get("issued_preference_shares_number", 0)),
        "subscribed_capital_total": str(capital_structure.get("subscribed_capital_total", 0.0)),
        "subscribed_equity_shares_number": str(capital_structure.get("subscribed_equity_shares_number", 0)),
        "subscribed_preference_shares_number": str(capital_structure.get("subscribed_preference_shares_number", 0)),
        "paid_up_capital_total": str(capital_structure.get("paid_up_capital_total", 0.0)),
        "paid_up_equity_shares_number": str(capital_structure.get("paid_up_equity_shares_number", 0)),
        "paid_up_preference_shares_number": str(capital_structure.get("paid_up_preference_shares_number", 0)),
        "allotment_to_employees": str(capital_structure.get("allotment_to_employees", False)),
        "allotment_to_existing_shareholders": str(capital_structure.get("allotment_to_existing_shareholders", False)),
        "allotment_to_directors": str(capital_structure.get("allotment_to_directors", False)),
        "allotment_to_others": str(capital_structure.get("allotment_to_others", False)),
        "all_securities_allotted": str(capital_structure.get("all_securities_allotted", False)),
        "compliance_with_allotment": str(capital_structure.get("compliance_with_allotment", False))
    })
    
    # Create rows for each security type that has data
    security_types = ["preference_shares", "equity_shares", "debentures", "warrants_or_other_securities"]
    
    for security_type in security_types:
        security_data = pac_json.get(security_type, {})
        if security_data and any(str(v) for v in security_data.values() if v):
            row = base_info.copy()
            row.update({
                "security_type": security_type.replace("_", " ").title(),
                "number_of_shares": str(security_data.get("number_of_shares", 0)),
                "nominal_amount_per_share": str(security_data.get("nominal_amount_per_share", 0.0)),
                "total_nominal_amount": str(security_data.get("total_nominal_amount", 0.0)),
                "amount_paid_per_share": str(security_data.get("amount_paid_per_share", 0.0)),
                "total_amount_paid": str(security_data.get("total_amount_paid", 0.0)),
                "amount_due_per_share": str(security_data.get("amount_due_per_share", 0.0)),
                "total_amount_due": str(security_data.get("total_amount_due", 0.0)),
                "premium_per_share": str(security_data.get("premium_per_share", 0.0)),
                "total_premium_amount": str(security_data.get("total_premium_amount", 0.0)),
                "premium_paid_per_share": str(security_data.get("premium_paid_per_share", 0.0)),
                "total_premium_paid": str(security_data.get("total_premium_paid", 0.0)),
                "discount_per_share": str(security_data.get("discount_per_share", 0.0)),
                "total_discount": str(security_data.get("total_discount", 0.0)),
                "amount_to_be_paid_per_share": str(security_data.get("amount_to_be_paid_per_share", 0.0)),
                "total_amount_to_be_paid": str(security_data.get("total_amount_to_be_paid", 0.0)),
                "particulars": security_data.get("particulars", "")
            })
            csv_rows.append(row)
    
    # If no securities data found, create a single row with company info only
    if not csv_rows:
        row = base_info.copy()
        row.update({
            "security_type": "",
            "number_of_shares": "0",
            "nominal_amount_per_share": "0.0",
            "total_nominal_amount": "0.0",
            "amount_paid_per_share": "0.0",
            "total_amount_paid": "0.0",
            "amount_due_per_share": "0.0",
            "total_amount_due": "0.0",
            "premium_per_share": "0.0",
            "total_premium_amount": "0.0",
            "premium_paid_per_share": "0.0",
            "total_premium_paid": "0.0",
            "discount_per_share": "0.0",
            "total_discount": "0.0",
            "amount_to_be_paid_per_share": "0.0",
            "total_amount_to_be_paid": "0.0",
            "particulars": ""
        })
        csv_rows.append(row)
    
    return csv_rows


def process_all_pac_to_json_csv(input_dir: str = "No_XBRL", output_json_dir: str = "No_XBRL_JSON", output_csv_file: str = "pac_combined_data.csv") -> Dict[str, int]:
    """
    Process all PAC PDFs and export to JSON and CSV formats.
    
    Args:
        input_dir: Directory containing PDF files
        output_json_dir: Directory to save individual JSON files
        output_csv_file: Path for combined CSV file
        
    Returns:
        Dictionary with processing statistics
    """
    
    stats = {
        "total_files": 0,
        "pac_files": 0,
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
    
    print(f"Processing {len(pdf_files)} PDF files for PAC JSON/CSV export...")
    
    all_csv_rows = []
    
    # Process each PDF file
    for pdf_file in pdf_files:
        try:
            pdf_path = os.path.join(input_dir, pdf_file)
            cin, financial_year, extracted_info, form_type = process_pdf(pdf_path)
            
            if form_type == 'PAC' and extracted_info:
                stats["pac_files"] += 1
                
                # Transform to JSON
                pac_json = transform_pac_to_json(extracted_info, pdf_file)
                
                # Save individual JSON file
                json_filename = pdf_file.replace('.pdf', '_pac.json')
                json_path = os.path.join(output_json_dir, json_filename)
                
                if save_pac_json(pac_json, json_path):
                    stats["json_saved"] += 1
                    print(f"✓ JSON saved: {json_filename}")
                else:
                    stats["errors"] += 1
                    print(f"✗ Failed to save JSON: {json_filename}")
                
                # Convert to CSV rows
                csv_rows = pac_json_to_csv_rows(pac_json)
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
    print("\n=== PAC PROCESSING SUMMARY ===")
    print(f"Total PDF files processed: {stats['total_files']}")
    print(f"PAC files found: {stats['pac_files']}")
    print(f"JSON files saved: {stats['json_saved']}")
    print(f"CSV rows generated: {stats['csv_rows']}")
    print(f"Errors encountered: {stats['errors']}")
    
    return stats


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


def print_pac_info(extracted_info: Dict[str, str]):
    """Print PAC form information in a formatted way."""
    print("\n=== PAC FORM - PRIVATE ALLOTMENT CERTIFICATE ===")
    
    # Company basic information
    print(f"(1)(a) Corporate Identity Number (CIN): {extracted_info.get('CIN', 'Not found')}")
    print(f"(1)(b) Global Location Number (GLN): {extracted_info.get('GLN', 'Not found')}")
    print(f"(2)(a) Name of the company: {extracted_info.get('Company_Name', 'Not found')}")
    
    # Company address
    print(f"(2)(b) Address of the Registered office of the company:")
    address = extracted_info.get('Company_Address', 'Not found')
    if address != 'Not found' and address:
        # Format address for better readability
        formatted_address = address.replace('\r', '\n        ')
        print(f"        {formatted_address}")
    else:
        print(f"        {address}")
    
    print(f"(2)(c) Email Id of the company: {extracted_info.get('Email', 'Not found')}")
    print(f"Form Language: {extracted_info.get('Form_Language', 'Not found')}")
    print(f"Company Class: {extracted_info.get('Company_Class', 'Not found')}")
    
    # Allotment information
    print(f"\n=== SECURITIES ALLOTTED PAYABLE IN CASH ===")
    print(f"Number of allotments: {extracted_info.get('Number_Of_Allotments', 'Not found')}")
    
    allotment_details = extracted_info.get('Allotment_Details', {})
    if allotment_details:
        print(f"\n=== ALLOTMENT DETAILS ===")
        print(f"(i) Date of allotment: {allotment_details.get('Date_Of_Allotment', 'Not found')}")
        print(f"(ii)(a) Date of passing shareholders' resolution: {allotment_details.get('Date_Of_Passing_Resolution', 'Not found')}")
        print(f"(ii)(b) SRN of Form No. MGT-14: {allotment_details.get('SRN', 'Not found')}")
    
    # Preference shares information
    preference_shares = extracted_info.get('Preference_Shares', {})
    if preference_shares and any(preference_shares.values()):
        print(f"\n=== PREFERENCE SHARES ===")
        print(f"Brief particulars of terms and conditions: {preference_shares.get('Particulars', 'Not found')}")
        print(f"Number of securities allotted: {preference_shares.get('Number_Of_Shares', 'Not found')}")
        print(f"Nominal amount per security (in Rs.): {preference_shares.get('Nominal_Amount_Per_Share', 'Not found')}")
        print(f"Total nominal amount (in Rs.): {preference_shares.get('Total_Nominal_Amount', 'Not found')}")
        print(f"Amount paid per security on application (excluding premium) (in Rs.): {preference_shares.get('Amount_Paid_Per_Share', 'Not found')}")
        print(f"Total amount paid on application (excluding premium) (in Rs.): {preference_shares.get('Total_Amount_Paid', 'Not found')}")
        print(f"Amount due and payable on allotment per security (excluding premium) (in Rs.): {preference_shares.get('Amount_Due_Per_Share', 'Not found')}")
        print(f"Total Amount payable on allotment (excluding premium) (in Rs.): {preference_shares.get('Total_Amount_Due', 'Not found')}")
        print(f"Premium amount per security due and payable (if any) (in Rs.): {preference_shares.get('Premium_Per_Share', 'Not found')}")
        print(f"Total premium amount due and payable (if any) (in Rs.): {preference_shares.get('Total_Premium_Amount', 'Not found')}")
        print(f"Premium amount paid per security (if any): {preference_shares.get('Premium_Paid_Per_Share', 'Not found')}")
        print(f"Total premium amount paid (if any) (in Rs.): {preference_shares.get('Total_Premium_Paid', 'Not found')}")
        print(f"Amount of discount per security (if any) (in Rs.): {preference_shares.get('Discount_Per_Share', 'Not found')}")
        print(f"Total discount amount (if any) (in Rs.): {preference_shares.get('Total_Discount', 'Not found')}")
        print(f"Amount to be paid on calls per security (if any) (excluding premium) (in Rs.): {preference_shares.get('Amount_To_Be_Paid_Per_Share', 'Not found')}")
        print(f"Total amount to be paid on calls (if any) (excluding premium) (in Rs.): {preference_shares.get('Total_Amount_To_Be_Paid', 'Not found')}")
    
    # Equity shares information
    equity_shares = extracted_info.get('Equity_Shares', {})
    if equity_shares and any(equity_shares.values()):
        print(f"\n=== EQUITY SHARES ===")
        print(f"Brief particulars of terms and conditions: {equity_shares.get('Particulars', 'Not found')}")
        print(f"Number of securities allotted: {equity_shares.get('Number_Of_Shares', 'Not found')}")
        print(f"Nominal amount per security (in Rs.): {equity_shares.get('Nominal_Amount_Per_Share', 'Not found')}")
        print(f"Total nominal amount (in Rs.): {equity_shares.get('Total_Nominal_Amount', 'Not found')}")
        print(f"Amount paid per security on application (excluding premium) (in Rs.): {equity_shares.get('Amount_Paid_Per_Share', 'Not found')}")
        print(f"Total amount paid on application (excluding premium) (in Rs.): {equity_shares.get('Total_Amount_Paid', 'Not found')}")
        print(f"Amount due and payable on allotment per security (excluding premium) (in Rs.): {equity_shares.get('Amount_Due_Per_Share', 'Not found')}")
        print(f"Total Amount payable on allotment (excluding premium) (in Rs.): {equity_shares.get('Total_Amount_Due', 'Not found')}")
        print(f"Premium amount per security due and payable (if any) (in Rs.): {equity_shares.get('Premium_Per_Share', 'Not found')}")
        print(f"Total premium amount due and payable (if any) (in Rs.): {equity_shares.get('Total_Premium_Amount', 'Not found')}")
        print(f"Premium amount paid per security (if any): {equity_shares.get('Premium_Paid_Per_Share', 'Not found')}")
        print(f"Total premium amount paid (if any) (in Rs.): {equity_shares.get('Total_Premium_Paid', 'Not found')}")
        print(f"Amount of discount per security (if any) (in Rs.): {equity_shares.get('Discount_Per_Share', 'Not found')}")
        print(f"Total discount amount (if any) (in Rs.): {equity_shares.get('Total_Discount', 'Not found')}")
        print(f"Amount to be paid on calls per security (if any) (excluding premium) (in Rs.): {equity_shares.get('Amount_To_Be_Paid_Per_Share', 'Not found')}")
        print(f"Total amount to be paid on calls (if any) (excluding premium) (in Rs.): {equity_shares.get('Total_Amount_To_Be_Paid', 'Not found')}")
    
    # Capital structure information
    capital_structure = extracted_info.get('Capital_Structure', {})
    if capital_structure and any(capital_structure.values()):
        print(f"\n=== CAPITAL STRUCTURE OF THE COMPANY ===")
        print(f"Authorized Capital Total: Rs. {capital_structure.get('Authorized_Capital_Total', 'Not found')}")
        print(f"Issued Capital Total: Rs. {capital_structure.get('Issued_Capital_Total', 'Not found')}")
        print(f"Subscribed Capital Total: Rs. {capital_structure.get('Subscribed_Capital_Total', 'Not found')}")
        print(f"Paid-up Capital Total: Rs. {capital_structure.get('Paid_Up_Capital_Total', 'Not found')}")
        
        print(f"\n--- EQUITY SHARES ---")
        print(f"Authorized: {capital_structure.get('Authorized_Equity_Shares_Number', 'Not found')} shares (Rs. {capital_structure.get('Authorized_Equity_Shares_Value', 'Not found')})")
        print(f"Issued: {capital_structure.get('Issued_Equity_Shares_Number', 'Not found')} shares (Rs. {capital_structure.get('Issued_Equity_Shares_Value', 'Not found')})")
        print(f"Subscribed: {capital_structure.get('Subscribed_Equity_Shares_Number', 'Not found')} shares (Rs. {capital_structure.get('Subscribed_Equity_Shares_Value', 'Not found')})")
        print(f"Paid-up: {capital_structure.get('Paid_Up_Equity_Shares_Number', 'Not found')} shares (Rs. {capital_structure.get('Paid_Up_Equity_Shares_Value', 'Not found')})")
        
        print(f"\n--- PREFERENCE SHARES ---")
        print(f"Authorized: {capital_structure.get('Authorized_Preference_Shares_Number', 'Not found')} shares (Rs. {capital_structure.get('Authorized_Preference_Shares_Value', 'Not found')})")
        print(f"Issued: {capital_structure.get('Issued_Preference_Shares_Number', 'Not found')} shares (Rs. {capital_structure.get('Issued_Preference_Shares_Value', 'Not found')})")
        print(f"Subscribed: {capital_structure.get('Subscribed_Preference_Shares_Number', 'Not found')} shares (Rs. {capital_structure.get('Subscribed_Preference_Shares_Value', 'Not found')})")
        print(f"Paid-up: {capital_structure.get('Paid_Up_Preference_Shares_Number', 'Not found')} shares (Rs. {capital_structure.get('Paid_Up_Preference_Shares_Value', 'Not found')})")
        
        # Allotment categories
        print(f"\n--- ALLOTMENT CATEGORIES ---")
        print(f"To Employees: {capital_structure.get('Allotment_To_Employees', 'Not found')}")
        print(f"To Existing Shareholders: {capital_structure.get('Allotment_To_Existing_Shareholders', 'Not found')}")
        print(f"To Directors: {capital_structure.get('Allotment_To_Directors', 'Not found')}")
        print(f"To Others: {capital_structure.get('Allotment_To_Others', 'Not found')}")
        
        # Compliance information
        print(f"\n--- COMPLIANCE INFORMATION ---")
        print(f"All Securities Allotted: {capital_structure.get('All_Securities_Allotted', 'Not found')}")
        print(f"Compliance with Allotment: {capital_structure.get('Compliance_With_Allotment', 'Not found')}")
        print(f"Money Received Against Allotment: {capital_structure.get('Money_Received_Against_Allotment', 'Not found')}")


def main():
    """
    Main function with options for different processing modes.
    """
    print("=== PDF Information Extractor ===")
    print("1. Display mode: Show detailed information for each PDF")
    print("2. Export mode: Export all MGT7 data to JSON and CSV")
    print("3. Export mode: Export all PAC data to JSON and CSV")
    print("4. Both modes: Display and export")
    
    while True:
        choice = input("\nSelect mode (1, 2, 3, 4, or 'q' to quit): ").strip()
        
        if choice.lower() == 'q':
            return
        elif choice in ['1', '2', '3', '4']:
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 'q'.")
    
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
    
    # Export mode for MGT7 (option 2)
    if choice == '2':
        print("\n" + "="*60)
        print("EXPORT MODE: Processing all MGT7 files for JSON/CSV export")
        print("="*60)
        stats = process_all_mgt7_to_json_csv()
        return
    
    # Export mode for PAC (option 3)
    elif choice == '3':
        print("\n" + "="*60)
        print("EXPORT MODE: Processing all PAC files for JSON/CSV export")
        print("="*60)
        stats = process_all_pac_to_json_csv()
        return
    
    # Both modes (option 4) - process both MGT7 and PAC
    elif choice == '4':
        print("\n" + "="*60)
        print("EXPORT MODE: Processing all MGT7 and PAC files for JSON/CSV export")
        print("="*60)
        
        print("Processing MGT7 files...")
        mgt7_stats = process_all_mgt7_to_json_csv()
        
        print("\nProcessing PAC files...")
        pac_stats = process_all_pac_to_json_csv()
        
        print("\n=== COMBINED PROCESSING SUMMARY ===")
        print(f"MGT7 files processed: {mgt7_stats['mgt7_files']}")
        print(f"PAC files processed: {pac_stats['pac_files']}")
        print(f"Total JSON files saved: {mgt7_stats['json_saved'] + pac_stats['json_saved']}")
        print(f"Total errors: {mgt7_stats['errors'] + pac_stats['errors']}")
        return
    
    # Display mode (option 1)
    if choice == '1':
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
            elif form_type == 'PAC' and extracted_info:
                print_pac_info(extracted_info)
                
                # Show a sample of the JSON structure for PAC
                pac_json = transform_pac_to_json(extracted_info, pdf_file)
                print("\n=== JSON TRANSFORMATION SAMPLE ===")
                print("Company Information:")
                print(f"  CIN: {pac_json['company_cin']}")
                print(f"  Name: {pac_json['company_name']}")
                print(f"  Class: {pac_json['company_class']}")
                print(f"  Number of Allotments: {pac_json['number_of_allotments']}")
                
                # Show securities information
                if pac_json['preference_shares']:
                    print(f"  Preference Shares: {pac_json['preference_shares']['number_of_shares']} shares")
                if pac_json['equity_shares']:
                    print(f"  Equity Shares: {pac_json['equity_shares']['number_of_shares']} shares")
                
                # Demonstrate CSV-ready format
                csv_rows = pac_json_to_csv_rows(pac_json)
                print(f"\nCSV Format: Ready for export with {len(csv_rows)} rows")
                
            elif form_type == 'UNKNOWN':
                print("\nForm type could not be determined. No structured data extracted.")
            
            print(f"{'='*60}")


if __name__ == "__main__":
    main()