angular.module('starter.services')

.service('UserService', function($http, AppConfigService) {
    var service = this;

    this.get_open_id = function(params) {
        var url = "/wechat/openid";
        $http({
            "url": url,
            "method": "GET", 
            "timeout": 10000,
        })
        
        .success(function(protocol) {
            if (!protocol.openid) {
                if (params.success) {
                    params.success("SUCCESS", "SUCCESS", protocol);
                }
            }
            else {
                if (params.fail) {
                    params.fail("FAIL", "FAIL");
                }
            }
        })
            
        .error(function(protocol) {
            if (params.error) {
                params.error("ERROR", "网络错误");
            }
        });
    }

    return this;
});
