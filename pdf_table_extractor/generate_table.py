#!/usr/bin/env python3
"""
Simple command-line interface for generating table results from PDF forms.
"""

import sys
import os

# Add the pdf_table_extractor module to the path
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pdf_table_extractor'))

from table_generator import generate_table_result, print_available_tables


def main():
    """Main function with interactive interface"""
    print("=" * 60)
    print("PDF Table Generator")
    print("=" * 60)
    
    # Show available tables
    print_available_tables()
    
    while True:
        try:
            # Get table number from user
            table_input = input("\nEnter table number (or 'q' to quit): ").strip()
            
            if table_input.lower() in ['q', 'quit', 'exit']:
                print("Goodbye!")
                break
            
            table_number = int(table_input)
            
            # Get PDF file path (optional)
            pdf_path = input("Enter PDF file path (or press Enter for default): ").strip()
            
            if not pdf_path:
                # Use default PDF file path
                project_root = os.path.dirname(os.path.abspath(__file__))
                pdf_path = os.path.join(project_root, "..","No_XBRL", "2__Form_AOC-4-13122024_signed.pdf")
            
            # Check if PDF file exists
            if not os.path.exists(pdf_path):
                print(f"Error: PDF file not found at {pdf_path}")
                continue
            
            # Generate and display result
            print(f"\nGenerating result for Table {table_number}...")
            result = generate_table_result(table_number, pdf_path)
            
            print(f"\n=== {result['table_name']} (Table {result['table_number']}) ===")
            print("=" * 60)
            
            # Pretty print the JSON result
            import json
            print(json.dumps(result['data'], indent=4))
            
            # Ask if user wants to continue
            continue_input = input("\nGenerate another table? (y/n): ").strip().lower()
            if continue_input not in ['y', 'yes']:
                print("Goodbye!")
                break
                
        except ValueError as e:
            print(f"Error: {e}")
            print("Please enter a valid table number.")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main() 