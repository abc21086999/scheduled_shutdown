import subprocess
import random


def run_shutdown(time: int):
    subprocess.run(["shutdown", "/s", "/t", time], shell=True)
    print(f'{time}秒')


def stop_shutdown():
    subprocess.run(["shutdown", "/a"], shell=True)
    print('取消關機')


def process_string(string: str):
    if string.isnumeric():
        return int(string), 0
    else:
        try:
            hour = float(string)
            integer, decimal = divmod(hour, 1)
            return int(integer), int(decimal * 60)
        except ValueError:
            return None, None

