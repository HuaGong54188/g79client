# -*- encoding: utf-8 -*-
__all__ = ["RentalServer"]
from ..network import NetEaseClientProxyX19
from .defines import *
import requests
import json

class RentalServer(NetEaseClientProxyX19):
    """网易我的世界租赁服操作类，继承自NetEaseClientProxyX19网络客户端"""

    def SearchRentalServerByName(self, server_name: str) -> SearchRentalServerByNameResponse:
        """
        通过名称搜索租赁服
        :param server_name: 租赁服名称关键词 (必填)
        :return: 包含搜索结果列表的响应对象，包含匹配的租赁服基础信息
        """
        return SearchRentalServerByNameResponse.from_dict(self.request(
            "POST",
            "https://g79mclobt.minecraft.cn",
            "/rental-server/query/search-by-name",
            json={"server_name": server_name}
        ).json())

    def GetRentalServerDetails(self, server_id: str) -> GetRentalServerDetailsResponse:
        """
        获取租赁服详细信息
        :param server_id: 租赁服唯一标识 (必填)
        :return: 包含租赁服完整详情的响应对象，包括配置、状态、所有者等信息
        """
        return GetRentalServerDetailsResponse.from_dict(self.request(
            "POST",
            "https://g79mclobt.minecraft.cn",
            "/rental-server-details/get",
            json={"server_id": server_id}
        ).json())

    def GetRentalServerPlayers(
        self,
        server_id: str,
        is_online: bool = True,
        length: int = 50,
        order_type: int = 0,
        offset: int = 0,
        status: int = 0
    ) -> GetRentalServerPlayersResponse:
        """
        查询租赁服玩家数据
        :param server_id: 租赁服唯一标识 (必填)
        :param is_online: 是否仅查询在线玩家，默认为 True 表示仅查询在线玩家
        :param length: 返回的最大记录数，默认为 50
        :param order_type: 排序类型，0 表示默认排序，1 表示按最后登录时间倒序
        :param offset: 偏移量，默认为 0 表示从第一条开始
        :param status: 玩家状态，0 表示所有状态玩家
        :return: 包含玩家列表的响应对象，如果请求失败则返回 None；默认返回：
                 - 最新 50 条记录
                 - 包含所有玩家状态
                 - 按最后登录时间倒序排序
                 - 仅显示在线玩家
        """
        return GetRentalServerPlayersResponse.from_dict(self.request(
            "POST",
            "https://g79mclobt.minecraft.cn",
            "/rental-server-player/query/search-by-server",
            json={
                "status": status,  # 0-所有状态玩家
                "server_id": server_id,
                "order_type": order_type,  # 1-按最后登录时间倒序
                "is_online": is_online,  # True-仅查询在线玩家
                "length": length,  # 50-返回最多 50 条记录
                "offset": offset  # 0-从第一条开始
            }
        ).json())

    def UpdateRentalServerLike(self, server_id: str, is_like: int) -> UpdateRentalServerLikeResponse:
        """
        点赞/取消点赞租赁服
        :param server_id: 租赁服唯一标识 (必填)
        :param is_like: 点赞状态，1-点赞 0-取消点赞
        :return: 包含操作结果的响应对象
        """
        return UpdateRentalServerLikeResponse.from_dict(self.request(
            "POST",
            "https://g79mclobt.minecraft.cn",
            "/rental-server-like/update",
            json={
                "server_id": server_id,
                "is_like": is_like
            }
        ).json())

    def GetAvailableRentalServers(
        self,
        sort_type: int = 0,
        order_type: int = 0,
        offset: int = 0
    ) -> GetAvailableRentalServersResponse:
        """
        查询可用租赁服
        :param sort_type: 排序类型，0-综合 1-在线人数 2-最新 3-最受欢迎
        :param order_type: 顺序类型，0-降序 1-升序
        :param offset: 偏移量，默认为 0
        :return: 包含可用租赁服列表的响应对象
        """
        return GetAvailableRentalServersResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewayobt.minecraft.cn",
            "/rental-server/query/available-by-sort-type",
            json={
                "sort_type": sort_type,
                "order_type": order_type,
                "offset": offset
            }
        ).json())

    def EnterRentalServerWorld(self, server_id: str, password: str = "") -> EnterRentalServerWorldResponse:
        """
        进入租赁服世界
        :param server_id: 租赁服唯一标识 (必填)
        :param password: 租赁服密码，默认为空字符串（公开服可不填）
        :return: 包含连接信息的响应对象，通常包含服务器地址和连接凭证
        """
        return EnterRentalServerWorldResponse.from_dict(self.request(
            "POST",
            "https://g79apigatewayobt.minecraft.cn",
            "/rental-server-world-enter/get",
            json={
                "server_id": server_id,
                "pwd": password
            }
        ).json())
