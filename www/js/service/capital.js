angular.module('starter.services')

.service('CapitalService', function($http, $interval, UserService, AppConfigService) {
    var service = this;
    this.capital_list = [];
    this.init_complete = false;
	this.money_list = [];
    this.deposit = function(params) {
        var url = AppConfigService.api_url + "pay/order";

        $http.get(url, { 
            "timeout": 30000,
            "params": {
                "user": params.deposit.user,
                "pay_type": params.deposit.pay_type,
                "amount": params.deposit.amount,
                "bank": params.deposit.bank.BankCode,
                "return_url": params.deposit.return_url,
            },
        })
        
        .success(function(protocol) {
            params.success(protocol);
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

		console.log(outWithdrawUrl);
		console.log(params.outamount);
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
                params.error("ERROR", "网络错误");
            }
        });
    }

    this.get_bank_list = function(params) {
        var url = AppConfigService.api_url + "pay/banklist";

        $http.get(url, { 
            "timeout": 30000,
            "params": { "pay_type": params.pay_type },
        })
        
        .success(function(protocol) {
            console.log(protocol);
            if (protocol.return_code === "SUCCESS") {
                if (params.success) {
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
    }
	//资金列表接口
    this.request_capital_list = function(complete) {
        var capital_listUrl = AppConfigService.build_api_url("v1/books");
        console.log(capital_listUrl);
        $http.get(capital_listUrl, { 
            "timeout": 3000,
            "params": { "begin": "2016-01-01" }
        })
        
        .success(function(protocol) {
            this.money_list=protocol;
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
