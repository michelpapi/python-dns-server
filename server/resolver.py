
from records import *


def create_response(data):
    request = DNSRecord.parse(data)
    reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
    qname = request.q.qname
    qn = str(qname).strip('.')
    qtype = request.q.qtype
    qt = QTYPE[qtype]

    print('{} Q: {}/{}'.format(time.asctime(), qname, qt))

    if qn not in records:
        reply.header.set_rcode(RCODE.NXDOMAIN)
    else:
        for rdata in resolve(qn):
            rqt = rdata.__class__.__name__
            if qt in ['*', rqt]:
                reply.add_answer(RR(rname=qname, rtype=qtype, rclass=1, ttl=TTL, rdata=rdata))
            elif rqt == 'CNAME':
                for cn_rdata in resolve(str(rdata.label)):
                    rqt = cn_rdata.__class__.__name__
                    if qt in ['*', rqt]:
                        reply.add_answer(
                            RR(rname=qname, rtype=qtype, rclass=1, ttl=TTL, rdata=cn_rdata))
    return reply.pack()


def resolve(qn):
    return records[qn.strip('.')]


