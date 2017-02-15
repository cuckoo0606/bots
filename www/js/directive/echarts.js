angular.module('ng-echarts',[])

.service('$echartsDelegate', ionic.DelegateService([
    'setOption', 'on'
]))

.controller('$echarts', function($scope, $element, $attrs, $ionicHistory, $echartsDelegate) {
    var chart = echarts.init($element[0]);

    var instance = $echartsDelegate._registerInstance(
        chart, $attrs.delegateHandle, function() {
            return $ionicHistory.isActiveScope($scope);
        }
    );

    $scope.$watch('option', function(value) {
        if (value) {
            chart.setOption(value);
        }
    }, true);

    $scope.$on('$destroy', function() {
        instance();
    });
})

.directive('ngEcharts', [ function() {
    return {
        restrict: 'E',
        controller: '$echarts',
        scope: {
            option:'=ecOption',
        },
    }
}]);
