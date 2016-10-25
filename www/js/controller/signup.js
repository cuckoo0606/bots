angular.module('starter.controllers')

.controller('SignupCtrl', function($scope, $rootScope, $http, $state, $timeout, $interval, $ionicHistory, $window, $ionicLoading, $ionicScrollDelegate, 
            UserService, QouteService, SMSService, AppConfigService) {
    $scope.message = "";
    $scope.is_signin = false;
    $scope.show_signup_code = AppConfigService.show_signup_code;
    
    $scope.user = { 
        "username": "",
        "passwd": "",
        "phone": "",
        "agree": true,
        "code": "",
    }

    $scope.sms_remaining = 0;
    $scope.sms_btn_text = "获取验证码";

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
        if ($scope.user.username == "") {
            $ionicLoading.show({ template: "用户名不能为空。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }
        if ($scope.user.passwd == "") {
            $ionicLoading.show({ template: "密码不能为空。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }
        if ($scope.user.passwd != $scope.user.confirm) {
            $ionicLoading.show({ template: "两次输入密码不一致。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }
        if (AppConfigService.show_signup_code && $scope.user.code == "") {
            $ionicLoading.show({ template: "请输入短信验证码。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }
        if ($scope.user.agree == false) {
            $ionicLoading.show({ template: "请阅读并同意协议。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }

        $ionicScrollDelegate.scrollTop(false);
        $scope.is_signin = true;
        $scope.spinner(true);
        UserService.signup({
            "username": $scope.user.username,
            "passwd": $scope.user.passwd,
            "group": $scope.user_category.name,
            "code": $scope.user.code,
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

    $scope.get_verify = function() {
        var pattern = /1\d{10}/;
        if ($scope.user.phone == "" || !pattern.test($scope.user.phone)) {
            $ionicLoading.show({ template: "无效的手机号码。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }

        $ionicLoading.show({ template: "正在获取验证码" });

        SMSService.get_verify({
            "phone": $scope.user.phone,
            "success": function(status, message, user) {
                $ionicLoading.hide();
                $scope.sms_remaining = 60;

                var stop = $interval(function() {
                    if($scope.sms_remaining > 0) {
                        $scope.sms_remaining = $scope.sms_remaining - 1;
                        $scope.sms_btn_text = "重新获取(" + $scope.sms_remaining + ")";
                    }
                    else {
                        $scope.sms_btn_text = "获取验证码";
                        $interval.cancel(stop); 
                    }
                }, 1000);
            },
            "fail": function(status, message) {
                $ionicLoading.show({ template: message });
                $timeout(function() {
                    $ionicLoading.hide();
                }, 3000);
            },
            "error": function(status, message) {
                $ionicLoading.show({ template: message });
                $timeout(function() {
                    $ionicLoading.hide();
                }, 3000);
            },
        });
    }
});
