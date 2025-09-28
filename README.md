## FastAPI Authentication System

Sistem autentikasi menggunakan FastAPI, SQLAlchemy, Alembic, PostgreSQL, dengan access token dan refresh token.

## Fitur
- Register user (password di-hash, UUID sebagai ID)
- Login (generate access token + refresh token)
- Refresh token (generate access token baru jika token masih valid)
- Logout (hapus refresh token dari DB)
- Access token dikirim di HttpOnly cookie

## Install Dependency
pip install -r requirements.txt

## Migrations Database
- alembic revision --autogenerate -m "initial migration"
- alembic upgrade head

## Run Project
uvicorn app.main:app --reload
