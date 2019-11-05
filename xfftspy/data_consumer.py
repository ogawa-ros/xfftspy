
import socket
import struct
import time

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
        
        header = {}
        header['ieee'] = struct.unpack('4s', h[0:4])[0]
        header['data_format'] = struct.unpack('4s', h[4:8])[0]
        header['package_length'] = struct.unpack('I', h[8:12])[0]
        header['BE_name'] = struct.unpack('8s', h[12:20])[0]
        header['timestamp'] = struct.unpack('28s', h[20:48])[0]
        header['integration_time'] = struct.unpack('I', h[48:52])[0]
        header['phase_number'] = struct.unpack('I', h[52:56])[0]
        header['BE_num'] = struct.unpack('I', h[56:60])[0]
        header['blocking'] = struct.unpack('I', h[60:64])[0]
        header['data_size'] = header['package_length'] - self.header_size
        header['received_time'] = now
        return header

    def _receive_data(self, header):
        rawdata = recv(self.sock, header['data_size'])
        
        counter = 0
        data = {}
        for i in range(header['BE_num']):
            BE_num = struct.unpack('I', rawdata[counter:counter+4])[0]
            ch_num = struct.unpack('I', rawdata[counter+4:counter+8])[0]
            spec = struct.unpack('{}f'.format(ch_num),
                                 rawdata[counter+8:counter+8+ch_num*4])
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
