"""
基础Flow类 - 所有Flow的基类
"""
import logging
from action import AuthAction, TravelAction

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
    
    def _extract_order_id(self, preserve_result: dict[str, object]) -> str | None:
        """
        从预订结果中提取订单ID
        
        Args:
            preserve_result: 预订响应数据
            
        Returns:
            订单ID字符串，如果未找到则返回None
        """
        if isinstance(preserve_result, dict):
            data = preserve_result.get("data", {})
            if isinstance(data, dict):
                return data.get("id") or data.get("orderId")
            elif isinstance(data, str):
                return data
            else:
                return preserve_result.get("id") or preserve_result.get("orderId")
        return None
    
    def _select_available_trip(self, trips: list) -> dict[str, object] | None:
        """
        从车次列表中选择第一个有票的车次
        
        Args:
            trips: 车次列表
            
        Returns:
            选中的车次信息，如果没有则返回None
        """
        for trip in trips:
            if isinstance(trip, dict):
                tickets = trip.get("tickets", {})
                if isinstance(tickets, dict):
                    economy = tickets.get("economyClass", {})
                    if isinstance(economy, dict) and economy.get("num", 0) > 0:
                        return trip
        return None

