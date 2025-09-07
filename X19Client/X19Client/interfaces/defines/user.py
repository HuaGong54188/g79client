from .base import *

@dataclass
class PEGrowth(Entity):
    """PE成长信息"""
    lv: int = 0  # 当前等级
    exp: int = 0  # 当前经验值
    need_exp: int = 0  # 升级所需经验值
    decorate: List[Any] = field(default_factory=list)  # 装饰信息列表
    is_vip: int = 0  # VIP状态 (0-非VIP, 1-VIP)

@dataclass
class UserGameInfo(Entity):
    """用户游戏信息"""
    game_type: bool = False  # 游戏类型标识
    game_id: bool = False  # 游戏ID标识
    game_info: bool = False  # 游戏信息标识

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserGameInfo":
        """自定义反序列化方法，处理特殊字段名"""
        return cls(
            game_type=data.get("game-type", False),
            game_id=data.get("game-id", False),
            game_info=data.get("game-info", False),
        )

    def to_dict(self) -> Dict[str, Any]:
        """自定义序列化方法，处理特殊字段名"""
        return {
            "game-type": self.game_type,
            "game-id": self.game_id,
            "game-info": self.game_info
        }

@dataclass
class StatisDataItem(Entity):
    """统计数据项"""
    type: int = -1  # 数据类型标识
    value: int = 0  # 数据值
    visible: int = 1  # 是否可见 (0-不可见, 1-可见)

@dataclass
class SearchPEGrowth(Entity):
    """搜索PE成长信息"""
    exp: int = 0  # 当前经验值
    lv: int = 0  # 当前等级
    decorate: List[Any] = field(default_factory=list)  # 装饰信息列表
    msg_background_id: int = 0  # 消息背景ID
    chat_bubble_id: int = 0 # 聊天气泡ID
    is_vip: bool = False  # VIP状态 
    is_vip_expr: bool = False  # VIP体验卡状态 
    need_exp: int = 0  # 升级所需经验值

@dataclass
class SearchUserEntity(Entity):
    """用户搜索信息实体"""
    uid: int = 0  # 用户ID
    nickname: str = ""  # 用户昵称
    headImage: str = ""  # 用户头像URL
    frame_id: str = ""  # 头像框ID
    moment_id: str = ""  # 动态ID
    public_flag: bool = False  # 是否公开个人主页
    online_status: str = ""  # 在线状态
    online_pcpe: int = 0  # PC/PE在线标识
    online_type: int = 0  # 在线类型
    game_info: list = field(default_factory=list)  # 游戏信息列表
    tLogout: int = 0  # 最后登出时间戳
    pe_growth: SearchPEGrowth = field(default_factory=SearchPEGrowth)  # PE成长信息
    recharge_vip_info: Dict[str, Any] = field(default_factory=dict)  # VIP充值信息
    recharge_vip_level: int = 0  # VIP等级

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchUserEntity":
        """自定义反序列化方法，处理嵌套实体"""
        data["pe_growth"] = SearchPEGrowth.from_dict(data.get("pe_growth", {}))
        return cls(
            **data
        )

@dataclass
class SearchUserByNameOrMailResponse(EntitiesResponse):
    """搜索用户响应"""
    entities: List[SearchUserEntity] = field(default_factory=list)  # 用户实体列表
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchUserByNameOrMailResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entities=[SearchUserEntity.from_dict(e) for e in data.get("entities", [])]
        )

