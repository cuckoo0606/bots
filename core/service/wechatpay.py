#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    from settings import WECHAT_SINGN_KEY, WECHAT_PAY_APPID, WECHAT_PAY_MCHID, WECHAT_PAY_CREATE_IP
except:
    WECHAT_SINGN_KEY = "61oETzKXQFGaYdkL5gEmGe39FuYhFEQn"
    WECHAT_PAY_APPID = "wxe4b34b117e5d52cc"
    WECHAT_PAY_MCHID = "1302574401"
    WECHAT_PAY_CREATE_IP = "114.80.201.90"

import md5
import uuid
import qrcode
import requests
import datetime
import xml.dom.minidom

# 微信固定参数
WECHAT_ORDER_URL = "https://api.mch.weixin.qq.com/pay/unifiedorder"
WECHAT_ORDER_QUERY_URL = "https://api.mch.weixin.qq.com/pay/orderquery"
WECHAT_ORDER_CLOSE_URL = "https://api.mch.weixin.qq.com/pay/closeorder"
WECHAT_REFUND_URL = "https://api.mch.weixin.qq.com/secapi/pay/refund"
WECHAT_REFUND_QUERY_URL = "https://api.mch.weixin.qq.com/pay/refundquery"
WECHAT_DOWNLOAD_BILL_URL = "https://api.mch.weixin.qq.com/pay/downloadbill"


class WeChatPay(object):
    def order(self, request):
        """
            统一下单
        """
        headers = { "content-type": "text/xml" }
        r = requests.post(WECHAT_ORDER_URL, data = repr(request), headers = headers)
        r.encoding = "utf8"

        result = OrderResult()
        result.parse(r.text.encode("utf8"))
        return result


    def query_order(self, request):
        """
            订单查询
        """
        headers = { "content-type": "text/xml" }
        r = requests.post(WECHAT_ORDER_QUERY_URL, data = repr(request), headers = headers)
        r.encoding = "utf8"

        result = QueryOrderResult()
        result.parse(r.text.encode("utf8"))
        return result


    def close_order(self, request):
        """
            关闭订单
        """
        headers = { "content-type": "text/xml" }
        r = requests.post(WECHAT_ORDER_CLOSE_URL, data = repr(request), headers = headers)
        r.encoding = "utf8"

        result = CloseOrderResult()
        result.parse(r.text.encode("utf8"))
        return result


    def refund(self, request):
        """
            申请退款
        """
        headers = { "content-type": "text/xml" }
        key = os.path.abspath("./core/service/apiclient_key.pem")
        cert = os.path.abspath("./core/service/apiclient_cert.pem")
        r = requests.post(WECHAT_REFUND_URL, data = repr(request), headers = headers, verify = ( cery, key ))
        r.encoding = "utf8"

        result = RefundResult()
        result.parse(r.text.encode("utf8"))
        return result


    def query_refund(self, request):
        """
            查询退款状态
        """
        headers = { "content-type": "text/xml" }
        r = requests.post(WECHAT_REFUND_QUERY_URL, data = repr(request), headers = headers)
        r.encoding = "utf8"

        result = QueryRefundResult()
        result.parse(r.text.encode("utf8"))
        return result


class Request(object):
    """
        微信支付接口请求基类
    """
    def __init__(self):
        # 微信分配的公众账号ID（企业号corpid即为此appId）
        # wxd678efh567hg6787
        self.appid = WECHAT_PAY_APPID
        # 微信支付分配的商户号
        # 1230000109
        self.mch_id = WECHAT_PAY_MCHID
        # 随机字符串，不长于32位。推荐随机数生成算法
        # 5K8264ILTKCH16CQ2502SI8ZNMTM67VS
        self.nonce_str = str(uuid.uuid1()).replace("-", "").upper()


    @property
    def sign(self):
        """
            签名，详见签名生成算法
        """
        return sign(self)


    def __repr__(self):
        """
            格式化成报文
        """
        keys = self.__dict__.keys()

        s = "<xml>\n"
        for k in keys:
            if self.__dict__[k]:
                s += "<{0}>{1}</{0}>\n".format(k, self.__dict__[k])
        
        s += "<sign>{0}</sign>\n".format(self.sign)
        s += "</xml>"
        return s


