import socket
import select
from urllib.parse import urlparse


def test_con(env, charger_info, log):
    url = charger_info.CentralStationAddress

    log.info(f'Test connection to {url}...')

    url_items = urlparse(url)    
    host = url_items.hostname
    port = url_items.port or 80
    path = url_items.path + '/' + charger_info.Id

    s = None
    try:
        log.info(f'1. Open raw connection to {host}:{port}')
        s = socket.create_connection((host, port), timeout=5.0)

        log.info(f'2. Send HTTP request GET {path}')
        req_lines = [
            f'GET {path} HTTP/1.1',
            'User-Agent: tiger',
            f'Host: {host}:{port}',
            'Upgrade: WebSocket',
            'Connection: Upgrade',
            'Pragma: no-cache',
            'Cache-Control: no-cache',
            'Sec-WebSocket-Key: omf+YISYGBBTwPNsGSiWtg==',
            'Sec-WebSocket-Protocol: ocpp1.5',
            'Sec-WebSocket-Version: 13',
            '\r\n',
        ]
        s.sendall('\r\n'.join(req_lines).encode('utf-8'))
    
        fd_read, fd_write, fd_err = select.select([s], [], [], 5.0)
        if s in fd_read:
            data = s.recv(1024)
            if data:
                log.info(data)
            else:
                raise Exception('Socket closed while reading')
        else:
            raise Exception('Timeout reading')
    
    
    except Exception as ex:
        log.error(ex)

    finally:
        try:
            if s: s.close()
            s = None
        except:
            pass
