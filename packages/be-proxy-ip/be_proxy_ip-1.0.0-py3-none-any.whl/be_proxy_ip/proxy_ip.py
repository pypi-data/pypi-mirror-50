"""
:author: Gatsby Lee
:since: 2019-08-01
"""

import json
import time

ALLOWED_PROXY_INFO_TYPE = (list, tuple,)


class ProxyIP(object):

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

    def __init__(self, proxy_info):
        """
        Init ProxyIP object

        Args:
            proxy_info: list, tuple, or serialized JSON
        """

        if type(proxy_info) in ALLOWED_PROXY_INFO_TYPE:
            proxy_info_tuple = proxy_info
        else:
            proxy_info_tuple = json.loads(proxy_info)
        self.proxy_id = proxy_info_tuple[0]
        self.proxy_ip = proxy_info_tuple[1]
        self.proxy_port = proxy_info_tuple[2]
        self.proxy_username = proxy_info_tuple[3]
        self.proxy_pwd = proxy_info_tuple[4]
        self.last_request_time = proxy_info_tuple[5]
        self.num_ok_requests = proxy_info_tuple[6]
        self.num_banned_requests = proxy_info_tuple[7]
        self.num_timedout_requests = proxy_info_tuple[8]
        self.counted = proxy_info_tuple[9]
        self.request_ip = proxy_info_tuple[10]

    def __repr__(self):
        return 'proxy_id: %s, proxy_ip: %s, proxy_request_ip : %s, ok_ct: %s, banned_ct: %s, timedout_ct: %s' % (
            self.proxy_id, self.proxy_ip, self.request_ip, self.num_ok_requests,
            self.num_banned_requests, self.num_timedout_requests)

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
