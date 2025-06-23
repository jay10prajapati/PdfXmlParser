"""
Data Pipeline Script for PDF/XML/XBRL Processing

This script orchestrates the following steps:

1. Extract XBRL attachments from PDFs.
2. Identify and separate XBRL and non-XBRL files.
3. Once all files are available in No_XBRL/ and XBRL_XML/, process them:
   a. Map tables from non-XBRL PDFs.
   b. Convert XBRL XML files to JSON.
   c. Convert XBRL JSON files to tables.

- Logs all actions with timestamps and clear error highlighting.
- Continues execution on errors, but errors are highly visible in logs.
- Designed to be run from the project root with system Python.

Usage:
    python run_data_pipeline.py
"""
import subprocess
import logging
import os
import sys
import time
from datetime import datetime

# --- Logging Setup ---
LOG_FILE = 'pipeline.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

BOLD_RED = '\033[1;31m'
RESET = '\033[0m'


def log_error(msg):
    logging.error(f"{BOLD_RED}{msg}{RESET}")

def run_script(script_path, description):
    logging.info(f"Starting: {description} ({script_path})")
    try:
        result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True)
        logging.info(f"Completed: {description}\nOutput:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        log_error(f"FAILED: {description}\nError Output:\n{e.stderr}")
    except Exception as e:
        log_error(f"Exception during {description}: {e}")

def wait_for_files(directory, min_files=1, timeout=300, poll_interval=5):
    """Wait until at least min_files are present in directory, or timeout (seconds) is reached."""
    logging.info(f"Waiting for at least {min_files} file(s) in {directory} (timeout: {timeout}s)...")
    waited = 0
    while waited < timeout:
        try:
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            if len(files) >= min_files:
                logging.info(f"Found {len(files)} file(s) in {directory}.")
                return True
        except Exception as e:
            log_error(f"Error checking files in {directory}: {e}")
        time.sleep(poll_interval)
        waited += poll_interval
    log_error(f"Timeout: Not enough files in {directory} after {timeout} seconds.")
    return False

def main():
    # Stage 1: Extraction (run sequentially, as per new order)
    run_script('get_xbrl_and_non_xbrl_files.py', 'Identify and separate XBRL and non-XBRL files')
    run_script('extract_xbrl_attachments.py', 'Extract XBRL attachments from PDFs')

    # Stage 2: Wait for required files
    no_xbrl_ready = wait_for_files('No_XBRL', min_files=1)
    xbrl_xml_ready = wait_for_files('XBRL_XML', min_files=1)

    if not (no_xbrl_ready and xbrl_xml_ready):
        log_error("Required files not found in No_XBRL or XBRL_XML. Skipping further processing.")
        return

    # Stage 3: Processing (run sequentially)
    run_script(os.path.join('pdf_table_extractor', 'pdf_no_xbrl_table_mapper.py'), 'Map tables from non-XBRL PDFs')
    run_script(os.path.join('xbrl_xml_extractor', 'xbrl_xml_to_json_batch.py'), 'Convert XBRL XML files to JSON')
    run_script(os.path.join('xbrl_xml_extractor', 'xbrl_json_to_table_batch.py'), 'Convert XBRL JSON files to tables')

    logging.info("Pipeline execution completed.")

if __name__ == "__main__":
    main() 