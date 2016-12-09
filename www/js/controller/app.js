angular.module('starter.controllers', [])

.controller('AppCtrl', function($scope, $rootScope, $ionicModal, $ionicSideMenuDelegate, $ionicScrollDelegate,
            $interval, $timeout, $filter, $ionicPlatform, $ionicHistory, $state, $http, $ionicLoading,
            AppConfigService, CloseOrderService, UserService, OrderService, QouteService) {
	$rootScope.iswecat = false;
	if(navigator.userAgent.toLowerCase().match(/MicroMessenger/i)=="micromessenger"){
		$rootScope.iswecat = true;
	};
    $scope.message = "";
    $scope.is_loading = false;
    $scope.show_update = ionic.Platform.isAndroid();
    $scope.system_name = AppConfigService.system_name;
    $scope.company_name = AppConfigService.company_name;
    $scope.show_system_name = AppConfigService.show_system_name;
    $scope.system_logo = AppConfigService.system_logo;
    $scope.show_system_logo = AppConfigService.show_system_logo;
    $scope.boundage = "";
    $scope.order_profit = OrderService.order_profit;
    $scope.last_result = [];
    $scope.phase = "";
    $scope.time_unit = "";
	$scope.trade_money = AppConfigService.trade_money;
	$scope.has_more_order = true;
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
        $scope.refresh_order();
    };

    $scope.toggle_order_confirm_panel = function(direction) {
        $scope.hold_order_modal.hide();
        angular.element(document.querySelectorAll(".history-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".order-state-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".order-confirm-panel")).toggleClass("open");
	      angular.element(document.querySelectorAll(".order-confirm-panel")).parent().toggleClass("glass_mask");
        $scope.order_params.direction = direction == "lookup" ? "1" : "0";
        $scope.trade_boundage();
        
        $timeout(function() {
            $ionicScrollDelegate.resize();
        }, 500);
    };

    $scope.toggle_order_state_panel = function () {
        $scope.hold_order_modal.hide();
        angular.element(document.querySelectorAll(".history-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".order-confirm-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".order-state-panel")).toggleClass("open");
	    angular.element(document.querySelectorAll(".order-state-panel")).parent().toggleClass("glass_mask");
    }
    
    $scope.continue_order = function() {
    	angular.element(document.querySelectorAll(".order-confirm-panel")).toggleClass("open");
        angular.element(document.querySelectorAll(".order-state-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".order-state-panel")).parent().removeClass("glass_mask");
        angular.element(document.querySelectorAll(".order-confirm-panel")).parent().toggleClass("glass_mask");
        $scope.order_params.direction = $scope.order_result.order.direction;
    }

    $scope.refresh_order = function() {
        $rootScope.trade_order_list = [];
        $scope.has_more_order = true;
        $scope.order_page_index = 0;
        $scope.load_more_order();
    }
    
    $scope.load_more_order = function() {
        OrderService.request_order_list($scope.order_page_index + 1, 20, function(protocol) {
            $scope.order_page_index = $scope.order_page_index + 1;
            protocol.data.forEach(function(value,index) {
            	value.profit = $scope.order_profit(value);
                value.qoute = QouteService.qoute(value.mode, value.assets.market, value.assets.code);
                var expired = new Date(value.expired);
                var now = new Date();
				
                var tick = now.getTime() + $rootScope.server_time_tick;
                var remaining = (expired.getTime() - tick) / 1000;
                value.remaining = remaining;
                value.alltime = new Date(value.expired).getTime() - new Date(value.created);
                if (remaining > 0) {
                    $rootScope.trade_order_list.push(value);
                }
                
            });

            if(protocol.data.length == 0) {
                $scope.has_more_order = false;
            }

            $scope.$broadcast('scroll.refreshComplete');
            $scope.$broadcast('scroll.infiniteScrollComplete');
        });
    }

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
    
    $scope.min_money = function() {
	   if(($scope.order_params.other_amount > $scope.trade_money.max_money)&&(event.keyCode!=8)) {
	   		event.preventDefault()
	   }
    }
    
    $scope.trade_boundage = function () {
        OrderService.trade_boundage({
            "success": function (status,protocol) {
                $scope.boundage = protocol;
            }
        })
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
                            
                            var expired = new Date(protocol.expired);
			                var now = new Date();
			
			                var tick = now.getTime() + $rootScope.server_time_tick;
			                var remaining = (expired.getTime() - tick) / 1000;
			                protocol.remaining = remaining;
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
    
   	$scope.$on('$destroy', function() {
   		$interval($scope.remain_interval);
   	});
});
