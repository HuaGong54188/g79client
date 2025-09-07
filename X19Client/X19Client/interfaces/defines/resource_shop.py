from .base import *

@dataclass
class RecommendItem(Entity):
    """推荐物品实体"""
    item_id: str = ""  # 物品ID
    first_type: int = 0  # 一级分类ID
    second_type: int = 0  # 二级分类ID
    pic_tag_state: int = 0  # 图片标签状态 (0-无特殊标记)
    res_name: str = ""  # 资源名称
    res_size: str = ""  # 资源大小 (字符串形式，单位字节)
    res_md5: str = ""  # 资源MD5校验值
    stars: float = 0.0  # 星级评分 (0-5分)
    download_num: str = "0"  # 总下载次数 (字符串形式)
    week_download_num: str = "0"  # 周下载次数 (字符串形式)
    points: int = 0  # 积分价格
    diamond: int = 0  # 钻石价格,
    res_version: int = 0  # 资源版本号
    is_item_time_limit: int = 0  # 是否限时物品 (0-非限时, 1-限时)
    item_remain_time: int = 0  # 物品剩余时间 (秒)
    buy_state: int = 0  # 购买状态 (0-未购买, 1-已购买)
    goods_state: int = 0  # 商品状态 (1-正常)
    status: int = 0  # 物品状态 (1-上架)
    skin_body_type: int = 0  # 皮肤体型类型 (0-默认)
    title_image_url: str = ""  # 标题图片URL
    title_image_version: int = 0  # 标题图片版本
    resource_packs_version: str = ""  # 资源包版本 (格式: "主,次,修订")
    behavior_packs_version: str = ""  # 行为包版本 (格式: "主,次,修订")
    lobby_tag: List[int] = field(default_factory=list)  # 大厅标签ID列表
    rel_iid: int = 0  # 相关物品ID
    is_competitive: int = 0  # 是否为竞技类物品 (0-否, 1-是)
    adv_obtain_num: int = 0  # 广告获取次数
    discount: int = 100  # 折扣百分比 (100表示原价)
    vip_discount: int = 100  # VIP折扣百分比
    is_vip_benefit: int = 0  # 是否为VIP福利 (0-否, 1-是)
    pay_channel: str = ""  # 支付渠道 (如"netease")
    product_id: str = ""  # 产品ID
    is_recommend: int = 0  # 是否为推荐物品 (0-否, 1-是)
    rec_info: List[Any] = field(default_factory=list)  # 推荐信息列表
    remark_num: int = 0  # 评论数量
    is_top: int = 0  # 是否置顶 (0-否, 1-是)
    is_joint: int = 0  # 是否为联合物品 (0-否, 1-是)
    sell_tags: List[Any] = field(default_factory=list)  # 销售标签列表
    rebate_activity_id: str = "0"  # 返利活动ID
    is_ea: int = 0  # 是否为EA(早期访问)物品 (0-否, 1-是)
    season_mod_id: str = "0"  # 赛季模组ID
    entity_id: str = ""  # 实体ID
    vip_only: bool = False  # 是否仅限VIP
    season_begin: int = 0  # 赛季开始时间戳
    rebate_max_num: int = 0  # 最大返利数量
    rebate_discount_num: int = 0  # 返利折扣数量
    playing_uuid: str = ""  # 游玩UUID
    behaviour_uuid: str = ""  # 行为UUID
    is_sync: int = 0  # 是否同步 (0-不同步, 1-同步)
    performance_score: float = 0.0  # 性能评分 (0-5分)
    playability_score: float = 0.0  # 可玩性评分 (0-5分)
    creativity_score: float = 0.0  # 创意评分 (0-5分)
    visual_score: float = 0.0  # 视觉效果评分 (0-5分)
    score_player_num: int = 0  # 参与评分玩家数量
    performance_distribution: Dict[str, int] = field(default_factory=dict)  # 性能评分分布 (1-5分对应人数)
    playability_distribution: Dict[str, int] = field(default_factory=dict)  # 可玩性评分分布
    creativity_distribution: Dict[str, int] = field(default_factory=dict)  # 创意评分分布
    visual_distribution: Dict[str, int] = field(default_factory=dict)  # 视觉效果评分分布
    score_trend_json: Union[Dict[str, Dict[str, float]], List] = field(default_factory=dict)  # 评分趋势数据 (按周)
    cur_num: Union[int, str] = 0  # 当前数量 (可能是整数或字符串)
    discount_end_time: int = 0  # 折扣结束时间戳
    mod_version: str = ""  # 模组版本号
    non_support_mod_versions: str = ""  # 不支持的模组版本
    rarity: int = 0  # 稀有度 (0-普通)
    is_lottery_reward: bool = False  # 是否为抽奖奖励
    is_persona: int = 0  # 是否为人格化物品 (0-否, 1-是)
    lottery_id: int = 0  # 抽奖ID
    persona_mtypeid: int = 0  # 人格主类型ID
    persona_stypeid: int = 0  # 人格子类型ID
    suit_id: str = "0"  # 套装ID
    dyeing: str = ""  # 染色信息
    tBuy: int = 0  # 购买时间戳
    tExpire: int = 0  # 过期时间戳
    activity_only: int = 0  # 是否仅限活动 (0-否, 1-是)
    developer_name: str = ""  # 开发者名称
    developer_urs: str = ""  # 开发者URS账号
    exchange_type: int = 0  # 兑换类型
    is_wish: int = 0  # 是否加入愿望单 (0-否, 1-是)
    refund_info: Dict[str, Any] = field(default_factory=dict)  # 退款信息
    is_official_item: int = 0  # 是否为官方物品 (0-否, 1-是)
    pvp: bool = False  # 是否支持PVP
    demo_id: str = "0"  # 演示ID
    vanity_number: str = ""  # 虚数编号 (自定义编号)
    normal_number: str = ""  # 普通编号
    perf_params: Optional[Union[Dict[str, Any], Any]] = "None"  # 性能参数 (字典或JSON字符串)
    value: str = ""  # 值 (意义不明确)
    reason: str = ""  # 推荐原因
    rating: str = ""  # 评分 (字符串形式)
    is_distribute: bool = False  # 是否分发
    rebate_tag: int = 0  # 返利标签
    is_fellow: int = 0  # 是否为伙伴物品 (0-否, 1-是)
    headimg: str = ""  # 头像图片URL

@dataclass
class RecommendEntity(Entity):
    """推荐实体容器"""
    ab_second_tag: int = 0  # AB测试二级标签
    ab_tag: int = 0  # AB测试标签
    tag: int = 0  # 标签ID
    campaign_id: int = 0  # 活动ID
    ret_list: List[RecommendItem] = field(default_factory=list)  # 推荐物品列表
    distribute_list: List[Any] = field(default_factory=list)  # 分发列表
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecommendEntity":
        """自定义反序列化方法，处理嵌套的推荐项列表"""
        ret_list = [RecommendItem(**item) for item in data.get("ret_list", [])]
        return cls(
            ab_second_tag=data.get("ab_second_tag", 0),
            ab_tag=data.get("ab_tag", 0),
            tag=data.get("tag", 0),
            campaign_id=data.get("campaign_id", 0),
            ret_list=ret_list,
            distribute_list=data.get("distribute_list", [])
        )

@dataclass
class ExtractRecommendListResponse(Response):
    """提取推荐列表响应"""
    entity: RecommendEntity = field(default_factory=RecommendEntity)  # 推荐实体
    total: str = "0"  # 推荐物品总数
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExtractRecommendList":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=RecommendEntity.from_dict(data.get("entity", {})),
            total=data.get("total", "0")
        )

