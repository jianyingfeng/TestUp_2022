# -*- coding: gbk -*-
import requests
import datetime,threading,shutil,os
from datetime import datetime, timezone, timedelta


class Result:
    def __init__(self, info=""):
        self.success = True
        self.info = info

    def __repr__(self):
        # 打印用
        return f"success={self.success}:{self.info}"

def clear_log():
    shutil.rmtree("logs",True)
    os.mkdir("logs")


def log(func):
    def inner(*args,**kwargs):
        r=func(*args,**kwargs)
        logger.info(f"{func.__name__} -> {r}")
        return r
    return inner



class MyLog:
    def __init__(self,log_level="INFO"):
        self.INFO = 1
        self.DEBUG = 2
        log_dict = {"INFO": self.INFO, "DEBUG": self.DEBUG}
        self.log_level = log_dict[log_level]

    def info(self,msg):
        # msg = msg if  #解决编码问题，gbk里没有\xa0，用空格替代
        timezone_offset = 8.0 #解决日志时区错误问题，设置为东8区
        tzinfo = timezone(timedelta(hours=timezone_offset))
        timestamp= datetime.now(tzinfo)
        try:
            scenario_name=threading.current_thread().scenario_name #暂时没用
        except:
            scenario_name = "UnNamed Scenario" #暂时没用
        if self.log_level >= self.INFO:
            print(f"[{scenario_name}][{timestamp}]{msg}".replace(u'\xa0', u' '))
        with open(f"logs//logs_{scenario_name}.txt","a") as f:
            f.write(f"[{timestamp}]{msg}\n".replace(u'\xa0', u' '))

    def debug(self,msg):
        # msg = msg.replace(u'\xa0', u' ') #解决编码问题，gbk里没有\xa0，用空格替代
        timezone_offset = 8.0 #解决日志时区错误问题，设置为东8区
        tzinfo = timezone(timedelta(hours=timezone_offset))
        timestamp= datetime.now(tzinfo)
        try:
            scenario_name=threading.current_thread().scenario_name #暂时没用
        except:
            scenario_name = "UnNamed Scenario" #暂时没用
        if self.log_level >= self.DEBUG:
            print(f"[{scenario_name}][{timestamp}]{msg}".replace(u'\xa0', u' '))
        with open(f"logs//logs_{scenario_name}.txt","a") as f:
            f.write(f"[{timestamp}]{msg}\n".replace(u'\xa0', u' '))


class Response:
    def __init__(self, code,body,raw_response):
        self.code = code
        self.body = body
        self.response = raw_response
        self.print_raw_request(raw_response)

    def __repr__(self):
        # 打印原始响应的状态码
        return f"{self.code} {self.body}"

    def print_raw_request(self,response):
        format_headers = lambda d: '\n'.join(f'{k}: {v}' for k, v in d.items())
        # 去掉了日志的简略输出。因为基本上也没什么用。
        # logger.info("{req.method} {req.url} {req.body}".format(req=response.request))
        # logger.info("{res.status_code} {res.text}".format(res=response))

        # 修改了下列日志的输出方式，去掉了format，增加了当body为空时不打印
        req = response.request
        res = response
        reqhdrs = format_headers(response.request.headers)
        reshdrs = format_headers(response.headers)
        logger.debug(f'''
---------------- request ----------------
{req.method} {req.url}
{reqhdrs}

{req.body if req.body else ""}
---------------- response ----------------
{res.status_code} {res.reason} {res.url}
{reshdrs}

{res.text if res.text else ""}
---------------- end ---------------------
''')


class RestClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def options(self,endpoint, **kwargs):
        r = self.session.options(self.base_url+endpoint, **kwargs)
        return self.process(r)

    def head(self,endpoint, **kwargs):
        r = self.session.head(self.base_url+endpoint, **kwargs)
        return self.process(r)

    def get(self,endpoint, **kwargs):
        r = self.session.get(self.base_url+endpoint, **kwargs)
        return self.process(r)

    def post(self,endpoint, data=None, json=None, **kwargs):
        r = self.session.post(self.base_url+endpoint,data, json, **kwargs)
        return self.process(r)

    def put(self,endpoint, data=None, **kwargs):
        r = self.session.put(self.base_url+endpoint, data, **kwargs)
        return self.process(r)

    def patch(self,endpoint, data=None, **kwargs):
        r = self.session.patch(self.base_url+endpoint,data, **kwargs)
        return self.process(r)

    def delete(self,endpoint, **kwargs):
        r = self.session.delete(self.base_url+endpoint,**kwargs)
        return self.process(r)


    @staticmethod
    def process(response):
        code = response.status_code
        try:
            body = response.json()
        except:
            body = str(response.content)
        return Response(code, body, response)


