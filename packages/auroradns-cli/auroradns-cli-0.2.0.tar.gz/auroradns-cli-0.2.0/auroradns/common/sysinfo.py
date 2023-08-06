#!/usr/bin/env python3
import ipaddress
import os
import pycurl
import socket
import sys
import tldextract


class Sysinfo:
    def __init__(self):
        self.inetaddr = {"ipv6": None, "ipv4": None}
        self.set_inetaddr(self.inetaddr)

        self.hostname = {"domain": None, "fqdn": None, "short": None}
        self.set_hostname()

    def set_inetaddr(self, inet_families):
        for inet_family in inet_families:
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, "https://ip-addr.net/")
            curl.setopt(pycurl.USERAGENT, u"AuroraDNS CLI")

            if inet_family == "ipv4":
                curl.setopt(pycurl.IPRESOLVE, pycurl.IPRESOLVE_V4)

            result = curl.perform_rs().rstrip("\n\r")

            if ipaddress.ip_address(result).version == 6:
                self.inetaddr["ipv6"] = ipaddress.IPv6Address(result)
            elif ipaddress.ip_address(result).version == 4:
                self.inetaddr["ipv4"] = ipaddress.IPv4Address(result)

    def set_hostname(self):
        try:
            sys.stderr = open(os.devnull, "w")
            ext = tldextract.extract(socket.gethostname())
            sys.stderr = sys.__stderr__
            self.hostname["fqdn"] = ".".join(ext).lower()
            self.hostname["domain"] = ".".join(ext[1:]).lower()
            self.hostname["short"] = ext[0].lower()
        except Exception as e:
            sys.exit("Error getting hostname: {}".format(e))


def main():
    sysinfo = Sysinfo()
    for key, value in sysinfo.hostname.items():
        print("{0}: {1}".format(key, value))
    for key, value in sysinfo.inetaddr.items():
        print("{0}: {1}".format(key, value))


if __name__ == "__main__":
    main()
