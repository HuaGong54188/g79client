# -*- encoding: utf-8 -*-
__all__ = ["User"]
from ..network import NetEaseClientProxyX19
from .defines import *
import requests
import json

class User(NetEaseClientProxyX19):
    """网易我的世界用户操作类，继承自NetEaseClientProxyX19网络客户端"""

    def QueryUserByEntityId(
        self,
        entity_id: str,
        include_detail: bool = True
    ) -> QueryUserByEntityIdResponse:
        """
        通过用户ID查询用户信息
        :param entity_id: 目标用户EntityID (必填)
        :param include_detail: 是否包含详细信息，默认True
        :return: 包含用户信息的响应对象，详细信息根据参数包含扩展数据
        """
        return QueryUserByEntityIdResponse.from_dict(self.request(
            "POST",
            "https://g79mclobt.minecraft.cn",
            "/user-detail/query/other",
            json={
                "entity_id": entity_id,
                "include_detail": include_detail
            }
        ).json())
    QueryUserByUserId = QueryUserByEntityId

    def SearchUserByNameOrMail(
        self,
        name_or_mail: str,
        search_type: int = 0,
        limit: int = 20
    ) -> SearchUserByNameOrMailResponse:
        """
        通过名称或邮箱搜索用户
        :param name_or_mail: 用户名/邮箱 (必填)
        :param search_type: 搜索类型 0-精确搜索 1-模糊搜索，默认0
        :param limit: 返回结果数量，默认20
        :return: 包含搜索结果列表的响应对象，每条结果包含用户基础信息
        """
        return SearchUserByNameOrMailResponse.from_dict(self.request(
            "POST",
            "https://g79mclobt.minecraft.cn",
            "/user-search-friend/",
            json={
                "name_or_mail": name_or_mail,
                "search_type": search_type,
                "limit": limit
            }
        ).json())

    def UpdatePersonalPageLike(
        self,
        owner_user_id: str,
        has_like: bool = True,
        visitor_user_id: str = None,
        entity_id: str = None
    ) -> UpdatePersonalPageLikeResponse:
        """
        更新个人主页点赞状态
        :param owner_user_id: 主页所有者用户ID (必填)
        :param has_like: 是否点赞
        :param visitor_user_id: 访问者用户ID (默认使用client内置用户ID)
        :param entity_id: 实体ID (默认与visitor_user_id相同)
        :return: 包含操作结果的响应对象，确认点赞状态是否更新成功
        """
        payload = {
            "personal_page_owner_user_id": owner_user_id,
            "has_like": has_like,
            "visitor_user_id": visitor_user_id or self.user_id,
            "entity_id": entity_id or (visitor_user_id or self.user_id)
        }
        return UpdatePersonalPageLikeResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewayobt.minecraft.cn",
            "/user-personal-page-like/update",
            json=payload
        ).json())

    def GetUserModDetail(
        self,
        user_id: str,
        include_statistics: bool = True
    ) -> GetUserModDetailResponse:
        """
        获取用户MOD详情
        :param user_id: 目标用户ID (必填)
        :param include_statistics: 是否包含统计信息，默认True
        :return: 包含用户MOD列表及统计信息的响应对象
        """
        return GetUserModDetailResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewayobt.minecraft.cn",
            "/user-mod-detail",
            json={
                "user_id": user_id,
                "include_statistics": include_statistics
            }
        ).json())

    def GetUserModUsageTime(
        self,
        user_id: str,
        sort_type: int = 0,
        filter_first_type: list = None,
        length: int = 10,
        offset: int = 0
    ) -> GetUserModUsageTimeResponse:
        """
        获取用户MOD使用时长
        :param user_id: 目标用户ID (必填)
        :param sort_type: 排序方式 0-时长排序 1-安装时间排序，默认0
        :param filter_first_type: 过滤类型列表，默认[4]（4表示MOD类型）
        :param length: 返回数量，默认10
        :param offset: 分页偏移量，默认0
        :return: 包含MOD使用时长排序结果的响应对象
        """
        return GetUserModUsageTimeResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewayobt.minecraft.cn",
            "/user-mod-detail/use-time",
            json={
                "user_id": user_id,
                "sort_type": sort_type,
                "filter_first_type": filter_first_type or [4],
                "length": length,
                "offset": offset
            }
        ).json())

    def ApplyFriendRequest(
        self,
        target_user_id: str,
        comment: str = "test",
        add_type: int = 5,
        message: str = "",
        add_ui: str = "个人主页"
    ) -> ApplyFriendRequestResponse:
        """
        发送好友申请
        :param target_user_id: 目标用户ID (必填)
        :param add_type: 添加方式类型 
                        5=个人主页添加 6=扫码添加 7=ID搜索添加，默认5
        :param comment: 申请人昵称（必填）
        :param message: 验证消息（发给对方的申请语），默认空
        :param add_ui: 添加来源界面标识，默认"个人主页"
        :return: 包含申请提交状态的响应对象
        """
        return ApplyFriendRequestResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewayobt.minecraft.cn",
            "/user-apply-friend/",
            json={
                "fid": target_user_id,
                "add_type": add_type,
                "comment": comment,
                "message": message,
                "add_ui": add_ui
            }
        ).json())

    def MomentReportRequest(
        self,
        msg: dict,
        type: str
    ) -> MomentReportRequestResponse:
        """
        发送用户举报
        :param msg: 举报内容 (必填，需包含具体证据信息)
        :param type: 举报类型 (必填，如"违规发言"、"恶意行为"等)
        :return: 包含举报提交结果的响应对象
        """
        return MomentReportRequestResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewayobt.minecraft.cn",
            "/user-moment-report/",
            json={
                "msg": msg,
                "type": type
            }
        ).json())

    def LikeUserTag(
        self,
        target_id: int,
        tag_id: int
    ) -> LikeUserTagResponse:
        """
        点赞用户标签
        :param target_id: 目标用户ID (必填)
        :param tag_id: 标签ID (必填)
        :return: 包含点赞操作状态的响应对象
        """
        return LikeUserTagResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewaygrayobt.nie.netease.com",
            "/user-stat/like-user-tag",
            json={
                "target_id": target_id,
                "tag_id": tag_id
            }
        ).json())

    def GetUserTagList(
        self,
        uid: str
    ) -> GetUserTagListResponse:
        """
        获取用户标签列表
        :param uid: 目标用户ID (必填)
        :return: 包含用户标签列表及标签属性的响应对象
        """
        return GetUserTagListResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewaygrayobt.nie.netease.com",
            "/user-home-page/get-tag-list",
            json={
                "uid": uid
            }
        ).json())

    def UpdateHomePageConfig(
        self,
        config_data: dict
    ) -> UpdateHomePageConfigResponse:
        """
        更新用户主页配置
        :param config_data: 配置数据 (必填，格式如 {"tag": [标签ID列表]})
        :return: 包含配置更新状态的响应对象
        """
        return UpdateHomePageConfigResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewaygrayobt.nie.netease.com",
            "/user-home-page/update-config",
            json={
                "config_data": config_data
            }
        ).json())

    def GetHomePageConfig(
        self,
        uid: str
    ) -> GetHomePageConfigResponse:
        """
        获取用户主页配置
        :param uid: 目标用户ID (必填)
        :return: 包含用户主页当前配置的响应对象
        """
        return GetHomePageConfigResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewaygrayobt.nie.netease.com",
            "/user-home-page/get-config/",
            json={
                "uid": uid
            }
        ).json())
