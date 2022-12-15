# 增加登入登出功能
# 登入的要点：
#     1、输入用户名、密码（通过基本认证实现）
#     2、添加 CSRF token

# 登入的要点：
#     1、删掉基本认证信息的请求头
#     2、删掉 CSRF token
import requests
import datetime, shutil, threading, os
import textwrap
from datetime import datetime, timezone, timedelta


def clear_log():
    # 递归删除logs目录
    shutil.rmtree('logs', True)
    # 创建logs
    # mkdir只能创建一级目录，不能创建多级目录
    os.mkdir('logs')


class Mylog:
    def __init__(self, log_level="INFO"):
        self.INFO = 1
        self.DEBUG = 2
        log_dict = {"INFO": 1, "DEBUG": 2}
        self.log_level = log_dict[log_level]

    def info(self, msg):
        # 解决编码问题，gbk里没有\xa0,用空格代替
        msg = msg.replace(u'\xa0', u' ')
        # 获取东八区时间戳
        timezone_offset = 8.0
        tzinfo = timezone(timedelta(hours=timezone_offset))
        timestamp = datetime.now(tzinfo)
        try:
            scenario_name = threading.current_thread().scenario_name
        except:
            scenario_name = 'UnNamed Scenario'
        # 如果日志等级大于等于INFO等级，则打印日志
        # 所以不管日志收集器是INFO还是DEBUG等级，调用info时都会打印日志
        if self.log_level >= self.INFO:
            print(f"[{scenario_name}][{timestamp}]{msg}")
        with open(f'logs/logs_{scenario_name}.txt', 'a') as f:
            # \n是换行符
            f.write(f'[{timestamp}]{msg}\n')

    def debug(self, msg):
        msg = msg.replace(u'\xa0', u' ')
        # 获取东八区时间戳
        timezone_offset = 8.0
        tzinfo = timezone(timedelta(hours=timezone_offset))
        timestamp = datetime.now(tzinfo)
        try:
            scenario_name = threading.current_thread().scenario_name
        except:
            scenario_name = 'UnNamed Scenario'
        # 如果日志等级大于等于DEBUG等级，则打印日志
        # 所以当日志收集器为INFO等级，调用debug不会打印日志
        # 只有当日志收集器为DEBUG等级，调用debug才会打印日志
        if self.log_level >= self.DEBUG:
            print(f"[{scenario_name}][{timestamp}]{msg}")
        with open(f"logs//logs_{scenario_name}.txt", "a") as f:
            f.write(f"[{timestamp}]{msg}\n")


# 数据类
class Response:
    def __init__(self, code, body, raw_response):
        self.code = code
        self.body = body
        self.raw_response = raw_response
        # 在构造函数里面调用示例方法，那么每次实例化对象时，都会自动调用该方法
        self.print_raw_response(raw_response)

    # 魔术方法，打印这个类时会自动调用这个方法
    def __repr__(self):
        # 返回响应状态码和响应体
        return f"{self.code} {self.body}"

    # 打印日志
    def print_raw_response(self, response):
        # 请求头和响应头处理方式一
        # 匿名函数
        # 将请求头、响应头中的键值对取出来，并用换行符分隔
        # format_headers = lambda headers: '\n'.join(f'{k}: {v}' for k, v in headers.items())
        format_headers = lambda headers: '\n'.join([f'{k}: {v}' for k, v in headers.items()])
        # 不能用函数中嵌套函数的方式解决
        # def format_headers(headers):
        #     '\n'.join(f'{k}: {v}' for k, v in headers.items())
        # logger.info("{req.method} {req.url} {req.body}".format(req=response.request))
        # logger.info("{res.status_code} {res.text}".format(res=response))
        # textwrap.dedent可以将多段文本左对齐输出
        req = response.request
        # 请求头不一定非得格式化
        # req_headers = response.request.headers
        req_headers = format_headers(response.request.headers)
        res = response
        # 响应头不一定非得格式化
        # res_headers = response.headers
        res_headers = format_headers(response.headers)
        logger.debug(f'''
---------------- request ----------------
{req.method} {req.url}
{req_headers}

{req.body if req.body else ""}
---------------- response ----------------
{res.status_code} {res.reason} {res.url}
{res_headers}

{res.text if res.text else ""}
---------------- end ----------------
            '''
        )

    # 请求头和响应头处理方式二
    # 另写一个方法
    # def format_headers(self, headers):
    #     a = ''
    #     for k,v in headers.items():
    #         b = f'{k}: {v}\n'
    #         a += b
    #     return a


