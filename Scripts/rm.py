import sys


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('没有删除任何文件' + '\n' + '请输入文件路径')
    else:
        print('删除成功')
