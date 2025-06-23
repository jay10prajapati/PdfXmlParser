# PDF & XBRL Data Pipeline

This repository provides tools for extracting attachments from PDFs (including those inside ZIP archives), as well as a robust, automated pipeline for processing PDF, XML, and XBRL files.

## Features

- **Extracts attachments** from PDF files, including those inside ZIP archives.
- **Maintains original directory structure** in output.
- **Handles both embedded files and annotation attachments** in PDFs.
- **Automated data pipeline** for sequential processing of PDF, XML, and XBRL files.
- **Robust logging and error handling** throughout the pipeline.

## Requirements

- Python 3.x
- Install dependencies with:
  ```bash
  pip install -r requirements.txt
  ```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jay10prajapati/PdfXmlParser.git
   cd PdfXmlParser
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. PDF Attachment Extraction

1. Place your ZIP files containing PDFs in the `Input_data/` folder.
2. Run the main extraction script:
   ```bash
   python main.py
   ```
   - This will create an `Extracted_data/` folder and extract all attachments from PDFs, preserving the original directory structure.

#### Output Structure Example

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

### 2. Data Pipeline Script: `run_data_pipeline.py`

This script automates the end-to-end data extraction and processing pipeline for PDF, XML, and XBRL files. **Run this from the project root.**

#### What It Does

1. **Stage 1: Extraction**
   - Runs `get_xbrl_and_non_xbrl_files.py` to identify and separate XBRL and non-XBRL files.
   - Then runs `extract_xbrl_attachments.py` to extract XBRL attachments from PDFs.
2. **Stage 2: File Check**
   - Waits for required files to appear in `No_XBRL/` and `XBRL_XML/` directories.
3. **Stage 3: Processing**
   - Maps tables from non-XBRL PDFs (`pdf_table_extractor/pdf_no_xbrl_table_mapper.py`).
   - Converts XBRL XML files to JSON (`xbrl_xml_extractor/xbrl_xml_to_json_batch.py`).
   - Converts XBRL JSON files to tables (`xbrl_xml_extractor/xbrl_json_to_table_batch.py`).

#### Logging & Error Handling

- All actions and outputs are logged to both the console and `pipeline.log`.
- Errors are highlighted in bold red in the console and clearly marked in the log file.
- The pipeline continues execution even if a step fails, but errors are highly visible.

#### Usage

From the project root, run:
```bash
python run_data_pipeline.py
```

#### Customization

- The script uses the system Python. To use a virtual environment, activate it before running the script.
- Timeout and polling intervals for file checks can be adjusted in the script.

#### Best Practices Followed

- Robust logging with timestamps and error highlighting.
- Sequential, dependency-aware execution.
- Graceful error handling and continuation.
- Clear documentation and maintainable code structure.

See the top of `run_data_pipeline.py` for further inline documentation.

## License

MIT License 