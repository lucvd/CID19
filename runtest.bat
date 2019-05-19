@echo off
call buildenv\Scripts\activate
call copy %secretsdjango%
call python manage.py jenkins --enable-coverage
call del secrets.yml
