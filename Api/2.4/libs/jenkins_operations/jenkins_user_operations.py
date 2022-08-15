from util.core import Operation
from libs.jenkins_api.jenkins_user_api import JenkinsUserApi
from util.core import Result


# 用户业务类
class JenkinsUserOperation(Operation, JenkinsUserApi):

    # 获取所有用户名
    def get_all_usernames(self):
        r = self.asynch_people()
        usernames = [i['user']['fullName'] for i in r.body['users']]
        return usernames