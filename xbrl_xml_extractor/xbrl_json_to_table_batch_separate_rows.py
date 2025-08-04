"""
xbrl_json_to_table_batch_separate_rows.py

This script 
    - batch-processes all JSON files in the XBRL_XML_JSON directory, 
    - extracts tabular data with each scenario as a separate row,
    - and saves it as CSV files in the XBRL_XML_JSON_TABLE directory. 
It also creates filtered CSVs for specific element names. 
The script logs its progress and errors for easier debugging and traceability.

Key Features:
    - Creates separate rows for each scenario dimension (normalized table structure)
    - Extracts comprehensive entity, period, and namespace information
    - Creates both full and filtered CSV files
    - Robust error handling and logging
    - Filename sanitization for Windows compatibility
"""

import pandas as pd
import json
import os
import logging
import re
import time

def sanitize_filename(filename):
    """
    Sanitize filename by removing or replacing problematic characters
    """
    # Remove or replace problematic characters
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Remove or replace other problematic characters
    filename = re.sub(r'[<>:"/\\|?*()]', '_', filename)
    
    # Remove multiple consecutive underscores
    filename = re.sub(r'_+', '_', filename)
    
    # Limit filename length (Windows has a 260 character path limit)
    if len(filename) > 200:
        name, ext = os.path.splitext(filename)
        filename = name[:200-len(ext)] + ext
    
    # Remove trailing periods and spaces (not allowed on Windows)
    filename = filename.rstrip('. ')
    
    return filename

