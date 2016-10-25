angular.module('starter.controllers')

.controller('HistoryCtrl', function($scope, $rootScope, $stateParams, $ionicModal, $ionicSlideBoxDelegate, OrderService, CloseOrderService) {
    $scope.category_index = parseInt($stateParams.index);
    $scope.order_list = OrderService.order_list;
    $scope.close_order_list = CloseOrderService.order_list;
    OrderService.init(function(){ });
    CloseOrderService.init(function(){ });
    
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
});
