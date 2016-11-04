/**
 * Created by liekkas.zeng on 2015/1/7.
 */
angular.module('ng-echarts',[])
    .directive('ngEcharts',[function(){
        return {
            link: function(scope,element,attrs,ctrl){
                function refreshChart(){
                    if (scope.option) {
                        var theme = (scope.config && scope.config.theme)
                            ? scope.config.theme : 'default';
                        var chart = echarts.init(element[0],theme);

                        scope.stock_chart = chart;

                        chart.setOption(scope.option);
                        chart.resize();
                    }
                };

                //自定义参数 - config
                // event 定义事件
                // theme 主题名称
                // dataLoaded 数据是否加载

                scope.$watch(
                    function () { return scope.config; },
                    function (value) {if (value) {refreshChart();}},
                    true
                );

                //图表原生option
                scope.$watch(
                    function () { return scope.option; },
                    function (value) {if (value) {refreshChart();}},
                    true
                );
            },
            scope:{
                option:'=ecOption',
                config:'=ecConfig'
            },
            restrict:'EA'
        }
    }]);
