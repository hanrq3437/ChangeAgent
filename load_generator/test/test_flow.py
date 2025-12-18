#!/usr/bin/env python3
"""
Flow测试脚本 - 简单直接地测试Flow
"""
import sys
import json
import logging
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 配置日志 - 让Flow中的logger信息能够输出到终端
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

import requests
import config
from flow import SimpleQueryFlow, SimpleLoginFlow, SimpleRegisterFlow, BookingFlow


class SimpleClient:
    """简单的HTTP客户端，用于测试Flow"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update(config.DEFAULT_HEADERS)
    
    def _build_url(self, endpoint: str) -> str:
        if endpoint.startswith('http'):
            return endpoint
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        return self.base_url + endpoint
    
    def post(self, endpoint: str, json: dict[str, object] | None = None, name: str | None = None, headers: dict[str, str] | None = None):
        url = self._build_url(endpoint)
        request_headers = dict(self.session.headers)
        if headers:
            request_headers.update(headers)
        response = self.session.post(url, json=json, headers=request_headers, timeout=config.REQUEST_TIMEOUT)
        return SimpleResponse(response)
    
    def get(self, endpoint: str, params: dict[str, object] | None = None, name: str | None = None, headers: dict[str, str] | None = None):
        url = self._build_url(endpoint)
        request_headers = dict(self.session.headers)
        if headers:
            request_headers.update(headers)
        response = self.session.get(url, params=params, headers=request_headers, timeout=config.REQUEST_TIMEOUT)  # type: ignore
        return SimpleResponse(response)
    
    def put(self, endpoint: str, json: dict[str, object] | None = None, name: str | None = None, headers: dict[str, str] | None = None):
        url = self._build_url(endpoint)
        request_headers = dict(self.session.headers)
        if headers:
            request_headers.update(headers)
        response = self.session.put(url, json=json, headers=request_headers, timeout=config.REQUEST_TIMEOUT)
        return SimpleResponse(response)
    
    def delete(self, endpoint: str, name: str | None = None, headers: dict[str, str] | None = None):
        url = self._build_url(endpoint)
        request_headers = dict(self.session.headers)
        if headers:
            request_headers.update(headers)
        response = self.session.delete(url, headers=request_headers, timeout=config.REQUEST_TIMEOUT)
        return SimpleResponse(response)


class SimpleResponse:
    """简单的响应对象"""
    
    def __init__(self, response: requests.Response):
        self._response = response
        self.status_code = response.status_code
        self.text = response.text
        self._json = None
    
    def json(self):
        if self._json is None:
            try:
                self._json = self._response.json()
            except (ValueError, AttributeError):
                self._json = {}
        return self._json


def print_result(result: dict):
    """打印测试结果"""
    print(f"\n{'='*60}")
    print(f"成功: {result.get('success', False)}")
    
    if result.get('success'):
        print("✅ 流程执行成功")
        if 'token' in result:
            token = result['token']
            print(f"Token: {token[:20]}..." if token and len(str(token)) > 20 else f"Token: {token}")
        if 'trip_id' in result:
            print(f"车次ID: {result['trip_id']}")
        if 'order_id' in result:
            print(f"订单ID: {result['order_id']}")
        if 'data' in result:
            data = result['data']
            if isinstance(data, list):
                print(f"数据条数: {len(data)}")
    else:
        print(f"❌ 流程执行失败: {result.get('error', '未知错误')}")
    
    print(f"\n完整结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"{'='*60}\n")


def main():
    """主函数"""
    print(f"目标服务器: {config.BASE_URL}\n")
    
    # 创建客户端
    client = SimpleClient(config.BASE_URL)
    
    # 解析命令行参数
    if len(sys.argv) > 1:
        flow_name = sys.argv[1].lower()
        
        if flow_name == "query":
            print("测试 SimpleQueryFlow")
            flow = SimpleQueryFlow(client)
            result = flow.execute()
            print_result(result)
            
        elif flow_name == "login":
            print("测试 SimpleLoginFlow")
            flow = SimpleLoginFlow(client)
            result = flow.execute()
            print_result(result)
            
        elif flow_name == "register":
            print("测试 SimpleRegisterFlow")
            flow = SimpleRegisterFlow(client)
            result = flow.execute()
            print_result(result)
            
        elif flow_name == "booking":
            print("测试 BookingFlow")
            flow = BookingFlow(client)
            result = flow.execute()
            print_result(result)
            
        else:
            print(f"❌ 未知的Flow: {flow_name}")
            print("\n可用选项:")
            print("  query    - 测试 SimpleQueryFlow")
            print("  login    - 测试 SimpleLoginFlow")
            print("  register - 测试 SimpleRegisterFlow")
            print("  booking  - 测试 BookingFlow")
    else:
        # 默认测试所有
        print("测试所有Flow...\n")
        
        print("1. SimpleQueryFlow")
        flow = SimpleQueryFlow(client)
        result = flow.execute()
        print_result(result)
        
        print("2. SimpleLoginFlow")
        flow = SimpleLoginFlow(client)
        result = flow.execute()
        print_result(result)
        
        print("3. SimpleRegisterFlow")
        flow = SimpleRegisterFlow(client)
        result = flow.execute()
        print_result(result)
        
        print("4. BookingFlow")
        flow = BookingFlow(client)
        result = flow.execute()
        print_result(result)


if __name__ == "__main__":
    main()


"""
用法示例：
python test_flow.py query  # 测试查询流程
python test_flow.py login  # 测试登录流程
python test_flow.py register  # 测试注册流程
python test_flow.py booking  # 测试订票流程
"""