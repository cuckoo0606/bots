angular.module('starter.controllers')

.controller('SigninCtrl', function($scope, $rootScope, $http, $state, $timeout, $ionicHistory, $window, 
            UserService, QouteService, AppConfigService) {
    $scope.phone = $window.localStorage.id;
    $scope.passwd = "";
    $scope.message = "";
    $scope.is_signin = false;
    $scope.show_sign_in_mistake = false;
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
            "success": function(user) {
                $rootScope.user_id = user.user_id;

                //获取系统时间用于计算订单时间
                UserService.request_time(function(time) {
                    var now = new Date().getTime();
                    $rootScope.server_time_tick = time - now;
                });

                UserService.request_user(function(user) {
                    $window.localStorage.id = $scope.phone;
                    $rootScope.user = user;
                    $ionicHistory.clearHistory();

	                QouteService.init(function() {
	                    $scope.is_signin = false;
	                    $scope.spinner(false);
	                    $state.go("tab.qoute");
	                });
                });
            },
            "fail": function(status, message) {
                $scope.message = message;
                $scope.show_sign_in_mistake = true;
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
