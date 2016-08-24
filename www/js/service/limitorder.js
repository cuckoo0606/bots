angular.module('starter.services')

.service('LimitOrderService', function($http, $interval, UserService, AppConfigService) {
    var service = this;
    this.order_list = [];
    this.init_complete = false;

    this.order = function(params) {
        var url = AppConfigService.api_url + "limitorder/save";

        $http.get(url, { 
            "timeout": 10000,
            "params": params.order,
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

    this.cancel_order = function(params) {
        var url = AppConfigService.api_url + "limitorder/delete";

        $http.get(url, { 
            "timeout": 10000,
            "params": params.params,
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
    
    this.request_order_list = function(complete) {
        var url = AppConfigService.api_url + "limitorder/list";
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
                service.request_order_list(function(order_list) {
                    while(service.order_list.length) {
                        service.order_list.pop();
                    }
                    angular.forEach(order_list, function(value) {
                        service.order_list.push(value);
                    });

                    if (complete) {
                        complete();
                    }
                });
            }, 1000);
        }
    };

    return this;
});
