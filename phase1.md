# Phase 1: Project Setup, DB Schema, and Landing Page

## Goal
User sees the landing page, and the `UserFinancials` table exists in Supabase.

---

## 1. Project Setup
- [ ] Initialize Git repository (if not already done)
- [ ] Set up project directory structure (frontend, backend, docs, etc.)
- [ ] Create and activate Python virtual environment
- [ ] Install backend dependencies (FastAPI, psycopg2, etc.)
- [ ] Set up frontend boilerplate (HTML, CSS with Aptos Display font, JS)
- [ ] Add README with setup instructions

## 2. Supabase Setup
- [ ] Create a new Supabase project (if not already done)
- [ ] Configure database credentials and access
- [ ] Create `UserFinancials` table with the following schema:
    - `session_id` (UUID, Primary Key)
    - `gross_salary` (NUMERIC(15, 2))
    - `basic_salary` (NUMERIC(15, 2))
    - `hra_received` (NUMERIC(15, 2))
    - `rent_paid` (NUMERIC(15, 2))
    - `deduction_80c` (NUMERIC(15, 2))
    - `deduction_80d` (NUMERIC(15, 2))
    - `standard_deduction` (NUMERIC(15, 2))
    - `professional_tax` (NUMERIC(15, 2))
    - `tds` (NUMERIC(15, 2))
    - `created_at` (TIMESTAMPTZ)
- [ ] Test DB connection from backend using psycopg2

## 3. Backend Setup
- [ ] Scaffold FastAPI app
- [ ] Create a health check endpoint (e.g., `/api/health`)
- [ ] Add CORS middleware for frontend-backend communication
- [ ] Add environment variable support for DB credentials
- [ ] (Optional) Set up basic logging

## 4. Frontend: Landing Page
- [ ] Design a modern, branded landing page (light theme, blue highlights)
- [ ] Use "Aptos Display" font for typography
- [ ] Add a prominent "Start" button
- [ ] Ensure responsive and accessible design
- [ ] Connect frontend to backend health check endpoint (to verify setup)

## 5. Version Control & Documentation
- [ ] Push code to GitHub (if not already done)
- [ ] Document setup steps in README
- [ ] Add .gitignore for Python, node_modules, environment files, etc.

---

## Clarifying Questions
1. **Frontend Framework:** Should we use any frontend framework (React, Vue, etc.), or strictly stick to vanilla HTML/CSS/JS as per PRD?
2. **Branding Assets:** Are there any logos, color palettes, or branding guidelines to use for the landing page?
3. **Supabase Project:** Is the Supabase project already created, or should we create a new one from scratch?
4. **Deployment:** Is local development sufficient for Phase 1, or do you want a basic deployment (e.g., Render preview) as part of this phase?
5. **Secrets Management:** Should we use a `.env` file for local DB credentials, or is there a preferred secrets management approach?

---

Feel free to answer the clarifying questions or add any additional requirements! 