import os
import sys
import re
import json
import pandas as pd
import spacy
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.pdfpage import PDFPage
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from unidecode import unidecode
from textblob import TextBlob

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Define stopwords
stop_words = set(stopwords.words('english'))

# Function to clean extracted text
def clean_text(text):
    # text = text.lower()  # Convert to lowercase
    # text = unidecode(text)  # Normalize unicode characters
    # text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    # text = re.sub(r'[^a-zA-Z0-9$%.,-]', ' ', text)  # Remove special characters
    # return text.strip()
    
    # text = text.lower() # Convert to lowercase
    # text = re.sub(r'[^a-zA-Z\s]', '', text) # Remove special characters and numbers
    # text = unidecode(text) # Normalize unicode characters (e.g., é → e)
    # corrected_text = str(TextBlob(text).correct()) # Correct spelling   
    # corrected_text = re.sub(r'\s+', ' ', corrected_text).strip() # Remove extra spaces
    # return corrected_text   
 
    text = text.lower() # Convert to lowercase
    text = re.sub(r'[^a-zA-Z\s]', '', text) # Remove special characters and numbers
    text = unidecode(text) # Normalize unicode characters (e.g., é → e)
    corrected_text = ""
    total_chars = len(text) # Perform spell correction with progress
    
    for i, char in enumerate(text):
        corrected_text += str(TextBlob(char).correct())  # Correct character by character

        # Print progress
        progress = (i + 1) / total_chars * 100
        sys.stdout.write(f"\rProgress: {progress:.2f}% ({i+1}/{total_chars} characters)")
        sys.stdout.flush()

    print("\nSpell correction complete!")
    return corrected_text.strip()

def fix_spaced_text(text):
    """
    Fixes words where letters are unnecessarily separated by spaces, e.g., "H E L L O" -> "HELLO".
    """
    # Find sequences of single letters separated by spaces
    return re.sub(r'\b(?:[A-Z]\s){2,}[A-Z]\b', lambda m: m.group(0).replace(" ", ""), text)

def extract_text_with_fix(pdf_path):
    """
    Extracts text from a PDF and fixes issues with spaced-out headlines.
    """
    raw_text = extract_text(pdf_path)
    
    # Fix spaced headlines
    cleaned_text = fix_spaced_text(raw_text)

    return cleaned_text.strip()

def extract_text_with_progress(pdf_path):
    try:
        # Get total number of pages
        with open(pdf_path, "rb") as f:
            total_pages = sum(1 for _ in PDFPage.get_pages(f))
        
        extracted_text = ""
        with open(pdf_path, "rb") as f:
            for page_num, page in enumerate(PDFPage.get_pages(f), start=1):
                # extracted_text += extract_text(pdf_path, page_numbers=[page_num-1])  # Extract page text
                extracted_text += fix_spaced_text(extract_text(pdf_path, page_numbers=[page_num-1])).strip()
                # Print progress
                progress = (page_num / total_pages) * 100
                sys.stdout.write(f"Progress: {progress:.2f}% ({page_num}/{total_pages} pages)")
                sys.stdout.flush()

        return extracted_text.strip()
    
    except PDFSyntaxError:
        print("Error: Invalid or corrupted PDF file.")
        return ""

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    return extract_text_with_progress(pdf_path)

# Function to process text for NLP
def preprocess_text(text):
    sentences = sent_tokenize(text)  # Sentence segmentation
    processed_sentences = []
    for sent in sentences:
        words = word_tokenize(sent)  # Tokenization
        words = [word for word in words if word.isalnum() and word not in stop_words]  # Remove stopwords & non-alphanumeric
        doc = nlp(' '.join(words))
        lemmatized_words = [token.lemma_ for token in doc]  # Lemmatization
        processed_sentences.append(' '.join(lemmatized_words))
    return ' '.join(processed_sentences)

# Function to clean and process ESG reports
def process_esg_reports(input_folder, output_file):
    data = []
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            raw_text = extract_text_from_pdf(pdf_path)
            cleaned_text = clean_text(raw_text)
            processed_text = preprocess_text(cleaned_text)
            data.append({"filename": filename, "cleaned_text": processed_text})
    
    # Save to JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Processed {len(data)} ESG reports and saved to {output_file}")

# Run script
input_folder = "./data/active"  # Folder containing ESG PDFs
output_file = "./data/output/esg_cleaned_data.json"
process_esg_reports(input_folder, output_file)