# WatchGhost, your invisible but loud monitoring pet
# Copyright © 2015 Kozea

import logging
import socket
import ssl
from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse, urlunparse

import aiohttp
from aioftp import Client as AsyncFTPClient
from aioftp import StatusCodeError

from .command import Run


class TCPConnector(aiohttp.TCPConnector):
    def _wrap_create_connection(self, *args, **kwargs):
        ssl = kwargs.get('ssl')
        if ssl and hasattr(ssl, 'hostname'):
            kwargs['server_hostname'] = ssl.hostname
        return super()._wrap_create_connection(*args, **kwargs)


class SSLContext(ssl.SSLContext):
    """SSL context with an explicit server hostname."""
    def wrap_socket(self, *args, **kwargs):
        if hasattr(self, 'hostname'):
            kwargs['server_hostname'] = self.hostname
        return super().wrap_socket(*args, **kwargs)


class Ping:
    """Probe pinging a server.

    This needs a 'ping' command installed.

    Specific configuration keys:

    - ip_version: call using IPv4 (4) or IPv6 (6)

    """
    config = {
        'repeat': 60,
        'timeout': 3,
        'ip_version': 4,
        'ping_command': 'ping',
        'ping6_command': 'ping -6'
    }

    @staticmethod
    async def check(server, config):
        if "command" not in config:
            if config['ip_version'] == 4:
                ping = config['ping_command'].split(' ')
            else:
                ping = config['ping6_command'].split(' ')
            timeout = '-W{}'.format(config['timeout'])
            ip = server.config.get('ipv{}'.format(config['ip_version']))
            if not ip:
                return {
                    "ok": False,
                    'timeout': False,
                    "message": "missing ip",
                }
            config['command'] = ping + ['-c1', timeout, ip]

        return await Run.check(server, config)


class HTTP:
    """Probe sending HTTP requests.

    Specific configuration keys:

    - ip_version: call using IPv4 (4) or IPv6 (6)
    - url: URL of the request sent to the HTTP server

    """
    config = {
        'repeat': 60,
        'timeout': 5,
        'url': '',
        'ip_version': 4,
        'status': OrderedDict([
            ('error', [{'ok': False}] + [
                {'code': i} for i in range(400, 432)
            ]),
            ('warning', [{'code': i} for i in range(300, 308)]),
            ('info', [{'code': i} for i in range(200, 226)]),
            ('critical', [{'code': i} for i in range(500, 512)]),
        ]),
    }

    @staticmethod
    async def check(server, config):
        """Send a HTTP request and check the response.

        Specific keys returned:

        - status: HTTP status of the response

        """
        url_parts = urlparse(
            config['url'].format(now=datetime.now(timezone.utc)))
        hostname = url_parts.hostname

        if url_parts.scheme == 'https':
            context = SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.hostname = hostname
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
            context.load_default_certs()
        else:
            context = None

        port, username, password = (
            url_parts.port, url_parts.username, url_parts.password)
        url_parts = list(url_parts)

        if not config.get('request_hostname'):
            if config.get('ip_version') == 6:
                url_parts[1] = '[{}]'.format(server.config['ipv6'])
            else:
                url_parts[1] = server.config['ipv4']
            if port:
                url_parts[1] += ':%s' % port
        if username:
            if password:
                url_parts[1] = '%s:%s@' % (username, password) + url_parts[1]
            else:
                url_parts[1] = '%s@' % username + url_parts[1]

        url = urlunparse(url_parts)

        headers = {'Host': hostname, 'User-Agent': 'WatchGhost'}
        timeout = aiohttp.ClientTimeout(total=config['timeout'])
        result = {'url': url, 'host': hostname}

        try:
            kwargs = dict(timeout=timeout, connector=TCPConnector())
            async with aiohttp.ClientSession(**kwargs) as session:
                response = await session.get(
                    url,
                    allow_redirects=config.get('allow_redirects', False),
                    headers=headers,
                    ssl=context,
                )
        except socket.timeout:
            result['ok'] = False
            result['message'] = 'The request timed out'
            result['timeout'] = True
        except OSError as e:
            result['ok'] = False
            result['message'] = str(e)
            result['timeout'] = False
        except aiohttp.ClientError as e:
            result['ok'] = False
            result['message'] = e.message
            result['code'] = e.code
            result['timeout'] = False
        except Exception as e:
            result['ok'] = False
            result['message'] = str(e)
            result['timeout'] = False
        else:
            result.update({
                'ok': True,
                'code': response.status,
                'timeout': False,
                'redirect': response.headers.getall('Location', []),
                'message': 'Status code is {}'.format(
                    response.status or 'unknown'
                )
            })
            if config.get('get_info'):
                try:
                    result['info'] = await response.json()
                except Exception:
                    result['info'] = None
        return result


