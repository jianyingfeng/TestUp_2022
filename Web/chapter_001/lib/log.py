import datetime
import shutil
import os
from datetime import datetime, timezone, timedelta


def clear_log():
    shutil.rmtree('logs', ignore_errors=True)
    os.mkdir('logs')


class Mylog:
    def info(self, msg):
        timezone_offset = 8.0
        tzinfo = timezone(timedelta(hours=timezone_offset))
        timestamp = datetime.now(tzinfo)
        print(f"[{timestamp}] {msg}")
        with open('logs/log.txt', 'a') as f:
            f.write(f"[{timestamp}] {msg}" + '\n')


clear_log()
logger = Mylog()
