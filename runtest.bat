@echo off
call D:\School\Industrieel_Ingenieur_Master\thesis\Projects\venv\Scripts\activate
call copy %myFile%
call python manage.py jenkins chat
call del secrets.yml