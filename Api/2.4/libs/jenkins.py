from libs.jenkins_operations.jenkins_job_operations import JenkinsJobOperation
from libs.jenkins_operations.jenkins_user_operations import JenkinsUserOperation
from util.core import HttpClient
from util.log import logger


# Jenkins类
class Jenkins(JenkinsJobOperation, JenkinsUserOperation):
    def __init__(self, base_url, username=None, password=None):
        # self.base_url = base_url
        self.http_object = HttpClient(base_url)
        # 给HttpClient类添加一个方法
        self.http_object.authenticate = self.authenticate
        # self.use_jenkins = JenkinsOperation(self)
        # CSRF token 键和值
        # 存入属性的目的估计为了方便调试
        self.crumbField_name = None
        self.crumbField_value = None
        if username and password:
            self.username = username
            self.password = password
            self.login(username, password)

    def login(self, username, password):
        logger.info(f"login username={username}")
        # 添加基本认证所需信息
        self.http_object.session.auth = username, password
        # 获取CSRF token键和值
        r = self.get_crumb()
        self.crumbField_name = r.body['crumbRequestField']
        self.crumbField_value = r.body['crumb']
        # 在请求头中添加CSRF token
        self.http_object.session.headers[self.crumbField_name] = self.crumbField_value
        # return不能去掉，否则在admin = Jenkins('http://127.0.0.1:8080').login('admin', 'admin')
        # 的登录方式下会返回None，后续无法操作了
        return self

    # csrf token失效后，重新登录
    def authenticate(self):
        self.login(self.username, self.password)

    def logout(self):
        # 删除请求头中CSRF token
        del self.http_object.session.headers[self.crumbField_name]
        # 删除基本认证信息
        self.http_object.session.auth = None
        self.crumbField_name = None
        self.crumbField_value = None
        self.username = None
        self.password = None

    # 执行命令行脚本
    def run_groovy(self, script):
        payload = {"script": script}
        # 必须传给data而不是json
        return self.http_object.post('/scriptText/', data=payload)

    # 获取CSRF token
    def get_crumb(self):
        return self.http_object.get('/crumbIssuer/api/json/')


if __name__ == '__main__':
    # admin = Jenkins('http://127.0.0.1:8080', 'admin', 'admin')
    # # admin = Jenkins('http://127.0.0.1:8080').login('admin', 'admin')
    # job_dsl = """properties([parameters([string(name: 'Run', defaultValue: 'Yes', description: 'a parameter')])])node {stage("test"){echo 'Hello World'}}"""
    # r = admin.list_jobs()
    # print(r)
    # r = admin.get_user('admin')
    # print(r)
    #
    # admin.get_all_usernames()
    # admin.delete_all_jobs()
    # admin.create_job_with_dsl(job_dsl, "xxjob")
    # admin.create_job_with_dsl(job_dsl, "xxjob")
    # admin.delete_all_jobs()
    # admin.get_all_usernames()

    admin = Jenkins('http://127.0.0.1:8080', 'admin', 'admin')
    admin.delete_all_jobs()