class Order(Request):
    """
        统一下单请求类
    """
    def __init__(self):
        # 终端设备号(门店号或收银设备ID)，注意：PC网页或公众号内支付请传"WEB"
        # 013467007045764
        self.device_info = ""
        # 商品或支付单简要描述
        # note: Ipad mini  16G  白色
        self.body = ""
        # 商品名称明细列表
        # note: Ipad mini  16G  白色
        self.detail = ""
        # 附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据
        # 深圳分店
        self.attach = ""
        # 商户系统内部的订单号,32个字符内、可包含字母, 其他说明见商户订单号
        # note: 20150806125346
        self.out_trade_no = ""
        # 符合ISO 4217标准的三位字母代码，默认人民币：CNY，其他值列表详见货币类型
        # note: CNY
        self.fee_type = ""
        # 订单总金额，单位为分，详见支付金额
        # note: 888
        self.total_fee = 0
        # APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP。
        # 123.12.12.123
        self.spbill_create_ip = WECHAT_PAY_CREATE_IP
        # 订单生成时间，格式为yyyyMMddHHmmss，如2009年12月25日9点10分10秒表示为20091225091010。其他详见时间规则
        # note: 20091225091010
        start = datetime.datetime.now()
        self.time_start = start.strftime("%Y%m%d%H%M%S")
        # 订单失效时间，格式为yyyyMMddHHmmss，如2009年12月27日9点10分10秒表示为20091227091010。其他详见时间规则
        # 注意：最短失效时间间隔必须大于5分钟
        # 20091227091010
        expire = start + datetime.timedelta(seconds = 60 * 10)
        self.time_expire = expire.strftime("%Y%m%d%H%M%S")
        # 商品标记，代金券或立减优惠功能的参数，说明详见代金券或立减优惠
        # note: WXG
        self.goods_tag = ""
        # 接收微信支付异步通知回调地址，通知url必须为直接可访问的url，不能携带参数。
        # http://www.weixin.qq.com/wxpay/pay.php
        self.notify_url = ""
        # 取值如下：JSAPI，NATIVE，APP，详细说明见参数规定
        # note: JSAPI
        self.trade_type = ""
        # trade_type=NATIVE，此参数必传。此id为二维码中包含的商品ID，商户自行定义。
        # note: 12235413214070356458058
        self.product_id = ""
        # no_credit--指定不能使用信用卡支付
        # no_credit
        self.limit_pay = ""
        # trade_type=JSAPI，此参数必传，用户在商户appid下的唯一标识。
        # openid如何获取，可参考【获取openid】。
        # 企业号请使用【企业号OAuth2.0接口】获取企业号内成员userid，再调用【企业号userid转openid接口】进行转换
        self.openid = ""
        
        super(Order, self).__init__()
    

    def __repr__(self):
        return super(Order, self).__repr__()


class QueryOrder(Request):
    """
        订单查询请求类
    """
    def __init__(self):
        # 商户系统内部的订单号，当没提供transaction_id时需要传这个。
        self.out_trade_no = ""
        # 微信的订单号，优先使用
        self.transaction_id = ""
        
        super(QueryOrder, self).__init__()


    def __repr__(self):
        return super(QueryOrder, self).__repr__()


class CloseOrder(Request):
    """
        关闭订单请求类
    """
    def __init__(self):
        # 商户系统内部的订单号
        self.out_trade_no = ""
        
        super(CloseOrder, self).__init__()


    def __repr__(self):
        return super(CloseOrder, self).__repr__()


class Refund(Request):
    """
        申请退款请求类
    """
    def __init__(self):
        # 终端设备号
        self.device_info = ""
        # 微信生成的订单号，在支付通知中有返回
        self.transaction_id = ""
        # 商户侧传给微信的订单号
        self.out_trade_no = ""
        # 商户系统内部的退款单号，商户系统内部唯一，同一退款单号多次请求只退一笔
        self.out_refund_no = ""
        # 订单总金额，单位为分，只能为整数，详见支付金额
        self.total_fee = 0
        # 退款总金额，订单总金额，单位为分，只能为整数，详见支付金额
        self.refund_fee = 0
        # 货币类型，符合ISO 4217标准的三位字母代码，默认人民币：CNY，其他值列表详见货币类型
        self.refund_fee_type = ""
        # 操作员帐号, 默认为商户号
        self.op_user_id = ""

        super(Refund, self).__init__()


    def __repr__(self):
        return super(Refund, self).__repr__()


