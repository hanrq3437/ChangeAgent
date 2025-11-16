"""
认证相关Action - 处理用户登录、注册等认证操作
"""
from .base_action import BaseAction


class AuthAction(BaseAction):
    """认证相关的API操作"""
    
    def login(self, username: str, password: str, verification_code: str | None = None) -> str:
        """
        用户登录
        
        Args:
            username: 用户名
            password: 密码
            verification_code: 验证码（可选）
            
        Returns:
            token字符串，如果登录失败则返回空字符串
            格式: "token"
            失败时: 空字符串
        """
        data = {
            "username": username,
            "password": password
        }
        if verification_code:
            data["verificationCode"] = verification_code
        
        result = self._post("/api/v1/users/login", data)
        # 登录接口返回格式: {"status": 1, "msg": "login success", "data": {"userId": "...", "username": "...", "token": "..."}}
        if isinstance(result, dict):
            # 检查status是否为1（成功）
            if result.get("status") == 1:
                data_obj = result.get("data")
                if isinstance(data_obj, dict):
                    token = data_obj.get("token")
                    if token:
                        return str(token)
        return ""
    
    def get_all_users(self) -> list[dict[str, object]]:
        """
        获取所有用户
        
        Returns:
            用户列表，如果失败则返回空列表
            格式: [{"userId": "...", "username": "...", ...}, ...]
        """
        response_json = self._get("/api/v1/users")
        
        # 获取用户列表接口返回格式: 直接返回列表 [{"id": "...", "username": "..."}, ...]
        # 或者错误时返回: {"status_code": 403, "message": "..."}
        if isinstance(response_json, list):
            return response_json
        return []

