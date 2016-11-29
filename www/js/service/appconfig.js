angular.module('starter.services', [])

.service('AppConfigService', function(ionicToast, $http, $ionicLoading, $ionicPopup) {
    var service = this;
    
    this.token = "";
    this.wx_auth = {}
    this.wx_user_info = {}

    this.system_name = "微交易系统";
    this.company_name = "云软微交易";
    this.show_system_name = true;
    this.system_logo = "img/logo/logo2.png";
    this.show_system_logo = true;
    this.show_nav_bar = true;
    this.show_signup_code = true;
    //配置注册跳转二维码
	this.if_weixin = {
		erweima_img:"img/logo/yunsof.jpg",
		weixin_name:"云软数据"
	}
	//配置交易金额
	this.trade_money={
		min_money:20,
		max_money:5000
	}

    this.api_url = "http://pay.longlix.cn/";
	this.qoute_url = "http://pay.longlix.cn:7794/";
    this.erweima_url= "http://pay.longlix.cn:8080/index.html";
    this.get_erweima_url = "http://pay.longlix.cn:8080/qrcode?text=";

    this.default_pay_type = "huanxun";
    this.pay_type_list = ["huanxun","huanxun_wecat"];

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
            	'code': 'ICBC',
            	'codenumber':'1100',
            	'icon':'icon-gongshangyinhang red',
            },
            {
            	'name': '农业银行', 
            	'code': 'ABC',
            	'codenumber':'1101',
            	'icon':'icon-nongyeyinxing1 green',
            },
            {
            	'name': '招商银行', 
            	'code': 'CMBC',
            	'codenumber':'1102',
            	'icon':'icon-zhaoshangyinhang red',
            },
            {
            	'name': '兴业银行', 
            	'code': 'CIB',
            	'codenumber':'1103',
            	'icon':'icon-xingyeyinhang blue',
            },
            {
            	'name': '中信银行', 
            	'code': 'ECITIC',
            	'codenumber':'1104',
            	'icon':'icon-zhongxinyinhang red',
            },
            {
            	'name': '建设银行', 
            	'code': 'CCB',
            	'codenumber':'1106',
            	'icon':'icon-jiansheyinhang blue',
            },
            {
            	'name': '中国银行', 
            	'code': 'BOC',
            	'codenumber':'1107',
            	'icon':'icon-zhongguoyinhang red',
            },
            {
            	'name': '交通银行', 
            	'code': 'BOCOM',
            	'codenumber':'1108',
            	'icon':'icon-jiaotongyinhang pay_purple',
            },
            {
            	'name': '浦发银行', 
            	'code': 'SPDB',
            	'codenumber':'1109',
            	'icon':'icon-pufayinhang pay_blue',
            },
            {
            	'name': '民生银行', 
            	'code': 'CMBCS',
            	'codenumber':'1110',
            	'icon':'icon-minshengyinhang pay_blue',
            },
            {
            	'name': '华夏银行', 
            	'code': 'HXB',
            	'codenumber':'1111',
            	'icon':'icon-huaxiayinhang red',
            },
            {
            	'name': '光大银行', 
            	'code': 'CEEBBANK',
            	'codenumber':'1112',
            	'icon':'icon-guangdayinhang pay_yellow',
            },
            {
            	'name': '广发银行', 
            	'code': 'CGB',
            	'codenumber':'1114',
            	'icon':'icon-guangfayinxing red',
            },
            {
            	'name': '邮政储蓄银行', 
            	'code': 'PSBC',
            	'codenumber':'1119',
            	'icon':'icon-youzhengyinhang green',
            },
            {
            	'name': '平安银行', 
            	'code': 'PINGAN',
            	'codenumber':'1121',
            	'icon':'icon-pinganyinxing orange',
            },
            {
            	'name': '北京银行', 
            	'codenumber':'1113',
            	'icon':'icon-beijingyinhang red',
            },
            {
            	'name': '南京银行', 
            	'codenumber':'1115',
            	'icon':'icon-nanjingyinhang red',
            },
            {
            	'name': '上海银行', 
            	'codenumber':'1116',
            	'icon':'icon-shanghaiyinhang orange',
            },
            {
            	'name': '杭州银行', 
            	'codenumber':'1117',
            	'icon':'icon-hangzhouyinhang pay_qing',
            },
            {
            	'name': '宁波银行', 
            	'codenumber':'1118',
            	'icon':'icon-ningboyinxing orange',
            },
            {
            	'name': '浙商银行', 
            	'codenumber':'1120',
            	'icon':'icon-zheshangyinhang pay_yellow',
            },
            {
            	'name': '东亚银行', 
            	'codenumber':'1122',
            	'icon':'icon-dongyayinhang red',
            },
            {
            	'name': '渤海银行', 
            	'codenumber':'1123',
            	'icon':'icon-bohaiyinhang blue',
            },
            {
            	'name': '北京农商行', 
            	'codenumber':'1124',
            	'icon':'icon-beijingnongshangyinhang red',
            },
            {
            	'name': '浙江泰隆商业银行', 
            	'codenumber':'1127',
            	'icon':'icon-zhejiangtailongshangyeyinhang orange',
            },
            {
            	'name': '徽商银行', 
            	'code':'HSB',
            	'icon':'icon-04403600 red',
            },
            {
            	'name': '长沙银行', 
            	'code':'CSCB',
            	'icon':'icon-04615510 red',
            },
            {
            	'name': '浙江省农村信用社联合社', 
            	'code':'ZJRCC',
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
    
    

    this.update = function (url) {
        if (!ionic.Platform.isAndroid()) {
            return false;
        }

        var path = cordova.file.externalCacheDirectory + "update.apk";
        var ft = new FileTransfer();

        ft.onprogress = function(progress) {
            var p = (progress.loaded / progress.total) * 100;    
            $ionicLoading.show({
                template: "正在下载更新文件<br/>已经下载：" + Math.floor(p) + "%"    
            });

            if (p > 99) {
                $ionicLoading.hide(); 
            }
        };

        ft.download(url, path,
            function(result) {
                cordova.plugins.fileOpener2.open(path, 'application/vnd.android.package-archive');    
                $ionicLoading.hide();    
            }, 
            function (err) {
                ionicToast.show('下载更新失败', 'short', 'bottom');
            },
            true,
            {}
        );
    }

    this.check_update = function (show_notify) {
        if (!ionic.Platform.isAndroid()) {
            return false;
        }
        
        $http.get(service.api_url + 'content/app_version.json')
        .then(function(resp){
            var server_version = resp.data.version;
            cordova.getAppVersion.getVersionNumber().then(function(version) {
                if (version != server_version) {
                    var popup = $ionicPopup.confirm({
                        title: '版本升级',
                        template: resp.data.release_note,
                        cancelText: '取消',
                        okText: '升级'
                    });

                    popup.then(function (res) {
                        if(res) {
                            service.update(resp.data.url);
                        }
                    });
                }
                else {
                    if (show_notify) {
                        ionicToast.show('已是最新版本', 'short', 'bottom');
                    }
                }
            });
        });
    }

    return this;
});
