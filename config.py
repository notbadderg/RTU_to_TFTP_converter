import os


class CustomException(Exception):
    pass


def get_params_from_env():
    params_names = [
        'BAT_NAME',
        
        'INPUT_FOLDER_NAME',
        'INPUT_LIST_NAME',

        'NEED_MAC_FORMATTING',
        'NEED_FIX_CARRIAGE',

        'NEED_INFILE_REPLACE',
        'REPLACE_FIND',
        'REPLACE_TO',

        'CFG_FILE_EXT',
        'TEMP_RAW_FOLDER_NAME',
        'TEMP_CLEAR_FOLDER_NAME',

        'REMOTE_TFTP_IP',
        'TFTP_LOCAL_ROOT',
    ]
    params = {}

    for name in params_names:
        value = os.getenv(name)
        if value:
            params[name] = value
        else:
            raise CustomException(f'!ERROR! PARAMETER MISSING: {name} - {value}')

    for k, v in params.items():
        if 'NEED' in k:
            if v != '1' and v != '0':
                raise CustomException(f'!ERROR! WRONG PARAMETER: {k} - {v}. MUST BE 1 or 0')

    if params['NEED_INFILE_REPLACE'] == '1' and not params['REPLACE_FIND'].isprintable():
        raise CustomException(f'!ERROR! MASS REPLACE AVOIDED')

    if params['REPLACE_TO'] == 'None':
        params['REPLACE_TO'] = ''

    return params


class Params:
    def __init__(self):

        self.params = get_params_from_env()

        self.bat_name = self.params['BAT_NAME']

        self.input_folder_name = self.params['INPUT_FOLDER_NAME']
        self.input_list_name = self.params['INPUT_LIST_NAME']

        self.need_mac_formatting = self.params['NEED_MAC_FORMATTING']
        self.need_fix_carriage = self.params['NEED_FIX_CARRIAGE']

        self.need_infile_replace = self.params['NEED_INFILE_REPLACE']
        self.replace_find = self.params['REPLACE_FIND']
        self.replace_to = self.params['REPLACE_TO']

        self.cfg_file_ext = self.params['CFG_FILE_EXT']
        self.temp_raw_folder_name = self.params['TEMP_RAW_FOLDER_NAME']
        self.temp_clear_folder_name = self.params['TEMP_CLEAR_FOLDER_NAME']

        self.remote_tftp_ip = self.params['REMOTE_TFTP_IP']
        self.tftp_local_root = self.params['TFTP_LOCAL_ROOT']

        self.input_list_path = os.path.join(os.getcwd(), self.input_folder_name, self.input_list_name)
        self.temp_raw_path = os.path.join(os.getcwd(), self.temp_raw_folder_name)
        self.temp_clear_path = os.path.join(os.getcwd(), self.temp_clear_folder_name)
        self.tftp_local_root_path = os.path.join(self.tftp_local_root)
