# 用户接口
class JenkinsUserApi:
    # 获取单个用户详情
    def get_user(self, username):
        return self.http_object.get(f'/user/{username}/api/json/')

    # 获取用户列表
    def asynch_people(self):
        return self.http_object.get('/asynchPeople/api/json')