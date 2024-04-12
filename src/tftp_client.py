import os
import stat
import subprocess


def download_files(tftp_server_ip: str, files: list, target_folder: os.path) -> tuple[int, list]:
    not_downloaded = []
    for file in files:
        target_path = f'{target_folder}\\{file}'
        print(f'{target_path} : ', end='')
        command = f'tftp -i {tftp_server_ip} get {file} {target_path}'
        try:
            print(subprocess.getoutput(command))
            os.chmod(os.path.join(target_path), stat.S_IWUSR)
        except FileNotFoundError:
            not_downloaded.append(file)

    return len(os.listdir(target_folder)), not_downloaded
