angular.module('starter.services')

.service('HistoryQouteService', function($http, AppConfigService) {
    this.request_history = function(symbol, period, complete) {
        var url = AppConfigService.api_url + "historyqoute/" + period;
        $http.get(url, { 
            "timeout": 10000,
            "params": { "symbol": symbol }
        })
        
        .success(function(protocol) {
            if (protocol.return_code === "SUCCESS") {
                if (complete) {
                    complete(protocol.data);
                }
            }
        });
    }
    
    this.build_ma_data = function (count, data) {
        var result = [];
        for (var i = 0, len = data.length; i < len; i++) {
            if (i < count) {
                result.push('-');
                continue;
            }
            var sum = 0;
            
            for (var j = 0; j < count; j++) {
                sum += data[i - j][1];
            }
            result.push(+(sum / count).toFixed(3));
        }
        return result;
    }

    return this;
});
