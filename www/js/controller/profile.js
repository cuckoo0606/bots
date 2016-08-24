angular.module('starter.controllers')

.controller('ProfileCtrl', function($scope, $rootScope, OrderService, LimitOrderService, CloseOrderService) {
    OrderService.init(function(){ });
    LimitOrderService.init(function(){ });
    CloseOrderService.init(function(){ });
    
    $scope.order_list = OrderService.order_list;
    $scope.limit_order_list = LimitOrderService.order_list;
    $scope.close_order_list = CloseOrderService.order_list;

    $scope.order_quantity_sum = function() {
        var sum = 0;
        angular.forEach($scope.order_list, function(value) {
            sum += value.Quantity;
        });
        return sum;
    }

    $scope.limit_order_quantity_sum = function() {
        var sum = 0;
        angular.forEach($scope.limit_order_list, function(value) {
            sum += value.Quantity;
        });
        return sum;
    }
});
