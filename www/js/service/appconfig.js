angular.module('starter.services', [])

.service('AppConfigService', function(ionicToast, $http, $ionicLoading, $ionicPopup) {
    var service = this;
    
    this.token = "";
    this.wx_auth = {}
    this.wx_user_info = {}

    this.system_name = "瑞盈财富通";
    this.company_name = "瑞盈财富通";
    this.show_system_name = false;
    this.system_logo = "img/logo/logo.png";
    this.show_system_logo = true;
    this.show_signup_code = true;
    //配置是否具有注册功能
    this.ifsignup = true;
    //配置注册跳转二维码
	this.if_weixin = {
		erweima_img:"img/logo/qcode.jpg",
		weixin_name:"瑞盈财富通"
	};
	//配置交易金额
	this.trade_money={
		min_money:20,
		max_money:5000
	};
	//配置货币符号
	this.currency_symbol = '￥';
	//配置接口地址
    this.api_url = "http://weixin.buut.cn:8793/";
    this.inmoney_url = "http://weixin.buut.cn:8989/";
	this.qoute_url = "http://weixin.leather-boss.com:7794/";
    this.erweima_url= "http://weixin.leather-boss.com:8085/index.html";
    this.get_erweima_url = "http://weixin.leather-boss.com:8085/qrcode?text=";

    this.bank_list = [ 
            { "name": "中国农业银行", "code": "ABC", 'icon':'icon-nongyeyinxing1 green'},
            { "name": "中国银行", "code": "BOC", 'icon':'icon-zhongguoyinhang red'},
            { "name": "中国工商银行", "code": "ICBC", 'icon':'icon-gongshangyinhang red'},
            { "name": "交通银行", "code": "BOCOM", 'icon':'icon-jiaotongyinhang pay_purple'},
            { "name": "中国建设银行", "code": "CCB", 'icon':'icon-jiansheyinhang blue' },
            { "name": "中国邮政储蓄银行", "code": "PSBC", 'icon':'icon-youzhengyinhang green' },
            { "name": "招商银行", "code": "CMBC", 'icon':'icon-zhaoshangyinhang red' },
            { "name": "浦发银行", "code": "SPDB", 'icon':'icon-pufayinhang pay_blue' },
            { "name": "中国光大银行", "code": "CEEBBANK", 'icon':'icon-guangdayinhang pay_yellow' },
            { "name": "中信银行", "code": "ECITIC", 'icon':'icon-zhongxinyinhang red' },
            { "name": "平安银行", "code": "PINGAN", 'icon':'icon-pinganyinxing orange' },
            { "name": "中国民生银行", "code": "CMBCS", 'icon':'icon-minshengyinhang pay_blue' },
            { "name": "华夏银行", "code": "HXB", 'icon':'icon-huaxiayinhang red' },
            { "name": "广发银行", "code": "CGB", 'icon':'icon-guangfayinxing red' },
            { "name": "兴业银行", "code": "CIB", 'icon':'icon-xingyeyinhang blue' },
            { "name": "徽商银行", "code": "HSB", 'icon':'icon-04403600 red' },
            { "name": "长沙银行", "code": "CSCB", 'icon':'icon-04615510 red' },
			{ "name": "浙江省农村信用社联合社", "code": "ZJRCC", 'icon':'icon-xinyonghezuoshe3 green' }
        ];
        
    this.pay_banklists = [
           {bank_title: "不选择银行", bank_code: "0000"},
           {bank_title: "中国银行", bank_code: "0001", 'icon':'icon-zhongguoyinhang red'},
	       {bank_title: "浦发银行", bank_code: "0002", 'icon':'icon-pufayinhang pay_blue'},
	       {bank_title: "中国民生银行", bank_code: "0003", 'icon':'icon-minshengyinhang pay_blue'},
	       {bank_title: "深圳发展银行", bank_code: "0004", 'icon':'icon-shenzhenfazhanyinhang pay_qing'},
	       {bank_title: "招商银行", bank_code: "0005", 'icon':'icon-zhaoshangyinhang red'},
	       {bank_title: "中国建设银行", bank_code: "0006", 'icon':'icon-jiansheyinhang blue'},
	       {bank_title: "中国农业银行", bank_code: "0007", 'icon':'icon-nongyeyinxing1 green'},
	       {bank_title: "中国邮政储蓄银行", bank_code: "0008", 'icon':'icon-youzhengyinhang green'},
	       {bank_title: "中国工商银行", bank_code: "0009", 'icon':'icon-gongshangyinhang red'},
	       {bank_title: "交通银行", bank_code: "0010", 'icon':'icon-jiaotongyinhang pay_purple'},
	       {bank_title: "华夏银行", bank_code: "0011", 'icon':'icon-huaxiayinhang red'},
	       {bank_title: "徽商银行", bank_code: "0012", 'icon':'icon-04403600 red'},
	       {bank_title: "中国光大银行", bank_code: "0013", 'icon':'icon-guangdayinhang pay_yellow'},
	       {bank_title: "中信银行", bank_code: "0014", 'icon':'icon-zhongxinyinhang red'},
	       {bank_title: "平安银行", bank_code: "0015", 'icon':'icon-pinganyinxing orange'},
	       {bank_title: "宁波银行", bank_code: "1001", 'icon':'icon-ningboyinxing orange'},
	       {bank_title: "南京银行", bank_code: "1002", 'icon':'icon-nanjingyinhang red'},
	       {bank_title: "杭州银行", bank_code: "1003", 'icon':'icon-hangzhouyinhang pay_qing'},
	       {bank_title: "北京银行", bank_code: "1004", 'icon':'icon-beijingyinhang red'},
	       {bank_title: "东亚银行", bank_code: "1005", 'icon':'icon-dongyayinhang red'},
	       {bank_title: "浙商银行", bank_code: "1006", 'icon':'icon-zheshangyinhang pay_yellow'},
	       {bank_title: "上海银行" ,bank_code: "1007", 'icon':'icon-shanghaiyinhang orange'},
	       {bank_title: "北京农村商业银行", bank_code: "2001", 'icon':'icon-beijingnongshangyinhang red'},
	       {bank_title: "上海农村商业银行", bank_code: "2002", 'icon':'icon-shanghainongshangyinhang-yy blue'},
	       {bank_title: "顺德农村信用合作社", bank_code: "2003", 'icon':'icon-xinyonghezuoshe3 pay_qing'},
	       {bank_title: "汉口银行", bank_code: "2004", 'icon':'icon-hankouyinhang blue'},
	       {bank_title: "广州市商业银行", bank_code: "2005", 'icon':'icon-guangzhoushishangyeyinhang pay_blue'},
	       {bank_title: "广州市农村信用合作社", bank_code: "2006", 'icon':'icon-xinyonghezuoshe3 green'},
	       {bank_title: "珠海市农村信用合作社", bank_code: "2007", 'icon':'icon-xinyonghezuoshe3 green'},
	       {bank_title: "尧都信用合作联社", bank_code: "2008", 'icon':'icon-xinyonghezuoshe3 green'},
	       {bank_title: "晋城市商业银行", bank_code: "2009", 'icon':'icon-guangzhoushishangyeyinhang pay_blue'},
	       {bank_title: "温州市商业银行", bank_code: "2010", 'icon':'icon-guangzhoushishangyeyinhang pay_blue'},
	       {bank_title: "兴业银行", bank_code: "2011", 'icon':'icon-xingyeyinhang blue'},
	       {bank_title: "渤海银行", bank_code: "2012", 'icon':'icon-bohaiyinhang blue'},
	       {bank_title: "广东发展银行", bank_code: "2013", 'icon':'icon-guangfayinxing red'},
	       {bank_title: "浙江泰隆商业银行", bank_code: "2014", 'icon':'icon-zhejiangtailongshangyeyinhang orange'},
		{bank_title: "银联电子商务", bank_code: "2015",'icon':'icon-yinlianzhifu pay_blue'},
		{bank_title: "上海浦东发展银行", bank_code: "2016",'icon':'icon-pufayinhang pay_blue'},
		{bank_title: "银联无卡支付", bank_code: "2017",'icon':'icon-yinlianzhifu pay_blue'},
		{bank_title: "银联其他银行", bank_code: "2018",'icon':'icon-yinlianzhifu pay_blue'},
		{bank_title: "中行-大额", bank_code: "2019",'icon':'icon-zhongguoyinhang red'}
     ]
	this.type_list = [
			{ "value": 0, "name": "初始化" },
            { "value": 1, "name": "入金" },
            { "value": 2, "name": "入金手续费" },
            { "value": 3, "name": "出金申请" },
            { "value": 4, "name": "出金手续费" },
            { "value": 5, "name": "出金失败" },
            { "value": 6, "name": "下单" },
            { "value": 7, "name": "结单" },
            { "value": 8, "name": "佣金" },
            { "value": 9, "name": "红利" },
            { "value": 10, "name": "管理员加款" }
	]
    this.build_api_url = function(url, params) {
        var url = service.api_url + url + "?access_token=" + service.token;
        if(params) {
            var args = params.map(function(key) {
                return key + "=" + params[key];
            });
            url += "&" + args.join("&");
        }
        return url;
        
    }
    
    return this;
});
