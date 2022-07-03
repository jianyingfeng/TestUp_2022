# import pytest
#
# from libs.jenkins import Jenkins
#
#
# admin = Jenkins("http://localhost:8080", "admin", "admin")
# nobody = Jenkins("http://localhost:8080")
#
#
# @pytest.mark.parametrize("user, to_get",
#                          [
#                              [admin, "admin"],
#                              (admin, "test"),
#                              (nobody, "admin"),
#                              (nobody, "not exists"),
#                              (nobody, "test")
#                          ])
# def test_jenkins_get_user_by_admin1(user, to_get):
#     actual_result = user.get_user(to_get)
#     assert actual_result.body["absoluteUrl"] == f"http://localhost:8080/user/{to_get}"
#     assert actual_result.body["fullName"] == to_get
#
#
# if __name__ == '__main__':
#     pytest.main()
