# Phase 4 Implementation Plan: Gemini-powered Advisor (Q&A, Suggestions)

## Overview
After the user completes tax comparison, the system will use Google Gemini to:
1. Proactively ask a smart, contextual follow-up question based on the user's data.
2. Accept the user's answer.
3. Provide personalized, actionable investment and tax-saving suggestions in a modern, readable card format.

---

## 1. Backend (FastAPI)
- **New Endpoint:** `/api/chat` (POST)
  - **Input:**
    - `session_id` (to fetch user data from DB)
    - `user_message` (user's answer to Gemini's question, or empty for first prompt)
  - **Logic:**
    - On first call (no user_message), Gemini is prompted with the user's tax data and asked to generate a relevant follow-up question.
    - On subsequent call, Gemini is prompted with the user's data and their answer, and asked to generate personalized suggestions.
    - All prompts are constructed to be context-aware and actionable.
  - **Output:**
    - `{ "question": ..., "suggestions": ... }` (one or both, depending on step)
- **Gemini API Integration:**
  - Use Google Gemini Flash API (or similar) for LLM calls.
  - Store Gemini API key in environment variables.
  - Add error handling and rate limiting.

## 2. Frontend (HTML/JS)
- **After tax comparison:**
  - Show a new card/section: "AI Advisor"
  - Step 1: Display Gemini's follow-up question and an input box for the user's answer.
  - Step 2: On submit, call `/api/chat` with the answer, then display Gemini's personalized suggestions in a visually distinct card.
- **UI/UX:**
  - Use a chat-like or Q&A card format for the interaction.
  - Suggestions are shown as a list or highlighted blocks (with icons, color, etc.).
  - Add loading spinner while waiting for Gemini's response.

## 3. API/Integration
- **API Contract:**
  - POST `/api/chat` with `{ session_id, user_message }`
  - Response: `{ question, suggestions }`
- **Security:**
  - Validate session_id and sanitize user input.
  - Do not expose Gemini API key to frontend.

## 4. Database
- Optionally store the user's answer and Gemini's suggestions in Supabase for analytics or future retrieval.

## 5. Testing & UX Polish
- Test with various user data and answers to ensure Gemini's questions and suggestions are relevant.
- Add error messages and retry options for failed API calls.
- Ensure the flow is smooth and visually consistent with the rest of the app.

---

## Example User Flow
1. User sees tax comparison results.
2. "AI Advisor" card appears: "Would you like to save more tax via Section 80C? If yes, what is your current investment?"
3. User answers: "I invest 50,000 in PPF."
4. Gemini responds: "You can invest up to ₹1.5L in 80C. Consider ELSS, PPF, or NPS. Based on your profile, here are personalized suggestions..."

---

## Next Steps
- Implement `/api/chat` endpoint in FastAPI.
- Integrate Gemini API and prompt engineering.
- Update frontend to support Q&A and suggestions card.
- Test end-to-end flow. 