@dataclass
class SearchByKeywordItemEntity(Entity):
    """搜索关键词物品实体"""
    item_id: str = ""  # 物品ID
    first_type: int = 0  # 一级分类ID（1=地图，2=模组/组件，6=玩法等）
    second_type: int = 0  # 二级分类ID（在first_type下的细分）
    pic_tag_state: str = "0"  # 图片标签状态 (0-无特殊标记)
    res_name: str = ""  # 资源名称
    res_size: str = "0"  # 资源大小 (字符串形式，单位字节)
    res_md5: str = ""  # 资源MD5校验值
    stars: float = 0.0  # 星级评分 (0-5分)
    download_num: str = "0"  # 总下载次数 (字符串形式)
    week_download_num: str = "0"  # 周下载次数 (字符串形式)
    points: int = 0  # 积分价格
    diamond: int = 0  # 钻石价格
    res_version: str = "0"  # 资源版本号
    is_item_time_limit: int = 0  # 是否限时物品 (0-非限时, 1-限时)
    item_remain_time: int = 0  # 物品剩余时间 (秒)
    buy_state: int = 0  # 购买状态 (0-未购买, 1-已购买)
    goods_state: int = 0  # 商品状态 (1-正常)
    status: int = 0  # 物品状态 (1-上架)
    skin_body_type: int = 0  # 皮肤体型类型 (0-默认)
    title_image_url: str = ""  # 标题图片URL
    title_image_version: int = 0  # 标题图片版本
    resource_packs_version: str = ""  # 资源包版本 (格式: "主,次,修订")
    behavior_packs_version: str = ""  # 行为包版本 (格式: "主,次,修订")
    lobby_tag: List[Any] = field(default_factory=list)  # 大厅标签ID列表
    rel_iid: str = "0"  # 相关物品ID
    is_competitive: int = 0  # 是否为竞技类物品 (0-否, 1-是)
    adv_obtain_num: int = 0  # 广告获取次数
    discount: int = 100  # 折扣百分比 (100表示原价)
    vip_discount: int = 100  # VIP折扣百分比
    is_vip_benefit: int = 0  # 是否为VIP福利 (0-否, 1-是)
    pay_channel: str = ""  # 支付渠道 (如"netease")
    product_id: str = ""  # 产品ID
    is_recommend: int = 0  # 是否为推荐物品 (0-否, 1-是)
    rec_info: List[Any] = field(default_factory=list)  # 推荐信息列表
    remark_num: int = 0  # 评论数量
    is_top: int = 0  # 是否置顶 (0-否, 1-是)
    is_joint: int = 0  # 是否为联合物品 (0-否, 1-是)
    sell_tags: List[Any] = field(default_factory=list)  # 销售标签列表
    rebate_activity_id: str = "0"  # 返利活动ID
    is_ea: int = 0  # 是否为EA(早期访问)物品 (0-否, 1-是)
    season_mod_id: str = "0"  # 赛季模组ID
    entity_id: str = ""  # 实体ID
    vip_only: bool = False  # 是否仅限VIP
    season_begin: str = "0"  # 赛季开始时间戳
    rebate_max_num: int = 0  # 最大返利数量
    rebate_discount_num: int = 0  # 返利折扣数量
    playing_uuid: str = ""  # 游玩UUID
    behaviour_uuid: str = ""  # 行为UUID
    is_sync: int = 0  # 是否同步 (0-不同步, 1-同步)
    performance_score: float = 0.0  # 性能评分 (0-5分)
    playability_score: float = 0.0  # 可玩性评分 (0-5分)
    creativity_score: float = 0.0  # 创意评分 (0-5分)
    visual_score: float = 0.0  # 视觉效果评分 (0-5分)
    score_player_num: int = 0  # 参与评分玩家数量
    performance_distribution: str = ""  # 性能评分分布 (1-5分对应人数，JSON格式)
    playability_distribution: str = ""  # 可玩性评分分布 (JSON格式)
    creativity_distribution: str = ""  # 创意评分分布 (JSON格式)
    visual_distribution: str = ""  # 视觉效果评分分布 (JSON格式)
    score_trend_json: str = ""  # 评分趋势数据 (按周，JSON格式)
    effect_mtypeid: int = 0  # 特效主类型ID (0-无特效)
    effect_stypeid: int = 0  # 特效子类型ID (0-无特效)
    cur_num: int = 0  # 当前数量 (可能是整数或字符串)
    discount_end_time: int = 0  # 折扣结束时间戳
    mod_version: str = ""  # 模组版本号
    non_support_mod_versions: str = ""  # 不支持的模组版本
    rarity: str = "0"  # 稀有度 (0-普通)
    is_lottery_reward: str = "0"  # 是否为抽奖奖励
    is_persona: str = "0"  # 是否为人格化物品 (0-否, 1-是)
    lottery_id: str = "0"  # 抽奖ID
    persona_mtypeid: str = "0"  # 人格主类型ID
    persona_stypeid: str = "0"  # 人格子类型ID
    suit_id: str = "0"  # 套装ID
    dyeing: str = ""  # 染色信息
    tBuy: int = 0  # 购买时间戳
    tExpire: int = 0  # 过期时间戳
    activity_only: int = 0  # 是否仅限活动 (0-否, 1-是)
    developer_name: str = ""  # 开发者名称
    developer_urs: str = ""  # 开发者URS账号
    exchange_type: int = 0  # 兑换类型
    is_wish: int = 0  # 是否加入愿望单 (0-否, 1-是)
    refund_info: Dict[str, Any] = field(default_factory=dict)  # 退款信息
    is_official_item: int = 0  # 是否为官方物品 (0-否, 1-是)
    pvp: bool = True  # 是否支持PVP
    demo_id: str = "0"  # 演示ID
    vanity_number: str = ""  # 虚数编号 (自定义编号)
    normal_number: str = ""  # 普通编号
    perf_params: Optional[Union[Dict[str, Any], str]] = "None"  # 性能参数 (字典或JSON字符串)
    rebate_tag: int = 0  # 返利标签
    jelly_id: str = ""  # 果冻ID
    source: str = "low"  # 来源 ("low"=普通来源)
    special_discount_activity: int = 0  # 特殊折扣活动 (0-无活动, 1-有活动)
    activity_id: str | None = None  # 活动ID（有一些组件没有活动ID）

    def to_dict(self) -> Dict[str, Any]:
        if self.activity_id == None:
            del self.activity_id # 保证还原出来的 dict 是一致的
        return super().to_dict()

@dataclass
class SearchByKeywordResponse(EntitiesResponse):
    """关键词搜索响应"""
    entities: List[SearchByKeywordItemEntity] = field(default_factory=list)  # 资源项实体列表（包含所有搜索结果）
    total: str = "0"  # 搜索结果总数
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchByKeywordResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),  
            message=data.get("message", ""),  
            details=data.get("details", ""),  
            entities=[SearchByKeywordItemEntity(**item) for item in data.get("entities", [])],  
            total=data.get("total", "0")  
        )

@dataclass
class DLCInfo(Entity):
    """DLC(下载内容)信息实体"""
    dlc_switch: bool = False  # DLC开关状态
    dlc_type: str = ""  # DLC类型 ("master"=主DLC, "slave"=从DLC)
    master: str = ""  # 主DLC的ID
    slave_list: List[str] = field(default_factory=list)  # 从DLCID列表

@dataclass
class RecentStarsData(Entity):
    """近期评分数据实体"""
    score: float = 0.0  # 近期平均评分
    user_count: int = 0  # 参与评分的用户数量

