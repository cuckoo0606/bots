angular.module('starter.services')

.service('CapitalService', function($http, $interval, UserService, AppConfigService) {
    var service = this;
    this.capital_list = [];
    this.init_complete = false;
	this.money_list = [];
    this.deposit_hc = function(params) {
        var url = AppConfigService.build_api_url("v1/pay/hcmobile")

        $http({
            "url": url,
            "method": "POST",
            "timeout": 30000,
            "data": {
                "fee": params.deposit.amount,
                "body": params.deposit.body,
                "bankcode": params.deposit.bank.code,
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

    this.get_bank_list = function(complete) {
        if (complete) {
            var bank_list = [
                { "name": "快捷支付", "code": "NOCARD" },
                { "name": "招商银行", "code": "CMB" },
                { "name": "工商银行", "code": "ICBC" },
                { "name": "农业银行", "code": "ABC" },
                { "name": "中国银行", "code": "BOCSH" },
                { "name": "建设银行", "code": "CCB" },
                { "name": "民生银行", "code": "CMBC" },
                { "name": "光大银行", "code": "CEB" },
                { "name": "交通银行", "code": "BOCOM" },
                { "name": "兴业银行", "code": "CIB" },
                { "name": "浦发银行", "code": "HXB" },
                { "name": "华夏银行", "code": "HXB" },
            ];
            complete(bank_list);
        }
    }

	//资金列表接口
    this.request_capital_list = function(complete) {
        var capital_listUrl = AppConfigService.build_api_url("v1/books");
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
