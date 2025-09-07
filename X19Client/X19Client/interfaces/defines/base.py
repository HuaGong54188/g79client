import json
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field

class Entity:
    """实体基类，提供序列化和反序列化的基础方法"""
    def to_dict(self) -> Dict[str, Any]:
        """通用递归序列化方法，将实体对象转换为字典"""
        result = {}
        for key, value in self.__dict__.items():
            # 递归处理嵌套的实体对象
            if isinstance(value, Entity):
                result[key] = value.to_dict()
            # 递归处理列表中的实体对象
            elif isinstance(value, list):
                result[key] = [
                    item.to_dict() if hasattr(item, "to_dict") else item
                    for item in value
                ]
            # 递归处理字典中的实体对象
            elif isinstance(value, dict):
                result[key] = {
                    k: v.to_dict() if hasattr(v, "to_dict") else v
                    for k, v in value.items()
                }
            else:
                result[key] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Entity":
        """基础反序列化方法（子类需覆盖）"""
        return cls(**data)

@dataclass
class Response(Entity):
    """API响应基类"""
    code: int  # 响应状态码 (0表示成功，其他表示错误)
    message: str  # 响应消息 (简要描述操作结果)
    details: str  # 响应详情 (提供更详细的错误或状态信息)

@dataclass
class EntityResponse(Response):
    """包含单个实体的响应基类"""
    entity: Entity  # 响应的主要实体数据
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EntityResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entity=Entity.from_dict((data.get("entity", {}) or {}))
        )

@dataclass
class EntitiesResponse(Response):
    """包含多个实体的响应基类"""
    entities: List[Entity] = field(default_factory=list)  # 实体列表
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EntitiesResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            entities=[Entity.from_dict(e) for e in data.get("entities", [])]
        )

@dataclass
class SummaryMD5EntityResponse(Response):
    """包含摘要MD5的响应基类"""
    summary_md5: str = ""  # 摘要MD5值 (用于数据校验)
    entity: Entity = field(default_factory=Entity)  # 主要实体数据
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SummaryMD5EntityResponse":
        """反序列化方法"""
        return cls(
            code=data.get("code", -1),
            message=data.get("message", ""),
            details=data.get("details", ""),
            summary_md5=data.get("summary_md5", ""),
            entity=Entity.from_dict((data.get("entity", {}) or {}))
        )
