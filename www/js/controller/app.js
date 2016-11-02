angular.module('starter.controllers', [])

.controller('AppCtrl', function($scope, $rootScope, $ionicModal, $ionicSideMenuDelegate, $ionicScrollDelegate,
            $interval, $timeout, $filter, $ionicPlatform, $ionicHistory, $state, $http, $ionicLoading,
            AppConfigService, CloseOrderService, UserService, OrderService, QouteService) {
    $scope.message = "";
    $scope.is_loading = false;
    $scope.show_update = ionic.Platform.isAndroid();
    $scope.show_nav_bar = AppConfigService.show_nav_bar;
    $scope.system_name = AppConfigService.system_name;
    $scope.show_system_name = AppConfigService.show_system_name;
    $scope.system_logo = AppConfigService.system_logo;
    $scope.show_system_logo = AppConfigService.show_system_logo;
    $scope.max_over = false;

    $scope.order_params = {
        "cycle": {},
        "amount": "",
        "other_amount" : "",
        "direction": "1",
    }

    $scope.order_result = {
        "status": "POST",
        "message": "正在提交订单",
    }

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

    $scope.modal_hold_order = {};
    $scope.modal_close_order = {};
    
    $ionicModal.fromTemplateUrl('templates/hold-order-modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.hold_order_modal = modal;
    });

    $scope.show_hold_order_modal = function(order) {
        $scope.modal_hold_order = order;
        $rootScope.trade_qoute = QouteService.qoute(order.symbol);
        $scope.hold_order_modal.show();
    };

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

     $scope.toggle_history_order_panel = function() {
        $scope.hold_order_modal.hide();
        angular.element(document.querySelectorAll(".order-confirm-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".order-confirm-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".history-panel")).toggleClass("open");
    };

    $scope.toggle_order_confirm_panel = function(direction) {
        $scope.hold_order_modal.hide();
        angular.element(document.querySelectorAll(".history-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".order-state-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".order-confirm-panel")).toggleClass("open");
        $scope.order_params.direction = direction == "lookup" ? "1" : "0";
        $ionicScrollDelegate.resize();
    };

    $scope.toggle_order_state_panel = function () {
        $scope.hold_order_modal.hide();
        angular.element(document.querySelectorAll(".history-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".order-confirm-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".order-state-panel")).toggleClass("open");
    }

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
    
    $scope.limit_account = function() {
	   if($scope.order_params.other_amount>5000) {
	    	$scope.max_over = true;
	    }else{
	    	$scope.max_over = false;
	    }
    }
    
    $scope.order = function() {
        var order = {
            "trade": $rootScope.trade.trade,
            "direction": $scope.order_params.direction,
            "money": ($scope.order_params.other_amount != "" && $scope.order_params.other_amount != "0") ? $scope.order_params.other_amount : $scope.order_params.amount,
            "cycle": $scope.order_params.cycle.time,
        };


        $scope.order_result = {
            "status": "POST",
            "message": "正在交易",
        }
        
        $scope.toggle_order_confirm_panel();
        $scope.toggle_order_state_panel();

        OrderService.order({
            "order": order,
            "success": function(status, protocol) {
                var check_order = function() {
                    OrderService.request_order(protocol._id, function(protocol) {
                        if (protocol.status === 1) {
                            $scope.order_result.status = "SUCCESS";
                            $scope.order_result.message = "交易成功";
                            $scope.order_result.order = protocol;
                            protocol.qoute = QouteService.qoute(protocol.mode, protocol.assets.market, protocol.assets.code);
                            $rootScope.trade_order_list.push(protocol);
                        }
                        else {
                            $timeout(check_order, 1000);                
                        }
                    });
                }

                $timeout(check_order, 1000);                
            },
            "fail": function(status, protocol) {
                $scope.order_result.status = "FAIL";
                $scope.order_result.message = "交易失败";
            },
            "error": function(status, message) {
                $scope.order_result.status = "FAIL";
                $scope.order_result.message = message;
            },
        });
    };

    var user_interval = $interval(function() {
        if ($rootScope.user) {
            UserService.request_user(function(user) {
                $rootScope.user = user;
            });
        }
    }, 1000);
});
