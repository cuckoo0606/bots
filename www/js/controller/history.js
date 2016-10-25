angular.module('starter.controllers')

.controller('HistoryCtrl', function($scope, $rootScope, $stateParams, $ionicModal, $ionicSlideBoxDelegate, OrderService, CloseOrderService) {
    $scope.order_page_index = 1;
    $scope.close_order_page_index = 1;

    $scope.order_list = [];
    $scope.has_more_order = true;
    $scope.close_order_list = [];
    $scope.has_more_close_order = true;

    $scope.category_index = parseInt($stateParams.index);
    $scope.order_list = OrderService.order_list;
    $scope.close_order_list = CloseOrderService.order_list;
    
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
        $scope.order_page_index = 1;
        $scope.load_more_order();
    }

    $scope.load_more_order = function() {
        OrderService.request_order_list($scope.order_page_index + 1, 20, function(protocol) {
            $scope.order_page_index = $scope.order_page_index + 1;
            protocol.data.forEach(function(value) {
                $scope.order_list.push(value);
            });

            if(protocol.data.length == 0) {
                $scope.has_more_order = false;
            }

            $scope.$broadcast('scroll.refreshComplete');
            $scope.$broadcast('scroll.infiniteScrollComplete');
        }); 
    }

    $scope.refresh_close_order = function() {
        $scope.close_order_list = [];
        $scope.has_more_close_order = true;
        $scope.close_order_page_index = 1;
        $scope.load_more_close_order();
    }

    $scope.load_more_close_order = function() {
        console.log($scope.close_order_page_index + 1);
        CloseOrderService.request_order_list($scope.close_order_page_index + 1, 20, function(protocol) {
            $scope.close_order_page_index = $scope.close_order_page_index + 1;
            protocol.data.forEach(function(value) {
                $scope.close_order_list.push(value);
            });

            if(protocol.data.length == 0) {
                $scope.has_more_close_order = false;
            }

            $scope.$broadcast('scroll.refreshComplete');
            $scope.$broadcast('scroll.infiniteScrollComplete');
        }); 
    }
});