@dataclass
class ItemDetailEntity(Entity):
    """物品详情实体"""
    item_id: str = ""  # 物品唯一ID
    first_type: int = 0  # 一级分类ID (1=地图, 2=模组/组件, 6=玩法等)
    second_type: int = 0  # 二级分类ID (在一级分类下的细分)
    pic_tag_state: int = 0  # 图片标签状态 (0=无特殊标记)
    res_name: str = ""  # 资源名称
    res_size: str = ""  # 资源大小 (字节数)
    res_md5: str = ""  # 资源MD5校验值
    stars: float = 0.0  # 星级评分 (0-5分)
    download_num: str = "0"  # 总下载次数
    week_download_num: str = "0"  # 本周下载次数
    points: int = 0  # 积分价格
    diamond: int = 0  # 钻石价格
    res_version: int = 0  # 资源版本号
    is_item_time_limit: int = 0  # 是否限时物品 (0=永久, 1=限时)
    item_remain_time: int = 0  # 物品剩余时间 (秒)
    buy_state: int = 0  # 购买状态 (0=未购买, 1=已购买)
    goods_state: int = 0  # 商品状态 (1=正常上架)
    status: int = 0  # 物品状态 (1=正常)
    skin_body_type: int = 0  # 皮肤体型类型 (0=默认)
    title_image_url: str = ""  # 标题图片URL
    title_image_version: int = 0  # 标题图片版本
    resource_packs_version: str = ""  # 资源包版本 (格式: "主,次,修订")
    behavior_packs_version: str = ""  # 行为包版本 (格式: "主,次,修订")
    lobby_tag: List[int] = field(default_factory=list)  # 大厅标签ID列表
    rel_iid: str = "0"  # 相关物品ID
    is_competitive: int = 0  # 是否为竞技类物品 (0=否, 1=是)
    adv_obtain_num: int = 0  # 广告获取次数
    discount: int = 100  # 折扣百分比 (100=原价)
    vip_discount: int = 100  # VIP折扣百分比
    is_vip_benefit: int = 0  # 是否为VIP福利 (0=否, 1=是)
    pay_channel: str = ""  # 支付渠道 ("netease"=网易支付)
    product_id: str = ""  # 产品ID
    is_recommend: int = 0  # 是否为推荐物品 (0=否, 1=是)
    rec_info: List[Any] = field(default_factory=list)  # 推荐信息列表
    remark_num: int = 0  # 评论数量
    is_top: int = 0  # 是否置顶 (0=否, 1=是)
    is_joint: int = 0  # 是否为联合物品 (0=否, 1=是)
    sell_tags: List[Any] = field(default_factory=list)  # 销售标签列表
    rebate_activity_id: int = 0  # 返利活动ID (0=无活动)
    is_ea: int = 0  # 是否为EA(早期访问)物品 (0=否, 1=是)
    season_mod_id: str = "0"  # 赛季模组ID ("0"=非赛季模组)
    entity_id: str = ""  # 实体ID (通常与item_id相同)
    refresh_time: int = 0  # 最后刷新时间戳
    create_time: int = 0  # 创建时间戳
    info: str = ""  # 物品详细信息 (HTML格式)
    developer_name: str = ""  # 开发者名称
    comment_count: int = 0  # 评论数量
    mod_format: int = 0  # 模组格式
    pic_url_list: List[str] = field(default_factory=list)  # 详情图片URL列表
    video_info_list: List[Any] = field(default_factory=list)  # 视频信息列表
    vip_only: bool = False  # 是否仅限VIP
    season_begin: int = 0  # 赛季开始时间戳
    discount_end_time: int = 0  # 折扣结束时间戳
    mod_version: str = ""  # 模组版本号
    non_support_mod_versions: str = ""  # 不支持的模组版本
    performance_score: float = 0.0  # 性能评分 (0-5分)
    playability_score: float = 0.0  # 可玩性评分 (0-5分)
    creativity_score: float = 0.0  # 创意评分 (0-5分)
    visual_score: float = 0.0  # 视觉效果评分 (0-5分)
    score_player_num: int = 0  # 参与评分玩家数量
    performance_distribution: Dict[str, int] = field(default_factory=dict)  # 性能评分分布 (1-5分对应人数)
    playability_distribution: Dict[str, int] = field(default_factory=dict)  # 可玩性评分分布
    creativity_distribution: Dict[str, int] = field(default_factory=dict)  # 创意评分分布
    visual_distribution: Dict[str, int] = field(default_factory=dict)  # 视觉效果评分分布
    score_trend_json: List[Any] = field(default_factory=list)  # 评分趋势数据
    developer_id: int = 0  # 开发者ID
    headimg: str = ""  # 开发者头像URL
    is_sync: int = 0  # 是否同步 (0=不同步, 1=同步)
    rarity: int = 0  # 稀有度 (0=普通)
    is_lottery_reward: bool = False  # 是否为抽奖奖励
    lottery_id: int = 0  # 抽奖ID (0=无抽奖)
    is_fellow: int = 0  # 是否为伙伴物品 (0=否, 1=是)
    fellow_num: int = 0  # 伙伴数量
    playing_uuid: str = ""  # 游玩UUID (游戏内加载用)
    behaviour_uuid: str = ""  # 行为UUID (游戏内加载用)
    auth_tag: Optional[Any] = None  # 认证标签
    effect_mtypeid: int = 0  # 特效主类型ID (0=无特效)
    effect_stypeid: int = 0  # 特效子类型ID (0=无特效)
    is_wish: int = 0  # 是否在愿望单 (0=否, 1=是)
    stars_distribution: List[float] = field(default_factory=list)  # 星级分布数据
    stars_status: int = 0  # 星级状态
    special_discount_activity: int = 0  # 特殊折扣活动 (0=无, 1=有)
    developer_urs: str = ""  # 开发者URS账号
    trial_ticket: List[Any] = field(default_factory=list)  # 试用券信息
    refund_info: Dict[str, Any] = field(default_factory=dict)  # 退款信息
    is_official_item: int = 0  # 是否为官方物品 (0=否, 1=是)
    pvp: bool = False  # 是否支持PVP
    tags: List[Any] = field(default_factory=list)  # 标签列表
    demo_id: str = "0"  # 演示ID ("0"=无演示)
    vanity_number: str = ""  # 虚数编号
    normal_number: str = ""  # 普通编号
    comp_list: List[Any] = field(default_factory=list)  # 组件列表
    jelly_id: str = ""  # 果冻ID
    item_remain_adv_num: int = 0  # 物品剩余广告获取次数
    item_means_daily_remain_num: int = 0  # 物品日均剩余数量
    item_means_daily_total_num: int = 0  # 物品日均总数量
    item_watch_num: int = 0  # 物品观看次数
    is_downloaded: int = 0  # 是否已下载 (0=否, 1=是)
    is_new: int = 0  # 是否新品 (0=否, 1=是)
    exchange_type: int = 0  # 兑换类型 (0=不可兑换)
    is_developer: int = 0  # 是否为开发者 (0=否, 1=是)
    is_core_developer: int = 0  # 是否核心开发者 (0=否, 1=是)
    joint_info: List[Any] = field(default_factory=list)  # 联合信息
    is_lobby_collection: int = 0  # 是否大厅收藏 (0=否, 1=是)
    b_has_mall: int = 0  # 是否有商城 (0=否, 1=是)
    activity_id: str = ""  # 活动ID
    dyeing_list: List[Any] = field(default_factory=list)  # 染色列表
    dyeing_origin_iid: str = ""  # 原始染色物品ID
    dyeing_currency_num: int = 0  # 染色货币数量
    dyeing_origin: bool = False  # 是否为原始染色
    card_sub_type: int = 0  # 卡片子类型
    benefit_item_create_time: int = 0  # 福利物品创建时间
    benefit_item_end_time: int = 0  # 福利物品结束时间
    linkage_res: int = 0  # 联动资源
    union_developer_list: List[Any] = field(default_factory=list)  # 联合开发者列表
    is_shopping_cart: int = 0  # 是否在购物车 (0=否, 1=是)
    full_reduction_activity: Optional[Any] = None  # 满减活动信息
    item_pack_iids: List[Any] = field(default_factory=list)  # 物品包ID列表
    new_topic_id: int = 0  # 新话题ID
    resource_pack_iids: List[Any] = field(default_factory=list)  # 资源包ID列表
    jump_activity_info: Dict[str, Any] = field(default_factory=dict)  # 跳转活动信息
    dlc_info: DLCInfo = field(default_factory=DLCInfo)  # DLC(下载内容)信息
    recent_stars_data: RecentStarsData = field(default_factory=RecentStarsData)  # 近期星级数据
    appearance_id: Optional[Any] = None  # 外观ID
    appearance_type: Optional[Any] = None  # 外观类型
    is_maintain: int = 0  # 是否维护中 (0=否, 1=是)
    free_play_time: int = 0  # 免费游玩时间 (秒)
    act_free_play_time: int = 0  # 活动免费游玩时间 (秒)
    perf_params: Optional[Union[Dict[str, Any], str]] = "None"  # 性能参数

