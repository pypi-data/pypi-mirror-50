from be_proxy_ip.__about__ import __version__
from be_proxy_ip.proxy_ip import ProxyIP


def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value


VERSION = tuple(map(int_or_str, __version__.split('.')))


__all__ = (
    '__version__',
    'VERSION',
    'ProxyIP',
)
