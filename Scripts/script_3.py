import re

raw = ('11'
       'Main PID: 210 (systemd-network)'
       '22'
       )
# \d表示匹配数字，+表示匹配一次及以上
# 加()，即为要匹配的部分
pattern = re.compile('Main PID: (\d+)')
it = re.findall(pattern, raw)
print(it)
print(type(it))
