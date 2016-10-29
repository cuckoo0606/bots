angular.module('starter.controllers')

.controller('TradeCtrl', function($scope, $filter, $rootScope, $timeout, ionicDatePicker, $echarts, $interval, $stateParams, 
            $ionicModal, QouteService, OrderService, UserService, HistoryQouteService, CloseOrderService) {
    
    $scope.chart_period = "m1";
    $scope.chart_period_m_list = [
        { "name" : "m1", "text" : " 1分钟" },
        { "name" : "m5", "text" : " 5分钟" },
        { "name" : "m15", "text" : "15分钟" },
        { "name" : "m30", "text" : "30分钟" },
    ];
    $scope.chart_period_m = $scope.chart_period_m_list[0];

    $scope.history_loading = false;
    $scope.chart_data = [];
    $scope.mode = $stateParams.mode;
    $scope.market = $stateParams.market;
    $scope.code = $stateParams.code;

    $scope.order_list = OrderService.order_list;
    $rootScope.qoute = QouteService.qoute($scope.mode, $scope.market, $scope.code);
    $scope.addfavo = false;
    $scope.collection = [];
    $scope.indexList = ["指标","MACD","RSI","DMI","DMA","MACD","RSI","DMI","DMA","MACD","RSI","DMI","DMA","MACD"];
    $scope.account_list = []

    // OrderService.init(function(){ });

<<<<<<< HEAD
//  OrderService.init(function(){ });
=======
>>>>>>> c777fef37462b5fd43e0487942287760c6a5b36d

    $scope.stockChartId = $echarts.generateInstanceIdentity();
    $scope.stockOption = {
        animation: false,
        backgroundColor: 'black',
        grid: [
            {
                left: 0,
                top: 10,
                bottom: 0,
                right: 'auto',
                height: 300,
            },
            {
                left: 0,
                top: 325,
                bottom: 0,
                right: 'auto',
                height: 80,
            },
        ],
        tooltip: { 
            show: false,
            showContent: false,
        },
        xAxis: [
            {
                type: 'category',
                data: [],
                axisLine: { show: false },
                axisTick: { show: false },
                axisLabel: { show: false },
                splitLine: { show: false },
                splitArea: { show: false },
            },
            {
                type: 'category',
                gridIndex: 1,
                data: [],
                axisLine: { show: false },
                axisTick: { show: false },
                axisLabel: { show: false },
                splitLine: { show: false },
                splitArea: { show: false },
            }
        ],
        yAxis: [
            {
                min: 'dataMin',
                max: 'dataMax',
                position: 'right',
                axisLine: { show: false },
                splitLine: { 
                    show: true, 
                    lineStyle: {
                        color: 'rgb(35,35,45)',
                        type: 'dotted',
                    }
                },
                axisLabel: {
                    textStyle: { color: 'rgb(185, 60, 65)' },
                    formatter: function (value, index) {
                        return value.toFixed(0);
                    }
                }
            },
            {
                min: 'dataMin',
                max: 'dataMax',
                position: 'right',
                gridIndex: 1,
                axisLine: { show: false },
                axisTick: { show: false },
                axisLabel: { show: false },
                splitLine: { show: false },
                splitArea: { show: false },
            }
        ],
        dataZoom: [
            { xAxisIndex: [0, 1], start: 50, end: 100, type : 'inside' },
        ],
        series: [
            {
                name: 'line',
                type: 'line',
                data: [],
                showSymbol: false,
                lineStyle: {
                    normal: {
                        width: 1
                    }
                }
            },
            {
                type: 'candlestick',
                name: 'stock',
                data: [],
                itemStyle: {
                    normal: {
                        color: 'black',
                        color0: 'rgb(80, 165, 50)',
                        borderColor: 'rgb(150, 55, 75)',
                        borderColor0: 'rgb(80, 165, 50)'
                    }
                }
            },
            {
                name: 'MA5',
                type: 'line',
                data: [],
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    normal: {
                        width: 1
                    }
                }
            },
            {
                name: 'MA10',
                type: 'line',
                data: [],
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    normal: {
                        width: 1
                    }
                }
            },
            {
                name: 'MA20',
                type: 'line',
                data: [],
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    normal: {
                        width: 1
                    }
                }
            },
            {
                name: 'MA30',
                type: 'line',
                data: [],
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    normal: {
                        width: 1
                    }
                }
            },
            {
                name: 'DIFF',
                type: 'line',
                data: [],
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
                name: 'EMA',
                type: 'line',
                data: [],
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
                name: 'MACD',
                type: 'bar',
                xAxisIndex: 1,
                yAxisIndex: 1,
                itemStyle: {
                    normal: {
                        color: '#006600',
                        borderColor: 'black',
                    }
                },
                data: [],
            },
        ]
    };

    function change_chart_data(history_list) {
        $scope.chart_data = history_list;
        var dates = history_list.map(function(value) {
            return value.time;
        });

        var data = history_list.map(function(value) {
            return [ value.open, value.close, value.low, value.high];
        });
       
        var line_data = history_list.map(function(value) {
            return value.close;
        });

        var diff = HistoryQouteService.build_diff_data(12, 26, data);
        var dea = HistoryQouteService.build_dea_data(9, diff);
        var macd = HistoryQouteService.build_macd_data(data, diff, dea);
            
        $scope.stockOption = {
            xAxis: [
                {
                    data: dates,
                },
                {
                    data: dates,
                }
            ],
            series: [
                {
                    data: $scope.chart_type === "line" ? line_data : [],
                },
                {
                    data: $scope.chart_type === "stock" ? data : [],
                },
                {
                    data: $scope.chart_type === "stock" ? HistoryQouteService.build_ma_data(5, data) : [],
                },
                {
                    data: $scope.chart_type === "stock" ? HistoryQouteService.build_ma_data(10, data) : [],
                },
                {
                    data: $scope.chart_type === "stock" ? HistoryQouteService.build_ma_data(20, data) : [],
                },
                {
                    data: $scope.chart_type === "stock" ? HistoryQouteService.build_ma_data(30, data) : [],
                },
                {
                    data: diff,
                },
                {
                    data: dea,
                },
                {
                    data: macd,
                },
            ]
        };
    }

    var history_interval = $interval(function() {
        if ($scope.chart_data.length > 0) {
            var last = $scope.chart_data[$scope.chart_data.length - 1];
            last.Close = $scope.qoute.Ask;
            if ($scope.qoute.Ask > last.High) {
                last.High = $scope.qoute.Ask;
            }
            if ($scope.qoute.Ask < last.Low) {
                last.Low = $scope.qoute.Ask;
            }
            change_chart_data($scope.chart_data);

            var timestamp = new Date(last.DateTime);
            timestamp.setMinutes(timestamp.getMinutes() + 1);
            if ($scope.history_loading == false && new Date() > timestamp) {
                $scope.history_loading = true;
                HistoryQouteService.request_history($scope.qid, $scope.chart_period, function(history_list) {
                    $scope.history_loading = false;
                    history_list.reverse();
                    change_chart_data(history_list);
                });
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
        angular.element(document.querySelectorAll(".trade-chart-period ul li")).removeClass("active");
        angular.element(document.querySelectorAll(".trade-chart-period ul li." + period)).addClass("active");

        if (period == "h1") {
            angular.element(document.querySelectorAll(".trade-chart-period ul li.hour")).addClass("active");
        }
        
        if ([ "m1", "m5", "m15", "m30" ].indexOf(period) >= 0) {
            angular.element(document.querySelectorAll(".trade-chart-period ul li.m")).addClass("active");
        }

        HistoryQouteService.request_history($scope.market, $scope.code, period, function(history_list) {
            console.log(history_list);
            history_list.reverse();
            change_chart_data(history_list);
            $scope.history_loading = false;
            
            $timeout(function() {
                var body = angular.element(document.querySelector('body'));
                body.append("<iframe src='/favicon.ico'></iframe>");

                $timeout(function() {
                    angular.element(document.querySelector('iframe')).remove();
                }, 100);
            }, 100);
        });
    }

    $scope.change_chart_period($scope.chart_period);

    $scope.$on('$destroy', function() {
        $interval.cancel(history_interval);
    });
    
    $scope.add_to_favo = function () {
        $scope.addfavo = !$scope.addfavo;
        if ($scope.addfavo) {
            angular.element(document.querySelector(".collection")).addClass("ion-ios-heart").removeClass("ion-ios-heart-outline");
            $scope.collection.push($scope.qoute);
            console.log($scope.collection)
        }else {
            angular.element(document.querySelector(".collection")).addClass("ion-ios-heart-outline").removeClass("ion-ios-heart");
            $scope.collection.splice(-1,1);
            console.log($scope.collection)
        }
    };

    $scope.change_index = function (index) {
        $scope.list_index = index;
    }


});
