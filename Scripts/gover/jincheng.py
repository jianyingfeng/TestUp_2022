import os
from multiprocessing import Process


def work(name):
    print(f'Run son process {name} id:{os.getpid()}')


if __name__ == '__main__':
    print(f'Main process id:{os.getpid()}')
    p = Process(target=work, args=('test',))
    p.start()
    p.join()
    print('Main process end.')
