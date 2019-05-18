@echo off
call mkdir build
call cd build
call D:\School\Industrieel_Ingenieur_Master\Python3.6\python.exe -m venv ..\build
call Scripts\activate
call cd ..
call pip install -r requirements.txt
rem D:\School\Industrieel_Ingenieur_Master\thesis\Projects\venv\Scripts\activate
call copy %secretsdjango%
call python manage.py jenkins --enable-coverage
call del secrets.yml

rem below should work, need to test it!
rem mkdir build
rem cd build
rem D:\School\Industrieel_Ingenieur_Master\Python3.6\python.exe -m venv ..\build
rem Scripts\activate
rem pip install -r requirements.txt