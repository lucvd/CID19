@echo off
call D:\School\Industrieel_Ingenieur_Master\thesis\Projects\venv\Scripts\activate
call copy %secretdjango%
call python manage.py jenkins chat
call del secrets.yml