#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import zlib
import base64
import hashlib
import binascii
import textwrap
import xmltodict
import requests
import arrow
import OpenSSL.crypto
from M2Crypto import X509, RSA


def gzencode(text):
    gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
    return gzip_compress.compress(text) + gzip_compress.flush()


def gzdecode(text):
    return zlib.decompress(text, zlib.MAX_WBITS | 16)


def md5(text):
    m = hashlib.md5()
    m.update(text)
    return m.digest()


def load_certificate(cert_path):
    cf = file(cert_path)
    ls = []
    for l in cf.readlines():
        if len(l) > 64:
            for x in (textwrap.wrap(l, 64)):
                ls.append(x + '\r\n')
        else:
            ls.append(l)
    return ''.join(ls)


def read_certificate(cert_path):
    cf = file(cert_path)
    ls = []
    for l in cf.readlines():
        if not l.startswith('-----'):
            ls.append(l)
    return ''.join(ls).replace("\r\n", "").replace("\r", "").replace("\n", "")


def rsa_encrypt(data, cert_path):
    cert = X509.load_cert_string(load_certificate(cert_path))
    pub_key = cert.get_pubkey()
    rsa_key = pub_key.get_rsa()
    bs = rsa_key.public_encrypt(data, RSA.pkcs1_padding)
    return base64.b64encode(bs)


def rsa_verify(content, signature, cert_path):
    cert = X509.load_cert_string(load_certificate(cert_path))
    pub_key = cert.get_pubkey()
    pub_key.reset_context(md='sha1')
    pub_key.verify_init()
    pub_key.verify_update(md5(content.encode('utf8')))
    return pub_key.verify_final(base64.b64decode(signature))


def sign_content(data, cert_path, password):
    p12 = OpenSSL.crypto.load_pkcs12(open(cert_path, 'rb').read(), password)
    key = p12.get_privatekey()
    return OpenSSL.crypto.sign(key, data, 'sha1')


class Head(object):

    def __init__(self, version, charset):
        self.version = version
        self.charset = charset

    def __repr__(self):
        return '<head><version>{0}</version><charset>{1}</charset></head>'.format(self.version, self.charset)


class Info(object):

    def __init__(self, mchtId, mchtBatchNo):
        self.mchtId = mchtId
        self.mchtBatchNo = mchtBatchNo

    def __repr__(self):
        return '<info><mchtId>{0}</mchtId><mchtBatchNo>{1}</mchtBatchNo></info>'.format(self.mchtId, self.mchtBatchNo)


class Record(object):

    def __init__(self, mchtOrderNo, accountNo, accountName, accountType, bankNo, bankName, amt, purpose='', remark=''):
        self.mchtOrderNo = mchtOrderNo
        self.accountNo = accountNo
        self.accountName = accountName
        self.accountType = accountType
        self.bankNo = bankNo
        self.bankName = bankName
        self.amt = amt
        self.purpose = purpose
        self.remark = remark

    def __repr__(self):
        return '<record><mchtOrderNo>{0}</mchtOrderNo><accountNo>{1}</accountNo><accountName>{2}</accountName><accountType>{3}</accountType><bankNo>{4}</bankNo><bankName>{5}</bankName><amt>{6}</amt><purpose>{7}</purpose><remark>{8}</remark></record>'.format(self.mchtOrderNo, self.accountNo, self.accountName, self.accountType, self.bankNo, self.bankName, self.amt, self.purpose, self.remark)


class Body(object):

    def __init__(self, info, records=None):
        self.info = info
        self.records = records

    def __repr__(self):
        records_xml = ''
        if self.records and len(self.records) > 0:
            records_xml = '<records>'
            for r in self.records:
                records_xml += repr(r)
            records_xml += '</records>'
        return '<body>' + repr(self.info) + records_xml + '</body>'


class Envelope(object):

    def __init__(self, head, body):
        self.head = head
        self.body = body

    def __repr__(self):
        return '<envelope>' + repr(self.head) + repr(self.body) + '</envelope>'


class Sign(object):

    def __init__(self, signType, certificate, signContent):
        self.signType = signType
        self.certificate = certificate
        self.signContent = signContent

    def __repr__(self):
        return '<sign><signType>{0}</signType><certificate>{1}</certificate><signContent>{2}</signContent></sign>'.format(self.signType, self.certificate, self.signContent)


class Request(object):

    def __init__(self, envelope, sign):
        self.envelope = envelope
        self.sign = sign

    def __repr__(self):
        return '<request>' + repr(self.envelope) + repr(self.sign) + '</request>'


