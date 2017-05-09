import requests
import json
import sys


class Client():
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def login(self):
        login_payload = "object={'login':{'username':'%s','password':'%s'}}" % ( self.username, self.password )
        login_endpoint = "http://%s/nitro/v1/config/login" % ( self.host )
        result = requests.post(login_endpoint, data=login_payload)
        cookie_header = result.headers.get('Set-Cookie')
        self.headers = {"Cookie": str(cookie_header)}

    def logout(self):
        requests.delete("http://%s/nitro/v1/config/login" % (self.host))
        self.headers = None

    def get(self, endpoint):
        url = "http://%s/%s" % ( self.host, endpoint )
        return requests.get(url ,headers=self.headers)

    def post(self, endpoint, body):
        url = "http://%s/%s" % ( self.host, endpoint )
        return requests.post(url, data=body,headers=self.headers)


if __name__ == "__main__":
    host = str(sys.argv[1])
    username = str(sys.argv[2])
    password = str(sys.argv[3])

    print("username: " + username)
    print("password: " + password)
    print("host: " + host)

    client = Client(host, username, password)

    client.login()
    endpoint = "nitro/v1/config/sdx_license"
    response = client.get(endpoint)
    print("endpoint: " + endpoint)
    print(response)
    print(json.dumps(response.json(),indent=4))

    license_count = 0
    for sdx_license in response.json().get("sdx_license"):
        license_count += int(sdx_license.get("max_number_of_ns_instances"))

    print("Number of instances available for this license: " + str(license_count))

    endpoint = "nitro/v1/config/ns"
    body = "object={'ns':{'ip_address':'10.66.8.90', 'name':'sdx-vpx-1', 'gateway':'10.66.8.47', 'network_interfaces':[{'port_name':'1/3'}], 'vm_memory_total':'2048' }}"
    response = client.post(endpoint, body)
    print("endpoint: " + endpoint)
    print(response)
    print(json.dumps(response.json(),indent=4))

    client.logout()
