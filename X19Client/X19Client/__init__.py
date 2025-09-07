from . import interfaces
from .network import NetEaseClientProxyX19
from .interfaces import __all__ as interface_name
X19Interfaces = []
for interface_name in interface_name:
    X19Interfaces.append(getattr(interfaces, interface_name))

class X19Client(*X19Interfaces, NetEaseClientProxyX19):
    pass