angular.module('starter.controllers')

.controller('SignupCtrl', function($scope, $rootScope, $http, $state, $timeout, $ionicHistory, $window, 
            UserService, QouteService, AppConfigService) {
    $scope.username = "";
    $scope.passwd = "";
    $scope.message = "";
    $scope.agree = false;
    $scope.is_signin = false;

    $scope.remote = AppConfigService.remote_list[0];
    $scope.remote_list = AppConfigService.remote_list; 
    $scope.user_category = $scope.remote.user_category[0];
    $scope.user_category_list = $scope.remote.user_category;

    $scope.remote_change = function() {
        AppConfigService.api_url = $scope.remote.url;
        $scope.user_category = $scope.remote.user_category;
    };

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

    $scope.signup = function() {
        $scope.is_signin = true;
        $scope.spinner(true);
        UserService.signup({
            "username": $scope.username,
            "passwd": $scope.passwd,
            "group": $scope.user_category.name,
            "success": function(status, message, user) {
                $rootScope.user = user;
                $window.localStorage.id = user.Id;
                $ionicHistory.clearHistory();

                QouteService.init(function() {
                    $scope.is_signin = false;
                    $scope.spinner(false);
                    $state.go("tab.qoute");
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
