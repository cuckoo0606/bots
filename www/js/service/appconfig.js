angular.module('starter.services', [])

.service('AppConfigService', function(ionicToast, $http, $ionicLoading, $ionicPopup) {
    var service = this;
    
    this.token = "";
    this.wx_auth = {}
    this.wx_user_info = {}

    this.system_name = "交易系统";
    this.company_name = "恒忆微盘";
    this.show_system_name = false;
    this.system_logo = "img/logo.png";
    this.show_system_logo = true;
    this.show_nav_bar = false;
    this.show_signup_code = true;

    this.api_url = "http://weixin.leather-boss.com:8793/";
	this.qoute_url = "http://weixin.leather-boss.com:7794/";
	this.erweima_url= "http://weixin.leather-boss.com/index.html";
	this.get_erweima_url = "http://weixin.leather-boss.com/qrcode?text=";

    this.bank_list = [ 
            { "name": "中国农业银行", "code": "ABC" },
            { "name": "中国银行", "code": "BOC" },
            { "name": "中国工商银行", "code": "ICBC" },
            { "name": "交通银行", "code": "BOCOM" },
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
            { "name": "微商银行", "code": "HSB" },
            { "name": "长沙银行", "code": "CSCB" },
			{ "name": "浙江省农村信用社联合社", "code": "ZJRCC" }
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
