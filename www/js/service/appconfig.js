angular.module('starter.services', [])

.service('AppConfigService', function(ionicToast, $http, $ionicLoading, $ionicPopup) {
    var service = this;
    this.api_url = "http://103.249.106.200:8090/";
    
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
