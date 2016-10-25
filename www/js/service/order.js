angular.module('starter.services')

.service('OrderService', function($http, $interval, UserService, AppConfigService) {
    var service = this;
    this.order_list = [];
    this.init_complete = false;

    this.order = function(params) {
        var url = AppConfigService.api_url + "order/create";

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

    this.update_order = function(params) {
        var url = AppConfigService.api_url + "order/update";

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

    this.request_order_list = function(complete) {
        var orderTodayUrl = AppConfigService.build_api_url("v1/orders/today");
        $http.get(orderTodayUrl, {
            "timeout": 3000,
            "params": { "status":"1" }
        })
        .success(function(protocol) {
            // if (protocol.return_code === "SUCCESS") {
                if (complete) {
                    complete(protocol);
                }
            // }
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
