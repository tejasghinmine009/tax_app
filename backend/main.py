import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from dotenv import load_dotenv
from fastapi import File, UploadFile, Form
from fastapi.responses import JSONResponse
import shutil
import uuid
import pdf_utils
import uuid as uuidlib
from fastapi import Body
from gemini_utils import call_gemini

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# DB connection check endpoint
@app.get("/api/db-check")
def db_check():
    try:
        conn = psycopg2.connect(
            host=os.getenv("SUPABASE_HOST"),
            dbname=os.getenv("SUPABASE_DBNAME"),
            user=os.getenv("SUPABASE_USER"),
            password=os.getenv("SUPABASE_PASSWORD"),
            port=os.getenv("SUPABASE_PORT", 5432)
        )
        cur = conn.cursor()
        cur.execute("SELECT to_regclass('public.\"UserFinancials\"');")
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result and result[0]:
            return {"db": "connected", "UserFinancials_table": "exists"}
        else:
            return {"db": "connected", "UserFinancials_table": "not found"}
    except Exception as e:
        return {"db": "error", "details": str(e)}

@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"error": "Only PDF files are allowed."})
    temp_filename = f"temp_{uuid.uuid4()}.pdf"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        data = pdf_utils.extract_financial_data_from_pdf(temp_filename)
    except Exception as e:
        os.remove(temp_filename)
        return JSONResponse(status_code=500, content={"error": f"Extraction failed: {str(e)}"})
    os.remove(temp_filename)
    return {"extracted": data}

@app.post("/api/save-financials")
async def save_financials(
    gross_salary: str = Form(...),
    basic_salary: str = Form(...),
    hra_received: str = Form(...),
    rent_paid: str = Form(...),
    deduction_80c: str = Form(...),
    deduction_80d: str = Form(...),
    standard_deduction: str = Form(...),
    professional_tax: str = Form(...),
    tds: str = Form(...)
):
    session_id = str(uuidlib.uuid4())
    try:
        conn = psycopg2.connect(
            host=os.getenv("SUPABASE_HOST"),
            dbname=os.getenv("SUPABASE_DBNAME"),
            user=os.getenv("SUPABASE_USER"),
            password=os.getenv("SUPABASE_PASSWORD"),
            port=os.getenv("SUPABASE_PORT", 5432)
        )
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO "UserFinancials" (
                session_id, gross_salary, basic_salary, hra_received, rent_paid, deduction_80c, deduction_80d, standard_deduction, professional_tax, tds
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
            (
                session_id,
                gross_salary,
                basic_salary,
                hra_received,
                rent_paid,
                deduction_80c,
                deduction_80d,
                standard_deduction,
                professional_tax,
                tds
            )
        )
        conn.commit()
        cur.close()
        conn.close()
        return {"saved": True, "session_id": session_id}
    except Exception as e:
        print("DB Insert Error:", e)  # This will print the error to your backend console
        return {"saved": False, "error": str(e)} 

# Tax calculation logic (FY 2024-25)
def calculate_old_regime(data):
    # Deductions: Standard Deduction (₹50k), HRA, Professional Tax, 80C, 80D, etc.
    gross = float(data.get('gross_salary', 0) or 0)
    std_ded = float(data.get('standard_deduction', 0) or 0)
    hra = float(data.get('hra_received', 0) or 0)
    rent = float(data.get('rent_paid', 0) or 0)
    d80c = float(data.get('deduction_80c', 0) or 0)
    d80d = float(data.get('deduction_80d', 0) or 0)
    prof_tax = float(data.get('professional_tax', 0) or 0)
    # Taxable income
    deductions = std_ded + hra + d80c + d80d + prof_tax
    taxable = max(gross - deductions, 0)
    # Slabs: 0% up to ₹2.5L, 5% up to ₹5L, 20% up to ₹10L, 30% above
    tax = 0
    if taxable > 250000:
        if taxable <= 500000:
            tax += (taxable - 250000) * 0.05
        elif taxable <= 1000000:
            tax += 250000 * 0.05
            tax += (taxable - 500000) * 0.20
        else:
            tax += 250000 * 0.05
            tax += 500000 * 0.20
            tax += (taxable - 1000000) * 0.30
    # 4% cess
    tax_with_cess = tax * 1.04
    return {
        'taxable_income': taxable,
        'tax': round(tax, 2),
        'tax_with_cess': round(tax_with_cess, 2),
        'breakdown': {
            'gross_salary': gross,
            'deductions': deductions,
            'std_deduction': std_ded,
            'hra': hra,
            'd80c': d80c,
            'd80d': d80d,
            'prof_tax': prof_tax
        }
    }

