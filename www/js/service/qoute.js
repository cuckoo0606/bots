angular.module('starter.services')

.service('QouteService', function($http, $interval, $filter, AppConfigService) {
	
    var service = this;
    this.mode = 0;
    this.qoute_list = [];
    this.trade_list = [];
    this.category_list = [];

    this.qoute = function(mode, market, code) {
        var result = $filter('filter')(service.qoute_list, { mode: mode, market: market, code: code });
        if (result.length > 0) {
            return result[0];
        }
        return false;
    };

    this.trade = function(mode, market, code) {
        var result = $filter('filter')(service.trade_list, { mode: mode, market: market, code: code });
        if (result.length > 0) {
            return result[0];
        }
        return false;
    };
    
	this.request_category = function(complete) {
        if (complete) {
            var categorys = [
                { "mode":2, "name": "按需"},
                { "mode":1, "name": "多空"},
            ]

        	service.mode = categorys[0].mode;
            complete(categorys);
        }
    };
    
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

    this.request_trades = function(mode, complete) {
        var tradesurl = AppConfigService.build_api_url("v1/trades");
        $http.get(tradesurl, {
        	"timeout": 10000 ,
        	"params": {"mode": mode}
    	})
        
        .success(function(protocol) {
            if(complete) {
                complete(protocol); 
            }
        });
    }

    this.request_qoute_list = function(mode, complete) {
	   	var codes = service.trade_list.map(function(value) {
            return value.market + ":" + value.code;
       });
        var url = AppConfigService.qoute_url + "last/"+ codes.join("|");
        $http.get(url, { 
        	"timeout": 10000 ,
        	"params": {"mode":mode}
    	})
        
        .success(function(protocol) {
        	console.log(protocol)
            if(complete) {
                complete(protocol);
            }
        });
    }

    this.init = function(complete) {
        while (service.qoute_list.length) {
            service.qoute_list.pop();
        }
        while (service.trade_list.length) {
            service.trade_list.pop();
        }
        while (service.category_list.length) {
            service.category_list.pop();
        }

        this.request_category(function(category_list) {
            angular.forEach(category_list, function(value) {
                service.category_list.push(value);
            });
            if (complete) {
                complete();
            }
        });

        service.category_list.forEach(function(category){
        	service.request_trades(category.mode, function(trades) {
        	    angular.forEach(trades, function(value) {
                    service.trade_list.push(value);
        	    	service.qoute_list.push({
                        "mode": value.mode,
                        "market": value.market,
                        "name": value.name,
                        "code": value.code,
                        "open": 0,
                        "close": 0,
                        "high": 0,
                        "low": 0,
                        "value": 0,
                        "trade": value.trade,
                        "decimal": value.decimal,
                        "change_value": "+0.00",
                        "change_percent": "+0.00%",
                    });
        	    });
        	    service.request_qoute_list(service.mode, function(qoute_list) {
		            angular.forEach(qoute_list, function(qoute) {
		                service.category_list.forEach(function(category) {
		                    var q = service.qoute(category.mode, qoute.market, qoute.code);
		                    if(q) {
		                        if (qoute.value != q.value) {
		                            var sub = q.value - q.open;
		                            var sub_percent = sub / q.open;
		                            if(q.open == 0) {
		                                sub_percent = 0;
		                            }
		                            q.change_value = sub.toFixed(2);
		                            q.change_percent = (sub_percent * 100).toFixed(2) + "%";
		                            if (sub >= 0) {
		                                q.change_value = "+" + q.change_value;
		                                q.change_percent = "+" + q.change_percent;
		                            }
		                        }
		                        if (qoute.value > q.value) {
		                            q.state = "up";
		                        }
		                        else if(qoute.value < q.value) {
		                            q.state = "down";
		                        }
		                        q.open = qoute.open;
		                        q.close = qoute.close;
		                        q.high = qoute.high;
		                        q.low = qoute.low;
		                        q.value = qoute.value;
		                        q.time = qoute.time;
		                    }
		                });
		            });
	            	service.socket = io(AppConfigService.socket_url);
				    service.socket.on('tick', function(data) {
				    	if(data){
				    		if(service.qoute_list){
				    			
				    			service.qoute_list.forEach(function(item){
					    			if(item.code==data.code){
					    				if(item.value < data.value){
					    					item.state = 'up'
					    				}else if(item.value > data.value){
					    					item.state = 'down'
					    				}
					    				item.value = data.value
					    				item.time = $filter('date')(data.time*1000,'yyyy-MM-dd HH:mm:ss')
					    				return item
					    			}
					    		})
				    		}
				    	}
				    });
		        });
            });
        })
        
    };
    return this;
});
