import datetime
import os


def logger(need_args=False):

    log_filename = 'running.log'
    prev_log_filename = 'prev_running.log'
    log_max_bytes = 128000

    def write_log_line(line: str) -> None:
        log_path = os.path.join(os.getcwd(), log_filename)
        prev_log_path = os.path.join(os.getcwd(), prev_log_filename)

        if os.path.exists(log_path):
            log_size = os.stat(log_path).st_size

            print(f'Log file size {log_size}')

            if log_size > log_max_bytes:
                print('Log size exceeded, making log backup')
                if os.path.exists(prev_log_path):
                    print('Prev log backup removing...')
                    os.remove(prev_log_path)

                os.rename(log_path, prev_log_path)

        with open(log_path, 'a') as f:
            f.write(f'{line}\n')

    def decorator(func):
        def wrapper(*args, **kwargs):
            f_start_date = datetime.datetime.now()
            f_name = func.__name__
            f_return = func(*args, **kwargs)
            f_end_date = datetime.datetime.now()
            if need_args:
                log_line = f'{f_start_date} - {f_end_date} - {f_name} - Args: {args} {kwargs} - Return: {f_return}'
            else:
                log_line = f'{f_start_date} - {f_end_date} - {f_name} - Return: {f_return}'
            write_log_line(log_line)
            print(log_line)
            return f_return
        return wrapper
    return decorator
