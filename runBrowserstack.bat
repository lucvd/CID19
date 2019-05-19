@echo off
call buildenv\Scripts\activate
call cd Browserstack_tests
call paver run parallel