@dataclass
class GetItemDetailResponse(SummaryMD5EntityResponse):
    """获取物品详情响应"""
    entity: ItemDetailEntity = field(default_factory=ItemDetailEntity)  # 物品详情实体
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetItemDetailResponse":
        """反序列化方法：将字典数据转换为GetItemDetailResponse对象"""
        entity_data = data.get("entity", {})
        entity_data["dlc_info"] = DLCInfo.from_dict(entity_data.get("dlc_info", {}))
        entity_data["recent_stars_data"] = RecentStarsData.from_dict(entity_data.get("recent_stars_data", {}))
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            summary_md5=data.get("summary_md5", ""),
            entity=ItemDetailEntity(**entity_data)
        )

@dataclass
class RecommendHotSpotItem(Entity):
    """热点推荐物品实体类，包含热点推荐物品的所有详细信息"""
    item_id: str = ""  # 物品唯一ID
    first_type: int = 0  # 一级分类ID (1=地图, 2=模组/组件, 6=玩法等)
    second_type: int = 0  # 二级分类ID (在一级分类下的细分)
    pic_tag_state: int = 0  # 图片标签状态 (0=无特殊标记)
    res_name: str = ""  # 资源名称
    res_size: str = ""  # 资源大小 (字节数)
    res_md5: str = ""  # 资源MD5校验值
    stars: float = 0.0  # 星级评分 (0-5分)
    download_num: str = "0"  # 总下载次数
    week_download_num: Union[int, str] = 0  # 本周下载次数
    points: int = 0  # 积分价格
    diamond: int = 0  # 钻石价格
    res_version: Union[int, str] = 0  # 资源版本号
    is_item_time_limit: int = 0  # 是否限时物品 (0=永久, 1=限时)
    item_remain_time: int = 0  # 物品剩余时间 (秒)
    buy_state: int = 0  # 购买状态 (0=未购买, 1=已购买)
    goods_state: int = 0  # 商品状态 (1=正常上架)
    status: int = 0  # 物品状态 (1=正常)
    skin_body_type: int = 0  # 皮肤体型类型 (0=默认)
    title_image_url: str = ""  # 标题图片URL
    title_image_version: int = 0  # 标题图片版本
    resource_packs_version: str = ""  # 资源包版本 (格式: "主,次,修订")
    behavior_packs_version: str = ""  # 行为包版本 (格式: "主,次,修订")
    lobby_tag: List[Any] = field(default_factory=list)  # 大厅标签ID列表
    rel_iid: Union[int, str] = 0  # 相关物品ID
    is_competitive: int = 0  # 是否为竞技类物品 (0=否, 1=是)
    adv_obtain_num: int = 0  # 广告获取次数
    discount: int = 100  # 折扣百分比 (100=原价)
    vip_discount: int = 100  # VIP折扣百分比
    is_vip_benefit: int = 0  # 是否为VIP福利 (0=否, 1=是)
    pay_channel: str = ""  # 支付渠道 ("netease"=网易支付)
    product_id: str = ""  # 产品ID
    is_recommend: int = 0  # 是否为推荐物品 (0=否, 1=是)
    rec_info: List[Any] = field(default_factory=list)  # 推荐信息列表
    remark_num: int = 0  # 评论数量
    is_top: int = 0  # 是否置顶 (0=否, 1=是)
    is_joint: int = 0  # 是否为联合物品 (0=否, 1=是)
    sell_tags: List[Any] = field(default_factory=list)  # 销售标签列表
    rebate_activity_id: str = "0"  # 返利活动ID (0=无活动)
    is_ea: int = 0  # 是否为EA(早期访问)物品 (0=否, 1=是)
    season_mod_id: str = "0"  # 赛季模组ID ("0"=非赛季模组)
    entity_id: str = ""  # 实体ID (通常与item_id相同)
    vip_only: bool = False  # 是否仅限VIP
    season_begin: Union[int, str] = 0  # 赛季开始时间戳
    rebate_max_num: int = 0  # 最大返利数量
    rebate_discount_num: int = 0  # 返利折扣数量
    playing_uuid: str = ""  # 游玩UUID (游戏内加载用)
    behaviour_uuid: str = ""  # 行为UUID (游戏内加载用)
    is_sync: int = 0  # 是否同步 (0=不同步, 1=同步)
    performance_score: float = 0.0  # 性能评分 (0-5分)
    playability_score: float = 0.0  # 可玩性评分 (0-5分)
    creativity_score: float = 0.0  # 创意评分 (0-5分)
    visual_score: float = 0.0  # 视觉效果评分 (0-5分)
    score_player_num: int = 0  # 参与评分玩家数量
    performance_distribution: Dict[str, int] = field(default_factory=dict)  # 性能评分分布 (1-5分对应人数)
    playability_distribution: Dict[str, int] = field(default_factory=dict)  # 可玩性评分分布
    creativity_distribution: Dict[str, int] = field(default_factory=dict)  # 创意评分分布
    visual_distribution: Dict[str, int] = field(default_factory=dict)  # 视觉效果评分分布
    score_trend_json: Union[Dict[str, Dict[str, float]], List, str] = field(default_factory=dict)  # 评分趋势数据
    effect_mtypeid: int = 0  # 特效主类型ID (0=无特效)
    effect_stypeid: int = 0  # 特效子类型ID (0=无特效)
    cur_num: Union[int, str] = 0  # 当前数量
    discount_end_time: int = 0  # 折扣结束时间戳
    mod_version: str = ""  # 模组版本号
    non_support_mod_versions: str = ""  # 不支持的模组版本
    rarity: Union[int, str] = 0  # 稀有度 (0=普通)
    is_lottery_reward: Union[bool, str] = False  # 是否为抽奖奖励
    is_persona: Union[int, str] = 0  # 是否为人格化物品 (0=否, 1=是)
    lottery_id: Union[int, str] = 0  # 抽奖ID (0=无抽奖)
    persona_mtypeid: Union[int, str] = 0  # 人格主类型ID
    persona_stypeid: Union[int, str] = 0  # 人格子类型ID
    suit_id: str = "0"  # 套装ID
    dyeing: str = ""  # 染色信息
    tBuy: int = 0  # 购买时间戳
    tExpire: int = 0  # 过期时间戳
    activity_only: int = 0  # 是否仅限活动 (0=否, 1=是)
    pic_url_list: List[str] = field(default_factory=list)  # 详情图片URL列表
    video_info_list: List[Dict[str, Any]] = field(default_factory=list)  # 视频信息列表
    developer_name: str = ""  # 开发者名称
    developer_urs: str = ""  # 开发者URS账号
    exchange_type: int = 0  # 兑换类型 (0=不可兑换)
    is_wish: int = 0  # 是否在愿望单 (0=否, 1=是)
    refund_info: Dict[str, Any] = field(default_factory=dict)  # 退款信息
    is_official_item: int = 0  # 是否为官方物品 (0=否, 1=是)
    pvp: bool = False  # 是否支持PVP
    demo_id: str = "0"  # 演示ID ("0"=无演示)
    vanity_number: str = ""  # 虚数编号
    normal_number: str = ""  # 普通编号
    perf_params: Optional[Union[Dict[str, Any], Any]] = "None"  # 性能参数 (字典或JSON字符串)
    linkage_res: int = 0  # 联动资源
    jelly_id: str = ""  # 果冻ID
    dyeing_list: List[Any] = field(default_factory=list)  # 染色列表
    dyeing_origin_iid: str = ""  # 原始染色物品ID
    dyeing_currency_num: int = 0  # 染色货币数量
    rebate_tag: int = 0  # 返利标签
    special_discount_activity: int = 0  # 特殊折扣活动 (0=无, 1=有)
    activity_id: Optional[str] = None  # 活动ID（可选字段）
    price_type: int = 0  # 价格类型 (1=免费, 2=付费)

    def to_dict(self) -> Dict[str, Any]:
        if self.activity_id == None:
            del self.activity_id
        return super().to_dict()

