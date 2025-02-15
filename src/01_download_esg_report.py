import os
import requests

# Sample ESG report URLs (replace with actual URLs)
ESG_REPORT_URLS = [
    "https://investor.econhealthcare.com/misc/sr2024.pdf",
    "https://www.isechealthcare.com/wp-content/uploads/2024/03/ISEC_Sustainability-Report-2023.pdf", # Failed
    "https://www.fullertonhealth.com/wp-content/uploads/2024/09/Fullerton-Health-Sustainability-Report-FY2023.pdf",
    "https://www.rafflesmedicalgroup.com/wp-content/uploads/2023/04/Raffles-Medical-Group_Sustainability-Report-2022.pdf"
]

# Folder to save reports
SAVE_FOLDER = "data/esg_reports"
os.makedirs(SAVE_FOLDER, exist_ok=True)

def download_file(url, folder):
    filename = os.path.join(folder, url.split("/")[-1])
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {url}")

# Download all ESG reports
for url in ESG_REPORT_URLS:
    download_file(url, SAVE_FOLDER)

print("All downloads completed!")