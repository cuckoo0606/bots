angular.module('starter.services')

.service('CloseOrderService', function($http, $interval, UserService, AppConfigService) {
    var service = this;
    this.order_list = [];
    this.init_complete = false;

    this.order = function(params) {
        var url = AppConfigService.api_url + "closeorder/create";

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

    this.request_order_list = function(page, size, complete) {
        var url = AppConfigService.build_api_url("v1/orders");
        $http.get(url, {
            "timeout": 3000,
            "params": { 
                "size" : size, 
                "status" : [ '110', '120' ], 
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
