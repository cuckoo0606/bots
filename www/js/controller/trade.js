angular.module('starter.controllers')

.controller('TradeCtrl', function($scope, $filter, $rootScope, $timeout, $interval, $stateParams, $echartsDelegate,
            $ionicModal, QouteService, OrderService, UserService, HistoryQouteService, CloseOrderService) {
    $scope.chart_period = "m5";

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
	var aCss = [];
	var nCss = [];
	
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
                console.log($rootScope.trade_order_list);
                
                aCss = document.styleSheets[2];
		        nCss = document.styleSheets[2].cssRules;
		        for(var i = 0;i<nCss.length;i++){
		        	if(nCss[i].name==='animate_width'){
		        		aCss.deleteRule(i);
		        		aCss.insertRule("@keyframes animate_width{from{width:"+value.remaining/value.cycle+"%;}to{width: 0%;}}",i)
		        	}
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

    var has_new_history = function(dt_now, dt_chart, period) {
        var sub = dt_now.getTime() - dt_chart.getTime();
        sub = sub / 1000;

        if (period == "m1") {
            if (sub / 60 >= 1) {
                return true;
            }
        }
        else if (period == "m5") {
            if (sub / 60 / 5 >= 1) {
                return true;
            }
        }
        else if (period == "m15") {
            if (sub / 60 / 15 >= 1) {
                return true;
            }
        }
        else if (period == "m30") {
            if (sub / 60 / 30 >= 1) {
                return true;
            }
        }
        else if (period == "h1") {
            if (sub / 60 / 60 >= 1) {
                return true;
            }
        }
        else if (period == "d1") {
            if (sub / 60 / 60 / 24 >= 1) {
                return true;
            }
        }

        return false;
    }

    function change_chart_data(history_list) {
        $scope.chart_data = history_list;
        var dates = history_list.map(function(value) {
            return value.datetime;
        });

        var data = history_list.map(function(value) {
            return [ value.open, value.close, value.low, value.high];
        });
        if (data.length > 0) {
            data[data.length - 1][1] = $rootScope.qoute.value;
        }
       
        var line_data = history_list.map(function(value) {
            return value.close;
        });
        if (line_data.length > 0) {
            line_data[line_data.length - 1] = $rootScope.qoute.value;
        }

        var diff = HistoryQouteService.build_diff_data(12, 26, data);
        var dea = HistoryQouteService.build_dea_data(9, diff);
        var macd = HistoryQouteService.build_macd_data(data, diff, dea);
        var m5 = HistoryQouteService.build_ma_data(5, data);
        var m10 = HistoryQouteService.build_ma_data(10, data);
        var m20 = HistoryQouteService.build_ma_data(20, data);
        var m30 = HistoryQouteService.build_ma_data(30, data);

        $scope.diff = diff;
        $scope.dea = dea;
        $scope.macd = macd;

        $scope.chart_option = {
            animation: false,
            backgroundColor: 'rgb(25, 25, 26)',
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
                            if ($scope.chart_period == "d1") {
                                var time = value.split(" ")[0];
                                var split = time.split("-");
                                return split[1] + "/" + split[2];
                            }
                            else {
                                var time = value.split(" ")[1];
                                var split = time.split(":");
                                return split[0] + ":" + split[1];
                            }
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
                    splitLine: { 
                        show: true,
                        lineStyle: {
                            color: 'rgb(35, 34, 38)',
                        }
                    }
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
                    markPoint: {
                        symbol: "rect",
                        animation: false,
                        symbolSize: [60, 18],
                        symbolOffset: [-21, 0],
                        data: [
                        { 
                            name: '最新价', 
                            x: '100%',
                            yAxis: line_data[line_data.length - 1],
                            value: line_data[line_data.length - 1],
                            label: {
                                normal: {
                                    position: [ 0, 2 ],
                                    textStyle: {
                                        color: "#FFFFFF",
                                    },
                                    formatter: function(params) {
                                        return params.value.toFixed($rootScope.qoute.decimal);
                                    },
                                }
                            },
                        }
                        ]
                    },
                    markLine: {
                        symbolSize: 0,
                        animation: false,
                        label: {
                            normal: {
                                show: false,
                            }
                        },
                        lineStyle: {
                            normal: {
                                type: 'dashed',
                                width: 1,
                            },
                        },
                        data: [
                            [
                            {
                                name: $rootScope.qoute.value,
                                x: 0,
                                yAxis: line_data[line_data.length - 1],
                            },
                            {
                                name: $rootScope.qoute.value,
                                x: '100%',
                                yAxis: line_data[line_data.length - 1],
                            }
                            ],
                        ]
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
                            color: 'rgb(25, 25, 26)',
                            color0: 'rgb(19, 233, 236)',
                            borderColor: 'rgb(250, 46, 66)',
                            borderColor0: 'rgb(19, 233, 236)',
                        }
                    }
                },
                {
                    name: 'ma5',
                    type: 'line',
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    data: $scope.chart_type === "stock" ? m5 : [],
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
                    data: $scope.chart_type === "stock" ? m10 : [],
                    smooth: true,
                    showSymbol: false,
                    lineStyle: {
                        normal: {
                            width: 1,
                            color: '#86da2b'
                        }
                    }
                },
                {
                    name: 'ma20',
                    type: 'line',
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    data: $scope.chart_type === "stock" ? m20 : [],
                    smooth: true,
                    showSymbol: false,
                    lineStyle: {
                        normal: {
                            width: 1,
                            color: '#ff5382'
                        }
                    }
                },
                {
                    name: 'ma30',
                    type: 'line',
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    data: $scope.chart_type === "stock" ? m30 : [],
                    smooth: true,
                    showSymbol: false,
                    lineStyle: {
                        normal: {
                            width: 1,
                            color: '#3d8ef6'
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
                            width: 1,
                            color: '#00ffff'
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
                            width: 1,
                            color: '#fe337f'
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
                            color: 'rgb(31, 198, 91)',
                            borderColor: 'black',
                        }
                    },
                    data: macd,
                },
            ]
        };
    }

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
        angular.element(document.querySelectorAll(".trade-chart-period")).removeClass("active");
        angular.element(document.querySelectorAll(".trade-chart-period." + period)).addClass("active");

        HistoryQouteService.request_history($scope.market, $scope.code, period, function(history_list) {
            history_list.reverse();
            change_chart_data(history_list);
            $scope.history_qoute = history_list[history_list.length - 1];
        });
    }

    var qoute_watcher = $rootScope.$watch('qoute', function(qoute) {
        if($scope.chart_option) {
            var line_chart = $scope.chart_option.series[0];
            line_chart.data[line_chart.data.length - 1] = qoute.value;

            var stock = $scope.chart_option.series[1];
            stock.data[stock.data.length - 1][1] = qoute.value;
            if (qoute.value > stock.data[stock.data.length - 1][3]) {
                stock.data[stock.data.length - 1][3] = qoute.value;
            }
            if (qoute.value < stock.data[stock.data.length - 1][2]) {
                stock.data[stock.data.length - 1][2] = qoute.value;
            }

            var mark_point = $scope.chart_option.series[0].markPoint;
            mark_point.data[0].value = qoute.value;
            mark_point.data[0].yAxis = qoute.value;

            var mark_line = $scope.chart_option.series[0].markLine;
            mark_line.data[0][0].yAxis = qoute.value;
            mark_line.data[0][1].yAxis = qoute.value;
                
            var dates = $scope.chart_option.xAxis[0].data;
            if (dates && $rootScope.qoute) {
                var dt_now = new Date($rootScope.qoute.time.replace(/-/g, "/"));
                var dt_chart = new Date(dates[dates.length - 1].replace(/-/g, "/"));
                if (has_new_history(dt_now, dt_chart, $scope.chart_period)) {
                    $scope.change_chart_period($scope.chart_period)
                }
            }
        }
    }, true);

    $scope.change_chart_period($scope.chart_period);
    $scope.$on('$destroy', function() {
        if (qoute_watcher) {
            qoute_watcher();
        }
        if (order_interval) {
            $interval.cancel(order_interval);
        }
        if ($scope.history_interval) {
            $interval.cancel(history_interval);
        }
    });
});
