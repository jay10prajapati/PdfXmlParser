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