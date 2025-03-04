import os
import pdfplumber
import pandas as pd
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    """Extracts full text from a PDF file without any filtering."""
    try:
        return extract_text(pdf_path).strip()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

def extract_tables_from_pdf(pdf_path):
    """Extracts all tables from a PDF and returns them as DataFrames."""
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            extracted_tables = page.extract_tables()
            for table_idx, table in enumerate(extracted_tables, start=1):
                if table:  # Ensure table is not empty
                    df = pd.DataFrame(table)
                    tables.append((page_num, table_idx, df))  # Store table with page and index
    return tables

def extract_data_from_pdf(pdf_path):
    """Extracts full text and tables from a PDF."""
    print(f"Processing: {pdf_path}")

    # Extract text
    full_text = extract_text_from_pdf(pdf_path)

    # Extract tables
    extracted_tables = extract_tables_from_pdf(pdf_path)

    return full_text, extracted_tables

def process_pdf_folder(pdf_folder, output_folder):
    """Processes all PDF files in a folder and extracts full text & tables."""
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            full_text, extracted_tables = extract_data_from_pdf(pdf_path)

            # Save extracted text
            text_output_file = os.path.join(output_folder, f"{filename}.txt")
            with open(text_output_file, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(f"✅ Text saved: {text_output_file}")

            # Save extracted tables
            for page_num, table_idx, table_df in extracted_tables:
                table_output_file = os.path.join(output_folder, f"{filename}_page{page_num}_table{table_idx}.csv")
                table_df.to_csv(table_output_file, index=False, header=False)
                print(f"✅ Table saved: {table_output_file}")

# Example Usage
# pdf_folder = "pdf_reports"  # Folder containing ESG PDF reports
# output_folder = "esg_extracted_data"  # Folder to store extracted text & tables
pdf_folder = "./data/data_set_1"  # Folder containing ESG PDFs
output_folder = "./data/output/data_set_1"
process_pdf_folder(pdf_folder, output_folder)
