import time
from random import randint


class Result:
    pass


def some_http_request(x, y, z=3):
    i = randint(x, y)
    print(f'随机数：{i}')
    r = Result()
    if z == i:
        print(f'{z}=={i}')
        r.success = True
    else:
        print(f'{z}!={i}')
        r.success = False
    return r


def wait_until_keyword_success(keyword, timeout, period, *args, **kwargs):
    print(f'args参数：{args}')
    print(f'kwargs参数：{kwargs}')
    end_time = time.time() + timeout
    while time.time() <= end_time:
        keyword_result = some_http_request(*args, **kwargs)
        if keyword_result.success is True:
            print('命中')
            return keyword_result
        print('歇一秒')
        time.sleep(period)
    print('超时，仍未命中')
    return keyword_result


if __name__ == '__main__':
    # wait_until_keyword_success(some_http_request, 10, 1, 1, y=10)
    # wait_until_keyword_success(some_http_request, 10, 1, 1, 10, 3)
    # wait_until_keyword_success(some_http_request, 10, 1, z=5, y=10, x=1)
    my_dict = {'x': 1, 'y': 10, 'z': 3}
    wait_until_keyword_success(some_http_request, 10, 1, **my_dict)
