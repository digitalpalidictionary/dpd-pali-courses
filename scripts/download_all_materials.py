"""
Script to download latest course materials from Google Docs as a ZIP archive.
Facilitates keeping Markdown source files in sync with original sources if needed.
"""
import requests
import os
import zipfile
import re
import sys # Added for sys.exit()
from tools.printer import printer as pr

# --- Configuration ---
BPC_INFO = [
    {"name": "Beginner Pāli Course", "url": "https://docs.google.com/document/d/1FOKjmABrz6reeFDBWwpjDq1_J3m83-bd1TMXPcgEHmY/"},
    {"name": "BPC Exercises", "url": "https://docs.google.com/document/d/1jqKL8Nlghi1T2m9y0BAN17yk2Na-34fFan1tMI4mrGw/"},
    {"name": "BPC Key to Exercises", "url": "https://docs.google.com/document/d/1AX4wqoVokRfTfr89EKxHPC1Yb80HKa2sqxX4q-nofso/"},
]

IPC_INFO = [
    {"name": "Intermediate Pāli Course", "url": "https://docs.google.com/document/d/1qsYPFOifOUN2HIbFCH7kaglJyI2CVd9MH9A6Kt9rSxg/"},
    {"name": "IPC Exercises", "url": "https://docs.google.com/document/d/15x3PRqzW5VRuFQSJ-oOvKOZ2y1tNIgwYdhDWd-plHRI/"},
    {"name": "IPC Key to Exercises", "url": "https://docs.google.com/document/d/1AXSKpmYYuiinQYTBJ133rMZJc53qbZSLr_7UE-syofg/"},
]

OUTPUT_BASE_DIR = "sources"  # Base directory for all generated files
# Updated ZIP Filenames
BPC_PDF_ZIP_FILENAME = "beginner_pali_course_pdfs.zip"
BPC_DOCX_ZIP_FILENAME = "beginner_pali_course_docx.zip"
IPC_PDF_ZIP_FILENAME = "intermediate_pali_course_pdfs.zip"
IPC_DOCX_ZIP_FILENAME = "intermediate_pali_course_docx.zip"
# --- End Configuration ---

def sanitize_filename(name):
    """Replaces spaces with underscores and removes other problematic characters for filenames."""
    name = name.replace(" ", "_")
    # Keep alphanumeric, underscore, hyphen, period. Remove others.
    return re.sub(r'[^\w\-_.]', '', name)

def extract_doc_id(url):
    """Extracts Google Doc ID from its URL."""
    match = re.search(r'/document/d/([a-zA-Z0-9-_]+)', url)
    if match:
        return match.group(1)
    pr.warning(f"Could not extract document ID from URL: {url}")
    return None

def download_google_doc(doc_id, base_filename, export_format, download_to_dir):
    """Downloads a Google Doc in the specified format (pdf or docx)."""
    if not doc_id:
        return None

    output_filename = f"{base_filename}.{export_format}"
    output_filepath = os.path.join(download_to_dir, output_filename)
    export_url = f"https://docs.google.com/document/d/{doc_id}/export?format={export_format}"

    pr.green(f"Downloading {output_filename}")
    try:
        response = requests.get(export_url, stream=True)
        response.raise_for_status()
        with open(output_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        pr.yes("ok")
        return output_filepath
    except requests.exceptions.RequestException as e:
        pr.no("failed")
        pr.warning(str(e))
        return None

def create_zip_archive(file_paths, zip_filename, archive_base_dir):
    """Creates a ZIP archive from a list of file paths."""
    zip_filepath = os.path.join(archive_base_dir, zip_filename)
    pr.green(f"Creating {zip_filename}")
    try:
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in file_paths:
                if file_path and os.path.exists(file_path):
                    zf.write(file_path, arcname=os.path.basename(file_path))
                else:
                    pr.warning(f"File not found, skipping: {file_path}")
        pr.yes("ok")
        return zip_filepath
    except Exception as e:
        pr.no("failed")
        pr.warning(str(e))
        return None

def process_course_documents(course_docs_info, course_name_prefix, output_dir):
    """
    Downloads PDF and DOCX versions of documents for a specific course.
    Returns a tuple of (list_of_pdf_paths, list_of_docx_paths).
    If any download fails, returns (None, None) to signal failure.
    """
    downloaded_pdfs = []
    downloaded_docx_files = []

    pr.title(f"{course_name_prefix} Pāli Course")

    for doc_info in course_docs_info:
        original_name = doc_info["name"]
        doc_url = doc_info["url"]
        doc_id = extract_doc_id(doc_url)
        if not doc_id:
            pr.warning(f"Skipping '{original_name}' — missing document ID.")
            continue

        base_filename = sanitize_filename(original_name)

        pdf_filepath = download_google_doc(doc_id, base_filename, "pdf", output_dir)
        if pdf_filepath:
            downloaded_pdfs.append(pdf_filepath)
        else:
            pr.no(f"PDF failed: {original_name}")
            return None, None

        docx_filepath = download_google_doc(doc_id, base_filename, "docx", output_dir)
        if docx_filepath:
            downloaded_docx_files.append(docx_filepath)
        else:
            pr.no(f"DOCX failed: {original_name}")
            return None, None

    return downloaded_pdfs, downloaded_docx_files

def main():
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    all_downloads_successful = True

    bpc_pdfs, bpc_docx_files = process_course_documents(BPC_INFO, "Beginner", OUTPUT_BASE_DIR)
    if bpc_pdfs is None or bpc_docx_files is None:
        pr.no("Beginner course download failed")
        all_downloads_successful = False

    ipc_pdfs, ipc_docx_files = process_course_documents(IPC_INFO, "Intermediate", OUTPUT_BASE_DIR)
    if ipc_pdfs is None or ipc_docx_files is None:
        pr.no("Intermediate course download failed")
        all_downloads_successful = False

    if not all_downloads_successful:
        pr.error("Critical errors during download — aborting.")
        sys.exit(1)

    for paths, zip_name in [
        (bpc_pdfs, BPC_PDF_ZIP_FILENAME),
        (bpc_docx_files, BPC_DOCX_ZIP_FILENAME),
        (ipc_pdfs, IPC_PDF_ZIP_FILENAME),
        (ipc_docx_files, IPC_DOCX_ZIP_FILENAME),
    ]:
        if paths:
            create_zip_archive(paths, zip_name, OUTPUT_BASE_DIR)
        else:
            pr.warning(f"No files downloaded for {zip_name}")

    pr.info(f"Output: {os.path.abspath(OUTPUT_BASE_DIR)}")

if __name__ == "__main__":
    main()