class JenkinsOperation:
    def __init__(self, jenkins):
        self.jenkins = jenkins

    @log
    def get_all_job_names(self):
        r = self.jenkins.list_jobs()
        jobs = [_['name'] for _ in r.body['jobs']]
        return jobs

    @log
    def get_all_job_names_with_url(self):
        r = self.jenkins.list_jobs("name,url")
        jobs = {_['name']:_['url'] for _ in r.body['jobs']}
        return jobs

    @log
    def delete_all_jobs(self):
        names = self.get_all_job_names()
        for name in names:
            self.jenkins.delete_job(name)
        return Result(f"{names} all deleted")

    @log
    def create_job_with_dsl(self, dsl, job_name):
        result = Result()
        r = self.jenkins.get_job(job_name)
        if r.code == 200:
            result.success = False
            result.info = "Job Aready Exist"
            return result
        script = f"""def jobDSL=\"\"\"{dsl}\"\"\";
def flowDefinition = new org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition(jobDSL, true);
def parent = Jenkins.instance;
def job = new org.jenkinsci.plugins.workflow.job.WorkflowJob(parent, "{job_name}")
job.definition = flowDefinition
job.save();
Jenkins.instance.reload()"""
        self.jenkins.run_groovy(script)
        r = self.jenkins.get_job(job_name)
        if r.code == 200 and r.body.get("displayName")== job_name:
            result.success = True
            result.info = f"Job Created at {r.body.get('url')}"
            return result
        else:
            result.success= False
            result.info = f"Job={job_name} Created Failed"
            return result

class Jenkins:
    def __init__(self, base_url, username=None, password=None):
        self.base_url = base_url
        # 用rest client替代requests的session
        self.rest_client = RestClient(base_url)
        self.use_jenkins = JenkinsOperation(self)
        self.crumb_field_name = None
        self.crumb_field_value = None
        # 增加了在初始化时登入的机制
        if username and password:
            self.login(username,password)


    def login(self,username,password):
        self.rest_client.session.auth = username, password
        r = self.get_crumber_issuer()
        self.crumb_field_name = r.body['crumbRequestField']
        self.crumb_field_value = r.body['crumb']
        # 在session中设置curmb的字段名和值
        self.rest_client.session.headers[self.crumb_field_name] = self.crumb_field_value
        return self

    def logout(self):
        self.rest_client.auth = None
        del self.rest_client.session.headers[self.crumb_field_name]
        self.crumb_field_name = None
        self.crumb_field_value = None

    def get_crumber_issuer(self):
        return self.rest_client.get("/crumbIssuer/api/json")


    def list_jobs(self,attribute_to_show="name"):
        return self.rest_client.get(f"/api/json?tree=jobs[{attribute_to_show}]")

    def get_user(self, username):
        return self.rest_client.get(f"/user/{username}/api/json")

    # def build(self,path):
    #     return self.rest_client.post(f"{path}/build")
    #
    # def build_with_parameters(self,path,params):
    #     return self.rest_client.post(f"{path}/buildWithParameters",params=params)

    def run_groovy(self,script):
        payload = {'script': script}
        return self.rest_client.post(f"/scriptText", data=payload)

    def get_job(self,job):
        return self.rest_client.get(f"/job/{job}/api/json")

    def delete_job(self,job_name):
        return self.rest_client.post(f"/job/{job_name}/doDelete")


if __name__=="__main__":
    clear_log()
    logger = MyLog() #默认info级
    admin = Jenkins("http://localhost:8080","admin","admin")
    job_dsl = """properties([parameters([string(name: 'Run', defaultValue: 'Yes', description: 'a parameter')])])node {stage("test"){echo 'Hello World'}}"""
    r = admin.use_jenkins.get_all_job_names()
    # r = admin.use_jenkins.delete_all_jobs()
    # r1 = admin.use_jenkins.create_job_with_dsl(job_dsl, "testjob0001")
    # r2 = admin.use_jenkins.create_job_with_dsl(job_dsl, "testjob0001")
    # r = admin.use_jenkins.delete_all_jobs()
