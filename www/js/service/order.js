angular.module('starter.services')

.service('OrderService', function($http, $interval, UserService, AppConfigService, QouteService) {
    var service = this;

    this.order_profit = function(order) {
        var qoute = QouteService.qoute(order.mode, order.assets.market, order.assets.code);
        var profit = order.money * order.inprice;

        var buy = parseFloat(order.buyQoute.toFixed(qoute.decimal));
        var value = parseFloat(qoute.value.toFixed(qoute.decimal));
        if (value == buy) {
            return 0;
        }

        if (order.direction == 0 && value > buy) {
            profit = profit * -1;
        }
        if (order.direction == 1 && value < buy) {
            profit = profit * -1;
        }
        return profit;
    }

    this.order = function(params) {
        var url = AppConfigService.build_api_url("v1/orders/buy");

        $http({
            "url": url,
            "method": "POST",
            "timeout": 10000,
            "data": params.order,
        })

        .success(function(protocol) {
            if (!protocol.error_code) {
                if (params.success) {
                    params.success("SUCCESS", protocol);
                }
            }
            else {
                if (params.fail) {
                    params.success("FAIL", protocol);
                }
            }
        })

        .error(function(protocol) {
            if (params.error) {
                var message = "网络错误";
                if (protocol.error_code) {
                    message = protocol.error_code;
                    if (message == "Market_Close") {
                        message = "非交易时间";
                    }
                }

                params.error("ERROR", message);
            }
        });
    }

    this.request_order = function(id, complete) {
        var url = AppConfigService.build_api_url("v1/orders/" + id);
        $http.get(url, {
            "timeout": 10000,
        }).success(function (protocol) {
            if(complete) {
                complete(protocol);
            }
        })

        .error(function(protocol) {
            if (params.error) {
                params.error("ERROR", "网络错误");
            }
        });
    }

    this.request_order_list = function(page, size, complete) {
        var url = AppConfigService.build_api_url("v1/orders");
        $http.get(url, {
            "timeout": 3000,
            "params": { 
                "size" : size, 
                "status" : 1, 
                "page" : page, 
            }
        })
        .success(function(protocol) {
            if (complete) {
                complete(protocol);
            }
        });
    }

    return this;
});
