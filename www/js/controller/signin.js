angular.module('starter.controllers')

.controller('SigninCtrl', function($scope, $rootScope, $http, $state, $timeout, $ionicHistory, $window, 
            UserService, QouteService, AppConfigService) {
    $scope.username = $window.localStorage.id;
    $scope.passwd = "";
    $scope.message = "";
    $scope.is_signin = false;

    $scope.spinner = function(visible) {
        if (visible) {
            angular.element(document.querySelectorAll(".spinner-view")).removeClass("hide");
            $timeout(function() {
                angular.element(document.querySelectorAll(".spinner-view")).addClass("open");
            }, 0);
        }
        else {
            angular.element(document.querySelectorAll(".spinner-view")).removeClass("open");
            $timeout(function() {
                angular.element(document.querySelectorAll(".spinner-view")).addClass("hide");
            }, 300);
        }
    }; 

    $scope.signin = function() {
        $scope.is_signin = true;
        $scope.spinner(true);
        UserService.signin({
            "phone": $scope.phone,
            "passwd": $scope.passwd,
            "success": function(status, message, user) {
            	var userUrl=AppConfigService.build_api_url("v1/user")
            	$http.get(userUrl, { 
		            "timeout": 10000,
		            "params": {} 
		        }).success(function(protocol){
		        	$window.localStorage.id = protocol.username;
		        	$rootScope.user = protocol;
		        	$ionicHistory.clearHistory();
					
	                QouteService.init(function() {
	                    $scope.is_signin = false;
	                    $scope.spinner(false);
	                    $state.go("tab.qoute");
	                });
		        })
		        .error(function(protocol) {
		            if (params.error) {
		                params.error("ERROR", "网络错误");
		            }
		        });
            },
            "fail": function(status, message) {
                $scope.message = message;
                $timeout(function() {
                    $scope.message = "";
                    $scope.spinner(false);
                    $scope.is_signin = false;
                }, 2000);
            },
            "error": function(status, message) {
                $scope.message = message;
                $timeout(function() {
                    $scope.message = "";
                    $scope.spinner(false);
                    $scope.is_signin = false;
                }, 2000);
            },
        });
    }
});
