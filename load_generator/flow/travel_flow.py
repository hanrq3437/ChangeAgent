"""
旅行订票Flow - 从查票到订票的完整流程
"""
import logging
import random
from .base_flow import BaseFlow
import utils

logger = logging.getLogger(__name__)


class BookingFlow(BaseFlow):
    """订票流程 - 查票 -> 登录 -> 获取联系人 -> 订票"""
    
    def execute(
        self,
        start: str | None = None,
        end: str | None = None,
        date: str | None = None,
        username: str | None = None,
        password: str | None = None,
        seat_type: str | None = None,  # "1"表示舒适座，"2"表示经济座，None表示随机选择
        assurance: str | None = None,  # "0"表示不购买保险，None表示随机选择
        food_type: int | None = None  # 0表示不订购食物，None表示随机选择
    ) -> dict[str, object]:
        """
        执行订票流程
        
        Args:
            start: 起点站名称（可选，如果不提供则随机选择）
            end: 终点站名称（可选，如果不提供则随机选择，且不同于起点）
            date: 出发日期（可选，如果不提供则随机选择未来日期）
            username: 用户名（可选，如果不提供则随机选择）
            password: 密码（可选，如果不提供则随机选择，与用户名对应）
            seat_type: 座位类型，"1"表示舒适座，"2"表示经济座，None表示随机选择
            assurance: 保险类型索引，"0"表示不购买保险，None表示随机选择
            food_type: 食物类型，0表示不订购食物，None表示随机选择
            
        Returns:
            订票结果，包含订单信息
        """
        result = {
            "success": False,
            "order_id": None,
            "trip_id": None,
            "error": None
        }
        
        try:
            # 第一步：如果没有提供参数，则使用工具函数生成
            # 使用基于路线配置的函数确保路线存在
            if start is None:
                start = utils.get_random_start_station()
            
            if end is None:
                # 根据config中的路线信息选择终点站，确保路线存在
                end = utils.get_random_end_station_by_route(start)
                if end is None:
                    # 如果找不到存在的路线，尝试随机选择其他起点站
                    max_attempts = 10
                    for _ in range(max_attempts):
                        start = utils.get_random_start_station()
                        end = utils.get_random_end_station_by_route(start)
                        if end is not None:
                            break
                    if end is None:
                        result["error"] = "无法找到存在的路线"
                        logger.error(result["error"])
                        return result
            
            date = date or utils.get_random_travel_date()
            
            logger.info(f"开始订票流程: {start} -> {end}, 日期: {date}")
            
            # 第二步：同时查询高铁/动车和普通火车车票
            logger.info("步骤1: 查询车票（同时查询高铁/动车和普通火车）")
            
            # 同时查询两种类型的车次
            trips_high_speed = self.travel.query_trips_left(start, end, date)
            trips_normal = self.travel.query_trips_left_normal(start, end, date)
            
            # 合并结果
            trips = []
            if isinstance(trips_high_speed, list):
                trips.extend(trips_high_speed)
            if isinstance(trips_normal, list):
                trips.extend(trips_normal)
            
            if not trips:
                result["error"] = "未查询到符合条件的车次"
                logger.warning(result["error"])
                return result
            
            logger.info(f"查询到的车次数量: {len(trips)}")
            
            # 第三步：随机选择一个车次
            trip_id_str = utils.select_random_trip(trips)
            if not trip_id_str:
                result["error"] = "选择车次失败"
                logger.warning(result["error"])
                return result
            
            # 判断是否是高铁/动车：G或D开头
            is_high_speed = trip_id_str.startswith("G") or trip_id_str.startswith("D")
            
            logger.info(f"选择车次: {trip_id_str} ({'高铁/动车' if is_high_speed else '普通火车'})")
            
            # 第四步：登录获取token和用户ID
            logger.info("步骤2: 用户登录")
            if username is None or password is None:
                username, password = utils.get_random_user_credentials()
            
            # 登录并获取完整响应（需要修改login方法或直接调用_post）
            login_data = {
                "username": username,
                "password": password
            }
            login_result = self.auth._post("/api/v1/users/login", login_data)
            
            if not isinstance(login_result, dict) or login_result.get("status") != 1:
                result["error"] = "登录失败"
                logger.error(result["error"])
                return result
            
            login_data_obj = login_result.get("data", {})
            if not isinstance(login_data_obj, dict):
                result["error"] = "登录响应数据格式错误"
                logger.error(result["error"])
                return result
            
            token = login_data_obj.get("token")
            account_id = login_data_obj.get("userId")
            
            if not token or not account_id:
                result["error"] = "登录成功但无法获取token或用户ID"
                logger.error(result["error"])
                return result
            
            logger.info(f"登录成功，用户ID: {account_id}")
            
            # 第五步：查询保险类型并随机选择
            logger.info("步骤3: 查询保险类型")
            assurance_types = self.travel.get_assurance_types(token)
            
            # 随机决定要不要保险，如果要的话随机选择一个
            if assurance is None:
                if assurance_types and random.random() < 0.5:  # 50%概率购买保险
                    selected_assurance = random.choice(assurance_types)
                    assurance = str(selected_assurance.get("index", "0"))
                    logger.info(f"随机选择保险: {selected_assurance.get('name', 'Unknown')} (索引: {assurance})")
                else:
                    assurance = "0"
                    logger.info("随机决定不购买保险")
            else:
                logger.info(f"使用指定保险: {assurance}")
            
            # 第六步：获取联系人
            logger.info("步骤4: 获取联系人")
            contacts = self.contact.get_contacts_by_account(account_id, token)
            
            if not contacts:
                result["error"] = "用户没有联系人信息，无法订票"
                logger.warning(result["error"])
                return result
            
            # 随机选择一个联系人
            selected_contact = random.choice(contacts)
            contact_id = selected_contact.get("id")
            if not contact_id:
                result["error"] = "联系人ID无效"
                logger.error(result["error"])
                return result
            
            # 确保contact_id是字符串类型
            contact_id = str(contact_id)
            
            logger.info(f"选择联系人: {selected_contact.get('name', 'Unknown')}")
            
            # 第七步：随机选择座位类型
            if seat_type is None:
                seat_type = random.choice(["1", "2"])  # "1"表示舒适座，"2"表示经济座
                logger.info(f"随机选择座位类型: {'舒适座' if seat_type == '1' else '经济座'}")
            else:
                logger.info(f"使用指定座位类型: {'舒适座' if seat_type == '1' else '经济座'}")
            
            # 第八步：查询食物信息并随机选择
            logger.info("步骤5: 查询食物信息")
            foods_data = self.travel.get_all_foods(date, start, end, trip_id_str)
            
            # 随机决定要不要食物，如果要的话随机选择一个
            selected_food_type = 0
            food_name = None
            food_price = None
            station_name = None
            store_name = None
            
            if food_type is None:
                if foods_data and random.random() < 0.4:  # 40%概率订购食物
                    # 优先从 trainFoodList 中选择
                    train_food_list = foods_data.get("trainFoodList", [])
                    if train_food_list and isinstance(train_food_list, list):
                        selected_food = random.choice(train_food_list)
                        if isinstance(selected_food, dict):
                            selected_food_type = selected_food.get("foodType", 1)  # 默认使用foodType
                            food_name = selected_food.get("foodName")
                            food_price = selected_food.get("price")
                            logger.info(f"随机选择食物: {food_name} (类型: {selected_food_type}, 价格: {food_price})")
                    else:
                        # 如果没有trainFoodList，尝试从foodStoreListMap中选择
                        food_store_map = foods_data.get("foodStoreListMap", {})
                        if food_store_map and isinstance(food_store_map, dict):
                            # 随机选择一个站点
                            stations = list(food_store_map.keys())
                            if stations:
                                station_name = random.choice(stations)
                                stores = food_store_map.get(station_name, {})
                                if stores and isinstance(stores, dict):
                                    # 随机选择一个商店
                                    store_names = list(stores.keys())
                                    if store_names:
                                        store_name = random.choice(store_names)
                                        store_foods = stores.get(store_name, [])
                                        if store_foods and isinstance(store_foods, list):
                                            selected_food = random.choice(store_foods)
                                            if isinstance(selected_food, dict):
                                                selected_food_type = selected_food.get("foodType", 1)
                                                food_name = selected_food.get("foodName")
                                                food_price = selected_food.get("price")
                                                logger.info(f"随机选择食物: {food_name} (类型: {selected_food_type}, 价格: {food_price}, 站点: {station_name}, 商店: {store_name})")
                    if selected_food_type == 0:
                        logger.info("查询到食物但无法选择，不订购食物")
                else:
                    logger.info("随机决定不订购食物")
            else:
                selected_food_type = food_type if food_type is not None else 0
                logger.info(f"使用指定食物类型: {selected_food_type}")
            
            # 第九步：根据车次类型订票
            logger.info("步骤6: 预订车票")
            
            if is_high_speed:
                logger.info(f"预订高铁/动车车票: {trip_id_str}")
                preserve_result = self.travel.preserve_ticket(
                    account_id=account_id,
                    contacts_id=contact_id,
                    trip_id=trip_id_str,
                    seat_type=seat_type,
                    date=date,
                    from_station=start,
                    to_station=end,
                    assurance=assurance,
                    token=token,
                    food_type=selected_food_type,
                    food_name=food_name,
                    food_price=food_price,
                    station_name=station_name,
                    store_name=store_name
                )
            else:
                logger.info(f"预订普通火车车票: {trip_id_str}")
                preserve_result = self.travel.preserve_other_ticket(
                    account_id=account_id,
                    contacts_id=contact_id,
                    trip_id=trip_id_str,
                    seat_type=seat_type,
                    date=date,
                    from_station=start,
                    to_station=end,
                    assurance=assurance,
                    token=token,
                    food_type=selected_food_type,
                    food_name=food_name,
                    food_price=food_price,
                    station_name=station_name,
                    store_name=store_name
                )
            
            # 检查订票结果
            if isinstance(preserve_result, dict):
                if preserve_result.get("status") == 1:
                    result["success"] = True
                    result["trip_id"] = trip_id_str
                    # 订票成功，但响应中可能没有order_id，需要从订单服务查询
                    logger.info("订票成功！")
                else:
                    result["error"] = preserve_result.get("msg", "订票失败")
                    logger.error(f"订票失败: {result['error']}")
            else:
                result["error"] = "订票响应格式错误"
                logger.error(result["error"])
                
        except Exception as e:
            logger.error(f"订票流程失败: {str(e)}", exc_info=True)
            result["error"] = str(e)
        
        return result

