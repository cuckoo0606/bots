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
        var signupUrl = AppConfigService.api_url + "v1/register";
        
        $http({
            "url": signupUrl,
            "method": "POST", 
            "timeout": 10000,
            "data": { "username": params.phone, "password": params.passwd ,"referral_code":params.referralcode,"sms_code":params.code} 
        })
        .success(function(protocol) {
        	if(protocol.error=="USER_EXIST"){
        		alert("用户已存在");
        	}
            if (!protocol.error) {
            	console.log("注册成功");
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

    this.update_bank = function(params) {
        var updata_bankUrl = AppConfigService.build_api_url("v1/user");
        $http({
            "url": updata_bankUrl,
            "method": "POST", 
            "timeout": 10000,
            "data": { 
            	"name":params.name,
	        	"sex":params.sex,
	        	"phone":params.phone,
	        	"address":params.address,
	        	"email":params.email,
	        	"id_card":params.id_card,
	            "bank": params.bank,
	            "bankholder": params.bankholder,
	            "bankbranch": params.bankbranch,
	            "bankaccount": params.bankaccount
            }
        })
        
        .success(function(protocol) {
            if (protocol== "Created") {
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

    return this;
});
