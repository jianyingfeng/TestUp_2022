import requests


class Jenkins:
    def __init__(self, base_url):
        # 存域名
        self.base_url = base_url
        # 创建一个session对象
        self.session = requests.Session()

    def list_jobs(self, parameter='name'):
        url = self.base_url + f'/api/json/tree=jobs[{parameter}]'
        print(f'请求地址：{url}')
        r = self.session.get(url)
        return r

    def get_user(self, username):
        url = self.base_url + f'/user/{username}/api/json/'
        print(f'请求地址：{url}')
        r = self.session.get(url)
        return r


if __name__ == '__main__':
    # # 创建Jenkins类的一个实例
    # amo = Jenkins('http://localhost:8080')
    # # 调用封装好的方法（）
    # r = amo.list_jobs()
    # print('响应结果：', r.json())
    # # 解析响应，获得job名称列表
    # jobs = [i['name'] for i in r.json()['jobs']]
    # # 打印job名称列表
    # print(f'jobs列表:{jobs}')

    # 创建Jenkins类的一个实例
    amo = Jenkins('http://localhost:8080')
    # 调用封装好的方法（）
    r = amo.get_user('admin')
    print(f'响应状态码：{r.status_code}')
    print(f'响应结果：{r.json()}')
    r = amo.get_user('aaa')
    print(f'响应状态码：{r.status_code}')