class FTP:
    """Probe sending FTP requests.

    Currently only works with IPv4.

    Specific configuration keys:

    - url: URL of the request sent to the FTP server

    """
    config = {
        'repeat': 60,
        'timeout': 5,
        'ip_version': 4,
        'url': '',
    }

    # Deactivate barbarian logging
    logging.getLogger('aioftp.client').setLevel(1000)

    @staticmethod
    async def check(server, config):
        url_parts = urlparse(
            config['url'].format(now=datetime.now(timezone.utc)))
        response = {
            "ok": True, "message": "OK", 'path_exists': None, 'timeout': False
        }

        if config.get('ip_version') == 6:
            host = '[{}]'.format(server.config['ipv6'])
        else:
            host = server.config['ipv4']

        try:
            client = AsyncFTPClient(
                socket_timeout=config['timeout'],
                path_timeout=config['timeout']
            )
            await client.connect(host)
            if url_parts.username or url_parts.password:
                await client.login(url_parts.username, url_parts.password)
            else:
                await client.login("anonymous", "anonymous")

            command = 'NLST {}'.format(url_parts.path)
            async with client.get_stream(command, ('1xx', '2xx')) as stream:
                path_exists = bool((await stream.read()).strip())
            if not path_exists:
                response['ok'] = False
                response['message'] = "Path does not exists"
            client.close()
        except TimeoutError as e:
            response['ok'] = False
            response['message'] = 'Timeout' + e.message
            response['timeout'] = True
        except StatusCodeError as e:
            response['ok'] = False
            response['message'] = e.info
        except Exception as e:
            response['ok'] = False
            response['message'] = str(e)
        return response


class SecuredSocket:
    config = {
        'repeat': 60,
        'ip_version': 4,
        'hostname': '',
        'port': 443,
        'minimum_days_left': 30,
        'status': OrderedDict([
            ('error', [
                {'hostname_verified': False},
                {"in_period": False},
                {'connected': False},
            ]),
            ('warning', [{'enough_days_left': False}]),
            ('info', [{}]),
        ]),
    }

    @staticmethod
    async def check(server, config):
        result = {
            'hostname_verified': None,
            'in_period': None,
            'enough_days_left': None,
            'connected': None,
        }

        if config.get('ip_version') == 6:
            host = '[{}]'.format(server.config['ipv6'])
        else:
            host = server.config['ipv4']

        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        conn = context.wrap_socket(
            socket.socket(socket.AF_INET), server_hostname=config['hostname'],
        )
        try:
            conn.connect((host, config['port']))
            result['connected'] = True
        except (ssl.CertificateError, ssl.SSLError) as e:
            conn.close()
            result['hostname_verified'] = False
            result['message'] = str(e)
            return result
        except ConnectionRefusedError as e:
            result['connected'] = False
            result['message'] = str(e)
            return result

        result['hostname_verified'] = True

        cert = conn.getpeercert()

        not_after_timestamp = ssl.cert_time_to_seconds(cert['notAfter'])
        not_before_timestamp = ssl.cert_time_to_seconds(cert['notBefore'])
        not_after = datetime.utcfromtimestamp(not_after_timestamp)
        not_before = datetime.utcfromtimestamp(not_before_timestamp)
        now = datetime.utcnow()
        result['in_period'] = not_before < now < not_after
        result['enough_days_left'] = (
            not_after - now > timedelta(days=config['minimum_days_left'])
        )

        return result


class SSH:
    config = {
        'command': [],
        'status': OrderedDict([
            ('error', [{'exit_code': 2}]),
            ('warning', [{'exit_code': 1}]),
            ('info', [{'exit_code': 0}]),
        ]),
    }

    @staticmethod
    async def check(server, config):
        process = await server.ssh_command(config['command'])
        result = await process.wait(False)
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'exit_code': result.exit_status,
            'ok': result.exit_status == 0,
        }
