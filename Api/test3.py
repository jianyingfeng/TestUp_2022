class A:
    def __init__(self):
        self.name = '展示'

    def hh(self):
        print('哈哈哈')


a = A()
print(getattr(a, 'name'))
getattr(a, 'hh')()