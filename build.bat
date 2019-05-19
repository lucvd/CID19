@echo off
call mkdir buildenv
call cd buildenv
call D:\School\Industrieel_Ingenieur_Master\Python3.6\python.exe -m venv ..\buildenv
call Scripts\activate
call cd ..
call pip install -r requirements.txt