class QueryRefund(Request):
    """
        查询退款请求类
    """
    def __init__(self):
        # 终端设备号
        self.device_info = ""
        # 微信生成的订单号，在支付通知中有返回
        self.transaction_id = ""
        # 商户侧传给微信的订单号
        self.out_trade_no = ""
        # 商户侧传给微信的退款单号
        self.out_refund_no = ""
        # 微信生成的退款单号，在申请退款接口有返回
        self.refund_id = ""

        super(QueryRefund, self).__init__()


    def __repr__(self):
        return super(QueryRefund, self).__repr__()


class DownloadBill(Request):
    """
        下载对账单
    """
    def __init__(self):
        # 终端设备号
        self.device_info = ""
        # 下载对账单的日期，格式：20140603
        self.bill_date = ""
        # ALL，返回当日所有订单信息，默认值
        # SUCCESS，返回当日成功支付的订单
        # REFUND，返回当日退款订单
        # REVOKED，已撤销的订单
        self.bill_type = "ALL"

        super(DownloadBill, self).__init__()


    def __repr__(self):
        return super(DownloadBill, self).__repr__()


class Result(object):
    def __init__(self):
        # 调用接口提交的公众账号ID
        self.appid = ""
        # 调用接口提交的商户号
        self.mch_id = ""
        # 微信返回的随机字符串
        self.nonce_str = ""
        # 微信返回的签名，详见签名算法
        self.sign = ""
        # SUCCESS/FAIL
        # 此字段是通信标识，非交易标识，交易是否成功需要查看result_code来判断
        self.return_code = ""
        # 返回信息，如非空，为错误原因
        # 签名失败
        # 参数格式校验错误
        self.return_msg = ""


    def parse(self, text):
        """
            将xml转换为结果对象
        """
        dom = xml.dom.minidom.parseString(text)
        root = dom.documentElement

        for name in self.__dict__.keys():
            nodes = root.getElementsByTagName(name)
            if nodes:
                node = nodes[0].firstChild
                if node:
                    value = ""
                    t = type(self.__dict__[name])
                    if t != str:
                        value = t(node.nodeValue.encode("utf8"))
                    else:
                        value = node.nodeValue.encode("utf8")
                    
                    self.__setattr__(name, value)


    @property
    def key_map(self):
        """
            结果类属性对应xml节点名转换关系
        """
        return {}


    def __repr__(self):
        """
            格式化成报文
        """
        keys = self.__dict__.keys()

        s = "<xml>\n"
        for k in keys:
            if self.__dict__[k]:
                if k in self.key_map.keys():
                    k = self.key_map[k]
                s += "<{0}>{1}</{0}>\n".format(k, self.__dict__[k])
        s += "</xml>"
        return s


class OrderResult(Result):
    """
        下单结果类
    """
    def __init__(self):
        # 调用接口提交的终端设备号，
        self.device_info = ""
        # SUCCESS/FAIL
        self.result_code = ""
        # 详细参见第6节错误列表
        # 错误码:
        # NOAUTH - 请商户前往申请此接口权限
        # NOTENOUGH - 用户帐号余额不足，请用户充值或更换支付卡后再支付
        # ORDERPAID - 商户订单已支付，无需更多操作
        # ORDERCLOSED - 当前订单已关闭，请重新下单
        # SYSTEMERROR - 系统异常，请用相同参数重新调用
        # APPID_NOT_EXIST - 请检查APPID是否正确
        # MCHID_NOT_EXIST - 请检查MCHID是否正确
        # APPID_MCHID_NOT_MATCH - 请确认appid和mch_id是否匹配
        # LACK_PARAMS - 请检查参数是否齐全
        # OUT_TRADE_NO_USED - 请核实商户订单号是否重复提交
        # SIGNERROR - 请检查签名参数和方法是否都符合签名算法要求
        # XML_FORMAT_ERROR - 请检查XML参数格式是否正确
        # REQUIRE_POST_METHOD - 请检查请求参数是否通过post方法提交
        # POST_DATA_EMPTY - 请检查post数据是否为空
        # NOT_UTF8 - 请使用NOT_UTF8编码格式
        self.err_code = ""
        # 错误返回的信息描述
        self.err_code_des = ""

        # 以下字段在return_code 和result_code都为SUCCESS的时候有返回

        # 调用接口提交的交易类型，取值如下：JSAPI，NATIVE，APP，详细说明见参数规定
        self.trade_type = ""
        # 微信生成的预支付回话标识，用于后续接口调用中使用，该值有效期为2小时
        self.prepay_id = ""
        # trade_type为NATIVE是有返回，可将该参数值生成二维码展示出来进行扫码支付
        self.code_url = ""

        super(OrderResult, self).__init__()


    def __repr__(self):
        return super(OrderResult, self).__repr__()


