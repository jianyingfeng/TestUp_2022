import time
from random import randint


class Result:
    pass


def fun(x, y, z=3):
    i = randint(x, y)
    r = Result()
    if z == i:
        print(f'{z}等于{i}')
        r.success = True
    else:
        print(f'{z}不等于{i}')
        r.success = False
    return r


def wait_until_keyword_success(keyword, timeout, period, *args, **kwargs):
    end_time = time.time() + timeout
    while time.time() <= end_time:
        try:
            result = keyword(*args, **kwargs)
            assert result.success is True
            print('命中')
            return True
        except:
            time.sleep(period)
            print('歇一秒')
    print('超时')


if __name__ == '__main__':
    wait_until_keyword_success(fun, 10, 1, 1, 10)
