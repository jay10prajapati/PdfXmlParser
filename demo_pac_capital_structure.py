#!/usr/bin/env python3
"""
Demo script to show PAC capital structure extraction functionality.
This script demonstrates how the capital structure information is extracted from PAC forms.
"""

import sys
import os
from collections import OrderedDict

# Add the current directory to Python path to import the extraction module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extract_pdf_info_v2 import extract_pac_info, transform_pac_to_json, pac_json_to_csv_rows

def demo_pac_capital_structure():
    """Demo PAC capital structure extraction with sample data."""
    
    # Sample form_fields data with capital structure information
    form_fields = OrderedDict({
        # Basic company information
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].CIN_C[0]': 'U74999KA2017PTC105368',
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].CompanyName_C[0]': 'YULU BIKES PRIVATE LIMITED',
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].Email_C[0]': 'amit@yulu.bike',
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].FormLanguage[0]': '/ENGL',
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].hiddencompanyclass[0]': 'PRIV',
        
        # Capital structure information
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].Cap_Authrsd[0]': '9000000',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumAuthSharesEq_N[0]': '80000',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValAuthEq_N[0]': '800000',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalAmtAuthPEqS[0]': '10',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumSharesAuthPref_N[0]': '102097',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValAuthPref_N[0]': '8200000',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalAmtAuthPPrfS[0]': '10, 100',
        
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CapIssuOfCompany[0]': '4705360',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumIssSharesEq_N[0]': '44520',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValIssueEq_N[0]': '445200',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalIssuAmtPEqS[0]': '10',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumSharesIssPref_N[0]': '62695',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValIssPref_N[0]': '4260160',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalAmtIssPPrfS[0]': '10, 100',
        
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CapSubscrbCapOfCompany[0]': '4705360',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumSharesSubEq1_N[0]': '44520',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValSubEq1_N[0]': '445200',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalAmtSubPEqS[0]': '10',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumSharesSubPref1_N[0]': '62695',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValSubPref1_N[0]': '4260160',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalAmtSubPPrfS[0]': '10, 100',
        
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CapPaidUpOfCompany[0]': '4705360',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumSharesPaidEq_N[0]': '44520',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValPaidEq_N[0]': '445200',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalAmtPaidPEqS[0]': '10',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NumSharesPaidPref_N[0]': '62695',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NomValPaidPref_N[0]': '4260160',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].NominalAmtPaidPPrfS[0]': '10, 100',
        
        # Allotment categories
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CBExistShrHldr[0]': '/ESHR',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CBOthers[0]': '/OTHR',
        
        # Compliance checkboxes
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CB11b1[0]': '/ALLSEC',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CB11b4[0]': '/COMALL',
        'data[0].Form2_Dtls[0].MainPage[0].CapitalStructure[0].CB11b5[0]': '/RECMON',
    })
    
    print("=== PAC CAPITAL STRUCTURE EXTRACTION DEMO ===")
    print(f"Total form fields: {len(form_fields)}")
    
    # Extract PAC information
    print("\n=== EXTRACTING PAC INFORMATION ===")
    pac_info = extract_pac_info(form_fields)
    
    # Display capital structure information
    capital_structure = pac_info.get('Capital_Structure', {})
    if capital_structure:
        print("\n=== CAPITAL STRUCTURE EXTRACTED ===")
        print(f"Authorized Capital Total: Rs. {capital_structure.get('Authorized_Capital_Total', 'Not found')}")
        print(f"Issued Capital Total: Rs. {capital_structure.get('Issued_Capital_Total', 'Not found')}")
        print(f"Subscribed Capital Total: Rs. {capital_structure.get('Subscribed_Capital_Total', 'Not found')}")
        print(f"Paid-up Capital Total: Rs. {capital_structure.get('Paid_Up_Capital_Total', 'Not found')}")
        
        print(f"\nEquity Shares - Authorized: {capital_structure.get('Authorized_Equity_Shares_Number', 'Not found')}")
        print(f"Equity Shares - Issued: {capital_structure.get('Issued_Equity_Shares_Number', 'Not found')}")
        print(f"Preference Shares - Authorized: {capital_structure.get('Authorized_Preference_Shares_Number', 'Not found')}")
        print(f"Preference Shares - Issued: {capital_structure.get('Issued_Preference_Shares_Number', 'Not found')}")
        
        print(f"\nAllotment to Existing Shareholders: {capital_structure.get('Allotment_To_Existing_Shareholders', 'Not found')}")
        print(f"Allotment to Others: {capital_structure.get('Allotment_To_Others', 'Not found')}")
        print(f"All Securities Allotted: {capital_structure.get('All_Securities_Allotted', 'Not found')}")
        print(f"Compliance with Allotment: {capital_structure.get('Compliance_With_Allotment', 'Not found')}")
    
    # Transform to JSON
    print("\n=== JSON TRANSFORMATION ===")
    pac_json = transform_pac_to_json(pac_info, "demo_pac_form.pdf")
    
    # Show capital structure in JSON format
    json_capital_structure = pac_json.get("capital_structure", {})
    if json_capital_structure:
        print("Capital Structure in JSON format:")
        print(f"  Authorized Capital Total: {json_capital_structure.get('authorized_capital_total', 0.0)}")
        print(f"  Issued Capital Total: {json_capital_structure.get('issued_capital_total', 0.0)}")
        print(f"  Paid-up Capital Total: {json_capital_structure.get('paid_up_capital_total', 0.0)}")
        print(f"  Authorized Equity Shares: {json_capital_structure.get('authorized_equity_shares_number', 0)}")
        print(f"  Issued Equity Shares: {json_capital_structure.get('issued_equity_shares_number', 0)}")
        print(f"  Allotment to Existing Shareholders: {json_capital_structure.get('allotment_to_existing_shareholders', False)}")
        print(f"  All Securities Allotted: {json_capital_structure.get('all_securities_allotted', False)}")
    
    # Convert to CSV format
    print("\n=== CSV TRANSFORMATION ===")
    csv_rows = pac_json_to_csv_rows(pac_json)
    print(f"Generated {len(csv_rows)} CSV rows")
    
    if csv_rows:
        print("Sample CSV data (first row):")
        sample_row = csv_rows[0]
        print(f"  Company Name: {sample_row.get('company_name', '')}")
        print(f"  CIN: {sample_row.get('company_cin', '')}")
        print(f"  Authorized Capital Total: {sample_row.get('authorized_capital_total', '')}")
        print(f"  Issued Capital Total: {sample_row.get('issued_capital_total', '')}")
        print(f"  Paid-up Capital Total: {sample_row.get('paid_up_capital_total', '')}")
        print(f"  Authorized Equity Shares: {sample_row.get('authorized_equity_shares_number', '')}")
        print(f"  Allotment to Existing Shareholders: {sample_row.get('allotment_to_existing_shareholders', '')}")
    
    print(f"\n=== DEMO COMPLETED SUCCESSFULLY ===")
    print("✓ Capital structure information extracted successfully")
    print("✓ JSON transformation completed")
    print("✓ CSV transformation completed")
    print("\nThe PAC form now supports complete capital structure extraction!")

def main():
    """Main function to run the demo."""
    demo_pac_capital_structure()

if __name__ == "__main__":
    main()