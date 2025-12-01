"""
简单Flow - 只包含单个或少量操作的简单流程
"""
import logging
import random
from .base_flow import BaseFlow
import utils
import config

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


class SimpleRegisterFlow(BaseFlow):
    """简单注册流程 - 先登录获取token，然后注册新用户"""
    
    def execute(self, user_name: str | None = None, password: str | None = None,
                gender: int | None = None, document_type: int | None = None,
                document_num: str | None = None, email: str | None = None) -> dict[str, object]:
        """
        执行简单注册流程
        
        Args:
            user_name: 要注册的用户名（可选，如果不提供则随机生成）
            password: 要注册的密码（可选，如果不提供则使用默认密码"111111"）
            gender: 性别（可选，如果不提供则随机选择，1表示男性，0表示女性）
            document_type: 证件类型（可选，如果不提供则默认为1表示身份证）
            document_num: 证件号码（可选，如果不提供则随机生成）
            email: 邮箱地址（可选，如果不提供则随机生成）
            
        Returns:
            注册结果，包含注册的用户信息
        """
        result = {
            "success": False,
            "user_id": None,
            "user_name": None,
            "error": None
        }
        
        try:
            # 第一步：使用管理员账号登录获取token（从config中读取）
            logger.info(f"管理员登录: {config.ADMIN_USERNAME}")
            token = self.auth.login(config.ADMIN_USERNAME, config.ADMIN_PASSWORD)
            
            if not token:
                result["error"] = "管理员登录失败，无法获取token"
                logger.error(result["error"])
                return result
            
            logger.info("管理员登录成功，获取到token")
            
            # 第二步：生成或使用提供的注册数据
            if user_name is None or password is None:
                # 使用工具函数生成完整的注册数据
                register_data = utils.generate_register_data(user_name, password)
                user_name = str(register_data.get("user_name", ""))
                password = str(register_data.get("password", ""))
                if gender is None:
                    gender_val = register_data.get("gender", 1)
                    gender = int(gender_val) if isinstance(gender_val, (int, str)) else 1
                if document_type is None:
                    doc_type_val = register_data.get("document_type", 1)
                    document_type = int(doc_type_val) if isinstance(doc_type_val, (int, str)) else 1
                if document_num is None:
                    document_num = str(register_data.get("document_num", ""))
                if email is None:
                    email = str(register_data.get("email", ""))
            else:
                # 如果提供了用户名和密码，但其他字段未提供，则生成
                if gender is None:
                    gender = random.choice([0, 1])
                if document_type is None:
                    document_type = 1
                if document_num is None:
                    document_num = utils.generate_random_id_number()
                if email is None:
                    email = utils.generate_random_email(user_name)
            
            # 确保所有必需字段都有值
            assert user_name is not None, "user_name不能为None"
            assert password is not None, "password不能为None"
            assert gender is not None, "gender不能为None"
            assert document_type is not None, "document_type不能为None"
            assert document_num is not None, "document_num不能为None"
            assert email is not None, "email不能为None"
            
            logger.info(f"注册新用户: {user_name}, 邮箱: {email}")
            
            # 第三步：调用注册接口
            register_result = self.auth.register(
                user_name=user_name,
                password=password,
                gender=gender,
                document_type=document_type,
                document_num=document_num,
                email=email,
                token=token
            )
            
            # 检查注册结果
            if isinstance(register_result, dict):
                if register_result.get("status") == 1:
                    # 注册成功
                    data = register_result.get("data", {})
                    if isinstance(data, dict):
                        result["success"] = True
                        result["user_id"] = data.get("userId")
                        result["user_name"] = data.get("userName")
                        logger.info(f"注册成功！用户ID: {result['user_id']}, 用户名: {result['user_name']}")
                    else:
                        result["error"] = "注册响应数据格式错误"
                else:
                    # 注册失败
                    result["error"] = register_result.get("msg", "注册失败")
                    logger.error(f"注册失败: {result['error']}")
            else:
                result["error"] = "注册响应格式错误"
                logger.error(result["error"])
                
        except Exception as e:
            logger.error(f"注册流程失败: {str(e)}", exc_info=True)
            result["error"] = str(e)
        
        return result

