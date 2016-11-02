angular.module('starter.controllers')

.controller('TradeCtrl', function($scope, $filter, $rootScope, $timeout, $interval, $stateParams, 
            $ionicModal, QouteService, OrderService, UserService, HistoryQouteService, CloseOrderService) {
    $scope.chart_period = "m5";

    $scope.history_loading = false;
    $scope.chart_data = [];
    $rootScope.trade_order_list = [];

    $scope.mode = $stateParams.mode;
    if ($scope.mode == "default") {
    	$scope.mode = QouteService.category_list[0].mode;
    }
    $scope.market = $stateParams.market;
    if ($scope.market == "default") {
    	$scope.market = QouteService.qoute_list[0].market;
    }
    $scope.code = $stateParams.code;
    if ($scope.code == "default") {
    	$scope.code = QouteService.qoute_list[0].code;
    }

    $rootScope.qoute = QouteService.qoute($scope.mode, $scope.market, $scope.code);
    $rootScope.trade = QouteService.trade($scope.mode, $scope.market, $scope.code);

    $scope.order_params.cycle = $rootScope.trade.cycle[0];
    $scope.order_params.amount = $rootScope.trade.amounts[0];

    $scope.change_cycle = function(c) {
        $scope.order_params.cycle = c;
    }

    $scope.change_amount = function(a) {
        $scope.order_params.amount = a;
        $scope.order_params.other_amount = "";
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
            protocol.data.forEach(function(value) {
                value.profit = $scope.order_profit(value);
                value.qoute = QouteService.qoute(value.mode, value.assets.market, value.assets.code);
                var expired = new Date(value.expired);
                var now = new Date();

                var tick = now.getTime() + $rootScope.server_time_tick;
                var remaining = (expired.getTime() - tick) / 1000;
                value.remaining = remaining;
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


    $scope.refresh_order();

    $scope.chart_config = {
        "theme": "default",
        "dataLoaded": true,
    }

    function change_chart_data(history_list) {
        $scope.chart_data = history_list;
        var dates = history_list.map(function(value) {
            return value.datetime;
        });

        var data = history_list.map(function(value) {
            return [ value.open, value.close, value.low, value.high];
        });
       
        var line_data = history_list.map(function(value) {
            return value.close;
        });

        function calculateMA(dayCount, data) {
            var result = [];
            for (var i = 0, len = data.length; i < len; i++) {
                if (i < dayCount) {
                    result.push('-');
                    continue;
                }
                var sum = 0;
                for (var j = 0; j < dayCount; j++) {
                    sum += data[i - j][1];
                }
                result.push(sum / dayCount);
            }
            return result;
        }

        var diff = HistoryQouteService.build_diff_data(12, 26, data);
        var dea = HistoryQouteService.build_dea_data(9, diff);
        var macd = HistoryQouteService.build_macd_data(data, diff, dea);

        $scope.stock_dates = dates;
        $scope.stock_data = data;
        $scope.stock_m5 = calculateMA(5, data);
        $scope.stock_m10 = calculateMA(10, data);
        $scope.stock_m20 = calculateMA(20, data);
        $scope.stock_m30 = calculateMA(30, data);
        $scope.diff = diff;
        $scope.dea = dea;
        $scope.macd = macd;

        $scope.chart_option = {
            animation: false,
            backgroundColor: 'black',
            legend: {
                show: false,
            },
            tooltip: {
                show: false,
            },
            grid: [
                {
                    top: 20,
                    bottom: 5,
                    left: 5,
                    right: 60,
                    height: 300,
                },
                {
                    top: 355,
                    bottom: 5,
                    left: 5,
                    right: 60,
                    height: 100,
                },
            ],
            xAxis: [
                {
                    gridIndex: 0,
                    type: 'category',
                    data: dates,
                    axisLine: { 
                        show: false,
                    },
                    axisTick: {
                        show: false,
                    },
                    axisLabel: {
                        textStyle: { color: 'rgb(100, 100, 100)' },
                        formatter: function (value, index) {
                            var time = value.split(" ")[1];
                            var split = time.split(":");
                            return split[0] + ":" + split[1];
                        }   
                    },
                },
                {
                    gridIndex: 1,
                    type: 'category',
                    data: dates,
                    axisLine: { 
                        show: false,
                    },
                    axisTick: {
                        show: false,
                    },
                    axisLabel: {
                        show: false,
                    },
                },
            ],
            yAxis: [
                {
                    gridIndex: 0,
                    position: "right",
                    scale: true,
                    axisLabel: {
                        textStyle: { color: 'rgb(100, 100, 100)' },
                        formatter: function (value, index) {
                            return value.toFixed($rootScope.qoute.decimal);
                        }   
                    },
                    axisLine: { 
                        show: false,
                    },
                    axisTick: {
                        show: false,
                    },
                    splitLine: { show: false }
                },
                {
                    gridIndex: 1,
                    position: "right",
                    scale: true,
                    axisLabel: {
                        textStyle: { color: 'rgb(100, 100, 100)' },
                        formatter: function (value, index) {
                            if (value >= 0) {
                                return "+" + value.toFixed(4);
                            }
                            return value.toFixed(4);
                        }   
                    },
                    axisLine: { 
                        show: false,
                    },
                    axisTick: {
                        show: false,
                    },
                    splitLine: { show: false }
                },
            ],
            dataZoom: [
                { 
                    xAxisIndex: [0, 1], 
                    startValue: dates[dates.length - 61],
                    endValue: dates[dates.length - 1],
                    type : 'inside' },
            ],
            series: [
                {   
                    name: 'line',
                    type: 'line',
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    data: $scope.chart_type === "line" ? line_data : [], 
                    showSymbol: false,
                    lineStyle: {
                        normal: {
                            width: 1,
                            color: 'rgb(253, 209, 42)',
                        }   
                    },
                    areaStyle: {
                        normal: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgb(87, 72, 38)'
                            }, {
                                offset: 1,
                                color: 'rgb(47, 44, 40)'
                            }])
                        },
                    },
                },  
                {
                    name: 'stick',
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    type: 'candlestick',
                    data: $scope.chart_type === "stock" ? data : [],
                    itemStyle: {
                        normal: {
                            color: 'black',
                            color0: 'rgb(20, 190, 82)',
                            borderColor: 'red',
                            borderColor0: 'rgb(20, 190, 82)',
                        }
                    }
                },
                {
                    name: 'ma5',
                    type: 'line',
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    data: $scope.chart_type === "stock" ? calculateMA(5, data) : [],
                    smooth: true,
                    showSymbol: false,
                    lineStyle: {
                        normal: {
                            width: 1
                        }
                    }
                },
                {
                    name: 'ma10',
                    type: 'line',
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    data: $scope.chart_type === "stock" ? calculateMA(10, data) : [],
                    smooth: true,
                    showSymbol: false,
                    lineStyle: {
                        normal: {
                            width: 1
                        }
                    }
                },
                {
                    name: 'ma20',
                    type: 'line',
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    data: $scope.chart_type === "stock" ? calculateMA(20, data) : [],
                    smooth: true,
                    showSymbol: false,
                    lineStyle: {
                        normal: {
                            width: 1
                        }
                    }
                },
                {
                    name: 'ma30',
                    type: 'line',
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    data: $scope.chart_type === "stock" ? calculateMA(30, data) : [],
                    smooth: true,
                    showSymbol: false,
                    lineStyle: {
                        normal: {
                            width: 1
                        }
                    }
                },
                {
                    name: 'diff',
                    type: 'line',
                    data: diff,
                    smooth: true,
                    showSymbol: false,
                    xAxisIndex: 1,
                    yAxisIndex: 1,
                    lineStyle: {
                        normal: {
                            width: 1
                        }
                    }
                },
                {
                    name: 'ema',
                    type: 'line',
                    data: dea,
                    smooth: true,
                    showSymbol: false,
                    xAxisIndex: 1,
                    yAxisIndex: 1,
                    lineStyle: {
                        normal: {
                            width: 1
                        }
                    }
                },
                {
                    name: 'macd',
                    type: 'bar',
                    xAxisIndex: 1,
                    yAxisIndex: 1,
                    itemStyle: {
                        normal: {
                            color: '#006600',
                            borderColor: 'black',
                        }
                    },
                    data: macd,
                },
            ]
        };
    }

    var history_interval = $interval(function() {
        if ($scope.chart_data.length > 0) {
        }
    }, 1000);

    var order_interval = $interval(function() {
        if ($rootScope.trade_order_list.length > 0) {
            for (var i = 0; i < $rootScope.trade_order_list.length; i++) {
                var o = $rootScope.trade_order_list[i];
                o.profit = $scope.order_profit(o);
                var expired = new Date(o.expired);
                var now = new Date();

                var tick = now.getTime() + $rootScope.server_time_tick;
                var remaining = (expired.getTime() - tick) / 1000;
                o.remaining = remaining;
                if(o.remaining <= 0) {
                    $rootScope.trade_order_list.splice(i, 1);

                    if (o == $scope.order_result.order) {
                        $scope.order_result.status = "POST";
                        $scope.order_result.message = "正在完成订单";
                        
                        var check_order = function() {
                            OrderService.request_order(o._id, function(protocol) {
                                if (protocol.status === 110) {
                                    $scope.order_result.status = "FINISH";
                                    $scope.order_result.message = "交易完成";
                                    $scope.order_result.order = protocol;
                                }
                                else {
                                    $timeout(check_order, 1000);                
                                }
                            });
                        }

                        $timeout(check_order, 1000);                
                    }
                }
            }
        }
    }, 1000);

    $scope.chart_type = "stock";

    $scope.change_chart_type = function(type) {
        angular.element(document.querySelectorAll(".trade-chart-type")).removeClass("active");
        angular.element(document.querySelectorAll(".trade-chart-type." + type)).addClass("active");
        $scope.chart_type = type;
        change_chart_data($scope.chart_data);
    }

    $scope.change_chart_period = function(period) {
        $scope.chart_period = period;
        $scope.history_loading = true;
        angular.element(document.querySelectorAll(".trade-chart-period")).removeClass("active");
        angular.element(document.querySelectorAll(".trade-chart-period." + period)).addClass("active");

        HistoryQouteService.request_history($scope.market, $scope.code, period, function(history_list) {
            history_list.reverse();
            change_chart_data(history_list);
            $scope.history_loading = false;
            $scope.history_qoute = history_list[history_list.length - 1];
        });
    }

    $scope.change_chart_period($scope.chart_period);
    $scope.$on('$destroy', function() {
        $interval.cancel(order_interval);
        $interval.cancel(history_interval);
    });
});
