import urllib2
import sys


def run(server_host, server_port, filename):
    url = "http://"+server_host+":"+str(server_port)+"/"+filename
    print url
    urllib2.urlopen(url).read()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise ValueError("Usage : clientone.py <server_IP_address> <port_number> <filename>")
    host = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]
    run(host, port, filename)