@dataclass
class RecommendHotSpotEntity(Entity):
    """热点推荐实体类，包含一个关键词及其相关的推荐物品列表"""
    word: str = ""  # 关键词
    recommend_reason: str = ""  # 推荐理由
    iid_list: List[RecommendHotSpotItem] = field(default_factory=list)  # 推荐物品列表
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecommendHotSpotEntity":
        """反序列化方法"""
        return cls(
            word=data.get("word", ""),
            recommend_reason=data.get("recommend_reason", ""),
            iid_list=[RecommendHotSpotItem(**item) for item in data.get("iid_list", [])]
        )

@dataclass
class QueryRecommendHotSpotResponse(EntitiesResponse):
    """热点推荐查询响应类，包含多个热点推荐实体"""
    entities: List[RecommendHotSpotEntity] = field(default_factory=list)  # 热点实体列表
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QueryRecommendHotSpotResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entities=[RecommendHotSpotEntity.from_dict(e) for e in data.get("entities", [])]
        )


@dataclass
class WaterFallItem(Entity):
    """瀑布物品实体"""
    item_id: str = ""  # 物品ID
    first_type: int = 0  # 一级分类ID
    second_type: int = 0  # 二级分类ID
    pic_tag_state: int = 0  # 图片标签状态 (0-无特殊标记)
    res_name: str = ""  # 资源名称
    res_size: str = ""  # 资源大小 (字符串形式，单位字节)
    res_md5: str = ""  # 资源MD5校验值
    stars: float = 0.0  # 星级评分 (0-5分)
    download_num: str = "0"  # 总下载次数 (字符串形式)
    week_download_num: str = "0"  # 周下载次数 (字符串形式)
    points: int = 0  # 积分价格
    diamond: int = 0  # 钻石价格,
    res_version: int = 0  # 资源版本号
    is_item_time_limit: int = 0  # 是否限时物品 (0-非限时, 1-限时)
    item_remain_time: int = 0  # 物品剩余时间 (秒)
    buy_state: int = 0  # 购买状态 (0-未购买, 1-已购买)
    goods_state: int = 0  # 商品状态 (1-正常)
    status: int = 0  # 物品状态 (1-上架)
    skin_body_type: int = 0  # 皮肤体型类型 (0-默认)
    title_image_url: str = ""  # 标题图片URL
    title_image_version: int = 0  # 标题图片版本
    resource_packs_version: str = ""  # 资源包版本 (格式: "主,次,修订")
    behavior_packs_version: str = ""  # 行为包版本 (格式: "主,次,修订")
    lobby_tag: List[int] = field(default_factory=list)  # 大厅标签ID列表
    rel_iid: int = 0  # 相关物品ID
    is_competitive: int = 0  # 是否为竞技类物品 (0-否, 1-是)
    adv_obtain_num: int = 0  # 广告获取次数
    discount: int = 100  # 折扣百分比 (100表示原价)
    vip_discount: int = 100  # VIP折扣百分比
    is_vip_benefit: int = 0  # 是否为VIP福利 (0-否, 1-是)
    pay_channel: str = ""  # 支付渠道 (如"netease")
    product_id: str = ""  # 产品ID
    is_recommend: int = 0  # 是否为推荐物品 (0-否, 1-是)
    rec_info: List[Any] = field(default_factory=list)  # 推荐信息列表
    remark_num: int = 0  # 评论数量
    is_top: int = 0  # 是否置顶 (0-否, 1-是)
    is_joint: int = 0  # 是否为联合物品 (0-否, 1-是)
    sell_tags: List[Any] = field(default_factory=list)  # 销售标签列表
    rebate_activity_id: str = "0"  # 返利活动ID
    is_ea: int = 0  # 是否为EA(早期访问)物品 (0-否, 1-是)
    season_mod_id: str = "0"  # 赛季模组ID
    entity_id: str = ""  # 实体ID
    vip_only: bool = False  # 是否仅限VIP
    season_begin: int = 0  # 赛季开始时间戳
    rebate_max_num: int = 0  # 最大返利数量
    rebate_discount_num: int = 0  # 返利折扣数量
    playing_uuid: str = ""  # 游玩UUID
    behaviour_uuid: str = ""  # 行为UUID
    is_sync: int = 0  # 是否同步 (0-不同步, 1-同步)
    performance_score: float = 0.0  # 性能评分 (0-5分)
    playability_score: float = 0.0  # 可玩性评分 (0-5分)
    creativity_score: float = 0.0  # 创意评分 (0-5分)
    visual_score: float = 0.0  # 视觉效果评分 (0-5分)
    score_player_num: int = 0  # 参与评分玩家数量
    performance_distribution: Dict[str, int] = field(default_factory=dict)  # 性能评分分布 (1-5分对应人数)
    playability_distribution: Dict[str, int] = field(default_factory=dict)  # 可玩性评分分布
    creativity_distribution: Dict[str, int] = field(default_factory=dict)  # 创意评分分布
    visual_distribution: Dict[str, int] = field(default_factory=dict)  # 视觉效果评分分布
    score_trend_json: Union[Dict[str, Dict[str, float]], List] = field(default_factory=dict)  # 评分趋势数据 (按周)
    cur_num: Union[int, str] = 0  # 当前数量 (可能是整数或字符串)
    discount_end_time: int = 0  # 折扣结束时间戳
    mod_version: str = ""  # 模组版本号
    non_support_mod_versions: str = ""  # 不支持的模组版本
    rarity: int = 0  # 稀有度 (0-普通)
    is_lottery_reward: bool = False  # 是否为抽奖奖励
    is_persona: int = 0  # 是否为人格化物品 (0-否, 1-是)
    lottery_id: int = 0  # 抽奖ID
    persona_mtypeid: int = 0  # 人格主类型ID
    persona_stypeid: int = 0  # 人格子类型ID
    suit_id: str = "0"  # 套装ID
    dyeing: str = ""  # 染色信息
    tBuy: int = 0  # 购买时间戳
    tExpire: int = 0  # 过期时间戳
    activity_only: int = 0  # 是否仅限活动 (0-否, 1-是)
    developer_name: str = ""  # 开发者名称
    developer_urs: str = ""  # 开发者URS账号
    exchange_type: int = 0  # 兑换类型
    is_wish: int = 0  # 是否加入愿望单 (0-否, 1-是)
    refund_info: Dict[str, Any] = field(default_factory=dict)  # 退款信息
    is_official_item: int = 0  # 是否为官方物品 (0-否, 1-是)
    pvp: bool = False  # 是否支持PVP
    demo_id: str = "0"  # 演示ID
    vanity_number: str = ""  # 虚数编号 (自定义编号)
    normal_number: str = ""  # 普通编号
    perf_params: Optional[Union[Dict[str, Any], str]] = "None"  # 性能参数 (字典或JSON字符串)
    rebate_tag: int = 0  # 返利标签
    is_distribute: bool = False  # 是否分发

