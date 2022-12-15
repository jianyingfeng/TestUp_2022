import requests


class Response:
    def __init__(self, code, body, raw_response):
        self.code = code
        self.body = body
        self.raw_response = raw_response

    def __repr__(self):
        return f'code:{self.code}\nbody:{self.body}'


class HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, url, **kwargs):
        url = self.base_url + url
        print(f'GET {url}')
        res = self.session.get(url, **kwargs)
        return self.process(res)

    def options(self, url, **kwargs):
        url = self.base_url + url
        print(f'OPTIONS {url}')
        res = self.session.options(url, **kwargs)
        return self.process(res)

    def head(self, url, **kwargs):
        url = self.base_url + url
        print(f'HEAD {url}')
        res = self.session.head(url, **kwargs)
        return self.process(res)

    def post(self, url, data=None, json=None, **kwargs):
        url = self.base_url + url
        print(f'POST {url}')
        res = self.session.post(url, data=data, json=json, **kwargs)
        return self.process(res)

    def put(self, url, data=None, **kwargs):
        url = self.base_url + url
        print(f'PUT {url}')
        res = self.session.put(url, data=data, **kwargs)
        return self.process(res)

    def patch(self, url, data=None, **kwargs):
        url = self.base_url + url
        print(f'PATCH {url}')
        res = self.session.patch(url, data=data, **kwargs)
        return self.process(res)

    def delete(self, url, **kwargs):
        url = self.base_url + url
        print(f'DELETE {url}')
        res = self.session.delete(url, **kwargs)
        return self.process(res)

    def process(self, res):
        code = res.status_code
        try:
            body = res.json()
        except:
            body = str(res.content)
        return Response(code, body, res)


class Jenkins:
    def __init__(self, base_url):
        self.http_object = HttpClient(base_url)
        self.use_jenkins = JenkinsOperation(self)
        self.crumbRequestField = None
        self.crumb = None

    def login(self, username, password):
        self.http_object.session.auth = username, password
        res = self.get_csrf_token()
        self.crumbRequestField = res.body['crumbRequestField']
        self.crumb = res.body['crumb']
        self.http_object.session.headers[self.crumbRequestField] = self.crumb
        return self

    def get_csrf_token(self):
        return self.http_object.get('/crumbIssuer/api/json/')

    def logout(self):
        del self.http_object.session.headers[self.crumbRequestField]
        self.http_object.session.auth = None
        self.crumbRequestField = None
        self.crumb = None

    def list_jobs(self, attribute_name='name'):
        url = f'/api/json?tree=jobs[{attribute_name}]'
        return self.http_object.get(url)

    def get_user(self, user):
        url = f'/user/{user}/api/json/'
        return self.http_object.get(url)


class JenkinsOperation:
    def __init__(self, jenkins):
        self.jenkins = jenkins

    def get_all_jobs_name(self):
        res = self.jenkins.list_jobs('name')
        print(res.raw_response.request.headers)
        jobs = [i['name'] for i in res.body['jobs']]
        return jobs

    def get_all_jobs_name_with_url(self):
        res = self.jenkins.list_jobs('name,url')
        jobs = {i['name']: i['url'] for i in res.body['jobs']}
        return jobs


if __name__ == '__main__':
    amo = Jenkins('http://localhost:8080').login('admin', 'admin')
    # res_1 = amo.list_jobs()
    # print(res_1.code)
    # print(res_1.body)
    # print(res_1)
    # print(f'jobs = {[i["name"] for i in res_1.body["jobs"]]}')

    # res_2 = amo.get_user('admin')
    # print(f'获取用户原始响应：{res_2}')

    # res_3 = amo.get_user('jyf')
    # print(f'获取用户原始响应：{res_3}')

    # res_4 = amo.get_all_jobs_name()
    # print(res_4)
    #
    # res_5 = amo.get_all_jobs_name_with_url()
    # print(res_5)

    res_6 = amo.use_jenkins.get_all_jobs_name()
    print(res_6)
    # res_7 = amo.use_jenkins.get_all_jobs_name_with_url()
    # print(res_7)