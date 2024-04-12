import os
import subprocess
import sys

from config import Params
from src.logger import logger
from src.tftp_client import download_files
from src.utils import get_config_filenames, prepare_temp_folder, update_cfg_files, remove_carriage, infile_replacing


@logger()
def main():
    step = 0
    try:
        par = Params()
        
        print(subprocess.getoutput('chcp 865'))
        print()

        step = 1
        configs_filenames = get_config_filenames(par.input_list_path, par.cfg_file_ext, par.need_mac_formatting)
        print('\n'.join(configs_filenames))
        print()

        step = 2
        prepare_temp_folder(par.temp_raw_path)
        prepare_temp_folder(par.temp_clear_path)
        print()

        step = 3
        downloaded_count, not_downloaded = download_files(par.remote_tftp_ip, configs_filenames, par.temp_raw_path)
        print()

        step = 4
        if par.need_infile_replace == '1':
            infile_replacing(par.temp_raw_path, par.cfg_file_ext, par.replace_find, par.replace_to)
            print()

        step = 5
        remove_carriage(par.temp_raw_path, par.temp_clear_path, par.cfg_file_ext, par.need_fix_carriage)
        print()

        step = 6
        update_res = update_cfg_files(par.temp_clear_path, par.tftp_local_root_path, par.cfg_file_ext)
        print()

    except Exception as e:
        return f'STEP {step} - {sys.exc_info()}'

    else:
        requested_count = len(configs_filenames)
        state_str = f'{par.bat_name}: ' \
                    f'requested {requested_count}, ' \
                    f'downloaded: {downloaded_count}, ' \
                    f'copied: {update_res["copied"]}, ' \
                    f'replaced: {update_res["replaced"]}.'

        if requested_count == downloaded_count:
            end_state = ' - OK'
        else:
            end_state = f' - OK, but requested_count != downloaded_count: {not_downloaded}'

        return_str = state_str + end_state
        return return_str


if __name__ == '__main__':
    main()
