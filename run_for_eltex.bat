@echo off

cd C:\RTU_to_TFTP_converter


set BAT_NAME=ELTEX

set INPUT_FOLDER_NAME=input
set INPUT_LIST_NAME=eltex_macs.txt

set NEED_MAC_FORMATTING=1
set NEED_FIX_CARRIAGE=1

set NEED_INFILE_REPLACE=1
set REPLACE_FIND=XXXXXX
set REPLACE_TO=None

set CFG_FILE_EXT=yaml
set TEMP_RAW_FOLDER_NAME=eltex_temp_raw
set TEMP_CLEAR_FOLDER_NAME=eltex_temp_clear

set REMOTE_TFTP_IP=XXXXXX
set TFTP_LOCAL_ROOT=XXXXXX


venv\Scripts\python.exe main.py

timeout /t 30
