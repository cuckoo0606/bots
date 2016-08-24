angular.module('starter.controllers', [])

.controller('AppCtrl', function($scope, $rootScope, $ionicModal, $ionicSideMenuDelegate, $timeout, $filter, $ionicPlatform, 
            AppConfigService, AccountService, CloseOrderService, UserService, OrderService, LimitOrderService, QouteService) {
    $scope.message = "";
    $scope.is_loading = false;
    $scope.account = AccountService.account;
    $scope.show_update = ionic.Platform.isAndroid();

    $scope.check_update = AppConfigService.check_update;
    $ionicPlatform.ready(function() {    
        $scope.check_update();
    });

    $scope.app_exit = function() {
        ionic.Platform.exitApp(); 
    }

    $scope.order_params = {
        order_id: "",
        limit_id: "",
        quantity: 1,
        stop_price: "",
        profit_price: "",
        limit_price: 0,
        validity: "",
    };
    $scope.modal_hold_order = {};
    $scope.modal_limit_order = {};
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
    
    $ionicModal.fromTemplateUrl('templates/limit-order-modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.limit_order_modal = modal;
    });

    $scope.show_limit_order_modal = function(order) {
        $scope.order_params.limit_id = order.Id;
        $scope.modal_limit_order = order;
        $rootScope.trade_qoute = QouteService.qoute(order.symbol);
        $scope.limit_order_modal.show();
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

    $scope.toggle_order_panel = function() {
        $scope.hold_order_modal.hide();
        $scope.limit_order_modal.hide();
        angular.element(document.querySelectorAll(".close-order-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".history-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".limit-order-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".order-panel")).toggleClass("open");

        if (angular.element(document.querySelectorAll(".order-panel")).hasClass("open")) {
            $scope.order_params.order_id = "";
            $rootScope.trade_qoute = $rootScope.qoute;
            $scope.order_params.quantity = 1;
            $scope.order_params.stop_price = "";
            $scope.order_params.profit_price = "";
        }
    };
   
    $scope.toggle_order_update = function(o) {
        $scope.toggle_order_panel();

        if (angular.element(document.querySelectorAll(".order-panel")).hasClass("open")) {
            $rootScope.trade_qoute = QouteService.qoute(o.Symbol);
            $scope.order_params.order_id = o.Id;
            $scope.order_params.quantity = o.Quantity;
            $scope.order_params.stop_price = o.StopPrice;
            $scope.order_params.profit_price = o.ProfitPrice;
        }
    };
    
    $scope.toggle_limit_order_panel = function() {
        $scope.hold_order_modal.hide();
        $scope.limit_order_modal.hide();
        angular.element(document.querySelectorAll(".order-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".history-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".limit-order-panel")).toggleClass("open");

        if (angular.element(document.querySelectorAll(".limit-order-panel")).hasClass("open")) {
            $rootScope.trade_qoute = $rootScope.qoute;
            $scope.order_params.limit_id = "";
            $scope.order_params.quantity = 1;
            $scope.order_params.stop_price = "";
            $scope.order_params.profit_price = "";
            $scope.order_params.limit_price = 0;
            $scope.order_params.validity = $filter('date')(new Date(), 'yyyy-MM-dd');
        }
    };
   
    $scope.toggle_limit_order_update = function(o) {
        $scope.toggle_limit_order_panel();

        if (angular.element(document.querySelectorAll(".limit-order-panel")).hasClass("open")) {
            $rootScope.trade_qoute = QouteService.qoute(o.Symbol);
            $scope.order_params.limit_id = o.Id;
            $scope.order_params.quantity = o.Quantity;
            $scope.order_params.stop_price = o.StopPrice;
            $scope.order_params.profit_price = o.ProfitPrice;
            $scope.order_params.limit_price = o.LimitPrice;
            $scope.order_params.validity = o.Time;
        }
    };

    $scope.toggle_close_order_panel = function() {
        $scope.hold_order_modal.hide();
        $scope.limit_order_modal.hide();
        angular.element(document.querySelectorAll(".order-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".history-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".limit-order-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".close-order-panel")).toggleClass("open");
    };

    $scope.toggle_history_order_panel = function() {
        $scope.hold_order_modal.hide();
        $scope.limit_order_modal.hide();
        angular.element(document.querySelectorAll(".close-order-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".order-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".limit-order-panel")).removeClass("open");
        angular.element(document.querySelectorAll(".history-panel")).toggleClass("open");
    };

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

    $scope.limitorder = function(category) {
        var order = {
            "id": $scope.order_params.limit_id,
            "user": UserService.user.Id,
            "category": category,
            "limit_price": $scope.order_params.limit_price,
            "quantity": $scope.order_params.quantity,
            "symbol": $rootScope.qoute.Id,
            "stop_price": $scope.order_params.stop_price,
            "profit_price": $scope.order_params.profit_price,
            "validity": $scope.order_params.validity,
        };

        $scope.is_loading = true;
        LimitOrderService.order({
            "order": order,
            "success": function(status, message) {
                $scope.toggle_limit_order_panel();
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
                $scope.message = "网络错误";
                $timeout(function () {
                    $scope.message = "";
                }, 2000);
            },
        });
    };

    $scope.cancel_limitorder = function() {
        var params = {
            "id": $scope.order_params.limit_id,
            "user": UserService.user.Id,
        };

        $scope.is_loading = true;
        LimitOrderService.cancel_order({
            "params": params,
            "success": function(status, message) {
                $scope.limit_order_modal.hide();
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
                $scope.message = "网络错误";
                $timeout(function () {
                    $scope.message = "";
                }, 2000);
            },
        });
    };

    $scope.order = function(category) {
        var order = {
            "id": $scope.order_params.order_id,
            "user": UserService.user.Id,
            "category": category,
            "quantity": $scope.order_params.quantity,
            "symbol": $rootScope.qoute.Id,
            "stop_price": $scope.order_params.stop_price,
            "profit_price": $scope.order_params.profit_price,
        };

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
