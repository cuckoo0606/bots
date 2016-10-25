angular.module('starter.services')

.service('UserService', function($http, AppConfigService) {
    this.user = {};
    var service = this;

    this.signin = function(params) {
        var url = AppConfigService.build_api_url("v1/authorize");
        $http({
            "url": url,
            "method": "POST", 
            "timeout": 10000,
            "data": { "username": params.username, "password": params.passwd } 
        })
        
        .success(function(protocol) {
            if (!protocol.error_code) {
                if (params.success) {
                    AppConfigService.token = protocol.access_token;
                    params.success("SUCCESS", protocol);
                }
            }
            else {
                if (params.fail) {
                    params.fail("FAIL", protocol);
                }
            }
        })
            
        .error(function(protocol) {
            if (params.error) {
                params.error("ERROR", "网络错误");
            }
        });
    };

    this.signup = function(params) {
        var signupUrl = AppConfigService.build_api_url("user/rigister");
        $http({
            "url": signupUrl,
            "method": "POST", 
            "timeout": 10000,
            "data": { "username": params.username, "password": params.passwd ,"phone":params.phone} 
        })
        
        .success(function(protocol) {
            if (!error) {
                if (params.success) {
                	console.log("success");
                    service.user = protocol.data;
                    params.success(protocol.return_code, protocol.return_message, protocol.data);
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

    this.update_bank = function(params) {
        var url = AppConfigService.api_url + "user/updatebank";
        $http.get(url, { 
            "timeout": 10000,
            "params": { "user": params.user, "bank": params.bank, "bank_user": params.bank_user, "bank_brand": params.bank_brand, "bank_card": params.bank_card } 
        })
        
        .success(function(protocol) {
            if (protocol.return_code === "SUCCESS") {
                if (params.success) {
                    service.user = protocol.data;
                    params.success(protocol.return_code, protocol.return_message, protocol.data);
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
