import requests


session = requests.session()
session.auth = "admin", "admin"
r1 = session.get('http://localhost:8080/crumbIssuer/api/json/')
crumbField_name = r1.json()['crumbRequestField']
crumbField_value = r1.json()['crumb']
session.headers[crumbField_name] = crumbField_value
r2 = session.post('http://localhost:8080/job/hasaki111/doDelete')
print(r2)