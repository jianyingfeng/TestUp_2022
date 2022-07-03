import requests


class HttpClient:
    def __init__(self, base_url):
        # 存域名
        self.base_url = base_url
        # 创建一个session对象
        self.session = requests.Session()

    def get(self, url):
        """
        :param url: api路由
        :return:
        """
        # 完整的接口请求地址
        full_url = self.base_url + url
        print(f'请求地址：{full_url}')
        return self.session.get(full_url)


class Jenkins:
    def __init__(self, base_url):
        # self.base_url = base_url
        self.http_object = HttpClient(base_url)

    def list_jobs(self, parameter='name'):
        return self.http_object.get(f'/api/json?tree=jobs[{parameter}]')

    def get_user(self, username):
        return self.http_object.get(f'/user/{username}/api/json/')


if __name__ == '__main__':
    # 创建Jenkins类的一个实例
    amo = Jenkins('http://localhost:8080')
    # 调用封装好的方法（）
    r = amo.list_jobs()
    print('响应结果：', r.json())
    # 解析响应，获得job名称列表
    jobs = [i['name'] for i in r.json()['jobs']]
    # 打印job名称列表
    print(f'jobs列表:{jobs}')

    # 调用封装好的方法（）
    r = amo.get_user('admin')
    print(f'响应状态码：{r.status_code}')
    print(f'响应结果：{r.json()}')
    r = amo.get_user('aaa')
    print(f'响应状态码：{r.status_code}')