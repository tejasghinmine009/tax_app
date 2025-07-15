# Tax Advisor - Phase 1 Setup

## Overview
This project is a local prototype for the Tax Advisor app. It includes a FastAPI backend (with Supabase DB check) and a modern, responsive landing page using vanilla HTML, CSS, and JS.

---

## Backend (FastAPI)

### 1. Setup Python Environment
```
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Mac/Linux
```

### 2. Install Dependencies
```
pip install fastapi uvicorn psycopg2 python-dotenv
```

### 3. Environment Variables
- Copy `.env.example` to `.env` and fill in your Supabase credentials.

### 4. Run the Backend
```
uvicorn main:app --reload
```
- The API will be available at `http://localhost:8000`
- Health check: `GET /api/health`
- DB check: `GET /api/db-check`

---

## Frontend (Landing Page)

### 1. Open the Landing Page
- Open `frontend/index.html` directly in your browser.
- The page will attempt to connect to the backend health endpoint and show status.

### 2. Customization
- Edit `styles.css` for theme tweaks.
- The "Start" button is a placeholder for future flow.

---

## Environment Variables
See `backend/.env.example` for required variables:
- `SUPABASE_HOST`
- `SUPABASE_DBNAME`
- `SUPABASE_USER`
- `SUPABASE_PASSWORD`
- `SUPABASE_PORT`

---

## Notes
- No version control or deployment is included in this phase.
- The backend expects the `UserFinancials` table to exist in Supabase as per the PRD.
- For any issues, check your DB credentials and backend logs. 

---

## Phase 2: PDF Upload & Data Review

### Backend
- Install new dependencies:
  ```
  pip install PyPDF2 pytesseract pdf2image
  ```
- Start the backend as before.

### Frontend
- Open `frontend/upload.html` in your browser.
- Upload a PDF, review/edit extracted data, and confirm to save.

### Notes
- Only PDF files are supported.
- Multi-page PDFs are handled.
- Data is only saved after user confirmation. 