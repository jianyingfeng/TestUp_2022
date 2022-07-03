import requests, textwrap
import datetime, threading, shutil, os
from datetime import datetime, timezone, timedelta
import time


# def func():
#     start_time = time.time()
#     print("hello")
#     time.sleep(1)
#     print("world")
#     end_time = time.time()
#     print(end_time-start_time)


# def deco(fun):
#     start_time = time.time()
#     fun()
#     end_time = time.time()
#     print(end_time-start_time)
#
#
# def func():
#     print("hello")
#     time.sleep(1)
#     print("world")


# def deco(fun):
#     def inner():
#         start_time = time.time()
#         fun()
#         end_time = time.time()
#         print(end_time-start_time)
#     return inner
#
# @deco
# def func():
#     print("hello")
#     time.sleep(1)
#     print("world")


# def deco(fun):
#     def inner(a, b):
#         start_time = time.time()
#         fun(a, b)
#         end_time = time.time()
#         print(end_time-start_time)
#     return inner
#
# @deco
# def func(a, b):
#     print("hello")
#     time.sleep(1)
#     print("world")
#     print(f"result is {a+b}")


def deco(fun):
    def inner(*args, **kwargs):
        start_time = time.time()
        fun(*args, **kwargs)
        end_time = time.time()
        print(end_time-start_time)
    return inner
#
@deco
def func_1(a, b):
    print("hello")
    time.sleep(1)
    print("world")
    print(f"result is {a+b}")


@deco
def func_2(a, b, c):
    print("hello")
    time.sleep(1)
    print("world")
    print(f"result is {a+b+c}")


# def deco_1(fun):
#     print(1111111)
#     def inner(*args, **kwargs):
#         print("deco_1 start")
#         fun(*args, **kwargs)
#         print("deco_1 end")
#     return inner
#
#
# def deco_2(fun):
#     print(2222222)
#     def inner(*args, **kwargs):
#         print("deco_2 start")
#         fun(*args, **kwargs)
#         print("deco_2 end")
#     return inner
#
#
# @deco_1
# @deco_2
# def func_1():
#     print("hello")
#     # time.sleep(1)
#     print("world")
#     # print(f"result is {a+b}")


# class Tree:
#     def __init__(self, name):
#         self.name = name
#         self.cate = "植物"
#
#     def __getattribute__(self, *args, **kwargs):
#         if args[0] == 'name':
#             print("我爱吃苹果")
#             return super().__getattribute__(*args)
#         else:
#             return super().__getattribute__(*args)


class Tree:
    def __init__(self, name):
        self.name = name
        self.cate = "植物"

    def __getattribute__(self, *args, **kwargs):
        # if args[0] == 'name':
        #     return super().__getattribute__(*args)
        # else:
        #     return self.wind()
        result = super().__getattribute__(*args, **kwargs)
        return result()

    def wind(self):
        return "树大招风"


if __name__ == '__main__':
    # func_1(1, 2)
    apple = Tree("苹果树")
    # print(apple.name)
    # print(apple.cate)
    print(apple.wind)
