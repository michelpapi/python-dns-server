from dnslib import *

records = {
    'example.com': [A('1.1.1.1'), AAAA((0,) * 16), SOA(), MX('mail.example.com.'), NS('ns1.example.com.'),
                     NS('ns2.example.com.')],
    'www.example.com': [CNAME('example.com.'), A('1.1.1.1'), A('1.1.1.2'), A('1.1.1.3')],
    'mail.example.com': [A('1.1.1.1')],
    'dev.example.com': [A('1.1.1.1')],
    'ns1.example.com': [A('1.1.1.1')],
    'ns2.example.com': [A('1.1.1.1')],
    '1.1.1.1.in-addr.arpa': [PTR('www.example.com')]
}

TTL = 300
