# Phase 3: Tax Calculation Engine & Regime Comparison UI

## Goal
User sees tax comparison cards (Old vs. New Regime) based on their data, and the data is saved to the database.

---

## 1. Backend: Tax Calculation Engine
- **Endpoint:** `POST /api/calculate-tax`
  - **Input:** All user financial fields + preferred regime (JSON)
  - **Logic:**
    - Calculates tax for both Old and New regimes (FY 2024-25 slabs, deductions, 4% cess)
    - Returns detailed breakdowns for both regimes
    - Indicates which regime is better and the savings
  - **Output:** JSON with old_regime, new_regime, preferred_regime, better_regime, savings
- **Integration:**
  - Called after user confirms data and selects regime

---

## 2. Frontend: Regime Selection & Comparison UI
- **Regime Selection:**
  - After data review, user selects "Old" or "New" regime (radio/toggle)
  - On confirm, sends all data + preferred regime to `/api/calculate-tax`
- **Comparison Cards:**
  - Two cards: Old Regime and New Regime
  - Each card shows:
    - Taxable income
    - Tax (before and after cess)
    - Visual highlights (emojis, badges, color)
    - User's pick and best regime are clearly marked
    - Savings banner if applicable
  - Social-style: playful icons, badges, responsive layout
- **User Flow:**
  1. Upload/review data → Save
  2. Select regime → Compare
  3. See results in cards
  4. Option to edit data or try again

---

## 3. UI/UX Principles
- Modern, engaging, and social-network-inspired design
- Responsive and accessible
- Clear highlights for user’s pick and best regime
- Playful elements (emojis, badges, savings banner)

---

## 4. Error Handling & Validation
- Validate all user inputs before calculation
- Handle backend errors gracefully (show user-friendly messages)
- Show loading and error states in the UI

---

## 5. Testing Tips
- Test with various salary/deduction combinations
- Try both regimes as user’s pick
- Check savings calculation and card highlights
- Test on mobile and desktop

---

## 6. Clarifying Notes
- Tax logic is based on FY 2024-25 slabs and rules (see PRD)
- All calculations include 4% cess
- Data is saved to DB before calculation
- Extendable for future features (AI suggestions, session retrieval)

---

Feel free to update this documentation as the implementation evolves! 