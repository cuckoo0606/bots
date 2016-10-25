angular.module('starter.services')

.service('AccountService', function($rootScope, $http, $interval, $filter, UserService, AppConfigService) {
    var service = this;
    this.account = {};
	this.account.Amount=$rootScope.user.amount;
//  this.get_account = function(complete) {
//      var url = AppConfigService.api_url + "account/get";
//      $http.get(url, { 
//          "timeout": 10000, 
//          "params": { "user": UserService.user.Id } 
//      })
//      
//      .success(function(protocol) {
//          if (protocol.return_code === "SUCCESS") {
//              if (complete) {
//                  complete(protocol.data);
//              }
//          }
//      });
//  };
//
//  $interval(function() {
//      if (UserService.user.Id) {
//          service.get_account(function(account) {
//              service.account.Amount = 123;
//              service.account.Profit = account.Profit;
//              service.account.Net = account.Net;
//              service.account.Risk = account.Risk;
//              service.account.RiskString = account.RiskString;
//              service.account.OccupiedMoney = account.OccupiedMoney;
//              service.account.FreeMoney = account.FreeMoney;
//              service.account.FreezingMoney = account.FreezingMoney;
//          });
//      }
//  }, 1000);

    return this;
});
