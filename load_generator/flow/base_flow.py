"""
基础Flow类 - 所有Flow的基类
"""
import logging
from action import AuthAction, TravelAction, ContactAction

logger = logging.getLogger(__name__)


class BaseFlow:
    """Flow基类，提供通用的流程执行框架"""
    
    def __init__(self, client):
        """
        初始化Flow
        
        Args:
            client: Locust的HttpUser.client对象
        """
        self.client = client
        # 初始化各个Action类
        self.auth = AuthAction(client)
        self.travel = TravelAction(client)
        self.contact = ContactAction(client)
    
    def execute(self, *args, **kwargs) -> dict[str, object]:
        """
        执行流程（子类必须实现）
        
        Args:
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            执行结果字典
        """
        raise NotImplementedError("子类必须实现execute方法")
    
    def _extract_token(self, login_result: dict[str, object]) -> str | None:
        """
        从登录结果中提取token
        
        Args:
            login_result: 登录响应数据
            
        Returns:
            token字符串，如果未找到则返回None
        """
        if isinstance(login_result, dict):
            data = login_result.get("data", {})
            if isinstance(data, dict):
                return data.get("token")
        return None
    
    def _extract_user_id(self, login_result: dict[str, object]) -> str | None:
        """
        从登录结果中提取用户ID
        
        Args:
            login_result: 登录响应数据
            
        Returns:
            用户ID字符串，如果未找到则返回None
        """
        if isinstance(login_result, dict):
            data = login_result.get("data", {})
            if isinstance(data, dict):
                return data.get("userId")
        return None
    