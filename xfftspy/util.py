


def recv(sock, nbytes, default_recv_block=65536):
    received = b''
    
    while len(received) < nbytes:
        rest = nbytes - len(received)
        if rest < default_recv_block:
            recv_block = rest
        else:
            recv_block = default_recv_block
            pass
        
        new = sock.recv(recv_block)
        if new == b'':
            # if failed to receive completely
            # then return 0 byte
            return b''
        
        received += new
        continue
    
    return received

