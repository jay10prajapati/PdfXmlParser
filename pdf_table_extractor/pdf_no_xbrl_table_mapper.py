"""
pdf_no_xbrl_table_mapper.py

This script automates the extraction and mapping of tabular data from PDF files, specifically for financial and XBRL-related forms. It provides:

1. Batch processing of all PDFs in the No_XBRL directory, generating mapped tables and saving results as JSON in No_XBRL_JSON.
2. Command-line mode to generate a specific table for a given PDF.
3. Mapping logic for various financial tables (balance sheet, borrowings, profit and loss, etc.) using configuration mappings.
4. Extraction of interactive form fields from PDFs using PyPDF2.
5. Logging of execution flow, errors, and key actions for debugging and traceability.
6. Modular mapping functions for different table types and periods.
7. Output of available table types and error handling for invalid input.

This script is intended for use in financial data extraction pipelines where structured tabular data is required from regulatory PDF forms.
"""

import copy
import json
import os
import sys
import logging
from collections import OrderedDict

from PyPDF2 import PdfReader

from pdf_table_extractor.mapping_config import (
    balance_sheet_mapping,
    long_term_borrowing_mapping,
    short_term_borrowing_mapping,
    long_term_loan_unsecured_mapping,
    long_term_loan_doubtful_mapping,
    trade_receivable_mapping,
    financial_parameters_mapping,
    share_capital_raised_mapping,
    profit_and_loss_mapping,
    earnings_in_foreign_exchange_mapping,
    expenditure_in_foreign_exchange_mapping,
    financial_parameter_profit_and_loss_mapping
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def get_fields(obj, tree=None, retval=None, fileobj=None):
    """
    Extracts field data if this PDF contains interactive form fields.
    The *tree* and *retval* parameters are for recursive use.

    :param fileobj: A file object (usually a text file) to write
        a report to on all interactive form fields found.
    :return: A dictionary where each key is a field name, and each
        value is a :class:`Field<PyPDF2.generic.Field>` object. By
        default, the mapping name is used for keys.
    :rtype: dict, or ``None`` if form data could not be located.
    """
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
    return OrderedDict((k, v.get('/V', '')) for k, v in fields.items())


def map_balance_sheet_data(mapping, resulted_dictionary):
    """Map balance sheet data with current and previous periods"""
    balance_sheet_current = copy.deepcopy(mapping)
    balance_sheet_previous = copy.deepcopy(mapping)

    mapped_data = {
        "Current balance sheet": balance_sheet_current,
        "Previous balance sheet": balance_sheet_previous
    }

    def fill_values(template_dict, result_dict, is_current):
        for key, value in template_dict.items():
            if isinstance(value, dict):
                fill_values(value, result_dict, is_current)
            elif isinstance(value, tuple):
                if is_current:
                    template_dict[key] = result_dict.get(value[0])
                else:
                    template_dict[key] = result_dict.get(value[1])

    fill_values(mapped_data["Current balance sheet"], resulted_dictionary, True)
    fill_values(mapped_data["Previous balance sheet"], resulted_dictionary, False)

    return mapped_data


def map_period_data(template, data_dict, mapping_dict):
    """Generic function to map data with current and previous periods"""
    mapped_data = {
        "Current reporting period": {},
        "Previous reporting period": {}
    }

    def fill_data(target_dict, source_data, is_current):
        for key, value_map in mapping_dict.items():
            if isinstance(value_map, dict):
                target_dict[key] = {}
                for sub_key, sub_value_map in value_map.items():
                    if is_current:
                        target_dict[key][sub_key] = source_data.get(sub_value_map[0])
                    else:
                        target_dict[key][sub_key] = source_data.get(sub_value_map[1])
            else:
                if is_current:
                    target_dict[key] = source_data.get(value_map[0])
                else:
                    target_dict[key] = source_data.get(value_map[1])

    fill_data(mapped_data["Current reporting period"], data_dict, True)
    fill_data(mapped_data["Previous reporting period"], data_dict, False)

    return mapped_data


def map_simple_data(template, data_dict, mapping_dict):
    """Generic function to map simple data without periods"""
    mapped_data = {}
    for key, value_map in mapping_dict.items():
        mapped_data[key] = data_dict.get(value_map)
    return mapped_data


def map_share_capital_data(template, data_dict):
    """Map share capital data with current and previous periods"""
    mapped_data = {
        "Current reporting period": {},
        "Previous reporting period": {}
    }

    def fill_data(target_dict, source_data, is_current):
        for key, value_map in share_capital_raised_mapping.items():
            if isinstance(value_map, dict):
                target_dict[key] = {}
                for sub_key, sub_value_map in value_map.items():
                    target_dict[key][sub_key] = source_data.get(sub_value_map)
            else:
                target_dict[key] = source_data.get(value_map)

    fill_data(mapped_data["Current reporting period"], data_dict, True)
    fill_data(mapped_data["Previous reporting period"], data_dict, False)

    return mapped_data


def map_with_multiple_dict_value_data(template, data_dict, mapping_dict):
    """Map profit and loss data"""
    mapped_data = {}
    for key, value_map in mapping_dict.items():
        if isinstance(value_map, dict):
            mapped_data[key] = {}
            for sub_key, sub_value in value_map.items():
                mapped_data[key][sub_key] = data_dict.get(sub_value)
        else:
            mapped_data[key] = data_dict.get(value_map)
    return mapped_data

def map_with_3_level_dict_value_data(template, data_dict, mapping_dict):
    """Recursively map up to 3-level (or more) nested dicts to values from data_dict."""
    def recursive_map(mapping):
        if isinstance(mapping, dict):
            result = {}
            for k, v in mapping.items():
                result[k] = recursive_map(v)
            return result
        else:
            return data_dict.get(mapping)
    return recursive_map(mapping_dict)


def map_earnings_in_foreign_exchange_data(template, data_dict):
    """Map earnings in foreign exchange data"""
    mapped_data = {}
    for key, value_map in earnings_in_foreign_exchange_mapping.items():
        mapped_data[key] = data_dict.get(value_map)
    return mapped_data

def map_expenditure_in_foreign_exchange_data(template, data_dict):
    """Map expenditure in foreign exchange data"""
    mapped_data = {}
    for key, value_map in expenditure_in_foreign_exchange_mapping.items():
        mapped_data[key] = data_dict.get(value_map)
    return mapped_data  

def map_financial_parameter_profit_and_loss_data(template, data_dict):
    """Map financial parameter profit and loss data"""
    mapped_data = {}
    for key, value_map in financial_parameter_profit_and_loss_mapping.items():
        mapped_data[key] = data_dict.get(value_map)
    return mapped_data
# Table mapping configuration
TABLE_MAPPINGS = {
    1: {
        "name": "Balance Sheet",
        "mapping": balance_sheet_mapping,
        "function": map_balance_sheet_data
    },
    2: {
        "name": "Long Term Borrowings",
        "mapping": long_term_borrowing_mapping,
        "function": map_period_data
    },
    3: {
        "name": "Short Term Borrowings",
        "mapping": short_term_borrowing_mapping,
        "function": map_period_data
    },
    4: {
        "name": "Long Term Loans Unsecured",
        "mapping": long_term_loan_unsecured_mapping,
        "function": map_period_data
    },
    5: {
        "name": "Long Term Loans Doubtful",
        "mapping": long_term_loan_doubtful_mapping,
        "function": map_period_data
    },
    6: {
        "name": "Trade Receivables",
        "mapping": trade_receivable_mapping,
        "function": map_period_data
    },
    7: {
        "name": "Financial Parameters",
        "mapping": financial_parameters_mapping,
        "function": map_with_3_level_dict_value_data
    },
    8: {
        "name": "Share Capital Raised",
        "mapping": share_capital_raised_mapping,
        "function": map_with_3_level_dict_value_data
    },
    9: {
        "name": "Profit and Loss",
        "mapping": profit_and_loss_mapping,
        "function": map_with_3_level_dict_value_data
    },
    10: {
        "name": "Earnings in Foreign Exchange",
        "mapping": earnings_in_foreign_exchange_mapping,
        "function": map_with_3_level_dict_value_data
    },
    11: {
        "name": "Expenditure in Foreign Exchange",
        "mapping": expenditure_in_foreign_exchange_mapping,
        "function": map_with_3_level_dict_value_data
    },
    12: {
        "name": "Financial Parameters Profit and Loss",
        "mapping": financial_parameter_profit_and_loss_mapping,
        "function": map_with_3_level_dict_value_data
    }  
}


def generate_table_result(table_number, pdf_file_path):
    """
    Generate result for a specific table number
    
    Args:
        table_number (int): The table number (1-9)
        pdf_file_path (str): Path to the PDF file
    
    Returns:
        dict: The mapped data for the specified table
    """
    if table_number not in TABLE_MAPPINGS:
        available_tables = ", ".join(map(str, TABLE_MAPPINGS.keys()))
        raise ValueError(f"Invalid table number. Available tables: {available_tables}")
    
    # Get form fields from PDF
    field_and_values = get_form_fields(pdf_file_path)
    
    # Get table configuration
    table_config = TABLE_MAPPINGS[table_number]
    
    # Generate result using the appropriate mapping function
    if table_config["function"] == map_period_data:
        result = table_config["function"](None, field_and_values, table_config["mapping"])
    elif table_config["function"] in [map_with_multiple_dict_value_data, map_with_3_level_dict_value_data]:
        result = table_config["function"](None,field_and_values, table_config["mapping"])
    else:
        result = table_config["function"](table_config["mapping"], field_and_values)
    
    return {
        "table_name": table_config["name"],
        "table_number": table_number,
        "data": result
    }


def print_available_tables():
    """Print all available table numbers and names"""
    logging.info("[pdf_no_xbrl_table_mapper.py] Available Tables:")
    logging.info("-" * 50)
    for table_num, config in TABLE_MAPPINGS.items():
        logging.info(f"Table {table_num}: {config['name']}")
    logging.info("-" * 50)


def process_all_pdfs_in_no_xbrl():
    """
    For each PDF in No_XBRL, generate all table results and save as a single JSON file in No_XBRL_JSON.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    no_xbrl_dir = os.path.join(project_root, "No_XBRL")
    output_dir = os.path.join(project_root, "No_XBRL_JSON")
    os.makedirs(output_dir, exist_ok=True)

    pdf_files = [f for f in os.listdir(no_xbrl_dir) if f.lower().endswith('.pdf')]
    if not pdf_files:
        logging.warning(f"[pdf_no_xbrl_table_mapper.py] No PDF files found in {no_xbrl_dir}")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(no_xbrl_dir, pdf_file)
        logging.info(f"[pdf_no_xbrl_table_mapper.py] Processing: {pdf_file}")
        all_results = {}
        for table_number in sorted(TABLE_MAPPINGS.keys()):
            try:
                result = generate_table_result(table_number, pdf_path)
                all_results[f"Table_{table_number}_{result['table_name'].replace(' ', '_')}"] = result['data']
                logging.info(f"[pdf_no_xbrl_table_mapper.py] Successfully generated Table {table_number} for {pdf_file}")
            except Exception as e:
                all_results[f"Table_{table_number}_error"] = str(e)
                logging.error(f"[pdf_no_xbrl_table_mapper.py] Error generating Table {table_number} for {pdf_file}: {e}")
        # Save to JSON file
        json_filename = os.path.splitext(pdf_file)[0] + ".json"
        json_path = os.path.join(output_dir, json_filename)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=4, ensure_ascii=False)
        logging.info(f"[pdf_no_xbrl_table_mapper.py] Saved results to {json_path}\n")


def main():
    """Main function to run the table generator"""
    if len(sys.argv) < 2:
        logging.info("[pdf_no_xbrl_table_mapper.py] No arguments provided. Running batch mode for all PDFs in No_XBRL...\n")
        process_all_pdfs_in_no_xbrl()
        return
    try:
        table_number = int(sys.argv[1])
        # Use default PDF file if not provided
        if len(sys.argv) >= 3:
            pdf_file_path = sys.argv[2]
        else:
            # Default PDF file path
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            pdf_file_path = os.path.join(project_root, "No_XBRL", "6__Form_AOC-4-30102022.pdf")
            # pdf_file_path = os.path.join(project_root, "No_XBRL", "2__Form_AOC-4-13122024_signed.pdf")

        # Check if PDF file exists
        if not os.path.exists(pdf_file_path):
            logging.error(f"[pdf_no_xbrl_table_mapper.py] Error: PDF file not found at {pdf_file_path}")
            return
        # Generate result
        result = generate_table_result(table_number, pdf_file_path)
        # Print result
        logging.info(f"[pdf_no_xbrl_table_mapper.py] === {result['table_name']} (Table {result['table_number']}) ===")
        logging.info(json.dumps(result['data'], indent=4))
    except ValueError as e:
        logging.error(f"[pdf_no_xbrl_table_mapper.py] Error: {e}")
        print_available_tables()
    except Exception as e:
        logging.error(f"[pdf_no_xbrl_table_mapper.py] Error: {e}")


if __name__ == "__main__":
    main() 