class QueryOrderResult(Result):
    """
        查询订单结果类
    """
    def __init__(self):
        # 微信支付分配的终端设备号，
        self.device_info = ""
        # 用户在商户appid下的唯一标识
        self.openid = ""
        # 用户是否关注公众账号，Y-关注，N-未关注，仅在公众账号类型支付有效
        self.is_subscribe = ""
        # 调用接口提交的交易类型，取值如下：JSAPI，NATIVE，APP，MICROPAY，详细说明见参数规定
        self.trade_type = ""
        # SUCCESS—支付成功
        # REFUND—转入退款
        # NOTPAY—未支付
        # CLOSED—已关闭
        # REVOKED—已撤销（刷卡支付）
        # USERPAYING--用户支付中
        # PAYERROR--支付失败(其他原因，如银行返回失败)
        self.trade_state = ""
        # 银行类型，采用字符串类型的银行标识
        self.bank_type = ""
        # 订单总金额，单位为分
        self.total_fee = 0
        # 货币类型，符合ISO 4217标准的三位字母代码，默认人民币：CNY，其他值列表详见货币类型
        self.fee_type = ""
        # 现金支付金额订单现金支付金额，详见支付金额
        self.cash_fee = 0
        # 货币类型，符合ISO 4217标准的三位字母代码，默认人民币：CNY，其他值列表详见货币类型
        self.cash_fee_type = ""
        # “代金券或立减优惠”金额<=订单总金额，订单总金额-“代金券或立减优惠”金额=现金支付金额，详见支付金额
        self.coupon_fee = 0
        # 代金券或立减优惠使用数量
        self.coupon_count = 0
        # 代金券或立减优惠批次ID ,$n为下标，从0开始编号
        self.coupon_batch_id_n = ""
        # 代金券或立减优惠ID, $n为下标，从0开始编号
        self.coupon_id_n = ""
        # 单个代金券或立减优惠支付金额, $n为下标，从0开始编号
        self.coupon_fee_n = 0
        # 微信支付订单号
        self.transaction_id = ""
        # 商户系统的订单号，与请求一致。
        self.out_trade_no = ""
        # 附加数据，原样返回
        self.attach = ""
        # 订单支付时间，格式为yyyyMMddHHmmss，如2009年12月25日9点10分10秒表示为20091225091010。其他详见时间规则
        self.time_end = ""
        # 对当前查询订单状态的描述和下一步操作的指引
        self.trade_state_desc = ""
        # SUCCESS/FAIL
        self.result_code = ""
        # 错误码:
        # ORDERNOTEXIST - 此交易订单号不存在
        # 原因: 查询系统中不存在此交易订单号 解决: 该API只能查提交支付交易返回成功的订单，请商户检查需要查询的订单号是否正确
        # SYSTEMERROR - 系统错误
        # 原因: 后台系统返回错误  解决: 系统异常，请再调用发起查询
        self.err_code = ""
        # 错误返回的信息描述
        self.err_code_des = ""

        super(QueryOrderResult, self).__init__()


    @property
    def key_map(self):
        """
            结果类属性对应xml节点名转换关系
        """
        return { "coupon_batch_id_n" : "coupon_batch_id_$n", "coupon_id_n" : "coupon_id_$n", "coupon_fee_n" : "coupon_fee_$n" }


    def __repr__(self):
        return super(QueryOrderResult, self).__repr__()


