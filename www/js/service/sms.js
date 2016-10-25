angular.module('starter.services')

.service('SMSService', function($http, AppConfigService) {
    this.get_verify = function(params) {
        var verifyUrl = AppConfigService.api_url + "v1/smscode";
        console.log(verifyUrl);
        $http({
            "url": verifyUrl,
            "method": "POST", 
            "timeout": 10000,
            "data": { "phone": params.phone} 
        })
        
        .success(function(protocol) {
        	console.log("succee")
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
