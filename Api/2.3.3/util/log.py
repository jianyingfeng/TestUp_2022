import shutil
import os
import threading
import datetime
from datetime import datetime, timezone, timedelta


def clear_log():
    # 递归删除logs目录
    shutil.rmtree('logs', True)
    # 创建logs
    # mkdir只能创建一级目录，不能创建多级目录
    os.mkdir('logs')


# 日志装饰器
# def log(fun):
#     def inner(*args, **kwargs):
#         r = fun(*args, **kwargs)
#         logger.info(f"{fun.__name__} -> {r}")
#         return r
#     return inner


class Mylog:
    def __init__(self, log_level="INFO"):
        self.INFO = 1
        self.DEBUG = 2
        log_dict = {"INFO": 1, "DEBUG": 2}
        self.log_level = log_dict[log_level]

    def info(self, msg):
        # 解决编码问题，gbk里没有\xa0,用空格代替
        msg = msg.replace(u'\xa0', u' ')
        # 获取东八区时间戳
        timezone_offset = 8.0
        tzinfo = timezone(timedelta(hours=timezone_offset))
        timestamp = datetime.now(tzinfo)
        try:
            scenario_name = threading.current_thread().scenario_name
        except:
            scenario_name = 'UnNamed Scenario'
        # 如果日志等级大于等于INFO等级，则打印日志
        # 所以不管日志收集器是INFO还是DEBUG等级，调用info时都会打印日志
        if self.log_level >= self.INFO:
            print(f"[{scenario_name}][{timestamp}]{msg}")
        with open(f'logs/logs_{scenario_name}.txt', 'a') as f:
            # \n是换行符
            f.write(f'[{timestamp}]{msg}\n')

    def debug(self, msg):
        msg = msg.replace(u'\xa0', u' ')
        # 获取东八区时间戳
        timezone_offset = 8.0
        tzinfo = timezone(timedelta(hours=timezone_offset))
        timestamp = datetime.now(tzinfo)
        try:
            scenario_name = threading.current_thread().scenario_name
        except:
            scenario_name = 'UnNamed Scenario'
        # 如果日志等级大于等于DEBUG等级，则打印日志
        # 所以当日志收集器为INFO等级，调用debug不会打印日志
        # 只有当日志收集器为DEBUG等级，调用debug才会打印日志
        if self.log_level >= self.DEBUG:
            print(f"[{scenario_name}][{timestamp}]{msg}")
        with open(f"logs//logs_{scenario_name}.txt", "a") as f:
            f.write(f"[{timestamp}]{msg}\n")


clear_log()
logger = Mylog()