class CloseOrderResult(Result):
    """
        关闭订单结果类
    """
    def __init__(self):
        # 详细参见第6节错误列表
        # 错误码:
        # ORDERPAID - 订单已支付，不能发起关单，请当作已支付的正常交易
        # SYSTEMERROR - 系统异常，请重新调用该API
        # ORDERNOTEXIST - 不需要关单，当作未提交的支付的订单
        # ORDERCLOSED - 订单已关闭，无需继续调用
        # SIGNERROR - 请检查签名参数和方法是否都符合签名算法要求
        # REQUIRE_POST_METHOD - 请检查请求参数是否通过post方法提交
        # XML_FORMAT_ERROR - 请检查XML参数格式是否正确
        self.err_code = ""
        # 错误返回的信息描述
        self.err_code_des = ""

        super(CloseOrderResult, self).__init__()


    def __repr__(self):
        return super(CloseOrderResult, self).__repr__()


class RefundResult(Result):
    """
        申请退款结果类
    """
    def __init__(self):
        # SUCCESS/FAIL
        # SUCCESS退款申请接收成功，结果通过退款查询接口查询
        # FAIL 提交业务失败
        self.result_code = ""
        # 微信支付分配的终端设备号，与下单一致
        self.device_info = ""
        # 微信订单号
        self.transaction_id = ""
        # 商户系统内部的订单号
        self.out_trade_no = ""
        # 商户退款单号
        self.out_refund_no = ""
        # 微信退款单号
        self.refund_id = ""
        # ORIGINAL—原路退款
        # BALANCE—退回到余额
        self.refund_channel = ""
        # 退款总金额,单位为分,可以做部分退款
        self.refund_fee = 0
        # 订单总金额，单位为分，只能为整数，详见支付金额
        self.total_fee = 0
        # 订单金额货币类型，符合ISO 4217标准的三位字母代码，默认人民币：CNY，其他值列表详见货币类型
        self.fee_type = ""
        # 现金支付金额，单位为分，只能为整数，详见支付金额
        self.cash_fee = 0
        # 现金退款金额，单位为分，只能为整数，详见支付金额
        self.cash_refund_fee = 0
        # 代金券或立减优惠退款金额=订单金额-现金退款金额，注意：立减优惠金额不会退回
        self.coupon_refund_fee = 0
        # 代金券或立减优惠使用数量
        self.coupon_refund_count = 0
        # 代金券或立减优惠ID
        self.coupon_refund_id = ""
        # 错误码:
        # SYSTEMERROR - 请用相同参数再次调用API
        # INVALID_TRANSACTIONID - 请求参数错误，检查原交易号是否存在或发起支付交易接口返回失败
        # PARAM_ERROR - 请求参数错误，请重新检查再调用退款申请
        # APPID_NOT_EXIST - 请检查APPID是否正确
        # MCHID_NOT_EXIST - 请检查MCHID是否正确
        # APPID_MCHID_NOT_MATCH - 请确认appid和mch_id是否匹配
        # REQUIRE_POST_METHOD - 请检查请求参数是否通过post方法提交
        # SIGNERROR - 请检查签名参数和方法是否都符合签名算法要求
        # XML_FORMAT_ERROR - 请检查XML参数格式是否正确
        self.err_code = ""
        # 错误返回的信息描述
        self.err_code_des = ""

        super(RefundResult, self).__init__()


    def __repr__(self):
        return super(RefundResult, self).__repr__()


