"""
xbrl_json_to_table_batch.py

This script 
    - batch-processes all JSON files in the XBRL_XML_JSON directory, 
    - extracts tabular data, 
    - and saves it as CSV files in the XBRL_XML_JSON_TABLE directory. 
It also creates filtered CSVs for specific element names. 
The script logs its progress and errors for easier debugging and traceability.
"""

import pandas as pd
import json
import os
import logging

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
os.makedirs(csv_folder, exist_ok=True)

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

json_files = [f for f in os.listdir(json_folder) if f.lower().endswith('.json')]
if not json_files:
    logging.info(f"No JSON files found in {json_folder}")
else:
    logging.info(f"Found {len(json_files)} JSON file(s) in {json_folder}")

for json_file in json_files:
    json_path = os.path.join(json_folder, json_file)
    csv_file = os.path.splitext(json_file)[0] + '.csv'
    csv_path = os.path.join(csv_folder, csv_file)
    filtered_csv_path = os.path.join(csv_folder, os.path.splitext(json_file)[0] + '_filtered.csv')
    logging.info(f"Processing {json_file} ...")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # Prepare a list to hold the extracted data for the DataFrame
        extracted_data = []

        # Iterate through each item in the JSON data
        for item in json_data:
            element_name = item.get("elementName")
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

            # Scenario extraction (first scenario if present)
            scenario_list = context_details.get("scenario", [])
            if scenario_list and isinstance(scenario_list, list):
                scenario = scenario_list[0]
                scenario_type = scenario.get("type", "")
                scenario_dimension = scenario.get("dimension", "")
                scenario_value = scenario.get("value", "")
            else:
                scenario_type = ""
                scenario_dimension = ""
                scenario_value = ""

            # Create a dictionary for the current row with desired columns
            row_data = {
                "ElementName": element_name,
                "Value": value,
                "unitref": unit_ref,
                "decimals": decimals,
                "period_type": period_type,
                "startDate/instant": start_or_instant_date,
                "endDate": end_date,
                "contextRef": context_ref,
                "scenario_type": scenario_type,
                "scenario_dimension": scenario_dimension,
                "scenario_value": scenario_value
            }
            extracted_data.append(row_data)

        # Create the Pandas DataFrame from the extracted data
        df = pd.DataFrame(extracted_data)

        # Save the DataFrame as CSV
        df.to_csv(csv_path, index=False)
        logging.info(f"Saved CSV to {csv_path}")

        # Filter DataFrame and save filtered CSV
        filtered_df = df[df['ElementName'].isin(filter_elements)]
        filtered_df.to_csv(filtered_csv_path, index=False)
        logging.info(f"Saved filtered CSV to {filtered_csv_path}")
    except Exception as e:
        logging.error(f"Failed to process {json_file}: {e}")
