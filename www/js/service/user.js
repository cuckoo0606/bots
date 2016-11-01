angular.module('starter.services')

.service('UserService', function($http, AppConfigService) {
    this.user = {};
    var service = this;

    this.signin = function(params) {
        var signinUrl = AppConfigService.build_api_url("v1/authorize");
        $http({
            "url": signinUrl,
            "method": "POST", 
            "timeout": 10000,
            "data": { "username": params.phone, "password": params.passwd } 
        })
        
        .success(function(protocol) {
            if (!protocol.error_code) {
                if (params.success) {
                    AppConfigService.token = protocol.access_token;
                    params.success(protocol);
                }
            }
            else {
                if (params.fail) {
                    params.fail("FAIL", "帐号或密码错误");
                }
            }
        })
            
        .error(function(protocol) {
            if (params.error) {
                params.error("ERROR", "网络错误");
            }
        });
    };

    this.request_user = function(complete) {
        var url = AppConfigService.build_api_url("v1/user")
        $http.get(url, {
            "timeout": 10000,
        })
        
        .success(function(protocol) {
            if (complete) {
                complete(protocol);
            }
        })
    };
	
    this.request_time = function(complete) {
        var url = AppConfigService.build_api_url("v1/time")
        $http.get(url, {
            "timeout": 10000,
        })
        
        .success(function(protocol) {
            if (complete) {
                complete(protocol);
            }
        })
    };
    
    this.signup = function(params) {
        var signupUrl = AppConfigService.api_url + "v1/register";
        
        $http({
            "url": signupUrl,
            "method": "POST", 
            "timeout": 10000,
            "data": { "username": params.phone, "password": params.passwd ,"referral_code":params.referralcode,"sms_code":params.code} 
        })
        .success(function(protocol) {
            if (!protocol.error) {
                params.success();
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
	
    this.update_user = function(params) {
        var updata_bankUrl = AppConfigService.build_api_url("v1/user");
        $http({
            "url": updata_bankUrl,
            "method": "POST", 
            "timeout": 10000,
            "data": { 
            	"name": params.name,
	        	"sex": params.sex,
	        	"phone": params.phone,
	        	"address": params.address,
	        	"email": params.email,
	        	"idcard": params.id_card,
	            "bank": params.bank,
	            "bankholder": params.bankholder,
	            "bankbranch": params.bankbranch,
	            "bankaccount": params.bankaccount
            }
        })
        
        .success(function(protocol) {
            if (protocol== "Created") {
                    params.success("SUCCESS", "SUCCESS", protocol);
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
