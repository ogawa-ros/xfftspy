# xfftspy

## Installation
`pip install xfftspy`


## Usage

    >>> import xfftspy

    # initialize XFFTS boards
    >>> cmd = xffts.udp_client(host='localhost')
    >>> cmd.stop()
    >>> cmd.set_synctime(100000)          # synctime : 100 ms
    >>> cmd.set_usedsections([1])         # use board : 1
    >>> cmd.set_board_bandwidth(1, 2500)  # bandwidth : 2500 MHz
    >>> cmd.configure()                   # apply settings
    >>> cmd.caladc()                      # calibrate ADCs
    >>> cmd.start()                       # start measurement
    
    # receive spectra
    >>> rcv = xffts.data_consumer(host='localhost')
    >>> rcv.clear_buffer()
    >>> rcv.receive_once()
    