#! /usr/bin/env python
# _*_ coding: UTF-8 _*_


import socket


class udp_client(object):
    """
    DESCRIPTION
    ===========
    This class controls UDP transport between XFFTS and GIGABYTE PC.

    ARGUMENTS
    =========
    1. host      : Host name of XFFTS.
         Type    : str or 'xxx.xxx.xxx.xxx'
         Default : 'localhost'
    2. port      : Port number of XFFTS.
         Type    : int
         Default : 16210
    3. bufsize   : Buffer size.
         Type    : int
         Default : 16*1024
    4. print     : Whether to print massage on terminal or not.
         Type    : True or False
         Default : True
    """
    def __init__(self, host='localhost', port=16210, print=True, bufsize=16*1024):
        self.host = host
        self.port = port
        self.print = print
        self.bufsize = bufsize
        self.open()
        pass

    # Base func
    # ---------
    def open(self):
        """
        Open UDP connection.
        --------------------
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return self.sock

    def close(self):
        """
        Close UDP connection.
        ---------------------
        """
        self.sock.close()
        self.sock = None
        return self.sock

    def send(self, msg):
        """
        Send input massage to XFFTS.
        ----------------------------
        """
        if self.print:
            print('SEND> {0}'.format(msg))
        msg += '\n'
        ret = self.sock.sendto(bytes(msg, 'utf8'), (self.host, self.port))
        return ret

    def recv(self, byte=16*1024):
        """
        Receive return massage from XFFTS.
        ----------------------------------
        """
        ret = self.sock.recv(byte)
        if self.print:
            print('RECV> {0}'.format(ret))
        return ret

    # XFFTS Methods
    # -------------
    def start(self):
        """
        RPG:XFFTS:START
        ---------------
        Start measurement in first phase.
        """
        self.send('RPG:XFFTS:START')
        return self.recv(self.bufsize)

    def stop(self):
        """
        XFFTS:STOP
        ----------
        Stop measurement (after last phase).
        """
        self.send('RPG:XFFTS:STOP')
        return self.recv(self.bufsize)

    def abort(self):
        """
        XFFTS:ABORT
        -----------
        Abort measurement after current phase.
        """
        self.send('RPG:XFFTS:ABORT')
        return self.recv(self.bufsize)

    def configure(self):
        """
        XFFTS:CONFIGURE
        ---------------
        Configure FFTS; activate all commanded settings.
        """
        self.send('RPG:XFFTS:CONFIGURE')
        return self.recv(self.bufsize)

    def initialize(self):
        """
        XFFTS:INITSYNTHESIZER
        ---------------------
        Initialize all FFTS on-board synthesizer.
        """
        self.send('RPG:XFFTS:INITSYNTHESIZER')
        return self.recv(self.bufsize)

    # XFFTS Properties -----
    def query_state(self):
        """
        XFFTS:STATE
        -----------
        FFTS state: ENABLED, DISABLED.
        """
        self.send('RPG:XFFTS:STATE')
        return self.recv(self.bufsize)

    """
    def set_state_enabled(self):
        self.send('RPG:XFFTS:STATE ENABLED')
        return self.recv(self.bufsize)

    def set_state_disabled(self):
        self.send('RPG:XFFTS:STATE DISABLED')
        return self.recv(self.bufsize)
    """

    def query_blanktime(self):
        """
        XFFTS:BLANKTIME
        ---------------
        Get Blank time in us.
        """
        """
        :return:
        """
        self.send('RPG:XFFTS:BLANKTIME')
        ret = self.recv(self.bufsize)
        return int(ret.split()[1])

    def set_blanktime(self, usec):
        """
        RPG:XFFTS:CMDBLANKTIME <num>
        --------------------------
        Set new Blank time in us, min. 1 ms.
        """
        if usec < 1000:
            print('ERROR:MINIMUM BLANKTIME IS 1000 [us]')
            return self.query_blanktime()
        self.send('RPG:XFFTS:CMDBLANKTIME {0}'.format(usec))
        ret = self.recv(self.bufsize)
        blanktime = int(ret.split()[1])
        return blanktime

    def query_synctime(self):
        """
        XFFTS:SYNCTIME
        -------------
        Get Sync time in us.
        """
        self.send('RPG:XFFTS:SYNCTIME')
        ret = self.recv(self.bufsize)
        return int(ret.split()[1])

    def set_synctime(self, usec):
        """
        XFFTS:CMDSYNCTIME <num>
        -----------------------
        Set new Sync time in us, range 100 ms – 5 s.
        """
        if usec < 100000:
            print('ERROR:MINIMUM SYNCTIME IS 100,000 [us]')
            return self.query_synctime()
        self.send('RPG:XFFTS:CMDSYNCTIME {0}'.format(usec))
        ret = self.recv(self.bufsize)
        blanktime = int(ret.split()[1])
        return blanktime

    def query_numphases(self):
        """
        XFFTS:NUMPHASES
        ---------------
        Get number of Blank/Sync Phases.
        """
        self.send('RPG:XFFTS:NUMPHASES')
        ret = self.recv(self.bufsize)
        result = int(ret.split()[1])
        return result

    def set_numphases(self, phase):
        """
        XFFTS:CMDNUMPHASES
        ------------------
        Get new number of Phases, range 1 – 4 Phases.

        < phase : [1,4] >
        """
        self.send('RPG:XFFTS:CMDNUMPHASES {0}'.format(phase))
        ret = self.recv(self.bufsize)
        result = int(ret.split()[1])
        return result

    def query_mode(self):
        """
        XFFTS:MODE
        ----------
        Blank/Sync mode: INTERNAL or EXTERNAL
        """
        self.send('RPG:XFFTS:MODE')
        ret = self.recv(self.bufsize)
        result = ret.split()[1]
        return result

    def set_mode(self, mode):
        """
        XFFTS:CMDMODE <mode>
        --------------------
        Set Blank/Sync mode to INTERNAL or EXTERNAL

        < mode = INTERNAL | EXTERNAL>
        """
        self.send('RPG:XFFTS:CMDMODE %s'.format(mode))
        return self.recv(self.bufsize)

    def query_usedsections(self):
        """
        XFFTS:USEDSECTIONS
        ------------------
        Display which FFTS-Boards (sections) are selected to transmit spectra via TCP protocol.
        """
        self.send('RPG:XFFTS:USEDSECTIONS')
        ret = self.recv(self.bufsize)
        ret = ret.split()[1:-1]
        ret_int = list(map(int, ret))
        return ret_int

    def set_usedsections(self, section):
        """
        XFFTS:CMDUSEDSECTIONS <list>
        ----------------------------
        Select FFTS-Boards which are allowed to transmit spectra via TCP protocol

        < section : list : Length = any >
        """
        """
        if len(section)!=32:
            section += [0] * (32-len(section))
            pass
        """
        self._used = section
        section_str = ' '.join(map(str, section))
        self.send('RPG:XFFTS:CMDUSEDSECTIONS {0}'.format(section_str))
        return self.recv(self.bufsize)

    def query_version(self):
        """
        XFFTS:VERSION
        -------------
        Get FFTS software version number.
        """
        self.send('RPG:XFFTS:VERSION')
        ret = self.recv(self.bufsize)
        return ret.split()[1]

    def release_date(self):
        """
        XFFTS:RELEASE
        -------------
        Get FFTS release date.
        """
        self.send('RPG:XFFTS:RELEASE')
        ret = self.recv(self.bufsize)
        return ret.split()[1]

    def caladc(self):
        """
        XFFTS:CALADC
        ------------
        (re-)calibrate the ADC interleaving of all ADCs
        """
        self.send('RPG:XFFTS:CALADC')
        return self.recv(self.bufsize)

    def info(self, n):
        """
        XFFTS:INFO <num>
        ----------------
        Display FFTS-Board information for board n (n: 1..x)
        (Maybe) The information is not returned to UDP client but on FFTS window.
        """
        self.send('RPG:XFFTS:INFO {0}'.format(n))
        ret = self.recv(self.bufsize)
        return int(ret.split()[1])

    def dump(self, n):
        """
        XFFTS:DUMP <num>
        ----------------
        Dump out m spectra from selected boards via TCP
        """
        self.send('RPG:XFFTS:DUMP {0}'.format(n))
        return self.recv(self.bufsize)

    def saveadcdelays(self):
        """
        XFFTS:SAVEADCDELAYS
        -------------------
        Save all ADC delays in file “ADCdelay.data”
        """
        #self.send('RPG:XFFTS:SAVEADCDELAYS')
        #return self.recv(self.bufsize)
        pass

    def loadadcdelays(self):
        """
        XFFTS:LOADADCDELAYS
        -------------------
        (re-)load ADC delays from file “ADCdelay.data”
        """
        #self.send('RPG:XFFTS:LOADADCDELAYS')
        #return self.recv(self.bufsize)
        pass

    # Band dependent command
    # ----------------------
    def query_board_numspecchan(self, n):
        """
        XFFTS:BANDn:NUMSPECCHAN
        -----------------------
        Get number of spectral channels
        """
        self.send('RPG:XFFTS:BAND{0}:NUMSPECCHAN'.format(n))
        ret = self.recv(self.bufsize)
        numspecchan = int(ret.split()[1])
        return numspecchan

    def set_board_numspecchan(self, n, chan):
        """
        XFFTS:BANDn:CMDNUMSPECCHAN <num>
        --------------------------------
        Set number of spectral channels (only power of two values are allowed: 8192, 4096, 2048, ...)
        """
        self.send('RPG:XFFTS:BAND{0}:CMDNUMSPECCHAN {1}'.format(n, chan))
        ret = self.recv(self.bufsize)
        numspecchan = int(ret.split()[1])
        return numspecchan

    def query_board_bandwidth(self, n):
        """
        XFFTS:BANDn:BANDWIDTH
        ---------------------
        Get bandwidth [MHz] of FFTS-Board n
        """
        self.send('RPG:XFFTS:BAND{0}:BANDWIDTH'.format(n))
        ret = self.recv(self.bufsize)
        return float(ret.split()[1])

    def set_board_bandwidth(self, n, width):
        """
        XFFTS:BANDn:CMDBANDWIDTH
        ------------------------
        Set bandwidth [MHz].
        Possible bandwidth depends on the FPGA core. Default: 2500 MHz
        """
        self.send('RPG:XFFTS:BAND{0}:CMDBANDWIDTH {1}'.format(n, width))
        ret = self.recv(self.bufsize)
        bandwidth = ret.split()[1]
        if bandwidth == 'ERROR':
            return 'ERROR:INVALID_BAND MONEY!!'
        else:
            return float(bandwidth)

    def query_board_mirrorspectra(self, n):
        """
        XFFTS:BANDn:MIRRORSPECTRA
        -------------------------
        Get “mirror spectra” info: 0:mirror off (default)/ 1:mirror on (e.g. for even Nyquist zone sampling)
        """
        self.send('RPG:XFFTS:BAND{0}:MIRROSPECTRA'.format(n))
        ret = self.recv(self.bufsize)
        if ret.split()[1] == '0':
            result = 'MIRROR OFF'
            pass
        elif ret.split()[1] == '1':
            result = 'MIRROR ON'
            pass
        else:
            result = 'ERROR:INVALID_BAND'
            pass
        return result

    def set_board_mirrorspectra(self, n, switch):
        """
        XFFTS:BANDn:CMDMIRRORSPECTRA
        ----------------------------
        Set “mirror spectra”: 0:mirror off / 1:mirror on (e.g. for even Nyquist zone sampling)
        """
        self.send('RPG:XFFTS:BAND{0}:CMDMIRROSPECTRA {1}'.format(n, switch))
        return self.recv(self.bufsize)

    def board_caladc(self, n):
        """
        XFFTS:BANDn:CALADC
        ------------------
        Calibrate/optimize ADC interleaving
        """
        self.send('RPG:XFFTS:BAND{0}:CALADC'.format(n))
        return self.recv(self.bufsize)

    def board_adcdelay(self, n):
        """
        XFFTS:BANDn:ADCDELAY
        --------------------
        Depending on the FPGA core and the total bandwidth, the timing between the ADC and FPGA has to be adjusted.
        For the default core and 2.5 GHz bandwidth, this command is more or less obsolete.
        """
        self.send('RPG:XFFTS:BAND{0}:ADCDELAY'.format(n))
        ret = self.recv(self.bufsize)
        delay = float(ret.split()[1])
        return delay

    def query_board_time(self, n):
        """
        XFFTS:BANDn:TIME
        ----------------
        Get GPS/IRIG-B time and date
        """
        self.send('RPG:XFFTS:BAND{0}:TIME'.format(n))
        ret = self.recv(self.bufsize)
        time = ret.split()[1]
        return time

    def query_board_temperature(self, n):
        """
        XFFTS:BANDn:TEMPERATURE
        -----------------------
        Get FFTS-Board temperatures in °C for the ADC, FPGA and power supplies
        """
        self.send('RPG:XFFTS:BAND{0}:TEMPERATURE'.format(n))
        ret = self.recv(self.bufsize)
        temp = list(map(float, [ret.split()[1], ret.split()[2], ret.split()[3]]))
        return temp

    def query_all_temperature(self):
        all_temp = []
        for i, used in enumerate(self.query_usedsections()):
            if used == 1:
                ret = self.query_board_temperature(i+1)
                all_temp.append(ret)
            else:
                all_temp.append(None)
                pass
            continue
        return all_temp

    def board_specfilter(self, n):
        """
        XFFTS:BANDn:SPECFILTER
        ----------------------
        Due to the ADC interleaving,
        a narrow interference line (birdie) can appear
        in one frequency bin exactly in the middle of the band.
        Mostly, this birdie can be minimized by calibrating the ADCs
        after they reached the finalstable temperature, e.g. 5 minutes.
        If not, the command SPECFILTER 2 divides the total bandwidth
        in 2 parts and remove the birdie by interpolating between
        the direct neighbor bins of both parts.
        The SPECFILTER can also be defined in the FFTS configure file: FFTS.cfg.
        """
        self.send('RPG:XFFTS:BAND{0}:SPECFILTER'.format(n))
        ret = self.recv(self.bufsize)
        return int(ret.split()[1])


# Written by Y.Kozuki
# Modified by T.Inaba
