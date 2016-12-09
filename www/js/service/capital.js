angular.module('starter.services')

.service('CapitalService', function($http, $interval, UserService, AppConfigService) {
    var service = this;
    this.capital_list = [];
    this.init_complete = false;

    this.deposit_wechat = function(params) {
        var url = "/pay/wechat/order";

        $http({
            "url": url,
            "method": "POST",
            "timeout": 30000,
            "data": {
                "user": params.deposit.user,
                "amount": params.deposit.amount,
                "openid": params.deposit.openid,
            },
        })

        .success(function(protocol) {
            if (protocol.return_code === "SUCCESS") {
                params.success(protocol.return_code, protocol.return_msg, protocol);
            }
            else {
                params.fail(protocol.return_code, protocol.return_msg, protocol);
            }
        })

        .error(function(protocol) {
            if (params.error) {
                params.error("ERROR", "网络错误");
            }
        });
    }

    //一麻袋接口
    this.deposit_ymd = function(params) {
        var url = AppConfigService.build_api_url("v1/pay/yemadaikj");
        $http({
            "url": url,
            "method": "POST",
            "timeout": 30000,
            "data": {
                "fee": params.deposit.amount,
                "body": params.deposit.body,
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

    //汇潮接口
    this.deposit_hc = function(params) {
        var url = AppConfigService.build_api_url("v1/pay/hcmobile")

        $http({
            "url": url,
            "method": "POST",
            "timeout": 30000,
            "data": {
                "fee": params.deposit.amount,
                "body": params.deposit.body,
                "bankcode": params.bankcode,
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
    
    //中云接口
    this.deposit_zhongyun = function(params) {
        var url = AppConfigService.build_api_url("v1/pay/yz")

        $http({
            "url": url,
            "method": "POST",
            "timeout": 30000,
            "data": {
                "fee": params.deposit.amount,
                "body": "入金",
                "bankcode": "yjzf",
                "tongdao" : "YeePayYjzf",
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
    
    //中云微信接口
    this.deposit_zhongyun_wecat = function(params) {
        var url = AppConfigService.build_api_url("v1/pay/yz")

        $http({
            "url": url,
            "method": "POST",
            "timeout": 30000,
            "data": {
                "fee": params.deposit.amount,
                "body": "入金",
                "bankcode": "WXZF",
                "tongdao" : "ShaoBeiGzh",
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

	//环迅接口
    this.deposit_hx = function(params) {
        var url = AppConfigService.build_api_url("v1/pay/ips")

        $http({
            "url": url,
            "method": "POST",
            "timeout": 30000,
            "data": {
                "fee": params.deposit.amount,
                "body": "入金",
                "bankcode": params.bankcode,
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
    
    //环迅微信接口
    this.deposit_hxwecat = function(params) {
        var url = AppConfigService.build_api_url("v1/pay/ipswx")

        $http({
            "url": url,
            "method": "POST",
            "timeout": 30000,
            "data": {
                "fee": params.deposit.amount,
                "body": "入金"
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
    
    //智慧接口
    this.deposit_zhihui = function(params) {
        var url = AppConfigService.build_api_url("v1/pay/chinag")

        $http({
            "url": url,
            "method": "POST",
            "timeout": 30000,
            "data": {
                "fee": params.deposit.amount,
                "body": "入金",
                "txnType" :params.txnType,
                "payType":params.payType,
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
    
    //商银快捷短信下发接口
    this.deposit_shangyin_mes = function(params) {
        var url = AppConfigService.build_api_url("v1/pay/allscore/fastsms")
        $http({
            "url": url,
            "method": "POST",
            "timeout": 30000,
            "data": {
                "fee": params.deposit.amount,
                "body": "income",
                "bankCardNo" :params.bankCard,
                "bankId":params.bankId,
				"cardId":params.cardId,
				"phoneNo":params.phone,
				"realName":params.realName
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
    
    //商银验证码接口
    this.deposit_shangyin_sure = function(params) {
        var url = AppConfigService.build_api_url("v1/pay/allscore/fastpay")
        $http({
            "url": url,
            "method": "POST",
            "timeout": 30000,
            "data": {
                "no": params.no,
                "verifyCode": params.verifyCode,
            },
        })
        
        .success(function(protocol) {
        	if(protocol.status == 0){
        		params.fail();
        	}else if(protocol.status == 1){
        		params.success(protocol);
        	}
        })
            
        .error(function(protocol) {
            if (params.error) {
                params.error("ERROR", "网络错误");
            }
        });
    }
    //威富通公众号接口
    this.deposit_swift = function(params) {
        var url = AppConfigService.build_api_url("v1/pay/swiftpass")

        $http({
            "url": url,
            "method": "POST",
            "timeout": 30000,
            "data": {
                "fee": params.deposit.amount,
                "body": params.deposit.body,
                "openid": params.deposit.openid,
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
