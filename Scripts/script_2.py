import sys


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('请至少输入两个参数')
    else:
        print(sys.argv[2])