@dataclass
class WaterFallEntity(Entity):
    """瀑布实体容器"""
    tag: int = 0  # 标签ID
    campaign_id: int = 0  # 活动ID
    ret_list: List[WaterFallItem] = field(default_factory=list)  # 瀑布物品列表
    distribute_list: List[Any] = field(default_factory=list)  # 分发列表
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WaterFallEntity":
        """自定义反序列化方法，处理嵌套的瀑布项列表"""
        ret_list = [WaterFallItem(**item) for item in data.get("ret_list", [])]
        return cls(
            tag=data.get("tag", 0),
            campaign_id=data.get("campaign_id", 0),
            ret_list=ret_list,
            distribute_list=data.get("distribute_list", [])
        )

@dataclass
class WaterFallResponse(Response):
    """瀑布响应"""
    entity: WaterFallEntity = field(default_factory=WaterFallEntity)  # 瀑布实体
    total: str = "0"  # 瀑布物品总数
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WaterFallResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=WaterFallEntity.from_dict(data.get("entity", {})),
            total=data.get("total", "0")
        )

@dataclass
class SearchByIdItemEntity(Entity):
    """搜索ID物品实体"""
    item_id: str = ""  # 物品唯一ID
    first_type: int = 0  # 一级分类ID (1=地图, 2=模组/组件, 6=玩法等)
    second_type: int = 0  # 二级分类ID (在一级分类下的细分)
    pic_tag_state: int = 0  # 图片标签状态 (0=无特殊标记)
    res_name: str = ""  # 资源名称
    res_size: str = ""  # 资源大小 (字节数)
    res_md5: str = ""  # 资源MD5校验值
    stars: float = 0.0  # 星级评分 (0-5分)
    download_num: str = "0"  # 总下载次数
    week_download_num: str = "0"  # 本周下载次数
    points: int = 0  # 积分价格
    diamond: int = 0  # 钻石价格
    res_version: int = 0  # 资源版本号
    is_item_time_limit: int = 0  # 是否限时物品 (0=永久, 1=限时)
    item_remain_time: int = 0  # 物品剩余时间 (秒)
    buy_state: int = 0  # 购买状态 (0=未购买, 1=已购买)
    goods_state: int = 0  # 商品状态 (1=正常上架)
    status: int = 0  # 物品状态 (1=正常)
    skin_body_type: int = 0  # 皮肤体型类型 (0=默认)
    title_image_url: str = ""  # 标题图片URL
    title_image_version: int = 0  # 标题图片版本
    resource_packs_version: str = ""  # 资源包版本 (格式: "主,次,修订")
    behavior_packs_version: str = ""  # 行为包版本 (格式: "主,次,修订")
    lobby_tag: List[int] = field(default_factory=list)  # 大厅标签ID列表
    rel_iid: str = "0"  # 相关物品ID
    is_competitive: int = 0  # 是否为竞技类物品 (0=否, 1=是)
    adv_obtain_num: int = 0  # 广告获取次数
    discount: int = 100  # 折扣百分比 (100=原价)
    vip_discount: int = 100  # VIP折扣百分比
    is_vip_benefit: int = 0  # 是否为VIP福利 (0=否, 1=是)
    pay_channel: str = ""  # 支付渠道 ("netease"=网易支付)
    product_id: str = ""  # 产品ID
    is_recommend: int = 0  # 是否为推荐物品 (0=否, 1=是)
    rec_info: List[Any] = field(default_factory=list)  # 推荐信息列表
    remark_num: int = 0  # 评论数量
    is_top: int = 0  # 是否置顶 (0=否, 1=是)
    is_joint: int = 0  # 是否为联合物品 (0=否, 1=是)
    sell_tags: List[Any] = field(default_factory=list)  # 销售标签列表
    rebate_activity_id: int = 0  # 返利活动ID (0=无活动)
    is_ea: int = 0  # 是否为EA(早期访问)物品 (0=否, 1=是)
    season_mod_id: str = "0"  # 赛季模组ID ("0"=非赛季模组)
    entity_id: str = ""  # 实体ID (通常与item_id相同)
    vip_only: bool = False  # 是否仅限VIP
    season_begin: int = 0  # 赛季开始时间戳
    rebate_max_num: int = 0  # 最大返利数量
    rebate_discount_num: int = 0  # 返利折扣数量
    playing_uuid: str = ""  # 游玩UUID (游戏内加载用)
    behaviour_uuid: str = ""  # 行为UUID (游戏内加载用)
    is_sync: int = 0  # 是否同步 (0=不同步, 1=同步)
    performance_score: float = 0.0  # 性能评分 (0-5分)
    playability_score: float = 0.0  # 可玩性评分 (0-5分)
    creativity_score: float = 0.0  # 创意评分 (0-5分)
    visual_score: float = 0.0  # 视觉效果评分 (0-5分)
    score_player_num: int = 0  # 参与评分玩家数量
    performance_distribution: Dict[str, int] = field(default_factory=dict)  # 性能评分分布 (1-5分对应人数)
    playability_distribution: Dict[str, int] = field(default_factory=dict)  # 可玩性评分分布
    creativity_distribution: Dict[str, int] = field(default_factory=dict)  # 创意评分分布
    visual_distribution: Dict[str, int] = field(default_factory=dict)  # 视觉效果评分分布
    score_trend_json: List[Any] = field(default_factory=list)  # 评分趋势数据
    effect_mtypeid: int = 0  # 特效主类型ID (0=无特效)
    effect_stypeid: int = 0  # 特效子类型ID (0=无特效)
    cur_num: Union[int, str] = 0  # 当前数量 (可能是整数或字符串)
    discount_end_time: int = 0  # 折扣结束时间戳
    mod_version: str = ""  # 模组版本号
    non_support_mod_versions: str = ""  # 不支持的模组版本
    rarity: int = 0  # 稀有度 (0=普通)
    is_lottery_reward: bool = False  # 是否为抽奖奖励
    is_persona: int = 0  # 是否为人格化物品 (0-否, 1-是)
    lottery_id: int = 0  # 抽奖ID (0=无抽奖)
    persona_mtypeid: int = 0  # 人格主类型ID
    persona_stypeid: int = 0  # 人格子类型ID
    suit_id: str = "0"  # 套装ID
    dyeing: str = ""  # 染色信息
    tBuy: int = 0  # 购买时间戳
    tExpire: int = 0  # 过期时间戳
    activity_only: int = 0  # 是否仅限活动 (0-否, 1-是)
    pic_url_list: List[str] = field(default_factory=list)  # 详情图片URL列表
    video_info_list: List[Any] = field(default_factory=list)  # 视频信息列表
    developer_name: str = ""  # 开发者名称
    developer_urs: str = ""  # 开发者URS账号
    exchange_type: int = 0  # 兑换类型 (0=不可兑换)
    is_wish: int = 0  # 是否在愿望单 (0=否, 1=是)
    refund_info: Dict[str, Any] = field(default_factory=dict)  # 退款信息
    is_official_item: int = 0  # 是否为官方物品 (0=否, 1=是)
    pvp: bool = False  # 是否支持PVP
    demo_id: str = "0"  # 演示ID ("0"=无演示)
    vanity_number: str = ""  # 虚数编号
    normal_number: str = "4737660"  # 普通编号
    perf_params: Optional[Union[Dict[str, Any], Any]] = "None"  # 性能参数 (字典或JSON字符串)
    linkage_res: int = 0  # 联动资源
    jelly_id: str = ""  # 果冻ID
    dyeing_list: List[Any] = field(default_factory=list)  # 染色列表
    dyeing_origin_iid: str = ""  # 原始染色物品ID
    dyeing_currency_num: int = 0  # 染色货币数量
    rebate_tag: int = 0  # 返利标签
    special_discount_activity: int = 0  # 特殊折扣活动 (0=无, 1=有)
    price_type: int = 1  # 价格类型 (1=免费, 2=付费)
    resource_pack_iids: List[Any] = field(default_factory=list)  # 资源包ID列表
    dlc_info: Dict[str, Any] = field(default_factory=dict)  # DLC(下载内容)信息
    tags: List[Any] = field(default_factory=list)  # 标签列表
    card_sub_type: int = 0  # 卡片子类型
    benefit_item_create_time: int = 0  # 福利物品创建时间
    benefit_item_end_time: int = 0  # 福利物品结束时间
    montly_card_valid: bool = False  # 月卡是否有效
    appearance_id: str = "None"  # 外观ID
    appearance_type: str = "None"  # 外观类型

