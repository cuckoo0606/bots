angular.module('starter.controllers', [])

.controller('AppCtrl', function($scope, $rootScope, $ionicModal, $ionicSideMenuDelegate,
            $timeout, $filter, $ionicPlatform, $ionicHistory, $state,$http,
            AppConfigService, CloseOrderService, UserService, OrderService, QouteService,OrderInfoService,$interval) {
    $scope.message = "";
    $scope.is_loading = false;
    $scope.show_update = ionic.Platform.isAndroid();
    $scope.show_nav_bar = AppConfigService.show_nav_bar;
    $scope.system_name = AppConfigService.system_name;
    $scope.show_system_name = AppConfigService.show_system_name;
    $scope.system_logo = AppConfigService.system_logo;
    $scope.show_system_logo = AppConfigService.show_system_logo;

    $scope.orderall_list={};
    $scope.info_list = OrderInfoService.info_list;
    $scope.success_info_list = OrderInfoService.success_info_list;
    $scope.getinfo = OrderInfoService.getinfo;
    $scope.buy_direction = "";
    $scope.choice = "";

    $scope.order_type_list = [{time: 60,profit:75 + "%"},{time: 120,profit:75 + "%"},{time: 240,profit:80 + "%"},{time: 300,profit:80 + "%"}];
    $scope.account_list = [5000,2000,1000,500,200,100];

    $scope.check_update = AppConfigService.check_update;
    $ionicPlatform.ready(function() {    
        $scope.check_update();
    });

    $scope.app_exit = function() {
        if (ionic.Platform.isWebView) {
            $rootScope.user = "";
            $ionicHistory.clearHistory();
            $state.go("signin");
        }
        else {
            ionic.Platform.exitApp();
        } 
    }

    $scope.order_params = {
        mode: 0,
        amount: 0,
        period: 0,
        direction: 1,
    };
    $scope.modal_hold_order = {};
    $scope.modal_close_order = {};

    $scope.toggleLeftSideMenu = function() {
        $ionicSideMenuDelegate.toggleLeft();
    };

    $scope.toggleRightSideMenu = function() {
        $ionicSideMenuDelegate.toggleRight();
    };
    
    $ionicModal.fromTemplateUrl('templates/hold-order-modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.hold_order_modal = modal;
    });

    $scope.show_hold_order_modal = function(order) {
        $scope.order_params.order_id = order.Id;
        $scope.modal_hold_order = order;
        $rootScope.trade_qoute = QouteService.qoute(order.symbol);
        $scope.hold_order_modal.show();
    };

    // 确认订单弹窗
    $ionicModal.fromTemplateUrl('templates/confirm_order.html',{
        scope: $scope,
        animation: 'slide-in-up'
    }).then (
        function (modal) {
            $scope.confirm_order = modal
        }
    );

    $scope.well_selected = function (index) {
        $scope.index = index;
    }

    $scope.amount_selected = function (index) {
        $scope.selectedRow = index;
        $scope.choice = $scope.account_list[$scope.selectedRow];
        angular.element(document.querySelector("#other_account")).removeClass("selected");
    }


    $scope.toggle_confirm_order_panel_rise = function () {
        $scope.confirm_order.show();
        $scope.direction = 1;
        if($scope.direction == 1) {
            $scope.buy_direction = "买涨"
        }
    }

    $scope.toggle_confirm_order_panel_fall = function () {
        $scope.confirm_order.show();
        $scope.direction = 0;
        if($scope.direction == 0) {
            $scope.buy_direction = "买跌"
        }
    }

    $scope.other_choice = function () {
        angular.element(document.querySelectorAll(".price_box")).removeClass("selected");
        angular.element(document.querySelector("#other_account")).addClass("selected");
        $scope.choice = angular.element(document.querySelector("#other_account"))[0].value;
    }

    $scope.change_border_color = function (index) {
        $scope.index_price = index;
    }

    $scope.toggle_confirm_order = function () {
        $scope.order_success.show();
        $scope.confirm_order.hide();

        OrderInfoService.getinfo({
                "trade": $rootScope.qoute.trade,
                "direction":$scope.direction,
                "money":$scope.account_list[$scope.selectedRow],
                "cycle":$scope.order_type_list[$scope.index].time,
                "success":function(message){
                    $scope.orderall_list=message;
                    var timer = $interval(function () {
                        $scope.orderall_list.cycle -= 1;
                        if($scope.orderall_list.cycle==0){
                            $interval.cancel(timer);
                            $scope.order_success.hide();
                        }
                    },1000);

                }
        }
        );
    }

    // 下单成功弹窗
    $ionicModal.fromTemplateUrl('templates/order_success.html',{
        scope: $scope,
        animation: 'slide-in-up'
    }).then (
        function (modal) {
            $scope.order_success = modal;

        }
    );

    $scope.toggle_order_success = function () {
        $scope.order_success.hide();
        $scope.confirm_order.show();
    }

    $ionicModal.fromTemplateUrl('templates/close-order-modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.close_order_modal = modal;
    });

    $scope.show_close_order_modal = function(order) {
        $scope.modal_close_order = order;
        $rootScope.trade_qoute = QouteService.qoute(order.symbol);
        $scope.close_order_modal.show();
    };

    $scope.toggle_order_panel = function(direction) {
        $scope.hold_order_modal.hide();
        angular.element(document.querySelectorAll(".close-order-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".history-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".order-panel")).toggleClass("open");

        if (angular.element(document.querySelectorAll(".order-panel")).hasClass("open")) {
            $rootScope.trade = QouteService.trade($rootScope.qoute.mode, $rootScope.qoute.market, $rootScope.qoute.code);
            $rootScope.trade_qoute = $rootScope.qoute;
            $scope.order_params.mode = $rootScope.qoute.mode;
            $scope.order_params.period = $rootScope.trade.cycle[0];
            $scope.order_params.amount = $rootScope.trade.amounts[0];
            $scope.order_params.direction = direction == "lookup" ? "1" : "0";
            console.log($scope.order_params.direction);
        }
    };

    $scope.toggle_close_order_panel = function() {
        $scope.hold_order_modal.hide();
        angular.element(document.querySelectorAll(".order-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".history-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".close-order-panel")).toggleClass("open");
    };

    $scope.toggle_history_order_panel = function() {
        $scope.hold_order_modal.hide();
        angular.element(document.querySelectorAll(".close-order-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".order-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".history-panel")).toggleClass("open");
    };

    $scope.order_profit = OrderService.order_profit;

    $scope.close_order = function() {
        var order = {
            "quantity": $scope.modal_hold_order.Quantity,
            "holdid": $scope.modal_hold_order.Id,
        };

        $scope.is_loading = true;
        CloseOrderService.order({
            "order": order,
            "success": function(status, message) {
                $scope.toggle_close_order_panel();
                $scope.is_loading = false;
                $scope.message = "交易成功";
                $timeout(function () {
                    $scope.message = "";
                }, 2000);
            },
            "fail": function(status, message) {
                $scope.is_loading = false;
                $scope.message = message;
                $timeout(function () {
                    $scope.message = "";
                }, 2000);
            },
            "error": function(status, message) {
                $scope.is_loading = false;
                $scope.message = message;
                $timeout(function () {
                    $scope.message = "";
                }, 2000);
            },
        });
    };

    $scope.order = function(category) {
        var order = {
            "money": $scope.order_params.amount,
            "cycle": $scope.order_params.period.time,
            "direction": $scope.order_params.direction,
            "trade": $rootScope.trade.trade,
        };

        console.log(order);

        $scope.is_loading = true;
        OrderService.order({
            "order": order,
            "success": function(status, message) {
                $scope.toggle_order_panel();
                $scope.is_loading = false;
                $scope.message = "交易成功";
                $timeout(function () {
                    $scope.message = "";
                }, 2000);
            },
            "fail": function(status, message) {
                $scope.is_loading = false;
                $scope.message = message;
                $timeout(function () {
                    $scope.message = "";
                }, 2000);
            },
            "error": function(status, message) {
                $scope.is_loading = false;
                $timeout(function () {
                    $scope.message = "";
                }, 2000);
            },
        });
    };

    $scope.update_order = function() {
        var order = {
            "id": $scope.order_params.order_id,
            "stop_price": $scope.order_params.stop_price,
            "profit_price": $scope.order_params.profit_price,
        };

        $scope.is_loading = true;
        OrderService.update_order({
            "order": order,
            "success": function(status, message) {
                $scope.toggle_order_panel();
                $scope.is_loading = false;
                $scope.message = "操作成功";
                $timeout(function () {
                    $scope.message = "";
                }, 2000);
            },
            "fail": function(status, message) {
                $scope.is_loading = false;
                $scope.message = message;
                $timeout(function () {
                    $scope.message = "";
                }, 2000);
            },
            "error": function(status, message) {
                $scope.is_loading = false;
                $timeout(function () {
                    $scope.message = "";
                }, 2000);
            },
        });
    };
});