def calculate_new_regime(data):
    # Deductions: Standard Deduction (₹50k) only
    gross = float(data.get('gross_salary', 0) or 0)
    std_ded = float(data.get('standard_deduction', 0) or 0)
    taxable = max(gross - std_ded, 0)
    # Slabs: 0% up to ₹3L, 5% up to ₹6L, 10% up to ₹9L, 15% up to ₹12L, 20% up to ₹15L, 30% above
    tax = 0
    if taxable > 300000:
        if taxable <= 600000:
            tax += (taxable - 300000) * 0.05
        elif taxable <= 900000:
            tax += 300000 * 0.05
            tax += (taxable - 600000) * 0.10
        elif taxable <= 1200000:
            tax += 300000 * 0.05
            tax += 300000 * 0.10
            tax += (taxable - 900000) * 0.15
        elif taxable <= 1500000:
            tax += 300000 * 0.05
            tax += 300000 * 0.10
            tax += 300000 * 0.15
            tax += (taxable - 1200000) * 0.20
        else:
            tax += 300000 * 0.05
            tax += 300000 * 0.10
            tax += 300000 * 0.15
            tax += 300000 * 0.20
            tax += (taxable - 1500000) * 0.30
    # 4% cess
    tax_with_cess = tax * 1.04
    return {
        'taxable_income': taxable,
        'tax': round(tax, 2),
        'tax_with_cess': round(tax_with_cess, 2),
        'breakdown': {
            'gross_salary': gross,
            'std_deduction': std_ded
        }
    }

@app.post("/api/calculate-tax")
def calculate_tax(
    gross_salary: str = Body(...),
    basic_salary: str = Body(...),
    hra_received: str = Body(...),
    rent_paid: str = Body(...),
    deduction_80c: str = Body(...),
    deduction_80d: str = Body(...),
    standard_deduction: str = Body(...),
    professional_tax: str = Body(...),
    tds: str = Body(...),
    preferred_regime: str = Body(...)
):
    data = {
        'gross_salary': gross_salary,
        'basic_salary': basic_salary,
        'hra_received': hra_received,
        'rent_paid': rent_paid,
        'deduction_80c': deduction_80c,
        'deduction_80d': deduction_80d,
        'standard_deduction': standard_deduction,
        'professional_tax': professional_tax,
        'tds': tds
    }
    old = calculate_old_regime(data)
    new = calculate_new_regime(data)
    better = 'old' if old['tax_with_cess'] < new['tax_with_cess'] else 'new'
    savings = abs(old['tax_with_cess'] - new['tax_with_cess'])
    return {
        'old_regime': old,
        'new_regime': new,
        'preferred_regime': preferred_regime,
        'better_regime': better,
        'savings': round(savings, 2)
    } 

@app.post("/api/chat")
def chat(session_id: str = Body(...), user_message: str = Body("")):
    # Fetch user data from DB
    conn = psycopg2.connect(
        host=os.getenv("SUPABASE_HOST"),
        dbname=os.getenv("SUPABASE_DBNAME"),
        user=os.getenv("SUPABASE_USER"),
        password=os.getenv("SUPABASE_PASSWORD"),
        port=os.getenv("SUPABASE_PORT", 5432)
    )
    cur = conn.cursor()
    cur.execute('SELECT * FROM "UserFinancials" WHERE session_id = %s', (session_id,))
    user_data = cur.fetchone()
    cur.close()
    conn.close()
    if not user_data:
        return {"error": "Session not found."}

    # Prepare prompt
    if not user_message:
        # First call: ask Gemini to generate a follow-up question
        prompt = (
            "You are a tax advisor. Here is the user's tax data:\n"
            f"{user_data}\n"
            "Ask a single, relevant follow-up question to help them save more tax. Be concise."
        )
        messages = [{"role": "user", "content": prompt}]
        question = call_gemini(messages)
        return {"question": question}
    else:
        # Second call: generate personalized suggestions
        prompt = (
            "You are a tax advisor. Here is the user's tax data:\n"
            f"{user_data}\n"
            f"User's answer to your previous question: {user_message}\n"
            "Now, provide 2-4 actionable, personalized tax-saving suggestions in a friendly, readable format."
        )
        messages = [{"role": "user", "content": prompt}]
        suggestions = call_gemini(messages)
        return {"suggestions": suggestions} 