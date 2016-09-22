angular.module('starter.services')

.service('QouteService', function($http, $interval, $filter, AppConfigService) {
    var service = this;
    this.qoute_list = [];
    this.category_list = [];

    this.qoute = function(id) {
        var result = $filter('filter')(service.qoute_list, { Id: id });
        if (result.length > 0) {
            return result[0];
        }
        return false;
    }

    this.request_qoute = function(id, complete) {
        var url = AppConfigService.api_url + "qoute/get";
        $http.get(url, { 
            "timeout": 10000, 
            "params": { "id": id } 
        })
        
        .success(function(protocol) {
            if (protocol.return_code === "SUCCESS") {
                if (complete) {
                    complete(protocol.data);
                }
            }
        });
    }

    this.request_qoute_list = function(complete) {
        var url = AppConfigService.api_url + "qoute/list";
        $http.get(url, { "timeout": 10000 })
        
        .success(function(protocol) {
            if (protocol.return_code === "SUCCESS") {
                if (complete) {
                    complete(protocol.data);
                }
            }
        });
    }

    this.request_category = function(complete) {
        var url = AppConfigService.api_url + "qoute/category";
        $http.get(url, { "timeout": 10000 })

        .success(function(protocol) {
            if (protocol.return_code === "SUCCESS") {

                if (complete) {
                    complete(protocol.data);
                }
            }
        });
    };

    this.init = function(complete) {
        this.request_category(function(category_list) {
            angular.forEach(category_list, function(value) {
                service.category_list.push(value);
            });
            if (complete) {
                complete();
            }
        });
        
        $interval(function() {
            service.request_qoute_list(function(qoute_list) {
                angular.forEach(qoute_list, function(value) {
                    var q = service.qoute(value.Id);
                    if(!q) {
                        value.ChangeValue = "+0.00";
                        value.ChangePercent = "+0.00%";
                        service.qoute_list.push(value);
                        q = value;
                    }

                    if (value.Bid != q.Bid) {
                        var sub = q.Ask - q.Open;
                        var sub_percent = sub / q.Open;
                        q.ChangeValue = sub.toFixed(2);
                        q.ChangePercent = (sub_percent * 100).toFixed(2) + "%";
                        if (sub >= 0) {
                            q.ChangeValue = "+" + q.ChangeValue;
                            q.ChangePercent = "+" + q.ChangePercent;
                        }
                    }
                    if (value.Bid > q.Bid) {
                        q.Fluctuation = true;
                    }
                    else if(value.Bid < q.Bid) {
                        q.Fluctuation = false;
                    }
                    q.Open = value.Open;
                    q.Close = value.Close;
                    q.High = value.High;
                    q.Low = value.Low;
                    q.Bid = value.Bid;
                    q.Ask = value.Ask;
                    q.Time = value.Time;
                });
            });
        }, 1000);
    };

    return this;
});
