set quiet
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# List recipes
default:
    just --list

# Build the Hindi BPC PDFs (pdf_exports/) and DOCX files (docx_exports/) from docs/bpc_hi*
hindi:
    uv run python scripts/generate_mkdocs_yaml.py
    uv run python scripts/generate_indexes.py
    uv run python scripts/generate_pdfs.py bpc_hi
    uv run python scripts/generate_pdfs.py bpc_hi_ex
    uv run python scripts/generate_pdfs.py bpc_hi_key
    uv run python scripts/generate_docx.py --folder bpc_hi
    uv run python scripts/generate_docx.py --folder bpc_hi_ex
    uv run python scripts/generate_docx.py --folder bpc_hi_key
    echo "PDF:  {{join(justfile_directory(), 'pdf_exports')}}"
    echo "DOCX: {{join(justfile_directory(), 'docx_exports')}}"
