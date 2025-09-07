from .base import *

@dataclass
class AvailableRentalServerEntity(Entity):
    """可用租赁服务器实体"""
    entity_id: str = ""  # 服务器唯一标识符
    name: str = ""  # 服务器名称（通常为数字ID）
    owner_id: int = 0  # 服务器所有者用户ID
    visibility: int = 0  # 服务器可见性 (0-公开, 1-私有)
    status: int = 0  # 服务器状态 (1-在线, 0-离线)
    icon_index: int = 0  # 服务器图标索引编号
    capacity: int = 0  # 服务器最大玩家容量
    mc_version: str = ""  # 支持的Minecraft版本
    player_count: int = 0  # 当前在线玩家数量
    like_num: int = 0  # 服务器点赞数
    server_type: str = ""  # 服务器类型 (如"docker_new")
    offset: int | None = None # 在列表中的位置偏移量
    has_pwd: str = "0"  # 是否有密码保护 ("0"-无密码, "1"-有密码)
    image_url: str = ""  # 服务器图片URL
    world_id: str = ""  # 世界ID标识
    min_level: int = 0  # 加入服务器所需最低等级
    pvp: bool = True  # 是否开启PVP
    server_name: str = ""  # 服务器显示名称

@dataclass
class GetAvailableRentalServersResponse(EntitiesResponse):
    """获取可用租赁服务器响应"""
    entities: List[AvailableRentalServerEntity] = field(default_factory=list)  # 服务器实体列表
    total: str = "0"  # 服务器总数
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetAvailableRentalServersResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entities=[AvailableRentalServerEntity(**server) for server in data.get("entities", [])],
            total=data.get("total", "0")
        )

@dataclass
class RentalServerConnectionInfo(Entity):
    """租赁服务器连接信息实体"""
    entity_id: str = ""  # 服务器唯一标识符 (与租赁服务器列表中的一致)
    mcserver_host: str = ""  # 服务器主机地址 (IP地址或域名)
    mcserver_port: int = 0  # 服务器端口号
    isp_enable: bool = True  # ISP是否启用 (通常为True)
    state: int = 0  # 服务器连接状态 (1-正常)
    async_progress: int = 0  # 异步加载进度 (0-100)
    total_progress: int = 0  # 总加载进度 (0-100)

@dataclass
class EnterRentalServerWorldResponse(EntityResponse):
    """进入租赁服务器世界响应"""
    entity: RentalServerConnectionInfo = field(default_factory=RentalServerConnectionInfo)  # 服务器连接信息实体
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EnterRentalServerWorldResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=RentalServerConnectionInfo(**data.get("entity", {}))
        )

@dataclass
class RentalServerLikeStatus(Entity):
    """租赁服务器点赞状态实体"""
    entity_id: str = ""  # 服务器唯一标识符
    is_like: int = 0  # 点赞状态 (0-未点赞, 1-已点赞)

@dataclass
class UpdateRentalServerLikeResponse(EntityResponse):
    """更新租赁服务器点赞状态响应"""
    entity: RentalServerLikeStatus = field(default_factory=RentalServerLikeStatus)  # 点赞状态实体
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UpdateRentalServerLikeResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=RentalServerLikeStatus(**data.get("entity", {}))
        )

@dataclass
class RentalServerPlayerPEGrowth(Entity):
    """租赁服务器玩家PE成长信息"""
    exp: int = 0  # 当前经验值
    lv: int = 0  # 当前等级
    decorate: List[Any] = field(default_factory=list)  # 装饰信息列表
    msg_background_id: int = 0  # 消息背景ID
    chat_bubble_id: int = 0  # 聊天气泡ID
    is_vip: bool = False  # 是否为VIP
    is_vip_expr: bool = False  # VIP是否过期
    need_exp: int = 0  # 升级所需经验值

