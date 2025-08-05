# MGT7 JSON Transformation Guide

This document explains how to use the new JSON transformation functionality for MGT7 forms in the PDF extraction pipeline.

## Overview

The enhanced `extract_pdf_info.py` module now includes powerful JSON transformation capabilities that make MGT7 data easy to work with and convert to various formats.

## New Functions Added

### 1. `transform_mgt7_to_json(extracted_info, pdf_filename="")`
Converts extracted MGT7 data into a clean, structured JSON format.

**Features:**
- Flattened structure for easy CSV conversion
- Clear, descriptive field names
- Timestamp tracking
- Cleaned and formatted data

**Example JSON Structure:**
```json
{
  "source_file": "company_mgt7.pdf",
  "form_type": "MGT7",
  "extraction_timestamp": "2024-01-15 10:30:00",
  "company_cin": "L12345AB2020PLC123456",
  "company_name": "Example Company Ltd",
  "company_type": "Private Company",
  "business_activities": [
    {
      "serial_number": "1",
      "main_activity_group_code": "12345",
      "main_activity_description": "Manufacturing",
      "business_activity_code": "67890",
      "business_activity_description": "Software Development",
      "percentage_turnover": "85.5"
    }
  ]
}
```

### 2. `save_mgt7_json(mgt7_json, output_file)`
Saves JSON data to a file with proper formatting.

### 3. `mgt7_json_to_csv_rows(mgt7_json)`
Converts JSON data to flat dictionaries suitable for CSV export.

**Features:**
- One row per business activity
- Company information repeated for each activity
- All fields flattened for easy CSV conversion

### 4. `process_all_mgt7_to_json_csv(input_dir, output_json_dir, output_csv_file)`
Batch processes all MGT7 PDFs and exports to both JSON and CSV formats.

## Usage Examples

### Basic Usage - Single File

```python
from extract_pdf_info import process_pdf, transform_mgt7_to_json, save_mgt7_json

# Process a single PDF
cin, financial_year, extracted_info, form_type = process_pdf("path/to/mgt7.pdf")

if form_type == 'MGT7':
    # Transform to JSON
    mgt7_json = transform_mgt7_to_json(extracted_info, "mgt7.pdf")
    
    # Save JSON file
    save_mgt7_json(mgt7_json, "output.json")
    
    # Get CSV-ready data
    csv_rows = mgt7_json_to_csv_rows(mgt7_json)
```

### Batch Processing - All Files

```python
from extract_pdf_info import process_all_mgt7_to_json_csv

# Process all MGT7 files
stats = process_all_mgt7_to_json_csv(
    input_dir="No_XBRL",
    output_json_dir="MGT7_JSON",
    output_csv_file="all_mgt7_data.csv"
)

print(f"Processed {stats['mgt7_files']} MGT7 files")
```

### Using the Enhanced Main Function

The main function now offers three modes:

```bash
python extract_pdf_info.py
```

**Mode Options:**
1. **Display mode**: Show detailed information for each PDF
2. **Export mode**: Export all MGT7 data to JSON and CSV
3. **Both modes**: Display and export

## Data Structure Benefits

### JSON Format Advantages:
- **Easy to read**: Clear field names and structure
- **Programmatically accessible**: Easy to parse and manipulate
- **Timestamped**: Tracks when extraction occurred
- **Complete**: Contains all MGT7 form data

### CSV Format Advantages:
- **Flat structure**: One row per business activity
- **Excel compatible**: Can be opened directly in Excel
- **Database ready**: Easy to import into databases
- **Analysis friendly**: Perfect for data analysis tools

## File Outputs

When using batch processing, you'll get:

1. **Individual JSON files**: One per MGT7 PDF in the output directory
   - Format: `filename_mgt7.json`
   - Contains complete structured data for each company

2. **Combined CSV file**: All companies in one spreadsheet
   - One row per business activity
   - Company information repeated for each activity
   - Perfect for analysis and reporting

## Demo Script

Run the demonstration script to see the functionality in action:

```bash
python demo_mgt7_json.py
```

This will:
- Process a sample MGT7 file
- Show JSON transformation
- Demonstrate batch processing
- Create example output files

## Field Mapping

The JSON format uses these standardized field names:

| Original Field | JSON Field Name | Description |
|---|---|---|
| CIN | company_cin | Corporate Identification Number |
| Company_Name | company_name | Company name |
| Type_Of_Company | company_type | Company type (decoded) |
| Address | registered_office_address | Cleaned address |
| Business_Activities | business_activities | Array of activities |

## Error Handling

The functions include robust error handling:
- File I/O errors are caught and reported
- Missing data is handled gracefully
- Statistics are provided for batch operations
- Clear error messages for troubleshooting

## Integration with Existing Pipeline

The new JSON functionality integrates seamlessly with your existing pipeline:
- Uses the same extraction functions
- Compatible with current PDF processing
- Extends rather than replaces existing functionality
- Maintains backward compatibility

---

For questions or issues, refer to the main project documentation or examine the function docstrings in `extract_pdf_info.py`.