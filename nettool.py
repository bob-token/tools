import sys
import re
import time
import logging
from logging.handlers import RotatingFileHandler
from subprocess import call

def fillter_hex_to_str(hex,count):
    raw1 = hex.replace("0x", "")
    return raw1.zfill(count)

def ip_to_raw_hex(ip):
    d = ip.split('.')
    d1 = int(d[0])
    d2 = int(d[1])
    d3 = int(d[2])
    d4 = int(d[3])
    dd = d4<<24|d3<<16|d2<<8|d1
    raw1 = str(hex(dd))
    return fillter_hex_to_str(raw1,8)

def raw_hex_to_ip_port(rawHex):
    ip = rawHex.split(":")[0]
    port = rawHex.split(":")[1]
    return raw_hex_to_ip(ip)+":"+raw_hex_to_decimal(port)

def raw_hex_to_decimal(rawHex):
    return str(eval("0x"+rawHex))

def raw_hex_to_ip(rawHex):
    d1 = rawHex[0:2]
    d2 = rawHex[2:4]
    d3 = rawHex[4:6]
    d4 = rawHex[6:8]
    t1 = raw_hex_to_decimal(d4)
    t2 = raw_hex_to_decimal(d3)
    t3 = raw_hex_to_decimal(d2)
    t4 = raw_hex_to_decimal(d1)
    return  t1 +"."+t2+"."+t3+"."+t4

def socketState(code):
    stat = {'01':'TCP_ESTABLISHED',
            '02': 'TCP_SYC_SENT',
            '03': 'TCP_SYC_RECV',
            '04': 'TCP_FIN_WAIT1',
            '05': 'TCP_FIN_WAIT2',
            '06': 'TCP_TIME_WAIT',
            '07': 'TCP_CLOSE',
            '08': 'TCP_CLOSE_WAIT',
            '09': 'TCP_LAST_ACK',
            '0A': 'TCP_LISTEN',
            '0B': 'TCP_CLOSING'
            }
    return stat.get(code,"EUNKONWN_CODE")

def localAddress(dict):
    return dict['local_address']

def remAddress(dict):
    return dict['rem_address']

def rxQueue(dict):
    return raw_hex_to_decimal(dict['rx_queue'])

def txQueue(dict):
    return raw_hex_to_decimal(dict['tx_queue'])


def parseLine(line):
    sl="0"
    local_address="127.0.0.1:80"
    rem_address="127.0.0.1:80"
    st="0A"
    tx_queue="00000000"
    rx_queue="00000000"
    tr=""
    tm_when=""
    retrnsmt=""
    uid=""
    timeout=""
    inode=""
    chunks = re.split(' +', line)
    sl = chunks[0].replace(":","")
    if sl=='sl':
        return "",False


    tx_queue = chunks[4].split(':')[0]
    rx_queue = chunks[4].split(':')[1]
    tr=chunks[5].split(':')[0]
    tm_when = chunks[5].split(':')[1]
    dict = {'sl':chunks[0],
            "local_address":raw_hex_to_ip_port(chunks[1]),
            'rem_address':raw_hex_to_ip_port(chunks[2]),
            "st":socketState(chunks[3]),
            'tx_queue':tx_queue,
            "rx_queue":rx_queue,
            'tr':tr,
            "tm_when":tm_when,
            "retrnsmt":chunks[6],
            "uid":chunks[7],
            "timeout":chunks[8],
            "inode":chunks[9]}

    # logger.info(dict)
    return dict,True


def tcpInfo(ipPort):
    # logger.info(ipPort)
    with open('/proc/net/tcp') as file:
        for line in file.readlines():
            if -1 != line.find(ipPort.upper()):
                line = line.rstrip()
                line = line.lstrip()
                logger.info(line)
                parseLine(line)


def local_monitor(ipPort):
    ip = ipPort.split(":")[0]
    port = ipPort.split(":")[1]
    rawIp = ip_to_raw_hex(ip)
    rawPort = fillter_hex_to_str(str(hex(int(port))),4)
    objStr = rawIp+":"+rawPort
    tcpInfo(objStr)


def sort_send_queue(topCount,length):
    with open('/proc/net/tcp') as file:
        for line in file.readlines():
            line = line.rstrip()
            line = line.lstrip()
            dict,err = parseLine(line)
            if not err:
                continue
            rl = dict['tx_queue']
            if int(txQueue(dict)) > length:
                logger.info("local:"+localAddress(dict)+
                            " remote:"+remAddress(dict)+
                            " tx_queue:"+txQueue(dict)+
                            " rx_queue:"+rxQueue(dict)
                            )



if __name__ == '__main__':

    call('awk \'{print $6}\' monitor_tcp.log | awk - F \':\' \'{print $2}\' | sort - n')
    logger = logging.getLogger('monitor_tcp')
    hdlr = RotatingFileHandler('monitor_tcp.log', mode='a', maxBytes=5 * 1024 * 1024,
                        backupCount=2, encoding=None, delay=0)
    # hdlr = logging.FileHandler('monitor_tcp.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    while(1):
        for i in sys.argv[1:]:
            # local_monitor(i)
            sort_send_queue(10,10000)
        time.sleep(1)