def safe_file_write(df, file_path, max_retries=3, retry_delay=1):
    """
    Safely write DataFrame to CSV with error handling and retries
    """
    for attempt in range(max_retries):
        try:
            df.to_csv(file_path, index=False)
            return True
        except PermissionError:
            if attempt < max_retries - 1:
                logging.warning(f"Permission denied for {file_path}, retrying in {retry_delay} seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                logging.error(f"Permission denied for {file_path}. Please ensure:")
                logging.error("  1. The file is not open in Excel or another program")
                logging.error("  2. You have write permissions to the directory")
                logging.error("  3. The file is not set to read-only")
                return False
        except Exception as e:
            logging.error(f"Unexpected error writing to {file_path}: {e}")
            return False
    return False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Set up input and output directories
json_folder = os.path.join(os.path.dirname(__file__), '..', 'XBRL_XML_JSON')
csv_folder = os.path.join(os.path.dirname(__file__), '..', 'XBRL_XML_JSON_TABLE')

# Create output directory and test write permissions
try:
    os.makedirs(csv_folder, exist_ok=True)
    # Test write permissions by creating a temporary file
    test_file = os.path.join(csv_folder, 'test_write_permission.tmp')
    with open(test_file, 'w') as f:
        f.write('test')
    os.remove(test_file)
    logging.info(f"Output directory: {csv_folder}")
except PermissionError:
    logging.error(f"Permission denied: Cannot write to output directory {csv_folder}")
    logging.error("Please check directory permissions and try again.")
    exit(1)
except Exception as e:
    logging.error(f"Error setting up output directory {csv_folder}: {e}")
    exit(1)

# List of element names to filter
filter_elements = [
    "RevenueFromOperations",
    "ProfitBeforeExceptionalItemsAndTax",
    "FinanceCosts",
    "DepreciationDepletionAndAmortizationExpense",
    "ProfitBeforeTax",
    "ProfitLossForPeriodFromContinuingOperations",
    "BasicEarningsLossPerShare",
    "DilutedEarningsLossPerShare",
    "Equity",
    "CashFlowsFromUsedInOperations",
    "CostOfMaterialsConsumed",
    "PurchasesOfStockInTrade",
    "ChangesInInventoriesOfFinishedGoodsWorkInProgressAndStockInTrade",
    "EmployeeBenefitExpense",
    "FinanceCosts",
    "TaxExpense",
    "BorrowingsCurrent",
    "BorrowingsNonCurrent",
    "Borrowings",
    "SubclassOfBorrowingsAxis",
    "EquityShareCapital",
    "OtherEquity",
    "TradeReceivablesCurrent",
    "PropertyPlantAndEquipment",
    "GrossCarryingAmountMember",
    "CarryingAmountAccumulatedDepreciationAndGrossCarryingAmountAxis",
    "PropertyPlantAndEquipment",
    "CapitalWorkInProgress",
    "CurrentInvestments",
    "NoncurrentInvestments",
    "CurrentAssets",
    "CurrentLiabilities",
    "Inventories",
    "TradeReceivablesCurrent",
    "BankBalanceOtherThanCashAndCashEquivalents",
    "CashAndCashEquivalents",
    "Assets"
]

# Check if input directory exists
if not os.path.exists(json_folder):
    logging.error(f"Input directory does not exist: {json_folder}")
    exit(1)

json_files = [f for f in os.listdir(json_folder) if f.lower().endswith('.json')]
if not json_files:
    logging.info(f"No JSON files found in {json_folder}")
    exit(0)
else:
    logging.info(f"Found {len(json_files)} JSON file(s) in {json_folder}")

# Check for potentially open CSV files (common issue)
existing_csv_files = [f for f in os.listdir(csv_folder) if f.lower().endswith('.csv')]
if existing_csv_files:
    logging.info(f"Found {len(existing_csv_files)} existing CSV files in output directory")
    logging.info("If you encounter permission errors, please ensure CSV files are not open in Excel or other programs")

for json_file in json_files:
    json_path = os.path.join(json_folder, json_file)
    
    # Sanitize the base filename to avoid file system issues
    base_filename = os.path.splitext(json_file)[0]
    sanitized_base = sanitize_filename(base_filename)
    
    csv_file = sanitized_base + '_separate_rows.csv'
    filtered_csv_file = sanitized_base + '_separate_rows_filtered.csv'
    
    csv_path = os.path.join(csv_folder, csv_file)
    filtered_csv_path = os.path.join(csv_folder, filtered_csv_file)
    
    # Log original and sanitized filenames if they differ
    if base_filename != sanitized_base:
        logging.info(f"Sanitized filename: '{base_filename}' -> '{sanitized_base}'")
    
    logging.info(f"Processing {json_file} ...")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # Prepare a list to hold the extracted data for the DataFrame
        extracted_data = []
        total_scenarios = 0
        elements_with_multiple_scenarios = 0
        total_rows_created = 0

        # Iterate through each item in the JSON data
        for item in json_data:
            element_name = item.get("elementName")
            namespace_prefix = item.get("namespacePrefix")
            namespace_uri = item.get("namespaceURI")
            value = item.get("value")
            unit_ref = item.get("unitRef")
            decimals = item.get("decimals")
            context_ref = item.get("contextRef")

            # Accessing nested contextDetails and period information
            context_details = item.get("contextDetails", {})
            period_details = context_details.get("period", {})

            period_type = period_details.get("type")
            start_date = period_details.get("startDate")
            instant_date = period_details.get("instant") # This is for 'instant' type periods
            end_date = period_details.get("endDate")

            # Combine startDate and instant into a single column, prioritizing instant if period type is 'instant'
            start_or_instant_date = instant_date if period_type == "instant" else start_date

            # Entity information extraction
            entity_details = context_details.get("entity", {})
            entity_scheme = entity_details.get("scheme", "")
            entity_value = entity_details.get("value", "")

            # Scenario extraction - CREATE SEPARATE ROWS FOR EACH SCENARIO
            scenario_list = context_details.get("scenario", [])
            
            if scenario_list and isinstance(scenario_list, list):
                # Create a separate row for each scenario
                scenario_count = len(scenario_list)
                total_scenarios += scenario_count
                
                if scenario_count > 1:
                    elements_with_multiple_scenarios += 1
                
                for scenario_index, scenario in enumerate(scenario_list):
                    scenario_type = scenario.get("type", "")
                    scenario_dimension = scenario.get("dimension", "")
                    scenario_value = scenario.get("value", "")
                    
                    # Create a dictionary for the current row with desired columns
                    row_data = {
                        "ElementName": element_name,
                        "NamespacePrefix": namespace_prefix,
                        "NamespaceURI": namespace_uri,
                        "Value": value,
                        "UnitRef": unit_ref,
                        "Decimals": decimals,
                        "PeriodType": period_type,
                        "StartDate_Instant": start_or_instant_date,
                        "EndDate": end_date,
                        "ContextRef": context_ref,
                        "EntityScheme": entity_scheme,
                        "EntityValue": entity_value,
                        "ScenarioIndex": scenario_index + 1,  # 1-based index
                        "ScenarioType": scenario_type,
                        "ScenarioDimension": scenario_dimension,
                        "ScenarioValue": scenario_value,
                        "TotalScenariosForElement": scenario_count
                    }
                    extracted_data.append(row_data)
                    total_rows_created += 1
            else:
                # No scenarios - create one row with empty scenario fields
                row_data = {
                    "ElementName": element_name,
                    "NamespacePrefix": namespace_prefix,
                    "NamespaceURI": namespace_uri,
                    "Value": value,
                    "UnitRef": unit_ref,
                    "Decimals": decimals,
                    "PeriodType": period_type,
                    "StartDate_Instant": start_or_instant_date,
                    "EndDate": end_date,
                    "ContextRef": context_ref,
                    "EntityScheme": entity_scheme,
                    "EntityValue": entity_value,
                    "ScenarioIndex": 0,  # 0 indicates no scenarios
                    "ScenarioType": "",
                    "ScenarioDimension": "",
                    "ScenarioValue": "",
                    "TotalScenariosForElement": 0
                }
                extracted_data.append(row_data)
                total_rows_created += 1

        # Create the Pandas DataFrame from the extracted data
        df = pd.DataFrame(extracted_data)
        
        # Log processing statistics
        logging.info(f"Processed {len(json_data)} elements with {total_scenarios} total scenarios")
        logging.info(f"Elements with multiple scenarios: {elements_with_multiple_scenarios}")
        logging.info(f"Total rows created: {total_rows_created}")

        # Save the DataFrame as CSV with error handling
        if safe_file_write(df, csv_path):
            logging.info(f"Saved full CSV to {csv_path} ({len(df)} rows, {len(df.columns)} columns)")
        else:
            logging.error(f"Failed to save full CSV to {csv_path}")
            continue  # Skip to next file if we can't write the main CSV

        # Filter DataFrame and save filtered CSV
        filtered_df = df[df['ElementName'].isin(filter_elements)]
        if safe_file_write(filtered_df, filtered_csv_path):
            logging.info(f"Saved filtered CSV to {filtered_csv_path} ({len(filtered_df)} rows)")
        else:
            logging.error(f"Failed to save filtered CSV to {filtered_csv_path}")
        
        # Log some sample scenario information if available
        multi_scenario_elements = df[df['TotalScenariosForElement'] > 1]
        if not multi_scenario_elements.empty:
            sample_element = multi_scenario_elements.iloc[0]
            logging.info(f"Sample multi-scenario element: {sample_element['ElementName']} "
                        f"with {sample_element['TotalScenariosForElement']} scenarios (showing scenario {sample_element['ScenarioIndex']})")
            
        # Show data expansion summary
        original_elements = len(json_data)
        final_rows = len(df)
        expansion_ratio = final_rows / original_elements if original_elements > 0 else 0
        logging.info(f"Data expansion: {original_elements} elements -> {final_rows} rows (ratio: {expansion_ratio:.2f})")
        
    except Exception as e:
        logging.error(f"Failed to process {json_file}: {e}")

logging.info("Batch conversion completed!")