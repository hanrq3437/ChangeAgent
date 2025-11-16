"""
简单Flow - 只包含单个或少量操作的简单流程
"""
import logging
from .base_flow import BaseFlow
import utils

logger = logging.getLogger(__name__)


class SimpleQueryFlow(BaseFlow):
    """简单查询流程 - 只执行查票操作"""
    
    def execute(self, start: str | None = None, end: str | None = None, 
                date: str | None = None) -> dict[str, object]:
        """
        执行简单查询流程
        
        Args:
            start: 起点站名称（可选，如果不提供则随机选择）
            end: 终点站名称（可选，如果不提供则随机选择，且不同于起点）
            date: 出发日期（可选，如果不提供则随机选择未来日期）
            
        Returns:
            查询结果
        """
        result = {
            "success": False,
            "data": None,
            "error": None
        }
        
        try:
            # 如果没有提供参数，则使用工具函数生成
            start = start or utils.get_random_start_station()
            end = end or utils.get_random_end_station(start)
            date = date or utils.get_random_travel_date()
            
            logger.info(f"查询车票: {start} -> {end}, 日期: {date}")
            
            query_result = self.travel.query_trips_left(start, end, date)
            
            if query_result:
                result["success"] = True
                result["data"] = query_result
            else:
                result["error"] = "未查询到符合条件的车次"
            
        except Exception as e:
            logger.error(f"查询失败: {str(e)}", exc_info=True)
            result["error"] = str(e)
        
        return result


class SimpleLoginFlow(BaseFlow):
    """简单登录流程 - 只执行登录操作"""
    
    def execute(self, username: str | None = None, password: str | None = None, 
                verification_code: str | None = None) -> dict[str, object]:
        """
        执行简单登录流程
        
        Args:
            username: 用户名（可选，如果不提供则随机选择）
            password: 密码（可选，如果不提供则随机选择，与用户名对应）
            verification_code: 验证码（可选）
            
        Returns:
            登录结果，包含token
        """
        result = {
            "success": False,
            "token": None,
            "error": None
        }
        
        try:
            # 如果没有提供用户名和密码，则使用工具函数生成
            if username is None or password is None:
                username, password = utils.get_random_user_credentials()
            
            logger.info(f"用户登录: {username}")
            token = self.auth.login(username, password, verification_code)
            
            if token:
                result["success"] = True
                result["token"] = token
                logger.info(f"登录成功，获取到token")
            else:
                result["error"] = "登录失败，未获取到token"
                
        except Exception as e:
            logger.error(f"登录失败: {str(e)}", exc_info=True)
            result["error"] = str(e)
        
        return result

