"""
基础Action类 - 所有Action的基类
"""
import logging
from typing import Any

logger = logging.getLogger(__name__)


class BaseAction:
    """Action基类，提供通用的HTTP请求方法"""
    
    def __init__(self, client):
        """
        初始化Action
        
        Args:
            client: Locust的HttpUser.client对象，用于发送HTTP请求
        """
        self.client = client
    
    def _post(self, endpoint: str, json_data: dict[str, Any], name: str | None = None, headers: dict[str, str] | None = None) -> dict[str, object] | list[dict[str, object]]:
        """
        发送POST请求的通用方法
        
        Args:
            endpoint: API端点路径
            json_data: 请求体JSON数据
            name: Locust统计中的名称（如果为None，使用endpoint）
            headers: 请求头（可选，用于认证等）
            
        Returns:
            响应JSON数据
        """
        response = self.client.post(
            endpoint,
            json=json_data,
            name=name or endpoint,
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            return {"status_code": 403, "message": "权限不足"}
        else:
            return {"status_code": response.status_code, "message": response.text}
    
    def _get(self, endpoint: str, params: dict[str, object] | None = None, name: str | None = None) -> list[dict[str, object]] | dict[str, object]:
        """
        发送GET请求的通用方法
        
        Args:
            endpoint: API端点路径
            params: URL参数
            name: Locust统计中的名称（如果为None，使用endpoint）
            
        Returns:
            响应JSON数据（可能是字典或列表）
        """
        response = self.client.get(
            endpoint,
            params=params,
            name=name or endpoint
        )
        
        if response.status_code == 200:
            try:
                return response.json()
            except:
                # 如果不是JSON，返回文本
                return {"status_code": 200, "message": response.text}
        elif response.status_code == 403:
            return {"status_code": 403, "message": "权限不足", "status": 0}
        else:
            try:
                # 尝试解析错误响应中的JSON
                error_data = response.json()
                return error_data
            except:
                return {"status_code": response.status_code, "message": response.text, "status": 0}
    
    def _put(self, endpoint: str, json_data: dict[str, object], name: str | None = None) -> dict[str, object]:
        """
        发送PUT请求的通用方法
        
        Args:
            endpoint: API端点路径
            json_data: 请求体JSON数据
            name: Locust统计中的名称（如果为None，使用endpoint）
            
        Returns:
            响应JSON数据
        """
        response = self.client.put(
            endpoint,
            json=json_data,
            name=name or endpoint
        )
        
        if response.status_code == 200:
            try:
                return response.json()
            except:
                return {"status_code": 200, "message": response.text}
        else:
            try:
                error_data = response.json()
                return error_data
            except:
                return {"status_code": response.status_code, "message": response.text, "status": 0}
    
    def _delete(self, endpoint: str, name: str | None = None, headers: dict[str, str] | None = None) -> dict[str, object]:
        """
        发送DELETE请求的通用方法
        
        Args:
            endpoint: API端点路径
            name: Locust统计中的名称（如果为None，使用endpoint）
            headers: 请求头（可选，用于认证等）
            
        Returns:
            响应JSON数据
        """
        response = self.client.delete(
            endpoint,
            name=name or endpoint,
            headers=headers
        )
        
        if response.status_code == 200:
            try:
                return response.json()
            except:
                return {"status_code": 200, "message": response.text}
        else:
            try:
                error_data = response.json()
                return error_data
            except:
                return {"status_code": response.status_code, "message": response.text, "status": 0}

