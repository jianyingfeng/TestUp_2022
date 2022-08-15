import pytest

from libs.jenkins import Jenkins
from util.log import logger


def test_jenkins_get_user_by_admin1():
    admin = Jenkins("http://localhost:8080", "admin", "admin")
    actual_result = admin.get_user("test")
    assert actual_result.body["absoluteUrl"] == "http://localhost:8080/user/test"
    assert actual_result.body["fullName"] == "test"


def test_jenkins_get_user_by_admin2():
    admin = Jenkins("http://localhost:8080", "admin", "admin")
    actual_result = admin.get_user("admin")
    assert actual_result.body["absoluteUrl"] == "http://localhost:8080/user/admin"
    assert actual_result.body["fullName"] == "admin"


def test_jenkins_get_user_by_nobody1():
    amo = Jenkins("http://localhost:8080")
    actual_result = amo.get_user("test")
    assert actual_result.body["absoluteUrl"] == "http://localhost:8080/user/test"
    assert actual_result.body["fullName"] == "test"


def test_jenkins_get_user_by_nobody2():
    amo = Jenkins("http://localhost:8080")
    actual_result = amo.get_user("notxx")
    assert actual_result.body["absoluteUrl"] == "http://localhost:8080/user/notxx"
    assert actual_result.body["fullName"] == "notxx"


def test_jenkins_get_user_by_nobody3():
    amo = Jenkins("http://localhost:8080")
    actual_result = amo.get_user("admin")
    assert actual_result.body["absoluteUrl"] == "http://localhost:8080/user/admin"
    assert actual_result.body["fullName"] == "admin"


if __name__ == '__main__':
    pytest.main(["-s"])
