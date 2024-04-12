@echo off

cd C:\RTU_to_TFTP_converter

start run_for_eltex.bat
timeout /t 5
start run_for_qtech.bat

timeout /t 15