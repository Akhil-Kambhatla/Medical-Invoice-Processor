import pytesseract
from PIL import Image
import re
import pytesseract
from pdf2image import convert_from_path
import tempfile


pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def extract_invoice_data(file_path):
    image = Image.open(file_path)
    raw_text = pytesseract.image_to_string(image)

    # Print raw OCR text to help debugging
    print("\n--- OCR Raw Text ---\n")
    print(raw_text)

    extracted_data = {
        "patient_name": extract_field(raw_text, r"BILL TO\s*\n(.+)"),
        "claim_amount": extract_field(raw_text, r"TOTAL DUE\s*\(USD\)\s*\$([\d,.]+)"),
        "diagnosis": extract_field(raw_text, r"(MRI Scan|Consultation Fee|Medication Charges)"),
        "date_of_service": extract_field(raw_text, r"Issue date[:.]?\s*(\d{1,2}/\d{1,2}/\d{4})")
    }

    return extracted_data

def extract_field(text, pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else "Not Found"
