@echo off
call buildenv\Scripts\activate
call cd Browserstack_tests
call python browserstack_tests.py