@dataclass
class UserDetailEntity(Entity):
    """用户详细信息实体"""
    id: int = 0  # 用户ID
    nickname: str = ""  # 用户昵称
    signature: str = ""  # 个性签名
    headImage: str = ""  # 用户头像URL
    frame_id: str = ""  # 头像框ID
    moment_id: str = ""  # 动态ID
    public_flag: bool = False  # 是否公开个人主页
    pe_growth: PEGrowth = field(default_factory=PEGrowth)  # PE成长信息
    user_game_info: UserGameInfo = field(default_factory=UserGameInfo)  # 用户游戏信息
    friend_recommend: int = 0  # 好友推荐数
    friend_apply: int = 0  # 好友申请数
    tag: List[Any] = field(default_factory=list)  # 用户标签列表
    is_developer: bool = False  # 是否为开发者
    mark: str = ""  # 用户备注
    is_friend: bool = False  # 是否为好友
    today_liked: List[Any] = field(default_factory=list)  # 今日点赞列表
    statis_data: List[StatisDataItem] = field(default_factory=list)  # 统计数据列表
    homepage_bg: int = 0  # 主页背景ID
    visit_card_bg: int = 0  # 访客卡片背景ID
    city_no: int = 0  # 城市编号
    recharge_vip_level: int = 0  # VIP等级
    recharge_vip_info: Dict[str, Any] = field(default_factory=dict)  # VIP充值信息

    lbs_info: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserDetailEntity":
        """自定义反序列化方法，处理嵌套实体"""
        new_data = {}
        for k, v in data.items():
            if k not in ["pe_growth", "user_game_info", "statis_data"]:
                new_data[k] = v
    
        return cls(
            **new_data,
            pe_growth=PEGrowth.from_dict(data.get("pe_growth", {})),
            user_game_info=UserGameInfo.from_dict(data.get("user_game_info", {})),
            statis_data=[StatisDataItem(**item) for item in data.get("statis_data", [])]
        )

@dataclass
class QueryUserByEntityIdResponse(SummaryMD5EntityResponse):
    """查询用户信息响应"""
    entity: UserDetailEntity = field(default_factory=UserDetailEntity)  # 用户详细信息实体
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QueryUserByEntityIdResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            summary_md5=data.get("summary_md5", ""),
            entity=UserDetailEntity.from_dict((data.get("entity", {}) or {}))
        )

@dataclass
class LikeStatusEntity(Entity):
    """点赞状态实体"""
    entity_id: str = ""  # 实体ID (点赞对象ID)
    visitor_user_id: str = ""  # 访客用户ID
    personal_page_owner_user_id: str = ""  # 个人主页所有者用户ID
    has_like: bool = False  # 是否已点赞

@dataclass
class UpdatePersonalPageLikeResponse(EntityResponse):
    """更新个人主页点赞状态响应"""
    entity: LikeStatusEntity = field(default_factory=LikeStatusEntity)  # 点赞状态实体
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UpdatePersonalPageLikeResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=LikeStatusEntity(**(data.get("entity", {}) or {}))
        )

@dataclass
class UserModDetailEntity(Entity):
    """用户模组详情实体"""
    is_visible: int = 1  # 是否可见 (1-可见, 0-不可见)
    mod_counts: Dict[str, int] = field(default_factory=dict)  # 模组数量统计 (模组ID: 数量)

@dataclass
class GetUserModDetailResponse(EntityResponse):
    """获取用户模组详情响应"""
    entity: UserModDetailEntity = field(default_factory=UserModDetailEntity)  # 模组详情实体
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetUserModDetailResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=UserModDetailEntity(
                is_visible=(data.get("entity", {}) or {}).get("is_visible", 1),
                mod_counts=(data.get("entity", {}) or {}).get("mod_counts", {})
            )
        )

@dataclass
class UserModUsageTimeEntity(Entity):
    """用户模组使用时间实体"""
    mod_use_time: Dict[str, int] = field(default_factory=dict)  # 模组总使用时间 (模组ID: 秒数)
    mod_recently_use_time: Dict[str, int] = field(default_factory=dict)  # 模组最近使用时间 (模组ID: 秒数)

@dataclass
class GetUserModUsageTimeResponse(EntityResponse):
    """获取用户模组使用时间响应"""
    entity: UserModUsageTimeEntity = field(default_factory=UserModUsageTimeEntity)  # 模组使用时间实体
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetUserModUsageTimeResponse":
        """反序列化方法"""
        entity_data = (data.get("entity", {}) or {})
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=UserModUsageTimeEntity(
                mod_use_time=entity_data.get("mod_use_time", {}),
                mod_recently_use_time=entity_data.get("mod_recently_use_time", {})
            )
        )

