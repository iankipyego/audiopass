# Audiopass

OAE-only hearing screening system for a hospital in Kenya, following the
Learn to Screen (NCHAM) OAE protocol. Replaces paper forms. Children aged 0-5.
Owner is the only developer, so keep things simple and readable.

## Stack
- Backend: Python, Django, Django REST Framework, PostgreSQL (backend/)
- Frontend: React, TypeScript, Vite, Tailwind, shadcn/ui (frontend/)
- Tests: pytest, pytest-django

## Roles
admin, supervisor, screener. Permissions are enforced on the server, never only in the UI.

## Hard rules
1. All protocol logic (next step, due dates, closing a case) lives ONLY in
   screening/engine.py. It is a pure Python module with no database access.
   Never put protocol rules in views, serializers or React.
2. Every tenant-owned model has a hospital foreign key, and every query is
   filtered by the user's hospital. One hospital must never see another's data.
3. Screenings and referral outcomes are append-only. Corrections create a new
   record, never an edit or delete.
4. Never use the word "fail". Use "Pass" and "Refer".
5. Never put results, names or phone numbers in logs or error messages.
   Reminder messages never include results.
6. Never commit secrets. Settings come from .env.

## How to work
- Before writing code, explain the plan in plain language and list the files you will change.
- Make small changes, one file at a time. Do not refactor unrelated code.
- Explain what each new model, setting or function does, because the owner wants to understand everything.
- Write tests for every new rule. Never edit a test just to make it pass.
- Protocol rules must match the Learn to Screen OAE protocol. If unsure, ask instead of guessing.
- Ask before adding a new dependency.

## Commands
- Database: docker compose up -d
- Backend: cd backend && source .venv/bin/activate && python manage.py runserver
- Tests: cd backend && pytest
