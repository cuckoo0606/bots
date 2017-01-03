angular.module('starter.services')

.service('HistoryQouteService', function($http, AppConfigService) {
    this.request_history = function(market, code, period, complete) {
        var url = "";
        if(period == "m1") {
            url = AppConfigService.qoute_url + "minutes/1";
        }
        else if(period == "m5") {
            url = AppConfigService.qoute_url + "minutes/5";
        }
        else if(period == "m15") {
            url = AppConfigService.qoute_url + "minutes/15";
        }
        else if(period == "m30") {
            url = AppConfigService.qoute_url + "minutes/30";
        }
        else if(period == "h1") {
            url = AppConfigService.qoute_url + "hours";
        }
        else if(period == "d1") {
            url = AppConfigService.qoute_url + "days";
        }

        $http.get(url, { 
            "timeout": 10000,
            "params": { "market": market, "code": code, "limit": 50 }
        })
        
        .success(function(protocol) {
            if (complete) {
                complete(protocol.data);
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
            result.push(sum / count);
        }
        return result;
    }
    
    this.build_diff_data = function (m_short, m_long, data) {
        var result = [];
        var pre_emashort = 0;
        var pre_emalong = 0;
        for (var i = 0, len = data.length; i < len; i++) {
            var ema_short = data[i][1];
            var ema_long = data[i][1];
            
            if (i != 0) {
                ema_short = (1.0 / m_short) * data[i][1] + (1 - 1.0 / m_short) * pre_emashort;
                ema_long = (1.0 / m_long) * data[i][1] + (1 - 1.0 / m_long) * pre_emalong;
            }

            pre_emashort = ema_short;
            pre_emalong = ema_long;
            var diff = ema_short - ema_long;

            result.push(diff);
        }

        return result;
    }
    
    this.build_dea_data = function (m, diff) {
        var result = [];
        var pre_ema_diff = 0;
        for (var i = 0, len = diff.length; i < len; i++) {
            var ema_diff = diff[i];
            
            if (i != 0) {
                ema_diff = (1.0 / m) * diff[i] + (1 - 1.0 / m) * pre_ema_diff;
            }
            pre_ema_diff = ema_diff;

            result.push(ema_diff);
        }

        return result;
    }
    
    this.build_macd_data = function (data, diff, dea) {
        var result = [];
        
        for (var i = 0, len = data.length; i < len; i++) {
            var macd = 2 * (diff[i] - dea[i]);
            result.push(macd);
        }

        return result;
    }

    return this;
});
