angular.module('starter.controllers')

.controller('QouteCtrl', function($scope, $interval, $ionicSlideBoxDelegate, $timeout, QouteService) {
    $scope.category_index = 0;
    $scope.qoute_list = QouteService.qoute_list;
    $scope.category_list = QouteService.category_list;

    $scope.slide_change = function(index) {
        if (isNaN(index)) {
            return;
        }
        $scope.category_index = index;
    };

    $scope.change_category = function(index) {
        $scope.category_index = index;
        
        var slide = $ionicSlideBoxDelegate.$getByHandle('slide-qoute');
        if (slide) {
            slide.slide(index);
        }
    };
});
