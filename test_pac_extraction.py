#!/usr/bin/env python3
"""
Test script for PAC (Private Allotment Certificate) form extraction functionality.
This script tests the PAC extraction using the provided form_fields data.
"""

import sys
import os
from collections import OrderedDict

# Add the current directory to Python path to import the extraction module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extract_pdf_info_v2 import extract_pac_info, detect_form_type, print_pac_info

def test_pac_extraction():
    """Test PAC form extraction with sample data."""
    
    # Sample form_fields data provided by the user
    form_fields = OrderedDict({
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].GLN_C[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].Prefill_B[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].CIN_C[0]': 'U74999KA2017PTC105368', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].CompanyAdd_C[0]': 'Villa 119, Adarsh Palm Retreat\rOuter Ring Road, Devarabeesanahalli\rBangalore\rBangalore\rKarnataka\r560103', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].CompanyName_C[0]': 'YULU BIKES PRIVATE LIMITED', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].Email_C[0]': 'amit@yulu.bike', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].ExtractedVersion[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].DOC_READY[0]': '1', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].HostAppName[0]': 'Adobe PDF Library', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].Hidden_FormLanguage[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].hiddenSmallCmpny_F[0]': 'N', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].FormLanguage[0]': '/ENGL', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].error_c[0]': 'CIN', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].hiddencompanyclass[0]': 'PRIV', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].hid[0]': 'Y', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].hid_ifsc[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].hid_class_comp[0]': 'PRIV', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].hid_sec8[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].Page1[0].hid_nidhi[0]': '', 
        'Page1[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].Heading1[0].NumOfAllotmnt_N[0]': '1', 
        'data[0].Form2_Dtls[0].MainPage[0].Heading1[0].HiddenNumOfAllotmnt_N[0]': '', 
        'Heading1[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefNumShares_N[0]': '12154', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqNumShares_N[0]': '20', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefPerNom_N[0]': '100', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerNom_N[0]': '10', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefPerShare_N[0]': '100', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerShare_N[0]': '10', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefPerAllot_N[0]': '0', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerAllot_N[0]': '0', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefPerPremiumDue_N[0]': '130645.2', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerPremiumDue_N[0]': '130735.2', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefPerPremium_N[0]': '130645.2', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerPremium_N[0]': '130735.2', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefPerDisc_N[0]': '0', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerDisc_N[0]': '0', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefTotAllot_N[0]': '0', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotAllot_N[0]': '0', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefTotNom_N[0]': '1215400', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotNom_N[0]': '200', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefTotApp_N[0]': '1215400', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefTotPremDue_N[0]': '1587861760.8', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefTotPremium_N[0]': '1587861760.8', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefTotDisc_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotApp_N[0]': '200', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotPremDue_N[0]': '2614704', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotPremium_N[0]': '2614704', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotDisc_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].Pref1[0]': '/PREF', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].Equity1[0]': '/EQTY', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DateAllotment_D[0]': '15/09/2022', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefAmtToBePaid_N[0]': '0', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefTotalAmtToBePaid_N[0]': '0', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqAmtToBePaid_N[0]': '0', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotalAmtToBePaid_N[0]': '0', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].PrefParticulars[0]': 'Please refer to the list of allottees', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqParticulars[0]': 'Rank pari-passu with existing equity shares', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].Hidden_CurrentDate2[0]': '15/09/2022', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].SRN_C[0]': 'F24636896', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].Date_D[0]': '14/09/2022', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].Equity2[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].Deb1[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotalAmtToBePaid_N_WDR[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqAmtToBePaid_N_WDR[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotDisc_N_WDR[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerDisc_N_WDR[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotPremium_N_WDR[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerPremium_N_WDR[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotPremDue_N_WDR[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerPremiumDue_N_WDR[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotAllot_N_WDR[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerAllot_N_WDR[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotApp_N_WDR[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerShare_N_WDR[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqTotNom_N_WDR[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqPerNom_N_WDR[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqNumShares_N_WDR[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].EqParticulars_WDR[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DebTotalAmtToBePaid_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DebAmtToBePaid_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DebTotDisc_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DebPerDisc_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DebTotPremium_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DebPerPremium_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DebTotPremDue_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DebPerPremiumDue_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DebTotAllot_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DebPerAllot_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DebTotApp_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DebPerShare_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DebTotNom_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DebPerNom_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DebNumShares_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].DebParticulars[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].Index_Dynamic_Roman[0]': '1', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].hidate1[0]': '2022-09-15$', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].hidate2[0]': '2022-09-14$', 
        'data[0].Form2_Dtls[0].MainPage[0].FirstAllotment1[0].hisrn1[0]': 'F24636896$', 
        'FirstAllotment1[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].Heading2[0].NumOfAllotmnt1_N[0]': '', 
        'data[0].Form2_Dtls[0].MainPage[0].Heading2[0].HiddenNumOfAllotmnt1_N[0]': '', 
        'Heading2[0]': ''
    })
    
    print("=== PAC FORM EXTRACTION TEST ===")
    print(f"Total form fields: {len(form_fields)}")
    
    # Test form type detection
    form_type = detect_form_type(form_fields)
    print(f"Detected form type: {form_type}")
    
    if form_type != 'PAC':
        print("ERROR: Form type detection failed!")
        return False
    
    # Test PAC information extraction
    print("\n=== EXTRACTING PAC INFORMATION ===")
    pac_info = extract_pac_info(form_fields)
    
    # Verify key information was extracted
    expected_values = {
        'CIN': 'U74999KA2017PTC105368',
        'Company_Name': 'YULU BIKES PRIVATE LIMITED',
        'Email': 'amit@yulu.bike',
        'Form_Language': 'English',
        'Company_Class': 'PRIV',
        'Number_Of_Allotments': '1'
    }
    
    print("\n=== VERIFICATION ===")
    all_passed = True
    for key, expected_value in expected_values.items():
        actual_value = pac_info.get(key, '')
        status = "✓" if actual_value == expected_value else "✗"
        print(f"{status} {key}: Expected '{expected_value}', Got '{actual_value}'")
        if actual_value != expected_value:
            all_passed = False
    
    # Check nested structures
    allotment_details = pac_info.get('Allotment_Details', {})
    if allotment_details.get('Date_Of_Allotment') == '15/09/2022':
        print("✓ Allotment Date: 15/09/2022")
    else:
        print(f"✗ Allotment Date: Expected '15/09/2022', Got '{allotment_details.get('Date_Of_Allotment', '')}'")
        all_passed = False
    
    # Check preference shares
    preference_shares = pac_info.get('Preference_Shares', {})
    if preference_shares.get('Number_Of_Shares') == '12154':
        print("✓ Preference Shares Count: 12154")
    else:
        print(f"✗ Preference Shares Count: Expected '12154', Got '{preference_shares.get('Number_Of_Shares', '')}'")
        all_passed = False
    
    # Check equity shares
    equity_shares = pac_info.get('Equity_Shares', {})
    if equity_shares.get('Number_Of_Shares') == '20':
        print("✓ Equity Shares Count: 20")
    else:
        print(f"✗ Equity Shares Count: Expected '20', Got '{equity_shares.get('Number_Of_Shares', '')}'")
        all_passed = False
    
    print(f"\n=== TEST RESULT ===")
    if all_passed:
        print("✓ ALL TESTS PASSED! PAC extraction is working correctly.")
        
        # Display the extracted information using the print function
        print_pac_info(pac_info)
        
        return True
    else:
        print("✗ SOME TESTS FAILED! Please check the extraction logic.")
        return False

def main():
    """Main function to run the test."""
    success = test_pac_extraction()
    
    if success:
        print("\n🎉 PAC form extraction functionality has been successfully implemented!")
        print("You can now process PAC forms using the main extraction script.")
    else:
        print("\n❌ PAC form extraction needs debugging.")
    
    return success

if __name__ == "__main__":
    main()