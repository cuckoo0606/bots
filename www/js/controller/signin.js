angular.module('starter.controllers')

.controller('SigninCtrl', function($scope, $rootScope, $http, $state, $timeout, $ionicHistory, $window, 
            UserService, QouteService) {
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
            "username": $scope.username,
            "passwd": $scope.passwd,
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
