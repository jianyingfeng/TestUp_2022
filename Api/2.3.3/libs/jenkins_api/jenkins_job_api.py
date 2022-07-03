# Job接口类
class JenkinsJobApi:

    def list_jobs(self, parameter='name'):
        return self.http_object.get(f'/api/json?tree=jobs[{parameter}]')

    def delete_job(self, name):
        "http://localhost:8080/job/hasaki/doDelete"
        # allow_redirects=False 不允许重定向
        # return self.http_object.post(f'/job/{name}/doDelete', allow_redirects=False)
        return self.http_object.post(f'/job/{name}/doDelete')

    def get_user(self, username):
        return self.http_object.get(f'/user/{username}/api/json/')

    # 获取单个job详情
    def get_job(self, job):
        return self.http_object.get(f'/job/{job}/api/json')