@dataclass
class SearchByIdListResponse(EntitiesResponse):
    """搜索ID物品响应"""
    entities: List[SearchByIdItemEntity] = field(default_factory=list)  # 搜索ID物品实体
    total: int = 0  # 搜索结果总数

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchByIdListResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entities=[SearchByIdItemEntity.from_dict(e) for e in data.get("entities", [])],
            total=data.get("total", 0)
        )

@dataclass
class Banner(Entity):
    """横幅信息"""
    id: int = 0  # 横幅ID
    name: str = ""  # 横幅名称
    banner_type: int = 0  # 横幅类型
    member_type: int = 0  # 会员类型
    pic_list: Dict[str, str] = field(default_factory=dict)  # 图片URL字典
    jump_type: str = ""  # 跳转类型
    jump_target: str = ""  # 跳转目标
    begin_time: int = 0  # 开始时间戳
    end_time: int = 0  # 结束时间戳
    banner_source: str = ""  # 横幅来源
    sort_score: int = 0  # 排序分数
    version_limit: str = ""  # 版本限制
    is_recommend_banner: int = 0  # 是否推荐横幅 (0-否, 1-是)
    target: str = ""  # 目标信息
    target_extra: Optional[str] = None  # 额外目标信息

@dataclass
class BannerListEntity(Entity):
    """横幅列表实体"""
    resource_center: List[Banner] = field(default_factory=list)  # 资源中心横幅列表
    vip: List[Any] = field(default_factory=list)  # VIP横幅列表
    star_show: List[Any] = field(default_factory=list)  # 明星展示列表
    wechat: Optional[Any] = None  # 微信相关信息
    campaign_id: int = 0  # 活动ID
    tag: int = 0  # 标签信息

@dataclass
class GetBannerListResponse(EntityResponse):
    """获取横幅列表响应"""
    entity: BannerListEntity = field(default_factory=BannerListEntity)  # 横幅列表实体
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetBannerListResponse":
        """反序列化方法，处理嵌套实体"""
        entity_data = data.get("entity", {})
        data_dict = entity_data.get("data", {})
        
        # 解析resource_center列表
        resource_center = [
            Banner(
                id=item.get("id", 0),
                name=item.get("name", ""),
                banner_type=item.get("banner_type", 0),
                member_type=item.get("member_type", 0),
                pic_list=item.get("pic_list", {}),
                jump_type=item.get("jump_type", ""),
                jump_target=item.get("jump_target", ""),
                begin_time=item.get("begin_time", 0),
                end_time=item.get("end_time", 0),
                banner_source=item.get("banner_source", ""),
                sort_score=item.get("sort_score", 0),
                version_limit=item.get("version_limit", ""),
                is_recommend_banner=item.get("is_recommend_banner", 0),
                target=item.get("target", ""),
                target_extra=item.get("target_extra")
            ) for item in data_dict.get("resource_center", [])
        ]
        
        # 创建BannerListEntity实体
        banner_data = BannerListEntity(
            resource_center=resource_center,
            vip=data_dict.get("vip", []),
            star_show=data_dict.get("star_show", []),
            wechat=data_dict.get("wechat"),
            campaign_id=data_dict.get("campaign_id", 0),
            tag=data_dict.get("tag", 0)
        )
        
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=banner_data
        )

@dataclass
class TopicListEntity(Entity):
    """主题列表实体"""
    data: List[Dict[str, Any]] = field(default_factory=list)  # 主题实体列表
    count: int = 0  # 主题总数

@dataclass
class GetTopicListResponse(EntityResponse):
    """获取主题列表响应"""
    entity: TopicListEntity = field(default_factory=TopicListEntity)  # 主题列表数据实体

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetTopicListResponse":
        entity_data = data.get("entity", {})
        topic_list_data = TopicListEntity(
            data=entity_data.get("data", []),
            count=entity_data.get("count", 0)
        )
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=topic_list_data
        )

@dataclass
class RecommendItemTagEntity(Entity):
    """推荐项目标签实体"""
    tag: str = ""  # 标签名称
    iid_list: List[str] = field(default_factory=list)  # 项目ID列表

@dataclass
class QueryRecommendItemTagResponse(EntityResponse):
    """查询推荐项目标签响应"""
    entity: RecommendItemTagEntity = field(default_factory=RecommendItemTagEntity)  # 推荐项目标签实体
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QueryRecommendItemTagResponse":
        """反序列化方法"""
        entity_data = data.get("entity", {})
        
        # 创建RecommendItemTagEntity实体
        tag_entity = RecommendItemTagEntity(
            tag=entity_data.get("tag", ""),
            iid_list=entity_data.get("iid_list", [])
        )
        
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=tag_entity
        )

