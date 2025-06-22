# PDF Table Generator

This script allows you to generate structured data from PDF forms by specifying a table number. It extracts form fields from PDF files and maps them to predefined table structures.

## Available Tables

| Table Number | Table Name |
|--------------|------------|
| 1 | Balance Sheet |
| 2 | Long Term Borrowings |
| 3 | Short Term Borrowings |
| 4 | Long Term Loans Unsecured |
| 5 | Long Term Loans Doubtful |
| 6 | Trade Receivables |
| 7 | Financial Parameters |
| 8 | Share Capital Raised |
| 9 | Profit and Loss |

## Usage

### Method 1: Interactive Interface (Recommended)

Run the interactive script:

```bash
python generate_table.py
```

This will:
1. Show you all available tables
2. Ask you to enter a table number
3. Ask for a PDF file path (or use default)
4. Generate and display the result
5. Ask if you want to generate another table

### Method 2: Command Line Arguments

Run the table generator directly with arguments:

```bash
# Generate table 1 (Balance Sheet) with default PDF
python pdf_table_extractor/table_generator.py 1

# Generate table 2 (Long Term Borrowings) with custom PDF
python pdf_table_extractor/table_generator.py 2 /path/to/your/file.pdf
```

### Method 3: Programmatic Usage

You can also use the functions in your own Python code:

```python
from pdf_table_extractor.table_generator import generate_table_result

# Generate result for table 1
result = generate_table_result(1, "path/to/your/file.pdf")
print(result)
```

## Example Output

When you run the script, you'll get output like this:

```
=== Balance Sheet (Table 1) ===
{
    "Current balance sheet": {
        "EQUITY AND LIABILITIES": {
            "Shareholder's Fund": {
                "Share capital": "1000000",
                "Reserves and surplus": "500000",
                ...
            },
            ...
        },
        "ASSETS": {
            ...
        }
    },
    "Previous balance sheet": {
        ...
    }
}
```

## File Structure

- `generate_table.py` - Interactive command-line interface
- `pdf_table_extractor/table_generator.py` - Main table generation logic
- `pdf_table_extractor/mapping_config.py` - Table mapping configurations
- `No_XBRL/2__Form_AOC-4-13122024-signed.pdf` - Default PDF file

## Requirements

- Python 3.6+
- PyPDF2
- The PDF file must contain interactive form fields

## Error Handling

The script includes comprehensive error handling for:
- Invalid table numbers
- Missing PDF files
- PDF files without form fields
- Invalid input

## Notes

- The script automatically uses a default PDF file if none is specified
- All results are returned in JSON format for easy parsing
- The script supports both current and previous period data where applicable
- Table structures are predefined based on the AOC-4 form format 