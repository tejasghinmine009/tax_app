import PyPDF2
import pytesseract
from pdf2image import convert_from_path
import os
import re

def extract_field(text, label):
    # Adjust label patterns as needed to match your PDF
    match = re.search(rf"{label}[:\s]+([\d,\.]+)", text, re.IGNORECASE)
    return match.group(1).replace(',', '') if match else "0"

def extract_financial_data_from_pdf(pdf_path):
    # Try extracting text with PyPDF2
    text = ""
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    # If text is too short, try OCR
    if len(text.strip()) < 50:
        images = convert_from_path(pdf_path)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img)
    print("Extracted text:\n", text)  # For debugging

    # Default all fields to '0' (string zero)
    data = {
        'gross_salary': '0',
        'basic_salary': '0',
        'hra_received': '0',
        'rent_paid': '0',
        'deduction_80c': '0',
        'deduction_80d': '0',
        'standard_deduction': '0',
        'professional_tax': '0',
        'tds': '0'
    }

    # Map PDF fields to expected keys
    # Gross Salary
    m = re.search(r'Gross Salary\s+(\d+)', text)
    if m:
        data['gross_salary'] = m.group(1)
    # Basic Salary (from 'Basic')
    m = re.search(r'Basic\s+(\d+)', text)
    if m:
        data['basic_salary'] = m.group(1)
    # HRA Received (from 'House Rent Allowance')
    m = re.search(r'House Rent Allowance\s+(\d+)', text)
    if m:
        data['hra_received'] = m.group(1)
    # Rent Paid (not present in sample, leave as '0')
    # Deduction 80C (not present in sample, leave as '0')
    # Deduction 80D (not present in sample, leave as '0')
    # Standard Deduction (not present in sample, leave as '0')
    # Professional Tax
    m = re.search(r'Professional Tax\s+(\d+)', text)
    if m:
        data['professional_tax'] = m.group(1)
    # TDS
    m = re.search(r'TDS\s+(\d+)', text)
    if m:
        data['tds'] = m.group(1)

    return data 