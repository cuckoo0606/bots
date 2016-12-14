angular.module('starter.services', [])

.service('AppConfigService', function(ionicToast, $http, $ionicLoading, $ionicPopup) {
    var service = this;
    
    this.token = "";
    this.wx_auth = {}
    this.wx_user_info = {}

    this.system_name = "瑞达财富通";
    this.company_name = "瑞达财富通";
    this.show_system_name = false;
    this.system_logo = "img/logo/logo.png";
    this.show_system_logo = true;
    this.show_signup_code = true;
    //配置是否具有注册功能
    this.ifsignup = false;
    //配置注册跳转二维码
	this.if_weixin = {
		erweima_img:"img/logo/qcode.jpg",
		weixin_name:"瑞达财富通"
	};
	//配置交易金额
	this.trade_money={
		min_money:20,
		max_money:5000
	};
	//配置货币符号
	this.currency_symbol = '$';
	//配置接口地址
    this.api_url = "http://weixin.leather-boss.com:8793/";
	this.qoute_url = "http://weixin.leather-boss.com:7794/";
    this.erweima_url= "http://weixin.leather-boss.com:8085/index.html";
    this.get_erweima_url = "http://weixin.leather-boss.com:8085/qrcode?text=";

    this.default_pay_type = "ymd";
    this.pay_type_list = [ "ymd","weifutong" ];

    this.bank_list = [ 
            { "name": "中国农业银行", "code": "ABC" },
            { "name": "中国银行", "code": "BOC"},
            { "name": "中国工商银行", "code": "ICBC"},
            { "name": "交通银行", "code": "BOCOM"},
            { "name": "中国建设银行", "code": "CCB" },
            { "name": "中国邮政储蓄银行", "code": "PSBC" },
            { "name": "招商银行", "code": "CMBC" },
            { "name": "浦发银行", "code": "SPDB" },
            { "name": "中国光大银行", "code": "CEEBBANK" },
            { "name": "中信银行", "code": "ECITIC" },
            { "name": "平安银行", "code": "PINGAN" },
            { "name": "中国民生银行", "code": "CMBCS" },
            { "name": "华夏银行", "code": "HXB" },
            { "name": "广发银行", "code": "CGB" },
            { "name": "兴业银行", "code": "CIB" },
            { "name": "徽商银行", "code": "HSB" },
            { "name": "长沙银行", "code": "CSCB" },
			{ "name": "浙江省农村信用社联合社", "code": "ZJRCC" }
        ];
        
        
    this.deposit_bank_list = [ 
            {
            	'name': '工商银行', 
            	'HCcode': 'ICBC',
            	'HYcode':'1100',
            	'SXcode':'ICBC',
            	'icon':'icon-gongshangyinhang red',
            },
            {
            	'name': '农业银行', 
            	'HCcode': 'ABC',
            	'HYcode':'1101',
            	'SXcode':'ABC',
            	'icon':'icon-nongyeyinxing1 green',
            },
            {
            	'name': '招商银行', 
            	'HCcode': 'CMBC',
            	'HYcode':'1102',
            	'icon':'icon-zhaoshangyinhang red',
            },
            {
            	'name': '兴业银行', 
            	'HCcode': 'CIB',
            	'HYcode':'1103',
            	'SXcode':'CIB',
            	'icon':'icon-xingyeyinhang blue',
            },
            {
            	'name': '中信银行', 
            	'HCcode': 'ECITIC',
            	'HYcode':'1104',
            	'icon':'icon-zhongxinyinhang red',
            },
            {
            	'name': '建设银行', 
            	'HCcode': 'CCB',
            	'HYcode':'1106',
            	'SXcode':'CCB',
            	'icon':'icon-jiansheyinhang blue',
            },
            {
            	'name': '中国银行', 
            	'HCcode': 'BOC',
            	'HYcode':'1107',
            	'SXcode':'BOC',
            	'icon':'icon-zhongguoyinhang red',
            },
            {
            	'name': '交通银行', 
            	'HCcode': 'BOCOM',
            	'HYcode':'1108',
            	'icon':'icon-jiaotongyinhang pay_purple',
            },
            {
            	'name': '浦发银行', 
            	'HCcode': 'SPDB',
            	'HYcode':'1109',
            	'SXcode':'SPDB',
            	'icon':'icon-pufayinhang pay_blue',
            },
            {
            	'name': '民生银行', 
            	'HCcode': 'CMBCS',
            	'HYcode':'1110',
            	'icon':'icon-minshengyinhang pay_blue',
            },
            {
            	'name': '华夏银行', 
            	'HCcode': 'HXB',
            	'HYcode':'1111',
            	'icon':'icon-huaxiayinhang red',
            },
            {
            	'name': '光大银行', 
            	'HCcode': 'CEEBBANK',
            	'HYcode':'1112',
            	'SXcode':'CEB',
            	'icon':'icon-guangdayinhang pay_yellow',
            },
            {
            	'name': '广发银行', 
            	'HCcode': 'CGB',
            	'HYcode':'1114',
            	'icon':'icon-guangfayinxing red',
            },
            {
            	'name': '邮政储蓄银行', 
            	'HCcode': 'PSBC',
            	'HYcode':'1119',
            	'icon':'icon-youzhengyinhang green',
            },
            {
            	'name': '平安银行', 
            	'HCcode': 'PINGAN',
            	'HYcode':'1121',
            	'SXcode':'SPABANK',
            	'icon':'icon-pinganyinxing orange',
            },
            {
            	'name': '北京银行', 
            	'HYcode':'1113',
            	'icon':'icon-beijingyinhang red',
            },
            {
            	'name': '南京银行', 
            	'HYcode':'1115',
            	'icon':'icon-nanjingyinhang red',
            },
            {
            	'name': '上海银行', 
            	'HYcode':'1116',
            	'icon':'icon-shanghaiyinhang orange',
            },
            {
            	'name': '杭州银行', 
            	'HYcode':'1117',
            	'icon':'icon-hangzhouyinhang pay_qing',
            },
            {
            	'name': '宁波银行', 
            	'HYcode':'1118',
            	'icon':'icon-ningboyinxing orange',
            },
            {
            	'name': '浙商银行', 
            	'HYcode':'1120',
            	'icon':'icon-zheshangyinhang pay_yellow',
            },
            {
            	'name': '东亚银行', 
            	'HYcode':'1122',
            	'icon':'icon-dongyayinhang red',
            },
            {
            	'name': '渤海银行', 
            	'HYcode':'1123',
            	'icon':'icon-bohaiyinhang blue',
            },
            {
            	'name': '北京农商行', 
            	'HYcode':'1124',
            	'icon':'icon-beijingnongshangyinhang red',
            },
            {
            	'name': '浙江泰隆商业银行', 
            	'HYcode':'1127',
            	'icon':'icon-zhejiangtailongshangyeyinhang orange',
            },
            {
            	'name': '徽商银行', 
            	'HCcode':'HSB',
            	'icon':'icon-04403600 red',
            },
            {
            	'name': '长沙银行', 
            	'HCcode':'CSCB',
            	'icon':'icon-04615510 red',
            },
            {
            	'name': '浙江省农村信用社联合社', 
            	'HCcode':'ZJRCC',
            	'icon':'icon-xinyonghezuoshe3 green',
            },
        ];
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