@dataclass
class ApplyFriendRequestResponse(Response):
    """申请好友请求响应"""
    entity: str = ""  # 操作结果消息 (如"操作成功")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApplyFriendRequestResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=(data.get("entity", "") or "")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """序列化方法"""
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
            "entity": self.entity
        }

@dataclass
class ReportMessageContent(Entity):
    """举报消息内容实体"""
    type: str = ""  # 举报类型
    message: str = ""  # 消息内容
    nickName: str = ""  # 被举报用户昵称
    uid: int = 0  # 被举报用户ID
    detail: str = ""  # 详细信息
    re_uid: int = 0  # 相关用户ID
    re_nickName: str = ""  # 相关用户昵称

@dataclass
class MomentReportEntity(Entity):
    """动态举报实体"""
    msg_id: ReportMessageContent = field(default_factory=ReportMessageContent)  # 举报消息内容
    type: str = ""  # 举报类型 (如"头像举报")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MomentReportEntity":
        """自定义反序列化方法，处理JSON字符串"""
        # 解析 msg_id 字符串为 ReportMessageContent 对象
        msg_id_str = data.get("msg_id", "{}")
        try:
            # 处理 Unicode 转义字符
            msg_id_str = bytes(msg_id_str, "utf-8").decode("unicode_escape")
            msg_id_data = json.loads(msg_id_str)
        except (json.JSONDecodeError, TypeError):
            msg_id_data = {}
        
        return cls(
            msg_id=ReportMessageContent(**msg_id_data),
            type=data.get("type", "")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """自定义序列化方法，将对象转为JSON字符串"""
        return {
            "msg_id": json.dumps(self.msg_id.to_dict(), separators=(',', ':')),
            "type": self.type
        }

@dataclass
class MomentReportRequestResponse(EntityResponse):
    """动态举报响应"""
    entity: MomentReportEntity = field(default_factory=MomentReportEntity)  # 举报实体
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MomentReportRequestResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=MomentReportEntity.from_dict(data.get("entity", {}))
        )

@dataclass
class LikeUserTagEntity(Entity):
    """用户标签点赞实体"""
    target_id: int = 0  # 目标ID (用户ID)
    tag_id: int = 0  # 标签ID

@dataclass
class LikeUserTagResponse(EntityResponse):
    """用户标签点赞响应"""
    entity: LikeUserTagEntity = field(default_factory=LikeUserTagEntity)  # 标签点赞实体
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LikeUserTagResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=LikeUserTagEntity(
                target_id=data.get("entity", {}).get("target_id", 0),
                tag_id=data.get("entity", {}).get("tag_id", 0)
            )
        )

@dataclass
class TagEntity(Entity):
    """标签实体"""
    tag_id: int = 0  # 标签ID
    tag_name: str = ""  # 标签名称
    likes: int = 0  # 点赞总数
    today_liked: int = 0  # 今日点赞数

@dataclass
class TagCategoryEntity(Entity):
    """标签分类实体"""
    category_id: int = 0  # 分类ID
    category_name: str = ""  # 分类名称
    tags: List[TagEntity] = field(default_factory=list)  # 标签列表
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TagCategoryEntity":
        """反序列化方法"""
        return cls(
            category_id=data.get("category_id", 0),
            category_name=data.get("category_name", ""),
            tags=[TagEntity(**tag) for tag in data.get("tags", [])]
        )

@dataclass
class GetUserTagListResponse(EntitiesResponse):
    """获取用户标签列表响应"""
    entities: List[TagCategoryEntity] = field(default_factory=list)  # 标签分类实体列表
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetUserTagListResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entities=[TagCategoryEntity.from_dict(e) for e in data.get("entities", [])]
        )

