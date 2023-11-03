import dpkt
import json

def find_word (word, text):
    if word in text:
        print(text)

def find_header(word, dic):
    for key, val in dic.items():
        if word in key:
            print(key,':', val)
        elif word in val:
            print(key, ':', val)

def find_object(word, obj):
    memdic = json.loads(obj)
    for key, val in memdic.items():
        if word in key:
            print(key, ':', val)
        elif word in val:
            print(key,':',val)


s = 'secret'

f = open('ass1_1.pcap', 'rb')
pcap = dpkt.pcap.Reader(f)

for timestamp, data in pcap:
    #convert to link layer object
    eth = dpkt.ethernet.Ethernet(data)

    if not isinstance(eth.data, dpkt.ip.IP) and not isinstance(eth.data, dpkt.ip6.IP6):
        continue

    #get network layer content
    ip = eth.data

    if not isinstance(ip.data, dpkt.tcp.TCP):
        continue

    #get transport layer 
    tcp = ip.data

    if not len(tcp.data) > 0:
        continue

    if tcp.dport == 80:
        try:
            http = dpkt.http.Request(tcp.data)
            find_word(s, http.method)
            find_word(s, http.version)
            find_word(s, http.uri)
            find_header(s, http.headers)
            find_object(s, http.body)
           
        except:
            pass
