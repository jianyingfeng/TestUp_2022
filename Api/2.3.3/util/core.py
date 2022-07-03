import requests

from util.log import logger


class Operation:
    def __getattribute__(self, item):
        # 返回是属性名称或方法名称，并非方法执行的结果
        result = super().__getattribute__(item)
        # 如果result类型是方法，则打印日志
        # 如果result类型是属性，则直接返回
        if type(result) == type(logger.info):
            def log(*args, **kwargs):
                # 执行方法，获取响应结果
                res = result(*args, **kwargs)
                # 如果响应不是Response的实例，才记录日志
                # 即如果调的是API类的方法，不记录日志
                # 调的是业务类的方法，才记录日志
                if not isinstance(res, Response):
                    logger.info(f"{result.__name__} -> {res}")
                return res

            return log
        return result


# 处理业务类返回值的数据类
class Result:
    def __init__(self, success=True, info=""):
        self.success = success
        self.info = info

    def __repr__(self):
        return f"{self.success}：{self.info}"


# 处理API类返回值的数据类
class Response:
    def __init__(self, code, body, raw_response):
        self.code = code
        self.body = body
        self.raw_response = raw_response
        # 有重定向请求时，会打印重定向过程中的请求
        self.print_history(raw_response)
        # 在构造函数里面调用示例方法，那么每次实例化对象时，都会自动调用该方法
        self.print_raw_response(raw_response)

    # 魔术方法，打印这个类时会自动调用这个方法
    def __repr__(self):
        # 返回响应状态码和响应体
        return f"{self.code} {self.body}"

    def print_history(self, response):
        for r in response.history:
            self.print_raw_response(r)

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
        req_headers = format_headers(response.request.headers)
        res = response
        res_headers = format_headers(response.headers)
        # 写成res.text而不是res.json()的目的是当响应返回的是html时，不会报错
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
''')

    # 请求头和响应头处理方式二
    # 另写一个方法
    # def format_headers(self, headers):
    #     a = ''
    #     for k,v in headers.items():
    #         b = f'{k}: {v}\n'
    #         a += b
    #     return a


# 发送请求的工具类
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
        return self.request('get', full_url, **kwargs)

    def options(self, url, **kwargs):
        full_url = self.base_url + url
        return self.request('options', full_url, **kwargs)

    def head(self, url, **kwargs):
        full_url = self.base_url + url
        return self.request('head', full_url, **kwargs)

    def post(self, url, **kwargs):
        full_url = self.base_url + url
        return self.request('post', full_url, **kwargs)

    def put(self, url, **kwargs):
        full_url = self.base_url + url
        return self.request('put', full_url, **kwargs)

    def patch(self, url, **kwargs):
        full_url = self.base_url + url
        return self.request('patch', full_url, **kwargs)

    def delete(self, url, **kwargs):
        full_url = self.base_url + url
        return self.request('delete', full_url, **kwargs)

    # 该方法用于判断csrf token是否失效，失效则重新登录
    # 然后重新请求
    def request(self, method_name, url, **kwargs):
        r = self.session.request(method_name, url, **kwargs)
        # r = getattr(self.session, method_name)(url, **kwargs)
        if r.status_code == 403 and 'No valid crumb' in r.text:
            # HttpClient类并没有这个方法，是在Jenkins类中添加的
            self.authenticate()
            r = self.session.request(method_name, url, **kwargs)
            # r = getattr(self.session, method_name)(url, **kwargs)
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
