"""
API接口测试脚本 - 简洁版
"""
import requests
import json

BASE_URL = "http://10.10.1.98:32677"

# ============================================================================
# 通用响应处理函数
# ============================================================================
def print_response(response):
    """智能打印响应内容，自动适配不同类型"""
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type', 'unknown')}")
    
    content_type = response.headers.get('Content-Type', '').lower()
    
    # 尝试解析JSON
    if 'application/json' in content_type:
        try:
            data = response.json()
            print("Response (JSON):")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            print("Response (Text):")
            print(response.text)
    # 处理文本类型
    elif 'text/' in content_type:
        print("Response (Text):")
        print(response.text)
    # 处理HTML
    elif 'text/html' in content_type:
        print("Response (HTML):")
        print(response.text[:500])  # 只打印前500字符
    # 处理二进制
    elif 'image/' in content_type or 'application/octet-stream' in content_type:
        print(f"Response (Binary): {len(response.content)} bytes")
    # 其他情况，尝试JSON，失败则显示文本
    else:
        try:
            data = response.json()
            print("Response (JSON):")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            if response.text:
                print("Response (Text):")
                print(response.text)
            else:
                print(f"Response (Empty or Binary): {len(response.content)} bytes")

# ============================================================================
# GET请求示例
# ============================================================================
def test_get():
    endpoint = "/api/v1/users"
    url = f"{BASE_URL}{endpoint}"
    
    print(f"GET {url}")
    response = requests.get(url)
    print_response(response)

# ============================================================================
# POST请求示例
# ============================================================================
def test_post():
    endpoint = "/api/v1/users/login"
    url = f"{BASE_URL}{endpoint}"
    data = {
        "username": "fdse_microservice",
        "password": "111111"
    }
    
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
    response = requests.post(url, json=data)
    print_response(response)
    
    # 如果登录成功，提取token
    if response.status_code == 200:
        try:
            result = response.json()
            token = result.get("data", {}).get("token")
            if token:
                print(f"\n✅ Token: {token[:50]}...")
                return token
        except:
            pass
    return None

# ============================================================================
# 带认证的GET请求示例
# ============================================================================
def test_get_with_auth():
    # 先登录获取token
    token = None
    endpoint = "/api/v1/users/login"
    url = f"{BASE_URL}{endpoint}"
    data = {
        "username": "admin",
        "password": "222222"
    }
    
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
    response = requests.post(url, json=data)
    print_response(response)
    
    # 如果登录成功，提取token
    if response.status_code == 200:
        try:
            result = response.json()
            token = result.get("data", {}).get("token")
            if token:
                print(f"\n✅ Token: {token[:50]}...")
        except:
            pass

    if not token:
        print("❌ 登录失败，无法获取token")
        return
    
    endpoint = "/api/v1/adminuserservice/users"
    url = f"{BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "documentType": "1",
        "documentNum": "123456789012345678",
        "email": "test@test.com",
        "gender": "1",
        "userName": "test",
        "password": "111111"
    }
    print(f"\nPOST {url} (with token)")
    response = requests.post(url, json=data, headers=headers)
    print_response(response)

# ============================================================================
# 在这里修改要测试的接口
# ============================================================================
if __name__ == "__main__":
    # 取消注释要测试的方法
    # test_get()  # 不带认证的GET请求（可能返回403）
    # test_post()  # 登录获取token
    test_get_with_auth()  # 带认证的GET请求
