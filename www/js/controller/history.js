angular.module('starter.controllers')

.controller('HistoryCtrl', function($scope, $rootScope, $stateParams, $ionicModal, $ionicSlideBoxDelegate, $interval, OrderService, CloseOrderService, QouteService) {
    $scope.order_page_index = 0;
    $scope.close_order_page_index = 0;

    $scope.order_list = [];
    $scope.has_more_order = true;
    $scope.close_order_list = [];
    $scope.has_more_close_order = true;
    $scope.category_index = parseInt($stateParams.index);
    
    $scope.slide_change = function(index) {
        if (isNaN(index)) {
            return;
        }
        $scope.category_index = index;
    };

    $scope.change_category = function(index) {
        $scope.category_index = index;
        
        var slide = $ionicSlideBoxDelegate.$getByHandle('slide-history');
        if (slide) {
            slide.slide(index);
        }
    };

    $scope.refresh_order = function() {
        $scope.order_list = [];
        $scope.has_more_order = true;
        $scope.order_page_index = 0;
        $scope.load_more_order();
    }

    $scope.load_more_order = function() {
        OrderService.request_order_list($scope.order_page_index + 1, 20, function(protocol) {
            $scope.order_page_index = $scope.order_page_index + 1;
            protocol.data.forEach(function(value) {
                value.profit = $scope.order_profit(value);
                value.qoute = QouteService.qoute(value.mode, value.assets.market, value.assets.code);
                var expired = new Date(value.expired);
                var now = new Date();

                var tick = now.getTime() + $rootScope.server_time_tick;
                var remaining = (expired.getTime() - tick) / 1000;
                value.remaining = remaining;
                if (remaining > 0) {
                    $scope.order_list.push(value);
                }
            });

            if(protocol.data.length === 0) {
                $scope.has_more_order = false;
            }

            $scope.$broadcast('scroll.refreshComplete');
            $scope.$broadcast('scroll.infiniteScrollComplete');
        }); 
    }

    $scope.refresh_close_order = function() {
        $scope.close_order_list = [];
        $scope.has_more_close_order = true;
        $scope.close_order_page_index = 0;
        $scope.load_more_close_order();
    }

    $scope.load_more_close_order = function() {
        CloseOrderService.request_order_list($scope.close_order_page_index + 1, 20, function(protocol) {
            $scope.close_order_page_index = $scope.close_order_page_index + 1;
            console.log($scope.close_order_page_index);
            protocol.data.forEach(function(value) {
                $scope.close_order_list.push(value);
            });

            if(protocol.data.length === 0) {
                $scope.has_more_close_order = false;
            }

            $scope.$broadcast('scroll.refreshComplete');
            $scope.$broadcast('scroll.infiniteScrollComplete');
        }); 
    }

    var order_interval = $interval(function() {
        if ($scope.order_list.length > 0) {
            for (var i = 0; i < $scope.order_list.length; i++) {
                var o = $scope.order_list[i];
                o.profit = $scope.order_profit(o);
                var expired = new Date(o.expired);
                var now = new Date();

                var tick = now.getTime() + $rootScope.server_time_tick;
                var remaining = (expired.getTime() - tick) / 1000;
                o.remaining = remaining;
                if(o.remaining <= 0) {
                    $scope.order_list.splice(i, 1);
                }
            }
        }
    }, 1000);
    
    $scope.$on('$destroy', function() {
        $interval.cancel(order_interval);
    });
});