@dataclass
class UpdateHomePageConfigResponse(Response):
    """更新主页配置响应"""
    entity: None = None  # 实体数据 (固定为None)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UpdateHomePageConfigResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=None
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """序列化方法"""
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
            "entity": None
        }

@dataclass
class TagItem(Entity):
    """标签项实体 (用于主页配置)"""
    tag_id: int = 0  # 标签ID
    tag_name: str = ""  # 标签名称

@dataclass
class AppearanceReward(Entity):
    """外观奖励实体"""
    appear_platform: List[str] = field(default_factory=list)  # 适用平台列表 (如["pe", "pc"])
    bag_item_id: int = 0  # 背包物品ID
    id: int = 0  # 奖励ID
    jumpType: str = ""  # 跳转类型
    nb: int = 0  # 奖励数量
    rewardName: str = ""  # 奖励名称
    rewardRarity: int = 0  # 奖励稀有度
    tips: str = ""  # 提示信息
    tp: int = 0  # 类型标识
    url: str = ""  # 奖励图标URL

@dataclass
class AppearanceIIDItem(Entity):
    """外观IID项实体"""
    icon: str = ""  # 图标URL
    iid: str = ""  # IID标识
    name: str = ""  # 名称
    is_buy: bool = False  # 是否已购买

@dataclass
class AppearanceDetail(Entity):
    """外观详情实体"""
    background_url: str = ""  # 背景图片URL
    begin_time: str = ""  # 开始时间
    collect_num: int = 0  # 收集数量
    iid_list: List[AppearanceIIDItem] = field(default_factory=list)  # IID项列表
    name: str = ""  # 名称
    rewards: List[AppearanceReward] = field(default_factory=list)  # 奖励列表
    title_url: str = ""  # 标题图片URL
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppearanceDetail":
        """反序列化方法"""
        return cls(
            background_url=data.get("background_url", ""),
            begin_time=data.get("begin_time", ""),
            collect_num=data.get("collect_num", 0),
            iid_list=[AppearanceIIDItem(**item) for item in data.get("iid_list", [])],
            name=data.get("name", ""),
            rewards=[AppearanceReward(**reward) for reward in data.get("rewards", [])],
            title_url=data.get("title_url", "")
        )

@dataclass
class HomePageConfigEntity(Entity):
    """主页配置实体"""
    favorite_iid: str = ""  # 收藏的IID
    achievement_iid: str = ""  # 成就IID
    favorite_reason: str = ""  # 收藏理由
    tag: List[TagItem] = field(default_factory=list)  # 标签列表
    comment_permission: int = 0  # 评论权限 (0-不允许, 1-允许)
    appearance_id: int = 0  # 外观ID
    favorite_iid_name: str = ""  # 收藏IID名称
    achievement_iid_name: str = ""  # 成就IID名称
    appearance_detail: AppearanceDetail = field(default_factory=AppearanceDetail)  # 外观详情
    appearance_type: int = 0  # 外观类型
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HomePageConfigEntity":
        """反序列化方法"""
        return cls(
            favorite_iid=data.get("favorite_iid", ""),
            achievement_iid=data.get("achievement_iid", ""),
            favorite_reason=data.get("favorite_reason", ""),
            tag=[TagItem(**t) for t in data.get("tag", [])],
            comment_permission=data.get("comment_permission", 0),
            appearance_id=data.get("appearance_id", 0),
            favorite_iid_name=data.get("favorite_iid_name", ""),
            achievement_iid_name=data.get("achievement_iid_name", ""),
            appearance_detail=AppearanceDetail.from_dict(data.get("appearance_detail", {})),
            appearance_type=data.get("appearance_type", 0)
        )

@dataclass
class GetHomePageConfigResponse(EntityResponse):
    """获取主页配置响应"""
    entity: HomePageConfigEntity = field(default_factory=HomePageConfigEntity)  # 主页配置实体
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetHomePageConfigResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=HomePageConfigEntity.from_dict(data.get("entity", {}))
        )
