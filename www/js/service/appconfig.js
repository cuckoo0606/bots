angular.module('starter.services', [])

.service('AppConfigService', function(ionicToast, $http, $ionicLoading, $ionicPopup) {
    var service = this;
    
    this.token = "";
    this.system_name = "交易系统";
    this.show_system_name = false;
    this.system_logo = "img/logo.png";
    this.show_system_logo = true;
    this.show_nav_bar = false;
    this.show_signup_code = true;
    this.api_url = "http://weixin.leather-boss.com:8793/";
	this.qoute_url = "http://weixin.leather-boss.com:7794/";
	this.erweima_url= "http://weixin.leather-boss.com:8085/index.html";
    this.bank_list = [ 
            "招商银行", 
            "工商银行", 
            "农业银行",
            "中国银行", 
            "建设银行", 
            "民生银行", 
            "光大银行", 
            "交通银行",
            "兴业银行", 
            "浦发银行", 
            "华夏银行", 
        ];

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