# 工具类
class HttpClient:
    def __init__(self, base_url):
        # 存域名
        self.base_url = base_url
        # 创建一个session对象
        self.session = requests.Session()

    def get(self, url, **kwargs):
        """
        :param url: api路由
        :return:
        """
        # 完整的接口请求地址
        full_url = self.base_url + url
        # print(f'GET {full_url}')
        r = self.session.get(full_url, **kwargs)
        # 先对响应进行处理，再返回
        return self.process(r)

    def options(self, url, **kwargs):
        full_url = self.base_url + url
        # print(f'OPTIONS {full_url}')
        r = self.session.options(full_url, **kwargs)
        return self.process(r)

    def head(self, url, **kwargs):
        full_url = self.base_url + url
        # print(f'HEAD {full_url}')
        r = self.session.head(full_url, **kwargs)
        return self.process(r)

    def post(self, url, data=None, json=None, **kwargs):
        full_url = self.base_url + url
        # print(f'POST {full_url}')
        r = self.session.post(full_url, data, json, **kwargs)
        return self.process(r)

    def put(self, url, data=None, **kwargs):
        full_url = self.base_url + url
        # print(f'PUT {full_url}')
        r = self.session.put(full_url, data, **kwargs)
        return self.process(r)

    def patch(self, url, data=None, **kwargs):
        full_url = self.base_url + url
        # print(f'PATCH {full_url}')
        r = self.session.patch(full_url, data, **kwargs)
        return self.process(r)

    def delete(self, url, **kwargs):
        full_url = self.base_url + url
        # print(f'DELETE {full_url}')
        r = self.session.patch(full_url, **kwargs)
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
    def __init__(self, base_url, username=None, password=None):
        # self.base_url = base_url
        self.http_object = HttpClient(base_url)
        self.use_jenkins = JenkinsOperation(self)
        # CSRF token 键和值
        # 存入属性的目的估计为了方便调试
        self.crumbField_name = None
        self.crumbField_value = None
        if username and password:
            self.login(username, password)

    def login(self, username, password):
        # 添加基本认证所需信息
        self.http_object.session.auth = username, password
        # 获取CSRF token键和值
        r = self.get_crumb()
        self.crumbField_name = r.body['crumbRequestField']
        self.crumbField_value = r.body['crumb']
        # 在请求头中添加CSRF token
        self.http_object.session.headers[self.crumbField_name] = self.crumbField_value
        return self

    def logout(self):
        # 删除请求头中CSRF token
        del self.http_object.session.headers[self.crumbField_name]
        # 删除基本认证信息
        self.http_object.session.auth = None
        self.crumbField_name = None
        self.crumbField_value = None

    def list_jobs(self, parameter='name'):
        return self.http_object.get(f'/api/json?tree=jobs[{parameter}]')

    def delete_job(self, name):
        "http://localhost:8080/job/hasaki/doDelete"
        return self.http_object.post(f'/job/{name}/doDelete')

    def get_user(self, username):
        return self.http_object.get(f'/user/{username}/api/json/')

    # 获取单个job详情
    def get_job(self, job):
        return self.http_object.get(f'/job/{job}/api/json')

    # 执行命令行脚本
    def run_groovy(self, script):
        payload = {"script": script}
        # 必须传给data而不是json
        return self.http_object.post('/scriptText/', data=payload)

    # 获取CSRF token
    def get_crumb(self):
        return self.http_object.get('/crumbIssuer/api/json/')


# Jenkins业务类
class JenkinsOperation:
    def __init__(self, jenkins):
        self.jenkins = jenkins

    def get_all_job_name(self):
        r = self.jenkins.list_jobs()
        print(r.raw_response.request.headers)
        job = [i['name'] for i in r.body['jobs']]
        return job

    def get_all_job_name_with_url(self):
        r = self.jenkins.list_jobs('name,url')
        job = {i['name']: i['url'] for i in r.body['jobs']}
        return job

    def create_job_with_dsl(self, dsl, job_name):
        r = self.jenkins.get_job(job_name)
        if r.code == 200:
            return "Fail:Job Aready Exist"
        script = f"""def jobDSL=\"\"\"{dsl}\"\"\";

                       def flowDefinition = new org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition(jobDSL, true);
                       def parent = Jenkins.instance;
                       def job = new org.jenkinsci.plugins.workflow.job.WorkflowJob(parent, "{job_name}")
                       job.definition = flowDefinition
                       job.save();
                       Jenkins.instance.reload()"""
        r = self.jenkins.run_groovy(script)
        r = self.jenkins.get_job(job_name)
        if r.code == 200 and r.body.get('displayName') == job_name:
            return f"OK:Job Created at {r.body.get('url')}"


if __name__ == '__main__':
    clear_log()
    logger = Mylog(log_level="DEBUG")
    admin = Jenkins('http://127.0.0.1:8080', 'admin', 'admin')
    job_dsl = """properties([parameters([string(name: 'Run', defaultValue: 'Yes', 
    description: 'a parameter')])])node {stage("test"){echo 'Hello World'}}"""
    admin.use_jenkins.create_job_with_dsl(job_dsl, 'hasaki')
    r = admin.delete_job('hasaki')
    print(r.code)
