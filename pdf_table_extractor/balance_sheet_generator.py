import copy
import json
import os
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
    # Copy the template to create independent dictionaries

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
                # This assumes 'value' is a tuple of (current_key, previous_key)
                if is_current:
                    template_dict[key] = result_dict.get(value[0])
                else:
                    template_dict[key] = result_dict.get(value[1])
            else:
                # For top-level keys like "Total" directly under "EQUITY AND LIABILITIES" or "ASSETS"
                # This handles cases where 'Total' might not be a nested dict, but a direct value
                # (though in the provided template, 'Total' is directly assigned None)
                pass

    fill_values(mapped_data["Current balance sheet"], resulted_dictionary, True)
    fill_values(mapped_data["Previous balance sheet"], resulted_dictionary, False)

    return mapped_data


def map_long_term_borrowings(template, data_dict):
    mapped_data = {
        "Current reporting period": {},
        "Previous reporting period": {}
    }

    def fill_data(target_dict, source_data, is_current):
        for key, value_map in long_term_borrowing_mapping.items():
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


def map_short_term_borrowings(template, data_dict):
    mapped_data = {
        "Current reporting period": {},
        "Previous reporting period": {}
    }

    def fill_data(target_dict, source_data, is_current):
        for key, value_map in short_term_borrowing_mapping.items():
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


def map_long_term_loans_unsecured(template, data_dict):
    mapped_data = {
        "Current reporting period": {},
        "Previous reporting period": {}
    }

    def fill_data(target_dict, source_data, is_current):
        for key, value_map in long_term_loan_unsecured_mapping.items():
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


def map_long_term_loans_doubtful(template, data_dict):
    mapped_data = {
        "Current reporting period": {},
        "Previous reporting period": {}
    }

    def fill_data(target_dict, source_data, is_current):
        for key, value_map in long_term_loan_doubtful_mapping.items():
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


def map_trade_receivables(template, data_dict):
    mapped_data = {
        "Current reporting period": {},
        "Previous reporting period": {}
    }

    def fill_data(target_dict, source_data, is_current):
        for key, value_map in trade_receivable_mapping.items():
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


def map_financial_parameters(template, data_dict):
    mapped_data = {}

    for key, value_map in financial_parameters_mapping.items():
        mapped_data[key] = data_dict.get(value_map)

    return mapped_data


def map_share_capital_raised(template, data_dict):
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


# Profit and Loss mapping
def map_profit_and_loss(template, data_dict):
    mapped_data = {}
    for key, value_map in profit_and_loss_mapping.items():
        if isinstance(value_map, dict):
            mapped_data[key] = {}
            for sub_key, sub_value in value_map.items():
                mapped_data[key][sub_key] = data_dict.get(sub_value)
        else:
            mapped_data[key] = data_dict.get(value_map)
    return mapped_data

# Earnings in Foreign Exchange mapping
def map_earnings_in_foreign_exchange(template, data_dict):
    mapped_data = {}
    for key, value_map in earnings_in_foreign_exchange_mapping.items():
        if isinstance(value_map, dict):
            mapped_data[key] = {}
            for sub_key, sub_value in value_map.items():
                mapped_data[key][sub_key] = data_dict.get(sub_value)
        else:
            mapped_data[key] = data_dict.get(value_map)
    return mapped_data

# Expenditure in Foreign Exchange mapping
def map_expenditure_in_foreign_exchange(template, data_dict):
    mapped_data = {}
    for key, value_map in expenditure_in_foreign_exchange_mapping.items():
        if isinstance(value_map, dict):
            mapped_data[key] = {}
            for sub_key, sub_value in value_map.items():
                mapped_data[key][sub_key] = data_dict.get(sub_value)
        else:
            mapped_data[key] = data_dict.get(value_map)
    return mapped_data