class QueryRefundResult(Result):
    """
        查询退款结果类
    """
    def __init__(self):
        # 终端设备号
        self.device_info = ""
        # SUCCESS/FAIL
        # SUCCESS退款申请接收成功，结果通过退款查询接口查询
        # FAIL
        self.result_code = ""
        # 微信订单号
        self.transaction_id = ""
        # 商户系统内部的订单号
        self.out_trade_no = ""
        # 订单总金额，单位为分，只能为整数，详见支付金额
        self.total_fee = 0
        # 订单金额货币类型，符合ISO 4217标准的三位字母代码，默认人民币：CNY，其他值列表详见货币类型
        self.fee_type = ""
        # 现金支付金额，单位为分，只能为整数，详见支付金额
        self.cash_fee = 0
        # 退款记录数
        self.refund_count = ""
        # 商户退款单号
        self.out_refund_no_n = ""
        # 微信退款单号
        self.refund_id_n = ""
        # ORIGINAL—原路退款
        # BALANCE—退回到余额
        self.refund_channel_n = ""
        # 退款总金额,单位为分,可以做部分退款
        self.refund_fee_n = 0
        # 代金券或立减优惠退款金额<=退款金额，退款金额-代金券或立减优惠退款金额为现金，说明详见代金券或立减优惠
        self.coupon_refund_fee_n = 0
        # 代金券或立减优惠使用数量 ,$n为下标,从0开始编号
        self.coupon_refund_count_n = 0
        # 批次ID ,$n为下标，$m为下标，从0开始编号
        self.coupon_refund_batch_id_n_m = 0
        # 代金券或立减优惠ID, $n为下标，$m为下标，从0开始编号
        self.coupon_refund_id_n_m = ""
        # 单个代金券或立减优惠支付金额, $n为下标，$m为下标，从0开始编号
        self.coupon_refund_fee_n_m = 0
        # 退款状态：
        # SUCCESS—退款成功
        # FAIL—退款失败
        # PROCESSING—退款处理中
        # NOTSURE—未确定，需要商户原退款单号重新发起
        # CHANGE—转入代发，退款到银行发现用户的卡作废或者冻结了，导致原路退款银行卡失败
        # 资金回流到商户的现金帐号，需要商户人工干预，通过线下或者财付通转账的方式进行退款。
        self.refund_status_n = ""
        # 取当前退款单的退款入账方
        # 1）退回银行卡：
        # {银行名称}{卡类型}{卡尾号}
        # 2）退回支付用户零钱:
        #    支付用户零钱
        self.refund_recv_accout_n = ""
        # 错误码:
        # SYSTEMERROR - 请尝试再次掉调用API。
        # INVALID_TRANSACTIONID - 请求参数错误，检查原交易号是否存在或发起支付交易接口返回失败
        # PARAM_ERROR - 请求参数错误，请检查参数再调用退款申请
        # APPID_NOT_EXIST - 请检查APPID是否正确
        # MCHID_NOT_EXIST - 请检查MCHID是否正确
        # APPID_MCHID_NOT_MATCH - 请确认appid和mch_id是否匹配
        # REQUIRE_POST_METHOD - 请检查请求参数是否通过post方法提交
        # SIGNERROR - 请检查签名参数和方法是否都符合签名算法要求
        # XML_FORMAT_ERROR - 请检查XML参数格式是否正确
        self.err_code = ""
        # 错误返回的信息描述
        self.err_code_des = ""

        super(QueryRefundResult, self).__init__()


    def __repr__(self):
        return super(QueryRefundResult, self).__repr__()


class NotifyReturnResult(object):
    def __init__(self):
        # SUCCESS/FAIL
        self.return_code = ""
        # 返回信息，如非空，为错误原因
        self.return_msg = ""


    # 重写__repr__方法
    def __repr__(self):
        """
            格式化成报文
        """
        # 将类的所有自建属性提取出来
        keys = self.__dict__.keys()

        s = "<xml>\n"
        # 将自建属性转为xml格式
        for k in keys:
            if self.__dict__[k]:
                s += "<{0}>{1}</{0}>\n".format(k, self.__dict__[k])
        s += "</xml>"
        return s


