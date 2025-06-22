import copy
import json

from pdf_table_extractor.mapping_config import (
    balance_sheet_mapping,
    long_term_borrowing_mapping,
    short_term_borrowing_mapping,
    long_term_loan_unsecured_mapping,
    long_term_loan_doubtful_mapping,
    trade_receivable_mapping,
    financial_parameters_mapping,
    share_capital_raised_mapping
)

from pdf_table_extractor.resulted_dict_for_testing import (
    balance_sheet_resulted_dictionary,
    long_term_resulted_dictionary,
    short_term_borrowings_resulted_dictionary,
    long_term_loans_resulted_dictionary,
    long_term_loans_doubtful_resulted_dictionary,
    trade_receivables_resulted_dictionary,
    financial_parameters_resulted_dictionary,
    share_capital_raised_resulted_dictionary
)

from pdf_table_extractor.balance_sheet_generator import (
    map_balance_sheet_data,
    map_long_term_borrowings,
    map_short_term_borrowings,
    map_long_term_loans_unsecured,
    map_long_term_loans_doubtful,
    map_trade_receivables,
    map_financial_parameters,
    map_share_capital_raised
)


def test_balance_sheet_mapping():
    """Test balance sheet mapping with static test data"""
    print("Testing Balance Sheet Mapping...")
    final_balance_sheets = map_balance_sheet_data(balance_sheet_mapping, balance_sheet_resulted_dictionary)
    print(json.dumps(final_balance_sheets, indent=4))
    print("\n" + "="*50 + "\n")


def test_long_term_borrowings_mapping():
    """Test long term borrowings mapping with static test data"""
    print("Testing Long Term Borrowings Mapping...")
    final_long_term_borrowings = map_long_term_borrowings(long_term_borrowing_mapping, long_term_resulted_dictionary)
    print(json.dumps(final_long_term_borrowings, indent=4))
    print("\n" + "="*50 + "\n")


def test_short_term_borrowings_mapping():
    """Test short term borrowings mapping with static test data"""
    print("Testing Short Term Borrowings Mapping...")
    final_short_term_borrowings = map_short_term_borrowings(short_term_borrowing_mapping, short_term_borrowings_resulted_dictionary)
    print(json.dumps(final_short_term_borrowings, indent=4))
    print("\n" + "="*50 + "\n")


def test_long_term_loans_unsecured_mapping():
    """Test long term loans unsecured mapping with static test data"""
    print("Testing Long Term Loans Unsecured Mapping...")
    final_long_term_loans_unsecured = map_long_term_loans_unsecured(long_term_loan_unsecured_mapping, long_term_loans_resulted_dictionary)
    print(json.dumps(final_long_term_loans_unsecured, indent=4))
    print("\n" + "="*50 + "\n")


def test_long_term_loans_doubtful_mapping():
    """Test long term loans doubtful mapping with static test data"""
    print("Testing Long Term Loans Doubtful Mapping...")
    final_long_term_loans_doubtful = map_long_term_loans_doubtful(long_term_loan_doubtful_mapping, long_term_loans_doubtful_resulted_dictionary)
    print(json.dumps(final_long_term_loans_doubtful, indent=4))
    print("\n" + "="*50 + "\n")


def test_trade_receivables_mapping():
    """Test trade receivables mapping with static test data"""
    print("Testing Trade Receivables Mapping...")
    final_trade_receivables = map_trade_receivables(trade_receivable_mapping, trade_receivables_resulted_dictionary)
    print(json.dumps(final_trade_receivables, indent=4))
    print("\n" + "="*50 + "\n")


def test_financial_parameters_mapping():
    """Test financial parameters mapping with static test data"""
    print("Testing Financial Parameters Mapping...")
    final_financial_parameters = map_financial_parameters(financial_parameters_mapping, financial_parameters_resulted_dictionary)
    print(json.dumps(final_financial_parameters, indent=4))
    print("\n" + "="*50 + "\n")


def test_share_capital_raised_mapping():
    """Test share capital raised mapping with static test data"""
    print("Testing Share Capital Raised Mapping...")
    final_share_capital_raised = map_share_capital_raised(share_capital_raised_mapping, share_capital_raised_resulted_dictionary)
    print(json.dumps(final_share_capital_raised, indent=4))
    print("\n" + "="*50 + "\n")


def run_all_tests():
    """Run all mapping tests with static test data"""
    print("Running All Balance Sheet Generator Tests with Static Data")
    print("="*60 + "\n")
    
    test_balance_sheet_mapping()
    test_long_term_borrowings_mapping()
    test_short_term_borrowings_mapping()
    test_long_term_loans_unsecured_mapping()
    test_long_term_loans_doubtful_mapping()
    test_trade_receivables_mapping()
    test_financial_parameters_mapping()
    test_share_capital_raised_mapping()
    
    print("All tests completed!")


if __name__ == "__main__":
    run_all_tests() 