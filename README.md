# PDF Attachment Extractor

A Python script to extract attachments from PDF files within zip archives while maintaining the original directory structure.

## Features

- Processes multiple zip files containing PDFs
- Extracts attachments from PDF files
- Maintains original directory structure in output
- Handles both embedded files and annotation attachments
- Skips numeric attachment IDs
- Creates organized output structure

## Requirements

- Python 3.x
- pypdf library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pdf-attachment-extractor.git
cd pdf-attachment-extractor
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Create an `Input_data` folder in the project directory
2. Place your zip files containing PDFs in the `Input_data` folder
3. Run the script:
```bash
python main.py
```

The script will:
- Create an `Extracted_data` folder
- Process each zip file in `Input_data`
- Extract attachments from all PDFs
- Maintain the original directory structure in `Extracted_data`

## Output Structure

```
Input_data/
    zip1.zip
        folder1/
            doc1.pdf
            doc2.pdf
        folder2/
            doc3.pdf
    zip2.zip
        doc4.pdf
        doc5.pdf

Extracted_data/
    zip1/
        folder1/
            doc1/
                [extracted attachments]
            doc2/
                [extracted attachments]
        folder2/
            doc3/
                [extracted attachments]
    zip2/
        doc4/
            [extracted attachments]
        doc5/
            [extracted attachments]
```

## License

MIT License

## Data Pipeline Script: `run_data_pipeline.py`

This script automates the end-to-end data extraction and processing pipeline for PDF, XML, and XBRL files. It is designed to be run from the project root and uses the system Python interpreter.

### What It Does
1. **Extracts XBRL attachments** from PDFs using `extract_xbrl_attachments.py`.
2. **Identifies and separates** XBRL and non-XBRL files using `get_xbrl_and_non_xbrl_files.py`.
3. **Waits for required files** to appear in `No_XBRL/` and `XBRL_XML/` directories.
4. **Processes files**:
   - Maps tables from non-XBRL PDFs (`pdf_table_extractor/pdf_no_xbrl_table_mapper.py`).
   - Converts XBRL XML files to JSON (`xbrl_xml_extractor/xbrl_xml_to_json_batch.py`).
   - Converts XBRL JSON files to tables (`xbrl_xml_extractor/xbrl_json_to_table_batch.py`).

### Logging & Error Handling
- All actions and outputs are logged to both the console and `pipeline.log`.
- Errors are highlighted in bold red in the console and clearly marked in the log file.
- The pipeline continues execution even if a step fails, but errors are highly visible.

### Usage
From the project root, run:

```bash
python run_data_pipeline.py
```

### Customization
- The script uses the system Python. To use a virtual environment, modify the script to activate your environment before running.
- Timeout and polling intervals for file checks can be adjusted in the script.

### Best Practices Followed
- Robust logging with timestamps and error highlighting.
- Sequential, dependency-aware execution.
- Graceful error handling and continuation.
- Clear documentation and maintainable code structure.

See the top of `run_data_pipeline.py` for further inline documentation. 