import socket
import struct
import time

import numpy as np

from .util import recv


class data_consumer(object):
    header_size = 64

    def __init__(self, host='localhost', port=25144):
        self.connect(host, port)
        pass

    def connect(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self.sock.connect((host, port))

    def close(self):
        self.sock.close()
        return

    def receive_once(self):
        header = self._receive_header()
        data = self._receive_data(header)
        return {'header': header, 'data': data}

    def _receive_header(self):
        h = recv(self.sock, self.header_size)
        now = time.time()
        mv = memoryview(h)

        header = {}
        header['ieee'] = struct.unpack_from('4s', mv, 0)[0]
        header['data_format'] = struct.unpack_from('4s', mv, 4)[0]
        header['package_length'] = struct.unpack_from('I', mv, 8)[0]
        header['BE_name'] = struct.unpack_from('8s', mv, 12)[0]
        header['timestamp'] = struct.unpack_from('28s', mv, 20)[0]
        header['integration_time'] = struct.unpack_from('I', mv, 48)[0]
        header['phase_number'] = struct.unpack_from('I', mv, 52)[0]
        header['BE_num'] = struct.unpack_from('I', mv, 56)[0]
        header['blocking'] = struct.unpack_from('I', mv, 60)[0]
        header['data_size'] = header['package_length'] - self.header_size
        header['received_time'] = now
        return header

    def _receive_data(self, header):
        rawdata = recv(self.sock, header['data_size'])
        mv = memoryview(rawdata)

        counter = 0
        data = {}
        for i in range(header['BE_num']):
            BE_num = struct.unpack_from('I', mv, counter)[0]
            ch_num = struct.unpack_from('I', mv, counter + 4)[0]
            spec = np.frombuffer(mv, dtype=np.float32, count=ch_num, offset=counter + 8)
            data[BE_num] = spec
            counter += 8 + ch_num * 4
            continue

        return data

    def clear_buffer(self):
        t0 = time.time()
        while True:
            _d = self.receive_once()
            t1 = time.time()
            if t1 - t0 > _d['header']['integration_time'] / 1e6 * 0.9:
                break
            t0 = t1
            continue
        return
