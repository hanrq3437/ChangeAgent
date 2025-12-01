"""
工具函数模块 - 提供数据生成、随机选择等工具函数
"""
import random
from datetime import datetime, timedelta
import config


def get_random_station(exclude: list[str] = []) -> str:
    """
    随机选择一个车站
    
    Args:
        exclude: 要排除的车站列表（例如，选择终点时排除起点）
    
    Returns:
        随机选择的车站名称
    """
    available_stations = [s for s in config.DEFAULT_STATIONS if s not in exclude]
    if not available_stations:
        # 如果没有可用车站，返回第一个车站
        return config.DEFAULT_STATIONS[0]
    return random.choice(available_stations)


def get_random_start_station() -> str:
    """
    随机选择一个起点站
    
    Returns:
        随机选择的起点站名称
    """
    return get_random_station()


def get_random_end_station(start_station: str | None = None) -> str:
    """
    随机选择一个终点站（排除起点站）
    
    Args:
        start_station: 起点站名称，如果提供则排除它
    
    Returns:
        随机选择的终点站名称
    """
    exclude = [start_station] if start_station else []
    return get_random_station(exclude)


def get_future_date(days_ahead: int | None = None, max_days: int = 30) -> str:
    """
    生成一个未来的日期字符串
    
    Args:
        days_ahead: 指定多少天后（如果为None则随机选择）
        max_days: 最大天数（当days_ahead为None时使用）
    
    Returns:
        日期字符串，格式：YYYY-MM-DD
    """
    if days_ahead is None:
        days_ahead = random.randint(1, max_days)
    
    future_date = datetime.now() + timedelta(days=days_ahead)
    return future_date.strftime("%Y-%m-%d")


def get_random_travel_date() -> str:
    """
    随机选择一个旅行日期（从配置的日期列表中选择，或生成未来日期）
    
    Returns:
        日期字符串，格式：YYYY-MM-DD
    """
    if config.DEFAULT_TRAVEL_DATES:
        return random.choice(config.DEFAULT_TRAVEL_DATES)
    # 如果没有配置日期，生成一个未来7-30天的随机日期
    return get_future_date(max_days=30)


def get_random_user() -> dict[str, str]:
    """
    随机选择一个用户凭据
    
    Returns:
        包含username和password的字典
    """
    if not config.DEFAULT_USERS:
        # 如果没有配置用户，返回默认值
        return {"username": "fdse_microservices", "password": "111111"}
    return random.choice(config.DEFAULT_USERS)


def get_random_user_credentials() -> tuple[str, str]:
    """
    随机获取一对用户名和密码
    
    Returns:
        (username, password) 元组
    """
    user = get_random_user()
    return user["username"], user["password"]


def generate_random_id_number() -> str:
    """
    生成一个随机的18位身份证号码
    
    Returns:
        18位身份证号码字符串
    """
    # 生成前17位（地区码+出生日期+顺序码）
    area_code = random.choice(["110", "120", "130", "140", "150", "210", "220", "230", "310", "320", "330", "340", "350"])
    birth_date = f"{random.randint(1970, 2000)}{random.randint(1, 12):02d}{random.randint(1, 28):02d}"
    sequence = f"{random.randint(100, 999)}"
    first_17 = area_code + birth_date + sequence
    
    # 计算校验码（简化版，使用随机数）
    check_code = random.choice(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "X"])
    
    return first_17 + check_code


def generate_random_email(username: str | None = None) -> str:
    """
    生成一个随机邮箱地址
    
    Args:
        username: 用户名（可选，如果不提供则随机生成）
    
    Returns:
        邮箱地址字符串
    """
    if username is None:
        username = f"user{random.randint(100000, 999999)}"
    
    domains = ["gmail.com", "qq.com", "163.com", "sina.com", "outlook.com", "test.com"]
    domain = random.choice(domains)
    
    return f"{username}@{domain}"


def generate_random_username(prefix: str = "test") -> str:
    """
    生成一个随机用户名
    
    Args:
        prefix: 用户名前缀
    
    Returns:
        用户名字符串
    """
    suffix = random.randint(100000, 999999)
    return f"{prefix}{suffix}"


def generate_register_data(user_name: str | None = None, password: str | None = None) -> dict[str, object]:
    """
    生成注册所需的数据
    
    Args:
        user_name: 用户名（可选，如果不提供则随机生成）
        password: 密码（可选，如果不提供则使用默认密码）
    
    Returns:
        包含注册所需所有字段的字典
    """
    user_name = user_name or generate_random_username()
    password = password or "111111"
    gender = random.choice([0, 1])  # 0表示女性，1表示男性
    document_type = 1  # 1表示身份证
    document_num = generate_random_id_number()
    email = generate_random_email(user_name)
    
    return {
        "user_name": user_name,
        "password": password,
        "gender": gender,
        "document_type": document_type,
        "document_num": document_num,
        "email": email
    }

