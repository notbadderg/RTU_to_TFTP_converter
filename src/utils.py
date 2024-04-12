import os
import shutil
import hashlib
import time


class CustomException(Exception):
    pass


def format_mac(raw_string: str) -> str:
    char_list = []
    for char in raw_string:
        if not char.isalnum():
            continue
        elif char.isdigit():
            char_list.append(char)
        elif char in ['a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F']:
            char_list.append(char.upper())
        else:
            raise CustomException(f'BAD SYMBOL "{char}"')
    else:
        if len(char_list) != 12:
            raise CustomException(f'STRING LENGTH IS WRONG: {len(char_list)}')

    formatted_mac = '{0}{1}.{2}{3}.{4}{5}.{6}{7}.{8}{9}.{10}{11}'.format(*char_list)
    return formatted_mac


def get_config_filenames(raw_macs_list_path: os.path, file_cfg_ext: str, need_mac_formatting: str) -> list:
    names_list = []
    with open(raw_macs_list_path) as file:
        for raw_line in file.readlines():
            if need_mac_formatting == '1':
                name = format_mac(raw_line.strip())
            else:
                name = raw_line.strip()
            if name not in names_list:
                names_list.append(name)

    names_list.sort()
    filenames = [f'{mac}.{file_cfg_ext}' for mac in names_list]
    return filenames


def prepare_temp_folder(temp_path: os.path) -> None:
    if os.path.exists(temp_path):
        i = 10
        while i > 0:
            try:
                shutil.rmtree(temp_path)
            except Exception:
                print('..trying..', end='')
                time.sleep(0.5)
                i -= 1
            else:
                break
        else:
            raise CustomException(f'Exceeded count of trying to delete folder {temp_path}')
        print(f'Deleted {temp_path}')

    i = 10
    while i > 0:
        try:
            os.mkdir(temp_path)
        except Exception:
            print('..trying..', end='')
            time.sleep(0.5)
            i -= 1
        else:
            break
    else:
        raise CustomException(f'Exceeded count of trying to create folder {temp_path}')
    print(f'Created {temp_path}')


def compare_files(file_1_path: os.path, file_2_path: os.path) -> bool:
    with open(file_1_path, 'rb') as f1:
        file_1_content = f1.read()
    with open(file_2_path, 'rb') as f2:
        file_2_content = f2.read()

    if hashlib.sha1(file_1_content).hexdigest() == hashlib.sha1(file_2_content).hexdigest():
        return True
    else:
        return False


def copy_file(src: os.path, dst: os.path):
    i = 15
    while i > 0:
        try:
            shutil.copy(src, dst)
        except Exception:
            print('..trying..', end='')
            time.sleep(1)
            i -= 1
        else:
            break
    else:
        raise CustomException("Exceeded count of trying to copy cfg")
    print('File placed')


def update_cfg_files(temp_path: os.path, target_path: os.path, ext):
    copied = 0
    replaced = 0

    temp_files = [file for file in os.listdir(temp_path) if ext in file]
    for file in temp_files:
        print(f'{file} : ', end='')

        temp_file_path = os.path.join(temp_path, file)
        target_file_path = os.path.join(target_path, file)

        if os.path.exists(target_file_path):
            if not compare_files(temp_file_path, target_file_path):
                print('File is not the same, replacing...', end='')
                i = 15
                while i > 0:
                    try:
                        os.remove(target_file_path)
                    except Exception:
                        print('..trying..', end='')
                        time.sleep(1)
                        i -= 1
                    else:
                        break
                else:
                    raise CustomException("Exceeded count of trying to delete cfg")

                copy_file(temp_file_path, target_file_path)
                replaced += 1
            else:
                print('File is already the same')
        else:
            print('File does not exists yet, copying...', end='')
            copy_file(temp_file_path, target_file_path)
            copied += 1

    return {'copied': copied, 'replaced': replaced}


def infile_replacing(temp_path: os.path, ext, replace_find, replace_to):
    temp_files = [file for file in os.listdir(temp_path) if ext in file]
    for file in temp_files:
        print(f'{file} : ', end='')

        temp_file_path = os.path.join(temp_path, file)

        try:
            with open(temp_file_path, 'r', encoding='utf8') as f:
                text = f.read()
                text = text.replace(replace_find, replace_to)

            with open(temp_file_path, 'w', encoding='utf8') as f:
                f.write(text)

            print(f'...changing {replace_find} to {replace_to}...', end='')
        except FileNotFoundError:
            raise CustomException('Replacing not performed for some reason')
        else:
            print('CHANGED')


def remove_carriage(temp_path: os.path, target_path: os.path, ext, need_fix_carriage):
    temp_files = [file for file in os.listdir(temp_path) if ext in file]
    for file in temp_files:
        print(f'{file} : ', end='')

        temp_file_path = os.path.join(temp_path, file)
        target_file_path = os.path.join(target_path, file)

        try:
            with open(temp_file_path, 'r', encoding='UTF-8') as f:
                content = f.read()

            if need_fix_carriage == '1':
                with open(target_file_path, 'w', encoding='UTF-8', newline='\n') as f:
                    f.write(content)
            else:
                with open(target_file_path, 'w', encoding='UTF-8') as f:
                    f.write(content)

        except Exception:
            raise CustomException('Carriage not removed for some reason')
        else:
            print('CARRIAGE REMOVED')
