angular.module('starter.services')

.service('OrderInfoService',function ($http,AppConfigService,$rootScope, $timeout) {
    var service = this;
    this.info_list = [];
    this.success_info_list = [];
    this.order_type_list = [{time: 60,profit:75 + "%"},{time: 120,profit:75 + "%"},{time: 240,profit:80 + "%"},{time: 300,profit:80 + "%"}];


    this.getinfo = function (option) {
        var url = AppConfigService.build_api_url("v1/orders/buy");//下单接口
        $http({
            "url": url,
            "method": "POST",
            "timeout": 10000,
            "data": {"trade": option.trade,"direction":option.direction,"money":option.money,"cycle":option.cycle}
        }).success(function (protocol) {
            service.info_list.push(protocol);
            url = AppConfigService.build_api_url("v1/orders/" + service.info_list[0]._id);
            console.log(url);
            var check_order_state = function() {
                $http.get(url, {        //获取订单明细接口
                    "timeout": 10000
                }).success(function (value) {
                    if(value.status == 1) {
                        option.success(value);
                        service.success_info_list.push(value);
                        $timeout.cancel();
                    }
                    else {
                        $timeout(check_order_state, 1000);
                    }
                });
            };
            $timeout(check_order_state, 1000);
        });
    }
    return this;
})
