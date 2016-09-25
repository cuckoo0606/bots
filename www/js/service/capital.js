angular.module('starter.services')

.service('CapitalService', function($http, $interval, UserService, AppConfigService) {
    var service = this;
    this.capital_list = [];
    this.init_complete = false;

    this.deposit = function(params) {
        var url = AppConfigService.api_url + "pay/order";

        $http.get(url, { 
            "timeout": 30000,
            "params": params.deposit,
        })
        
        .success(function(protocol) {
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

    this.withdraw = function(params) {
        var url = AppConfigService.api_url + "capital/withdraw";

        $http.get(url, { 
            "timeout": 10000,
            "params": params.withdraw,
        })
        
        .success(function(protocol) {
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

    this.request_capital_list = function(complete) {
        var url = AppConfigService.api_url + "capital/list";
        $http.get(url, { 
            "timeout": 3000,
            "params": { "user": UserService.user.Id }
        })
        
        .success(function(protocol) {
            if (protocol.return_code === "SUCCESS") {
                if (complete) {
                    complete(protocol.data);
                }
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
