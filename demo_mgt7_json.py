#!/usr/bin/env python3
"""
Demonstration script for MGT7 JSON transformation functionality.

This script shows how to use the new JSON transformation functions
to convert MGT7 PDF data into structured JSON and CSV formats.
"""

import os
from extract_pdf_info import (
    process_pdf, 
    transform_mgt7_to_json, 
    save_mgt7_json, 
    mgt7_json_to_csv_rows,
    process_all_mgt7_to_json_csv
)
import json

def demo_single_file():
    """Demonstrate processing a single MGT7 file."""
    print("=== SINGLE FILE DEMO ===")
    
    # Check if we have any MGT7 files to process
    input_dir = "No_XBRL"
    if not os.path.exists(input_dir):
        print(f"Directory '{input_dir}' not found. Creating demo data...")
        return
    
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("No PDF files found for demo")
        return
    
    # Process the first PDF file
    pdf_file = pdf_files[0]
    pdf_path = os.path.join(input_dir, pdf_file)
    
    print(f"Processing: {pdf_file}")
    
    # Extract information
    cin, financial_year, extracted_info, form_type = process_pdf(pdf_path)
    
    if form_type == 'MGT7' and extracted_info:
        print("✓ MGT7 form detected")
        
        # Transform to JSON
        mgt7_json = transform_mgt7_to_json(extracted_info, pdf_file)
        
        # Display JSON structure
        print("\n--- JSON Structure ---")
        print(f"Source File: {mgt7_json['source_file']}")
        print(f"Form Type: {mgt7_json['form_type']}")
        print(f"Timestamp: {mgt7_json['extraction_timestamp']}")
        print(f"Company CIN: {mgt7_json['company_cin']}")
        print(f"Company Name: {mgt7_json['company_name']}")
        print(f"Business Activities: {len(mgt7_json['business_activities'])}")
        
        # Save JSON file
        output_file = "demo_mgt7_output.json"
        if save_mgt7_json(mgt7_json, output_file):
            print(f"✓ JSON saved to: {output_file}")
        
        # Convert to CSV format
        csv_rows = mgt7_json_to_csv_rows(mgt7_json)
        print(f"✓ CSV format ready: {len(csv_rows)} rows, {len(csv_rows[0]) if csv_rows else 0} columns")
        
        # Show sample CSV data
        if csv_rows:
            print("\n--- Sample CSV Row (first 5 fields) ---")
            sample_row = csv_rows[0]
            for i, (key, value) in enumerate(sample_row.items()):
                if i >= 5:  # Show only first 5 fields
                    break
                print(f"{key}: {value}")
            print("...")
        
    else:
        print(f"✗ Not an MGT7 form (detected: {form_type})")

def demo_batch_processing():
    """Demonstrate batch processing of all MGT7 files."""
    print("\n=== BATCH PROCESSING DEMO ===")
    
    # Process all MGT7 files
    stats = process_all_mgt7_to_json_csv(
        input_dir="No_XBRL",
        output_json_dir="Demo_JSON_Output",
        output_csv_file="demo_mgt7_combined.csv"
    )
    
    print("\nBatch processing completed!")
    return stats

def main():
    """Main demonstration function."""
    print("MGT7 JSON Transformation Demo")
    print("="*40)
    
    # Demo single file processing
    demo_single_file()
    
    # Demo batch processing
    demo_batch_processing()
    
    print("\n" + "="*40)
    print("Demo completed!")
    print("\nFiles created:")
    print("- demo_mgt7_output.json (single file demo)")
    print("- Demo_JSON_Output/ (batch processing - individual JSON files)")
    print("- demo_mgt7_combined.csv (batch processing - combined CSV)")

if __name__ == "__main__":
    main()