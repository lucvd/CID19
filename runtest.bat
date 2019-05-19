@echo off
call mkdir buildenv
call cd buildenv
rem Command below is specific to one pc since Jenkins runs locally for now..
call D:\School\Industrieel_Ingenieur_Master\Python3.6\python.exe -m venv ..\buildenv
call Scripts\activate
call cd ..
call pip install -r requirements.txt
call copy %secretsdjango%
call python manage.py jenkins --enable-coverage
