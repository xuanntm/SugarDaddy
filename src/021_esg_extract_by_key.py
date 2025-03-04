import os
import re
from pdfminer.high_level import extract_text

# Define ESG-related keywords (can be customized)
ESG_KEYWORDS = [
    "environment", "sustainability", "carbon", "emission", "climate",
    "social responsibility", "diversity", "inclusion", "governance",
    "ethics", "corporate responsibility", "renewable", "green energy"
]

def extract_text_from_pdf(pdf_path):
    """Extracts raw text from a PDF file."""
    try:
        return extract_text(pdf_path)
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

def filter_esg_content(text):
    """Filters ESG-related content from the extracted text using keyword matching."""
    esg_sentences = []
    
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in ESG_KEYWORDS):
            esg_sentences.append(sentence)

    return "\n".join(esg_sentences)

def extract_esg_from_pdf(pdf_path):
    """Extracts ESG-related content from a PDF."""
    print(f"Processing: {pdf_path}")

    # Extract raw text from PDF
    raw_text = extract_text_from_pdf(pdf_path)

    # Filter relevant ESG-related sentences
    esg_content = filter_esg_content(raw_text)

    return esg_content

def process_pdf_folder(folder_path, output_folder):
    """Processes all PDF files in a folder and extracts ESG data."""
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            esg_data = extract_esg_from_pdf(pdf_path)

            if esg_data:
                output_file = os.path.join(output_folder, f"{filename}.txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(esg_data)
                print(f"✅ ESG data saved: {output_file}")
            else:
                print(f"⚠️ No ESG data found in {filename}")

# Example Usage
# pdf_folder = "pdf_reports"  # Folder containing ESG PDF reports
# output_folder = "esg_extracted_data"  # Folder to store ESG-extracted text
pdf_folder = "./data/data_set_1"  # Folder containing ESG PDFs
output_folder = "./data/output/data_set_1"
process_pdf_folder(pdf_folder, output_folder)
