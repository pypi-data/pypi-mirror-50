"""
:author: Gatsby Lee
:since: 2019-08-01
"""

import json
import time

ALLOWED_PROXY_INFO_TYPE = (list, tuple,)


class ProxyIP(object):

    NO_PROXY_IP = 'noproxyip'

    __slots__ = [
        'proxy_id',
        'proxy_ip',
        'proxy_port',
        'proxy_username',
        'proxy_pwd',
        'last_request_time',
        'num_ok_requests',
        'num_banned_requests',
        'num_timedout_requests',
        'counted',
        'request_ip',
    ]

    def __init__(self,
                 proxy_ip, proxy_port, proxy_username, proxy_pwd, request_ip,
                 proxy_id=-1, last_request_time=-1, num_ok_requests=0,
                 num_banned_requests=0, num_timedout_requests=0, counted=0):
        """
        Init ProxyIP object
        """
        self.proxy_id = proxy_id
        self.proxy_ip = proxy_ip
        self.proxy_port = proxy_port
        self.proxy_username = proxy_username
        self.proxy_pwd = proxy_pwd
        self.last_request_time = last_request_time
        self.num_ok_requests = num_ok_requests
        self.num_banned_requests = num_banned_requests
        self.num_timedout_requests = num_timedout_requests
        self.counted = counted
        self.request_ip = request_ip

    def __str__(self):
        masked_pwd = '*' * len(self.proxy_pwd)
        return ("ProxyIP(proxy_ip='%s', proxy_port=%s, request_ip='%s', proxy_id=%s, \
num_ok_requests=%s, num_banned_requests=%s, num_timedout_requests=%s, \
proxy_username='%s', proxy_pwd='%s', counted=%s)") % (
            self.proxy_ip, self.proxy_port, self.request_ip, self.proxy_id,
            self.num_ok_requests, self.num_banned_requests, self.num_timedout_requests,
            self.proxy_username, masked_pwd, self.counted)

    @classmethod
    def create_from_tuple(cls, proxyip_info):
        """
        Create ProxyIP object with proxyip_info

        Args:
            proxyip_info: (tuple)
        Return
            ProxyIP object
        """
        return ProxyIP(
            proxy_id=proxyip_info[0],
            proxy_ip=proxyip_info[1],
            proxy_port=proxyip_info[2],
            proxy_username=proxyip_info[3],
            proxy_pwd=proxyip_info[4],
            last_request_time=proxyip_info[5],
            num_ok_requests=proxyip_info[6],
            num_banned_requests=proxyip_info[7],
            num_timedout_requests=proxyip_info[8],
            counted=proxyip_info[9],
            request_ip=proxyip_info[10],
        )

    @classmethod
    def create_noproxy(cls):
        """
        Create ProxyIP object with proxyip_info

        Args:
            proxyip_info: (tuple)
        Return
            ProxyIP object
        """
        return ProxyIP(
            proxy_id=-1,
            proxy_ip=cls.NO_PROXY_IP,
            proxy_port=-1,
            proxy_username=cls.NO_PROXY_IP,
            proxy_pwd=cls.NO_PROXY_IP,
            request_ip=cls.NO_PROXY_IP,
        )

    def reset_stats(self):
        self.num_ok_requests = 0
        self.num_banned_requests = 0
        self.num_timedout_requests = 0
        self.counted = 0
        self.last_request_time = -1

    def set_banned(self):
        self.last_request_time = int(time.time())
        self.num_ok_requests = 0
        self.num_banned_requests = 1
        self.num_timedout_requests = 0
        self.counted = 0

    def is_partially_used(self, threshold):
        """
        Args:
            threshold: int
        Return:
            bool
        """
        return self.num_ok_requests < threshold \
            and self.num_banned_requests == 0 \
            and self.num_timedout_requests == 0

    def is_noproxy(self):
        return self.proxy_ip == self.NO_PROXY_IP

    def serialize_proxy(self):
        """
        Return JSON serialized one
        """
        proxy_tuple = (
            self.proxy_id,
            self.proxy_ip,
            self.proxy_port,
            self.proxy_username,
            self.proxy_pwd,
            self.last_request_time,
            self.num_ok_requests,
            self.num_banned_requests,
            self.num_timedout_requests,
            self.counted,
            self.request_ip,
        )
        return json.dumps(proxy_tuple)

    def bad_proxy_str(self):
        """
        Return JSON serialized one
        """
        proxy_tuple = (
            self.proxy_id,
            self.proxy_ip,
            self.proxy_port,
            self.proxy_username,
            self.proxy_pwd,
            self.last_request_time,
            self.request_ip
        )
        return json.dumps(proxy_tuple)

    def timedout_proxy_str(self):
        """
        Return JSON serialized one
        """
        proxy_tuple = (
            self.proxy_id,
            self.proxy_ip,
            self.proxy_port,
            self.proxy_username,
            self.proxy_pwd,
            self.last_request_time,
            self.request_ip
        )
        return json.dumps(proxy_tuple)
