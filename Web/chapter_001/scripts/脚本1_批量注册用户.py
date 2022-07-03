from Web.chapter_001.lib.domain.jenkins import Jenkins
from Web.chapter_001.lib.log import clear_log


clear_log()
admin = Jenkins()
for i in range(10):
    admin.register_test_user('jyf' + '00' + str(i), 123456)
