import urllib3
import json

# 创建 PoolManager 对象
http = urllib3.PoolManager()

# 发送 GET 请求
def get():
    response = http.request('GET', 'https://ky9oss.top')
    print(response.status)      # 响应状态码
    print(response.data.decode('utf-8'))    # 响应内容

# 发送 POST 请求
def post():
    data = {'field1': 'value1', 'field2': 'value2'}
    response = http.request('POST', 'http://httpbin.org/post', fields=data)
    print(response.status)      # 响应状态码
    print(response.data.decode('utf-8'))    # 响应内容


# 发送 POST 请求，发送 JSON 数据
def post_json():
    data = {'field1': 'value1', 'field2': 'value2'}
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(data).encode('utf-8')
    response = http.request('POST', 'http://httpbin.org/post',
                            body=json_data, headers=headers)
    print(response.status)      # 响应状态码
    print(response.data.decode('utf-8'))    # 响应内容


if __name__ == '__main__':
    get()
