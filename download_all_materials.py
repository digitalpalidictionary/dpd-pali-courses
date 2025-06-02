import requests
import os
import zipfile
import re

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

OUTPUT_BASE_DIR = "output_documents"  # Base directory for all generated files
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
    # Regex to find the ID in URLs like /document/d/DOC_ID/edit or /document/d/DOC_ID/
    match = re.search(r'/document/d/([a-zA-Z0-9-_]+)', url)
    if match:
        return match.group(1)
    else:
        print(f"Error: Could not extract document ID from URL: {url}")
        return None

def download_google_doc(doc_id, base_filename, export_format, download_to_dir):
    """Downloads a Google Doc in the specified format (pdf or docx)."""
    if not doc_id:
        return None

    file_extension = export_format
    # The export URL uses 'pdf' and 'docx' directly as format parameters.
    export_url = f"https://docs.google.com/document/d/{doc_id}/export?format={export_format}"
    
    output_filename = f"{base_filename}.{file_extension}"
    output_filepath = os.path.join(download_to_dir, output_filename)

    print(f"Downloading {output_filename} (doc_id: {doc_id})...")
    try:
        response = requests.get(export_url, stream=True)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)

        with open(output_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded: {output_filepath}")
        return output_filepath
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {output_filename}: {e}")
        return None

def create_zip_archive(file_paths, zip_filename, archive_base_dir):
    """Creates a ZIP archive from a list of file paths."""
    zip_filepath = os.path.join(archive_base_dir, zip_filename)
    print(f"Creating ZIP archive: {zip_filepath}...")
    try:
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in file_paths:
                if file_path and os.path.exists(file_path):
                    # arcname ensures the file is stored with its base name in the zip
                    arcname = os.path.basename(file_path)
                    zf.write(file_path, arcname=arcname)
                    print(f"  Added {arcname} to {zip_filename}")
                else:
                    print(f"  Warning: File not found or invalid, skipping: {file_path}")
        print(f"Successfully created ZIP: {zip_filepath}")
        return zip_filepath
    except Exception as e:
        print(f"Error creating ZIP archive {zip_filepath}: {e}")
        return None

def process_course_documents(course_docs_info, course_name_prefix, output_dir):
    """
    Downloads PDF and DOCX versions of documents for a specific course.
    Returns a tuple of (list_of_pdf_paths, list_of_docx_paths).
    """
    downloaded_pdfs = []
    downloaded_docx_files = []

    print(f"\n--- Processing {course_name_prefix} Pāli Course ---")

    for doc_info in course_docs_info:
        original_name = doc_info["name"]
        doc_url = doc_info["url"]

        print(f"\nProcessing document: '{original_name}'")
        doc_id = extract_doc_id(doc_url)
        if not doc_id:
            print(f"Skipping '{original_name}' due to missing document ID.")
            continue

        # Sanitize the original name to create a safe base filename
        base_filename = sanitize_filename(original_name)

        # Download as PDF
        pdf_filepath = download_google_doc(doc_id, base_filename, "pdf", output_dir)
        if pdf_filepath:
            downloaded_pdfs.append(pdf_filepath)

        # Download as DOCX
        docx_filepath = download_google_doc(doc_id, base_filename, "docx", output_dir)
        if docx_filepath:
            downloaded_docx_files.append(docx_filepath)
            
    return downloaded_pdfs, downloaded_docx_files

def main():
    # Ensure the base output directory exists
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)

    # Process Beginner Pāli Course
    bpc_pdfs, bpc_docx_files = process_course_documents(BPC_INFO, "Beginner", OUTPUT_BASE_DIR)
    
    # Process Intermediate Pāli Course
    ipc_pdfs, ipc_docx_files = process_course_documents(IPC_INFO, "Intermediate", OUTPUT_BASE_DIR)

    # Create ZIP archives for Beginner Pāli Course
    if bpc_pdfs:
        create_zip_archive(bpc_pdfs, BPC_PDF_ZIP_FILENAME, OUTPUT_BASE_DIR)
    else:
        print(f"No PDF files were downloaded for {BPC_PDF_ZIP_FILENAME} to archive.")

    if bpc_docx_files:
        create_zip_archive(bpc_docx_files, BPC_DOCX_ZIP_FILENAME, OUTPUT_BASE_DIR)
    else:
        print(f"No DOCX files were downloaded for {BPC_DOCX_ZIP_FILENAME} to archive.")

    # Create ZIP archives for Intermediate Pāli Course
    if ipc_pdfs:
        create_zip_archive(ipc_pdfs, IPC_PDF_ZIP_FILENAME, OUTPUT_BASE_DIR)
    else:
        print(f"No PDF files were downloaded for {IPC_PDF_ZIP_FILENAME} to archive.")

    if ipc_docx_files:
        create_zip_archive(ipc_docx_files, IPC_DOCX_ZIP_FILENAME, OUTPUT_BASE_DIR)
    else:
        print(f"No DOCX files were downloaded for {IPC_DOCX_ZIP_FILENAME} to archive.")

    print("\n--- Processing Complete ---")
    print(f"All output files are located in: {os.path.abspath(OUTPUT_BASE_DIR)}")
    
    # Print paths to created archives
    for zip_filename in [BPC_PDF_ZIP_FILENAME, BPC_DOCX_ZIP_FILENAME, IPC_PDF_ZIP_FILENAME, IPC_DOCX_ZIP_FILENAME]:
        if os.path.exists(os.path.join(OUTPUT_BASE_DIR, zip_filename)):
            print(f"Archive created: {zip_filename}")

if __name__ == "__main__":
    main()