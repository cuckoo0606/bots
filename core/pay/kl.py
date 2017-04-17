# -*- coding: utf-8 -*-
import base64
import time
import requests
import xmltodict
from hashlib import md5
from urllib import quote
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class Record(object):

    def __init__(self, mchtId, mchtOrderNo, accountNo, accountName, accountType, bankNo, bankName, amt, remark=''):
        self.mchId = mchtId
        self.mchtOrderNo = mchtOrderNo
        self.accountNo = accountNo
        self.accountName = accountName
        self.accountType = accountType
        self.bankNo = bankNo
        self.bankName = bankName
        self.amt = amt
        self.remark = remark


class AgentPay(object):

    def __init__(self, mchtId, payUrl, notifyUrl, keyFile):

        self.mchId = mchtId
        self.payUrl = payUrl
        self.notifyUrl = notifyUrl
        self.keyFile = keyFile

    def pay(self, record):

        request_xml = self.make_pay_request(record)
        response_xml = self.send_request(request_xml)
        return response_xml

    def make_pay_request(self, record):

        orderDateTime = time.strftime('%Y%m%d%H%M%S')
        body = '<envelope><head><version>v1.0.7.6</version><charset>UTF-8</charset></head><body>' \
               '<mchtId>{0}</mchtId><mchtOrderNo>{1}</mchtOrderNo><accountNo>{2}</accountNo>' \
               '<accountName>{3}</accountName><accountType>{4}</accountType><bankNo>{5}</bankNo>' \
               '<bankName>{6}</bankName><amt>{7}</amt><remark>{8}</remark><notifyUrl>{9}</notifyUrl>' \
               '<orderDateTime>{10}</orderDateTime></body></envelope>'\
            .format(self.mchId, record.mchtOrderNo, record.accountNo, record.accountName, record.accountType,
                    record.bankNo, record.bankName, record.amt, record.remark, self.notifyUrl, orderDateTime)
        signature = self.sign(body)

        return '<request>{0}<sign><signType>1</signType><certificate></certificate><signContent>{1}</signContent>' \
               '</sign></request>'.format(body, signature)

    def send_request(self, request_xml):

        print request_xml
        data = quote(base64.b64encode(request_xml))
        req = requests.post(self.payUrl+'?reqMsg='+data)
        if req.status_code == 200:
            response_xml = base64.b64decode(req.text)
            res_dict = xmltodict.parse(response_xml)
            # print 'res_dict', res_dict
            if res_dict['response']['envelope']['body']['responseCode'] == 'E0000':
                print res_dict
                return res_dict

            else:
                # 签名失败
                # pass
                print res_dict['response']['envelope']['body']['responseMsg']
                return res_dict
        else:
            print '请求失败'
            # 请求失败
            pass

    def sign(self, body):

        try:
            with open(self.keyFile) as f:
                privkey = f.read()
                key = RSA.importKey(privkey)
                h = SHA.new(md5(body).digest())
                signer = PKCS1_v1_5.new(key)
                signature = signer.sign(h)
                return base64.b64encode(signature)
        except Exception, e:
            print e

if __name__ == '__main__':
    payUrl = 'https://pg.openepay.com/gateway/singleagentpay'
    notifyUrl = 'http://120.76.188.10:8888'
    agent = AgentPay('105850170110002', payUrl, notifyUrl, '/Users/kangxiaomin/Downloads/firmhwy/xghq/private.key')
    record = Record('105850170110002', '000000000000000025', '6214832013135665', 'test', 'PERSONAL', '308581002136', '招商银行', '10')
    pay = agent.pay(record)

