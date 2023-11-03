import requests


URL = "https://kartik-labeling-cvpr-0ed3099180c2.herokuapp.com/ecs152a_ass1"


headers = {"Student-Id": "920603707"}
response = requests.get(URL, headers=headers, verify='C:\\Users\\ouatt\\.mitmproxy\\mitmproxy-ca-cert.pem')

print(response.headers)