class AgentPay(object):

    def __init__(self, payUrl, queryUrl, mchtId, tlPublicKeyFile, mchtPublicKeyFile, mchtPrivateKeyFile, mchtPrivateKeyPassword):
        self.payUrl = payUrl
        self.queryUrl = queryUrl
        self.mchtId = mchtId
        self.tlPublicKeyFile = tlPublicKeyFile
        self.mchtPublicKeyFile = mchtPublicKeyFile
        self.mchtPrivateKeyFile = mchtPrivateKeyFile
        self.mchtPrivateKeyPassword = mchtPrivateKeyPassword

    # def add_record(self, mchtOrderNo, accountNo, accountName, accountType, bankNo, bankName, amt, purpose='', remark=''):
    #     accountNo = rsa_encrypt(accountNo, self.tlPublicKeyFile)
    #     accountName = rsa_encrypt(accountName, self.tlPublicKeyFile)
    #     record = Record(mchtOrderNo, accountNo, accountName, accountType, bankNo, bankName, amt, purpose, remark)
    #     self.records.append(record)

    def make_pay_request(self, mchtBatchNo, records):
        # 加密帐号姓名
        if records is not None:
            for record in records:
                record.accountNo = rsa_encrypt(record.accountNo, self.tlPublicKeyFile)
                record.accountName = rsa_encrypt(record.accountName, self.tlPublicKeyFile)

        head = Head('v1.0.7.1', 'UTF-8')
        info = Info(self.mchtId, mchtBatchNo)
        body = Body(info, records)
        envelope = Envelope(head, body)
        # 生成请求内容文档
        envelope_xml = repr(envelope)
        signContent = sign_content(envelope_xml, self.mchtPrivateKeyFile, self.mchtPrivateKeyPassword)
        signContent = binascii.hexlify(bytearray(signContent)).upper()
        certificate = read_certificate(self.mchtPublicKeyFile)
        sign = Sign(1, certificate, signContent)
        request = Request(envelope, sign)
        return repr(request)

    def make_query_request(self, mchtBatchNo):
        head = Head('v1.0.7.5', 'UTF-8')
        info = Info(self.mchtId, mchtBatchNo)
        body = Body(info)
        envelope = Envelope(head, body)
        # 生成请求内容文档
        envelope_xml = repr(envelope)
        signContent = sign_content(envelope_xml, self.mchtPrivateKeyFile, self.mchtPrivateKeyPassword)
        signContent = binascii.hexlify(bytearray(signContent)).upper()
        certificate = read_certificate(self.mchtPublicKeyFile)
        sign = Sign(1, certificate, signContent)
        request = Request(envelope, sign)
        return repr(request)


    def send_request(self, url, data):
        data = base64.b64encode(gzencode(data))
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post(url, headers=headers, data=data)
        if r.status_code == 200:
            response_xml = gzdecode(base64.b64decode(r.text)).decode('utf-8')
            if self.verify_response(response_xml):
                return response_xml
            else:
                # 签名失败
                # pass
                print "签名失败"
        else:
            # 请求失败
            pass

    def verify_response(self, response_xml):
        envelope_xml = response_xml[response_xml.index('<envelope>'):response_xml.index('</envelope>') + 11]
        signContent = response_xml[response_xml.index('<signContent>') + 13:response_xml.index('</signContent>')]
        verify = rsa_verify(envelope_xml, signContent, self.tlPublicKeyFile)
        if verify == 1:
            return True
        else:
            return False

    def pay(self, mchtBatchNo, records):
        request_xml = self.make_pay_request(mchtBatchNo, records)
        print request_xml
        response_xml = self.send_request(self.payUrl, request_xml)
        print response_xml
        if response_xml is not None:
            return request_xml, response_xml

    def query(self, mchtBatchNo):
        request_xml = self.make_query_request(mchtBatchNo)
        response_xml = self.send_request(self.queryUrl, request_xml)
        if response_xml is not None:
            return request_xml, response_xml


if __name__ == '__main__':
    # url = "http://221.133.244.5:443/gateway/batch/agentpay"
    # agent = AgentPay(url, '103000314120004',
    # '/Users/shadOw/Downloads/TLCertReal.cer',
    # '/Users/shadOw/Downloads/103000314120004.cer',
    # '/Users/shadOw/Downloads/103000314120004.pfx',
    # '111111')

    payUrl = "http://101.231.189.62:10080/gateway/batch/agentpay"
    queryUrl = "http://101.231.189.62:10080/gateway/batch/agentpayQuery"
    agent = AgentPay(payUrl, queryUrl, '100020091218008',
                     '/Users/shadOw/Downloads/TLCert.cer',
                     '/Users/shadOw/Downloads/test.cer',
                     '/Users/shadOw/Downloads/teststore.pfx', '111111')
    now = arrow.now()
    mchtBatchNo = 'BM-' + now.format('YYYYMMDDhhmmss')
    mchtOrderNo = 'BMDetail-' + now.format('YYYYMMDDhhmmss')

    record = Record(mchtOrderNo, '6225880209595231', '林博', 'PERSONAL', '308', '招商银行', 1)

    # request_xml, response_xml = agent.pay(mchtBatchNo, [record])
    # print request_xml
    # print response_xml.encode('utf8')
    # response = xmltodict.parse(response_xml)
    # code = response['response']['envelope']['body']['info']['responseCode']
    # print code
    # if code == 'E0000':
    #     print "成功"
    # else:
    #     print response['response']['envelope']['body']['info']['responseMsg']

    request_xml, response_xml = agent.query('BM-FD0912105130088398')
    print request_xml
    print response_xml.encode('utf8')
    response = xmltodict.parse(response_xml)
    code = response['response']['envelope']['body']['info']['responseCode']
    print code
    if code == 'E0000':
        print "成功"
    else:
        print response['response']['envelope']['body']['info']['responseMsg']