@dataclass
class RecentPlayItemEntity(Entity):
    """最近游玩物品实体"""
    item_id: str = ""  # 物品唯一ID
    first_type: int = 0  # 一级分类ID (1=地图, 2=模组/组件, 6=玩法等)
    second_type: int = 0  # 二级分类ID (在一级分类下的细分)
    pic_tag_state: int = 0  # 图片标签状态 (0=无特殊标记)
    res_name: str = ""  # 资源名称
    res_size: str = ""  # 资源大小 (字节数)
    res_md5: str = ""  # 资源MD5校验值
    stars: float = 0.0  # 星级评分 (0-5分)
    download_num: str = "0"  # 总下载次数
    week_download_num: str = "0"  # 本周下载次数
    points: int = 0  # 积分价格
    diamond: int = 0  # 钻石价格
    res_version: int = 0  # 资源版本号
    is_item_time_limit: int = 0  # 是否限时物品 (0=永久, 1=限时)
    item_remain_time: int = 0  # 物品剩余时间 (秒)
    buy_state: int = 0  # 购买状态 (0=未购买, 1=已购买)
    goods_state: int = 0  # 商品状态 (1=正常上架)
    status: int = 0  # 物品状态 (1=正常)
    skin_body_type: int = 0  # 皮肤体型类型 (0=默认)
    title_image_url: str = ""  # 标题图片URL
    title_image_version: int = 0  # 标题图片版本
    resource_packs_version: str = ""  # 资源包版本 (格式: "主,次,修订")
    behavior_packs_version: str = ""  # 行为包版本 (格式: "主,次,修订")
    lobby_tag: List[int] = field(default_factory=list)  # 大厅标签ID列表
    rel_iid: str = "0"  # 相关物品ID
    is_competitive: int = 0  # 是否为竞技类物品 (0=否, 1=是)
    adv_obtain_num: int = 0  # 广告获取次数
    discount: int = 100  # 折扣百分比 (100=原价)
    vip_discount: int = 100  # VIP折扣百分比
    is_vip_benefit: int = 0  # 是否为VIP福利 (0=否, 1=是)
    pay_channel: str = ""  # 支付渠道 ("netease"=网易支付)
    product_id: str = ""  # 产品ID
    is_recommend: int = 0  # 是否为推荐物品 (0=否, 1=是)
    rec_info: List[Any] = field(default_factory=list)  # 推荐信息列表
    remark_num: int = 0  # 评论数量
    is_top: int = 0  # 是否置顶 (0=否, 1=是)
    is_joint: int = 0  # 是否为联合物品 (0=否, 1=是)
    sell_tags: List[Any] = field(default_factory=list)  # 销售标签列表
    rebate_activity_id: str = "0"  # 返利活动ID ("0"=无活动)
    is_ea: int = 0  # 是否为EA(早期访问)物品 (0=否, 1=是)
    season_mod_id: str = "0"  # 赛季模组ID ("0"=非赛季模组)
    entity_id: str = ""  # 实体ID (通常与item_id相同)
    vip_only: bool = False  # 是否仅限VIP
    season_begin: int = 0  # 赛季开始时间戳
    rebate_max_num: int = 0  # 返利最大数量
    rebate_discount_num: int = 0  # 返利折扣数量
    playing_uuid: str = ""  # 游玩UUID (游戏内加载用)
    behaviour_uuid: str = ""  # 行为UUID (游戏内加载用)
    is_sync: int = 0  # 是否同步 (0=不同步, 1=同步)
    performance_score: float = 0.0  # 性能评分 (0-5分)
    playability_score: float = 0.0  # 可玩性评分 (0-5分)
    creativity_score: float = 0.0  # 创意评分 (0-5分)
    visual_score: float = 0.0  # 视觉效果评分 (0-5分)
    score_player_num: int = 0  # 参与评分玩家数量
    performance_distribution: Dict[str, int] = field(default_factory=dict)  # 性能评分分布 (1-5分对应人数)
    playability_distribution: Dict[str, int] = field(default_factory=dict)  # 可玩性评分分布
    creativity_distribution: Dict[str, int] = field(default_factory=dict)  # 创意评分分布
    visual_distribution: Dict[str, int] = field(default_factory=dict)  # 视觉效果评分分布
    score_trend_json: Dict[str, Dict[str, float]] = field(default_factory=dict)  # 评分趋势数据
    effect_mtypeid: int = 0  # 特效主类型ID (0=无特效)
    effect_stypeid: int = 0  # 特效子类型ID (0=无特效)
    cur_num: int = 0  # 当前数量
    discount_end_time: int = 0  # 折扣结束时间戳
    mod_version: str = ""  # 模组版本号
    non_support_mod_versions: str = ""  # 不支持的模组版本
    rarity: int = 0  # 稀有度 (0=普通)
    is_lottery_reward: bool = False  # 是否为抽奖奖励
    is_persona: int = 0  # 是否为人格物品 (0=否, 1=是)
    lottery_id: int = 0  # 抽奖ID (0=无抽奖)
    persona_mtypeid: int = 0  # 人格主类型ID
    persona_stypeid: int = 0  # 人格子类型ID
    suit_id: str = "0"  # 套装ID
    dyeing: str = ""  # 染色信息
    tBuy: int = 0  # 购买时间戳
    tExpire: int = 0  # 过期时间戳
    activity_only: int = 0  # 是否仅活动可用 (0=否, 1=是)
    pic_url_list: List[str] = field(default_factory=list)  # 详情图片URL列表
    video_info_list: List[Any] = field(default_factory=list)  # 视频信息列表
    developer_name: str = ""  # 开发者名称
    developer_urs: str = ""  # 开发者URS账号
    exchange_type: int = 0  # 兑换类型 (0=不可兑换)
    is_wish: int = 0  # 是否在愿望单 (0=否, 1=是)
    refund_info: Dict[str, Any] = field(default_factory=dict)  # 退款信息
    is_official_item: int = 0  # 是否为官方物品 (0=否, 1=是)
    pvp: bool = False  # 是否支持PVP
    demo_id: str = "0"  # 演示ID ("0"=无演示)
    vanity_number: str = ""  # 虚数编号
    normal_number: str = ""  # 普通编号
    perf_params: Optional[Union[Dict[str, Any], Any]] = "None"  # 性能参数 (字典或JSON字符串)

@dataclass
class GetRecentPlayItemResponse(EntitiesResponse):
    """获取最近游玩物品响应"""
    entities: List[RecentPlayItemEntity] = field(default_factory=list)  # 物品实体列表
    total: int = 0  # 物品总数
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetRecentPlayItemResponse":
        """反序列化方法"""
        entities_data = data.get("entities", [])
        
        # 解析每个物品实体
        entities = []
        for item in entities_data:
            entities.append(RecentPlayItemEntity.from_dict(item))
        
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entities=entities,
            total=data.get("total", 0)
        )

@dataclass
class WishListItem(Entity):
    """愿望单物品实体"""
    iid: str = ""  # 物品唯一ID
    create_time: int = 0  # 加入愿望单的时间戳

@dataclass
class WishListEntity(Entity):
    """愿望单实体"""
    data: List[str] = field(default_factory=list)  # 物品ID列表
    count: int = 0  # 愿望单物品总数
    src_data: List[WishListItem] = field(default_factory=list)  # 详细的愿望单物品列表
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WishListData":
        """自定义反序列化方法，处理嵌套实体"""
        # 处理src_data列表
        src_data = []
        for item in data.get("src_data", []):
            src_data.append(WishListItem(
                iid=item.get("iid", ""),
                create_time=int(item.get("create_time", 0))
            ))
        
        return cls(
            data=data.get("data", []),
            count=data.get("count", 0),
            src_data=src_data
        )

@dataclass
class GetWishListResponse(EntityResponse):
    """获取愿望单响应"""
    entity: WishListEntity = field(default_factory=WishListEntity)  # 愿望单数据实体
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetWishListResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=WishListEntity.from_dict(data.get("entity", {}))
        )

@dataclass
class DownloadInfoEntity(Entity):
    """下载信息实体"""
    entity_id: str = ""  # 实体ID
    res_url: str = ""  # 资源下载地址
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DownloadInfoEntity":
        """反序列化方法"""
        return cls(
            entity_id=data.get("entity_id", ""),
            res_url=data.get("res_url", "")
        )

@dataclass
class GetDownloadInfoResponse(EntityResponse):
    """获取下载信息响应"""
    entity: DownloadInfoEntity = field(default_factory=DownloadInfoEntity)  # 下载信息实体
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetDownloadInfoResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=DownloadInfoEntity.from_dict(data.get("entity", {}))
        )
