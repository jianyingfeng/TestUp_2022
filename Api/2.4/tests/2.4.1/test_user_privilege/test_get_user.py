from libs.jenkins import Jenkins
import pytest


# 测试数据
admin = Jenkins('http://localhost:8080', 'admin', 'admin')
nobody = Jenkins('http://localhost:8080')


# 跟测试紧密相关的一些公用方法
def get_user(user_to_get, login_user):
    actual_result = login_user.get_user(user_to_get)
    return actual_result


def check_get_user_result(actual_result, expected_status_code, user_to_get, expected_full_name):
    assert actual_result.code == expected_status_code
    if actual_result.code != 404:
        assert actual_result.body['absoluteUrl'] == 'http://localhost:8080/user/' + user_to_get
        assert actual_result.body['fullName'] == expected_full_name