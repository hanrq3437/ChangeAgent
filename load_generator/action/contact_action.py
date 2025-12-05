"""
联系人相关Action - 处理联系人信息管理操作
"""
from .base_action import BaseAction


class ContactAction(BaseAction):
    """联系人相关的API操作"""
    
    def get_contacts_by_account(self, account_id: str, token: str) -> list[dict[str, object]]:
        """
        根据账户ID获取所有联系人
        
        Args:
            account_id: 账户ID（UUID格式）
            token: 认证token（需要先通过login方法获取）
            
        Returns:
            联系人列表，如果失败则返回空列表
            格式: [{"id": "...", "accountId": "...", "name": "...", "documentType": 1, "documentNumber": "...", "phoneNumber": "..."}, ...]
        """
        headers = {"Authorization": f"Bearer {token}"}
        
        result = self._get(f"/api/v1/contactservice/contacts/account/{account_id}", headers=headers)
        # 接口返回格式: {"status": 1, "msg": "Success", "data": [...]}
        if isinstance(result, dict):
            # 检查status是否为1（成功）
            if result.get("status") == 1:
                data_list = result.get("data")
                if isinstance(data_list, list):
                    return data_list
        elif isinstance(result, list):
            # 如果直接返回列表（虽然不太可能，但为了兼容性）
            return result
        return []

