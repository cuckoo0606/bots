angular.module('starter.services')

.service('CapitalService', function($http, $interval, UserService, AppConfigService) {
    var service = this;
    this.capital_list = [];
    this.init_complete = false;

    //获取支付通道列表接口
    this.get_pay_channel = function(params){
        var url = AppConfigService.inmoney_url+'v2/payment-channel?access_token='+AppConfigService.token;
        $http.get(url, {
            "timeout": 10000,
            "params": { 
                "client_type" : params.client_type
            }
        })
        .success(function(protocol) {
        	if(protocol.code == 0){
        		if(params.success){
        			params.success(protocol.data);
        		}
        	}else{
        		params.fail(protocol.message);
        	}
        })
        .error(function(protocol) {
            if (params.error) {
                var message = "网络错误";
                params.error(message);
            }
        });
    }

    //入金接口
    this.payment = function(params){
        var url = AppConfigService.inmoney_url+'v2/payment?access_token='+AppConfigService.token;
        $http({
            "url": url,
            "method": "POST", 
            "timeout": 3000,
            "data": { "fee":params.fee ,'bank_code':params.bank_code, 'payment_channel':params.payment_channel} 
        })
        
        .success(function(protocol) {
        	if(protocol.code==0&&params.success){
        		params.success(protocol);
        	}else{
        		params.fail(protocol.message);
        	}
        })
            
        .error(function(protocol) {
            if (params.error) {
                var message = "网络错误";
                if (protocol.error_message) {
                    message = protocol.error_message;
                }
                params.error(message);
            }
        });
    }
    //需要openid接口
    this.pay_openid = function(params){
        var url = AppConfigService.inmoney_url+'v2/payment?access_token='+AppConfigService.token;
        $http({
            "url": url,
            "method": "POST", 
            "timeout": 3000,
            "data": { "fee":params.fee , 'payment_channel':params.payment_channel, 'openid':params.openid} 
        })
        
        .success(function(protocol) {
        	if(protocol.code==0&&params.success){
        		params.success(protocol);
        	}else{
        		params.fail(protocol.message);
        	}
        })
            
        .error(function(protocol) {
            if (params.error) {
                var message = "网络错误";
                if (protocol.error_message) {
                    message = protocol.error_message;
                }
                params.error(message);
            }
        });
    }
	//系统配置接口
	this.system_config = function(params){
		var system_config_url = AppConfigService.build_api_url("v1/config/"+params.type);
        $http.get(system_config_url, {
            "timeout": 10000,
        }).success(function (protocol) {
            if(params.success) {
                params.success(protocol);
            }
        })

        .error(function(protocol) {
            if (params.error) {
                params.error("ERROR", "网络错误");
            }
        });
	}
	//出金接口
    this.out_withdraw = function(params) {
        var outWithdrawUrl = AppConfigService.build_api_url("v1/outflow");

        $http({
            "url": outWithdrawUrl,
            "method": "POST", 
            "timeout": 3000,
            "data": { "amount": params.outamount } 
        })
        
        .success(function(protocol) {
            params.success(protocol);
        })
            
        .error(function(protocol) {
            if (params.error) {
                var message = "网络错误";
                if (protocol.error_message) {
                    message = protocol.error_message;
                }
                params.error(message);
            }
        });
    }


	//资金列表历史接口
    this.request_capital_list = function(complete) {
        var capital_listUrl = AppConfigService.build_api_url("v1/books");
        $http.get(capital_listUrl, { 
            "timeout": 3000,
            "params": { "begin": complete.startDate,"end":complete.overDate,"page":complete.page,"size":complete.size }
        })
        
        .success(function(protocol) {
            if(complete){
            	complete.success(protocol);
            }
            
        });
    }

    this.init = function(complete) {
        if (!service.init_complete) {
            service.init_complete = true;
            $interval(function() {
                service.request_capital_list(function(capital_list) {
                    while(service.capital_list.length) {
                        service.capital_list.pop();
                    }
                    angular.forEach(capital_list, function(value) {
                        service.capital_list.push(value);
                    });

                    if (complete) {
                        complete();
                    }
                });
            }, 5000);
        }
    };

    return this;
});
