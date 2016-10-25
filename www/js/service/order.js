angular.module('starter.services')

.service('OrderService', function($http, $interval, UserService, AppConfigService, QouteService) {
    var service = this;

    this.order_profit = function(order) {
        var qoute = QouteService.qoute(order.mode, order.assets.market, order.assets.code);
        var profit = order.money * order.inprice;
        if (order.direction == 0 && qoute.value > order.buyQoute) {
            profit = profit * -1;
        }
        if (order.direction == 1 && qoute.value < order.buyQoute) {
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