class NotifyResult(Result):
    """
        微信通知结果类
    """
    def __init__(self):
        # 微信支付分配的终端设备号
        self.device_info = ""
        # SUCCESS/FAIL
        self.result_code = ""
        # 错误返回的信息描述
        self.err_code = ""
        # 错误返回的信息描述
        self.err_code_des = ""
        # 用户在商户appid下的唯一标识
        self.openid = ""
        # 用户是否关注公众账号，Y-关注，N-未关注，仅在公众账号类型支付有效
        self.is_subscribe = ""
        # JSAPI、NATIVE、APP
        self.trade_type = ""
        # 银行类型，采用字符串类型的银行标识，银行类型见银行列表
        self.bank_type = ""
        # 订单总金额，单位为分
        self.total_fee = 0
        # 货币类型，符合ISO4217标准的三位字母代码，默认人民币：CNY，其他值列表详见货币类型
        self.fee_type = ""
        # 现金支付金额订单现金支付金额，详见支付金额
        self.cash_fee = 0
        # 货币类型，符合ISO4217标准的三位字母代码，默认人民币：CNY，其他值列表详见货币类型
        self.cash_fee_type = ""
        # 代金券或立减优惠金额<=订单总金额，订单总金额-代金券或立减优惠金额=现金支付金额，详见支付金额
        self.coupon_fee = 0
        # 代金券或立减优惠使用数量
        self.coupon_count = 0
        # 代金券或立减优惠ID,$n为下标，从0开始编号
        self.coupon_id_n = ""
        # 单个代金券或立减优惠支付金额,$n为下标，从0开始编号
        self.coupon_fee_n = 0
        # 微信支付订单号
        self.transaction_id = ""
        # 商户系统的订单号，与请求一致。
        self.out_trade_no = ""
        # 商家数据包，原样返回
        self.attach = ""
        # 支付完成时间，格式为yyyyMMddHHmmss，如2009年12月25日9点10分10秒表示为20091225091010。其他详见时间规则
        self.time_end = ""

        super(NotifyResult, self).__init__()


    @property
    def key_map(self):
        """
            结果类属性对应xml节点名转换关系
        """
        return { "self.coupon_id_n" : "self.coupon_id_$n", "self.coupon_fee_n" : "self.coupon_fee_$n" }


    def __repr__(self):
        return super(NotifyResult, self).__repr__()


class JSAPIRequest(object):
    """
        微信支付接口请求基类
    """
    def __init__(self):
        self.appid = WECHAT_PAY_APPID
        self.timestamp = int(time.time())
        self.noncestr = str(uuid.uuid1()).replace("-", "").upper()
        self.package = ""
        self.signtype = "MD5"

    @property
    def sign(self):
        """
            签名，详见签名生成算法
        """
        return sign(self)


def sign(request):
    """
        生成加密签名
    """
    keys = request.__dict__.keys()
    keys = sorted(keys)

    s = ""
    for k in keys:
        if request.__dict__[k]:
            if not s:
                s = "{0}={1}".format(k, request.__dict__[k])
            else:
                s = "{0}&{1}={2}".format(s, k, request.__dict__[k])

    s = "{0}&key={1}".format(s, WECHAT_SINGN_KEY)
    
    m = md5.new()
    m.update(s)
    return m.hexdigest().upper()


if __name__ == "__main__":
    # 下单
    request = Order()
    request.appid = "wxe4b34b117e5d52cc"
    request.mch_id = "1302574401"
    request.body = "移动流量包100M"  # 订单主体提示
    request.detail = "测试"   # 随便填
    request.attach = "和沃易"  # 随便填
    request.out_trade_no = str(uuid.uuid1()).replace("-", "")   # 生成订单号
    request.fee_type = "CNY"    # 货币(人民币)
    request.total_fee = 1   # 以分为单位
    request.spbill_create_ip = "14.19.198.14"
    request.notify_url = "http://www.weixin.qq.com/wxpay/pay.php"
    request.trade_type = "NATIVE"
    request.product_id = "12235413214070356458058"

    client = WeChatPay()
    result = client.order(request)
   
    q = qrcode.main.QRCode()
    q.add_data(result.code_url)
    q.make()
    m = q.make_image()
    m.save("/Users/lixingtie/Downloads/pay.jpg")

    # 查询订单
    #request = QueryOrder()
    #request.appid = "wxe4b34b117e5d52cc"
    #request.mch_id = "1302574401"
    #request.out_trade_no = "e94bcbf8b6a911e5bc76a8667f14e6b5"

    #client = WeChatPay()
    #result = client.query_order(request)
    #
    #print result

    # 关闭订单
    #request = CloseOrder()
    #request.appid = "wxe4b34b117e5d52cc"
    #request.mch_id = "1302574401"
    #request.out_trade_no = "e94bcbf8b6a911e5bc76a8667f14e6b5"

    #client = WeChatPay()
    #result = client.close_order(request)
    #
    #print result
