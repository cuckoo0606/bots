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
                    params.success();
        })
            
        .error(function(protocol) {
            if (params.error) {
                params.error("ERROR", "网络错误");
            }
        });
    };

    return this;
});
