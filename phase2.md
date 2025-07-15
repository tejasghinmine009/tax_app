# Phase 2: PDF Upload, Extraction, and Manual Data Review

## Goal
User can upload a PDF and review/edit the auto-extracted data in a form.

---

## 1. Architecture Overview
- **Frontend:**
  - HTML/CSS/JS interface for PDF upload and data review form.
  - Calls backend API for PDF processing.
- **Backend:**
  - FastAPI server handles file upload, PDF extraction, and returns structured data.
  - Uses PyPDF2, pytesseract, and pdf2image for extraction.
- **Storage:**
  - Temporary storage of uploaded PDFs (ephemeral disk, deleted after processing).

---

## 2. Key Endpoints
- `POST /api/upload-pdf`
  - Accepts PDF file upload (multipart/form-data).
  - Extracts data from PDF and returns structured JSON.
- (Optional) `POST /api/parse-pdf` (if extraction and upload are separated)
- (Optional) `POST /api/save-financials`
  - Saves reviewed/edited data to Supabase DB.

---

## 3. Backend Libraries & Tools
- **PyPDF2:** For extracting text from PDFs.
- **pytesseract:** For OCR on scanned PDFs.
- **pdf2image:** For converting PDF pages to images (for OCR).
- **FastAPI:** API framework.
- **psycopg2:** For DB operations.
- **python-dotenv:** For environment variable management.

---

## 4. Frontend Flow
1. User lands on the upload page.
2. User selects and uploads a PDF (Pay Slip or Form 16).
3. Frontend sends the file to `/api/upload-pdf`.
4. Receives extracted data as JSON.
5. Displays a form pre-filled with extracted data for user review/edit.
6. User can edit fields and submit the reviewed data.

---

## 5. Backend Flow
1. Receive PDF file via `/api/upload-pdf`.
2. Save PDF temporarily to disk.
3. Try extracting text with PyPDF2.
4. If text extraction is insufficient, convert pages to images (pdf2image) and run OCR (pytesseract).
5. Structure extracted data into JSON (matching UserFinancials schema).
6. Return JSON to frontend.
7. (Optional) Delete PDF after processing.

---

## 6. Error Handling
- Validate file type and size on upload.
- Handle extraction failures (return clear error messages).
- Ensure temporary files are deleted after processing.
- Provide user feedback for upload and extraction errors.

---

## 7. Security & Privacy
- No persistent storage of uploaded PDFs.
- All processing is session-based.
- Environment variables for all secrets.

---

## 8. Clarifying Questions
1. Should we support only PDF, or also images (JPG/PNG)?
2. What is the max file size allowed for upload?
3. Should we allow multiple pages, or only single-page PDFs?
4. Should we save the reviewed data immediately, or only after user confirmation?
5. Any specific fields to extract beyond those in the UserFinancials schema?

---

Feel free to answer the clarifying questions or add any additional requirements for Phase 2! 