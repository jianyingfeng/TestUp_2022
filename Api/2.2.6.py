import requests


# 数据类
class Response:
    def __init__(self, code, body, raw_response):
        self.code = code
        self.body = body
        self.raw_response = raw_response

    # 魔术方法，打印这个类时会自动调用这个方法
    def __repr__(self):
        # 返回响应状态码和响应体
        return f"response code：{self.code}\nresponse body：{self.body}"


# 工具类
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
        r = self.session.get(full_url)
        # 先对响应进行处理，再返回
        return self.process(r)

    def process(self, response):
        # 获取响应状态码
        code = response.status_code
        # 获取响应体
        try:
            body = response.json()
        except:
            body = str(response.content)
        # 新建Response类作为返回值
        return Response(code, body, response)


# Jenkins接口类
class Jenkins:
    def __init__(self, base_url):
        # self.base_url = base_url
        self.http_object = HttpClient(base_url)
        self.use_jenkins = JenkinsOperation(self)

    def list_jobs(self, parameter='name'):
        return self.http_object.get(f'/api/json?tree=jobs[{parameter}]')

    def get_user(self, username):
        return self.http_object.get(f'/user/{username}/api/json/')


# Jenkins业务类
class JenkinsOperation:
    def __init__(self, jenkins):
        self.jenkins = jenkins

    def get_all_job_name(self):
        r = self.jenkins.list_jobs()
        job = [i['name'] for i in r.body['jobs']]
        return job

    def get_all_job_name_with_url(self):
        r = self.jenkins.list_jobs('name,url')
        job = {i['name']:i['url'] for i in r.body['jobs']}
        return job


if __name__ == '__main__':
    # 创建Jenkins类的一个实例
    # 调用方式一：
    # amo = Jenkins('http://localhost:8080')
    # operation = JenkinsOperation(amo)
    # r = operation.get_all_job_name()
    # print(r)
    # r = operation.get_all_job_name_with_url()
    # print(r)

    # 调用方式二：
    amo = Jenkins('http://localhost:8080')
    r = amo.use_jenkins.get_all_job_name()
    print(r)
    r = amo.use_jenkins.get_all_job_name_with_url()
    print(r)