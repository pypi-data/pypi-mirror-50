
.. image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. image:: https://badge.fury.io/py/be-proxy-ip.svg
    :target: https://pypi.org/project/be-proxy-ip/

.. image:: https://img.shields.io/travis/Gatsby-Lee/be-proxy-ip.svg
   :target: https://travis-ci.org/Gatsby-Lee/be-proxy-ip


BE Proxy IP
===========

Defining Proxy IP object


How to install
--------------

.. code-block:: bash

    pip install be-proxy-ip


How to init ProxyIP object
--------------------------

Using ProxyIP init
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    >>> from be_proxy_ip import ProxyIP
    >>> p = ProxyIP(proxy_ip='1.2.3.4',
    ....    proxy_port=8888,
    ....    proxy_username='hello',
    ....    proxy_pwd='doyouknow',
    ....    request_ip='1.2.3.4')
    >>> print(p)
    ProxyIP(proxy_ip='1.2.3.4', proxy_port=8888, request_ip='1.2.3.4', proxy_id=-1, num_ok_requests=0, num_banned_requests=0, num_timedout_requests=0, proxy_username='hello', proxy_pwd='*********', counted=0)


Using ProxyIP.create_from_tuple
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Order in PROXY_INFO tuple

0. proxy_id
1. proxy_ip
2. proxy_port
3. proxy_username
4. proxy_pwd
5. last_request_time
6. num_ok_requests
7. num_banned_requests
8. num_timedout_requests
9. counted
10. request_ip

.. code-block:: python

    >>> PROXY_INFO = [
    ...     1, '1.2.3.4', 3999, 'hello-proxy', 'hellop-proxy-pwd',
    ...     -1, 11, 22, 33, 44, '4.5.6.7'
    ... ]
    >>> from be_proxy_ip import ProxyIP
    >>> p = ProxyIP.create_from_tuple(PROXY_INFO)
    >>> print(p)
    ProxyIP(proxy_ip='1.2.3.4', proxy_port=3999, request_ip='4.5.6.7', proxy_id=1, num_ok_requests=11, num_banned_requests=22, num_timedout_requests=33, proxy_username='hello-proxy', proxy_pwd='****************', counted=44)
