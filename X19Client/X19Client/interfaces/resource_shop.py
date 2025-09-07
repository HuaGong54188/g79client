# -*- encoding: utf-8 -*-
__all__ = ["ResourceShop"]
from ..network import NetEaseClientProxyX19
from .defines import *
import requests
import json

class ResourceShop(NetEaseClientProxyX19):
    """网易我的世界资源商店操作类，继承自NetEaseClientProxyX19网络客户端"""

    def GetItemDetail(
        self, 
        item_id: str, 
        channel_id: int = 5, 
        need_record: int = 0, 
        source: int = 3
    ) -> GetItemDetailResponse:
        """
        获取资源详细信息
        :param item_id: 资源唯一标识 (必填)
        :param channel_id: 渠道标识，默认5表示中国版客户端
        :param need_record: 是否需要记录访问行为，0-不记录 1-记录
        :param source: 请求来源标识，3表示常规客户端请求
        :return: 包含资源详情信息的响应对象
        """
        return GetItemDetailResponse.from_dict(self.request(
            "POST", 
            "https://g79apigatewayobt.minecraft.cn", 
            "/pe-item-detail-v2", 
            json={
                "item_id": item_id, 
                "channel_id": channel_id, 
                "need_record": need_record, 
                "source": source
            }
        ).json())

    '''
    def PurchaseItem(
        self, 
        item_id: str, 
        buy_path: str = None, 
        cdk_code: str = "", 
        component_view: str = "资源中心首页_推荐-资源中心分类列表-功能玩法-全部", 
        coupon_ids: list = None, 
        expertcomment_info: dict = None
    ) -> PurchaseItemResponse:
        """
        购买指定资源
        :param item_id: 资源唯一标识 (必填)
        :param buy_path: 购买路径追踪标识，默认自动生成
        :param cdk_code: CDK兑换码，默认为空
        :param component_view: 组件展示位置标识，用于埋点统计
        :param coupon_ids: 使用的优惠券ID列表，默认空列表
        :param expertcomment_info: 专家推荐信息字典，包含专家ID、评论ID和视频URL
        :return: 包含购买订单信息的响应对象
        """
        if buy_path is None:
            buy_path = f"首页无主城_资源中心_全部资源_功能玩法_组件详情资源中心详情页:{item_id}"
        if coupon_ids is None:
            coupon_ids = []
        if expertcomment_info is None:
            expertcomment_info = {"expert_id": "0", "expertcomment_id": "0", "video_url": "0"}
        return PurchaseItemResponse.from_dict(self.request(
            "POST", 
            "https://g79mclobt.minecraft.cn", 
            "/pe-purchase-item", 
            json={
                "buy_path": buy_path,
                "cdk_code": cdk_code,
                "component_view": component_view,
                "coupon_ids": coupon_ids,
                "expertcomment_info": expertcomment_info,
                "item_id": item_id
            }
        ).json())

    def QueryBuyResult(
        self, 
        order_id: str, 
        buy_type: int = 0
    ) -> QueryBuyResultResponse:
        """
        查询购买结果
        :param order_id: 订单唯一标识 (必填)
        :param buy_type: 购买类型，0-普通购买 1-礼包购买
        :return: 包含订单状态的响应对象
        """
        return QueryBuyResultResponse.from_dict(self.request(
            "POST", 
            "https://g79mclobt.minecraft.cn", 
            "/buy-item-result", 
            json={
                "buy_type": buy_type, 
                "orderid": order_id
            }
        ).json())
    '''

    def ExtractRecommendList(
        self, 
        channel_id: int = 5, 
        client_type: int = 1, 
        referer: int = 2
    ) -> ExtractRecommendListResponse:
        """
        获取精选推荐资源列表
        :param channel_id: 渠道标识，默认5
        :param client_type: 客户端类型，1-移动端
        :param referer: 推荐来源，2-资源中心首页
        :return: 包含推荐列表的响应对象
        """
        return ExtractRecommendListResponse.from_dict(self.request(
            "POST", 
            "https://g79mclobt.minecraft.cn", 
            "/pe-item/extract-recommend-list", 
            json={
                "channel_id": channel_id, 
                "client_type": client_type, 
                "referer": referer
            }
        ).json())

    def QueryRecommendHotSpot(
        self, 
        channel_id: int = 5
    ) -> QueryRecommendHotSpotResponse:
        """
        查询推荐热点资源
        :param channel_id: 渠道标识，默认5
        :return: 包含热点资源的响应对象
        """
        return QueryRecommendHotSpotResponse.from_dict(self.request(
            "POST", 
            "https://g79mclobt.minecraft.cn", 
            "/pe-item/query/recommend-hot-spot", 
            json={"channel_id": channel_id}
        ).json())

    def WaterFall(
        self, 
        item_ids: list, 
        channel_id: int = 5, 
        version: int = 2
    ) -> WaterFallResponse:
        """
        批量获取资源信息（瀑布流接口）
        :param item_ids: 资源ID列表 (必填)
        :param channel_id: 渠道标识，默认5
        :param version: 接口版本，当前为2
        :return: 包含批量资源信息的响应对象
        """
        return WaterFallResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewayobt.minecraft.cn",
            "/pe-item/water_fall",
            json={
                "channel_id": channel_id,
                "version": version,
                "item_ids": item_ids
            }
        ).json())

    def SearchByIdList(
        self,
        item_id_list: list,
        channel_id: int = 5,
        pe_user_item_tag: int = 1,
        resource_status: bool = True
    ) -> SearchByIdListResponse:
        """
        通过ID列表批量搜索资源
        :param item_id_list: 资源ID列表 (必填)
        :param channel_id: 渠道标识，默认5
        :param pe_user_item_tag: 用户资源标签，1-已购买
        :param resource_status: 是否筛选有效资源，True-仅返回可用资源
        :return: 包含搜索结果的响应对象
        """
        return SearchByIdListResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewayobt.minecraft.cn",
            "/pe-item/query/search-by-id-list",
            json={
                "channel_id": channel_id,
                "item_id_list": item_id_list,
                "pe_user_item_tag": pe_user_item_tag,
                "resource_status": resource_status
            }
        ).json())

    def GetBannerList(self) -> GetBannerListResponse:
        """
        获取首页轮播图列表
        :return: 包含Banner信息的响应对象
        """
        return GetBannerListResponse.from_dict(self.request(
            "GET",
            "https://g79apigatewayobt.minecraft.cn",
            "/pe-banner/get-list"
        ).json())

    def GetTopicList(
        self,
        length: int = 10,
        is_new_topic: int = 1,
        topic_type: int = 0,
        offset: int = 0
    ) -> GetTopicListResponse:
        """
        获取专题活动列表
        :param length: 请求数量，默认10
        :param is_new_topic: 是否新专题，1-是 0-否
        :param topic_type: 专题类型，0-常规专题
        :param offset: 分页偏移量，默认0
        :return: 包含专题列表的响应对象
        """
        return GetTopicListResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewayobt.minecraft.cn",
            "/pe-topic/get-list",
            json={
                "length": length,
                "is_new_topic": is_new_topic,
                "topic_type": topic_type,
                "offset": offset
            }
        ).json())

    def QueryRecommendItemTag(
        self, 
        channel_id: int = 5
    ) -> QueryRecommendItemTagResponse:
        """
        查询推荐资源标签
        :param channel_id: 渠道标识，默认5
        :return: 包含推荐标签的响应对象
        """
        return QueryRecommendItemTagResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewayobt.minecraft.cn",
            "/pe-item/query/recommend-item-tag",
            json={"channel_id": channel_id}
        ).json())

    def SearchByKeyword(
        self,
        keyword: str,
        channel_id: int = 5,
        length: int = 24,
        offset: int = 0,
        first_type: str = "0",
        second_type: str = "",
        official_skin: int = 0,
        init: int = 0
    ) -> SearchByKeywordResponse:
        """
        关键字搜索资源
        :param keyword: 搜索关键词 (必填)
        :param channel_id: 渠道标识，默认5
        :param length: 每页数量，默认24
        :param offset: 分页偏移量，默认0
        :param first_type: 一级分类ID，"0"表示全部
        :param second_type: 二级分类ID，空表示不限
        :param official_skin: 是否官方皮肤，0-不限 1-仅官方
        :param init: 是否初始化搜索，0-常规搜索 1-初始化
        :return: 包含搜索结果的响应对象
        """
        return SearchByKeywordResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewayobt.minecraft.cn",
            "/pe-item/query/search-by-keyword/",
            json={
                "second_type": second_type,
                "channel_id": channel_id,
                "length": length,
                "first_type": first_type,
                "keyword": keyword,
                "offset": offset,
                "official_skin": official_skin,
                "init": init
            }
        ).json())

    def GetRecentPlayItem(
        self,
        uid: str,
        channel_id: int = 5,
        need_record: int = 0,
        source: int = 3
    ) -> GetRecentPlayItemResponse:
        """
        获取用户最近游玩资源
        :param uid: 用户ID (必填)
        :param channel_id: 渠道标识，默认5
        :param need_record: 是否需要记录，0-否 1-是
        :param source: 来源标识，3-客户端常规请求
        :return: 包含最近游玩记录的响应对象
        """
        return GetRecentPlayItemResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewayobt.minecraft.cn",
            "/pe-item/query/get-recent-play-item",
            json={
                "channel_id": channel_id,
                "uid": uid,
                "need_record": need_record,
                "source": source
            }
        ).json())

    def GetWishList(
        self,
        uid: str,
        length: int = 5,
        first_type: str = "0",
        resource_pack_flag: int = 1,
        offset: int = 0,
        wish_type: int = 0
    ) -> GetWishListResponse:
        """
        获取用户愿望单
        :param uid: 用户ID (必填)
        :param length: 返回数量，默认5
        :param first_type: 一级分类，默认"0"表示全部
        :param resource_pack_flag: 资源包标识，1-包含资源包
        :param offset: 分页偏移量，默认0
        :param wish_type: 愿望单类型，0-普通愿望单
        :return: 包含愿望单列表的响应对象
        """
        return GetWishListResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewayobt.minecraft.cn",
            "/pe-item/wish/get_list",
            json={
                "length": length,
                "first_type": first_type,
                "resource_pack_flag": resource_pack_flag,
                "uid": uid,
                "offset": offset,
                "wish_type": wish_type
            }
        ).json())

    def GetDownloadInfo(self, item_id: str) -> GetDownloadInfoResponse:
        """
        获取资源下载信息
        :param item_id: 资源唯一标识 (必填)
        :return: 包含下载地址等信息的响应对象
        """
        return GetDownloadInfoResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewayobt.minecraft.cn",
            "/pe-download-item/get-download-info",
            json={"item_id": item_id}
        ).json())
