import subprocess

# # 绝对路径
# subprocess.run(r'python C:\Users\Jyf\Desktop\TestUp\Web\chapter_001\test_sce\场景2_快捷登录.py')
# # 相对路径
# subprocess.run(r'python ..\test_sce\场景2_快捷登录.py')


def execuotr_one_test(path):
    # logger.info(f"开始执行测试：{path}")
    subprocess.run(path)
