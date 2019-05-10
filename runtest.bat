@echo off
call D:\School\Industrieel_Ingenieur_Master\thesis\Projects\venv\Scripts\activate
call copy %secretsdjango%
call python manage.py jenkins --enable-coverage
call del secrets.yml