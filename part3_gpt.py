import requests

url = "https://kartik-labeling-cvpr-0ed3099180c2.herokuapp.com/ecs152a_ass1"
headers = {
    "Student-Id": "920603707",
}

# Specify the path to your custom certificate file
certificate_path = "C:\\Users\\ouatt\\.mitmproxy\\mitmproxy-ca-cert.pem"

response = requests.get(url, headers=headers, verify=certificate_path)

# Print the response header
print("Response Header:")
for key, value in response.headers.items():
    print(f"{key}: {value}")