# Financial Parameters Profit and Loss mapping
# write function according to the mapping_config.py file where value_map may have multiple values
# for example:
# "Proposed Dividend": {
#   "Amount": "data[0].FormAOC4_Dtls[0].Segment2_3[0].Table12[0].Row1[0].NumericField143[0]",
#   "Percentage": "data[0].FormAOC4_Dtls[0].Segment2_3[0].Table12[0].Row1[0].NumericField144[0]"
# }
# so we need to get the value of Amount and Percentage from the data_dict
# and return a dictionary with the key as the name of the mapping and the value as the value of the mapping
# for example:
# {
#   "Proposed Dividend": {
#     "Amount": "100000",
#     "Percentage": "10%"
#   }   
def map_financial_parameter_profit_and_loss(template, data_dict):
    mapped_data = {}
    for key, value_map in financial_parameter_profit_and_loss_mapping.items():
        if isinstance(value_map, dict):
            mapped_data[key] = {}
            for sub_key, sub_value in value_map.items():
                mapped_data[key][sub_key] = data_dict.get(sub_value)
        else:
            mapped_data[key] = data_dict.get(value_map)
    return mapped_data
    



# Example usage and testing
if __name__ == "__main__":
    # get project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdf_file_name = os.path.join(project_root, "No_XBRL", "2__Form_AOC-4-13122024_signed.pdf")
    field_and_values = get_form_fields(pdf_file_name)
    #
    # # Balance Sheet mapping
    # final_balance_sheets = map_balance_sheet_data(balance_sheet_mapping, field_and_values)
    #
    # # Long term borrowings mapping
    # final_long_term_borrowings = map_long_term_borrowings(long_term_borrowing_mapping, field_and_values)
    #
    # # Short term borrowings mapping
    # final_short_term_borrowings = map_short_term_borrowings(short_term_borrowing_mapping, field_and_values)
    #
    # # Long term loans unsecured mapping
    # final_long_term_loans_unsecured = map_long_term_loans_unsecured(long_term_loan_unsecured_mapping, field_and_values)
    #
    # # Long term loans doubtful mapping
    # final_long_term_loans_doubtful = map_long_term_loans_doubtful(long_term_loan_doubtful_mapping, field_and_values)
    #
    # # Trade receivables mapping
    # final_trade_receivables = map_trade_receivables(trade_receivable_mapping, field_and_values)
    #
    # # Financial parameters mapping
    # final_financial_parameters = map_financial_parameters(financial_parameters_mapping, field_and_values)
    #
    # # Share capital raised mapping
    # final_share_capital_raised = map_share_capital_raised(share_capital_raised_mapping, field_and_values)
    #
    # # Profit and Loss mapping
    # final_profit_and_loss = map_profit_and_loss(profit_and_loss_mapping, field_and_values)
    #
    # # Earnings in Foreign Exchange mapping
    # final_earnings_in_foreign_exchange = map_earnings_in_foreign_exchange(earnings_in_foreign_exchange_mapping, field_and_values)
    #
    # # Expenditure in Foreign Exchange mapping
    # final_expenditure_in_foreign_exchange = map_expenditure_in_foreign_exchange(expenditure_in_foreign_exchange_mapping, field_and_values)
    #
    # # Financial Parameters Profit and Loss mapping
    final_financial_parameter_profit_and_loss = map_financial_parameter_profit_and_loss(financial_parameter_profit_and_loss_mapping, field_and_values)

    # # Print results
    # print("Balance Sheets:")
    # print(json.dumps(final_balance_sheets, indent=4))
    # print("\nLong Term Borrowings:")
    # print(json.dumps(final_long_term_borrowings, indent=4))
    # print("\nShort Term Borrowings:")
    # print(json.dumps(final_short_term_borrowings, indent=4))
    # print("\nLong Term Loans Unsecured:")
    # print(json.dumps(final_long_term_loans_unsecured, indent=4))
    # print("\nLong Term Loans Doubtful:")
    # print(json.dumps(final_long_term_loans_doubtful, indent=4))
    # print("\nTrade Receivables:")
    # print(json.dumps(final_trade_receivables, indent=4))
    # print("\nFinancial Parameters:")
    # print(json.dumps(final_financial_parameters, indent=4))
    # print("\nShare Capital Raised:")
    # print(json.dumps(final_share_capital_raised, indent=4))
    # print("\nProfit and Loss:")
    # print(json.dumps(final_profit_and_loss, indent=4))
    # print("\nEarnings in Foreign Exchange:")
    # print(json.dumps(final_earnings_in_foreign_exchange, indent=4))
    # print("\nExpenditure in Foreign Exchange:")
    # print(json.dumps(final_expenditure_in_foreign_exchange, indent=4))
    print("\nFinancial Parameters Profit and Loss:")
    print(json.dumps(final_financial_parameter_profit_and_loss, indent=4))  