@dataclass
class RentalServerPlayerEntity(Entity):
    """租赁服务器玩家实体"""
    entity_id: str = ""  # 玩家实体ID
    server_id: str = ""  # 服务器ID
    user_id: str = ""  # 用户ID
    name: str = ""  # 玩家名称
    status: int = 0  # 玩家状态 (0-正常)
    create_ts: int = 0  # 创建时间戳
    delete_ts: int = 0  # 删除时间戳 (0-未删除)
    headImage: str = ""  # 玩家头像URL
    frame_id: str = ""  # 头像框URL
    pe_growth: RentalServerPlayerPEGrowth = field(default_factory=RentalServerPlayerPEGrowth)  # PE成长信息
    is_online: bool = False  # 是否在线
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RentalServerPlayerEntity":
        """自定义反序列化方法，处理嵌套实体"""
        pe_growth_data = data.get("pe_growth", {})
        return cls(
            entity_id=data.get("entity_id", ""),
            server_id=data.get("server_id", ""),
            user_id=data.get("user_id", ""),
            name=data.get("name", ""),
            status=data.get("status", 0),
            create_ts=data.get("create_ts", 0),
            delete_ts=data.get("delete_ts", 0),
            headImage=data.get("headImage", ""),
            frame_id=data.get("frame_id", ""),
            pe_growth=RentalServerPlayerPEGrowth(**pe_growth_data),
            is_online=data.get("is_online", False)
        )

@dataclass
class GetRentalServerPlayersResponse(EntitiesResponse):
    """获取租赁服务器玩家列表响应"""
    entities: List[RentalServerPlayerEntity] = field(default_factory=list)  # 玩家实体列表
    total: str = "0"  # 玩家总数
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetRentalServerPlayersResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entities=[RentalServerPlayerEntity.from_dict(e) for e in data.get("entities", [])],
            total=data.get("total", "0")
        )

@dataclass
class RentalServerDetailsEntity(Entity):
    """租赁服务器详细信息实体"""
    entity_id: str = ""  # 服务器唯一标识符
    world_id: str = ""  # 世界ID标识
    owner_id: str = ""  # 服务器所有者用户ID
    name: str = ""  # 服务器名称（通常为数字ID）
    brief_summary: str = ""  # 服务器简介
    icon_index: int = 0  # 服务器图标索引编号
    begin_time: int = 0  # 服务器创建时间戳
    mc_version: str = ""  # 支持的Minecraft版本
    capacity: int = 0  # 服务器最大玩家容量
    active_components: List[Any] = field(default_factory=list)  # 活跃组件列表
    update_active_components: List[Any] = field(default_factory=list)  # 待更新的活跃组件列表
    status: int = 0  # 服务器状态 (1-在线, 0-离线)
    visibility: int = 0  # 服务器可见性 (0-公开, 1-私有)
    player_count: int = 0  # 当前在线玩家数量
    like_num: int = 0  # 服务器点赞数
    server_type: str = ""  # 服务器类型 (如"docker_new")
    has_pwd: str = "0"  # 是否有密码保护 ("0"-无密码, "1"-有密码)
    image_url: str = ""  # 服务器图片URL
    min_level: int = 0  # 加入服务器所需最低等级
    server_name: str = ""  # 服务器显示名称
    pvp: bool = True  # 是否开启PVP

@dataclass
class GetRentalServerDetailsResponse(EntityResponse):
    """获取租赁服务器详细信息响应"""
    entity: RentalServerDetailsEntity = field(default_factory=RentalServerDetailsEntity)  # 服务器详情实体
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetRentalServerDetailsResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=RentalServerDetailsEntity(**data.get("entity", {}))
        )


@dataclass
class SearchRentalServerByNameResponse(EntitiesResponse):
    """搜索租赁服务器响应"""
    entities: List[AvailableRentalServerEntity] = field(default_factory=list)  # 服务器实体列表
    total: str = "0"  # 服务器总数
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchRentalServerResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entities=[AvailableRentalServerEntity(**server) for server in data.get("entities", [])],
            total=data.get("total", "0")
        )
