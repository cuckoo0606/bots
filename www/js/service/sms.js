angular.module('starter.services')

.service('SMSService', function($http, AppConfigService) {
    this.get_verify = function(params) {
        var url = AppConfigService.api_url + "sms/get";
        $http.get(url, { 
            "timeout": 10000,
            "params": { "phone": params.phone } 
        })
        
        .success(function(protocol) {
            if (protocol.return_code === "SUCCESS") {
                if (params.success) {
                    params.success(protocol.return_code, protocol.return_message);
                }
            }
            else {
                if (params.fail) {
                    params.fail(protocol.return_code, protocol.return_message);
                }
            }
        })
            
        .error(function(protocol) {
            if (params.error) {
                params.error("ERROR", "网络错误");
            }
        });
    };

    return this;
});
