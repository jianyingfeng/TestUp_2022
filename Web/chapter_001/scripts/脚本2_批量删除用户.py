from Web.chapter_001.lib.domain.jenkins import Jenkins
from Web.chapter_001.lib.log import clear_log


clear_log()
admin = Jenkins()
user_list = admin.get_user_list()
for i in user_list:
    if i not in ['admin', 'test']:
        admin.delete_user(i)
